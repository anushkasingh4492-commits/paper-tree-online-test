import { NextRequest, NextResponse } from "next/server";
import { Pool } from "pg";

export const dynamic = "force-dynamic";
export const revalidate = 0;

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
  const cookie = request.cookies.get("student_session")?.value;

  if (!cookie) {
    return "";
  }

  try {
    const parsed = JSON.parse(cookie);

    if (
      parsed &&
      typeof parsed === "object" &&
      parsed.studentId !== undefined &&
      parsed.studentId !== null
    ) {
      return String(parsed.studentId).trim();
    }
  } catch {
    // Cookie can directly contain the student ID.
  }

  return cookie.trim();
}

function getStudentAcademyId(request: NextRequest): string {
  const cookie = request.cookies.get("student_session")?.value;

  if (!cookie) return "";

  try {
    const parsed = JSON.parse(cookie);
    return String(parsed?.academyId ?? "").trim();
  } catch {
    return "";
  }
}

/* ============================================================
   UUID
============================================================ */

function isUuid(value: string): boolean {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(
    value
  );
}

/* ============================================================
   STATUS
============================================================ */

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
   HELPERS
============================================================ */

function safeNumber(value: unknown, fallback = 0): number {
  const number = Number(value);

  return Number.isFinite(number) ? number : fallback;
}

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

  const start = new Date(String(startedAt)).getTime();
  const end = new Date(String(submittedAt)).getTime();

  if (
    !Number.isFinite(start) ||
    !Number.isFinite(end) ||
    end <= start
  ) {
    return 0;
  }

  return (end - start) / 60000;
}

function getQuestionCount(attempt: any): number {
  let count = safeNumber(attempt.question_count, 0);

  if (count > 0) {
    return count;
  }

  const correct = safeNumber(attempt.correct_count, 0);
  const incorrect = safeNumber(attempt.incorrect_count, 0);
  const unanswered = safeNumber(attempt.unanswered_count, 0);

  count = correct + incorrect + unanswered;

  if (count > 0) {
    return count;
  }

  if (Array.isArray(attempt.questions)) {
    return attempt.questions.length;
  }

  return 0;
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

/* ============================================================
   GET
============================================================ */

export async function GET(request: NextRequest) {
  const pool = getPool();
  const client = await pool.connect();

  try {
    /* ========================================================
       STUDENT SESSION
    ======================================================== */

    const studentId = getStudentId(request);
    const academyId = getStudentAcademyId(request);

    if (!studentId || !academyId) {
      return NextResponse.json(
        {
          success: false,
          error: "Student session not found.",
        },
        { status: 401 }
      );
    }

    if (!isUuid(studentId)) {
      return NextResponse.json(
        {
          success: false,
          error: "Invalid student session.",
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
        academy_id,
        created_at
      FROM students
      WHERE id::text = $1::text
        AND academy_id::text = $2::text
      LIMIT 1
      `,
      [studentId, academyId]
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
       ATTEMPTS
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
        ON t.id::text = ta.test_id::text

      LEFT JOIN scheduled_tests st
        ON st.id::text = ta.scheduled_test_id::text
        AND st.academy_id::text = $2::text

      WHERE ta.student_id::text = $1::text
        AND (
          t.academy_id::text = $2::text
          OR st.academy_id::text = $2::text
        )

      ORDER BY
        COALESCE(
          ta.submitted_at,
          ta.started_at,
          ta.created_at
        ) DESC
      `,
      [studentId, academyId]
    );

    const attempts = attemptsResult.rows;

    /* ========================================================
       COMPLETED
    ======================================================== */

    const completedTests: TestSummaryItem[] = attempts
      .filter((attempt) => isCompletedStatus(attempt.status))
      .map((attempt) => {
        const correct = safeNumber(attempt.correct_count);
        const incorrect = safeNumber(attempt.incorrect_count);
        const unanswered = safeNumber(attempt.unanswered_count);

        const attempted = correct + incorrect;

        const accuracy =
          attempted > 0
            ? Number(((correct / attempted) * 100).toFixed(2))
            : 0;

        const durationMinutes = getDurationMinutes(
          attempt.started_at,
          attempt.submitted_at
        );

        const questionCount = getQuestionCount(attempt);

        const exam =
          String(attempt.exam || "MHT-CET").trim() || "MHT-CET";

        const name =
          String(attempt.scheduled_title || "").trim() ||
          `${exam} Test • ${questionCount} Questions`;

        return {
          id: String(
            attempt.test_id ??
              attempt.scheduled_test_id ??
              attempt.attempt_id
          ),

          attemptId: String(attempt.attempt_id),

          name,

          exam,

          status: "Completed",

          questionCount,

          startTime: attempt.started_at ?? null,

          endTime: attempt.submitted_at ?? null,

          description: attempt.scheduled_title
            ? `Scheduled test: ${attempt.scheduled_title}`
            : null,

          comment: null,

          score:
            attempt.score === null ||
            attempt.score === undefined
              ? null
              : safeNumber(attempt.score),

          totalMarks:
            attempt.total_marks === null ||
            attempt.total_marks === undefined
              ? null
              : safeNumber(attempt.total_marks),

          correct,

          incorrect,

          unanswered,

          durationMinutes: Number(
            durationMinutes.toFixed(2)
          ),

          accuracy,

          attempted,

          date: formatDate(
            attempt.submitted_at ?? attempt.started_at
          ),

          startedAtFormatted: formatDateTime(
            attempt.started_at
          ),

          submittedAtFormatted: formatDateTime(
            attempt.submitted_at
          ),

          duration: formatDuration(durationMinutes),
        };
      });

    /* ========================================================
       IN PROGRESS
    ======================================================== */

    const inProgressTests: TestSummaryItem[] = attempts
      .filter((attempt) =>
        isInProgressStatus(attempt.status)
      )
      .map((attempt) => {
        const correct = safeNumber(attempt.correct_count);
        const incorrect = safeNumber(attempt.incorrect_count);
        const unanswered = safeNumber(attempt.unanswered_count);

        const questionCount = getQuestionCount(attempt);

        const exam =
          String(attempt.exam || "MHT-CET").trim() || "MHT-CET";

        const durationMinutes = getDurationMinutes(
          attempt.started_at,
          new Date().toISOString()
        );

        return {
          id: String(
            attempt.test_id ??
              attempt.scheduled_test_id ??
              attempt.attempt_id
          ),

          attemptId: String(attempt.attempt_id),

          name:
            String(attempt.scheduled_title || "").trim() ||
            `${exam} Test • ${questionCount} Questions`,

          exam,

          status: "In Progress",

          questionCount,

          startTime: attempt.started_at ?? null,

          endTime: attempt.submitted_at ?? null,

          description: attempt.scheduled_title
            ? `Scheduled test: ${attempt.scheduled_title}`
            : null,

          comment: null,

          score: null,

          totalMarks:
            attempt.total_marks === null ||
            attempt.total_marks === undefined
              ? null
              : safeNumber(attempt.total_marks),

          correct,

          incorrect,

          unanswered,

          durationMinutes: Number(
            durationMinutes.toFixed(2)
          ),

          date: formatDate(attempt.started_at),

          startedAtFormatted: formatDateTime(
            attempt.started_at
          ),

          submittedAtFormatted: formatDateTime(
            attempt.submitted_at
          ),

          duration: formatDuration(durationMinutes),
        };
      });

    /* ========================================================
       ASSIGNMENTS
    ======================================================== */

    const assignmentResult = await client.query(
      `
      SELECT
        id,
        student_id,
        test_id,
        created_at
      FROM student_tests
      WHERE student_id::text = $1::text
      `,
      [studentId]
    );

    const assignments = assignmentResult.rows;

    const assignedTestIds = new Set(
      assignments
        .filter(
          (item) =>
            item.test_id !== null &&
            item.test_id !== undefined
        )
        .map((item) => String(item.test_id))
    );

    /* ========================================================
       SCHEDULED TESTS
    ======================================================== */

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
        st.status,
        st.created_at
      FROM scheduled_tests st
      WHERE
        st.academy_id::text = $2::text
        AND (
          (
            st.batch_id IS NOT NULL
            AND EXISTS (
              SELECT 1
              FROM batch_students bs
              WHERE bs.batch_id::text = st.batch_id::text
                AND bs.student_id::text = $1::text
            )
          )
          OR
          (
            st.batch_id IS NULL
            AND EXISTS (
              SELECT 1
              FROM scheduled_test_students sts
              WHERE sts.scheduled_test_id::text = st.id::text
                AND sts.student_id::text = $1::text
            )
          )
        )
      ORDER BY st.start_time ASC
      `,
      [studentId, academyId]
    );

    const scheduledTests = scheduledResult.rows;

    /* ========================================================
       COMPLETED IDS
    ======================================================== */

    const completedTestIds = new Set<string>();

    for (const attempt of attempts) {
      if (!isCompletedStatus(attempt.status)) {
        continue;
      }

      if (
        attempt.test_id !== null &&
        attempt.test_id !== undefined
      ) {
        completedTestIds.add(String(attempt.test_id));
      }

      if (
        attempt.scheduled_test_id !== null &&
        attempt.scheduled_test_id !== undefined
      ) {
        completedTestIds.add(
          String(attempt.scheduled_test_id)
        );
      }
    }

    /* ========================================================
       SCHEDULED CLASSIFICATION
    ======================================================== */

    const now = Date.now();

    const upcomingTests: TestSummaryItem[] = [];
    const missedTests: TestSummaryItem[] = [];

    for (const test of scheduledTests) {
      const testId = String(test.id);

      const paperId =
        test.paper_id !== null &&
        test.paper_id !== undefined
          ? String(test.paper_id)
          : "";

      /*
       * If explicit student assignments exist, respect them.
       * Otherwise batch membership controls visibility.
       */
      if (
        assignments.length > 0 &&
        !assignedTestIds.has(testId) &&
        (!paperId || !assignedTestIds.has(paperId))
      ) {
        continue;
      }

      /*
       * A completed scheduled test should not also appear
       * as Upcoming/Missed.
       */
      if (
        completedTestIds.has(testId) ||
        (paperId && completedTestIds.has(paperId))
      ) {
        continue;
      }

      const start = new Date(
        String(test.start_time)
      ).getTime();

      const end = new Date(
        String(test.end_time)
      ).getTime();

      if (!Number.isFinite(start)) {
        continue;
      }

      /*
       * Some scheduled tests may not have an end time.
       * In that case derive it from duration.
       */
      let effectiveEnd = end;

      if (
        !Number.isFinite(effectiveEnd) &&
        test.duration_minutes !== null &&
        test.duration_minutes !== undefined
      ) {
        const duration = safeNumber(
          test.duration_minutes
        );

        if (duration > 0) {
          effectiveEnd =
            start + duration * 60 * 1000;
        }
      }

      /*
       * If there is still no valid end time,
       * treat the test as upcoming until its start.
       */
      const questionCount = 0;

      const base: TestSummaryItem = {
        id: testId,

        name:
          String(test.title || "").trim() ||
          "Scheduled Test",

        exam: "MHT-CET",

        status:
          now < start
            ? "Upcoming"
            : Number.isFinite(effectiveEnd) &&
                now > effectiveEnd
              ? "Missed"
              : "In Progress",

        questionCount,

        startTime: test.start_time ?? null,

        endTime: Number.isFinite(effectiveEnd)
          ? new Date(effectiveEnd).toISOString()
          : test.end_time ?? null,

        description: null,

        comment: null,

        score: null,

        totalMarks: null,

        correct: null,

        incorrect: null,

        unanswered: null,

        durationMinutes: safeNumber(
          test.duration_minutes
        ),

        date: formatDate(test.start_time),
      };

      if (now < start) {
        upcomingTests.push(base);
        continue;
      }

      if (
        Number.isFinite(effectiveEnd) &&
        now > effectiveEnd
      ) {
        missedTests.push(base);
      }
    }

    /* ========================================================
       REMOVE DUPLICATE IN-PROGRESS SCHEDULED TESTS
    ======================================================== */

    const inProgressAttemptIds = new Set<string>();

    for (const attempt of attempts) {
      if (!isInProgressStatus(attempt.status)) {
        continue;
      }

      if (
        attempt.scheduled_test_id !== null &&
        attempt.scheduled_test_id !== undefined
      ) {
        inProgressAttemptIds.add(
          String(attempt.scheduled_test_id)
        );
      }
    }

    const filteredUpcomingTests =
      upcomingTests.filter(
        (test) =>
          !inProgressAttemptIds.has(
            String(test.id)
          )
      );

    const filteredMissedTests =
      missedTests.filter(
        (test) =>
          !inProgressAttemptIds.has(
            String(test.id)
          )
      );

    /* ========================================================
       SORT
    ======================================================== */

    completedTests.sort((a, b) => {
      const aTime = new Date(
        String(a.endTime ?? a.startTime ?? 0)
      ).getTime();

      const bTime = new Date(
        String(b.endTime ?? b.startTime ?? 0)
      ).getTime();

      return bTime - aTime;
    });

    inProgressTests.sort((a, b) => {
      const aTime = new Date(
        String(a.startTime ?? 0)
      ).getTime();

      const bTime = new Date(
        String(b.startTime ?? 0)
      ).getTime();

      return bTime - aTime;
    });

    filteredUpcomingTests.sort((a, b) => {
      const aTime = new Date(
        String(a.startTime ?? 0)
      ).getTime();

      const bTime = new Date(
        String(b.startTime ?? 0)
      ).getTime();

      return aTime - bTime;
    });

    filteredMissedTests.sort((a, b) => {
      const aTime = new Date(
        String(a.endTime ?? a.startTime ?? 0)
      ).getTime();

      const bTime = new Date(
        String(b.endTime ?? b.startTime ?? 0)
      ).getTime();

      return bTime - aTime;
    });

    /* ========================================================
       COMBINE
    ======================================================== */

    const tests: TestSummaryItem[] = [
      ...completedTests,
      ...inProgressTests,
      ...filteredMissedTests,
      ...filteredUpcomingTests,
    ];

    /* ========================================================
       SUMMARY
    ======================================================== */

    const summary = {
      total: tests.length,

      taken: completedTests.length,

      missed: filteredMissedTests.length,

      upcoming: filteredUpcomingTests.length,
    };

    /* ========================================================
       RESPONSE
    ======================================================== */

    return NextResponse.json(
      {
        success: true,

        student: {
          id: String(student.id),

          name: String(
            student.name ?? "Student"
          ),

          rollNumber:
            student.roll_number ?? null,

          email:
            student.email ?? null,
        },

        summary,

        tests,

        counts: {
          active: inProgressTests.length,

          upcoming:
            filteredUpcomingTests.length,

          completed:
            completedTests.length,

          missed:
            filteredMissedTests.length,

          total: tests.length,
        },

        activeTests: inProgressTests,

        upcomingTests:
          filteredUpcomingTests,

        completedTests,

        missedTests:
          filteredMissedTests,

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

          studentId: String(student.id),
        },
      },
      {
        status: 200,
        headers: {
          "Cache-Control":
            "no-store, no-cache, must-revalidate, proxy-revalidate",
          Pragma: "no-cache",
          Expires: "0",
        },
      }
    );
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