import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function POST(request: Request) {
  const client = await pool.connect();

  try {
    /*
     * =======================================================
     * TEACHER SESSION
     * =======================================================
     */

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
      academyId?: string;
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

    /*
     * Only teachers can use this endpoint.
     */

    if (session.role !== "TEACHER") {
      return NextResponse.json(
        {
          success: false,
          error: "Teacher access required.",
        },
        { status: 403 }
      );
    }

    /*
     * Teacher MUST belong to an academy.
     */

    const academyId = session.academyId
      ? String(session.academyId).trim()
      : "";

    if (!academyId) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Teacher is not assigned to an academy.",
        },
        { status: 403 }
      );
    }

    /*
     * =======================================================
     * REQUEST BODY
     * =======================================================
     */

    const body = await request.json();

    /*
     * Target can be:
     *
     * 1. batch
     * OR
     * 2. single student
     */

    const batchId = body.batchId
      ? String(body.batchId).trim()
      : null;

    const studentId = body.studentId
      ? String(body.studentId).trim()
      : null;

    /*
     * =======================================================
     * TARGET VALIDATION
     * =======================================================
     */

    if (!batchId && !studentId) {
      return NextResponse.json(
        {
          success: false,
          error: "Select a batch or a student.",
        },
        { status: 400 }
      );
    }

    if (batchId && studentId) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Select either a batch or a single student, not both.",
        },
        { status: 400 }
      );
    }

    /*
     * =======================================================
     * TEST DETAILS
     * =======================================================
     */

    const title = String(
      body.title || "Scheduled Test"
    ).trim();

    if (!title) {
      return NextResponse.json(
        {
          success: false,
          error: "Test title is required.",
        },
        { status: 400 }
      );
    }

    const startTime = new Date(body.startTime);
    const endTime = new Date(body.endTime);

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

    if (endTime <= startTime) {
      return NextResponse.json(
        {
          success: false,
          error:
            "End time must be after start time.",
        },
        { status: 400 }
      );
    }

    const duration = Math.max(
      1,
      Number(body.duration) || 60
    );

    /*
     * =======================================================
     * GENERATED TEST
     * =======================================================
     */

    const generatedTest = body.test;

    if (!generatedTest) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Generated test data is missing.",
        },
        { status: 400 }
      );
    }

    /*
     * Questions can exist in:
     *
     * generatedTest.questions
     *
     * OR
     *
     * generatedTest.data.questions
     */

    const questions =
      Array.isArray(generatedTest.questions)
        ? generatedTest.questions
        : Array.isArray(
            generatedTest.data?.questions
          )
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

    /*
     * =======================================================
     * VERIFY TARGET BELONGS TO SAME ACADEMY
     * =======================================================
     */

    if (batchId) {
      const batchCheck = await client.query(
        `
        SELECT
          id,
          name,
          class_name
        FROM batches
        WHERE id = $1
          AND academy_id = $2
        LIMIT 1
        `,
        [batchId, academyId]
      );

      if (batchCheck.rowCount === 0) {
        return NextResponse.json(
          {
            success: false,
            error:
              "Batch not found in your academy.",
          },
          { status: 403 }
        );
      }
    }

    if (studentId) {
      /*
       * Verify:
       *
       * - student exists
       * - student belongs to same academy
       */

      const studentCheck = await client.query(
        `
        SELECT
          id,
          name,
          email,
          class_name
        FROM students
        WHERE id = $1
          AND academy_id = $2
        LIMIT 1
        `,
        [studentId, academyId]
      );

      if (studentCheck.rowCount === 0) {
        return NextResponse.json(
          {
            success: false,
            error:
              "Student not found in your academy.",
          },
          { status: 403 }
        );
      }
    }

    /*
     * =======================================================
     * START TRANSACTION
     * =======================================================
     */

    await client.query("BEGIN");

    /*
     * =======================================================
     * CREATE TEST
     * =======================================================
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
  difficulty,
  academy_id
)
  VALUES (
  $1,
  $2,
  $3,
  $4::jsonb,
  NOW(),
  $5,
  $6
)
      `,
      [
  testId,
  generatedTest.exam || "MHT-CET",
  questions.length,
  JSON.stringify(questions),
  generatedTest.difficulty || "Balanced",
  academyId,
]
    );

    /*
     * =======================================================
     * CREATE TEST QUESTIONS
     * =======================================================
     */

    for (let i = 0; i < questions.length; i++) {
      const question = questions[i];

      const questionId = String(
        question.id ||
          question.question_id ||
          ""
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
     * =======================================================
     * CREATE PAPER
     * =======================================================
     *
     * Paper is owned by the teacher's academy.
     *
     * This is important for:
     *
     * Vigyan Academy
     *      ↓
     * only Vigyan papers
     *
     * Infinity Classes
     *      ↓
     * only Infinity papers
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
        academy_id,
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
        $7,
        NOW(),
        NOW(),
        'Scheduled'
      )
      `,
      [
        paperId,
        `PAPER-${paperId
          .slice(0, 8)
          .toUpperCase()}`,
        generatedTest.exam || "MHT-CET",
        title,
        duration,
        session.id || null,
        academyId,
      ]
    );

    /*
     * =======================================================
     * LINK QUESTIONS TO PAPER
     * =======================================================
     */

    for (let i = 0; i < questions.length; i++) {
      const question = questions[i];

      const questionId = String(
        question.id ||
          question.question_id ||
          ""
      ).trim();

      if (!questionId) {
        continue;
      }
await client.query(`
  ALTER TABLE tests
  ADD COLUMN IF NOT EXISTS academy_id UUID
`);
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
     * =======================================================
     * CREATE SCHEDULED TEST
     * =======================================================
     *
     * BATCH:
     *
     * scheduled_tests.batch_id = batchId
     *
     * SINGLE STUDENT:
     *
     * scheduled_tests.batch_id = NULL
     * scheduled_test_students contains student
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
        academy_id,
        created_at
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
        NOW()
      )
      `,
      [
        scheduledTestId,
        paperId,
        batchId,
        title,
        startTime.toISOString(),
        endTime.toISOString(),
        duration,
        "Upcoming",
        academyId,
      ]
    );

    /*
     * =======================================================
     * SINGLE STUDENT ASSIGNMENT
     * =======================================================
     *
     * Only executed when studentId was selected.
     */

    if (studentId) {
      await client.query(
        `
        INSERT INTO scheduled_test_students (
          scheduled_test_id,
          student_id,
          created_at
        )
        VALUES (
          $1,
          $2,
          NOW()
        )
        ON CONFLICT (
          scheduled_test_id,
          student_id
        )
        DO NOTHING
        `,
        [
          scheduledTestId,
          studentId,
        ]
      );
    }

    /*
     * =======================================================
     * COMMIT
     * =======================================================
     */

    await client.query("COMMIT");

    /*
     * =======================================================
     * RESPONSE
     * =======================================================
     */

    return NextResponse.json({
      success: true,

      message:
        "Test published successfully.",

      testId,

      paperId,

      scheduledTestId,

      title,

      targetType: batchId
        ? "batch"
        : "student",

      batchId,

      studentId,

      academyId,

      startTime:
        startTime.toISOString(),

      endTime:
        endTime.toISOString(),

      duration,

      questionCount:
        questions.length,
    });
  } catch (error) {
    /*
     * =======================================================
     * ROLLBACK
     * =======================================================
     */

    try {
      await client.query("ROLLBACK");
    } catch {
      // Ignore rollback errors.
    }

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