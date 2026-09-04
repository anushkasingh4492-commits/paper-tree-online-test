import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

async function getAcademyAdmin() {
  const cookieStore = await cookies();
  const session = cookieStore.get("master_session");

  if (!session) return null;

  try {
    const data = JSON.parse(session.value);

    if (data.role !== "ACADEMY_ADMIN" || !data.academyId) {
      return null;
    }

    return data;
  } catch {
    return null;
  }
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
        b.name AS batch_name
      FROM scheduled_tests st
      LEFT JOIN batches b
        ON b.id = st.batch_id
      WHERE st.academy_id = $1
      ORDER BY st.start_time DESC
      `,
      [admin.academyId]
    );

    return NextResponse.json(result.rows);
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

    // Make sure the paper belongs to this academy
    const paperCheck = await pool.query(
      `
      SELECT id
      FROM papers
      WHERE id = $1
        AND academy_id = $2
      `,
      [paperId, admin.academyId]
    );

    if (paperCheck.rowCount === 0) {
      return NextResponse.json(
        { error: "Paper not found in your academy" },
        { status: 403 }
      );
    }

    const testId = crypto.randomUUID();

    const result = await pool.query(
      `
      INSERT INTO scheduled_tests (
        id,
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
        $1,
        $2,
        $3,
        $4,
        $5,
        $6,
        $7,
        'Upcoming',
        $8
      )
      RETURNING *
      `,
      [
        testId,
        paperId,
        batchId,
        title,
        startTime,
        endTime,
        Number(durationMinutes),
        admin.academyId,
      ]
    );

    return NextResponse.json(result.rows[0], { status: 201 });
  } catch (error) {
    console.error("ACADEMY TEST POST ERROR:", error);

    return NextResponse.json(
      { error: "Failed to schedule test" },
      { status: 500 }
    );
  }
}
