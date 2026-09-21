import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";

async function isMasterAdmin() {
  const value = (await cookies()).get("master_session")?.value;
  if (!value) return false;
  try {
    const session = JSON.parse(decodeURIComponent(value));
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
await pool.query(`
  ALTER TABLE academies
  ADD COLUMN IF NOT EXISTS logo_data TEXT,
  ADD COLUMN IF NOT EXISTS domain VARCHAR(255)
`);
  const body = await request.json();
  const updates: string[] = [];
  const values: unknown[] = [];


  if (body.academyName !== undefined) {
    const name = String(body.academyName).trim();
    if (!name) return NextResponse.json({ success: false, error: "Academy name cannot be empty." }, { status: 400 });
    values.push(name);
    updates.push(`name = $${values.length}`);
  }
  if (body.domain !== undefined) {
  const domain = String(body.domain || "")
    .trim()
    .toLowerCase();

  if (
    domain &&
    !/^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?(?::\d+)?$/.test(domain)
  ) {
    return NextResponse.json(
      {
        success: false,
        error: "Please enter a valid domain.",
      },
      { status: 400 }
    );
  }

  values.push(domain || null);
  updates.push(`domain = $${values.length}`);
}
  if (body.logoData !== undefined) {
    const logoData = String(body.logoData || "");
    if (logoData && (!logoData.startsWith("data:image/") || logoData.length > 2_000_000)) {
      return NextResponse.json({ success: false, error: "Logo must be a valid image smaller than 1.5 MB." }, { status: 400 });
    }
    values.push(logoData || null);
    updates.push(`logo_data = $${values.length}`);
  }

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

export async function DELETE(
  _request: Request,
  { params }: { params: Promise<{ academyId: string }> }
) {
  if (!(await isMasterAdmin())) {
    return NextResponse.json({ success: false, error: "Unauthorized" }, { status: 401 });
  }

  const { academyId } = await params;
  const client = await pool.connect();

  try {
    await client.query("BEGIN");
    const academy = await client.query(`SELECT id FROM academies WHERE id = $1 FOR UPDATE`, [academyId]);
    if (!academy.rowCount) {
      await client.query("ROLLBACK");
      return NextResponse.json({ success: false, error: "Academy not found." }, { status: 404 });
    }

    await client.query(`DELETE FROM notifications WHERE student_id IN (SELECT id::text FROM students WHERE academy_id = $1)`, [academyId]);
    await client.query(`DELETE FROM scheduled_test_students WHERE scheduled_test_id IN (SELECT id FROM scheduled_tests WHERE academy_id = $1) OR student_id IN (SELECT id FROM students WHERE academy_id = $1)`, [academyId]);
    await client.query(`DELETE FROM test_attempts WHERE scheduled_test_id IN (SELECT id FROM scheduled_tests WHERE academy_id = $1) OR student_id IN (SELECT id FROM students WHERE academy_id = $1)`, [academyId]);
    await client.query(`DELETE FROM paper_questions WHERE paper_id IN (SELECT id FROM papers WHERE academy_id = $1)`, [academyId]);
    await client.query(`DELETE FROM scheduled_tests WHERE academy_id = $1`, [academyId]);
    await client.query(`DELETE FROM papers WHERE academy_id = $1`, [academyId]);
    await client.query(`DELETE FROM batch_students WHERE batch_id IN (SELECT id FROM batches WHERE academy_id = $1) OR student_id IN (SELECT id FROM students WHERE academy_id = $1)`, [academyId]);
    await client.query(`DELETE FROM batches WHERE academy_id = $1`, [academyId]);
    await client.query(`DELETE FROM student_credentials WHERE student_id IN (SELECT id FROM students WHERE academy_id = $1)`, [academyId]);
    await client.query(`DELETE FROM students WHERE academy_id = $1`, [academyId]);
    await client.query(`DELETE FROM teachers WHERE academy_id = $1`, [academyId]);
    await client.query(`DELETE FROM admins WHERE academy_id = $1`, [academyId]);
    await client.query(`DELETE FROM academies WHERE id = $1`, [academyId]);
    await client.query("COMMIT");
    return NextResponse.json({ success: true });
  } catch (error) {
    await client.query("ROLLBACK");
    console.error("DELETE ACADEMY ERROR:", error);
    return NextResponse.json({ success: false, error: "Academy could not be deleted." }, { status: 409 });
  } finally {
    client.release();
  }
}