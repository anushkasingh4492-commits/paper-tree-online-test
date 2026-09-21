import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";

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
      parseSessionCookie<Record<string, unknown>>(
        sessionCookie
      );

    const studentId = String(
      session?.studentId || ""
    );

    const academyId = String(
      session?.academyId || ""
    );

    if (!studentId || !academyId) {
      return NextResponse.json(
        {
          success: false,
          error: "Invalid student session.",
        },
        { status: 401 }
      );
    }

    /*
     * Make sure the batch has a course column.
     * No psql required.
     */
    await pool.query(`
      ALTER TABLE batches
      ADD COLUMN IF NOT EXISTS course_name VARCHAR(255)
    `);

    /*
     * Get the student's assigned batch.
     */
    const result = await pool.query(
      `
      SELECT
        b.id AS batch_id,
        b.name AS batch_name,
        b.course_name,
        b.class_name
      FROM batch_students bs
      INNER JOIN batches b
        ON b.id = bs.batch_id
      INNER JOIN students s
        ON s.id = bs.student_id
      WHERE bs.student_id = $1
        AND s.academy_id = $2
        AND b.academy_id = $2
      ORDER BY bs.created_at DESC
      LIMIT 1
      `,
      [studentId, academyId]
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

    const assignment = result.rows[0];

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
            : "Could not load student course.",
      },
      { status: 500 }
    );
  }
}