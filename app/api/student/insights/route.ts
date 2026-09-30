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
    if (batch) {
      const rankResult = await pool.query(
        `WITH scores AS (
           SELECT s.id AS student_id,
                  COALESCE(AVG(CASE WHEN LOWER(REPLACE(COALESCE(ta.status,''),'-','_')) IN ('submitted','auto_submitted','auto submitted','completed','complete')
                    AND COALESCE(ta.total_marks,0) > 0
                    THEN (ta.score::numeric / ta.total_marks::numeric) * 100 END), 0) AS avg_pct
           FROM batch_students bs2
           INNER JOIN students s ON s.id = bs2.student_id
           LEFT JOIN test_attempts ta ON ta.student_id = s.id
           WHERE bs2.batch_id = $1 AND s.academy_id = $3
           GROUP BY s.id
         ), ranked AS (
           SELECT *, RANK() OVER (ORDER BY avg_pct DESC) AS rank
           FROM scores
         )
         SELECT *, (SELECT COUNT(*) FROM ranked)::int AS batch_size
         FROM ranked WHERE student_id = $2`,
        [batch.id, studentId, academyId]
      );
      if (rankResult.rows[0]) {
        rank = Number(rankResult.rows[0].rank);
        batchSize = Number(rankResult.rows[0].batch_size);
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
