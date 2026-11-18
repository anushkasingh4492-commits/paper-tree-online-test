import { NextResponse } from "next/server";
import bcrypt from "bcryptjs";
import { requireMasterAdmin } from "@/lib/internal-route";
import { ensureSalesSchema, isSalesPortalHost, salesPortalDisabled } from "@/lib/sales-portal";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function GET(request: Request) {
  if (!isSalesPortalHost(request.headers.get("host"))) return salesPortalDisabled();
  if (!(await requireMasterAdmin())) {
    return NextResponse.json({ success: false, error: "Unauthorized." }, { status: 401 });
  }

  try {
    await ensureSalesSchema();
    const result = await pool.query(`
      SELECT
        u.id, u.name, u.email, u.active, u.created_at,
        COUNT(l.id)::int AS institutes_set_up,
        COUNT(l.id) FILTER (WHERE l.status = 'REJECTED')::int AS rejected,
        COUNT(l.id) FILTER (WHERE l.status = 'FOLLOW_UP')::int AS follow_up,
        COUNT(l.id) FILTER (WHERE l.status = 'INTERESTED')::int AS interested,
        COUNT(l.id) FILTER (WHERE l.status = 'CONVERTED')::int AS converted,
        COALESCE(SUM(l.students_converted) FILTER (WHERE l.status = 'CONVERTED'), 0)::int AS students_converted,
        COALESCE(SUM(l.sale_amount) FILTER (WHERE l.status = 'CONVERTED'), 0)::numeric AS sales_amount,
        (COALESCE(SUM(l.sale_amount) FILTER (WHERE l.status = 'CONVERTED'), 0) * 0.1)::numeric AS commission
      FROM sales_users u
      LEFT JOIN sales_leads l ON l.sales_user_id = u.id
      GROUP BY u.id
      ORDER BY u.created_at DESC
    `);
    return NextResponse.json({ success: true, salesUsers: result.rows });
  } catch (error) {
    console.error("GET SALES TEAM ERROR:", error);
    return NextResponse.json({ success: false, error: "Could not load sales team." }, { status: 500 });
  }
}

export async function POST(request: Request) {
  if (!isSalesPortalHost(request.headers.get("host"))) return salesPortalDisabled();
  if (!(await requireMasterAdmin())) {
    return NextResponse.json({ success: false, error: "Unauthorized." }, { status: 401 });
  }

  try {
    const body = await request.json();
    const name = String(body.name || "").trim();
    const email = String(body.email || "").trim().toLowerCase();
    const password = String(body.password || "");
    if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || password.length < 8) {
      return NextResponse.json(
        { success: false, error: "Enter a name, valid email, and password with at least 8 characters." },
        { status: 400 },
      );
    }

    await ensureSalesSchema();
    const existingAccount = await pool.query(
      `SELECT email FROM admins WHERE LOWER(email) = $1
       UNION ALL
       SELECT email FROM teachers WHERE LOWER(email) = $1
       UNION ALL
       SELECT email FROM students WHERE LOWER(email) = $1
       LIMIT 1`,
      [email],
    );
    if (existingAccount.rowCount) {
      return NextResponse.json(
        { success: false, error: "That email is already used by another account." },
        { status: 409 },
      );
    }
    const passwordHash = await bcrypt.hash(password, 12);
    const result = await pool.query(
      `INSERT INTO sales_users (name, email, password_hash) VALUES ($1, $2, $3)
       RETURNING id, name, email, active, created_at`,
      [name, email, passwordHash],
    );
    return NextResponse.json({ success: true, salesUser: result.rows[0] }, { status: 201 });
  } catch (error) {
    console.error("CREATE SALES USER ERROR:", error);
    const duplicate = error instanceof Error && "code" in error && error.code === "23505";
    return NextResponse.json(
      { success: false, error: duplicate ? "A sales account already uses that email." : "Could not create sales account." },
      { status: duplicate ? 409 : 500 },
    );
  }
}

export async function PATCH(request: Request) {
  if (!isSalesPortalHost(request.headers.get("host"))) return salesPortalDisabled();
  if (!(await requireMasterAdmin())) {
    return NextResponse.json({ success: false, error: "Unauthorized." }, { status: 401 });
  }

  try {
    const body = await request.json();
    const id = String(body.id || "");
    if (!/^[0-9a-f-]{36}$/i.test(id) || typeof body.active !== "boolean") {
      return NextResponse.json({ success: false, error: "A valid account and active state are required." }, { status: 400 });
    }
    await ensureSalesSchema();
    const result = await pool.query(
      `UPDATE sales_users SET active = $1, updated_at = NOW() WHERE id = $2::uuid RETURNING id`,
      [body.active, id],
    );
    if (!result.rowCount) return NextResponse.json({ success: false, error: "Sales account not found." }, { status: 404 });
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("UPDATE SALES USER ERROR:", error);
    return NextResponse.json({ success: false, error: "Could not update sales account." }, { status: 500 });
  }
}
