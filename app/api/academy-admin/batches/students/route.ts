import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";

async function academyIdFromSession() {
  const value = (await cookies()).get("master_session")?.value;
  if (!value) return null;
  try { const session = JSON.parse(decodeURIComponent(value)); return session.role === "ACADEMY_ADMIN" ? session.academyId ?? null : null; } catch { return null; }
}

export async function GET(request: Request) {
  const academyId = await academyIdFromSession();
  const batchId = new URL(request.url).searchParams.get("batchId") ?? "";
  if (!academyId) return NextResponse.json({ success: false, error: "Unauthorized" }, { status: 401 });
  const result = await pool.query(
    `SELECT s.id, s.name, s.email, s.roll_number, s.class_name
     FROM batch_students bs JOIN students s ON s.id = bs.student_id JOIN batches b ON b.id = bs.batch_id
     WHERE bs.batch_id = $1 AND b.academy_id = $2 ORDER BY s.name`, [batchId, academyId]
  );
  return NextResponse.json({ success: true, students: result.rows });
}

export async function POST(request: Request) {
  const academyId = await academyIdFromSession();
  if (!academyId) return NextResponse.json({ success: false, error: "Unauthorized" }, { status: 401 });
  const body = await request.json();
  const batchId = String(body.batchId ?? ""); const studentId = String(body.studentId ?? "");
  const ownership = await pool.query(`SELECT 1 FROM batches b CROSS JOIN students s WHERE b.id=$1 AND s.id=$2 AND b.academy_id=$3 AND s.academy_id=$3`, [batchId, studentId, academyId]);
  if (!ownership.rowCount) return NextResponse.json({ success: false, error: "Batch or student was not found in this academy." }, { status: 404 });
  if (body.action === "remove") await pool.query(`DELETE FROM batch_students WHERE batch_id=$1 AND student_id=$2`, [batchId, studentId]);
  else await pool.query(`INSERT INTO batch_students(batch_id, student_id) VALUES($1,$2) ON CONFLICT DO NOTHING`, [batchId, studentId]);
  return NextResponse.json({ success: true });
}
