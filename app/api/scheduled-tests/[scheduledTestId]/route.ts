import { NextRequest, NextResponse } from "next/server";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function GET(
  request: NextRequest,
  {
    params,
  }: {
    params: Promise<{
      scheduledTestId: string;
    }>;
  }
) {
  const client = await pool.connect();

  try {
    const { scheduledTestId } = await params;

    const sessionCookie =
      request.cookies.get("student_session")?.value;

    if (!sessionCookie) {
      return NextResponse.json(
        {
          success: false,
          error: "Student session not found.",
        },
        { status: 401 }
      );
    }

    let studentId = "";

    try {
      const parsed = JSON.parse(sessionCookie);

      if (parsed?.studentId) {
        studentId = String(parsed.studentId);
      }
    } catch {
      studentId = sessionCookie;
    }

    studentId = studentId.trim();

    if (!studentId) {
      return NextResponse.json(
        {
          success: false,
          error: "Invalid student session.",
        },
        { status: 401 }
      );
    }

    /*
     * Get scheduled test + paper.
     *
     * The current project stores the scheduled test's
     * paper in scheduled_tests.paper_id.
     */

    const scheduledResult = await client.query(
      `
      SELECT
        st.id,
        st.paper_id,
        st.batch_id,
        st.title,
        st.start_time,
        st.end_time,
        st.duration_minutes,
        st.status AS scheduled_status,

        p.exam AS paper_exam,
        p.description AS paper_description,
        p.code AS paper_code,
        p.duration_minutes AS paper_duration

      FROM scheduled_tests st

      LEFT JOIN papers p
        ON p.id = st.paper_id

     WHERE st.id = $1
  AND (
    (
      st.batch_id IS NOT NULL
      AND EXISTS (
        SELECT 1
        FROM batch_students bs
        WHERE bs.batch_id = st.batch_id
          AND bs.student_id = $2
      )
    )
    OR
    (
      st.batch_id IS NULL
      AND EXISTS (
        SELECT 1
        FROM scheduled_test_students sts
        WHERE sts.scheduled_test_id = st.id
          AND sts.student_id = $2
      )
    )
  )

      LIMIT 1
      `,
      [scheduledTestId, studentId]
    );

    if (scheduledResult.rows.length === 0) {
      return NextResponse.json(
        {
          success: false,
          error: "Scheduled test not found.",
        },
        { status: 404 }
      );
    }

    const scheduled = scheduledResult.rows[0];

    /*
     * Get questions belonging to the paper.
     *
     * Your question data uses subject and chapter_name.
     */

    const questionsResult = await client.query(
      `
      SELECT
        q.id,
        q.subject,
        q.chapter_name
      FROM paper_questions pq
      INNER JOIN questions q
        ON q.id = pq.question_id
      WHERE pq.paper_id = $1
      ORDER BY pq.id ASC
      `,
      [scheduled.paper_id]
    );

    const questions = questionsResult.rows;

    const subjects = Array.from(
      new Set(
        questions
          .map((q: any) =>
            String(q.subject ?? "").trim()
          )
          .filter(Boolean)
      )
    );

    const chapters = Array.from(
      new Set(
        questions
          .map((q: any) =>
            String(q.chapter_name ?? "").trim()
          )
          .filter(Boolean)
      )
    );

    return NextResponse.json({
      success: true,

      test: {
        id: String(scheduled.id),

        scheduledTestId:
          String(scheduled.id),

        paperId:
          scheduled.paper_id
            ? String(scheduled.paper_id)
            : null,

        batchId:
          scheduled.batch_id
            ? String(scheduled.batch_id)
            : null,

        title:
          String(
            scheduled.title ??
              scheduled.paper_code ??
              "Scheduled Test"
          ),

        exam:
          String(
            scheduled.paper_exam ??
              "MHT-CET"
          ),

        description:
          String(
            scheduled.paper_description ??
              ""
          ),

        startTime:
          scheduled.start_time,

        endTime:
          scheduled.end_time,

        durationMinutes:
          Number(
            scheduled.duration_minutes ??
              scheduled.paper_duration ??
              0
          ),

        questionCount:
          questions.length,

        subjects,

        chapters,

        status:
          String(
            scheduled.scheduled_status ??
              "Upcoming"
          ),
      },
    });
  } catch (error) {
    console.error(
      "SCHEDULED TEST DETAILS ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to load scheduled test.",
      },
      { status: 500 }
    );
  } finally {
    client.release();
  }
}
