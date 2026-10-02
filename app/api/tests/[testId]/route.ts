import { NextResponse } from "next/server";
import { pool } from "@/lib/db";
import { cookies } from "next/headers";
import { parseSessionCookie } from "@/lib/session";

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
    /*
     * Tests are opened by students, whose login is stored in
     * student_session. Staff use master_session. The old implementation
     * checked only the staff cookie, so every correctly logged-in student
     * received a 401 before the test could load.
     */
    const sessionCookie =
      cookieStore.get("student_session")?.value ??
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

    let session: { academyId?: string; studentId?: string; id?: string };

    try {
      session = parseSessionCookie<{ academyId?: string; studentId?: string; id?: string }>(sessionCookie) || {};
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

    if (!session.studentId && !session.id) {
      return NextResponse.json(
        {
          success: false,
          error: "Invalid login session.",
        },
        { status: 401 }
      );
    }

    await pool.query(`
      ALTER TABLE tests
      ADD COLUMN IF NOT EXISTS academy_id UUID
    `);

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
        AND (
          academy_id = $2
          OR (
            $3::text IS NOT NULL
            AND EXISTS (
              SELECT 1
              FROM student_tests st
              WHERE st.test_id = tests.id
                AND st.student_id::text = $3::text
            )
          )
        )
      LIMIT 1
      `,
      [testId, session.academyId, session.studentId ?? null]
    );

    const rows = result.rows.map((row) => {
      let rawQuestions: unknown = row.questions;

      if (typeof rawQuestions === "string") {
        try {
          rawQuestions = JSON.parse(rawQuestions);
        } catch {
          rawQuestions = [];
        }
      }

      const safeQuestions = Array.isArray(rawQuestions)
        ? rawQuestions.map((question: Record<string, unknown>) => {
            const {
              correct_option: _correctOption,
              correct_answer_text: _correctAnswerText,
              solution: _solution,
              answer: _answer,
              ...safeQuestion
            } = question;
            return safeQuestion;
          })
        : [];

      return {
        id: row.id,
        exam: row.exam,
        question_count: row.question_count,
        created_at: row.created_at,
        questions: safeQuestions,
      };
    });

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
