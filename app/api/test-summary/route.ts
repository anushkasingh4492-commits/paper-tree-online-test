
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
   SESSION
============================================================ */

function getStudentId(request: NextRequest): string {
  const cookie =
    request.cookies.get("student_session")?.value;

  if (!cookie) {
    return "";
  }

  try {
    const parsed = JSON.parse(cookie);

    if (
      parsed &&
      typeof parsed === "object" &&
      parsed.studentId
    ) {
      return String(parsed.studentId).trim();
    }
  } catch {
    // Cookie may simply contain the student ID.
  }

  return cookie.trim();
}

/* ============================================================
   HELPERS
============================================================ */

function formatDateTime(value: unknown): string {
  if (!value) return "";

  const date = new Date(String(value));

  if (Number.isNaN(date.getTime())) {
    return "";
  }

  return date.toLocaleString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatDate(value: unknown): string {
  if (!value) return "";

  const date = new Date(String(value));

  if (Number.isNaN(date.getTime())) {
    return "";
  }

  return date.toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

function formatDuration(minutes: number): string {
  if (!Number.isFinite(minutes) || minutes <= 0) {
    return "0m";
  }

  const rounded = Math.round(minutes);

  const hours = Math.floor(rounded / 60);
  const mins = rounded % 60;

  if (hours === 0) {
    return `${mins}m`;
  }

  if (mins === 0) {
    return `${hours}h`;
  }

  return `${hours}h ${mins}m`;
}

function getDurationMinutes(
  startedAt: unknown,
  submittedAt: unknown
): number {
  if (!startedAt || !submittedAt) {
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

  return (end - start) / 60000;
}

function normalizeStatus(value: unknown): string {
  return String(value ?? "")
    .trim()
    .toUpperCase()
    .replace(/-/g, "_")
    .replace(/\s+/g, "_");
}

function isCompletedStatus(value: unknown): boolean {
  const status = normalizeStatus(value);

  return (
    status === "SUBMITTED" ||
    status === "AUTO_SUBMITTED" ||
    status === "COMPLETED" ||
    status === "FINISHED"
  );
}

function isInProgressStatus(value: unknown): boolean {
  const status = normalizeStatus(value);

  return (
    status === "IN_PROGRESS" ||
    status === "STARTED" ||
    status === "ONGOING"
  );
}

/* ============================================================
   GET
============================================================ */

export async function GET(
  request: NextRequest
) {
  const pool = getPool();
  const client = await pool.connect();

  try {
    /* ========================================================
       STUDENT SESSION
    ======================================================== */

    const studentId = getStudentId(request);

    if (!studentId) {
      return NextResponse.json(
        {
          success: false,
          error: "Student session not found.",
        },
        { status: 401 }
      );
    }

    /* ========================================================
       STUDENT
    ======================================================== */

    const studentResult = await client.query(
      `
      SELECT
        id,
        name,
        email,
        roll_number,
        class_name,
        created_at
      FROM students
      WHERE id = $1
      LIMIT 1
      `,
      [studentId]
    );

    if (studentResult.rows.length === 0) {
      return NextResponse.json(
        {
          success: false,
          error: "Student not found.",
        },
        { status: 404 }
      );
    }

    const student = studentResult.rows[0];

    /* ========================================================
       REAL ATTEMPTS

       IMPORTANT:

       Your real database contains an attempt like:

       test_id = NULL
       scheduled_test_id = test-1787481354334

       Therefore we do NOT depend on tests.id being present.
    ======================================================== */

    const attemptsResult = await client.query(
      `
      SELECT
        ta.id AS attempt_id,
        ta.test_id,
        ta.scheduled_test_id,
        ta.student_id,
        ta.status,
        ta.score,
        ta.total_marks,
        ta.correct_count,
        ta.incorrect_count,
        ta.unanswered_count,
        ta.started_at,
        ta.submitted_at,
        ta.created_at,

        t.exam,
        t.question_count,
        t.questions,

        st.title AS scheduled_title,
        st.paper_id AS scheduled_paper_id,
        st.batch_id AS scheduled_batch_id,
        st.start_time AS scheduled_start_time,
        st.end_time AS scheduled_end_time,
        st.duration_minutes AS scheduled_duration_minutes

      FROM test_attempts ta

      LEFT JOIN tests t
        ON t.id = ta.test_id

      LEFT JOIN scheduled_tests st
        ON st.id = ta.scheduled_test_id

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

    const attempts = attemptsResult.rows;

    /* ========================================================
       COMPLETED TESTS
    ======================================================== */

    const completedTests = attempts
      .filter((attempt) =>
        isCompletedStatus(attempt.status)
      )
      .map((attempt) => {
        const correct = Number(
          attempt.correct_count ?? 0
        );

        const incorrect = Number(
          attempt.incorrect_count ?? 0
        );

        const unanswered = Number(
          attempt.unanswered_count ?? 0
        );

        const attempted =
          correct + incorrect;

        const accuracy =
          attempted > 0
            ? Number(
                (
                  (correct / attempted) *
                  100
                ).toFixed(2)
              )
            : 0;

        const durationMinutes =
          getDurationMinutes(
            attempt.started_at,
            attempt.submitted_at
          );

        /*
         * Prefer the actual test question count.
         *
         * If tests.test_id is unavailable, use:
         * correct + incorrect + unanswered.
         *
         * This is important for your real attempt.
         */
        let questionCount = Number(
          attempt.question_count ?? 0
        );

        if (questionCount <= 0) {
          questionCount =
            correct +
            incorrect +
            unanswered;
        }

        /*
         * If we have JSON questions and still don't
         * have a question count, derive it.
         */
        if (
          questionCount <= 0 &&
          Array.isArray(attempt.questions)
        ) {
          questionCount =
            attempt.questions.length;
        }

        /*
         * Name priority:
         *
         * 1. Scheduled test title
         * 2. Exam + question count
         * 3. Generic Test
         */
        const exam =
          attempt.exam ||
          "MHT-CET";

        const name =
          attempt.scheduled_title ||
          `${exam} Test • ${questionCount} Questions`;

        return {
          id: String(
            attempt.test_id ??
              attempt.scheduled_test_id ??
              attempt.attempt_id
          ),

          attemptId: String(
            attempt.attempt_id
          ),

          name,

          exam: String(exam),

          status: "Completed",

          questionCount,

          startTime:
            attempt.started_at,

          endTime:
            attempt.submitted_at,

          description:
            attempt.scheduled_title
              ? `Scheduled test: ${attempt.scheduled_title}`
              : null,

          comment: null,

          score:
            attempt.score === null ||
            attempt.score === undefined
              ? null
              : Number(attempt.score),

          totalMarks:
            attempt.total_marks === null ||
            attempt.total_marks === undefined
              ? null
              : Number(
                  attempt.total_marks
                ),

          correct,

          incorrect,

          unanswered,

          durationMinutes: Number(
            durationMinutes.toFixed(2)
          ),

          accuracy,

          attempted,

          date: formatDate(
            attempt.submitted_at ??
              attempt.started_at
          ),

          startedAtFormatted:
            formatDateTime(
              attempt.started_at
            ),

          submittedAtFormatted:
            formatDateTime(
              attempt.submitted_at
            ),

          duration: formatDuration(
            durationMinutes
          ),
        };
      });

    /* ========================================================
       IN-PROGRESS ATTEMPTS
    ======================================================== */

    const inProgressTests = attempts
      .filter((attempt) =>
        isInProgressStatus(
          attempt.status
        )
      )
      .map((attempt) => {
        const correct = Number(
          attempt.correct_count ?? 0
        );

        const incorrect = Number(
          attempt.incorrect_count ?? 0
        );

        const unanswered = Number(
          attempt.unanswered_count ?? 0
        );

        let questionCount = Number(
          attempt.question_count ?? 0
        );

        if (questionCount <= 0) {
          questionCount =
            correct +
            incorrect +
            unanswered;
        }

        const exam =
          attempt.exam ||
          "MHT-CET";

        return {
          id: String(
            attempt.test_id ??
              attempt.scheduled_test_id ??
              attempt.attempt_id
          ),

          attemptId: String(
            attempt.attempt_id
          ),

          name:
            attempt.scheduled_title ||
            `${exam} Test • ${questionCount} Questions`,

          exam: String(exam),

          status: "In Progress",

          questionCount,

          startTime:
            attempt.started_at,

          endTime:
            attempt.submitted_at,

          description:
            attempt.scheduled_title
              ? `Scheduled test: ${attempt.scheduled_title}`
              : null,

          comment: null,

          score: null,

          totalMarks:
            attempt.total_marks === null ||
            attempt.total_marks === undefined
              ? null
              : Number(
                  attempt.total_marks
                ),

          correct,

          incorrect,

          unanswered,

          durationMinutes:
            getDurationMinutes(
              attempt.started_at,
              new Date().toISOString()
            ),

          date: formatDate(
            attempt.started_at
          ),
        };
      });

    /* ========================================================
       SCHEDULED TESTS

       These are the actual records currently present
       in scheduled_tests.

       We do NOT create fake upcoming/missed tests.
    ======================================================== */

  const scheduledResult =
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
      st.status,
      st.created_at
    FROM scheduled_tests st
    WHERE
      (
        st.batch_id IS NOT NULL
        AND EXISTS (
          SELECT 1
          FROM batch_students bs
          WHERE bs.batch_id = st.batch_id
            AND bs.student_id = $1
        )
      )
      OR
      (
        st.batch_id IS NULL
        AND EXISTS (
          SELECT 1
          FROM scheduled_test_students sts
          WHERE sts.scheduled_test_id = st.id
            AND sts.student_id = $1
        )
      )
    ORDER BY st.start_time ASC
    `,
    [studentId]
  );

    const scheduledTests =
      scheduledResult.rows;

    /* ========================================================
       STUDENT ASSIGNMENTS
    ======================================================== */

    const assignmentResult =
      await client.query(
        `
        SELECT
          id,
          student_id,
          test_id,
          created_at
        FROM student_tests
        WHERE student_id = $1
        `,
        [studentId]
      );

    const assignments =
      assignmentResult.rows;

    const assignedTestIds = new Set(
      assignments.map((item) =>
        String(item.test_id)
      )
    );

    /* ========================================================
       COMPLETED SCHEDULED IDs

       Used so a completed scheduled test doesn't appear
       again as upcoming/missed.
    ======================================================== */

    const completedScheduledIds =
      new Set(
        attempts
          .filter((attempt) =>
            isCompletedStatus(
              attempt.status
            )
          )
          .flatMap((attempt) => {
            const ids: string[] = [];

            if (attempt.test_id) {
              ids.push(
                String(attempt.test_id)
              );
            }

            if (
              attempt.scheduled_test_id
            ) {
              ids.push(
                String(
                  attempt.scheduled_test_id
                )
              );
            }

            return ids;
          })
      );

    /* ========================================================
       SCHEDULE CLASSIFICATION
    ======================================================== */

    const now = Date.now();

    const upcomingTests: TestSummaryItem[] =
      [];

    const missedTests: TestSummaryItem[] =
      [];

    for (const test of scheduledTests) {
      const testId = String(test.id);

      const paperId = test.paper_id
        ? String(test.paper_id)
        : "";

      /*
       * If student assignments exist, only show
       * tests assigned to this student.
       *
       * If there are no assignments at all, we don't
       * expose scheduled tests automatically.
       */
      if (
        assignments.length > 0 &&
        !assignedTestIds.has(testId) &&
        (!paperId ||
          !assignedTestIds.has(paperId))
      ) {
        continue;
      }

      /*
       * Don't duplicate a completed test.
       */
      if (
        completedScheduledIds.has(
          testId
        ) ||
        (paperId &&
          completedScheduledIds.has(
            paperId
          ))
      ) {
        continue;
      }

      const start = new Date(
        String(test.start_time)
      ).getTime();

      const end = new Date(
        String(test.end_time)
      ).getTime();

      if (
        !Number.isFinite(start) ||
        !Number.isFinite(end)
      ) {
        continue;
      }

      const questionCount = 0;

      const base: TestSummaryItem = {
        id: testId,

        name:
          String(test.title) ||
          "Scheduled Test",

        exam: "MHT-CET",

        status:
          now < start
            ? "Upcoming"
            : "Missed",

        questionCount,

        startTime:
          test.start_time,

        endTime:
          test.end_time,

        description: null,

        comment: null,

        score: null,

        totalMarks: null,

        correct: null,

        incorrect: null,

        unanswered: null,

        durationMinutes:
          Number(
            test.duration_minutes ?? 0
          ),
      };

      /*
       * Future
       */
      if (now < start) {
        upcomingTests.push(base);
        continue;
      }

      /*
       * Expired
       */
      if (now > end) {
        missedTests.push(base);
      }
    }

    /* ========================================================
       SORT
    ======================================================== */

    upcomingTests.sort(
      (a, b) =>
        new Date(
          String(a.startTime)
        ).getTime() -
        new Date(
          String(b.startTime)
        ).getTime()
    );

    missedTests.sort(
      (a, b) =>
        new Date(
          String(b.endTime)
        ).getTime() -
        new Date(
          String(a.endTime)
        ).getTime()
    );

    /* ========================================================
       COMBINE FOR FRONTEND
    ======================================================== */

    const tests: TestSummaryItem[] = [
      ...completedTests,
      ...inProgressTests,
      ...missedTests,
      ...upcomingTests,
    ];

    /* ========================================================
       SUMMARY

       This matches the EXACT shape expected by
       app/test-summary/page.tsx.
    ======================================================== */

    const summary = {
      total: tests.length,

      taken:
        completedTests.length,

      missed:
        missedTests.length,

      upcoming:
        upcomingTests.length,
    };

    /* ========================================================
       RESPONSE
    ======================================================== */

    return NextResponse.json({
      success: true,

      student: {
        id: String(student.id),

        name:
          String(
            student.name ?? "Student"
          ),

        rollNumber:
          student.roll_number ??
          null,

        email:
          student.email ??
          null,
      },

      summary,

      tests,

      /*
       * Keep these too for debugging / future frontend
       * features. They don't hurt the current page.
       */
      counts: {
        active: inProgressTests.length,

        upcoming:
          upcomingTests.length,

        completed:
          completedTests.length,

        missed:
          missedTests.length,

        total: tests.length,
      },

      activeTests:
        inProgressTests,

      upcomingTests,

      completedTests,

      missedTests,

      meta: {
        generatedAt:
          new Date().toISOString(),

        hasScheduledTests:
          scheduledTests.length > 0,

        hasAssignments:
          assignments.length > 0,

        hasCompletedTests:
          completedTests.length > 0,

        hasInProgressTests:
          inProgressTests.length > 0,

        studentId: String(
          student.id
        ),
      },
    });
  } catch (error) {
    console.error(
      "TEST SUMMARY API ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,

        error:
          error instanceof Error
            ? error.message
            : "Failed to load test summary.",
      },
      {
        status: 500,
      }
    );
  } finally {
    client.release();
  }
}

/* ============================================================
   TYPE
============================================================ */

type TestSummaryItem = {
  id: string;
  attemptId?: string | null;

  name: string;
  exam?: string | null;

  status:
    | "Upcoming"
    | "Missed"
    | "Completed"
    | "In Progress"
    | string;

  questionCount: number;

  startTime?: string | null;
  endTime?: string | null;

  description?: string | null;
  comment?: string | null;

  score?: number | null;
  totalMarks?: number | null;

  correct?: number | null;
  incorrect?: number | null;
  unanswered?: number | null;

  durationMinutes?: number | null;

  accuracy?: number | null;
  attempted?: number | null;

  date?: string | null;

  startedAtFormatted?: string | null;
  submittedAtFormatted?: string | null;
  duration?: string | null;
};

