import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";

type StudentSession = {
  studentId?: string;
  email?: string;
};

export async function GET() {
  try {
    const cookieStore = await cookies();

    const sessionCookie =
      cookieStore.get("student_session")?.value;

    if (!sessionCookie) {
      return NextResponse.json(
        {
          success: false,
          error: "Student session required.",
        },
        { status: 401 }
      );
    }

    const session =
      parseSessionCookie<StudentSession>(
        sessionCookie
      );

    if (!session) {
      return NextResponse.json(
        {
          success: false,
          error: "Invalid student session.",
        },
        { status: 401 }
      );
    }

    const sessionStudentId =
      String(
        session.studentId || ""
      ).trim();

    const sessionEmail =
      String(
        session.email || ""
      )
        .trim()
        .toLowerCase();

    if (
      !sessionStudentId &&
      !sessionEmail
    ) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Student information missing from session.",
        },
        { status: 401 }
      );
    }

    /*
     * Make sure batch fields exist.
     */
    await pool.query(`
      ALTER TABLE batches
      ADD COLUMN IF NOT EXISTS course_name VARCHAR(255)
    `);

    await pool.query(`
      ALTER TABLE batches
      ADD COLUMN IF NOT EXISTS class_name VARCHAR(255)
    `);

    /*
     * Resolve the student.
     */
    let studentResult;

    if (sessionStudentId) {
      studentResult =
        await pool.query(
          `
          SELECT
            id,
            name,
            email,
            academy_id
          FROM students
          WHERE id = $1
          LIMIT 1
          `,
          [sessionStudentId]
        );
    } else {
      studentResult = {
        rows: [],
        rowCount: 0,
      };
    }

    /*
     * Email fallback.
     */
    if (
      !studentResult.rowCount &&
      sessionEmail
    ) {
      studentResult =
        await pool.query(
          `
          SELECT
            id,
            name,
            email,
            academy_id
          FROM students
          WHERE LOWER(email) = $1
          LIMIT 1
          `,
          [sessionEmail]
        );
    }

    if (!studentResult.rowCount) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Student account could not be found.",
        },
        { status: 404 }
      );
    }

    const student =
      studentResult.rows[0];

    /*
     * Get all batches assigned to this student.
     *
     * Prefer batches that have a course_name because
     * the test generator needs it to determine the
     * student's course/group.
     */
    const result =
      await pool.query(
        `
        SELECT
          b.id AS batch_id,
          b.name AS batch_name,
          b.course_name,
          b.class_name,
          b.academy_id,
          b.created_at
        FROM batch_students bs
        INNER JOIN batches b
          ON b.id = bs.batch_id
        WHERE bs.student_id = $1
        ORDER BY
          CASE
            WHEN b.course_name IS NOT NULL
              AND TRIM(b.course_name) <> ''
            THEN 0
            ELSE 1
          END,
          b.created_at DESC
        `,
        [student.id]
      );

    if (!result.rowCount) {
      return NextResponse.json(
        {
          success: false,
          error:
            "You have not been assigned to a batch yet.",
        },
        { status: 404 }
      );
    }

    /*
     * Pick the first valid assignment.
     */
    const assignment =
      result.rows[0];

    /*
     * Course is required for the test generator.
     */
    if (
      !assignment.course_name ||
      !String(
        assignment.course_name
      ).trim()
    ) {
      return NextResponse.json(
        {
          success: false,
          error:
            `Your batch "${assignment.batch_name}" does not have a course assigned. Please ask the academy admin to update the batch course.`,
        },
        { status: 400 }
      );
    }

    return NextResponse.json({
      success: true,
      assignment,
    });
  } catch (error) {
    console.error(
      "STUDENT ASSIGNMENT ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Could not load student assignment.",
      },
      { status: 500 }
    );
  }
}