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
    const totalStudents = Number(body.totalStudents);
    const proposedSellingPrice = Number(body.proposedSellingPrice);
    const reaction = String(body.reaction || "").toUpperCase();
    if (
      !Number.isInteger(totalStudents) ||
      totalStudents < 0 ||
      !Number.isFinite(proposedSellingPrice) ||
      proposedSellingPrice < 0 ||
      !["HOT", "WARM", "COLD", "REJECTED"].includes(reaction)
    ) {
      return NextResponse.json({ success: false, error: "Enter a valid student count, proposed selling price, and reaction." }, { status: 400 });
    }
    const followUpAt = body.followUpAt ? String(body.followUpAt) : null;
    if (followUpAt) {
      const parsedDate = new Date(`${followUpAt}T00:00:00.000Z`);
      if (!/^\d{4}-\d{2}-\d{2}$/.test(followUpAt) || Number.isNaN(parsedDate.getTime()) || parsedDate.toISOString().slice(0, 10) !== followUpAt) {
        return NextResponse.json({ success: false, error: "Follow-up date must be a valid date." }, { status: 400 });
      }
    }

    const client = await pool.connect();
    try {
      await client.query("BEGIN");
      const result = await client.query(
        `UPDATE sales_leads
         SET status = $1,
             follow_up_at = $2::date,
             reaction = $3,
             total_students = $4,
             students_converted = CASE WHEN $1 = 'CONVERTED' THEN $4 ELSE 0 END,
             proposed_selling_price = $5,
             sale_amount = $4 * $5,
             updated_at = NOW()
         WHERE id = $6::uuid AND ($7::uuid IS NULL OR sales_user_id = $7)
         RETURNING id, academy_id, institute_name, contact_name, alternate_contact_numbers,
                   status, reaction, follow_up_at, total_students, proposed_selling_price,
                   sale_amount, notes, created_at, sales_user_id`,
        [status, followUpAt, reaction, totalStudents, proposedSellingPrice, leadId, isAdmin ? null : sales!.id],
      );
      if (!result.rowCount) {
        await client.query("ROLLBACK");
        return NextResponse.json({ success: false, error: "Institute demo not found." }, { status: 404 });
      }
      if (result.rows[0].academy_id) {
        await client.query(
          "UPDATE academies SET student_limit = $1 WHERE id = $2",
          [totalStudents, result.rows[0].academy_id],
        );
      }
      await client.query("COMMIT");
      const commissionResult = await client.query(
        "SELECT commission_percentage FROM sales_users WHERE id = $1",
        [result.rows[0].sales_user_id],
      );
      const commission = status === "CONVERTED"
        ? Number(result.rows[0].sale_amount || 0) * Number(commissionResult.rows[0]?.commission_percentage || 0) / 100
        : 0;
      return NextResponse.json({
        success: true,
        lead: { ...result.rows[0], commission },
      });
    } catch (error) {
      await client.query("ROLLBACK");
      throw error;
    } finally {
      client.release();
    }
  } catch (error) {
    console.error("UPDATE SALES LEAD ERROR:", error);
    return NextResponse.json({ success: false, error: "Could not update institute status." }, { status: 500 });
  }
}
