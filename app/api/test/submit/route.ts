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

type AnswerMap = Record<string, number | string | null>;

type MarkedMap = Record<string, boolean>;

type SubmitBody = {
  testId?: string;

  studentId?: string;

  answers?: AnswerMap;

  marked?: MarkedMap;

  automatic?: boolean;

  violationCount?: number;

  startedAt?: string;

  submittedAt?: string;
};

type EvaluatedAnswer = {
  questionId: string;

  selectedAnswer: number | null;

  isCorrect: boolean | null;

  marksAwarded: number;

  markedForReview: boolean;
};

/*
 * Convert an answer stored in different formats
 * into the zero-based option index.
 *
 * Supported:
 *
 * 0 -> 0
 * "0" -> 0
 * A -> 0
 * "A" -> 0
 * B -> 1
 * "B" -> 1
 * etc.
 */
function normalizeAnswer(
  value: unknown
): number | null {
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

    /*
     * Numeric answer.
     */
    const numericValue = Number(trimmed);

    if (
      Number.isFinite(numericValue) &&
      Number.isInteger(numericValue)
    ) {
      return numericValue;
    }

    /*
     * Letter answer.
     *
     * A = 0
     * B = 1
     * C = 2
     * D = 3
     */
    const letter = trimmed.toUpperCase();

    if (/^[A-Z]$/.test(letter)) {
      return letter.charCodeAt(0) - 65;
    }
  }

  return null;
}

/*
 * Resolve the authoritative correct answer.
 *
 * Priority:
 *
 * 1. question.answer
 * 2. question.correct_option
 * 3. question.correctOption
 */
function getCorrectAnswer(
  question: any
): number | null {
  /*
   * Primary answer field.
   */
  if (
    question.answer !== undefined &&
    question.answer !== null &&
    question.answer !== ""
  ) {
    const normalized = normalizeAnswer(
      question.answer
    );

    if (normalized !== null) {
      return normalized;
    }
  }

  /*
   * Legacy snake_case field.
   */
  if (
    question.correct_option !== undefined &&
    question.correct_option !== null &&
    question.correct_option !== ""
  ) {
    const normalized = normalizeAnswer(
      question.correct_option
    );

    if (normalized !== null) {
      return normalized;
    }
  }

  /*
   * Legacy camelCase field.
   */
  if (
    question.correctOption !== undefined &&
    question.correctOption !== null &&
    question.correctOption !== ""
  ) {
    const normalized = normalizeAnswer(
      question.correctOption
    );

    if (normalized !== null) {
      return normalized;
    }
  }

  return null;
}

export async function POST(
  request: NextRequest
) {
  const pool = getPool();

  const client = await pool.connect();

  let transactionStarted = false;

  try {
    /*
     * READ REQUEST BODY
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

    /*
     * TEST ID
     *
     * IMPORTANT:
     *
     * This route is:
     *
     * /api/test/submit
     *
     * NOT:
     *
     * /api/test/submit/[testId]
     *
     * Therefore testId must come from
     * the request body.
     */
    const testId = String(
      body.testId ?? ""
    ).trim();
    console.log("SUBMIT DEBUG:", {
  testId,
  studentId: body.studentId,
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
     * STUDENT ID
     */
    const studentId = String(
      body.studentId ?? ""
    ).trim();

    if (!studentId) {
      return NextResponse.json(
        {
          success: false,
          error: "Student ID is required.",
        },
        { status: 400 }
      );
    }

    /*
     * ANSWERS
     */
    const answers: AnswerMap =
      body.answers &&
      typeof body.answers === "object"
        ? body.answers
        : {};

    /*
     * MARKED QUESTIONS
     */
    const marked: MarkedMap =
      body.marked &&
      typeof body.marked === "object"
        ? body.marked
        : {};

    /*
     * SUBMISSION FLAGS
     */
    const automatic =
      Boolean(body.automatic);

    const violationCount = Math.max(
      0,
      Number(body.violationCount ?? 0)
    );

    /*
     * LOAD TEST
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
      LIMIT 1
      `,
      [testId]
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

    /*
     * PARSE QUESTIONS
     */
    let questions: any[] = [];

    if (Array.isArray(test.questions)) {
      questions = test.questions;
    } else if (
      typeof test.questions === "string"
    ) {
      try {
        const parsedQuestions =
          JSON.parse(test.questions);

        if (Array.isArray(parsedQuestions)) {
          questions = parsedQuestions;
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
          error:
            "This test contains no questions.",
        },
        { status: 400 }
      );
    }

    /*
     * SERVER-SIDE EVALUATION
     *
     * NEVER trust:
     *
     * correct
     * wrong
     * score
     * accuracy
     *
     * from the browser.
     *
     * Everything is calculated here.
     */
    let correct = 0;
    let wrong = 0;
    let unattempted = 0;

    const evaluatedAnswers: EvaluatedAnswer[] =
      [];

    for (
      let index = 0;
      index < questions.length;
      index++
    ) {
      const question = questions[index];

      /*
       * Normalize question ID.
       */
      const questionId = String(
        question.id ??
          question.question_id ??
          `question-${index + 1}`
      );

      /*
       * Get student's submitted answer.
       */
      const selectedRaw =
        answers[questionId];

      /*
       * Normalize selected answer.
       *
       * Example:
       *
       * "0" -> 0
       * 0 -> 0
       * "A" -> 0
       * "B" -> 1
       */
      const selectedAnswer =
        normalizeAnswer(selectedRaw);

      /*
       * Resolve authoritative answer
       * from the database question.
       */
      const correctAnswer =
        getCorrectAnswer(question);

      /*
       * Evaluate.
       */
      let isCorrect:
        | boolean
        | null = null;

      let marksAwarded = 0;

      if (selectedAnswer === null) {
        /*
         * Student did not answer.
         */
        unattempted++;
      } else if (
        correctAnswer !== null &&
        selectedAnswer === correctAnswer
      ) {
        /*
         * Correct answer.
         */
        correct++;

        isCorrect = true;

        marksAwarded = 1;
      } else {
        /*
         * Student answered but was wrong.
         */
        wrong++;

        isCorrect = false;

        marksAwarded = 0;
      }

      evaluatedAnswers.push({
        questionId,

        selectedAnswer,

        isCorrect,

        marksAwarded,

        markedForReview:
          Boolean(marked[questionId]),
      });
    }

    /*
     * SUMMARY
     */
    const totalQuestions =
      questions.length;

    const attempted =
      correct + wrong;

    const totalMarks =
      totalQuestions;

    /*
     * SCORE
     *
     * For now:
     *
     * 1 correct = 1 mark
     *
     * Score is percentage.
     */
    const score =
      totalMarks > 0
        ? Number(
            (
              (correct /
                totalMarks) *
              100
            ).toFixed(2)
          )
        : 0;

    /*
     * ACCURACY
     *
     * Accuracy only considers attempted questions.
     */
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

    /*
     * DATES
     */
    const submittedAt = body.submittedAt
      ? new Date(body.submittedAt)
      : new Date();

    const startedAt = body.startedAt
      ? new Date(body.startedAt)
      : new Date(test.created_at);

    /*
     * Validate dates.
     */
    const safeStartedAt =
      Number.isNaN(
        startedAt.getTime()
      )
        ? new Date(test.created_at)
        : startedAt;

    const safeSubmittedAt =
      Number.isNaN(
        submittedAt.getTime()
      )
        ? new Date()
        : submittedAt;

    /*
     * START TRANSACTION
     */
    await client.query("BEGIN");

    transactionStarted = true;

    /*
     * FIND EXISTING ATTEMPT
     *
     * This prevents duplicate attempts when:
     *
     * - student double-clicks submit
     * - timer submits
     * - anti-cheating auto-submits
     * - browser retries request
     */
    const existingAttemptResult =
      await client.query(
        `
        SELECT
          id,
          status,
          submitted_at
        FROM test_attempts
        WHERE scheduled_test_id = $1
          AND student_id = $2
        ORDER BY started_at DESC
        LIMIT 1
        FOR UPDATE
        `,
        [
          testId,
          studentId,
        ]
      );

    let attemptId: string;

    /*
     * EXISTING ATTEMPT
     */
    if (
      existingAttemptResult.rows
        .length > 0
    ) {
      const existing =
        existingAttemptResult.rows[0];

      /*
       * Already submitted.
       *
       * Do not create another attempt.
       */
      if (
        existing.status ===
          "SUBMITTED" ||
        existing.status ===
          "AUTO SUBMITTED"
      ) {
        await client.query("COMMIT");

        transactionStarted = false;

        return NextResponse.json({
          success: true,

          alreadySubmitted: true,

          attemptId: String(
            existing.id
          ),

          testId,

          total:
            totalQuestions,

          attempted,

          correct,

          wrong,

          unattempted,

          score,

          accuracy,
        });
      }

      /*
       * Existing in-progress attempt.
       */
      attemptId = String(
        existing.id
      );

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
    } else {
      /*
       * CREATE NEW ATTEMPT
       */
      attemptId =
        `attempt-${crypto.randomUUID()}`;

      await client.query(
        `
        INSERT INTO test_attempts (
          id,
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
          $11
        )
        `,
        [
          attemptId,

          testId,

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
     * REMOVE PREVIOUS ANSWERS
     *
     * Important when an existing in-progress
     * attempt is being submitted.
     */
    await client.query(
      `
      DELETE FROM test_answers
      WHERE attempt_id = $1
      `,
      [attemptId]
    );

    /*
     * SAVE EVERY QUESTION ANSWER
     */
    for (
      const answer of evaluatedAnswers
    ) {
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
        VALUES (
          $1,
          $2,
          $3,
          $4,
          $5,
          $6,
          $7,
          $8
        )
        `,
        [
          attemptId,

          answer.questionId,

          answer.selectedAnswer,

          answer.isCorrect,

          answer.marksAwarded,

          0,

          answer.markedForReview,

          answer.selectedAnswer ===
          null
            ? null
            : safeSubmittedAt,
        ]
      );
    }

    /*
     * SAVE ANTI-CHEATING VIOLATIONS
     */
    if (violationCount > 0) {
      /*
       * Remove old violation records for this
       * attempt before recreating them.
       */
      await client.query(
        `
        DELETE FROM test_violations
        WHERE attempt_id = $1
        `,
        [attemptId]
      );

      for (
        let i = 1;
        i <= violationCount;
        i++
      ) {
        await client.query(
          `
          INSERT INTO test_violations (
            attempt_id,
            violation_type,
            details,
            occurred_at
          )
          VALUES (
            $1,
            $2,
            $3,
            $4
          )
          `,
          [
            attemptId,

            "TAB_LEAVE",

            JSON.stringify({
              violationNumber: i,
            }),

            safeSubmittedAt,
          ]
        );
      }
    }

    /*
     * COMPLETE TRANSACTION
     */
    await client.query("COMMIT");

    transactionStarted = false;

    /*
     * RETURN FINAL SERVER RESULT
     */
    return NextResponse.json({
      success: true,

      alreadySubmitted: false,

      attemptId,

      testId,

      total:
        totalQuestions,

      attempted,

      correct,

      wrong,

      unattempted,

      score,

      accuracy,

      automatic,

      violationCount,
    });
  } catch (error) {
    /*
     * ROLLBACK ONLY IF TRANSACTION STARTED.
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