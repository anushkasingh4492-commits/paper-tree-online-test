import { NextRequest, NextResponse } from "next/server";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

function readStudentSession(value: string) {
  try {
    const parsed = JSON.parse(decodeURIComponent(value));

    return {
      studentId: String(parsed?.studentId ?? "").trim(),
      academyId: String(parsed?.academyId ?? "").trim(),
    };
  } catch {
    return {
      studentId: value.trim(),
      academyId: "",
    };
  }
}

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ scheduledTestId: string }> }
) {
  const client = await pool.connect();

  try {
    const { scheduledTestId } = await params;
    const sessionCookie = request.cookies.get("student_session")?.value;

    if (!sessionCookie) {
      return NextResponse.json(
        { success: false, error: "Student session not found." },
        { status: 401 }
      );
    }

    const { studentId, academyId } = readStudentSession(sessionCookie);

    if (!studentId || !academyId) {
      return NextResponse.json(
        { success: false, error: "Invalid student session." },
        { status: 401 }
      );
    }

    await client.query(`
      ALTER TABLE scheduled_tests
      ADD COLUMN IF NOT EXISTS test_id UUID
    `);

    const result = await client.query(
      `
      SELECT
        st.id,
        st.test_id,
        st.title,
        st.start_time,
        st.end_time,
        st.duration_minutes,
        p.exam,
        p.description,
        p.code,
        p.id AS paper_id
      FROM scheduled_tests st
      LEFT JOIN papers p
        ON p.id::text = st.paper_id::text
      WHERE st.id::text = $1::text
        AND st.academy_id::text = $2::text
        AND (
          (
            st.batch_id IS NOT NULL
            AND EXISTS (
              SELECT 1
              FROM batch_students bs
              WHERE bs.batch_id::text = st.batch_id::text
                AND bs.student_id::text = $3::text
            )
          )
          OR (
            st.batch_id IS NULL
            AND EXISTS (
              SELECT 1
              FROM scheduled_test_students sts
              WHERE sts.scheduled_test_id::text = st.id::text
                AND sts.student_id::text = $3::text
            )
          )
        )
      LIMIT 1
      `,
      [scheduledTestId, academyId, studentId]
    );

    if (result.rows.length === 0) {
      return NextResponse.json(
        { success: false, error: "Scheduled test not found." },
        { status: 404 }
      );
    }

    const scheduled = result.rows[0];
    const now = Date.now();
    const start = new Date(scheduled.start_time).getTime();
    const end = new Date(scheduled.end_time).getTime();

    if (!Number.isFinite(start) || !Number.isFinite(end)) {
      return NextResponse.json(
        { success: false, error: "This test has an invalid schedule." },
        { status: 500 }
      );
    }

    if (now < start) {
      return NextResponse.json(
        { success: false, error: "This test has not started yet." },
        { status: 403 }
      );
    }

    if (now >= end) {
      return NextResponse.json(
        { success: false, error: "This test has ended." },
        { status: 403 }
      );
    }

    if (!scheduled.test_id) {
      return NextResponse.json(
        { success: false, error: "This scheduled test has no paper attached." },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      testId: String(scheduled.test_id),
      scheduledTestId: String(scheduled.id),
      paperId: scheduled.paper_id ? String(scheduled.paper_id) : null,
      title: String(scheduled.title ?? scheduled.description ?? scheduled.code ?? "Scheduled Test"),
      exam: String(scheduled.exam ?? "MHT-CET"),
      duration: Number(scheduled.duration_minutes ?? 0),
      startTime: scheduled.start_time,
      endTime: scheduled.end_time,
    });
  } catch (error) {
    console.error("START SCHEDULED TEST ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error: error instanceof Error ? error.message : "Could not start scheduled test.",
      },
      { status: 500 }
    );
  } finally {
    client.release();
  }
}
