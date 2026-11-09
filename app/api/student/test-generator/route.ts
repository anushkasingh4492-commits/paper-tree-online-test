import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

type StudentSession = {
  studentId?: string;
  academyId?: string;
};

function normalizeExam(value: string) {
  const normalized = value.toLowerCase().replace(/[^a-z0-9]/g, "");
  if (normalized.includes("neet")) return "neet";
  if (normalized.includes("mhtcet")) return "mhtcet";
  if (normalized.includes("jee")) return "jee";
  if (normalized.includes("cat")) return "cat";
  return "";
}

export async function GET() {
  try {
    const raw = (await cookies()).get("student_session")?.value;
    const session = raw ? parseSessionCookie<StudentSession>(raw) : null;
    const studentId = String(session?.studentId ?? "").trim();
    const academyId = String(session?.academyId ?? "").trim();

    if (!studentId || !academyId) {
      return NextResponse.json(
        { success: false, error: "Student login required." },
        { status: 401 }
      );
    }

    const assignment = await pool.query(
      `SELECT b.course_name
       FROM batch_students bs
       INNER JOIN batches b ON b.id = bs.batch_id
       WHERE bs.student_id = $1 AND b.academy_id = $2
         AND NULLIF(TRIM(COALESCE(b.course_name, '')), '') IS NOT NULL
       ORDER BY b.created_at DESC
       LIMIT 1`,
      [studentId, academyId]
    );
    const course = String(assignment.rows[0]?.course_name ?? "").trim();
    const exam = normalizeExam(course);

    if (!course || !exam) {
      return NextResponse.json(
        { success: false, error: "Your assigned course does not have a supported test question bank." },
        { status: 400 }
      );
    }

    const result = await pool.query(
      `SELECT subject, chapter_name, COUNT(*)::int AS question_count
       FROM questions
       WHERE REGEXP_REPLACE(LOWER(TRIM(exam)), '[^a-z0-9]', '', 'g') = $1
         AND NULLIF(TRIM(COALESCE(subject, '')), '') IS NOT NULL
         AND NULLIF(TRIM(COALESCE(chapter_name, '')), '') IS NOT NULL
       GROUP BY subject, chapter_name
       ORDER BY subject, chapter_name`,
      [exam]
    );
    const chapters = result.rows.map((row) => ({
      subject: String(row.subject),
      chapter: String(row.chapter_name),
      questionCount: Number(row.question_count),
    }));

    return NextResponse.json({ success: true, course, exam, chapters });
  } catch (error) {
    console.error("STUDENT TEST GENERATOR DATA ERROR", error);
    return NextResponse.json(
      { success: false, error: error instanceof Error ? error.message : "Could not load test generator data." },
      { status: 500 }
    );
  }
}
