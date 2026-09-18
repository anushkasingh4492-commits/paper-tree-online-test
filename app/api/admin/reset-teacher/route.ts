import { NextResponse } from "next/server";
import bcrypt from "bcryptjs";
import crypto from "crypto";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function GET(request: Request) {
  try {
    const email = "teacher@example.com";
    const password = "Teacher@123";
    const hash = await bcrypt.hash(password, 12);
    const academyId = new URL(request.url).searchParams.get("academyId")?.trim();

    if (academyId) {
      const academy = await pool.query(
        `SELECT id FROM academies WHERE id = $1 LIMIT 1`,
        [academyId]
      );

      if (!academy.rows.length) {
        return NextResponse.json(
          { success: false, error: "The selected academy does not exist." },
          { status: 400 }
        );
      }
    }

    const existing = await pool.query(
      `SELECT id, academy_id FROM teachers WHERE LOWER(email) = LOWER($1) LIMIT 1`,
      [email]
    );

    if (existing.rows.length > 0) {
      const existingAcademyId = existing.rows[0].academy_id || academyId;

      if (!existingAcademyId) {
        return NextResponse.json(
          {
            success: false,
            error: "Provide academyId to assign this teacher to an academy.",
          },
          { status: 400 }
        );
      }

      await pool.query(
        `UPDATE teachers
         SET password_hash = $1, academy_id = $2
         WHERE id = $3`,
        [hash, existingAcademyId, existing.rows[0].id]
      );
    } else {
      if (!academyId) {
        return NextResponse.json(
          {
            success: false,
            error: "Provide academyId to create this teacher account.",
          },
          { status: 400 }
        );
      }

      await pool.query(
        `INSERT INTO teachers
         (id, name, email, password_hash, academy_id)
         VALUES ($1, $2, $3, $4, $5)`,
        [
          crypto.randomUUID(),
          "Teacher",
          email,
          hash,
          academyId,
        ]
      );
    }

    return NextResponse.json({
      success: true,
      email,
      password,
      academyId: academyId || existing.rows[0]?.academy_id,
      message: "Teacher account created/reset successfully.",
    });
  } catch (error) {
    console.error("RESET TEACHER ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to reset teacher.",
      },
      { status: 500 }
    );
  }
}
