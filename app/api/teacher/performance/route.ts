import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";
import { ensureFeatureSchema } from "@/lib/feature-schema";
import { getStudentGamification } from "@/lib/gamification";
import { getAcademySubscription } from "@/lib/subscription";

export const runtime = "nodejs";

type TeacherSession = {
  id?: string;
  role?: string;
};

export async function GET(request: Request) {
  try {
    await ensureFeatureSchema();
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

    const subscription = await getAcademySubscription(String(teacher.academy_id));
    if (!subscription.features.completeStudentReports) {
      return NextResponse.json(
        { success: false, error: "Student performance reports are not available for this academy." },
        { status: 403 }
      );
    }

    const completedStatuses = `
      LOWER(REPLACE(COALESCE(ta.status, ''), '-', '_')) IN
      ('submitted', 'auto_submitted', 'auto submitted', 'completed', 'complete')
    `;

    const studentId = new URL(request.url).searchParams.get("studentId")?.trim();

    if (studentId) {
      const studentResult = await pool.query(
        `
          SELECT id, name
          FROM students
          WHERE id::text = $1::text
            AND academy_id::text = $2::text
          LIMIT 1
        `,
        [studentId, teacher.academy_id]
      );

      if (!studentResult.rows.length) {
        return NextResponse.json(
          { success: false, error: "Student not found in your academy." },
          { status: 404 }
        );
      }

      const attemptsResult = await pool.query(
        `
          SELECT
            ta.id,
            ta.test_id,
            ta.scheduled_test_id,
            ta.score,
            ta.total_marks,
            ta.correct_count,
            ta.incorrect_count,
            ta.unanswered_count,
            ta.status,
            ta.started_at,
            ta.submitted_at,
            t.exam,
            t.question_count,
            t.questions AS test_questions,
            COALESCE(
              p.description,
              st.title,
              CONCAT('Test ', LEFT(COALESCE(ta.test_id, ta.scheduled_test_id)::text, 8))
            ) AS test_title
          FROM test_attempts ta
          LEFT JOIN tests t
            ON t.id::text = COALESCE(ta.test_id, ta.scheduled_test_id)::text
          LEFT JOIN scheduled_tests st
            ON st.id::text = ta.scheduled_test_id::text
           AND st.academy_id::text = $2::text
          LEFT JOIN papers p
            ON p.id::text = st.paper_id::text
           AND p.academy_id::text = $2::text
          WHERE ta.student_id::text = $1::text
            AND ${completedStatuses}
          ORDER BY ta.submitted_at DESC NULLS LAST, ta.started_at DESC NULLS LAST
        `,
        [studentId, teacher.academy_id]
      );

      /*
       * Build accurate test metadata from the test snapshot and
       * the canonical questions table. A test can contain a
       * partial question snapshot, so the DB question bank is
       * used as the fallback for subject/chapter/difficulty/type.
       */
      const questionIds = new Set<string>();

      const parsedAttempts = attemptsResult.rows.map((attempt) => {
        let snapshot: any[] = [];

        if (Array.isArray(attempt.test_questions)) {
          snapshot = attempt.test_questions;
        } else if (typeof attempt.test_questions === "string") {
          try {
            const parsed = JSON.parse(attempt.test_questions);
            if (Array.isArray(parsed)) snapshot = parsed;
          } catch {
            snapshot = [];
          }
        }

        for (const question of snapshot) {
          const id = String(
            question?.id ??
              question?.question_id ??
              question?.questionId ??
              ""
          ).trim();
          if (id) questionIds.add(id);
        }

        return { ...attempt, snapshot };
      });

      const questionBank = new Map<string, any>();

      if (questionIds.size > 0) {
        const questionResult = await pool.query(
          `
            SELECT
              id::text AS id,
              subject,
              chapter_name,
              difficulty,
              question_type
            FROM questions
            WHERE id::text = ANY($1::text[])
          `,
          [Array.from(questionIds)]
        );

        for (const row of questionResult.rows) {
          questionBank.set(String(row.id), row);
        }
      }

      const attempts = parsedAttempts.map((attempt) => {
        const subjects = new Set<string>();
        const chapters = new Set<string>();
        const difficulties = new Set<string>();
        const questionTypes = new Set<string>();

        for (const question of attempt.snapshot) {
          const id = String(
            question?.id ??
              question?.question_id ??
              question?.questionId ??
              ""
          ).trim();
          const bank = id ? questionBank.get(id) : undefined;

          const subject = String(
            question?.subject ??
              question?.subject_name ??
              bank?.subject ??
              ""
          ).trim();
          const chapter = String(
            question?.chapter ??
              question?.chapter_name ??
              bank?.chapter_name ??
              ""
          ).trim();
          const difficulty = String(
            question?.difficulty ??
              bank?.difficulty ??
              ""
          ).trim();
          const questionType = String(
            question?.question_type ??
              bank?.question_type ??
              ""
          ).trim();

          if (subject) subjects.add(subject);
          if (chapter) chapters.add(chapter);
          if (difficulty) difficulties.add(difficulty);
          if (questionType) questionTypes.add(questionType);
        }

        const totalQuestions = Number(
          attempt.question_count ??
          attempt.snapshot.length ??
          0
        );

        const score = Number(attempt.score ?? 0);
        const totalMarks = Number(attempt.total_marks ?? 0);

        return {
          id: String(attempt.id),
          test_id: attempt.test_id ? String(attempt.test_id) : null,
          scheduled_test_id: attempt.scheduled_test_id
            ? String(attempt.scheduled_test_id)
            : null,
          score,
          total_marks: totalMarks,
          correct_count: Number(attempt.correct_count ?? 0),
          incorrect_count: Number(attempt.incorrect_count ?? 0),
          unanswered_count: Number(attempt.unanswered_count ?? 0),
          status: attempt.status,
          started_at: attempt.started_at,
          submitted_at: attempt.submitted_at,
          test_title: attempt.test_title,
          exam: attempt.exam || null,
          question_count: totalQuestions,
          subjects: Array.from(subjects),
          chapters: Array.from(chapters),
          difficulties: Array.from(difficulties),
          question_types: Array.from(questionTypes),
          percentage:
            totalMarks > 0
              ? Number(((score / totalMarks) * 100).toFixed(1))
              : 0,
        };
      });

      return NextResponse.json({
        success: true,
        student: studentResult.rows[0],
        attempts,
      });
    }

    const result = await pool.query(
      `
        SELECT
          s.id,
          s.name,
          s.email,
          s.parent_phone,
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
          s.parent_phone,
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

    const students = await Promise.all(result.rows.map(async (row) => {
      const correct = Number(row.correct_answers || 0);
      const wrong = Number(row.wrong_answers || 0);
      const attempted = correct + wrong;
      let game = null;
      try {
        game = await getStudentGamification(String(row.id), String(teacher.academy_id));
      } catch (error) {
        console.error("TEACHER GAMIFICATION ERROR", row.id, error);
      }

      return {
        id: String(row.id),
        name: row.name,
        email: row.email,
        parentPhone: row.parent_phone || null,
        batches: row.batches || "Not assigned",
        testsTaken: Number(row.tests_taken || 0),
        averagePercentage: Number(row.average_percentage || 0),
        bestPercentage: Number(row.best_percentage || 0),
        correctAnswers: correct,
        wrongAnswers: wrong,
        unansweredQuestions: Number(row.unanswered_questions || 0),
        accuracy: attempted > 0 ? Number(((correct / attempted) * 100).toFixed(2)) : 0,
        level: game?.level ?? 1,
        levelName: game?.levelName ?? "Rookie",
        currentStreak: game?.streak ?? 0,
        lastActiveDate: game?.lastActiveDate ?? null,
        badgesEarned: game?.badges?.filter((b) => b.earned).length ?? 0,
      };
    }));

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
