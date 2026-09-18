import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";

type TeacherSession = {
  id?: string;
  role?: string;
  academyId?: string | null;
};

async function getTeacher() {
  const cookieStore = await cookies();

  const value =
    cookieStore.get("master_session")?.value;

  if (!value) {
    return null;
  }

  let session: TeacherSession;

  const parsedSession = parseSessionCookie<TeacherSession>(value);

  if (!parsedSession) {
    return null;
  }

  session = parsedSession;

  if (
    session.role !== "TEACHER" ||
    !session.id
  ) {
    return null;
  }

  /*
   * IMPORTANT:
   *
   * Do not rely on academyId stored in an old session.
   * Always get the current teacher record from DB.
   */
  const result = await pool.query(
    `
    SELECT
      id,
      name,
      email,
      academy_id
    FROM teachers
    WHERE id = $1
    LIMIT 1
    `,
    [session.id]
  );

  if (result.rows.length === 0) {
    return null;
  }

  return result.rows[0] as {
    id: string;
    name: string;
    email: string;
    academy_id: string | null;
  };
}

export async function GET() {
  try {
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

    if (!teacher.academy_id) {
      return NextResponse.json(
        {
          success: false,
          error:
            "This teacher is not assigned to an academy yet.",
        },
        { status: 403 }
      );
    }

    const academyId = teacher.academy_id;

    /*
     * Load academy, batches and students together.
     */
    const [
      academyResult,
      batchesResult,
      studentsResult,
    ] = await Promise.all([
      /*
       * ACADEMY
       */
      pool.query(
        `
        SELECT
          id,
          name,
          code
        FROM academies
        WHERE id = $1
        LIMIT 1
        `,
        [academyId]
      ),

      /*
       * BATCHES
       *
       * Include the number of students in each batch.
       */
      pool.query(
        `
        SELECT
          b.id,
          b.name,
          b.class_name,
          COUNT(bs.student_id)::int AS student_count
        FROM batches b
        LEFT JOIN batch_students bs
          ON bs.batch_id = b.id
        WHERE b.academy_id = $1
        GROUP BY
          b.id,
          b.name,
          b.class_name
        ORDER BY b.name ASC
        `,
        [academyId]
      ),

      /*
       * STUDENTS
       */
      pool.query(
        `
        SELECT
          s.id,
          s.name,
          s.email,
          s.class_name
        FROM students s
        WHERE s.academy_id = $1
        ORDER BY s.name ASC
        `,
        [academyId]
      ),
    ]);

    if (academyResult.rows.length === 0) {
      return NextResponse.json(
        {
          success: false,
          error:
            "The academy assigned to this teacher could not be found.",
        },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,

      teacher: {
        id: teacher.id,
        name: teacher.name,
        email: teacher.email,
      },

      academy: academyResult.rows[0],

      academyId,

      batches: batchesResult.rows,

      students: studentsResult.rows,
    });
  } catch (error) {
    console.error(
      "TEACHER TARGETS ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Could not load your academy data.",
      },
      { status: 500 }
    );
  }
}