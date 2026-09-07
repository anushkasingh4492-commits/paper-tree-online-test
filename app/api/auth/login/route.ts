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
        {
          success: false,
          error: "Email and password are required.",
        },
        { status: 400 }
      );
    }

    /*
     * ==========================================
     * 1. MASTER ADMIN / ACADEMY ADMIN
     * ==========================================
     */

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

      // Remove any old student session.
      response.cookies.delete("student_session");

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

    /*
     * ==========================================
     * 2. TEACHER
     * ==========================================
     */

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

      // Remove any old student session.
      response.cookies.delete("student_session");

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

    /*
     * ==========================================
     * 3. STUDENT
     * ==========================================
     */

    const studentResult = await pool.query(
      `
      SELECT
        s.id,
        s.name,
        s.email,
        s.roll_number,
        s.class_name,
        s.exam,
        s.academy_id,
        a.status AS academy_status,
        a.subscription_end,
        c.password_hash
      FROM students s
      INNER JOIN student_credentials c
        ON c.student_id = s.id
      LEFT JOIN academies a
        ON a.id = s.academy_id
      WHERE LOWER(s.email) = $1
      LIMIT 1
      `,
      [email]
    );

    if (studentResult.rows.length > 0) {
      const student = studentResult.rows[0];

      if (student.academy_status && student.academy_status !== "ACTIVE") {
        return NextResponse.json({ success: false, error: "Student access has been restricted by the academy." }, { status: 403 });
      }
      if (student.subscription_end && new Date(student.subscription_end) < new Date()) {
        return NextResponse.json({ success: false, error: "The academy subscription has expired." }, { status: 403 });
      }

      const valid = await bcrypt.compare(
        password,
        student.password_hash
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
        role: "STUDENT",
        user: {
          id: student.id,
          name: student.name,
          email: student.email,
          roll_number: student.roll_number,
          class_name: student.class_name,
          exam: student.exam,
          academyId: student.academy_id,
        },
      });

      // Remove any old staff/admin session.
      response.cookies.delete("master_session");

      response.cookies.set(
        "student_session",
        JSON.stringify({
          studentId: student.id,
          name: student.name,
          email: student.email,
          academyId: student.academy_id,
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
        error: "No account was found for this email. Check the email or run the master account setup.",
      },
      { status: 401 }
    );
  } catch (error) {
    console.error("UNIVERSAL LOGIN ERROR:", error);

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