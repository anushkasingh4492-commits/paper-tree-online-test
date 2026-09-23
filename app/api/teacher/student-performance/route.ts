import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";

export async function GET() {
  try {
    const value =
      (await cookies()).get("master_session")?.value;

    if (!value) {
      return NextResponse.json(
        {
          success: false,
          error: "Unauthorized.",
        },
        { status: 401 }
      );
    }

    const session = parseSessionCookie<{
      id?: string;
      role?: string;
    }>(value);

    if (
      !session ||
      session.role !== "TEACHER" ||
      !session.id
    ) {
      return NextResponse.json(
        {
          success: false,
          error: "Unauthorized.",
        },
        { status: 401 }
      );
    }

    const teacherResult =
      await pool.query(
        `
        SELECT id, academy_id
        FROM teachers
        WHERE id = $1
        LIMIT 1
        `,
        [session.id]
      );

    if (!teacherResult.rows.length) {
      return NextResponse.json(
        {
          success: false,
          error: "Teacher not found.",
        },
        { status: 404 }
      );
    }

    const academyId =
      teacherResult.rows[0].academy_id;

    if (!academyId) {
      return NextResponse.json(
        {
          success: false,
          error: "Teacher is not assigned to an academy.",
        },
        { status: 403 }
      );
    }

    /*
     * Only tests/papers created by this teacher
     * are included. This prevents a teacher from
     * seeing another teacher's test performance.
     */
    const result = await pool.query(
      `
      SELECT
        s.id AS student_id,
        s.name AS student_name,
        s.email,
        s.class_name,

        COUNT(ta.id)::int AS tests_taken,

        COALESCE(
          ROUND(
            AVG(
              CASE
                WHEN ta.score IS NOT NULL
                THEN ta.score
              END
            )::numeric,
            2
          ),
          0
        )::float AS average_score,

        COALESCE(
          ROUND(
            AVG(
              CASE
                WHEN ta.score IS NOT NULL
                THEN ta.score
              END
            )::numeric,
            2
          ),
          0
        )::float AS average_accuracy,

        COALESCE(
          SUM(
            CASE
              WHEN ta.correct_count IS NOT NULL
              THEN ta.correct_count
              ELSE 0
            END
          ),
          0
        )::int AS correct,

        COALESCE(
          SUM(
            CASE
              WHEN ta.incorrect_count IS NOT NULL
              THEN ta.incorrect_count
              ELSE 0
            END
          ),
          0
        )::int AS wrong,

        COALESCE(
          SUM(
            CASE
              WHEN ta.unanswered_count IS NOT NULL
              THEN ta.unanswered_count
              ELSE 0
            END
          ),
          0
        )::int AS unanswered

      FROM students s

      LEFT JOIN test_attempts ta
        ON ta.student_id::text = s.id::text
        AND (
          LOWER(COALESCE(ta.status, '')) IN (
            'submitted',
            'completed',
            'complete',
            'auto_submitted',
            'auto submitted'
          )
        )

      LEFT JOIN papers p
        ON p.id::text = COALESCE(
          ta.paper_id::text,
          ''
        )

      LEFT JOIN scheduled_tests st
        ON st.id::text = COALESCE(
          ta.scheduled_test_id::text,
          ''
        )

      WHERE
        s.academy_id::text = $1::text
        AND (
          p.created_by::text = $2::text
          OR st.paper_id::text IN (
            SELECT id::text
            FROM papers
            WHERE created_by::text = $2::text
          )
        )

      GROUP BY
        s.id,
        s.name,
        s.email,
        s.class_name

      ORDER BY s.name ASC
      `,
      [academyId, session.id]
    );

    return NextResponse.json({
      success: true,
      students: result.rows,
    });
  } catch (error) {
    console.error(
      "TEACHER STUDENT PERFORMANCE ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to load student performance.",
      },
      { status: 500 }
    );
  }
}