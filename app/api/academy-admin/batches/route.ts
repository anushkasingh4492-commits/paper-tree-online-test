import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { randomUUID } from "crypto";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";

const ALLOWED_COURSES = [
  "MHT-CET PCM",
  "MHT-CET PCB",
  "NEET PCB",
  "JEE PCM",
];

async function getBatchSession(
  targetAcademyId?: string
) {
  const value =
    (await cookies()).get("master_session")?.value;

  if (!value) return null;

  const session = parseSessionCookie<{
    id?: string;
    role?: string;
    academyId?: string;
  }>(value);

  if (!session) return null;

  // Academy Admin already belongs to one academy.
  if (
    session.role === "ACADEMY_ADMIN" &&
    session.id &&
    session.academyId
  ) {
    return session;
  }

  // Master Admin / Admin can work with
  // the academy selected in the UI.
  if (
    (session.role === "ADMIN" ||
      session.role === "MASTER_ADMIN") &&
    session.id &&
    targetAcademyId
  ) {
    return {
      ...session,
      academyId: targetAcademyId,
    };
  }

  return null;
}

export async function GET(request: Request) {
  try {
    const { searchParams } =
      new URL(request.url);

    const academyId =
      searchParams.get("academyId") ||
      undefined;

    const session =
      await getBatchSession(academyId);

    if (
      !session ||
      !session.academyId
    ) {
      return NextResponse.json(
        {
          success: false,
          error: "Unauthorized",
        },
        { status: 401 }
      );
    }

    await pool.query(`
      ALTER TABLE batches
      ADD COLUMN IF NOT EXISTS class_name VARCHAR(255)
    `);

    await pool.query(`
      ALTER TABLE batches
      ADD COLUMN IF NOT EXISTS course_name VARCHAR(255)
    `);

    const result =
      await pool.query(
        `
        SELECT
          b.id,
          b.name,
          b.class_name,
          b.course_name,
          b.created_at,
          COUNT(bs.student_id)::int AS student_count
        FROM batches b
        LEFT JOIN batch_students bs
          ON bs.batch_id = b.id
        WHERE b.academy_id = $1
        GROUP BY
          b.id,
          b.name,
          b.class_name,
          b.course_name,
          b.created_at
        ORDER BY b.name ASC
        `,
        [session.academyId]
      );

    return NextResponse.json({
      success: true,
      academyId: session.academyId,
      batches: result.rows,
    });
  } catch (error) {
    console.error(
      "ACADEMY BATCHES GET ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Could not load batches.",
      },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();

    const requestedAcademyId =
      String(
        body.academyId || ""
      ).trim();

    const session =
      await getBatchSession(
        requestedAcademyId ||
          undefined
      );

    if (
      !session ||
      !session.id ||
      !session.academyId
    ) {
      return NextResponse.json(
        {
          success: false,
          error: "Unauthorized",
        },
        { status: 401 }
      );
    }

    const name = String(
      body.name || ""
    ).trim();

    const className = String(
      body.className || ""
    ).trim();

    const courseName = String(
      body.courseName || ""
    )
      .trim()
      .toUpperCase();

    if (
      !name ||
      !className ||
      !courseName
    ) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Batch name, class and course are required.",
        },
        { status: 400 }
      );
    }

    if (
      !ALLOWED_COURSES.includes(
        courseName
      )
    ) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Invalid course. Choose MHT-CET PCM, MHT-CET PCB, NEET PCB or JEE PCM.",
        },
        { status: 400 }
      );
    }

    /*
     * Make sure these columns exist.
     */
    await pool.query(`
      ALTER TABLE batches
      ADD COLUMN IF NOT EXISTS class_name VARCHAR(255)
    `);

    await pool.query(`
      ALTER TABLE batches
      ADD COLUMN IF NOT EXISTS course_name VARCHAR(255)
    `);

    /*
     * created_by references teachers.
     *
     * Academy Admin can use its teacher ID.
     * Master Admin / Admin are not teachers,
     * so their batch creator must be NULL.
     */
    await pool.query(`
      ALTER TABLE batches
      ALTER COLUMN created_by DROP NOT NULL
    `);

  const createdBy = null;

    const result =
  await pool.query(
    `
    INSERT INTO batches (
      id,
      name,
      class_name,
      course_name,
      created_by,
      academy_id
    )
    VALUES (
      $1,
      $2,
      $3,
      $4,
      $5,
      $6
    )
    RETURNING
      id,
      name,
      class_name,
      course_name,
      created_at
    `,
    [
      randomUUID(),
      name,
      className,
      courseName,
      createdBy,
      session.academyId,
    ]
  );
    return NextResponse.json(
      {
        success: true,

        batch: {
          ...result.rows[0],
          student_count: 0,
        },
      },
      { status: 201 }
    );
  } catch (error) {
    console.error(
      "ACADEMY BATCHES POST ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Could not create batch.",
      },
      { status: 500 }
    );
  }
}

export async function DELETE(
  request: Request
) {
  try {
    const value =
      (await cookies()).get(
        "master_session"
      )?.value;

    const batchId =
      new URL(request.url)
        .searchParams.get("id") || "";

    if (!value) {
      return NextResponse.json(
        {
          success: false,
          error: "Unauthorized",
        },
        { status: 401 }
      );
    }

    const session =
      parseSessionCookie<{
        id?: string;
        role?: string;
        academyId?: string;
      }>(value);

    if (
      !session ||
      !session.academyId ||
      !session.id
    ) {
      return NextResponse.json(
        {
          success: false,
          error: "Invalid session",
        },
        { status: 401 }
      );
    }

    if (
      session.role !==
        "ACADEMY_ADMIN" &&
      session.role !== "ADMIN" &&
      session.role !== "MASTER_ADMIN"
    ) {
      return NextResponse.json(
        {
          success: false,
          error: "Unauthorized",
        },
        { status: 401 }
      );
    }

    const scheduled =
      await pool.query(
        `
        SELECT 1
        FROM scheduled_tests
        WHERE batch_id = $1
          AND academy_id = $2
        LIMIT 1
        `,
        [
          batchId,
          session.academyId,
        ]
      );

    if (scheduled.rowCount) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Cancel this batch's scheduled tests before removing the batch.",
        },
        { status: 409 }
      );
    }

    const client =
      await pool.connect();

    try {
      await client.query(
        "BEGIN"
      );

      await client.query(
        `
        DELETE FROM batch_students
        WHERE batch_id = $1
        `,
        [batchId]
      );

      const result =
        await client.query(
          `
          DELETE FROM batches
          WHERE id = $1
            AND academy_id = $2
          RETURNING id
          `,
          [
            batchId,
            session.academyId,
          ]
        );

      await client.query(
        "COMMIT"
      );

      if (!result.rowCount) {
        return NextResponse.json(
          {
            success: false,
            error:
              "Batch not found.",
          },
          { status: 404 }
        );
      }

      return NextResponse.json({
        success: true,
      });
    } catch (error) {
      await client.query(
        "ROLLBACK"
      );

      throw error;
    } finally {
      client.release();
    }
  } catch (error) {
    console.error(
      "ACADEMY BATCHES DELETE ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Could not remove batch.",
      },
      { status: 500 }
    );
  }
}