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
    const testQuestionCount = testCols.has("question_count") ? "t.question_count" : "NULL";
    const testQuestions = testCols.has("questions") ? "t.questions" : "'[]'::jsonb";

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
        ${testQuestionCount} AS question_count,
        ${pick("score", "0")} AS score,
        ${pick("total_marks", "0")} AS total_marks,
        ${pick("status", "''")} AS status,
        ${pick("started_at")} AS started_at,
        ${pick("submitted_at")} AS submitted_at,
        CASE
          WHEN COALESCE(answer_counts.attempted_count, 0) > 0
          THEN COALESCE(answer_counts.correct_count, 0)
          ELSE ${pick("correct_count", "0")}
        END::int AS correct_count,
        CASE
          WHEN COALESCE(answer_counts.attempted_count, 0) > 0
          THEN GREATEST(answer_counts.attempted_count - answer_counts.correct_count, 0)
          ELSE ${pick("incorrect_count", "0")}
        END::int AS incorrect_count,
        ${pick("unanswered_count", "0")} AS unanswered_count
      FROM test_attempts ta
      LEFT JOIN LATERAL (
        SELECT
          COUNT(DISTINCT answer.question_id) FILTER (
            WHERE answer.selected_answer IS NOT NULL
              AND answer.selected_answer::text <> ''
          )::int AS attempted_count,
          COUNT(DISTINCT answer.question_id) FILTER (
            WHERE answer.selected_answer IS NOT NULL
              AND answer.selected_answer::text <> ''
              AND answer.is_correct = TRUE
          )::int AS correct_count
        FROM test_answers answer
        WHERE answer.attempt_id::text = ${pick("id")}::text
      ) answer_counts ON TRUE
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
        AND COALESCE(
          NULLIF(${testQuestionCount}, 0),
          CASE
            WHEN jsonb_typeof(${testQuestions}) = 'array'
            THEN jsonb_array_length(${testQuestions})
          END,
          NULLIF(
            COALESCE(${pick("correct_count", "0")}, 0) +
            COALESCE(${pick("incorrect_count", "0")}, 0) +
            COALESCE(${pick("unanswered_count", "0")}, 0),
            0
          ),
          2
        ) <> 1
      ORDER BY COALESCE(${pick("submitted_at")}, ${pick("started_at")}) DESC NULLS LAST
      LIMIT 100
    `;

    const result = await pool.query(query, [studentId]);
    const tests = result.rows.map((r) => {
      const score = Number(r.score ?? 0);
      const total = Number(r.total_marks ?? 0);
      const correct = Number(r.correct_count ?? 0);
      const incorrect = Number(r.incorrect_count ?? 0);
      const questionCount = Number(r.question_count ?? 0);
      return {
        attemptId: String(r.attempt_id ?? ""),
        testId: r.test_id == null ? null : String(r.test_id),
        title: String(r.test_title || r.test_exam || "Practice Test"),
        score,
        totalMarks: total,
        percentage: total > 0 ? Number(((score / total) * 100).toFixed(1)) : 0,
        questionCount,
        status: String(r.status || "completed"),
        startedAt: r.started_at,
        submittedAt: r.submitted_at,
        correct,
        incorrect,
        unanswered: questionCount > 0
          ? Math.max(0, questionCount - correct - incorrect)
          : Number(r.unanswered_count ?? 0),
      };
    });

    return NextResponse.json({ success: true, tests });
  } catch (error) {
    console.error("STUDENT TEST HISTORY ERROR", error);
    return NextResponse.json({ success: false, error: error instanceof Error ? error.message : "Could not load past tests." }, { status: 500 });
  }
}
