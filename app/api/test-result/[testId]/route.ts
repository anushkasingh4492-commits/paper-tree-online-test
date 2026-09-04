import { NextRequest, NextResponse } from "next/server";
import { pool } from "@/lib/db";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export async function GET(
  request: NextRequest,
  {
    params,
  }: {
    params: Promise<{ testId: string }>;
  }
) {
  try {
    const { testId } = await params;

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
     * -------------------------------------------------------
     * STUDENT
     * -------------------------------------------------------
     */

    let studentId = "";

    const sessionCookie =
      request.cookies.get("student_session")?.value;

    if (sessionCookie) {
      try {
        const decoded =
          decodeURIComponent(
            sessionCookie
          );

        try {
          const parsed =
            JSON.parse(decoded);

          studentId = String(
            parsed?.studentId ?? ""
          ).trim();
        } catch {
          studentId =
            decoded.trim();
        }
      } catch {
        studentId =
          sessionCookie.trim();
      }
    }

    if (!studentId) {
      return NextResponse.json(
        {
          success: false,
          error: "Student session not found.",
        },
        { status: 401 }
      );
    }

    /*
     * -------------------------------------------------------
     * FIND COMPLETED ATTEMPT
     *
     * The dashboard already supports both:
     *
     * test_id
     * scheduled_test_id
     * -------------------------------------------------------
     */

    const attemptResult =
      await pool.query(
        `
        SELECT
          ta.id AS attempt_id,
          ta.test_id,
          ta.scheduled_test_id,
          ta.status,
          ta.score,
          ta.total_marks,
          ta.correct_count,
          ta.incorrect_count,
          ta.unanswered_count,
          ta.started_at,
          ta.submitted_at,

          t.exam,
          t.questions,
          t.question_count

        FROM test_attempts ta

        LEFT JOIN tests t
          ON t.id = COALESCE(
            ta.test_id,
            ta.scheduled_test_id
          )

        WHERE
          ta.student_id = $1
          AND (
            ta.test_id = $2
            OR ta.scheduled_test_id = $2
          )

        ORDER BY
          ta.submitted_at DESC NULLS LAST,
          ta.started_at DESC NULLS LAST

        LIMIT 1
        `,
        [studentId, testId]
      );

    if (attemptResult.rows.length === 0) {
      return NextResponse.json(
        {
          success: false,
          error: "Completed test result not found.",
        },
        { status: 404 }
      );
    }

    const attempt =
      attemptResult.rows[0];

    const status =
      String(
        attempt.status ?? ""
      )
        .trim()
        .toLowerCase();

    if (
      status !== "submitted" &&
      status !== "auto submitted" &&
      status !== "auto-submitted"
    ) {
      return NextResponse.json(
        {
          success: false,
          error:
            "This test has not been submitted yet.",
        },
        { status: 400 }
      );
    }

    /*
     * -------------------------------------------------------
     * QUESTIONS
     * -------------------------------------------------------
     */

    let questions: any[] = [];

    if (Array.isArray(attempt.questions)) {
      questions =
        attempt.questions;
    } else if (
      typeof attempt.questions ===
      "string"
    ) {
      try {
        const parsed =
          JSON.parse(
            attempt.questions
          );

        if (Array.isArray(parsed)) {
          questions = parsed;
        }
      } catch (error) {
        console.error(
          "RESULT QUESTIONS PARSE ERROR:",
          error
        );
      }
    }


 const answersResult =
  await pool.query(
    `
    SELECT
      question_id,
      selected_answer,
      is_correct,
      marks_awarded,
      marked_for_review
    FROM test_answers
    WHERE attempt_id = $1
    ORDER BY question_id
    `,
    [attempt.attempt_id]
  );

const answers: Record<
  string,
  number
> = {};

const marked: Record<
  string,
  boolean
> = {};

const marksAwarded: Record<
  string,
  number
> = {};

const correctness: Record<
  string,
  boolean | null
> = {};

for (
  const answer of
    answersResult.rows
) {
  const questionId =
    String(
      answer.question_id
    );

  if (
    answer.selected_answer !==
      null &&
    answer.selected_answer !==
      undefined
  ) {
    answers[
      questionId
    ] = Number(
      answer.selected_answer
    );
  }

  marked[
    questionId
  ] = Boolean(
    answer.marked_for_review
  );

  correctness[
    questionId
  ] =
    answer.is_correct === null ||
    answer.is_correct === undefined
      ? null
      : Boolean(
          answer.is_correct
        );

  marksAwarded[
    questionId
  ] = Number(
    answer.marks_awarded ?? 0
  );
}

    

    /*
     * -------------------------------------------------------
     * RESULT
     * -------------------------------------------------------
     */

    const total =
      Number(
        attempt.question_count ??
          questions.length ??
          0
      );

    const correct =
      Number(
        attempt.correct_count ??
          0
      );

    const wrong =
      Number(
        attempt.incorrect_count ??
          0
      );

    const unattempted =
      Number(
        attempt.unanswered_count ??
          Math.max(
            0,
            total -
              correct -
              wrong
          )
      );

    const attempted =
      correct + wrong;

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

    const result = {
      testId,

      attemptId:
        String(
          attempt.attempt_id
        ),

      total,
      correct,
      wrong,
      unattempted,

   answers,
marked,
marksAwarded,
correctness,
questions,

      submittedAt:
        attempt.submitted_at
          ? new Date(
              attempt.submitted_at
            ).toISOString()
          : undefined,

      automatic:
        status ===
        "auto submitted" ||
        status ===
        "auto-submitted",

      score:
        Number(
          attempt.score ?? 0
        ),

      accuracy,

      course: "",
      subject: "",
      chapters: [],
      difficulty: "",

      duration:
        attempt.started_at &&
        attempt.submitted_at
          ? Math.max(
              0,
              Math.round(
                (
                  new Date(
                    attempt.submitted_at
                  ).getTime() -
                  new Date(
                    attempt.started_at
                  ).getTime()
                ) / 60000
              )
            )
          : undefined,
    };

    return NextResponse.json({
      success: true,
      result,
    });
  } catch (error) {
    console.error(
      "GET TEST RESULT ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to load test result.",
      },
      { status: 500 }
    );
  }
}
