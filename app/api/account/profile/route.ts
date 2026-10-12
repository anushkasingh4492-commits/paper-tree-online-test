import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function PATCH(request: Request) {
  try {
    const raw = (await cookies()).get("student_session")?.value;
    const session = raw
      ? parseSessionCookie<{ studentId?: string; academyId?: string }>(raw)
      : null;

    const studentId = String(session?.studentId ?? "").trim();
    const academyId = String(session?.academyId ?? "").trim();

    if (!studentId || !academyId) {
      return NextResponse.json(
        { success: false, error: "Please log in as a student again." },
        { status: 401 }
      );
    }

    const body = await request.json();
    const name = typeof body.name === "string" ? body.name.trim() : "";

    if (name.length < 2 || name.length > 100) {
      return NextResponse.json(
        { success: false, error: "Name must be between 2 and 100 characters." },
        { status: 400 }
      );
    }

    const result = await pool.query(
      `UPDATE students
       SET name = $1
       WHERE id::text = $2::text
         AND academy_id::text = $3::text
       RETURNING id, name, roll_number, email`,
      [name, studentId, academyId]
    );

    if (!result.rows.length) {
      return NextResponse.json(
        { success: false, error: "Student account was not found." },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      student: {
        id: String(result.rows[0].id),
        name: String(result.rows[0].name),
        rollNumber: result.rows[0].roll_number ?? null,
        email: result.rows[0].email ?? null,
      },
    });
  } catch (error) {
    console.error("STUDENT PROFILE UPDATE ERROR:", error);
    return NextResponse.json(
      { success: false, error: "Could not update your profile." },
      { status: 500 }
    );
  }
}
