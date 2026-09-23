import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import bcrypt from "bcryptjs";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";

export async function POST(request: Request) {
  try {
    const body = await request.json();

    const currentPassword = String(body.currentPassword || "");
    const newPassword = String(body.newPassword || "");
    const confirmPassword = String(body.confirmPassword || "");

    if (!currentPassword || !newPassword || !confirmPassword) {
      return NextResponse.json(
        {
          success: false,
          error: "All password fields are required.",
        },
        { status: 400 }
      );
    }

    if (newPassword !== confirmPassword) {
      return NextResponse.json(
        {
          success: false,
          error: "New passwords do not match.",
        },
        { status: 400 }
      );
    }

    if (newPassword.length < 8) {
      return NextResponse.json(
        {
          success: false,
          error: "New password must be at least 8 characters long.",
        },
        { status: 400 }
      );
    }

    const cookieStore = await cookies();

    /* =========================================================
       TEACHER
    ========================================================= */

    const teacherCookie =
      cookieStore.get("master_session")?.value;

    if (teacherCookie) {
      const session = parseSessionCookie<{
        id?: string;
        role?: string;
      }>(teacherCookie);

      if (
        session?.role === "TEACHER" &&
        session.id
      ) {
        const result = await pool.query(
          `
          SELECT id, password_hash
          FROM teachers
          WHERE id = $1
          LIMIT 1
          `,
          [session.id]
        );

        if (!result.rows.length) {
          return NextResponse.json(
            {
              success: false,
              error: "Teacher account was not found.",
            },
            { status: 404 }
          );
        }

        const valid = await bcrypt.compare(
          currentPassword,
          result.rows[0].password_hash
        );

        if (!valid) {
          return NextResponse.json(
            {
              success: false,
              error: "Current password is incorrect.",
            },
            { status: 401 }
          );
        }

        const passwordHash = await bcrypt.hash(
          newPassword,
          12
        );

        await pool.query(
          `
          UPDATE teachers
          SET password_hash = $1
          WHERE id = $2
          `,
          [passwordHash, session.id]
        );

        return NextResponse.json({
          success: true,
          message: "Password changed successfully.",
        });
      }
    }

    /* =========================================================
       STUDENT
    ========================================================= */

    const studentCookie =
      cookieStore.get("student_session")?.value;

    if (studentCookie) {
      const session = parseSessionCookie<{
        studentId?: string;
      }>(studentCookie);

      if (session?.studentId) {
        const result = await pool.query(
          `
          SELECT
            s.id,
            c.password_hash
          FROM students s
          INNER JOIN student_credentials c
            ON c.student_id = s.id
          WHERE s.id = $1
          LIMIT 1
          `,
          [session.studentId]
        );

        if (!result.rows.length) {
          return NextResponse.json(
            {
              success: false,
              error: "Student account was not found.",
            },
            { status: 404 }
          );
        }

        const valid = await bcrypt.compare(
          currentPassword,
          result.rows[0].password_hash
        );

        if (!valid) {
          return NextResponse.json(
            {
              success: false,
              error: "Current password is incorrect.",
            },
            { status: 401 }
          );
        }

        const passwordHash = await bcrypt.hash(
          newPassword,
          12
        );

        await pool.query(
          `
          UPDATE student_credentials
          SET password_hash = $1
          WHERE student_id = $2
          `,
          [passwordHash, session.studentId]
        );

        return NextResponse.json({
          success: true,
          message: "Password changed successfully.",
        });
      }
    }

    return NextResponse.json(
      {
        success: false,
        error: "You are not logged in.",
      },
      { status: 401 }
    );
  } catch (error) {
    console.error("CHANGE PASSWORD ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to change password.",
      },
      { status: 500 }
    );
  }
}