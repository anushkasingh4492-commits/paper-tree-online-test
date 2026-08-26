import { NextResponse } from "next/server";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function GET() {
  try {
    const result = await pool.query(`
      SELECT
        exam,
        subject,
        chapter_name,
        difficulty,
        COUNT(*)::int AS total
      FROM questions
      GROUP BY
        exam,
        subject,
        chapter_name,
        difficulty
      ORDER BY
        exam,
        subject,
        chapter_name,
        difficulty;
    `);

    return NextResponse.json({
      success: true,
      totalRows: result.rows.length,
      data: result.rows,
    });
  } catch (error) {
    console.error(
      "DB INSPECTION ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : String(error),
      },
      { status: 500 }
    );
  }
}