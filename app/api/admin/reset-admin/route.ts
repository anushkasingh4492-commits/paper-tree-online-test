import { NextResponse } from "next/server";
import bcrypt from "bcryptjs";
import crypto from "crypto";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function GET() {
  try {
    const email = "admin@example.com";
    const password = "Admin@123";
    const hash = await bcrypt.hash(password, 12);

    const existing = await pool.query(
      `SELECT id FROM admins
       WHERE LOWER(email) = LOWER($1)
       LIMIT 1`,
      [email]
    );

    if (existing.rows.length > 0) {
      await pool.query(
        `UPDATE admins
         SET password_hash = $1,
             is_master = TRUE
         WHERE id = $2`,
        [hash, existing.rows[0].id]
      );
    } else {
      await pool.query(
        `INSERT INTO admins
         (id, name, email, password_hash, is_master)
         VALUES ($1, $2, $3, $4, TRUE)`,
        [
          crypto.randomUUID(),
          "Admin",
          email,
          hash,
        ]
      );
    }

    return NextResponse.json({
      success: true,
      email,
      password,
      message: "Admin account created/reset successfully.",
    });
  } catch (error) {
    console.error("RESET ADMIN ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to reset admin.",
      },
      { status: 500 }
    );
  }
}
