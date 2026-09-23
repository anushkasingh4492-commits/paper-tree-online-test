import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";

type TeacherSession = {
  id?: string;
  role?: string;
};

export async function GET() {
  try {
    const cookieStore = await cookies();
    const value = cookieStore.get("master_session")?.value;
    const session = value
      ? parseSessionCookie<TeacherSession>(value)
      : null;

    if (!session?.id || session.role !== "TEACHER") {
      return NextResponse.json(
        { success: false, error: "Teacher login required." },
        { status: 401 }
      );
    }

    const teacherResult = await pool.query(
      `
        SELECT id, name, academy_id
        FROM teachers
        WHERE id = $1
        LIMIT 1
      `,
      [session.id]
    );

    const teacher = teacherResult.rows[0];

    if (!teacher) {
      return NextResponse.json(
        { success: false, error: "Teacher account was not found." },
        { status: 401 }
      );
    }

    if (!teacher.academy_id) {
      return NextResponse.json(
        { success: false, error: "This teacher is not assigned to an academy." },
        { status: 403 }
      );
    }

    const completedStatuses = `
      LOWER(REPLACE(COALESCE(ta.status, ''), '-', '_')) IN
      ('submitted', 'auto_submitted', 'auto submitted', 'completed', 'complete')
    `;

    const result = await pool.query(
      `
        SELECT
          s.id,
          s.name,
          s.email,
          COALESCE(perf.tests_taken, 0)::int AS tests_taken,
          COALESCE(perf.average_percentage, 0) AS average_percentage,
          COALESCE(perf.best_percentage, 0) AS best_percentage,
          COALESCE(perf.correct_answers, 0)::int AS correct_answers,
          COALESCE(perf.wrong_answers, 0)::int AS wrong_answers,
          COALESCE(perf.unanswered_questions, 0)::int AS unanswered_questions,
          COALESCE(
            STRING_AGG(DISTINCT b.name, ', ' ORDER BY b.name),
            'Not assigned'
          ) AS batches
        FROM students s
        LEFT JOIN batch_students bs
          ON bs.student_id = s.id
        LEFT JOIN batches b
          ON b.id = bs.batch_id
         AND b.academy_id = $1
        LEFT JOIN (
          SELECT
            ta.student_id,
            COUNT(ta.id) FILTER (WHERE ${completedStatuses})::int AS tests_taken,
            COALESCE(
              ROUND(
                AVG(
                  CASE
                    WHEN ${completedStatuses}
                     AND COALESCE(ta.total_marks, 0) > 0
                    THEN (ta.score::numeric / ta.total_marks::numeric) * 100
                  END
                )::numeric,
                2
              ),
              0
            ) AS average_percentage,
            COALESCE(
              ROUND(
                MAX(
                  CASE
                    WHEN ${completedStatuses}
                     AND COALESCE(ta.total_marks, 0) > 0
                    THEN (ta.score::numeric / ta.total_marks::numeric) * 100
                  END
                )::numeric,
                2
              ),
              0
            ) AS best_percentage,
            COALESCE(
              SUM(
                CASE
                  WHEN ${completedStatuses} THEN COALESCE(ta.correct_count, 0)
                  ELSE 0
                END
              ),
              0
            )::int AS correct_answers,
            COALESCE(
              SUM(
                CASE
                  WHEN ${completedStatuses} THEN COALESCE(ta.incorrect_count, 0)
                  ELSE 0
                END
              ),
              0
            )::int AS wrong_answers,
            COALESCE(
              SUM(
                CASE
                  WHEN ${completedStatuses} THEN COALESCE(ta.unanswered_count, 0)
                  ELSE 0
                END
              ),
              0
            )::int AS unanswered_questions
          FROM test_attempts ta
          GROUP BY ta.student_id
        ) perf
          ON perf.student_id = s.id
        WHERE s.academy_id = $1
        GROUP BY
          s.id,
          s.name,
          s.email,
          perf.tests_taken,
          perf.average_percentage,
          perf.best_percentage,
          perf.correct_answers,
          perf.wrong_answers,
          perf.unanswered_questions
        ORDER BY s.name ASC
      `,
      [teacher.academy_id]
    );

    const students = result.rows.map((row) => {
      const correct = Number(row.correct_answers || 0);
      const wrong = Number(row.wrong_answers || 0);
      const attempted = correct + wrong;

      return {
        id: String(row.id),
        name: row.name,
        email: row.email,
        batches: row.batches || "Not assigned",
        testsTaken: Number(row.tests_taken || 0),
        averagePercentage: Number(row.average_percentage || 0),
        bestPercentage: Number(row.best_percentage || 0),
        correctAnswers: correct,
        wrongAnswers: wrong,
        unansweredQuestions: Number(row.unanswered_questions || 0),
        accuracy: attempted > 0
          ? Number(((correct / attempted) * 100).toFixed(2))
          : 0,
      };
    });

    return NextResponse.json({
      success: true,
      teacher: { id: teacher.id, name: teacher.name },
      students,
    });
  } catch (error) {
    console.error("TEACHER PERFORMANCE ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error: error instanceof Error
          ? error.message
          : "Could not load student performance.",
      },
      { status: 500 }
    );
  }
}
