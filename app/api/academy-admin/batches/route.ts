import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { randomUUID } from "crypto";
import { pool } from "@/lib/db";

async function getAcademyAdmin() {
  const cookieStore = await cookies();
  const session = cookieStore.get("master_session")?.value;

  if (!session) return null;

  try {
    const data = JSON.parse(session);

    if (data.role !== "ACADEMY_ADMIN" || !data.academyId) {
      return null;
    }

    return data;
  } catch {
    return null;
  }
}

export async function GET() {
  const admin = await getAcademyAdmin();

  if (!admin) {
    return NextResponse.json(
      { success: false, error: "Unauthorized" },
      { status: 401 }
    );
  }

  try {
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

    CASE
      WHEN st.batch_id IS NOT NULL THEN 'batch'
      ELSE 'student'
    END AS target_type,

    COALESCE(
      (
        SELECT COUNT(*)::int
        FROM scheduled_test_students sts
        WHERE sts.scheduled_test_id = st.id
      ),
      0
    ) AS assigned_student_count

  FROM scheduled_tests st

  LEFT JOIN batches b
    ON b.id = st.batch_id

  WHERE st.academy_id = $1

  ORDER BY st.start_time DESC
  `,
  [admin.academyId]
);
    return NextResponse.json({
      success: true,
      batches: result.rows,
    });
  } catch (error) {
    console.error("ACADEMY BATCH GET ERROR:", error);

    return NextResponse.json(
      { success: false, error: "Failed to load batches" },
      { status: 500 }
    );
  }
}

export async function POST(req: Request) {
  const admin = await getAcademyAdmin();

  if (!admin) {
    return NextResponse.json(
      { success: false, error: "Unauthorized" },
      { status: 401 }
    );
  }

  try {
    const body = await req.json();

    const name = String(body.name || "").trim();
    const className = String(body.className || "").trim();

    if (!name) {
      return NextResponse.json(
        { success: false, error: "Batch name is required" },
        { status: 400 }
      );
    }

    const batchId = randomUUID();

    await pool.query(
      `
      INSERT INTO batches
        (
          id,
          name,
          class_name,
          created_by,
          academy_id
        )
      VALUES
        ($1, $2, $3, $4, $5)
      `,
      [
        batchId,
        name,
        className || null,
        null,
admin.academyId,
      ]
    );

    return NextResponse.json({
      success: true,
      batch: {
        id: batchId,
        name,
        className,
      },
    });
  } catch (error) {
    console.error("ACADEMY BATCH POST ERROR:", error);

    return NextResponse.json(
      { success: false, error: "Failed to create batch" },
      { status: 500 }
    );
  }
}