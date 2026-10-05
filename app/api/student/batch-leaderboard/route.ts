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
    const academyId = String(session?.academyId ?? "").trim();

    if (!studentId || !academyId) {
      return NextResponse.json({ success: false, error: "Student login required." }, { status: 401 });
    }

    const batchResult = await pool.query(
      `SELECT b.id, b.name
       FROM batch_students bs
       INNER JOIN batches b ON b.id = bs.batch_id
       WHERE bs.student_id = $1 AND b.academy_id = $2
       ORDER BY b.created_at DESC
       LIMIT 1`,
      [studentId, academyId]
    );

    const batch = batchResult.rows[0];
    if (!batch) {
      return NextResponse.json({
        success: true,
        batch: null,
        students: [],
        currentStudent: null,
      });
    }

    // Keep this leaderboard consistent with the batch-rank metric shown on
    // the student dashboard: average percentage across completed attempts.
    const result = await pool.query(
      `WITH scores AS (
         SELECT
           s.id AS student_id,
           COALESCE(NULLIF(TRIM(COALESCE(s.name, '')), ''), 'Student') AS name,
           COALESCE(AVG(
             CASE
               WHEN LOWER(REPLACE(COALESCE(ta.status, ''), '-', '_'))
                    IN ('submitted', 'auto_submitted', 'auto submitted', 'completed', 'complete')
                AND COALESCE(ta.total_marks, 0) > 0
               THEN (ta.score::numeric / ta.total_marks::numeric) * 100
             END
           ), 0) AS avg_pct,
           COUNT(CASE
             WHEN LOWER(REPLACE(COALESCE(ta.status, ''), '-', '_'))
                  IN ('submitted', 'auto_submitted', 'auto submitted', 'completed', 'complete')
             THEN 1 END)::int AS tests_taken,
           COALESCE(SUM(CASE
             WHEN LOWER(REPLACE(COALESCE(ta.status, ''), '-', '_'))
                  IN ('submitted', 'auto_submitted', 'auto submitted', 'completed', 'complete')
             THEN COALESCE(ta.correct_count, 0) + COALESCE(ta.incorrect_count, 0)
                    + COALESCE(ta.unanswered_count, 0)
             ELSE 0 END), 0)::int AS questions_seen
         FROM batch_students bs
         INNER JOIN students s ON s.id = bs.student_id
         LEFT JOIN test_attempts ta ON ta.student_id = s.id
         WHERE bs.batch_id = $1
           AND s.academy_id = $2
         GROUP BY s.id, s.name
       ), ranked AS (
         SELECT *, ROW_NUMBER() OVER (ORDER BY avg_pct DESC, name ASC, student_id ASC) AS rank
         FROM scores
       )
       SELECT * FROM ranked ORDER BY rank ASC, name ASC`,
      [batch.id, academyId]
    );

    const students = result.rows.map((row) => ({
      id: String(row.student_id),
      name: String(row.name),
      average: Number(Number(row.avg_pct ?? 0).toFixed(1)),
      testsTaken: Number(row.tests_taken ?? 0),
      questionsSeen: Number(row.questions_seen ?? 0),
      rank: Number(row.rank ?? 0),
      isCurrent: String(row.student_id) === studentId,
    }));

    const current = students.find((student) => student.isCurrent) ?? null;

    return NextResponse.json({
      success: true,
      batch: {
        id: String(batch.id),
        name: String(batch.name),
        size: students.length,
      },
      students,
      currentStudent: current,
    });
  } catch (error) {
    console.error("BATCH LEADERBOARD ERROR", error);
    return NextResponse.json(
      { success: false, error: error instanceof Error ? error.message : "Could not load batch leaderboard." },
      { status: 500 }
    );
  }
}
