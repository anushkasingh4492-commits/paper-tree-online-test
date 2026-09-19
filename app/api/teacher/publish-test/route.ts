import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";

type Session = {
  id?: string;
  role?: string;
};

async function getTeacher() {
  const cookieStore = await cookies();

  const value = cookieStore.get("master_session")?.value;

  if (!value) {
    return null;
  }

  const parsedSession = parseSessionCookie<Session>(value);

  if (!parsedSession) {
    return null;
  }

  const session = parsedSession;

  if (session.role !== "TEACHER" || !session.id) {
    return null;
  }

  const result = await pool.query(
    `
      SELECT
        id,
        name,
        email,
        academy_id
      FROM teachers
      WHERE id::text = $1::text
      LIMIT 1
    `,
    [session.id]
  );

  if (
    result.rows.length === 0 ||
    !result.rows[0].academy_id
  ) {
    return null;
  }

  return result.rows[0] as {
    id: string;
    name: string;
    email: string;
    academy_id: string;
  };
}

export async function POST(request: Request) {
  const client = await pool.connect();

  try {
    // =======================================================
    // TEACHER
    // =======================================================

    const teacher = await getTeacher();

    if (!teacher) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Teacher account was not found. Please log in again.",
        },
        { status: 401 }
      );
    }

    const academyId = String(teacher.academy_id);

    // =======================================================
    // REQUEST BODY
    // =======================================================

    const body = await request.json();

    const batchId = body.batchId
      ? String(body.batchId).trim()
      : null;

    const requestedStudentIds = Array.isArray(body.studentIds)
      ? body.studentIds
          .map((id: unknown) => String(id).trim())
          .filter(Boolean)
      : body.studentId
        ? [String(body.studentId).trim()]
        : [];

    // =======================================================
    // TARGET VALIDATION
    // =======================================================

    if (!batchId && requestedStudentIds.length === 0) {
      return NextResponse.json(
        {
          success: false,
          error: "Select a batch or a student.",
        },
        { status: 400 }
      );
    }

    if (batchId && requestedStudentIds.length > 0) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Select either a batch or a single student, not both.",
        },
        { status: 400 }
      );
    }

    // =======================================================
    // TEST DETAILS
    // =======================================================

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
          error: "End time must be after start time.",
        },
        { status: 400 }
      );
    }

    const duration = Math.max(
      1,
      Number(body.duration) || 60
    );

    const allowReattempt =
      body.allowReattempt === true;

    // =======================================================
    // GENERATED TEST
    // =======================================================

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

    const questions = Array.isArray(
      generatedTest.questions
    )
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
          error: "No generated questions were found.",
        },
        { status: 400 }
      );
    }

    // =======================================================
    // VERIFY BATCH
    // =======================================================

    let recipientStudentIds: string[] = [];

    if (batchId) {
      const batchCheck = await client.query(
        `
          SELECT
            b.id,
            b.name,
            b.class_name,
            COUNT(bs.student_id)::int AS student_count
          FROM batches b
          LEFT JOIN batch_students bs
            ON bs.batch_id::text = b.id::text
          WHERE b.id::text = $1::text
            AND b.academy_id::text = $2::text
          GROUP BY
            b.id,
            b.name,
            b.class_name
          LIMIT 1
        `,
        [batchId, academyId]
      );

      if (batchCheck.rowCount === 0) {
        return NextResponse.json(
          {
            success: false,
            error: "Batch not found in your academy.",
          },
          { status: 403 }
        );
      }

      const recipients = await client.query(
        `
          SELECT s.id
          FROM batch_students bs
          INNER JOIN students s
            ON s.id::text = bs.student_id::text
          WHERE bs.batch_id::text = $1::text
            AND s.academy_id::text = $2::text
          ORDER BY s.id::text
        `,
        [batchId, academyId]
      );

      recipientStudentIds = recipients.rows.map(
        (row) => String(row.id)
      );

      if (recipientStudentIds.length === 0) {
        return NextResponse.json(
          {
            success: false,
            error:
              "This batch has no students. Add students to the batch first.",
          },
          { status: 409 }
        );
      }
    }

    // =======================================================
    // VERIFY STUDENTS
    // =======================================================

    if (requestedStudentIds.length > 0) {
      const studentCheck = await client.query(
        `
          SELECT
            id,
            name,
            email,
            class_name
          FROM students
          WHERE id::text = ANY($1::text[])
            AND academy_id::text = $2::text
        `,
        [requestedStudentIds, academyId]
      );

      if (
        studentCheck.rowCount !==
        requestedStudentIds.length
      ) {
        return NextResponse.json(
          {
            success: false,
            error:
              "Student not found in your academy.",
          },
          { status: 403 }
        );
      }

      recipientStudentIds = requestedStudentIds;
    }

    // =======================================================
    // TRANSACTION
    // =======================================================

    await client.query("BEGIN");

    // =======================================================
    // ENSURE REQUIRED COLUMNS EXIST
    // =======================================================

    await client.query(`
      ALTER TABLE tests
      ADD COLUMN IF NOT EXISTS academy_id UUID
    `);

    await client.query(`
      ALTER TABLE scheduled_tests
      ADD COLUMN IF NOT EXISTS test_id UUID,
      ADD COLUMN IF NOT EXISTS allow_reattempt BOOLEAN NOT NULL DEFAULT FALSE
    `);

    // =======================================================
    // CREATE TEST
    // =======================================================

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
          $1::uuid,
          $2,
          $3,
          $4::jsonb,
          NOW(),
          $5,
          $6::uuid
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

    // =======================================================
    // CREATE TEST QUESTIONS
    // =======================================================

    for (let i = 0; i < questions.length; i++) {
      const questionId = String(
        questions[i]?.id ||
          questions[i]?.question_id ||
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
            $1::uuid,
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

    // =======================================================
    // CREATE PAPER
    // =======================================================

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
          $1::uuid,
          $2,
          $3,
          $4,
          $5,
          $6,
          $7::uuid,
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

        teacher.id,

        academyId,
      ]
    );

    // =======================================================
    // LINK QUESTIONS TO PAPER
    // =======================================================

    for (let i = 0; i < questions.length; i++) {
      const questionId = String(
        questions[i]?.id ||
          questions[i]?.question_id ||
          ""
      ).trim();

      if (!questionId) {
        continue;
      }

      await client.query(
        `
          INSERT INTO paper_questions (
            paper_id,
            question_id,
            question_order
          )
          VALUES (
            $1::uuid,
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

    // =======================================================
    // CREATE SCHEDULED TEST
    // =======================================================

    const scheduledTestId =
      crypto.randomUUID();

    await client.query(
      `
        INSERT INTO scheduled_tests (
          id,
          test_id,
          paper_id,
          batch_id,
          title,
          start_time,
          end_time,
          duration_minutes,
          allow_reattempt,
          status,
          academy_id,
          created_at
        )
        VALUES (
          $1::uuid,
          $2::uuid,
          $3::uuid,
          $4,
          $5,
          $6,
          $7,
          $8,
          $9,
          $10,
          $11::uuid,
          NOW()
        )
      `,
      [
        scheduledTestId,
        testId,
        paperId,
        batchId,
        title,
        startTime.toISOString(),
        endTime.toISOString(),
        duration,
        allowReattempt,
        "Upcoming",
        academyId,
      ]
    );

    // =======================================================
    // ASSIGN STUDENTS
    // =======================================================

    if (recipientStudentIds.length > 0) {
      await client.query(
        `
          INSERT INTO scheduled_test_students (
            scheduled_test_id,
            student_id,
            created_at
          )
          SELECT
            $1::uuid,
            recipient.student_id::uuid,
            NOW()
          FROM UNNEST($2::text[]) AS recipient(student_id)
          ON CONFLICT (
            scheduled_test_id,
            student_id
          ) DO NOTHING
        `,
        [
          scheduledTestId,
          recipientStudentIds,
        ]
      );
    }

    // =======================================================
    // NOTIFICATIONS
    // =======================================================

    await client.query(
      `
        INSERT INTO notifications (
          id,
          student_id,
          scheduled_test_id,
          title,
          message,
          is_read,
          created_at
        )
        SELECT
          gen_random_uuid()::text,
          recipient.student_id::text,
          $1::text,
          $2,
          $3,
          false,
          NOW()
        FROM UNNEST($4::text[]) AS recipient(student_id)
      `,
      [
        scheduledTestId,
        "New test scheduled",
        `${title} starts ${startTime.toLocaleString(
          "en-IN",
          {
            day: "2-digit",
            month: "short",
            hour: "2-digit",
            minute: "2-digit",
          }
        )}.`,
        recipientStudentIds,
      ]
    );

    // =======================================================
    // COMMIT
    // =======================================================

    await client.query("COMMIT");

    // =======================================================
    // RESPONSE
    // =======================================================

    return NextResponse.json({
      success: true,

      message: `Test published! ${
        recipientStudentIds.length
      } student${
        recipientStudentIds.length === 1
          ? ""
          : "s"
      } notified.`,

      testId,

      paperId,

      scheduledTestId,

      title,

      targetType: batchId
        ? "batch"
        : "students",

      batchId,

      studentIds: recipientStudentIds,

      academyId,

      startTime:
        startTime.toISOString(),

      endTime:
        endTime.toISOString(),

      duration,

      questionCount:
        questions.length,

      notifiedStudents:
        recipientStudentIds.length,
    });
  } catch (error) {
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