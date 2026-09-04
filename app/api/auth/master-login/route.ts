import { NextResponse } from "next/server";
import bcrypt from "bcryptjs";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function POST(request: Request) {
  try {
    const body = await request.json();

    const email = String(body.email || "").trim().toLowerCase();
    const password = String(body.password || "");

    if (!email || !password) {
      return NextResponse.json(
        { success: false, error: "Email and password are required." },
        { status: 400 }
      );
    }

    // ==========================================
    // ADMIN / ACADEMY ADMIN
    // ==========================================

    const adminResult = await pool.query(
      `
      SELECT
        id,
        name,
        email,
        password_hash,
        academy_id,
        is_master
      FROM admins
      WHERE LOWER(email) = $1
      LIMIT 1
      `,
      [email]
    );

    if (adminResult.rows.length > 0) {
      const admin = adminResult.rows[0];

      const valid = await bcrypt.compare(
        password,
        admin.password_hash
      );

      if (!valid) {
        return NextResponse.json(
          {
            success: false,
            error: "Invalid email or password.",
          },
          { status: 401 }
        );
      }

      const role = admin.is_master
        ? "ADMIN"
        : "ACADEMY_ADMIN";

      const response = NextResponse.json({
        success: true,
        role,
        user: {
          id: admin.id,
          name: admin.name,
          email: admin.email,
          academyId: admin.academy_id,
        },
      });

      response.cookies.set(
        "master_session",
        JSON.stringify({
          id: admin.id,
          role,
          academyId: admin.academy_id || null,
        }),
        {
          httpOnly: true,
          secure: process.env.NODE_ENV === "production",
          sameSite: "lax",
          path: "/",
          maxAge: 60 * 60 * 24 * 7,
        }
      );

      return response;
    }

    // ==========================================
    // TEACHER
    // ==========================================

    const teacherResult = await pool.query(
      `
      SELECT
        id,
        name,
        email,
        password_hash,
        academy_id
      FROM teachers
      WHERE LOWER(email) = $1
      LIMIT 1
      `,
      [email]
    );

    if (teacherResult.rows.length > 0) {
      const teacher = teacherResult.rows[0];

      const valid = await bcrypt.compare(
        password,
        teacher.password_hash
      );

      if (!valid) {
        return NextResponse.json(
          {
            success: false,
            error: "Invalid email or password.",
          },
          { status: 401 }
        );
      }

      const response = NextResponse.json({
        success: true,
        role: "TEACHER",
        user: {
          id: teacher.id,
          name: teacher.name,
          email: teacher.email,
          academyId: teacher.academy_id,
        },
      });

      response.cookies.set(
        "master_session",
        JSON.stringify({
          id: teacher.id,
          role: "TEACHER",
          academyId: teacher.academy_id || null,
        }),
        {
          httpOnly: true,
          secure: process.env.NODE_ENV === "production",
          sameSite: "lax",
          path: "/",
          maxAge: 60 * 60 * 24 * 7,
        }
      );

      return response;
    }

    return NextResponse.json(
      {
        success: false,
        error: "Invalid email or password.",
      },
      { status: 401 }
    );
  } catch (error) {
    console.error("MASTER LOGIN ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Login failed.",
      },
      { status: 500 }
    );
  }
}