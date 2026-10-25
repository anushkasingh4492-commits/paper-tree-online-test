import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const raw = (await cookies()).get("student_session")?.value;
    const session = raw ? parseSessionCookie<Record<string, unknown>>(raw) : null;
    const studentId = String(session?.studentId ?? "").trim();

    if (!studentId) {
      return NextResponse.json({ success: false, error: "Student login required." }, { status: 401 });
    }

    const colsResult = await pool.query(
      `SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'test_attempts'`
    );
    const cols = new Set(colsResult.rows.map((r) => String(r.column_name)));
    const pick = (name: string, fallback = "NULL") => cols.has(name) ? `ta.${name}` : fallback;

    const testColsResult = await pool.query(
      `SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'tests'`
    );
    const testCols = new Set(testColsResult.rows.map((r) => String(r.column_name)));
    const testTitle = testCols.has("title") ? "t.title" : testCols.has("name") ? "t.name" : "NULL";
    const testExam = testCols.has("exam") ? "t.exam" : "NULL";

    const query = `
      SELECT
        ${pick("id")} AS attempt_id,
        COALESCE(
          t.id::text,
          NULLIF(${pick("test_id")}::text, ''),
          NULLIF(st.test_id::text, ''),
          NULLIF(${pick("scheduled_test_id")}::text, '')
        ) AS test_id,
        COALESCE(${testTitle}, ${testExam}, 'Practice Test') AS test_title,
        ${testExam} AS test_exam,
        ${pick("score", "0")} AS score,
        ${pick("total_marks", "0")} AS total_marks,
        ${pick("status", "''")} AS status,
        ${pick("started_at")} AS started_at,
        ${pick("submitted_at")} AS submitted_at,
        ${pick("correct_count", "0")} AS correct_count,
        ${pick("incorrect_count", "0")} AS incorrect_count,
        ${pick("unanswered_count", "0")} AS unanswered_count
      FROM test_attempts ta
      LEFT JOIN scheduled_tests st
        ON st.id::text = ${pick("scheduled_test_id")}::text
      LEFT JOIN tests t
        ON t.id::text = COALESCE(
          NULLIF(${pick("test_id")}::text, ''),
          NULLIF(st.test_id::text, ''),
          NULLIF(${pick("scheduled_test_id")}::text, '')
        )
      WHERE ta.student_id::text = $1::text
        AND LOWER(REPLACE(COALESCE(${pick("status", "''")}, ''), '-', '_'))
          IN ('submitted', 'auto_submitted', 'auto submitted', 'completed', 'complete')
      ORDER BY COALESCE(${pick("submitted_at")}, ${pick("started_at")}) DESC NULLS LAST
      LIMIT 100
    `;

    const result = await pool.query(query, [studentId]);
    const tests = result.rows.map((r) => {
      const score = Number(r.score ?? 0);
      const total = Number(r.total_marks ?? 0);
      return {
        attemptId: String(r.attempt_id ?? ""),
        testId: r.test_id == null ? null : String(r.test_id),
        title: String(r.test_title || r.test_exam || "Practice Test"),
        score,
        totalMarks: total,
        percentage: total > 0 ? Number(((score / total) * 100).toFixed(1)) : 0,
        status: String(r.status || "completed"),
        startedAt: r.started_at,
        submittedAt: r.submitted_at,
        correct: Number(r.correct_count ?? 0),
        incorrect: Number(r.incorrect_count ?? 0),
        unanswered: Number(r.unanswered_count ?? 0),
      };
    });

    return NextResponse.json({ success: true, tests });
  } catch (error) {
    console.error("STUDENT TEST HISTORY ERROR", error);
    return NextResponse.json({ success: false, error: error instanceof Error ? error.message : "Could not load past tests." }, { status: 500 });
  }
}
