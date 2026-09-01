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

/* ============================================================
   HELPERS
============================================================ */

function normalizeSubject(value: unknown): string {
  const subject = String(value ?? "")
    .trim()
    .toLowerCase();

  if (!subject) return "";

  if (subject === "physics") return "Physics";

  if (subject === "chemistry") return "Chemistry";

  if (
    subject === "mathematics" ||
    subject === "maths" ||
    subject === "math"
  ) {
    return "Mathematics";
  }

  if (subject === "biology") return "Biology";

  return (
    subject.charAt(0).toUpperCase() +
    subject.slice(1)
  );
}

/*
 * Normalizes an answer into a comparable string.
 *
 * Examples:
 *
 * "A" -> "a"
 * "A " -> "a"
 * 0 -> "0"
 * "0" -> "0"
 */
function normalizeAnswer(
  value: unknown
): string | null {
  if (
    value === null ||
    value === undefined ||
    String(value).trim() === ""
  ) {
    return null;
  }

  return String(value)
    .trim()
    .toLowerCase();
}

function formatDuration(
  minutes: number
): string {
  if (!minutes || minutes <= 0) {
    return "0m";
  }

  const rounded = Math.round(minutes);

  const hours = Math.floor(
    rounded / 60
  );

  const mins = rounded % 60;

  if (hours <= 0) {
    return `${mins}m`;
  }

  return `${hours}h ${mins}m`;
}

function getDurationMinutes(
  startedAt: unknown,
  submittedAt: unknown
): number {
  if (
    !startedAt ||
    !submittedAt
  ) {
    return 0;
  }

  const start = new Date(
    String(startedAt)
  ).getTime();

  const end = new Date(
    String(submittedAt)
  ).getTime();

  if (
    !Number.isFinite(start) ||
    !Number.isFinite(end) ||
    end <= start
  ) {
    return 0;
  }

  return (
    (end - start) / 60000
  );
}

function formatDate(
  value: unknown
): string {
  if (!value) return "";

  const date = new Date(
    String(value)
  );

  if (Number.isNaN(date.getTime())) {
    return "";
  }

  return date.toLocaleDateString(
    "en-IN",
    {
      day: "2-digit",
      month: "short",
      year: "numeric",
    }
  );
}

function formatDateTime(
  value: unknown
): string {
  if (!value) return "";

  const date = new Date(
    String(value)
  );

  if (Number.isNaN(date.getTime())) {
    return "";
  }

  return date.toLocaleString(
    "en-IN",
    {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }
  );
}

function getStatus(
  value: unknown
): string {
  return String(value ?? "")
    .trim()
    .toLowerCase()
    .replace(/-/g, "_");
}

function isCompletedStatus(
  value: unknown
): boolean {
  const status = getStatus(value);

  return (
    status === "submitted" ||
    status === "auto_submitted" ||
    status === "auto submitted" ||
    status === "completed" ||
    status === "complete"
  );
}

/*
 * Extract question IDs from the test.questions field.
 *
 * Supported:
 *
 * ["q1", "q2"]
 *
 * [
 *   { id: "q1" },
 *   { question_id: "q2" }
 * ]
 */
function extractQuestionIds(
  value: unknown
): string[] {
  if (!Array.isArray(value)) {
    return [];
  }

  const ids: string[] = [];

  for (const item of value) {
    if (typeof item === "string") {
      if (item.trim()) {
        ids.push(item.trim());
      }

      continue;
    }

    if (
      item &&
      typeof item === "object"
    ) {
      const obj =
        item as Record<
          string,
          unknown
        >;

      const id =
        obj.id ??
        obj.question_id ??
        obj.questionId;

      if (
        id !== null &&
        id !== undefined &&
        String(id).trim()
      ) {
        ids.push(
          String(id).trim()
        );
      }
    }
  }

  return Array.from(
    new Set(ids)
  );
}

function getTestDifficulty(
  value: unknown
): string {
  if (!Array.isArray(value)) {
    return "Balanced";
  }

  const difficulties =
    Array.from(
      new Set(
        value
          .map((item: any) =>
            String(
              item?.difficulty ?? ""
            )
              .trim()
              .toLowerCase()
          )
          .filter(Boolean)
      )
    );

  if (
    difficulties.length === 1
  ) {
    const difficulty =
      difficulties[0];

    return (
      difficulty.charAt(0).toUpperCase() +
      difficulty.slice(1)
    );
  }

  return "Balanced";
}

/*
 * Resolve the correct answer from a question.
 *
 * Supports the current answer field as well as
 * older database field names.
 */
function getCorrectAnswer(
  question: any
): string | null {
  const candidates = [
    question?.answer,
    question?.correct_option,
    question?.correctOption,
  ];

  for (const value of candidates) {
    const normalized =
      normalizeAnswer(value);

    if (normalized !== null) {
      return normalized;
    }
  }

  return null;
}

/* ============================================================
   TYPES
============================================================ */

type Stats = {
  total: number;
  attempted: number;
  correct: number;
  wrong: number;
  unanswered: number;
};

type ChapterStats = Stats & {
  subject: string;
  chapter: string;
};

/* ============================================================
   GET DASHBOARD
============================================================ */

export async function GET(
  request: NextRequest
) {
  let client: any;

  try {
    const pool = getPool();

    client =
      await pool.connect();

    /* ========================================================
       SESSION
    ======================================================== */

 const sessionCookie =
  request.cookies.get("student_session")?.value;

if (!sessionCookie) {
  return NextResponse.json(
    {
      success: false,
      error: "Student session not found.",
    },
    {
      status: 401,
    }
  );
}

let studentId = sessionCookie;

try {
  const parsed = JSON.parse(sessionCookie);

  if (
    parsed &&
    typeof parsed === "object" &&
    parsed.studentId
  ) {
    studentId = String(parsed.studentId);
  }

}catch {
      studentId =
        sessionCookie;
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
        {
          status: 401,
        }
      );
    }

    /* ========================================================
       STUDENT
    ======================================================== */
const studentQueryStart = Date.now();

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
console.log(
  "STUDENT QUERY:",
  Date.now() - studentQueryStart,
  "ms"
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
        {
          status: 404,
        }
      );
    }

    const student =
      studentResult.rows[0];

    /* ========================================================
       ALL ATTEMPTS
       
       A test attempt can reference the test through either:
       
       test_id
       scheduled_test_id
       
       Therefore resolve the actual test ID with COALESCE.
    ======================================================== */

        const attemptsQueryStart = Date.now();

const attemptsResult =
  await client.query(
        `
        SELECT
          ta.id,
          ta.student_id,
          ta.test_id,
          ta.scheduled_test_id,
          ta.started_at,
          ta.submitted_at,
          ta.status,
          ta.score,
          ta.total_marks,
          ta.correct_count,
          ta.incorrect_count,
          ta.unanswered_count,
          ta.created_at,

          COALESCE(
            NULLIF(ta.test_id, ''),
            NULLIF(ta.scheduled_test_id, '')
          ) AS resolved_test_id,

          t.id AS test_table_id,
          t.exam AS test_exam,
          t.question_count AS test_question_count,
          t.questions AS test_questions,
          t.created_at AS test_created_at

        FROM test_attempts ta

        LEFT JOIN tests t
          ON t.id = COALESCE(
            NULLIF(ta.test_id, ''),
            NULLIF(ta.scheduled_test_id, '')
          )

        WHERE ta.student_id = $1

        ORDER BY
          COALESCE(
            ta.submitted_at,
            ta.started_at,
            ta.created_at
          ) DESC
        `,
        [studentId]
      );
      console.log(
  "ATTEMPTS QUERY:",
  Date.now() - attemptsQueryStart,
  "ms",
  "rows:",
  attemptsResult.rows.length
);

    const attempts =
      attemptsResult.rows;

    /* ========================================================
       COMPLETED ATTEMPTS
    ======================================================== */

    const completedAttempts =
      attempts.filter(
        (attempt: any) =>
          isCompletedStatus(
            attempt.status
          )
      );

    const testsTaken =
      completedAttempts.length;

    /* ========================================================
       GLOBAL ANALYTICS
    ======================================================== */

    let totalQuestions = 0;
    let totalAttempted = 0;
    let totalCorrect = 0;
    let totalWrong = 0;
    let totalUnanswered = 0;
    let totalStudyMinutes = 0;

    const subjectStats: Record<
      string,
      Stats
    > = {};

    const chapterStats: Record<
      string,
      ChapterStats
    > = {};

    const attemptAnalytics =
      new Map<
        string,
        Stats
      >();

    /* ========================================================
       PROCESS COMPLETED ATTEMPTS
    ======================================================== */

    for (
      const attempt of
        completedAttempts
    ) {
      const analyticsStart = Date.now();
      const attemptId =
        String(attempt.id);

      totalStudyMinutes +=
        getDurationMinutes(
          attempt.started_at,
          attempt.submitted_at
        );

      /* ------------------------------------------------------
         QUESTION IDS
      ------------------------------------------------------ */

      let questionIds =
        extractQuestionIds(
          attempt.test_questions
        );

      /* ------------------------------------------------------
         ANSWERS
      ------------------------------------------------------ */

      const answersResult =
        await client.query(
          `
          SELECT
            id,
            question_id,
            selected_answer,
            is_correct,
            marks_awarded,
            time_spent_seconds,
            marked_for_review,
            answered_at
          FROM test_answers
          WHERE attempt_id = $1
          ORDER BY id ASC
          `,
          [attemptId]
        );

      const answers =
        answersResult.rows;

      /* ------------------------------------------------------
         FALLBACK QUESTION IDS
      ------------------------------------------------------ */

      if (
        questionIds.length === 0 &&
        answers.length > 0
      ) {
        questionIds =
          Array.from(
            new Set(
              answers.map(
                (answer: any) =>
                  String(
                    answer.question_id
                  )
              )
            )
          );
      }

      /* ------------------------------------------------------
         QUESTIONS
      ------------------------------------------------------ */

      let questions: any[] =
        [];

      if (
        questionIds.length > 0
      ) {
        const questionResult =
          await client.query(
            `
        SELECT
  id,
  exam,
  subject,
  standard,
  chapter_number,
  chapter_name,
  major_topic,
  subtopic,
  concept_tested,
  correct_option
FROM questions
            WHERE id = ANY($1::varchar[])
            `,
            [questionIds]
          );

        questions =
          questionResult.rows;
      }

      /* ------------------------------------------------------
         MAPS
      ------------------------------------------------------ */

      const answerMap =
        new Map<
          string,
          any
        >();

      for (
        const answer of
          answers
      ) {
        answerMap.set(
          String(
            answer.question_id
          ),
          answer
        );
      }

      const questionMap =
        new Map<
          string,
          any
        >();

      for (
        const question of
          questions
      ) {
        questionMap.set(
          String(
            question.id
          ),
          question
        );
      }

      /* ------------------------------------------------------
         QUESTION COUNT
      ------------------------------------------------------ */

      const configuredQuestionCount =
        Number(
          attempt.test_question_count ??
            0
        );

      const questionCount =
        configuredQuestionCount >
        0
          ? configuredQuestionCount
          : questionIds.length >
            0
          ? questionIds.length
          : answers.length;

      totalQuestions +=
        questionCount;

      let attemptTotal =
        questionCount;

      let attemptAttempted =
        0;

      let attemptCorrect =
        0;

      let attemptWrong =
        0;

      let attemptUnanswered =
        0;

      const analysisIds =
        questionIds.length > 0
          ? questionIds
          : questions.map(
              (question) =>
                String(
                  question.id
                )
            );

      const uniqueAnalysisIds =
        Array.from(
          new Set(
            analysisIds
          )
        );

      /* ------------------------------------------------------
         ANALYSE QUESTIONS
      ------------------------------------------------------ */

      for (
        const questionId of
          uniqueAnalysisIds
      ) {
        const question =
          questionMap.get(
            questionId
          );

        const answer =
          answerMap.get(
            questionId
          );

        const subject =
          normalizeSubject(
            question?.subject
          );

        const chapter =
          String(
            question?.chapter_name ??
              ""
          ).trim();

        /* ----------------------------------------------------
           SUBJECT
        ---------------------------------------------------- */

        if (subject) {
          if (
            !subjectStats[
              subject
            ]
          ) {
            subjectStats[
              subject
            ] = {
              total: 0,
              attempted: 0,
              correct: 0,
              wrong: 0,
              unanswered: 0,
            };
          }

          subjectStats[
            subject
          ].total++;
        }

        /* ----------------------------------------------------
           CHAPTER
        ---------------------------------------------------- */

        const chapterKey =
          `${subject}::${chapter}`;

        if (
          subject &&
          chapter
        ) {
          if (
            !chapterStats[
              chapterKey
            ]
          ) {
            chapterStats[
              chapterKey
            ] = {
              subject,
              chapter,
              total: 0,
              attempted: 0,
              correct: 0,
              wrong: 0,
              unanswered: 0,
            };
          }

          chapterStats[
            chapterKey
          ].total++;
        }

        /* ----------------------------------------------------
           UNANSWERED
        ---------------------------------------------------- */

        if (
          !answer ||
          normalizeAnswer(
            answer.selected_answer
          ) === null
        ) {
          attemptUnanswered++;

          if (subject) {
            subjectStats[
              subject
            ].unanswered++;
          }

          if (
            subject &&
            chapter
          ) {
            chapterStats[
              chapterKey
            ].unanswered++;
          }

          continue;
        }

        /* ----------------------------------------------------
           ATTEMPTED
        ---------------------------------------------------- */

        attemptAttempted++;

        if (subject) {
          subjectStats[
            subject
          ].attempted++;
        }

        if (
          subject &&
          chapter
        ) {
          chapterStats[
            chapterKey
          ].attempted++;
        }

        /* ----------------------------------------------------
           CORRECT / WRONG
        ---------------------------------------------------- */

        let isCorrect:
          | boolean
          | null =
          answer.is_correct;

        /*
         * If is_correct was not stored for some reason,
         * calculate it from the database question.
         */
        if (
          isCorrect === null ||
          isCorrect === undefined
        ) {
          const selected =
            normalizeAnswer(
              answer.selected_answer
            );

          const correct =
            getCorrectAnswer(
              question
            );

          if (
            selected !== null &&
            correct !== null
          ) {
            isCorrect =
              selected ===
              correct;
          }
        }

        if (
          isCorrect === true
        ) {
          attemptCorrect++;

          if (subject) {
            subjectStats[
              subject
            ].correct++;
          }

          if (
            subject &&
            chapter
          ) {
            chapterStats[
              chapterKey
            ].correct++;
          }
        } else {
          attemptWrong++;

          if (subject) {
            subjectStats[
              subject
            ].wrong++;
          }

          if (
            subject &&
            chapter
          ) {
            chapterStats[
              chapterKey
            ].wrong++;
          }
        }
      }

      /* ------------------------------------------------------
         ANSWER FALLBACK
      ------------------------------------------------------ */

      if (
        uniqueAnalysisIds.length ===
          0 &&
        answers.length > 0
      ) {
        attemptTotal =
          configuredQuestionCount >
          0
            ? configuredQuestionCount
            : answers.length;

        attemptAttempted =
          0;

        attemptCorrect =
          0;

        attemptWrong =
          0;

        attemptUnanswered =
          0;

        for (
          const answer of
            answers
        ) {
          const selected =
            normalizeAnswer(
              answer.selected_answer
            );

          if (
            selected === null
          ) {
            attemptUnanswered++;
            continue;
          }

          attemptAttempted++;

          if (
            answer.is_correct ===
            true
          ) {
            attemptCorrect++;
          } else {
            attemptWrong++;
          }
        }
      }

      /* ------------------------------------------------------
         SAFETY
      ------------------------------------------------------ */

      if (
        attemptAttempted +
          attemptUnanswered <
        attemptTotal
      ) {
        attemptUnanswered =
          Math.max(
            0,
            attemptTotal -
              attemptAttempted
          );
      }

      totalAttempted +=
        attemptAttempted;

      totalCorrect +=
        attemptCorrect;

      totalWrong +=
        attemptWrong;

      totalUnanswered +=
        attemptUnanswered;

      attemptAnalytics.set(
        attemptId,
        {
          total:
            attemptTotal,

          attempted:
            attemptAttempted,

          correct:
            attemptCorrect,

          wrong:
            attemptWrong,

          unanswered:
            attemptUnanswered,
        }
      );
      console.log(
  "DASHBOARD ANALYTICS LOOP:",
  Date.now() - analyticsStart,
  "ms",
  "completed attempts:",
  completedAttempts.length
);
    }

    /* ========================================================
       SCORE STATISTICS
    ======================================================== */

    const scores: number[] =
      completedAttempts.map(
        (
          attempt: any
        ): number =>
          Number(
            attempt.score ?? 0
          )
      );

    const averageScore =
      scores.length > 0
        ? Number(
            (
              scores.reduce(
                (
                  sum: number,
                  score: number
                ) =>
                  sum + score,
                0
              ) /
              scores.length
            ).toFixed(2)
          )
        : 0;

    const bestScore =
      scores.length > 0
        ? Number(
            Math.max(
              ...scores
            ).toFixed(2)
          )
        : 0;

    const lowestScore =
      scores.length > 0
        ? Number(
            Math.min(
              ...scores
            ).toFixed(2)
          )
        : 0;

    const totalAttempts =
      attempts.length;

    const overallAccuracy =
      totalAttempted > 0
        ? Number(
            (
              (totalCorrect /
                totalAttempted) *
              100
            ).toFixed(2)
          )
        : 0;

    /* ========================================================
       CONSISTENCY
    ======================================================== */

    let consistency = 0;

    if (scores.length >= 2) {
      const mean =
        averageScore;

      const variance =
        scores.reduce(
          (
            sum: number,
            score: number
          ) =>
            sum +
            Math.pow(
              score - mean,
              2
            ),
          0
        ) /
        scores.length;

      const standardDeviation =
        Math.sqrt(
          variance
        );

      consistency =
        Math.max(
          0,
          Math.min(
            100,
            Number(
              (
                100 -
                standardDeviation
              ).toFixed(0)
            )
          )
        );
    } else if (
      scores.length === 1
    ) {
      consistency = 100;
    }

    /* ========================================================
       PERFORMANCE TREND
    ======================================================== */

    const performanceTrend =
      [
        ...completedAttempts,
      ]
        .reverse()
        .map(
          (
            attempt: any,
            index: number
          ) => {
            const testId =
              attempt.resolved_test_id ??
              null;

            const date =
              attempt.submitted_at ??
              attempt.started_at ??
              attempt.created_at;

            return {
              attemptId:
                String(
                  attempt.id
                ),

              testId,

              score:
                Number(
                  attempt.score ??
                    0
                ),

              date,

              formattedDate:
                formatDate(
                  date
                ),

              label:
                `Test ${
                  index + 1
                }`,

              name: testId
                ? String(
                    testId
                  )
                : `Test ${
                    index + 1
                  }`,
            };
          }
        );

    /* ========================================================
       SUBJECT PERFORMANCE
    ======================================================== */

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
            stats.total === 0
          ) {
            return {
              subject,

              score: 0,

              accuracy: 0,

              total: 0,

              attempted: 0,

              correct: 0,

              wrong: 0,

              unanswered: 0,
            };
          }

          const accuracy =
            stats.attempted > 0
              ? Number(
                  (
                    (stats.correct /
                      stats.attempted) *
                    100
                  ).toFixed(2)
                )
              : 0;

          return {
            subject,

            score:
              accuracy,

            accuracy,

            total:
              stats.total,

            attempted:
              stats.attempted,

            correct:
              stats.correct,

            wrong:
              stats.wrong,

            unanswered:
              stats.unanswered,
          };
        }
      );

    /* ========================================================
       OTHER SUBJECTS
    ======================================================== */

    for (
      const [
        subject,
        stats,
      ] of Object.entries(
        subjectStats
      )
    ) {
      if (
        dashboardSubjects.includes(
          subject
        )
      ) {
        continue;
      }

      const accuracy =
        stats.attempted > 0
          ? Number(
              (
                (stats.correct /
                  stats.attempted) *
                100
              ).toFixed(2)
            )
          : 0;

      subjectPerformance.push({
        subject,

        score:
          accuracy,

        accuracy,

        total:
          stats.total,

        attempted:
          stats.attempted,

        correct:
          stats.correct,

        wrong:
          stats.wrong,

        unanswered:
          stats.unanswered,
      });
    }

    /* ========================================================
       CHAPTER PERFORMANCE
    ======================================================== */

    const chapterPerformance =
      Object.values(
        chapterStats
      )
        .map(
          (stats) => {
            const accuracy =
              stats.attempted > 0
                ? Number(
                    (
                      (stats.correct /
                        stats.attempted) *
                      100
                    ).toFixed(2)
                  )
                : 0;

            return {
              subject:
                stats.subject,

              chapter:
                stats.chapter,

              total:
                stats.total,

              attempted:
                stats.attempted,

              correct:
                stats.correct,

              wrong:
                stats.wrong,

              unanswered:
                stats.unanswered,

              accuracy,
            };
          }
        )
        .sort(
          (a, b) =>
            a.accuracy -
            b.accuracy
        );

    /* ========================================================
       WEAK AREAS
    ======================================================== */

    const weakAreas =
      chapterPerformance
        .filter(
          (item) =>
            item.attempted > 0
        )
        .slice(0, 10)
        .map(
          (item) => ({
            topic:
              item.chapter,

            chapter:
              item.chapter,

            subject:
              item.subject,

            score:
              item.accuracy,

            accuracy:
              item.accuracy,

            attempted:
              item.attempted,

            correct:
              item.correct,

            wrong:
              item.wrong,

            unanswered:
              item.unanswered,
          })
        );

    /* ========================================================
       SCORE DISTRIBUTION
    ======================================================== */

    const scoreDistribution = {
      above90:
        scores.filter(
          (score) =>
            score >= 90
        ).length,

      between70and89:
        scores.filter(
          (score) =>
            score >= 70 &&
            score < 90
        ).length,

      between50and69:
        scores.filter(
          (score) =>
            score >= 50 &&
            score < 70
        ).length,

      below50:
        scores.filter(
          (score) =>
            score < 50
        ).length,
    };

    /* ========================================================
       RESULTS
    ======================================================== */

    const results =
      completedAttempts
        .map(
          (
            attempt: any,
            index: number
          ) => {
            const analytics =
              attemptAnalytics.get(
                String(
                  attempt.id
                )
              );

            const accuracy =
              analytics &&
              analytics.attempted >
                0
                ? Number(
                    (
                      (analytics.correct /
                        analytics.attempted) *
                      100
                    ).toFixed(2)
                  )
                : 0;

            const testId =
              attempt.resolved_test_id ??
              null;

            const name =
              testId
                ? String(
                    testId
                  )
                : `Test ${
                    index + 1
                  }`;

            return {
              id: testId
                ? String(
                    testId
                  )
                : null,

              attemptId:
                String(
                  attempt.id
                ),

              difficulty:
                getTestDifficulty(
                  attempt.test_questions
                ),

              name,

              title:
                name,

              paperId:
                null,

              paperCode:
                null,

              exam:
                String(
                  attempt.test_exam ??
                    "MHT-CET"
                ),

              score:
                Number(
                  attempt.score ??
                    0
                ),

              totalMarks:
                Number(
                  attempt.total_marks ??
                    0
                ),

              accuracy,

              correct:
                analytics?.correct ??
                Number(
                  attempt.correct_count ??
                    0
                ),

              wrong:
                analytics?.wrong ??
                Number(
                  attempt.incorrect_count ??
                    0
                ),

              unanswered:
                analytics?.unanswered ??
                Number(
                  attempt.unanswered_count ??
                    0
                ),

              attempted:
                analytics?.attempted ??
                0,

              totalQuestions:
                analytics?.total ??
                Number(
                  attempt.test_question_count ??
                    0
                ),

              questionCount:
                analytics?.total ??
                Number(
                  attempt.test_question_count ??
                    0
                ),

              time:
                formatDuration(
                  getDurationMinutes(
                    attempt.started_at,
                    attempt.submitted_at
                  )
                ),

              durationMinutes:
                Number(
                  getDurationMinutes(
                    attempt.started_at,
                    attempt.submitted_at
                  ).toFixed(2)
                ),

              date:
                formatDate(
                  attempt.submitted_at ??
                    attempt.started_at ??
                    attempt.created_at
                ),

              rawDate:
                attempt.submitted_at ??
                attempt.started_at ??
                attempt.created_at,

              status:
                String(
                  attempt.status ??
                    "Submitted"
                ),
            };
          }
        )
        .reverse();

    /* ========================================================
       MY TESTS
    ======================================================== */

    const myTests =
      attempts.map(
        (
          attempt: any,
          index: number
        ) => {
          const analytics =
            attemptAnalytics.get(
              String(
                attempt.id
              )
            );

          const testId =
            attempt.resolved_test_id ??
            null;

          const name =
            testId
              ? String(
                  testId
                )
              : `Test ${
                  index + 1
                }`;

          return {
            id: testId
              ? String(
                  testId
                )
              : null,

            attemptId:
              String(
                attempt.id
              ),

            name,

            title:
              name,

            exam:
              String(
                attempt.test_exam ??
                  "MHT-CET"
              ),

            paperId:
              null,

            paperCode:
              null,

            questionCount:
              analytics?.total ??
              Number(
                attempt.test_question_count ??
                  0
              ),

            durationConfigured:
              0,

            createdAt:
              attempt.created_at ??
              attempt.started_at ??
              null,

            startedAt:
              attempt.started_at ??
              null,

            submittedAt:
              attempt.submitted_at ??
              null,

            status:
              String(
                attempt.status ??
                  "Not Started"
              ),

            score:
              attempt.score ===
              null
                ? null
                : Number(
                    attempt.score ??
                      0
                  ),

            totalMarks:
              Number(
                attempt.total_marks ??
                  0
              ),

            correct:
              analytics?.correct ??
              Number(
                attempt.correct_count ??
                  0
              ),

            wrong:
              analytics?.wrong ??
              Number(
                attempt.incorrect_count ??
                  0
              ),

            unanswered:
              analytics?.unanswered ??
              Number(
                attempt.unanswered_count ??
                  0
              ),

            attempted:
              analytics?.attempted ??
              0,

            durationMinutes:
              Number(
                getDurationMinutes(
                  attempt.started_at,
                  attempt.submitted_at
                ).toFixed(2)
              ),

            duration:
              formatDuration(
                getDurationMinutes(
                  attempt.started_at,
                  attempt.submitted_at
                )
              ),
          };
        }
      );

    /* ========================================================
       SCHEDULED TESTS
    ======================================================== */

    const scheduledTestsResult =
      await client.query(
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
LEFT JOIN batch_students bs
  ON bs.batch_id = st.batch_id
 AND bs.student_id = $1

WHERE (
  st.batch_id IS NULL
  OR bs.student_id = $1
)

        ORDER BY st.start_time ASC
        `,
        [studentId]
      );

    const scheduledTests =
      scheduledTestsResult.rows;
console.log(
  "SCHEDULED TESTS FROM DB:",
  scheduledTests
);
    /* ========================================================
       TEST SUMMARY ARRAYS
    ======================================================== */

    const activeTests: any[] =
      [];

    const upcomingTests: any[] =
      [];

    const completedTests: any[] =
      [];

    const missedTests: any[] =
      [];

    /* ========================================================
       COMPLETED TESTS
    ======================================================== */

    for (
      const attempt of
        completedAttempts
    ) {
      const analytics =
        attemptAnalytics.get(
          String(
            attempt.id
          )
        );

      const testId =
        attempt.resolved_test_id
          ? String(
              attempt.resolved_test_id
            )
          : null;

      const questionCount =
        analytics?.total ??
        Number(
          attempt.test_question_count ??
            0
        );

      const attempted =
        analytics?.attempted ??
        Number(
          attempt.correct_count ??
            0
        ) +
          Number(
            attempt.incorrect_count ??
              0
          );

      const correct =
        analytics?.correct ??
        Number(
          attempt.correct_count ??
            0
        );

      const wrong =
        analytics?.wrong ??
        Number(
          attempt.incorrect_count ??
            0
        );

      const unanswered =
        analytics?.unanswered ??
        Number(
          attempt.unanswered_count ??
            0
        );

      const accuracy =
        attempted > 0
          ? Number(
              (
                (correct /
                  attempted) *
                100
              ).toFixed(2)
            )
          : 0;

      completedTests.push({
        id: testId,

        attemptId:
          String(
            attempt.id
          ),

        difficulty:
          getTestDifficulty(
            attempt.test_questions
          ),

        name:
          testId ??
          "MHT-CET Test",

        title:
          testId ??
          "MHT-CET Test",

        exam:
          String(
            attempt.test_exam ??
              "MHT-CET"
          ),

        status:
          "Completed",

        questionCount,

        questions:
          questionCount,

        score:
          Number(
            attempt.score ?? 0
          ),

        totalMarks:
          Number(
            attempt.total_marks ??
              0
          ),

        accuracy,

        correct,

        wrong,

        unanswered,

        attempted,

        startedAt:
          attempt.started_at ??
          null,

        completedAt:
          attempt.submitted_at ??
          null,

        completedDate:
          formatDate(
            attempt.submitted_at ??
              attempt.started_at ??
              attempt.created_at
          ),

        completedDateTime:
          formatDateTime(
            attempt.submitted_at ??
              attempt.started_at ??
              attempt.created_at
          ),

        durationMinutes:
          Number(
            getDurationMinutes(
              attempt.started_at,
              attempt.submitted_at
            ).toFixed(2)
          ),

        duration:
          formatDuration(
            getDurationMinutes(
              attempt.started_at,
              attempt.submitted_at
            )
          ),

        description:
          "Completed test",

        comments:
          "",
      });
    }

    /* ========================================================
       ACTIVE ATTEMPTS
    ======================================================== */

    for (
      const attempt of
        attempts
    ) {
      if (
        isCompletedStatus(
          attempt.status
        )
      ) {
        continue;
      }

      const testId =
        attempt.resolved_test_id
          ? String(
              attempt.resolved_test_id
            )
          : null;

      activeTests.push({
        id: testId,

        attemptId:
          String(
            attempt.id
          ),

        difficulty:
          getTestDifficulty(
            attempt.test_questions
          ),

        name:
          testId ??
          "MHT-CET Test",

        title:
          testId ??
          "MHT-CET Test",

        exam:
          String(
            attempt.test_exam ??
              "MHT-CET"
          ),

        status:
          "Active",

        questionCount:
          Number(
            attempt.test_question_count ??
              0
          ),

        questions:
          Number(
            attempt.test_question_count ??
              0
          ),

        startedAt:
          attempt.started_at ??
          null,

        startTime:
          formatDateTime(
            attempt.started_at
          ),

        endTime:
          null,

        duration:
          "Not configured",

        description:
          "Test available to complete.",

        comments:
          "",
      });
    }

    /* ========================================================
       COMPLETED TEST IDS
    ======================================================== */

    const completedTestIds =
      new Set(
        completedAttempts
          .map(
            (attempt: any) =>
              attempt.resolved_test_id
                ? String(
                    attempt.resolved_test_id
                  )
                : null
          )
          .filter(
            Boolean
          )
      );

    /* ========================================================
       SCHEDULED TEST CLASSIFICATION
    ======================================================== */

    const now =
      Date.now();

    for (
      const scheduled of
        scheduledTests
    ) {
      const scheduledId =
        String(
          scheduled.id
        );

      /* ------------------------------------------------------
         Already completed
      ------------------------------------------------------ */

      if (
        completedTestIds.has(
          scheduledId
        )
      ) {
        continue;
      }

      const startTime =
        scheduled.start_time
          ? new Date(
              scheduled.start_time
            ).getTime()
          : NaN;

      const endTime =
        scheduled.end_time
          ? new Date(
              scheduled.end_time
            ).getTime()
          : NaN;

      const durationMinutes =
        Number(
          scheduled.duration_minutes ??
            scheduled.paper_duration ??
            0
        );

      const test = {
        id:
          scheduledId,

        scheduledTestId:
          scheduledId,

        paperId:
          scheduled.paper_id
            ? String(
                scheduled.paper_id
              )
            : null,

        batchId:
          scheduled.batch_id
            ? String(
                scheduled.batch_id
              )
            : null,

        name:
          String(
            scheduled.title ??
              scheduled.paper_code ??
              scheduled.paper_id ??
              "Scheduled Test"
          ),

        title:
          String(
            scheduled.title ??
              scheduled.paper_code ??
              scheduled.paper_id ??
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

        status:
          String(
            scheduled.scheduled_status ??
              "Scheduled"
          ),

        startTime:
          scheduled.start_time
            ? formatDateTime(
                scheduled.start_time
              )
            : "",

        endTime:
          scheduled.end_time
            ? formatDateTime(
                scheduled.end_time
              )
            : "",

        startAt:
          scheduled.start_time ??
          null,

        endAt:
          scheduled.end_time ??
          null,

        startTimestamp:
          Number.isFinite(
            startTime
          )
            ? startTime
            : null,

        endTimestamp:
          Number.isFinite(
            endTime
          )
            ? endTime
            : null,

        durationMinutes,

        duration:
          durationMinutes > 0
            ? formatDuration(
                durationMinutes
              )
            : "Not configured",

        questionCount:
          0,

        questions:
          0,

        score:
          null,

        attempted:
          0,

        correct:
          0,

        wrong:
          0,

        unanswered:
          0,

        accuracy:
          0,

        comments:
          "",
      };

      /* ------------------------------------------------------
         UPCOMING
      ------------------------------------------------------ */

      if (
        Number.isFinite(
          startTime
        ) &&
        now < startTime
      ) {
        upcomingTests.push({
          ...test,

          status:
            "Upcoming",
        });

        continue;
      }

      /* ------------------------------------------------------
         MISSED
      ------------------------------------------------------ */

      if (
        Number.isFinite(
          endTime
        ) &&
        now > endTime
      ) {
        missedTests.push({
          ...test,

          status:
            "Missed",
        });

        continue;
      }

      /* ------------------------------------------------------
         ACTIVE
      ------------------------------------------------------ */

      activeTests.push({
        ...test,

        status:
          "Active",
      });
    }

    /* ========================================================
       TEST SUMMARY
    ======================================================== */

    const testSummary = {
      all: [
        ...activeTests,
        ...upcomingTests,
        ...completedTests,
        ...missedTests,
      ],

      active:
        activeTests,

      upcoming:
        upcomingTests,

      completed:
        completedTests,

      missed:
        missedTests,

      counts: {
        active:
          activeTests.length,

        upcoming:
          upcomingTests.length,

        completed:
          completedTests.length,

        missed:
          missedTests.length,

        total:
          activeTests.length +
          upcomingTests.length +
          completedTests.length +
          missedTests.length,
      },
    };

    /* ========================================================
       LATEST TEST
    ======================================================== */

    const latestTest =
      results.length > 0
        ? results[
            results.length - 1
          ]
        : null;

    /* ========================================================
       FINAL RESPONSE
    ======================================================== */

    return NextResponse.json({
      success: true,

      /* ------------------------------------------------------
         STUDENT
      ------------------------------------------------------ */

      student: {
        id:
          String(
            student.id
          ),

        name:
          String(
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

      /* ------------------------------------------------------
         STATISTICS
      ------------------------------------------------------ */

      statistics: {
        testsTaken,

        averageScore,

        bestScore,

        lowestScore,

        attempts:
          totalAttempts,

        totalAttempts,

        totalQuestions,

        totalAttempted,

        totalCorrect,

        totalWrong,

        totalUnanswered,

        accuracy:
          overallAccuracy,

        overallAccuracy,

        studyTimeMinutes:
          Number(
            totalStudyMinutes.toFixed(
              2
            )
          ),

        studyTime:
          formatDuration(
            totalStudyMinutes
          ),

        consistency,
      },

      /* ------------------------------------------------------
         ANALYTICS
      ------------------------------------------------------ */

      performanceTrend,

      scoreDistribution,

      subjectPerformance,

      chapterPerformance,

      weakAreas,

      /* ------------------------------------------------------
         RESULTS
      ------------------------------------------------------ */

      results,

      myTests,

      latestTest,

      /* ------------------------------------------------------
         TEST SUMMARY
      ------------------------------------------------------ */

      testSummary,

      activeTests,

      upcomingTests,

      completedTests,

      missedTests,

      /* ------------------------------------------------------
         DASHBOARD COMPATIBILITY
      ------------------------------------------------------ */

      tests:
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
    if (client) {
      client.release();
    }
  }
}