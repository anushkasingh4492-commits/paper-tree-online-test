import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function POST(request: Request) {
  const client = await pool.connect();

  try {
    const cookieStore = await cookies();
    const sessionCookie =
      cookieStore.get("master_session")?.value;

    if (!sessionCookie) {
      return NextResponse.json(
        {
          success: false,
          error: "Teacher is not logged in.",
        },
        { status: 401 }
      );
    }

    let session: {
      id?: string;
      role?: string;
    };

    try {
      session = JSON.parse(sessionCookie);
    } catch {
      return NextResponse.json(
        {
          success: false,
          error: "Invalid teacher session.",
        },
        { status: 401 }
      );
    }

    if (session.role !== "TEACHER") {
      return NextResponse.json(
        {
          success: false,
          error: "Teacher access required.",
        },
        { status: 403 }
      );
    }

    const body = await request.json();

    const title = String(
      body.title || "Scheduled Test"
    ).trim();

    const startTime = new Date(body.startTime);
    const endTime = new Date(body.endTime);

    const duration = Math.max(
      1,
      Number(body.duration) || 60
    );

    const generatedTest = body.test;

    if (!generatedTest) {
      return NextResponse.json(
        {
          success: false,
          error: "Generated test data is missing.",
        },
        { status: 400 }
      );
    }

    if (
      Number.isNaN(startTime.getTime()) ||
      Number.isNaN(endTime.getTime())
    ) {
      return NextResponse.json(
        {
          success: false,
          error: "Invalid start or end time.",
        },
        { status: 400 }
      );
    }

    /*
     * The existing generator normally returns questions
     * either directly or inside the generated test object.
     */
    const questions =
      Array.isArray(generatedTest.questions)
        ? generatedTest.questions
        : Array.isArray(generatedTest.data?.questions)
          ? generatedTest.data.questions
          : [];

    if (questions.length === 0) {
      return NextResponse.json(
        {
          success: false,
          error:
            "No generated questions were found.",
        },
        { status: 400 }
      );
    }

    await client.query("BEGIN");

    /*
     * -------------------------------------------------------
     * CREATE TEST
     * -------------------------------------------------------
     */

    const testId = crypto.randomUUID();

    await client.query(
      `
      INSERT INTO tests (
        id,
        exam,
        question_count,
        questions,
        created_at,
        difficulty
      )
      VALUES (
        $1,
        $2,
        $3,
        $4::jsonb,
        NOW(),
        $5
      )
      `,
      [
        testId,
        generatedTest.exam || "MHT-CET",
        questions.length,
        JSON.stringify(questions),
        generatedTest.difficulty || "Balanced",
      ]
    );

    /*
     * -------------------------------------------------------
     * CREATE TEST QUESTIONS
     * -------------------------------------------------------
     */

    for (let i = 0; i < questions.length; i++) {
      const question = questions[i];

      const questionId = String(
        question.id || question.question_id || ""
      ).trim();

      if (!questionId) {
        continue;
      }

      await client.query(
        `
        INSERT INTO test_questions (
          id,
          test_id,
          question_id,
          question_number,
          marked_for_review,
          visited,
          created_at
        )
        VALUES (
          gen_random_uuid(),
          $1,
          $2,
          $3,
          false,
          false,
          NOW()
        )
        `,
        [
          testId,
          questionId,
          i + 1,
        ]
      );
    }

   /*
 * -------------------------------------------------------
 * CREATE PAPER
 * -------------------------------------------------------
 */

const paperId = crypto.randomUUID();

await client.query(
  `
  INSERT INTO papers (
    id,
    code,
    exam,
    description,
    duration_minutes,
    created_by,
    created_at,
    updated_at,
    status
  )
  VALUES (
    $1,
    $2,
    $3,
    $4,
    $5,
    $6,
    NOW(),
    NOW(),
    'Scheduled'
  )
  `,
  [
    paperId,
    `PAPER-${paperId.slice(0, 8).toUpperCase()}`,
    generatedTest.exam || "MHT-CET",
    title,
    duration,
    session.id || null,
  ]
);

/*
 * -------------------------------------------------------
 * LINK QUESTIONS TO PAPER
 * -------------------------------------------------------
 */

for (let i = 0; i < questions.length; i++) {
  const question = questions[i];

  const questionId = String(
    question.id || question.question_id || ""
  ).trim();

  if (!questionId) continue;

  await client.query(
    `
    INSERT INTO paper_questions (
      paper_id,
      question_id,
      question_order
    )
    VALUES (
      $1,
      $2,
      $3
    )
    `,
    [
      paperId,
      questionId,
      i + 1,
    ]
  );
}

/*
 * -------------------------------------------------------
 * SCHEDULE TEST
 * -------------------------------------------------------
 */

const scheduledTestId =
  crypto.randomUUID();

await client.query(
  `
  INSERT INTO scheduled_tests (
    id,
    paper_id,
    batch_id,
    title,
    start_time,
    end_time,
    duration_minutes,
    status,
    created_at
  )
  VALUES (
    $1,
    $2,
    NULL,
    $3,
    $4,
    $5,
    $6,
    'Upcoming',
    NOW()
  )
  `,
  [
    scheduledTestId,
    paperId,
    title,
    startTime.toISOString(),
    endTime.toISOString(),
    duration,
  ]
);
    await client.query("COMMIT");

return NextResponse.json({
  success: true,
  message: "Test published successfully.",
  testId,
  paperId,
  scheduledTestId,
  title,
  startTime: startTime.toISOString(),
  endTime: endTime.toISOString(),
  duration,
  questionCount: questions.length,
});
  } catch (error) {
    await client.query("ROLLBACK");

    console.error(
      "PUBLISH TEST ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to publish test.",
      },
      { status: 500 }
    );
  } finally {
    client.release();
  }
}
