
import { NextRequest, NextResponse } from "next/server";
import { Pool } from "pg";
import { parseSessionCookie } from "@/lib/session";
import { getAcademyTier, hasTierFeature } from "@/lib/subscription";

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

type AnswerMap = Record<string, number | string | number[] | null>;

type QuestionAnswerData = {
  id?: unknown;
  question_id?: unknown;
  questionId?: unknown;
  question_type?: unknown;
  questionType?: unknown;
  answer_format?: unknown;
  tita_answer?: unknown;
  accepted_answers?: unknown;
  acceptedAnswers?: unknown;
  correct_option?: unknown;
  correctOption?: unknown;
  correct_answers?: unknown;
  correctAnswers?: unknown;
  correct_answer_text?: unknown;
  correct_answer?: unknown;
  answer?: unknown;
};

type MarkedMap = Record<string, boolean>;

type SubmitBody = {
  testId?: string;
  scheduledTestId?: string;
  studentId?: string;
  answers?: AnswerMap;
  answersByQuestion?: unknown[];
  marked?: MarkedMap;
  automatic?: boolean;
  reattempt?: boolean;
  violationCount?: number;
  startedAt?: string;
  submittedAt?: string;
  questionTimes?: Record<string, number>;
};

type EvaluatedAnswer = {
  questionId: string;
  selectedAnswer: number | number[] | string | null;
  isCorrect: boolean | null;
  marksAwarded: number;
  markedForReview: boolean;
};

/*
 * =========================================================
 * NORMALIZE ANSWER
 * =========================================================
 */

function normalizeAnswer(value: unknown): number | null {
  if (
    value === undefined ||
    value === null ||
    value === ""
  ) {
    return null;
  }

  if (
    typeof value === "number" &&
    Number.isFinite(value) &&
    Number.isInteger(value)
  ) {
    return value;
  }

  if (typeof value === "string") {
    const trimmed = value.trim();

    if (!trimmed) {
      return null;
    }

    const numericValue = Number(trimmed);

    if (
      Number.isFinite(numericValue) &&
      Number.isInteger(numericValue)
    ) {
      return numericValue;
    }

    const letter = trimmed.toUpperCase();

    if (/^[A-Z]$/.test(letter)) {
      return letter.charCodeAt(0) - 65;
    }
  }

  return null;
}

/*
 * =========================================================
 * GET CORRECT ANSWER
 * =========================================================
 */

function isTitaQuestion(question: QuestionAnswerData): boolean {
  return (
    String(question.question_type ?? question.questionType ?? question.answer_format ?? "")
      .trim()
      .toUpperCase() === "TITA"
  );
}

function normalizeTitaAnswer(value: unknown): string | null {
  if (typeof value === "number") {
    return Number.isFinite(value) ? String(value) : null;
  }

  if (typeof value !== "string") return null;

  let cleaned = value.trim();
  if (!cleaned) return null;

  // Accept plain numbers, $160$, \(160\), and \boxed{160}.
  cleaned = cleaned
    .replace(/^\\\(([\s\S]*)\\\)$/, "$1")
    .replace(/^\$([\s\S]*)\$$/, "$1")
    .replace(/^\\boxed\{([^{}]+)\}$/, "$1")
    .trim();

  // Remove commas only when they form valid thousands grouping.
  if (/^[+-]?\d{1,3}(?:,\d{3})+(?:\.\d+)?$/.test(cleaned)) {
    cleaned = cleaned.replace(/,/g, "");
  }

  if (/^[+-]?\d+(?:\.\d+)?$/.test(cleaned)) {
    const number = Number(cleaned);
    return Number.isFinite(number) ? String(number) : null;
  }

  return cleaned.toLocaleLowerCase().replace(/\s+/g, " ");
}

function isMultiSelectQuestion(question: QuestionAnswerData): boolean {
  return (
    String(question.question_type ?? question.questionType ?? "")
      .trim()
      .toUpperCase() === "MULTI_SELECT"
  );
}

function normalizeMultiSelectAnswer(
  value: unknown
): number[] | null {
  if (Array.isArray(value)) {
    const result: number[] = [];
    for (const item of value) {
      const n = normalizeAnswer(item);
      if (n !== null) result.push(n);
    }
    return result.length > 0 ? result : null;
  }

  if (typeof value === "string") {
    const trimmed = value.trim();
    if (!trimmed) return null;
    const parts = trimmed.split(/[,;\s]+/).filter(Boolean);
    const result: number[] = [];
    for (const part of parts) {
      const n = normalizeAnswer(part);
      if (n !== null) result.push(n);
    }
    return result.length > 0 ? result : null;
  }

  return null;
}

function getCorrectMultiSelectAnswer(
  question: QuestionAnswerData
): number[] | null {
  const raw =
    question.correct_option ??
    question.correctOption ??
    question.correct_answers ??
    question.correctAnswers ??
    null;

  if (raw === null || raw === undefined) return null;

  if (Array.isArray(raw)) {
    const result: number[] = [];
    for (const item of raw) {
      const n = normalizeAnswer(item);
      if (n !== null) result.push(n);
    }
    return result.length > 0 ? result : null;
  }

  return normalizeMultiSelectAnswer(raw);
}

function arraysEqual(a: number[] | null, b: number[] | null): boolean {
  if (a === null || b === null) return false;
  if (a.length !== b.length) return false;
  const sortedA = [...a].sort((x, y) => x - y);
  const sortedB = [...b].sort((x, y) => x - y);
  for (let i = 0; i < sortedA.length; i++) {
    if (sortedA[i] !== sortedB[i]) return false;
  }
  return true;
}

function isNumberArray(value: unknown): value is number[] {
  return Array.isArray(value) && value.every((item) => typeof item === "number");
}

function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((item) => typeof item === "string");
}

function getCorrectAnswer(
  question: QuestionAnswerData
): number | null {
  for (const candidate of [
    question.answer,
    question.correct_option,
    question.correctOption,
  ]) {
    if (candidate !== undefined && candidate !== null && candidate !== "") {
      const normalized = normalizeAnswer(candidate);
      if (normalized !== null) return normalized;
    }
  }

  return null;
}

function getCorrectTitaAnswers(
  question: QuestionAnswerData
): string[] | null {
  const candidates = [
    question.accepted_answers,
    question.acceptedAnswers,
    question.correct_answers,
    question.correctAnswers,
    question.tita_answer,
    question.correct_answer_text,
    question.correct_answer,
    question.answer,
  ];
  const normalizedAnswers = candidates
    .flatMap((candidate) =>
      Array.isArray(candidate) ? candidate : [candidate]
    )
    .map(normalizeTitaAnswer)
    .filter((answer): answer is string => answer !== null);
  const uniqueAnswers = [...new Set(normalizedAnswers)];
  return uniqueAnswers.length > 0 ? uniqueAnswers : null;
}

/*
 * =========================================================
 * NORMALIZE STATUS
 * =========================================================
 */

function isSubmittedStatus(status: unknown): boolean {
  const normalized = String(status ?? "")
    .trim()
    .toLowerCase();

  return (
    normalized === "submitted" ||
    normalized === "auto submitted" ||
    normalized === "auto-submitted"
  );
}

function isAutomaticStatus(status: unknown): boolean {
  const normalized = String(status ?? "").trim().toLowerCase();
  return normalized === "auto submitted" || normalized === "auto-submitted";
}

/*
 * =========================================================
 * POST
 * =========================================================
 */

export async function POST(request: NextRequest) {
  const pool = getPool();
  const client = await pool.connect();

  let transactionStarted = false;

  try {
    /*
     * =======================================================
     * READ BODY
     * =======================================================
     */

    let body: SubmitBody;

    try {
      body = await request.json();
    } catch {
      return NextResponse.json(
        {
          success: false,
          error: "Invalid JSON request body.",
        },
        { status: 400 }
      );
    }

    const questionTimes: Record<string, number> =
      body.questionTimes && typeof body.questionTimes === "object"
        ? Object.fromEntries(
            Object.entries(body.questionTimes).map(([key, value]) => [
              key, Math.max(0, Math.min(36000, Math.round(Number(value) || 0))),
            ])
          )
        : {};

    /*
     * =======================================================
     * TEST ID
     * =======================================================
     */

    const testId = String(body.testId ?? "").trim();

    console.log("SUBMIT DEBUG:", {
      testId,
      bodyStudentId: body.studentId,
    });

    if (!testId) {
      return NextResponse.json(
        {
          success: false,
          error: "Test ID is required.",
        },
        { status: 400 }
      );
    }

    /*
     * =======================================================
     * STUDENT ID
     * =======================================================
     */

    let studentId = "";
    let academyId = "";

    const sessionCookie =
      request.cookies.get("student_session")?.value;

    if (sessionCookie) {
      const session = parseSessionCookie<{
        studentId?: unknown;
        academyId?: unknown;
      }>(sessionCookie);

      if (session) {
        studentId = String(session.studentId ?? "").trim();
        academyId = String(session.academyId ?? "").trim();
      }
    }

    if (!studentId || !academyId) {
      return NextResponse.json(
        {
          success: false,
          error: "Student session not found.",
        },
        { status: 401 }
      );
    }

    console.log("SUBMIT STUDENT:", studentId);
    if (!hasTierFeature(await getAcademyTier(academyId), "TIME_PER_QUESTION")) {
      for (const key of Object.keys(questionTimes)) delete questionTimes[key];
    }

    /*
     * =======================================================
     * ANSWERS
     * =======================================================
     */

    const answers: AnswerMap =
      body.answers &&
      typeof body.answers === "object"
        ? body.answers
        : {};
    const answersByQuestion = Array.isArray(body.answersByQuestion)
      ? body.answersByQuestion
      : [];

    /*
     * =======================================================
     * MARKED QUESTIONS
     * =======================================================
     */

    const marked: MarkedMap =
      body.marked &&
      typeof body.marked === "object"
        ? body.marked
        : {};

    /*
     * =======================================================
     * SUBMISSION FLAGS
     * =======================================================
     */

    const automatic = Boolean(body.automatic);

    const parsedViolationCount = Number(
      body.violationCount ?? 0
    );

    const violationCount = Number.isFinite(
      parsedViolationCount
    )
      ? Math.max(
          0,
          Math.floor(parsedViolationCount)
        )
      : 0;

    /*
     * =======================================================
     * LOAD TEST
     * =======================================================
     */

    const testResult = await client.query(
      `
      SELECT
        id,
        exam,
        question_count,
        questions,
        created_at
      FROM tests
      WHERE id = $1
        AND academy_id = $2
      LIMIT 1
      `,
      [testId, academyId]
    );

    if (testResult.rows.length === 0) {
      return NextResponse.json(
        {
          success: false,
          error: "Test not found.",
        },
        { status: 404 }
      );
    }

    const test = testResult.rows[0];

    await client.query(`
      ALTER TABLE scheduled_tests
      ADD COLUMN IF NOT EXISTS test_id UUID
    `);

    let scheduledTestId: string | null = null;
    let allowReattempt = false;

    const requestedScheduledTestId = String(
      body.scheduledTestId ?? ""
    ).trim();

    if (requestedScheduledTestId) {
      const scheduledResult = await client.query(
        `
        SELECT id
             , allow_reattempt
        FROM scheduled_tests
        WHERE id::text = $1::text
          AND test_id::text = $2::text
          AND academy_id::text = $3::text
        LIMIT 1
        `,
        [requestedScheduledTestId, testId, academyId]
      );

      if (scheduledResult.rows.length > 0) {
        scheduledTestId = String(
          scheduledResult.rows[0].id
        );
        allowReattempt = scheduledResult.rows[0].allow_reattempt === true;
      }
    }

    await client.query(`
      ALTER TABLE test_attempts
      ALTER COLUMN scheduled_test_id DROP NOT NULL
    `);

    await client.query(`
      ALTER TABLE test_attempts
      DROP CONSTRAINT IF EXISTS test_attempts_scheduled_test_id_fkey
    `);

    /*
     * =======================================================
     * EXAM MARKING SCHEME
     * =======================================================
     *
     * NEET:
     *   Correct      = +4
     *   Wrong        = -1
     *   Unattempted  = 0
     *
     * MHT-CET / Others:
     *   Correct      = +1
     *   Wrong        = 0
     *   Unattempted  = 0
     */

    const examName = String(
      test.exam ?? ""
    )
      .trim()
      .toLowerCase();

    const isNEET =
      examName === "neet" ||
      examName === "neet-ug" ||
      examName === "neet ug";

    const isJEE =
      examName === "jee" ||
      examName === "jee main" ||
      examName === "jee 2026" ||
      examName === "jee advanced";

    const isCAT =
      examName === "cat" ||
      examName === "cat 2025" ||
      examName === "cat 2026";

    const marksCorrect = isNEET || isJEE ? 4 : isCAT ? 3 : 1;
    const marksIncorrect = isNEET || isJEE ? -1 : 0;
    const marksUnattempted = 0;

    console.log("MARKING SCHEME:", {
      exam: test.exam,
      isNEET,
      marksCorrect,
      marksIncorrect,
      marksUnattempted,
    });

    /*
     * =======================================================
     * PARSE QUESTIONS
     * =======================================================
     */

    let questions: QuestionAnswerData[] = [];

    const rawQuestions: unknown = test.questions;

    if (Array.isArray(rawQuestions)) {
      questions = rawQuestions.filter(
        (question): question is QuestionAnswerData =>
          typeof question === "object" &&
          question !== null &&
          !Array.isArray(question)
      );
    } else if (typeof rawQuestions === "string") {
      try {
        const parsedQuestions: unknown = JSON.parse(rawQuestions);

        if (Array.isArray(parsedQuestions)) {
          questions = parsedQuestions.filter(
            (question): question is QuestionAnswerData =>
              typeof question === "object" &&
              question !== null &&
              !Array.isArray(question)
          );
        }
      } catch (error) {
        console.error(
          "Unable to parse test questions:",
          error
        );
      }
    }

    if (questions.length === 0) {
      return NextResponse.json(
        {
          success: false,
          error: "This test contains no questions.",
        },
        { status: 400 }
      );
    }

    /*
     * =======================================================
     * SERVER-SIDE EVALUATION
     * =======================================================
     */

    let correct = 0;
    let wrong = 0;
    let unattempted = 0;

    const evaluatedAnswers: EvaluatedAnswer[] = [];

    for (
      let index = 0;
      index < questions.length;
      index++
    ) {
      const question = questions[index];

      const questionId = String(
        question.id ??
          question.question_id ??
          question.questionId ??
          `question-${index + 1}`
      );

      const selectedRaw = Object.prototype.hasOwnProperty.call(
        answersByQuestion,
        index
      )
        ? answersByQuestion[index]
        : answers[questionId];

      const titaQuestion = isTitaQuestion(question);
      const multiSelectQuestion = isMultiSelectQuestion(question);

      const selectedAnswer: number | number[] | string | null = multiSelectQuestion
        ? normalizeMultiSelectAnswer(selectedRaw)
        : titaQuestion
          ? normalizeTitaAnswer(selectedRaw)
          : normalizeAnswer(selectedRaw);

      const correctAnswer: number | number[] | string[] | null = multiSelectQuestion
        ? getCorrectMultiSelectAnswer(question)
        : titaQuestion
          ? getCorrectTitaAnswers(question)
        : getCorrectAnswer(question);

      // CAT has no negative marking (MCQ and TITA both: +3 correct, 0 wrong).
      const questionMarksIncorrect = marksIncorrect;

      let isCorrect: boolean | null = null;

      let marksAwarded = marksUnattempted;

      /*
       * =====================================================
       * UNATTEMPTED
       * =====================================================
       */

      if (selectedAnswer === null) {
        unattempted++;

        isCorrect = null;

        marksAwarded = marksUnattempted;
      }

      /*
       * =====================================================
       * CORRECT
       * =====================================================
       */

      else if (
        correctAnswer !== null &&
        (titaQuestion
          ? typeof selectedAnswer === "string" &&
            isStringArray(correctAnswer) &&
            correctAnswer.includes(selectedAnswer)
          : multiSelectQuestion
            ? Array.isArray(selectedAnswer) &&
              isNumberArray(correctAnswer) &&
              arraysEqual(selectedAnswer, correctAnswer)
            : typeof selectedAnswer === "number" &&
              typeof correctAnswer === "number" &&
              selectedAnswer === correctAnswer)
      ) {
        correct++;

        isCorrect = true;

        marksAwarded = marksCorrect;
      }

      /*
       * =====================================================
       * WRONG
       * =====================================================
       */

      else {
        wrong++;

        isCorrect = false;

        marksAwarded = questionMarksIncorrect;
      }

      evaluatedAnswers.push({
        questionId,
        selectedAnswer,
        isCorrect,
        marksAwarded,
        markedForReview: Boolean(
          marked[questionId]
        ),
      });
    }

    /*
     * =======================================================
     * SUMMARY
     * =======================================================
     */

    const totalQuestions = questions.length;

    const attempted = correct + wrong;

    /*
     * Maximum possible marks.
     *
     * NEET:
     * 180 questions × 4 = 720
     *
     * MHT-CET:
     * 180 questions × 1 = 180
     */

    const totalMarks =
      totalQuestions * marksCorrect;

    /*
     * Actual score.
     *
     * NEET:
     * correct × 4 + wrong × (-1)
     *
     * MHT-CET:
     * correct × 1 + wrong × 0
     */

    const score =
      correct * marksCorrect +
      wrong * marksIncorrect +
      unattempted * marksUnattempted;

    /*
     * Accuracy is based only on attempted questions.
     */

    const accuracy =
      attempted > 0
        ? Number(
            (
              (correct / attempted) *
              100
            ).toFixed(2)
          )
        : 0;

    console.log("SUBMIT SCORE:", {
      totalQuestions,
      attempted,
      correct,
      wrong,
      unattempted,
      totalMarks,
      score,
      accuracy,
    });

    /*
     * =======================================================
     * DATES
     * =======================================================
     */

    const submittedAt = body.submittedAt
      ? new Date(body.submittedAt)
      : new Date();

    const startedAt = body.startedAt
      ? new Date(body.startedAt)
      : new Date(test.created_at);

    const safeStartedAt = Number.isNaN(
      startedAt.getTime()
    )
      ? new Date(test.created_at)
      : startedAt;

    const safeSubmittedAt = Number.isNaN(
      submittedAt.getTime()
    )
      ? new Date()
      : submittedAt;

    /*
     * =======================================================
     * START TRANSACTION
     * =======================================================
     */

    await client.query("BEGIN");

    transactionStarted = true;

    /*
     * =======================================================
     * FIND EXISTING ATTEMPT
     * =======================================================
     */

    const existingAttemptResult =
      await client.query(
        `
        SELECT
          id,
          test_id,
          scheduled_test_id,
          status,
          submitted_at,
          started_at,
          score,
          total_marks,
          correct_count,
          incorrect_count,
          unanswered_count
        FROM test_attempts
        WHERE (
          test_id::text = $1::text
          OR ($3::text <> '' AND scheduled_test_id::text = $3::text)
        )
        AND student_id::text = $2::text
        ORDER BY started_at DESC NULLS LAST
        LIMIT 1
        FOR UPDATE
        `,
        [testId, studentId, requestedScheduledTestId]
      );

    let attemptId: string;

    /*
     * =======================================================
     * EXISTING ATTEMPT
     * =======================================================
     */

    const existingAttempt = existingAttemptResult.rows[0];
    const canReattempt = Boolean(
      existingAttempt &&
      body.reattempt === true &&
      allowReattempt &&
      isAutomaticStatus(existingAttempt.status)
    );

    if (existingAttemptResult.rows.length > 0 && !canReattempt) {
      const existing = existingAttempt;

      /*
       * Already submitted
       */

      if (isSubmittedStatus(existing.status)) {
        await client.query("COMMIT");

        transactionStarted = false;

        return NextResponse.json({
          success: true,
          alreadySubmitted: true,
          attemptId: String(existing.id),
          testId,
          scheduledTestId,
          total: totalQuestions,
          attempted: Number(existing.correct_count ?? 0) + Number(existing.incorrect_count ?? 0),
          correct: Number(existing.correct_count ?? 0),
          wrong: Number(existing.incorrect_count ?? 0),
          unattempted: Number(existing.unanswered_count ?? 0),
          score: Number(existing.score ?? 0),
          totalMarks: Number(existing.total_marks ?? totalMarks),
          accuracy: (Number(existing.correct_count ?? 0) + Number(existing.incorrect_count ?? 0)) > 0
            ? Number((Number(existing.correct_count ?? 0) / (Number(existing.correct_count ?? 0) + Number(existing.incorrect_count ?? 0)) * 100).toFixed(2))
            : 0,
          automatic,
          violationCount,
        });
      }

      /*
       * Existing in-progress attempt.
       */

      attemptId = String(existing.id);

      await client.query(
        `
        UPDATE test_attempts
        SET
          submitted_at = $1,
          status = $2,
          score = $3,
          total_marks = $4,
          correct_count = $5,
          incorrect_count = $6,
          unanswered_count = $7
        WHERE id = $8
        `,
        [
          safeSubmittedAt,
          automatic
            ? "Auto Submitted"
            : "Submitted",
          score,
          totalMarks,
          correct,
          wrong,
          unattempted,
          attemptId,
        ]
      );
    }

    /*
     * =======================================================
     * CREATE NEW ATTEMPT
     * =======================================================
     */

    else {
      attemptId = `attempt-${crypto.randomUUID()}`;

      await client.query(
        `
        INSERT INTO test_attempts (
          id,
          test_id,
          scheduled_test_id,
          student_id,
          started_at,
          submitted_at,
          status,
          score,
          total_marks,
          correct_count,
          incorrect_count,
          unanswered_count
        )
        VALUES (
          $1,
          $2,
          $3,
          $4,
          $5,
          $6,
          $7,
          $8,
          $9,
          $10,
          $11,
          $12
        )
        `,
        [
          attemptId,
          testId,
          scheduledTestId,
          studentId,
          safeStartedAt,
          safeSubmittedAt,
          automatic
            ? "Auto Submitted"
            : "Submitted",
          score,
          totalMarks,
          correct,
          wrong,
          unattempted,
        ]
      );
    }

    /*
     * =======================================================
     * REMOVE PREVIOUS ANSWERS
     * =======================================================
     */

    await client.query(
      `
      DELETE FROM test_answers
      WHERE attempt_id = $1
      `,
      [attemptId]
    );

    /*
     * =======================================================
     * BULK INSERT ALL ANSWERS
     * =======================================================
     *
     * All answers are inserted using ONE query.
     */

    if (evaluatedAnswers.length > 0) {
      const values: unknown[] = [];

      const placeholders: string[] = [];

      evaluatedAnswers.forEach(
        (answer, index) => {
          const offset = index * 8;

          placeholders.push(
            `(
              $${offset + 1},
              $${offset + 2},
              $${offset + 3},
              $${offset + 4},
              $${offset + 5},
              $${offset + 6},
              $${offset + 7},
              $${offset + 8}
            )`
          );

          values.push(
            attemptId,
            answer.questionId,
            answer.selectedAnswer,
            answer.isCorrect,
            answer.marksAwarded,
            questionTimes[answer.questionId] ?? 0,
            answer.markedForReview,
            answer.selectedAnswer === null
              ? null
              : safeSubmittedAt
          );
        }
      );

      await client.query(
        `
        INSERT INTO test_answers (
          attempt_id,
          question_id,
          selected_answer,
          is_correct,
          marks_awarded,
          time_spent_seconds,
          marked_for_review,
          answered_at
        )
        VALUES ${placeholders.join(",")}
        `,
        values
      );
    }

    /*
     * =======================================================
     * SAVE ANTI-CHEATING VIOLATIONS
     * =======================================================
     *
     * Always clear previous violations first.
     */

    await client.query(
      `
      DELETE FROM test_violations
      WHERE attempt_id = $1
      `,
      [attemptId]
    );

    /*
     * Recreate violations if required.
     */

    if (violationCount > 0) {
      const violationValues: unknown[] = [];

      const violationPlaceholders: string[] = [];

      for (
        let i = 1;
        i <= violationCount;
        i++
      ) {
        const offset =
          (i - 1) * 4;

        violationPlaceholders.push(
          `(
            $${offset + 1},
            $${offset + 2},
            $${offset + 3},
            $${offset + 4}
          )`
        );

        violationValues.push(
          attemptId,
          "TAB_LEAVE",
          JSON.stringify({
            violationNumber: i,
          }),
          safeSubmittedAt
        );
      }

      await client.query(
        `
        INSERT INTO test_violations (
          attempt_id,
          violation_type,
          details,
          occurred_at
        )
        VALUES ${violationPlaceholders.join(",")}
        `,
        violationValues
      );
    }

    /*
     * =======================================================
     * COMMIT
     * =======================================================
     */

    await client.query("COMMIT");

    transactionStarted = false;

    /*
     * =======================================================
     * RETURN RESULT
     * =======================================================
     */

    return NextResponse.json({
      success: true,
      alreadySubmitted: false,
      attemptId,
      testId,
      scheduledTestId,
      allowReattempt,
      total: totalQuestions,
      attempted,
      correct,
      wrong,
      unattempted,
      totalMarks,
      score,
      accuracy,
      automatic,
      violationCount,
    });
  } catch (error) {
    /*
     * =======================================================
     * ROLLBACK
     * =======================================================
     */

    if (transactionStarted) {
      try {
        await client.query("ROLLBACK");
      } catch (rollbackError) {
        console.error(
          "ROLLBACK ERROR:",
          rollbackError
        );
      }
    }

    console.error(
      "TEST SUBMIT API ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to submit test.",
      },
      { status: 500 }
    );
  } finally {
    client.release();
  }
}
