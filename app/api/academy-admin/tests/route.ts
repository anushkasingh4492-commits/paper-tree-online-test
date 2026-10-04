import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

async function getAcademyAdmin() {
  const cookieStore = await cookies();
  const session = cookieStore.get("master_session");

  if (!session) return null;

  const data = parseSessionCookie<Record<string, unknown>>(session.value);

  if (data) {

    if (data.role !== "ACADEMY_ADMIN" || !data.academyId) {
      return null;
    }

    return data;
  }

  return null;
}

export async function GET() {
  try {
    const admin = await getAcademyAdmin();

    if (!admin) {
      return NextResponse.json(
        { error: "Unauthorized" },
        { status: 401 }
      );
    }

    const result = await pool.query(
      `
      SELECT
        st.id,
        st.paper_id,
        st.batch_id,
        st.title,
        st.start_time,
        st.end_time,
        st.duration_minutes,
        st.status,
        st.created_at,
        b.name AS batch_name,
        (
          SELECT COUNT(*)::int
          FROM batch_students bs
          WHERE bs.batch_id::text = st.batch_id::text
        ) AS assigned_count,
        (
          SELECT COUNT(*)::int
          FROM test_attempts ta
          WHERE ta.scheduled_test_id::text = st.id::text
            AND LOWER(REPLACE(ta.status, '-', ' ')) IN ('submitted', 'auto submitted', 'completed')
        ) AS completed_count,
        (
          SELECT ROUND(AVG(ta.score)::numeric, 2)
          FROM test_attempts ta
          WHERE ta.scheduled_test_id::text = st.id::text
            AND LOWER(REPLACE(ta.status, '-', ' ')) IN ('submitted', 'auto submitted', 'completed')
        ) AS average_score
      FROM scheduled_tests st
      LEFT JOIN batches b
        ON b.id = st.batch_id
      WHERE st.academy_id = $1
      ORDER BY st.start_time DESC
      `,
      [admin.academyId]
    );

    return NextResponse.json({ success: true, tests: result.rows });
  } catch (error) {
    console.error("ACADEMY TEST GET ERROR:", error);

    return NextResponse.json(
      { error: "Failed to fetch scheduled tests" },
      { status: 500 }
    );
  }
}

export async function POST(req: NextRequest) {
  try {
    const admin = await getAcademyAdmin();

    if (!admin) {
      return NextResponse.json(
        { error: "Unauthorized" },
        { status: 401 }
      );
    }

    const body = await req.json();

    const {
      paperId,
      batchId,
      title,
      startTime,
      endTime,
      durationMinutes,
    } = body;

    if (
      !paperId ||
      !batchId ||
      !title ||
      !startTime ||
      !endTime ||
      !durationMinutes
    ) {
      return NextResponse.json(
        { error: "Missing required fields" },
        { status: 400 }
      );
    }

    // Both legacy paper records and teacher-generated tests can be
    // scheduled by an Academy Admin. Generated tests use TEST:<uuid>
    // as their dropdown ID.
    await pool.query(`
      ALTER TABLE scheduled_tests
      ADD COLUMN IF NOT EXISTS test_id UUID
    `);

    await pool.query(`
      ALTER TABLE scheduled_tests
      ALTER COLUMN paper_id DROP NOT NULL
    `);

    await pool.query(`
      ALTER TABLE tests
      ADD COLUMN IF NOT EXISTS academy_id UUID,
      ADD COLUMN IF NOT EXISTS created_by_teacher_id UUID,
      ADD COLUMN IF NOT EXISTS title VARCHAR(255),
      ADD COLUMN IF NOT EXISTS duration_minutes INTEGER
    `);

    // Make sure the batch belongs to this academy
    const batchCheck = await pool.query(
      `
      SELECT id
      FROM batches
      WHERE id = $1
        AND academy_id = $2
      `,
      [batchId, admin.academyId]
    );

    if (batchCheck.rowCount === 0) {
      return NextResponse.json(
        { error: "Batch not found in your academy" },
        { status: 403 }
      );
    }

    let testId = "";
    let scheduledPaperId: string | null = null;
    let exam = "MHT-CET";
    let effectiveDuration = Number(durationMinutes);

    if (String(paperId).startsWith("TEST:")) {
      // Schedule an already-generated teacher test directly.
      const sourceTestId = String(paperId).slice("TEST:".length).trim();

      const testCheck = await pool.query(
        `
        SELECT
          id,
          exam,
          question_count,
          questions,
          duration_minutes,
          title
        FROM tests
        WHERE id::text = $1::text
          AND academy_id::text = $2::text
          AND created_by_teacher_id IS NOT NULL
        LIMIT 1
        `,
        [sourceTestId, admin.academyId]
      );

      if (testCheck.rowCount === 0) {
        return NextResponse.json(
          { error: "Generated test not found in your academy." },
          { status: 403 }
        );
      }

      const source = testCheck.rows[0];
      testId = String(source.id);
      exam = String(source.exam || "MHT-CET");
      effectiveDuration = Number(source.duration_minutes || durationMinutes || 60);
    } else {
      // Legacy paper path.
      const paperCheck = await pool.query(
        `
        SELECT id, exam, duration_minutes
        FROM papers p
        WHERE p.id = $1
          AND (
            p.academy_id = $2
            OR (
              p.academy_id IS NULL
              AND EXISTS (
                SELECT 1 FROM teachers t
                WHERE t.id::text = p.created_by::text
                  AND t.academy_id::text = $2::text
              )
            )
          )
        `,
        [paperId, admin.academyId]
      );

      if (paperCheck.rowCount === 0) {
        return NextResponse.json(
          { error: "Paper not found in your academy" },
          { status: 403 }
        );
      }

      scheduledPaperId = String(paperId);
      exam = String(paperCheck.rows[0]?.exam || "MHT-CET");
      effectiveDuration = Number(paperCheck.rows[0]?.duration_minutes || durationMinutes || 60);

      const paperQuestions = await pool.query(
        `
        SELECT
          q.id,
          q.subject,
          q.chapter_name,
          q.stem,
          q.options,
          q.correct_option,
          q.correct_answer_text,
          q.solution,
          q.difficulty,
          q.question_type,
          q.figure_asset
        FROM paper_questions pq
        INNER JOIN questions q
          ON q.id = pq.question_id
        WHERE pq.paper_id::text = $1::text
        ORDER BY pq.question_order ASC
        `,
        [paperId]
      );

      if (paperQuestions.rows.length === 0) {
        return NextResponse.json(
          { error: "The selected paper has no questions." },
          { status: 409 }
        );
      }

      testId = crypto.randomUUID();

      await pool.query(
        `
        INSERT INTO tests (
          id,
          exam,
          question_count,
          questions,
          created_at,
          difficulty,
          academy_id,
          title,
          duration_minutes
        )
        VALUES (
          $1::uuid,
          $2,
          $3,
          $4::jsonb,
          NOW(),
          $5,
          $6::uuid,
          $7,
          $8
        )
        `,
        [
          testId,
          exam,
          paperQuestions.rows.length,
          JSON.stringify(paperQuestions.rows),
          "Balanced",
          admin.academyId,
          title,
          effectiveDuration,
        ]
      );
    }

    const scheduledTestId = crypto.randomUUID();

    const result = await pool.query(
      `
      INSERT INTO scheduled_tests (
        id,
        test_id,
        paper_id,
        batch_id,
        title,
        start_time,
        end_time,
        duration_minutes,
        status,
        academy_id
      )
      VALUES (
        $1::uuid,
        $2::uuid,
        $3::uuid,
        $4,
        $5,
        $6,
        $7,
        $8,
        'Upcoming',
        $9::uuid
      )
      RETURNING *
      `,
      [
        scheduledTestId,
        testId,
        scheduledPaperId,
        batchId,
        title,
        startTime,
        endTime,
        effectiveDuration,
        admin.academyId,
      ]
    );

    return NextResponse.json(
      { success: true, ...result.rows[0], test_id: testId },
      { status: 201 }
    );
  } catch (error) {
    console.error("ACADEMY TEST POST ERROR:", error);

    return NextResponse.json(
      { error: "Failed to schedule test" },
      { status: 500 }
    );
  }
}

export async function DELETE(req: NextRequest) {
  const admin = await getAcademyAdmin();
  const testId = req.nextUrl.searchParams.get("id") || "";
  if (!admin) return NextResponse.json({ success: false, error: "Unauthorized" }, { status: 401 });
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    const owned = await client.query(`SELECT id FROM scheduled_tests WHERE id=$1 AND academy_id=$2`, [testId, admin.academyId]);
    if (!owned.rowCount) { await client.query("ROLLBACK"); return NextResponse.json({ success: false, error: "Scheduled test not found." }, { status: 404 }); }
    await client.query(`DELETE FROM notifications WHERE scheduled_test_id=$1::text`, [testId]);
    await client.query(`DELETE FROM scheduled_tests WHERE id=$1 AND academy_id=$2`, [testId, admin.academyId]);
    await client.query("COMMIT");
    return NextResponse.json({ success: true });
  } catch (error) { await client.query("ROLLBACK"); return NextResponse.json({ success: false, error: error instanceof Error ? error.message : "Could not cancel scheduled test." }, { status: 500 }); } finally { client.release(); }
}
