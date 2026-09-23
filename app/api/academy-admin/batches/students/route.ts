import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";

type Session = {
  id?: string;
  role?: string;
  academyId?: string | null;
};

async function getSession(): Promise<Session | null> {
  const value = (await cookies()).get("master_session")?.value;

  if (!value) {
    return null;
  }

  return parseSessionCookie<Session>(value);
}

/**
 * Returns the academy the current user is authorized to manage.
 *
 * ACADEMY_ADMIN:
 *   - Can manage ONLY their own academy.
 *   - academyId comes from their session.
 *
 * ADMIN / MASTER_ADMIN:
 *   - Can manage any academy.
 *   - academyId must come from the selected academy in the UI.
 */
async function getAuthorizedAcademyId(
  requestedAcademyId?: string
): Promise<string | null> {
  const session = await getSession();

  if (!session || !session.id || !session.role) {
    return null;
  }

  // Academy Admin → own academy only
  if (session.role === "ACADEMY_ADMIN") {
    return session.academyId || null;
  }

  // Master Admin → selected academy
  if (
    session.role === "ADMIN" ||
    session.role === "MASTER_ADMIN"
  ) {
    return requestedAcademyId || null;
  }

  return null;
}

/**
 * GET
 *
 * Loads all students currently assigned to a batch.
 *
 * Academy Admin:
 *   /api/academy-admin/batches/students?batchId=XXX
 *
 * Master Admin:
 *   /api/academy-admin/batches/students?batchId=XXX&academyId=XXX
 */
export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);

    const batchId =
      searchParams.get("batchId")?.trim() || "";

    const requestedAcademyId =
      searchParams.get("academyId")?.trim() || "";

    if (!batchId) {
      return NextResponse.json(
        {
          success: false,
          error: "Batch ID is required.",
        },
        { status: 400 }
      );
    }

    const academyId = await getAuthorizedAcademyId(
      requestedAcademyId
    );

    if (!academyId) {
      return NextResponse.json(
        {
          success: false,
          error: "Unauthorized",
        },
        { status: 401 }
      );
    }

    /*
     * Make sure:
     * 1. The batch belongs to the authorized academy.
     * 2. The students belong to the same academy.
     */
    const result = await pool.query(
      `
      SELECT
        s.id,
        s.name,
        s.email,
        s.roll_number
      FROM batch_students bs
      INNER JOIN students s
        ON s.id = bs.student_id
      INNER JOIN batches b
        ON b.id = bs.batch_id
      WHERE bs.batch_id = $1
        AND b.academy_id = $2
        AND s.academy_id = $2
      ORDER BY s.name ASC
      `,
      [batchId, academyId]
    );

    return NextResponse.json({
      success: true,
      students: result.rows,
    });
  } catch (error) {
    console.error(
      "BATCH STUDENTS GET ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Could not load batch students.",
      },
      { status: 500 }
    );
  }
}

/**
 * POST
 *
 * Adds or removes a student from a batch.
 *
 * body:
 * {
 *   batchId: string,
 *   studentId: string,
 *   academyId?: string,
 *   action?: "add" | "remove"
 * }
 *
 * Academy Admin:
 *   academyId is taken from the session.
 *
 * Master Admin:
 *   academyId comes from the selected academy.
 */
export async function POST(request: Request) {
  try {
    const body = await request.json();

    const batchId =
      String(body.batchId || "").trim();

    const studentId =
      String(body.studentId || "").trim();

    const requestedAcademyId =
      String(body.academyId || "").trim();

    const action =
      String(body.action || "add")
        .trim()
        .toLowerCase();

    if (!batchId || !studentId) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Batch ID and student ID are required.",
        },
        { status: 400 }
      );
    }

    if (action !== "add" && action !== "remove") {
      return NextResponse.json(
        {
          success: false,
          error:
            'Action must be either "add" or "remove".',
        },
        { status: 400 }
      );
    }

    const academyId = await getAuthorizedAcademyId(
      requestedAcademyId
    );

    if (!academyId) {
      return NextResponse.json(
        {
          success: false,
          error: "Unauthorized",
        },
        { status: 401 }
      );
    }

    /*
     * Verify BOTH records belong to the academy
     * the current user is authorized to manage.
     *
     * This prevents:
     * - adding a student from another academy
     * - adding to a batch from another academy
     * - cross-academy assignments
     */
    const ownership = await pool.query(
      `
      SELECT
        b.id AS batch_id,
        s.id AS student_id
      FROM batches b
      CROSS JOIN students s
      WHERE b.id = $1
        AND s.id = $2
        AND b.academy_id = $3
        AND s.academy_id = $3
      LIMIT 1
      `,
      [
        batchId,
        studentId,
        academyId,
      ]
    );

    if (!ownership.rowCount) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Batch or student was not found in this academy.",
        },
        { status: 404 }
      );
    }

    // Remove student from batch
    if (action === "remove") {
      await pool.query(
        `
        DELETE FROM batch_students
        WHERE batch_id = $1
          AND student_id = $2
        `,
        [batchId, studentId]
      );

      return NextResponse.json({
        success: true,
        action: "removed",
      });
    }

    // Add student to batch
    await pool.query(
      `
      INSERT INTO batch_students (
        batch_id,
        student_id
      )
      VALUES ($1, $2)
      ON CONFLICT DO NOTHING
      `,
      [batchId, studentId]
    );

    return NextResponse.json({
      success: true,
      action: "added",
    });
  } catch (error) {
    console.error(
      "BATCH STUDENTS POST ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Could not update batch students.",
      },
      { status: 500 }
    );
  }
}