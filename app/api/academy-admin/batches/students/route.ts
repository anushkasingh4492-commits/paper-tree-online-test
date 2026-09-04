import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";

async function getAcademyAdmin() {
  const cookieStore = await cookies();
  const session = cookieStore.get("master_session")?.value;

  if (!session) return null;

  try {
    const data = JSON.parse(session);

    if (data.role !== "ACADEMY_ADMIN" || !data.academyId) {
      return null;
    }

    return data;
  } catch {
    return null;
  }
}

// Get students assigned to a batch
export async function GET(req: Request) {
  const admin = await getAcademyAdmin();

  if (!admin) {
    return NextResponse.json(
      { success: false, error: "Unauthorized" },
      { status: 401 }
    );
  }

  try {
    const { searchParams } = new URL(req.url);
    const batchId = searchParams.get("batchId");

    if (!batchId) {
      return NextResponse.json(
        { success: false, error: "Batch ID is required" },
        { status: 400 }
      );
    }

    const batch = await pool.query(
      `
      SELECT id
      FROM batches
      WHERE id = $1
        AND academy_id = $2
      LIMIT 1
      `,
      [batchId, admin.academyId]
    );

    if (batch.rows.length === 0) {
      return NextResponse.json(
        { success: false, error: "Batch not found" },
        { status: 404 }
      );
    }

    const result = await pool.query(
      `
      SELECT
        s.id,
        s.name,
        s.email,
        s.roll_number,
        s.class_name
      FROM batch_students bs
      INNER JOIN students s
        ON s.id = bs.student_id
      WHERE bs.batch_id = $1
        AND s.academy_id = $2
      ORDER BY s.name
      `,
      [batchId, admin.academyId]
    );

    return NextResponse.json({
      success: true,
      students: result.rows,
    });
  } catch (error) {
    console.error("BATCH STUDENTS GET ERROR:", error);

    return NextResponse.json(
      { success: false, error: "Failed to load batch students" },
      { status: 500 }
    );
  }
}

// Add/remove student from batch
export async function POST(req: Request) {
  const admin = await getAcademyAdmin();

  if (!admin) {
    return NextResponse.json(
      { success: false, error: "Unauthorized" },
      { status: 401 }
    );
  }

  try {
    const body = await req.json();

    const batchId = String(body.batchId || "").trim();
    const studentId = String(body.studentId || "").trim();
    const action = String(body.action || "").trim();

    if (!batchId || !studentId) {
      return NextResponse.json(
        {
          success: false,
          error: "Batch ID and student ID are required",
        },
        { status: 400 }
      );
    }

    if (action !== "add" && action !== "remove") {
      return NextResponse.json(
        {
          success: false,
          error: "Invalid action",
        },
        { status: 400 }
      );
    }

    // Verify batch belongs to this academy
    const batch = await pool.query(
      `
      SELECT id
      FROM batches
      WHERE id = $1
        AND academy_id = $2
      LIMIT 1
      `,
      [batchId, admin.academyId]
    );

    if (batch.rows.length === 0) {
      return NextResponse.json(
        { success: false, error: "Batch not found" },
        { status: 404 }
      );
    }

    // Verify student belongs to the same academy
    const student = await pool.query(
      `
      SELECT id
      FROM students
      WHERE id = $1
        AND academy_id = $2
      LIMIT 1
      `,
      [studentId, admin.academyId]
    );

    if (student.rows.length === 0) {
      return NextResponse.json(
        { success: false, error: "Student not found" },
        { status: 404 }
      );
    }

    if (action === "add") {
      await pool.query(
        `
        INSERT INTO batch_students
          (batch_id, student_id)
        VALUES
          ($1, $2)
        ON CONFLICT DO NOTHING
        `,
        [batchId, studentId]
      );
    } else {
      await pool.query(
        `
        DELETE FROM batch_students
        WHERE batch_id = $1
          AND student_id = $2
        `,
        [batchId, studentId]
      );
    }

    return NextResponse.json({
      success: true,
      action,
    });
  } catch (error) {
    console.error("BATCH STUDENTS POST ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error: "Failed to update batch students",
      },
      { status: 500 }
    );
  }
}
