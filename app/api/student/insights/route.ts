import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";
import { getStudentGamification } from "@/lib/gamification";

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

    const data = await getStudentGamification(studentId, academyId);

    const batches = await pool.query(
      `SELECT b.id, b.name
       FROM batch_students bs
       INNER JOIN batches b ON b.id = bs.batch_id
       WHERE bs.student_id = $1 AND b.academy_id = $2
       ORDER BY b.created_at DESC`,
      [studentId, academyId]
    );
    const batch = batches.rows[0];

    let rank: number | null = null;
    let batchSize = 0;

    // The dashboard rank is the student's rank in their latest teacher-assigned
    // test from the selected batch. This is separate from the badge counters:
    // MVP/Podium are awarded once per teacher-assigned test.
    if (batch) {
      const latestAssigned = await pool.query(
        `SELECT ta.scheduled_test_id
         FROM test_attempts ta
         INNER JOIN scheduled_tests st ON st.id = ta.scheduled_test_id
         WHERE ta.student_id = $1
           AND st.batch_id = $2
           AND LOWER(REPLACE(COALESCE(ta.status,''),'-','_')) IN ('submitted','auto_submitted','auto submitted','completed','complete')
         ORDER BY COALESCE(ta.submitted_at, ta.started_at, ta.created_at) DESC
         LIMIT 1`,
        [studentId, batch.id]
      );

      const scheduledTestId = latestAssigned.rows[0]?.scheduled_test_id;
      if (scheduledTestId) {
        const rankResult = await pool.query(
          `WITH participants AS (
             SELECT DISTINCT ON (ta.student_id)
                    ta.student_id,
                    ta.score::numeric AS score,
                    ta.total_marks::numeric AS total_marks
             FROM test_attempts ta
             INNER JOIN scheduled_tests st ON st.id = ta.scheduled_test_id
             INNER JOIN batch_students bs
               ON bs.batch_id = st.batch_id
              AND bs.student_id = ta.student_id
             INNER JOIN students s ON s.id = ta.student_id
             WHERE ta.scheduled_test_id = $1
               AND st.batch_id = $2
               AND s.academy_id = $3
               AND COALESCE(ta.total_marks, 0) > 0
               AND LOWER(REPLACE(COALESCE(ta.status,''),'-','_')) IN ('submitted','auto_submitted','auto submitted','completed','complete')
             ORDER BY ta.student_id, COALESCE(ta.submitted_at, ta.started_at, ta.created_at) DESC
           ), ranked AS (
             SELECT student_id,
                    (score / NULLIF(total_marks, 0)) * 100 AS percentage,
                    RANK() OVER (ORDER BY (score / NULLIF(total_marks, 0)) DESC) AS rank
             FROM participants
           )
           SELECT r.rank, (SELECT COUNT(*) FROM ranked)::int AS batch_size
           FROM ranked r
           WHERE r.student_id = $4`,
          [scheduledTestId, batch.id, academyId, studentId]
        );
        if (rankResult.rows[0]) {
          rank = Number(rankResult.rows[0].rank);
          batchSize = Number(rankResult.rows[0].batch_size);
        }
      }
    }

    return NextResponse.json({
      success: true,
      ...data,
      rank,
      batchSize,
      batchName: batch?.name ?? "",
    });
  } catch (error) {
    console.error("STUDENT INSIGHTS ERROR", error);
    return NextResponse.json({ success: false, error: error instanceof Error ? error.message : "Could not load insights." }, { status: 500 });
  }
}
