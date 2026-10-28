import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
const VALID_AVATARS = new Set(Array.from({ length: 40 }, (_, i) => `${i < 20 ? "girl" : "boy"}-${String((i % 20) + 1).padStart(2, "0")}`));

async function getStudent() {
  const raw = (await cookies()).get("student_session")?.value;
  const session = raw ? parseSessionCookie<Record<string, unknown>>(raw) : null;
  const studentId = String(session?.studentId ?? "").trim();
  const academyId = String(session?.academyId ?? "").trim();
  return studentId && academyId ? { studentId, academyId } : null;
}
async function ensureAvatarColumn() {
  await pool.query(`ALTER TABLE students ADD COLUMN IF NOT EXISTS avatar_key VARCHAR(20)`);
}
export async function GET() {
  try {
    const student = await getStudent();
    if (!student) return NextResponse.json({ success: false, error: "Student login required." }, { status: 401 });
    await ensureAvatarColumn();
    const result = await pool.query(`SELECT avatar_key FROM students WHERE id::text = $1 AND academy_id::text = $2 LIMIT 1`, [student.studentId, student.academyId]);
    if (!result.rows.length) return NextResponse.json({ success: false, error: "Student account was not found." }, { status: 404 });
    return NextResponse.json({ success: true, avatarKey: result.rows[0].avatar_key ?? null });
  } catch (error) {
    console.error("STUDENT AVATAR GET ERROR", error);
    return NextResponse.json({ success: false, error: "Could not load your avatar." }, { status: 500 });
  }
}
export async function PATCH(request: Request) {
  try {
    const student = await getStudent();
    if (!student) return NextResponse.json({ success: false, error: "Student login required." }, { status: 401 });
    const body = await request.json();
    const avatarKey = typeof body.avatarKey === "string" ? body.avatarKey : "";
    if (!VALID_AVATARS.has(avatarKey)) return NextResponse.json({ success: false, error: "Choose one of the available avatars." }, { status: 400 });
    await ensureAvatarColumn();
    const result = await pool.query(`UPDATE students SET avatar_key = $1 WHERE id::text = $2 AND academy_id::text = $3 RETURNING avatar_key`, [avatarKey, student.studentId, student.academyId]);
    if (!result.rows.length) return NextResponse.json({ success: false, error: "Student account was not found." }, { status: 404 });
    return NextResponse.json({ success: true, avatarKey: result.rows[0].avatar_key });
  } catch (error) {
    console.error("STUDENT AVATAR UPDATE ERROR", error);
    return NextResponse.json({ success: false, error: "Could not save your avatar." }, { status: 500 });
  }
}
