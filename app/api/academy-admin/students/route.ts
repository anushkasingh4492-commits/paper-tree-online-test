import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { randomUUID } from "crypto";
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

export async function GET() {
  const admin = await getAcademyAdmin();

  if (!admin) {
    return NextResponse.json(
      { success: false, error: "Unauthorized" },
      { status: 401 }
    );
  }

  try {
    const result = await pool.query(
      `
      SELECT
        id,
        name,
        email,
        roll_number,
        class_name,
        created_at
      FROM students
      WHERE academy_id = $1
      ORDER BY name
      `,
      [admin.academyId]
    );

    return NextResponse.json({
      success: true,
      students: result.rows,
    });
  } catch (error) {
    console.error("ACADEMY STUDENTS GET ERROR:", error);

    return NextResponse.json(
      { success: false, error: "Failed to load students" },
      { status: 500 }
    );
  }
}

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

    const name = String(body.name || "").trim();
    const email = String(body.email || "").trim().toLowerCase();
    const rollNumber = String(body.rollNumber || "").trim();
    const className = String(body.className || "").trim();

    if (!name || !email) {
      return NextResponse.json(
        {
          success: false,
          error: "Name and email are required",
        },
        { status: 400 }
      );
    }

    const existing = await pool.query(
      `
      SELECT id
      FROM students
      WHERE LOWER(email) = LOWER($1)
      `,
      [email]
    );

    if (existing.rows.length > 0) {
      return NextResponse.json(
        {
          success: false,
          error: "Student email already exists",
        },
        { status: 409 }
      );
    }

    const studentId = randomUUID();

    await pool.query(
      `
      INSERT INTO students
        (
          id,
          name,
          email,
          roll_number,
          class_name,
          academy_id
        )
      VALUES
        ($1, $2, $3, $4, $5, $6)
      `,
      [
        studentId,
        name,
        email,
        rollNumber || null,
        className || null,
        admin.academyId,
      ]
    );

    return NextResponse.json({
      success: true,
      student: {
        id: studentId,
        name,
        email,
        rollNumber,
        className,
      },
    });
  } catch (error) {
    console.error("ACADEMY STUDENTS POST ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error: "Failed to create student",
      },
      { status: 500 }
    );
  }
}