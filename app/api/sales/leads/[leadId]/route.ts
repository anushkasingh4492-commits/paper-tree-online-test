import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";
import { ensureSalesSchema, isSalesLeadStatus, isSalesPortalHost, salesPortalDisabled } from "@/lib/sales-portal";

export const runtime = "nodejs";
type Context = { params: Promise<{ leadId: string }> };

export async function PATCH(request: Request, context: Context) {
  if (!isSalesPortalHost(request.headers.get("host"))) return salesPortalDisabled();
  const cookieStore = await cookies();
  const salesValue = cookieStore.get("sales_session")?.value;
  const sales = salesValue ? parseSessionCookie<{ id?: string; role?: string }>(salesValue) : null;
  const masterValue = cookieStore.get("master_session")?.value;
  const master = masterValue ? parseSessionCookie<{ role?: string }>(masterValue) : null;
  const isAdmin = master?.role === "ADMIN" || master?.role === "MASTER_ADMIN";
  if (!(sales?.role === "SALES" && sales.id) && !isAdmin) {
    return NextResponse.json({ success: false, error: "Unauthorized." }, { status: 401 });
  }

  try {
    await ensureSalesSchema();
    if (!isAdmin) {
      const activeUser = await pool.query(
        "SELECT id FROM sales_users WHERE id = $1::uuid AND active = TRUE",
        [sales!.id],
      );
      if (!activeUser.rowCount) return NextResponse.json({ success: false, error: "Sales account is inactive." }, { status: 403 });
    }
    const { leadId } = await context.params;
    const body = await request.json();
    const status = body.status;
    if (!isSalesLeadStatus(status)) {
      return NextResponse.json({ success: false, error: "Invalid institute status." }, { status: 400 });
    }
    const students = Number(body.studentsConverted ?? 0);
    const saleAmount = Number(body.saleAmount ?? 0);
    if (!Number.isInteger(students) || students < 0 || !Number.isFinite(saleAmount) || saleAmount < 0) {
      return NextResponse.json({ success: false, error: "Student count and sale amount must be non-negative values." }, { status: 400 });
    }
    const followUpAt = body.followUpAt ? String(body.followUpAt) : null;
    if (followUpAt) {
      const parsedDate = new Date(`${followUpAt}T00:00:00.000Z`);
      if (!/^\d{4}-\d{2}-\d{2}$/.test(followUpAt) || Number.isNaN(parsedDate.getTime()) || parsedDate.toISOString().slice(0, 10) !== followUpAt) {
        return NextResponse.json({ success: false, error: "Follow-up date must be a valid date." }, { status: 400 });
      }
    }

    const result = await pool.query(
      `UPDATE sales_leads
       SET status = $1,
           follow_up_at = $2::date,
           students_converted = CASE WHEN $1 = 'CONVERTED' THEN $3 ELSE 0 END,
           sale_amount = CASE WHEN $1 = 'CONVERTED' THEN $4 ELSE 0 END,
           updated_at = NOW()
       WHERE id = $5::uuid AND ($6::uuid IS NULL OR sales_user_id = $6)
       RETURNING id, institute_name, contact_name, email, phone, status, follow_up_at,
                 students_converted, sale_amount, notes, created_at,
                 (sale_amount * 0.1)::numeric AS commission`,
      [status, followUpAt, students, saleAmount, leadId, isAdmin ? null : sales!.id],
    );
    if (!result.rowCount) return NextResponse.json({ success: false, error: "Institute demo not found." }, { status: 404 });
    return NextResponse.json({ success: true, lead: result.rows[0] });
  } catch (error) {
    console.error("UPDATE SALES LEAD ERROR:", error);
    return NextResponse.json({ success: false, error: "Could not update institute status." }, { status: 500 });
  }
}
