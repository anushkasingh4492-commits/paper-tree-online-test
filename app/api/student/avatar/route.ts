import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const VALID_AVATARS = new Set([
  ...Array.from({ length: 20 }, (_, i) => `girl-${String(i + 1).padStart(2, "0")}`),
  ...Array.from({ length: 20 }, (_, i) => `boy-${String(i + 1).padStart(2, "0")}`),
]);
const VALID_GENDER_PREFERENCES = new Set(["girl", "boy", "prefer_not_to_say"]);

async function getStudent() {
  const raw = (await cookies()).get("student_session")?.value;
  const session = raw ? parseSessionCookie<Record<string, unknown>>(raw) : null;
  const studentId = String(session?.studentId ?? "").trim();
  const academyId = String(session?.academyId ?? "").trim();
  return studentId && academyId ? { studentId, academyId } : null;
}

async function ensureAvatarColumns() {
  await pool.query(`ALTER TABLE students ADD COLUMN IF NOT EXISTS avatar_key VARCHAR(20)`);
  await pool.query(`ALTER TABLE students ADD COLUMN IF NOT EXISTS avatar_gender_preference VARCHAR(24)`);
}

export async function GET() {
  try {
    const student = await getStudent();
    if (!student) return NextResponse.json({ success: false, error: "Student login required." }, { status: 401 });
    await ensureAvatarColumns();
    const result = await pool.query(
      `SELECT avatar_key, avatar_gender_preference FROM students WHERE id::text = $1 AND academy_id::text = $2 LIMIT 1`,
      [student.studentId, student.academyId],
    );
    if (!result.rows.length) return NextResponse.json({ success: false, error: "Student account was not found." }, { status: 404 });
    return NextResponse.json({
      success: true,
      avatarKey: result.rows[0].avatar_key ?? null,
      genderPreference: result.rows[0].avatar_gender_preference ?? null,
    });
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
    await ensureAvatarColumns();

    if (typeof body.genderPreference === "string") {
      const genderPreference = body.genderPreference;
      if (!VALID_GENDER_PREFERENCES.has(genderPreference)) {
        return NextResponse.json({ success: false, error: "Choose one of the available preferences." }, { status: 400 });
      }
      const result = await pool.query(
        `UPDATE students
 SET
   avatar_gender_preference = $1::varchar,
   avatar_key = CASE
     WHEN $1::varchar = 'girl' AND avatar_key LIKE 'boy-%' THEN NULL
     WHEN $1::varchar = 'boy' AND avatar_key LIKE 'girl-%' THEN NULL
     ELSE avatar_key
   END
 WHERE id::text = $2 AND academy_id::text = $3
 RETURNING avatar_gender_preference, avatar_key`,
        [genderPreference, student.studentId, student.academyId],
      );
      if (!result.rows.length) return NextResponse.json({ success: false, error: "Student account was not found." }, { status: 404 });
      return NextResponse.json({ success: true, genderPreference: result.rows[0].avatar_gender_preference, avatarKey: result.rows[0].avatar_key ?? null });
    }

    const avatarKey = typeof body.avatarKey === "string" ? body.avatarKey : "";
    if (!VALID_AVATARS.has(avatarKey)) {
      return NextResponse.json({ success: false, error: "Choose one of the available avatars." }, { status: 400 });
    }
    const result = await pool.query(
      `UPDATE students SET avatar_key = $1 WHERE id::text = $2 AND academy_id::text = $3 RETURNING avatar_key`,
      [avatarKey, student.studentId, student.academyId],
    );
    if (!result.rows.length) return NextResponse.json({ success: false, error: "Student account was not found." }, { status: 404 });
    return NextResponse.json({ success: true, avatarKey: result.rows[0].avatar_key });
  } catch (error) {
    console.error("STUDENT AVATAR UPDATE ERROR", error);
    return NextResponse.json({ success: false, error: "Could not save your avatar." }, { status: 500 });
  }
}
