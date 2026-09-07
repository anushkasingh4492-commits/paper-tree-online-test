import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";

async function isMasterAdmin() {
  const value = (await cookies()).get("master_session")?.value;
  if (!value) return false;
  try {
    const session = JSON.parse(value);
    return session.role === "ADMIN" || session.role === "MASTER_ADMIN";
  } catch {
    return false;
  }
}

export async function PATCH(request: Request, { params }: { params: Promise<{ academyId: string }> }) {
  if (!(await isMasterAdmin())) {
    return NextResponse.json({ success: false, error: "Unauthorized" }, { status: 401 });
  }

  const { academyId } = await params;
  const body = await request.json();
  const updates: string[] = [];
  const values: unknown[] = [];

  if (body.status && ["ACTIVE", "SUSPENDED", "RESTRICTED"].includes(body.status)) {
    values.push(body.status);
    updates.push(`status = $${values.length}`);
  }
  if (body.studentLimit !== undefined) {
    const limit = Number(body.studentLimit);
    if (!Number.isInteger(limit) || limit < 1) {
      return NextResponse.json({ success: false, error: "Student limit must be a positive whole number." }, { status: 400 });
    }
    values.push(limit);
    updates.push(`student_limit = $${values.length}`);
  }
  if (body.subscriptionEnd) {
    values.push(String(body.subscriptionEnd));
    updates.push(`subscription_end = $${values.length}`);
  }
  if (!updates.length) {
    return NextResponse.json({ success: false, error: "No valid changes supplied." }, { status: 400 });
  }

  values.push(academyId);
  const result = await pool.query(
    `UPDATE academies SET ${updates.join(", ")}, updated_at = NOW() WHERE id = $${values.length} RETURNING id, status, student_limit, subscription_end`,
    values
  );
  if (!result.rowCount) {
    return NextResponse.json({ success: false, error: "Academy not found." }, { status: 404 });
  }
  return NextResponse.json({ success: true, academy: result.rows[0] });
}