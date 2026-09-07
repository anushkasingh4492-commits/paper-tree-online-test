import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function GET(request: Request) {
  try {
    const cookieStore = await cookies();
    const sessionCookie =
      cookieStore.get("master_session")?.value;

    if (!sessionCookie) {
      return NextResponse.json(
        { success: false, error: "Teacher is not logged in." },
        { status: 401 }
      );
    }

let session: {
  role?: string;
  id?: string;
  academyId?: string;
};

    try {
      session = JSON.parse(sessionCookie);
    } catch {
      return NextResponse.json(
        { success: false, error: "Invalid teacher session." },
        { status: 401 }
      );
    }

if (
  session.role !== "TEACHER" ||
  !session.academyId
) {
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

    const values: string[] = [];
    const conditions: string[] = [];

    values.push(exam);
 values.push(session.academyId);
conditions.push(`academy_id = $${values.length}`);
    conditions.push(`exam = $${values.length}`);

    if (subject) {
      values.push(subject);
      conditions.push(`subject = $${values.length}`);
    }

    if (chapter) {
      values.push(chapter);
      conditions.push(`chapter_name = $${values.length}`);
    }

    if (difficulty) {
      values.push(difficulty);
      conditions.push(`difficulty = $${values.length}`);
    }

    if (search) {
      values.push(`%${search}%`);
      conditions.push(`stem ILIKE $${values.length}`);
    }

    const result = await pool.query(
      `
      SELECT
        id,
        exam,
        subject,
        standard,
        chapter_number,
        chapter_name,
        major_topic,
        subtopic,
        concept_tested,
        stem,
        options,
        correct_option,
        correct_answer_text,
        solution,
        formula_principle,
        difficulty,
        estimated_time,
        question_type,
        figure_asset
      FROM questions
      WHERE ${conditions.join(" AND ")}
      ORDER BY created_at DESC
      LIMIT 200
      let session: {
  role?: string;
  academyId?: string;
};
      `,
      values
    );

    return NextResponse.json({
      success: true,
      questions: result.rows,
    });
  } catch (error) {
    console.error("TEACHER QUESTIONS ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to load questions.",
      },
      { status: 500 }
    );
  }
}
