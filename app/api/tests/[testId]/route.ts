import { NextResponse } from "next/server";
import { pool } from "@/lib/db";
import { cookies } from "next/headers";

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
    const cookieStore = await cookies();
    const sessionCookie =
      cookieStore.get("master_session")?.value;

    if (!sessionCookie) {
      return NextResponse.json(
        {
          success: false,
          error: "Unauthorized",
        },
        { status: 401 }
      );
    }

    let session: { academyId?: string };

    try {
      session = JSON.parse(sessionCookie);
    } catch {
      return NextResponse.json(
        {
          success: false,
          error: "Unauthorized",
        },
        { status: 401 }
      );
    }

    if (!session.academyId) {
      return NextResponse.json(
        {
          success: false,
          error: "Academy not found.",
        },
        { status: 403 }
      );
    }

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
        AND academy_id = $2
      LIMIT 1
      `,
      [testId, session.academyId]
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