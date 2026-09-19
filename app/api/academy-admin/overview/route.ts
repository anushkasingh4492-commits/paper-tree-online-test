import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";

export async function GET() {
  const value = (await cookies()).get("master_session")?.value;
  if (!value) return NextResponse.json({ success: false, error: "Unauthorized" }, { status: 401 });
  let session: { role?: string; academyId?: string; id?: string };
  const parsedSession = parseSessionCookie<typeof session>(value);
  if (!parsedSession) return NextResponse.json({ success: false, error: "Invalid session" }, { status: 401 });
  session = parsedSession;
  if (session.role !== "ACADEMY_ADMIN" || !session.academyId) return NextResponse.json({ success: false, error: "Unauthorized" }, { status: 401 });

  await pool.query("ALTER TABLE academies ADD COLUMN IF NOT EXISTS logo_data TEXT");

  const [academy, counts, batches, tests] = await Promise.all([
    pool.query(`SELECT name, code, logo_data, student_limit, subscription_end, status FROM academies WHERE id = $1`, [session.academyId]),
    pool.query(`SELECT
      (SELECT COUNT(*)::int FROM teachers WHERE academy_id = $1) AS teachers,
      (SELECT COUNT(*)::int FROM students WHERE academy_id = $1) AS students,
      (SELECT COUNT(*)::int FROM batches WHERE academy_id = $1) AS batches,
      (SELECT COUNT(*)::int FROM scheduled_tests WHERE academy_id = $1 AND end_time >= NOW()) AS scheduled_tests`, [session.academyId]),
    pool.query(`SELECT b.id, b.name, b.class_name, COUNT(bs.student_id)::int AS student_count
      FROM batches b LEFT JOIN batch_students bs ON bs.batch_id = b.id
      WHERE b.academy_id = $1 GROUP BY b.id ORDER BY b.name LIMIT 5`, [session.academyId]),
    pool.query(`SELECT st.id, st.title, st.start_time, st.end_time, st.status, b.name AS batch_name
      FROM scheduled_tests st LEFT JOIN batches b ON b.id = st.batch_id
      WHERE st.academy_id = $1 AND st.end_time >= NOW() ORDER BY st.start_time LIMIT 5`, [session.academyId]),
  ]);
  if (!academy.rowCount) return NextResponse.json({ success: false, error: "Academy not found" }, { status: 404 });
  return NextResponse.json({ success: true, academy: academy.rows[0], counts: counts.rows[0], batches: batches.rows, tests: tests.rows });
}
