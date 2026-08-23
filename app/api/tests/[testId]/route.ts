import { NextResponse } from "next/server";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function GET(
  request: Request,
  { params }: { params: Promise<{ testId: string }> }
) {
  try {
    if (!process.env.DATABASE_URL) {
      return NextResponse.json(
        {
          success: false,
          error: "DATABASE_URL is not configured",
        },
        { status: 500 }
      );
    }

    const { testId } = await params;

    const result = await pool.query(
      `
      SELECT
        id,
        exam,
        question_count,
        questions,
        created_at
      FROM tests
      WHERE id = $1
      LIMIT 1
      `,
      [testId]
    );

    const rows = result.rows;

    if (rows.length === 0) {
      return NextResponse.json(
        {
          success: false,
          error: "Test not found",
        },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      test: rows[0],
    });
  } catch (error: unknown) {
    console.error("GET TEST ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to load test",
      },
      { status: 500 }
    );
  }
}
