import { NextResponse } from "next/server";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function GET() {
  try {
    const result = await pool.query(`
      SELECT
        id,
        code,
        exam,
        description,
        duration_minutes,
        created_by,
        created_at,
        updated_at,
        status,
        custom_section
      FROM papers
      ORDER BY created_at DESC
    `);

    return NextResponse.json({
      success: true,
      papers: result.rows,
    });
  } catch (error) {
    console.error("TEACHER PAPERS ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to load papers.",
      },
      { status: 500 }
    );
  }
}
