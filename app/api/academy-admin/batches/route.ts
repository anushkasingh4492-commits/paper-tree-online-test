import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { randomUUID } from "crypto";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function GET() {
  try {
    const cookieStore = await cookies();
    const sessionCookie = cookieStore.get("master_session")?.value;

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
      academyId?: string | null;
    };

    try {
      session = JSON.parse(decodeURIComponent(sessionCookie));
    } catch {
      return NextResponse.json(
        {
          success: false,
          error: "Invalid login session. Please log in again.",
        },
        { status: 401 }
      );
    }

    if (session.role !== "ACADEMY_ADMIN" || !session.id || !session.academyId) {
      return NextResponse.json(
        {
          success: false,
          error: "Invalid teacher session. Please log in again.",
        },
        { status: 401 }
      );
    }

    /*
     * Get the academy from the session first.
     * If an older session does not contain academyId,
     * resolve it directly from the teacher account.
     */
    const academyId = session.academyId;

    if (!academyId) {
      return NextResponse.json(
        {
          success: false,
          error:
            "This teacher is not assigned to an academy yet.",
        },
        { status: 403 }
      );
    }

    /*
     * IMPORTANT:
     * Load actual batches belonging to this academy.
     */
    const batchesResult = await pool.query(
      `
      SELECT
        b.id,
        b.name,
        b.class_name,
        b.created_at,
        COUNT(bs.student_id)::int AS student_count
      FROM batches b
      LEFT JOIN batch_students bs ON bs.batch_id = b.id
      WHERE b.academy_id = $1
      GROUP BY b.id
      ORDER BY b.name ASC
      `,
      [academyId]
    );

    /*
     * Load students belonging to this academy.
     */
    const studentsResult = await pool.query(
      `
      SELECT
        id,
        name,
        email,
        roll_number,
        class_name
      FROM students
      WHERE academy_id = $1
      ORDER BY name ASC
      `,
      [academyId]
    );

    return NextResponse.json({
      success: true,
      academyId,
      batches: batchesResult.rows,
      students: studentsResult.rows,
    });
  } catch (error) {
    console.error("TEACHER TARGETS ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Could not load batches and students.",
      },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  const value = (await cookies()).get("master_session")?.value;

  if (!value) {
    return NextResponse.json(
      { success: false, error: "Unauthorized" },
      { status: 401 }
    );
  }

  let session: {
    id?: string;
    role?: string;
    academyId?: string;
  };

  try {
    session = JSON.parse(decodeURIComponent(value));
  } catch {
    return NextResponse.json(
      { success: false, error: "Invalid session" },
      { status: 401 }
    );
  }

  if (
    session.role !== "ACADEMY_ADMIN" ||
    !session.id ||
    !session.academyId
  ) {
    return NextResponse.json(
      { success: false, error: "Unauthorized" },
      { status: 401 }
    );
  }

  const body = await request.json();

  const name = String(body.name ?? "").trim();
  const courseName = String(body.courseName ?? "").trim();

  if (!name || !courseName) {
    return NextResponse.json(
      {
        success: false,
        error: "Batch name and course are required.",
      },
      { status: 400 }
    );
  }

  // Make sure the database has the course column.
  await pool.query(`
    ALTER TABLE batches
    ADD COLUMN IF NOT EXISTS course_name VARCHAR(255)
  `);

  const result = await pool.query(
    `
    INSERT INTO batches (
      id,
      name,
      class_name,
      course_name,
      created_by,
      academy_id
    )
    VALUES ($1, $2, NULL, $3, $4, $5)
    RETURNING
      id,
      name,
      course_name,
      created_at
    `,
    [
      randomUUID(),
      name,
      courseName,
      session.id,
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
}
  

export async function DELETE(request: Request) {
  const value = (await cookies()).get("master_session")?.value;
  const batchId = new URL(request.url).searchParams.get("id") || "";
  if (!value) return NextResponse.json({ success: false, error: "Unauthorized" }, { status: 401 });
  let session: { role?: string; academyId?: string };
  try { session = JSON.parse(decodeURIComponent(value)); } catch { return NextResponse.json({ success: false, error: "Invalid session" }, { status: 401 }); }
  if (session.role !== "ACADEMY_ADMIN" || !session.academyId) return NextResponse.json({ success: false, error: "Unauthorized" }, { status: 401 });
  const scheduled = await pool.query(`SELECT 1 FROM scheduled_tests WHERE batch_id=$1 AND academy_id=$2 LIMIT 1`, [batchId, session.academyId]);
  if (scheduled.rowCount) return NextResponse.json({ success: false, error: "Cancel this batch's scheduled tests before removing the batch." }, { status: 409 });
  const client = await pool.connect();
  try { await client.query("BEGIN"); await client.query(`DELETE FROM batch_students WHERE batch_id=$1`, [batchId]); const result = await client.query(`DELETE FROM batches WHERE id=$1 AND academy_id=$2 RETURNING id`, [batchId, session.academyId]); await client.query("COMMIT"); if (!result.rowCount) return NextResponse.json({ success: false, error: "Batch not found." }, { status: 404 }); return NextResponse.json({ success: true }); } catch (error) { await client.query("ROLLBACK"); return NextResponse.json({ success: false, error: error instanceof Error ? error.message : "Could not remove batch." }, { status: 500 }); } finally { client.release(); }
}
