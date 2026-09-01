import { NextResponse } from "next/server";
import bcrypt from "bcryptjs";
import crypto from "crypto";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function GET() {
  try {
    const email = "teacher@example.com";
    const password = "Teacher@123";
    const hash = await bcrypt.hash(password, 12);

    const existing = await pool.query(
      `SELECT id FROM teachers WHERE LOWER(email) = LOWER($1) LIMIT 1`,
      [email]
    );

    if (existing.rows.length > 0) {
      await pool.query(
        `UPDATE teachers
         SET password_hash = $1
         WHERE id = $2`,
        [hash, existing.rows[0].id]
      );
    } else {
      await pool.query(
        `INSERT INTO teachers
         (id, name, email, password_hash)
         VALUES ($1, $2, $3, $4)`,
        [
          crypto.randomUUID(),
          "Teacher",
          email,
          hash,
        ]
      );
    }

    return NextResponse.json({
      success: true,
      email,
      password,
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
