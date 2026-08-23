import { NextRequest, NextResponse } from "next/server";
import { Pool } from "pg";

export const dynamic = "force-dynamic";

declare global {
  // eslint-disable-next-line no-var
  var __paperTreePool: Pool | undefined;
}

function getPool() {
  if (!process.env.DATABASE_URL) {
    throw new Error("DATABASE_URL is not configured.");
  }

  if (!global.__paperTreePool) {
    global.__paperTreePool = new Pool({
      connectionString: process.env.DATABASE_URL,
      ssl: {
        rejectUnauthorized: false,
      },
      max: 10,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 10000,
    });
  }

  return global.__paperTreePool;
}

/*
 * Safely parse questions from PostgreSQL JSON/JSONB.
 */
function parseQuestions(value: unknown): any[] {
  if (Array.isArray(value)) {
    return value;
  }

  if (typeof value === "string") {
    try {
      const parsed = JSON.parse(value);

      return Array.isArray(parsed)
        ? parsed
        : [];
    } catch {
      return [];
    }
  }

  return [];
}

/*
 * Normalize subject names so:
 *
 * Physics
 * PHYSICS
 * physics
 *
 * are treated as the same subject.
 */
function normalizeSubject(
  value: unknown
): string {
  const subject = String(
    value ?? ""
  )
    .trim()
    .toLowerCase();

  if (!subject) {
    return "";
  }

  if (subject === "physics") {
    return "Physics";
  }

  if (subject === "chemistry") {
    return "Chemistry";
  }

  if (
    subject === "mathematics" ||
    subject === "maths" ||
    subject === "math"
  ) {
    return "Mathematics";
  }

  if (subject === "biology") {
    return "Biology";
  }

  return (
    subject.charAt(0).toUpperCase() +
    subject.slice(1)
  );
}

export async function GET(
  request: NextRequest
) {
  const client =
    await getPool().connect();

  try {
    /*
     * ============================================================
     * STUDENT SESSION
     * ============================================================
     */

    const sessionCookie =
      request.cookies.get(
        "student_session"
      )?.value;

    if (!sessionCookie) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Student session not found.",
        },
        { status: 401 }
      );
    }

    let studentId = "";

    /*
     * Support:
     *
     * student_session = "student-id"
     *
     * OR
     *
     * student_session = {
     *   studentId: "..."
     * }
     */

    try {
      const parsed =
        JSON.parse(
          sessionCookie
        );

      if (
        parsed &&
        typeof parsed === "object" &&
        parsed.studentId
      ) {
        studentId = String(
          parsed.studentId
        );
      }
    } catch {
      studentId = sessionCookie;
    }

    studentId =
      studentId.trim();

    if (!studentId) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Invalid student session.",
        },
        { status: 401 }
      );
    }

    /*
     * ============================================================
     * STUDENT
     * ============================================================
     */

    const studentResult =
      await client.query(
        `
        SELECT
          id,
          name,
          roll_number,
          email
        FROM students
        WHERE id = $1
        LIMIT 1
        `,
        [studentId]
      );

    if (
      studentResult.rows.length ===
      0
    ) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Student not found.",
        },
        { status: 404 }
      );
    }

    const student =
      studentResult.rows[0];

    /*
     * ============================================================
     * TEST ATTEMPTS
     *
     * IMPORTANT:
     * We DO NOT select st.subject because
     * tests.subject does not exist in your database.
     *
     * Subject is taken from questions JSON.
     * ============================================================
     */

    const attemptsResult =
      await client.query(
        `
        SELECT
          ta.id,
          ta.scheduled_test_id,
          ta.status,
          ta.score,
          ta.total_marks,
          ta.correct_count,
          ta.incorrect_count,
          ta.unanswered_count,
          ta.started_at,
          ta.submitted_at,

          st.exam,
          st.question_count,
          st.created_at,
          st.questions

        FROM test_attempts ta

        LEFT JOIN tests st
          ON st.id =
             ta.scheduled_test_id

        WHERE ta.student_id = $1

        ORDER BY
          COALESCE(
            ta.submitted_at,
            ta.started_at
          ) DESC
        `,
        [studentId]
      );

    const attempts =
      attemptsResult.rows;

    /*
     * ============================================================
     * COMPLETED ATTEMPTS
     * ============================================================
     */

    const completedAttempts =
      attempts.filter(
        (attempt) =>
          attempt.status ===
            "SUBMITTED" ||
          attempt.status ===
            "AUTO_SUBMITTED"
      );

    /*
     * ============================================================
     * TESTS TAKEN
     * ============================================================
     */

    const testsTaken =
      completedAttempts.length;

    /*
     * ============================================================
     * AVERAGE SCORE
     * ============================================================
     */

    const averageScore =
      testsTaken > 0
        ? Number(
            (
              completedAttempts.reduce(
                (
                  sum,
                  attempt
                ) =>
                  sum +
                  Number(
                    attempt.score ??
                      0
                  ),
                0
              ) /
                testsTaken
            ).toFixed(2)
          )
        : null;

    /*
     * ============================================================
     * BEST SCORE
     * ============================================================
     */

    const bestScore =
      testsTaken > 0
        ? Number(
            Math.max(
              ...completedAttempts.map(
                (attempt) =>
                  Number(
                    attempt.score ??
                      0
                  )
              )
            ).toFixed(2)
          )
        : null;

    /*
     * ============================================================
     * TOTAL ATTEMPTS
     *
     * This includes submitted and in-progress attempts.
     * ============================================================
     */

    const totalAttempts =
      attempts.length;

    /*
     * ============================================================
     * PERFORMANCE TREND
     * ============================================================
     */

    const performanceTrend =
      [...completedAttempts]
        .reverse()
        .map(
          (
            attempt,
            index
          ) => ({
            attemptId:
              String(
                attempt.id
              ),

            testId:
              String(
                attempt.scheduled_test_id
              ),

            score:
              Number(
                attempt.score ??
                  0
              ),

            date:
              attempt.submitted_at ??
              attempt.started_at,

            label: `Test ${
              index + 1
            }`,
          })
        );

    /*
     * ============================================================
     * SUBJECT PERFORMANCE
     * ============================================================
     *
     * We calculate this from:
     *
     * tests.questions
     *
     * + test_answers
     *
     * We DO NOT rely on a tests.subject column.
     * ============================================================
     */

    const subjectStats: Record<
      string,
      {
        attempted: number;
        correct: number;
      }
    > = {};

    for (
      const attempt of
        completedAttempts
    ) {
      const questions =
        parseQuestions(
          attempt.questions
        );

      if (
        questions.length === 0
      ) {
        continue;
      }

      /*
       * Get answers for this attempt.
       */

      const answerResult =
        await client.query(
          `
          SELECT
            question_id,
            selected_answer,
            is_correct
          FROM test_answers
          WHERE attempt_id = $1
          `,
          [attempt.id]
        );

      /*
       * Map answers by question ID.
       */

      const answerMap =
        new Map<
          string,
          {
            selectedAnswer:
              | number
              | null;

            isCorrect:
              | boolean
              | null;
          }
        >();

      for (
        const answer of
          answerResult.rows
      ) {
        let selectedAnswer:
          | number
          | null = null;

        if (
          answer.selected_answer !==
            null &&
          answer.selected_answer !==
            undefined
        ) {
          const parsed =
            Number(
              answer.selected_answer
            );

          if (
            Number.isInteger(
              parsed
            )
          ) {
            selectedAnswer =
              parsed;
          }
        }

        /*
         * IMPORTANT:
         *
         * Do NOT use Boolean(null).
         *
         * null means unanswered.
         */

        let isCorrect:
          | boolean
          | null = null;

        if (
          answer.is_correct ===
          true
        ) {
          isCorrect = true;
        } else if (
          answer.is_correct ===
          false
        ) {
          isCorrect = false;
        }

        answerMap.set(
          String(
            answer.question_id
          ),
          {
            selectedAnswer,
            isCorrect,
          }
        );
      }

      /*
       * Calculate each subject.
       */

      for (
        const question of
          questions
      ) {
        const questionId =
          String(
            question.id ??
              question.question_id ??
              ""
          );

        if (!questionId) {
          continue;
        }

        const subject =
          normalizeSubject(
            question.subject ??
              question.subject_name
          );

        if (!subject) {
          continue;
        }

        /*
         * Initialize subject.
         */

        if (
          !subjectStats[
            subject
          ]
        ) {
          subjectStats[
            subject
          ] = {
            attempted: 0,
            correct: 0,
          };
        }

        const answer =
          answerMap.get(
            questionId
          );

        /*
         * No answer row / null selected answer
         * means unanswered.
         */

        if (
          !answer ||
          answer.selectedAnswer ===
            null
        ) {
          continue;
        }

        /*
         * This question was attempted.
         */

        subjectStats[
          subject
        ].attempted++;

        /*
         * Only TRUE is correct.
         */

        if (
          answer.isCorrect ===
          true
        ) {
          subjectStats[
            subject
          ].correct++;
        }
      }
    }

    /*
     * ============================================================
     * SUBJECT PERFORMANCE RESPONSE
     * ============================================================
     *
     * Always return the four MHT-CET subjects.
     * This makes the dashboard stable even before
     * every subject has been attempted.
     * ============================================================
     */

    const dashboardSubjects = [
      "Physics",
      "Chemistry",
      "Mathematics",
      "Biology",
    ];

    const subjectPerformance =
      dashboardSubjects.map(
        (subject) => {
          const stats =
            subjectStats[
              subject
            ];

          if (
            !stats ||
            stats.attempted ===
              0
          ) {
            return {
              subject,
              score: null,
              attempted: 0,
              correct: 0,
            };
          }

          return {
            subject,

            score: Number(
              (
                (stats.correct /
                  stats.attempted) *
                100
              ).toFixed(2)
            ),

            attempted:
              stats.attempted,

            correct:
              stats.correct,
          };
        }
      );

    /*
     * ============================================================
     * MY TESTS
     * ============================================================
     *
     * Show tests that this student has attempted.
     *
     * We use the attempts table rather than blindly
     * showing every test in the database.
     * ============================================================
     */

    const myTests = attempts.map(
      (attempt) => ({
        id: String(
          attempt.scheduled_test_id
        ),

        attemptId: String(
          attempt.id
        ),

        exam: String(
          attempt.exam ??
            "MHT-CET"
        ),

        questionCount:
          Number(
            attempt.question_count ??
              0
          ),

        createdAt:
          attempt.created_at ??
          attempt.started_at,

        status:
          String(
            attempt.status ??
              "IN_PROGRESS"
          ),

        score:
          attempt.score ===
          null
            ? null
            : Number(
                attempt.score
              ),

        submittedAt:
          attempt.submitted_at ??
          null,
      })
    );

    /*
     * ============================================================
     * RESPONSE
     * ============================================================
     */

    return NextResponse.json({
      success: true,

      student: {
        id: String(
          student.id
        ),

        name: String(
          student.name ??
            "Student"
        ),

        rollNumber:
          student.roll_number ??
          null,

        email:
          student.email ??
          null,
      },

      statistics: {
        testsTaken,

        averageScore,

        bestScore,

        attempts:
          totalAttempts,
      },

      performanceTrend,

      subjectPerformance,

      myTests,
    });
  } catch (error) {
    console.error(
      "DASHBOARD API ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,

        error:
          error instanceof Error
            ? error.message
            : "Failed to load dashboard.",
      },
      {
        status: 500,
      }
    );
  } finally {
    client.release();
  }
}