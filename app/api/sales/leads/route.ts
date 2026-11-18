import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";
import { ensureSalesSchema, isSalesPortalHost, salesPortalDisabled } from "@/lib/sales-portal";

export const runtime = "nodejs";

async function getActor() {
  const cookieStore = await cookies();
  const masterRaw = cookieStore.get("master_session")?.value;
  const master = masterRaw
    ? parseSessionCookie<{ role?: string }>(masterRaw)
    : null;
  if (master?.role === "ADMIN" || master?.role === "MASTER_ADMIN") return { id: null, isAdmin: true };

  const salesRaw = cookieStore.get("sales_session")?.value;
  const sales = salesRaw
    ? parseSessionCookie<{ id?: string; role?: string }>(salesRaw)
    : null;
  if (sales?.role === "SALES" && sales.id) return { id: sales.id, isAdmin: false };
  return null;
}

export async function GET(request: Request) {
  if (!isSalesPortalHost(request.headers.get("host"))) return salesPortalDisabled();
  const actor = await getActor();
  if (!actor) return NextResponse.json({ success: false, error: "Unauthorized." }, { status: 401 });

  try {
    await ensureSalesSchema();
    if (!actor.isAdmin) {
      const activeUser = await pool.query(
        "SELECT id FROM sales_users WHERE id = $1::uuid AND active = TRUE",
        [actor.id],
      );
      if (!activeUser.rowCount) return NextResponse.json({ success: false, error: "Sales account is inactive." }, { status: 403 });
    }
    const result = await pool.query(
      `SELECT l.id, l.institute_name, l.contact_name, l.email, l.phone, l.status,
              l.follow_up_at, l.students_converted, l.sale_amount, l.notes, l.created_at,
              u.name AS sales_person,
              (l.sale_amount * 0.1)::numeric AS commission
       FROM sales_leads l
       JOIN sales_users u ON u.id = l.sales_user_id
       WHERE ($1::uuid IS NULL OR l.sales_user_id = $1)
       ORDER BY l.created_at DESC`,
      [actor.id],
    );
    return NextResponse.json({ success: true, leads: result.rows });
  } catch (error) {
    console.error("GET SALES LEADS ERROR:", error);
    return NextResponse.json({ success: false, error: "Could not load institute demos." }, { status: 500 });
  }
}

export async function POST(request: Request) {
  if (!isSalesPortalHost(request.headers.get("host"))) return salesPortalDisabled();
  const actor = await getActor();
  if (!actor || actor.isAdmin || !actor.id) {
    return NextResponse.json({ success: false, error: "Sales team login required." }, { status: 401 });
  }

  try {
    await ensureSalesSchema();
    const activeUser = await pool.query(
      "SELECT id FROM sales_users WHERE id = $1::uuid AND active = TRUE",
      [actor.id],
    );
    if (!activeUser.rowCount) return NextResponse.json({ success: false, error: "Sales account is inactive." }, { status: 403 });
    const body = await request.json();
    const instituteName = String(body.instituteName || "").trim();
    const contactName = String(body.contactName || "").trim();
    const email = String(body.email || "").trim().toLowerCase() || null;
    const phone = String(body.phone || "").trim() || null;
    const notes = String(body.notes || "").trim() || null;
    if (!instituteName || !contactName || instituteName.length > 255 || contactName.length > 150) {
      return NextResponse.json({ success: false, error: "Institute and contact names are required." }, { status: 400 });
    }
    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return NextResponse.json({ success: false, error: "Enter a valid contact email." }, { status: 400 });
    }

    const result = await pool.query(
      `INSERT INTO sales_leads (institute_name, contact_name, email, phone, notes, sales_user_id)
       VALUES ($1, $2, $3, $4, $5, $6)
       RETURNING id, institute_name, contact_name, email, phone, status, follow_up_at,
                 students_converted, sale_amount, notes, created_at`,
      [instituteName, contactName, email, phone, notes, actor.id],
    );
    return NextResponse.json({ success: true, lead: result.rows[0] }, { status: 201 });
  } catch (error) {
    console.error("CREATE SALES LEAD ERROR:", error);
    return NextResponse.json({ success: false, error: "Could not save institute demo." }, { status: 500 });
  }
}
