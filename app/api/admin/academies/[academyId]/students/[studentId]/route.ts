import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";

async function isMasterAdmin() {
  const value = (await cookies()).get("master_session")?.value;
  if (!value) return false;
  try {
    const session = JSON.parse(decodeURIComponent(value));
    return session.role === "ADMIN" || session.role === "MASTER_ADMIN";
  } catch { return false; }
}

export async function PATCH(req: Request, { params }: { params: Promise<{ academyId: string; studentId: string }> }) {
  if (!(await isMasterAdmin())) return NextResponse.json({ success: false, error: "Unauthorized" }, { status: 401 });
  const { academyId, studentId } = await params;
  try {
    const body = await req.json();
    const name = String(body.name || "").trim();
    const email = String(body.email || "").trim().toLowerCase();
    const className = String(body.className || "").trim();
    if (!name || !email || !["Class 11", "Class 12", "Class 11 + 12"].includes(className)) {
      return NextResponse.json({ success: false, error: "Name, email and a valid class are required." }, { status: 400 });
    }
    const duplicate = await pool.query(`SELECT id FROM students WHERE LOWER(email) = $1 AND id <> $2 LIMIT 1`, [email, studentId]);
    if (duplicate.rows.length) return NextResponse.json({ success: false, error: "That email is already in use." }, { status: 409 });
    const result = await pool.query(`UPDATE students SET name=$1,email=$2,class_name=$3 WHERE id=$4 AND academy_id=$5 RETURNING id,name,email,class_name,created_at`, [name,email,className,studentId,academyId]);
    if (!result.rows.length) return NextResponse.json({ success: false, error: "Student not found." }, { status: 404 });
    return NextResponse.json({ success: true, student: result.rows[0] });
  } catch (error) {
    console.error("MASTER STUDENT PATCH ERROR:", error);
    return NextResponse.json({ success: false, error: "Failed to update student." }, { status: 500 });
  }
}

export async function DELETE(_req: Request, { params }: { params: Promise<{ academyId: string; studentId: string }> }) {
  if (!(await isMasterAdmin())) return NextResponse.json({ success: false, error: "Unauthorized" }, { status: 401 });
  const { academyId, studentId } = await params;
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    const student = await client.query(`SELECT id FROM students WHERE id=$1 AND academy_id=$2 LIMIT 1`, [studentId, academyId]);
    if (!student.rows.length) { await client.query("ROLLBACK"); return NextResponse.json({ success: false, error: "Student not found." }, { status: 404 }); }
    await client.query(`DELETE FROM batch_students WHERE student_id=$1`, [studentId]);
    await client.query(`DELETE FROM student_credentials WHERE student_id=$1`, [studentId]);
    await client.query(`DELETE FROM students WHERE id=$1 AND academy_id=$2`, [studentId, academyId]);
    await client.query("COMMIT");
    return NextResponse.json({ success: true });
  } catch (error) {
    await client.query("ROLLBACK");
    console.error("MASTER STUDENT DELETE ERROR:", error);
    return NextResponse.json({ success: false, error: "Student could not be removed. They may have related test records." }, { status: 409 });
  } finally { client.release(); }
}
