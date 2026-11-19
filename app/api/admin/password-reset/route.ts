import { NextResponse } from "next/server";
import bcrypt from "bcryptjs";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";

type Session = {
  id?: string;
  role?: string;
  academyId?: string | null;
};

function getSession(request: Request): Session | null {
  const cookieHeader = request.headers.get("cookie") || "";
  const match = cookieHeader.match(/(?:^|;\s*)master_session=([^;]+)/);
  if (!match) return null;
  return parseSessionCookie<Session>(decodeURIComponent(match[1]));
}

export async function GET(request: Request) {
  try {
    const session = getSession(request);

    // Only Master Admin can access password management.
    if (!session?.id || session.role !== "ADMIN") {
      return NextResponse.json(
        {
          success: false,
          error: "Master Admin access required.",
        },
        { status: 403 }
      );
    }

    const adminResult = await pool.query(
      `
      SELECT id, is_master
      FROM admins
      WHERE id = $1
      LIMIT 1
      `,
      [session.id]
    );

    if (
      !adminResult.rows.length ||
      !adminResult.rows[0].is_master
    ) {
      return NextResponse.json(
        {
          success: false,
          error: "Master Admin access required.",
        },
        { status: 403 }
      );
    }
const teachersResult = await pool.query(
  `
  SELECT
    t.id,
    t.name,
    t.email,
    a.name AS academy_name
  FROM teachers t
  LEFT JOIN academies a
    ON a.id = t.academy_id
  ORDER BY t.name ASC
  `
);

const studentsResult = await pool.query(
  `
  SELECT
    s.id,
    s.name,
    s.email,
    a.name AS academy_name
  FROM students s
  LEFT JOIN academies a
    ON a.id = s.academy_id
  ORDER BY s.name ASC
  `
);

    return NextResponse.json({
      success: true,
      masterId: session.id,
      teachers: teachersResult.rows,
      students: studentsResult.rows,
    });
  } catch (error) {
    console.error(
      "ADMIN PASSWORD RESET GET ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to load accounts.",
      },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const session = getSession(request);

    // Only Master Admin can reset passwords.
    if (!session?.id || session.role !== "ADMIN") {
      return NextResponse.json(
        {
          success: false,
          error: "Master Admin access required.",
        },
        { status: 403 }
      );
    }

    const adminResult = await pool.query(
      `
      SELECT id, is_master
      FROM admins
      WHERE id = $1
      LIMIT 1
      `,
      [session.id]
    );

    if (
      !adminResult.rows.length ||
      !adminResult.rows[0].is_master
    ) {
      return NextResponse.json(
        {
          success: false,
          error: "Master Admin access required.",
        },
        { status: 403 }
      );
    }

    const body = await request.json();

    const userType = String(
      body.userType || ""
    )
      .trim()
      .toUpperCase();

    const userId = String(
      body.userId || ""
    ).trim();

    const newPassword = String(
      body.newPassword || ""
    );

    if (!["STUDENT", "TEACHER", "MASTER"].includes(userType)) {
      return NextResponse.json(
        {
          success: false,
          error: "Invalid account type.",
        },
        { status: 400 }
      );
    }

    if (userType !== "MASTER" && !userId) {
      return NextResponse.json(
        {
          success: false,
          error: "Account ID is required.",
        },
        { status: 400 }
      );
    }

    if (newPassword.length < 6) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Password must be at least 6 characters long.",
        },
        { status: 400 }
      );
    }

    const passwordHash = await bcrypt.hash(
      newPassword,
      12
    );

    if (userType === "MASTER") {
      if (userId !== session.id) {
        return NextResponse.json(
          { success: false, error: "Only the signed-in master admin can change this password." },
          { status: 403 }
        );
      }
      await pool.query(
        `UPDATE admins SET password_hash = $1
         WHERE id = $2 AND is_master = TRUE`,
        [passwordHash, session.id]
      );
      return NextResponse.json({
        success: true,
        message: "Master Admin password changed successfully.",
      });
    }

    /*
     * ==========================================
     * TEACHER
     * ==========================================
     */
    if (userType === "TEACHER") {
      const teacherResult = await pool.query(
        `
        SELECT id
        FROM teachers
        WHERE id = $1
        LIMIT 1
        `,
        [userId]
      );

      if (!teacherResult.rows.length) {
        return NextResponse.json(
          {
            success: false,
            error: "Teacher account not found.",
          },
          { status: 404 }
        );
      }

      await pool.query(
        `
        UPDATE teachers
        SET password_hash = $1
        WHERE id = $2
        `,
        [passwordHash, userId]
      );

      return NextResponse.json({
        success: true,
        message:
          "Teacher password reset successfully.",
      });
    }

    /*
     * ==========================================
     * STUDENT
     * ==========================================
     */

    const studentResult = await pool.query(
      `
      SELECT id
      FROM students
      WHERE id = $1
      LIMIT 1
      `,
      [userId]
    );

    if (!studentResult.rows.length) {
      return NextResponse.json(
        {
          success: false,
          error: "Student account not found.",
        },
        { status: 404 }
      );
    }

    const credentialResult = await pool.query(
      `
      SELECT student_id
      FROM student_credentials
      WHERE student_id = $1
      LIMIT 1
      `,
      [userId]
    );

    if (credentialResult.rows.length) {
      await pool.query(
        `
        UPDATE student_credentials
        SET password_hash = $1
        WHERE student_id = $2
        `,
        [passwordHash, userId]
      );
    } else {
      await pool.query(
        `
        INSERT INTO student_credentials
        (student_id, password_hash)
        VALUES ($1, $2)
        `,
        [userId, passwordHash]
      );
    }

    return NextResponse.json({
      success: true,
      message:
        "Student password reset successfully.",
    });
  } catch (error) {
    console.error(
      "ADMIN PASSWORD RESET POST ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to reset password.",
      },
      { status: 500 }
    );
  }
}