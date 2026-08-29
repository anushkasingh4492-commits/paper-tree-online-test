import { NextResponse } from "next/server";
import { pool } from "@/lib/db";
import bcrypt from "bcryptjs";

export const runtime = "nodejs";

export async function POST(request: Request) {
  try {
    const body = await request.json();

    const name =
      typeof body.name === "string"
        ? body.name.trim()
        : "";

    const email =
      typeof body.email === "string"
        ? body.email.trim().toLowerCase()
        : "";

    const password =
      typeof body.password === "string"
        ? body.password
        : "";

    const role =
      typeof body.role === "string"
        ? body.role.trim().toUpperCase()
        : "";

    if (!name || !email || !password || !role) {
      return NextResponse.json(
        {
          success: false,
          error:
            "name, email, password and role are required.",
        },
        { status: 400 }
      );
    }

    if (!["ADMIN", "TEACHER"].includes(role)) {
      return NextResponse.json(
        {
          success: false,
          error: "Role must be ADMIN or TEACHER.",
        },
        { status: 400 }
      );
    }

    await pool.query(`
      CREATE TABLE IF NOT EXISTS staff_users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK (role IN ('ADMIN', 'TEACHER')),
        teacher_id TEXT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
      );
    `);

    const existing = await pool.query(
      `
      SELECT id
      FROM staff_users
      WHERE LOWER(email) = $1
      LIMIT 1
      `,
      [email]
    );

    if (existing.rows.length > 0) {
      return NextResponse.json(
        {
          success: false,
          error: "A staff account with this email already exists.",
        },
        { status: 409 }
      );
    }

    let teacherId: string | null = null;

    if (role === "TEACHER") {
      const teacher = await pool.query(
        `
        SELECT id
        FROM teachers
        WHERE LOWER(email) = $1
        LIMIT 1
        `,
        [email]
      );

      if (teacher.rows.length > 0) {
        teacherId = teacher.rows[0].id;
      }
    }

    const passwordHash =
      await bcrypt.hash(password, 12);

    const id =
      `staff-${Date.now()}-${Math.random()
        .toString(36)
        .slice(2, 8)}`;

    await pool.query(
      `
      INSERT INTO staff_users (
        id,
        name,
        email,
        password_hash,
        role,
        teacher_id
      )
      VALUES ($1, $2, $3, $4, $5, $6)
      `,
      [
        id,
        name,
        email,
        passwordHash,
        role,
        teacherId,
      ]
    );

    return NextResponse.json({
      success: true,
      staff: {
        id,
        name,
        email,
        role,
        teacherId,
      },
    });
  } catch (error: unknown) {
    console.error(
      "STAFF SETUP ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to create staff account.",
      },
      { status: 500 }
    );
  }
}
