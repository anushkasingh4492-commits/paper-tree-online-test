import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { randomUUID } from "crypto";
import bcrypt from "bcryptjs";
import { pool } from "@/lib/db";

async function getAcademyAdmin(targetAcademyId?: string) {
  const cookieStore = await cookies();
  const session = cookieStore.get("master_session")?.value;

  if (!session) return null;

  try {
    const data = JSON.parse(session);

    if (data.role === "ACADEMY_ADMIN" && data.academyId) {
      return data;
    }

    if (
      (data.role === "ADMIN" || data.role === "MASTER_ADMIN") &&
      targetAcademyId
    ) {
      return { ...data, academyId: targetAcademyId };
    }

    return null;
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
  const body = await req.json();
  const admin = await getAcademyAdmin(body.academyId);

  if (!admin) {
    return NextResponse.json(
      { success: false, error: "Unauthorized" },
      { status: 401 }
    );
  }

  try {
    const name = String(body.name || "").trim();
    const email = String(body.email || "").trim().toLowerCase();
    const password = String(body.password || "");
    const rollNumber = String(body.rollNumber || "").trim();
    const className = String(body.className || "").trim();

    if (!name || !email || !password) {
      return NextResponse.json(
        {
          success: false,
          error: "Name, email and password are required",
        },
        { status: 400 }
      );
    }

    if (password.length < 6) {
      return NextResponse.json(
        {
          success: false,
          error: "Student password must be at least 6 characters",
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
          error:
            "This email is already registered. Use a different email for another student.",
        },
        { status: 409 }
      );
    }

    const studentId = randomUUID();
    const passwordHash = await bcrypt.hash(password, 10);

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

    await pool.query(
      `
      INSERT INTO student_credentials
        (student_id, password_hash)
      VALUES
        ($1, $2)
      `,
      [studentId, passwordHash]
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
      credentials: {
        username: email,
        password,
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