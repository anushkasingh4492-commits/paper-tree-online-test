
import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";

export async function GET(request: Request) {
  try {
    const cookieStore = await cookies();
    const sessionCookie = cookieStore.get("master_session")?.value;

    if (!sessionCookie) {
      return NextResponse.json(
        { success: false, error: "Teacher is not logged in." },
        { status: 401 }
      );
    }

    const session = parseSessionCookie<Record<string, unknown>>(sessionCookie);

    if (!session) {
      return NextResponse.json(
        { success: false, error: "Invalid teacher session." },
        { status: 401 }
      );
    }

    if (session.role !== "TEACHER" || !session.id) {
      return NextResponse.json(
        { success: false, error: "Teacher access required." },
        { status: 403 }
      );
    }

    const { searchParams } = new URL(request.url);
    const exam = searchParams.get("exam") || "MHT-CET";
    const subject = searchParams.get("subject") || "";
    const chapter = searchParams.get("chapter") || "";
    const difficulty = searchParams.get("difficulty") || "";
    const search = searchParams.get("search") || "";

    const limit = Math.min(
      200,
      Math.max(1, Number.parseInt(searchParams.get("limit") || "50", 10) || 50)
    );
    const offset = Math.max(
      0,
      Number.parseInt(searchParams.get("offset") || "0", 10) || 0
    );

    const values: unknown[] = [exam];
    const conditions = ["LOWER(TRIM(exam)) = LOWER(TRIM($1))"];

    if (subject) {
      values.push(subject);
      conditions.push(`LOWER(TRIM(subject)) = LOWER(TRIM($${values.length}))`);
    }

    if (chapter) {
      values.push(chapter);
      conditions.push(`chapter_name = $${values.length}`);
    }

    if (difficulty) {
      values.push(difficulty);
      conditions.push(`LOWER(TRIM(difficulty)) = LOWER(TRIM($${values.length}))`);
    }

    if (search) {
      values.push(`%${search}%`);
      conditions.push(`stem ILIKE $${values.length}`);
    }

    const whereClause = conditions.join(" AND ");

    const countResult = await pool.query(
      `SELECT COUNT(*)::int AS total FROM questions WHERE ${whereClause}`,
      values
    );

    const total = Number(countResult.rows[0]?.total || 0);

    const pageValues = [...values, limit, offset];
    const limitParam = pageValues.length - 1;
    const offsetParam = pageValues.length;

    const result = await pool.query(
      `
      SELECT
        id, exam, subject, standard, chapter_number, chapter_name,
        major_topic, subtopic, concept_tested, stem, options,
        correct_option, correct_answer_text, solution, formula_principle,
        difficulty, estimated_time, question_type, figure_asset
      FROM questions
      WHERE ${whereClause}
      ORDER BY created_at DESC NULLS LAST, id
      LIMIT $${limitParam}
      OFFSET $${offsetParam}
      `,
      pageValues
    );

    return NextResponse.json({
      success: true,
      questions: result.rows,
      total,
      limit,
      offset,
      hasMore: offset + result.rows.length < total,
    });
  } catch (error) {
    console.error("TEACHER QUESTIONS ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error: error instanceof Error ? error.message : "Failed to load questions.",
      },
      { status: 500 }
    );
  }
}
