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

    const admin = await pool.query(
      `SELECT id, name, email, password_hash
       FROM admins
       WHERE LOWER(email) = $1
       LIMIT 1`,
      [email]
    );

    if (admin.rows.length > 0) {
      const valid = await bcrypt.compare(
        password,
        admin.rows[0].password_hash
      );

      if (!valid) {
        return NextResponse.json(
          { success: false, error: "Invalid email or password." },
          { status: 401 }
        );
      }

      const response = NextResponse.json({
        success: true,
        role: "ADMIN",
      user: {
  id: admin.rows[0].id,
  name: admin.rows[0].name,
  email: admin.rows[0].email,
},
      });

      response.cookies.set(
        "master_session",
        JSON.stringify({
          id: admin.rows[0].id,
          role: "ADMIN",
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

    const teacher = await pool.query(
      `SELECT id, name, email, password_hash
       FROM teachers
       WHERE LOWER(email) = $1
       LIMIT 1`,
      [email]
    );

    if (teacher.rows.length > 0) {
      const valid = await bcrypt.compare(
        password,
        teacher.rows[0].password_hash
      );

      if (!valid) {
        return NextResponse.json(
          { success: false, error: "Invalid email or password." },
          { status: 401 }
        );
      }

      const response = NextResponse.json({
        success: true,
        role: "TEACHER",
        user: {
  id: teacher.rows[0].id,
  name: teacher.rows[0].name,
  email: teacher.rows[0].email,
},
      });

      response.cookies.set(
        "master_session",
        JSON.stringify({
          id: teacher.rows[0].id,
          role: "TEACHER",
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
      { success: false, error: "Invalid email or password." },
      { status: 401 }
    );
  } catch (error) {
    console.error("MASTER LOGIN ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error: error instanceof Error ? error.message : "Login failed.",
      },
      { status: 500 }
    );
  }
}
