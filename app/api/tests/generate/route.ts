import { cookies } from "next/headers";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

type GenerateRequest = {
  exam?: string;
  course?: string;
  subject?: string;
  subjects?: string[];
  chapters?: string[];
  difficulty?: string;
  questionCount?: number;
  duration?: number;
};

type QuestionRow = {
  id: string;
  exam: string;
  subject: string;
  standard?: string | null;
  chapter_number?: string | number | null;
  chapter_name?: string | null;
  major_topic?: string | null;
  subtopic?: string | null;
  concept_tested?: string | null;
  stem?: string | null;
  options?: unknown;
  correct_option?: string | number | null;
  correct_answer_text?: string | null;
  solution?: string | null;
  formula_principle?: string | null;
  difficulty?: string | null;
  estimated_time?: number | null;
  question_type?: string | null;
  figure_asset?: string | null;
};

function clean(value: unknown): string {
  return String(value ?? "").trim();
}

function normalize(value: unknown): string {
  return clean(value)
    .toLowerCase()
    .replace(/[_-]+/g, " ")
    .replace(/\s+/g, " ");
}

export async function POST(request: Request) {
  try {
    /*
     * ---------------------------------------------------------
     * DATABASE
     * ---------------------------------------------------------
     */

    if (!process.env.DATABASE_URL) {
      return Response.json(
        {
          success: false,
          error: "DATABASE_URL is not configured",
        },
        { status: 500 }
      );
    }

    /*
     * ---------------------------------------------------------
     * STUDENT SESSION
     * ---------------------------------------------------------
     */

    const cookieStore = await cookies();

    const studentId =
      cookieStore.get("student_session")?.value;

    if (!studentId) {
      return Response.json(
        {
          success: false,
          error: "Student is not logged in.",
        },
        { status: 401 }
      );
    }

    /*
     * ---------------------------------------------------------
     * REQUEST
     * ---------------------------------------------------------
     */

    const body =
      (await request.json()) as GenerateRequest;

    const exam =
      clean(body.exam) ||
      clean(body.course) ||
      "MHT-CET";

    const subjects =
      Array.isArray(body.subjects)
        ? body.subjects
            .map(clean)
            .filter(Boolean)
        : body.subject
          ? [clean(body.subject)]
          : [];

    const chapters =
      Array.isArray(body.chapters)
        ? body.chapters
            .map(clean)
            .filter(Boolean)
        : [];

    const difficulty =
      clean(body.difficulty) || "Mixed";

    const questionCount = Math.max(
      1,
      Math.min(
        Number(body.questionCount) || 10,
        200
      )
    );

    const duration =
      Number(body.duration) || 60;

    console.log(
      "================================="
    );

    console.log(
      "GENERATE TEST REQUEST"
    );

    console.log(
      "Exam:",
      exam
    );

    console.log(
      "Subjects:",
      subjects
    );

    console.log(
      "Chapters:",
      chapters
    );

    console.log(
      "Difficulty:",
      difficulty
    );

    console.log(
      "Question Count:",
      questionCount
    );

    console.log(
      "================================="
    );

    /*
     * ---------------------------------------------------------
     * BUILD STRICT FILTER
     * ---------------------------------------------------------
     */

    const conditions: string[] = [
      `LOWER(TRIM(exam)) = LOWER(TRIM($1))`,
    ];

    const values: unknown[] = [
      exam,
    ];

    /*
     * SUBJECT FILTER
     */

    if (subjects.length > 0) {
      values.push(
        subjects.map(normalize)
      );

      conditions.push(`
        LOWER(
          REGEXP_REPLACE(
            TRIM(subject),
            '[_-]+',
            ' ',
            'g'
          )
        )
        = ANY(
          $${values.length}::text[]
        )
      `);
    }

    /*
     * CHAPTER FILTER
     *
     * IMPORTANT:
     * If a chapter is selected, we DO NOT ignore it.
     */

    if (chapters.length > 0) {
      values.push(
        chapters.map(normalize)
      );

      conditions.push(`
        LOWER(
          REGEXP_REPLACE(
            TRIM(chapter_name),
            '[_-]+',
            ' ',
            'g'
          )
        )
        = ANY(
          $${values.length}::text[]
        )
      `);
    }

    /*
     * DIFFICULTY FILTER
     *
     * Mixed means all difficulties.
     */

    if (
      difficulty &&
      normalize(difficulty) !== "mixed"
    ) {
      values.push(
        normalize(difficulty)
      );

      conditions.push(`
        LOWER(TRIM(difficulty))
        = $${values.length}
      `);
    }

    /*
     * ---------------------------------------------------------
     * CHECK HOW MANY MATCH
     * ---------------------------------------------------------
     */

    const countQuery = `
      SELECT COUNT(*)::int AS count
      FROM questions
      WHERE ${conditions.join(" AND ")}
    `;

    const countResult =
      await pool.query(
        countQuery,
        values
      );

    const available =
      Number(
        countResult.rows[0]?.count || 0
      );

    console.log(
      "Matching questions:",
      available
    );

    /*
     * ---------------------------------------------------------
     * NO QUESTIONS
     * ---------------------------------------------------------
     */

    if (available === 0) {
      return Response.json(
        {
          success: false,
          error:
            "No questions are available for the selected criteria.",
          details: {
            exam,
            subjects,
            chapters,
            difficulty,
            availableQuestions: 0,
          },
        },
        { status: 404 }
      );
    }

    /*
     * ---------------------------------------------------------
     * NOT ENOUGH QUESTIONS
     * ---------------------------------------------------------
     */

    if (available < questionCount) {
      return Response.json(
        {
          success: false,
          error:
            `Only ${available} question${available === 1 ? "" : "s"} available for the selected criteria. You requested ${questionCount}.`,
          details: {
            exam,
            subjects,
            chapters,
            difficulty,
            availableQuestions: available,
            requestedQuestions: questionCount,
          },
        },
        { status: 400 }
      );
    }

    /*
     * ---------------------------------------------------------
     * GET RANDOM QUESTIONS
     * ---------------------------------------------------------
     */

    const questionValues = [
      ...values,
      questionCount,
    ];

    const questionQuery = `
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
      ORDER BY RANDOM()
      LIMIT $${questionValues.length}
    `;

    const questionsResult =
      await pool.query(
        questionQuery,
        questionValues
      );

    const questions =
      questionsResult.rows as QuestionRow[];

    /*
     * ---------------------------------------------------------
     * SAFETY CHECK
     * ---------------------------------------------------------
     */

    if (questions.length < questionCount) {
      return Response.json(
        {
          success: false,
          error:
            "Unable to collect enough questions for this test.",
          details: {
            requested: questionCount,
            found: questions.length,
          },
        },
        { status: 500 }
      );
    }

    console.log(
      "Questions selected:",
      questions.length
    );

    /*
     * ---------------------------------------------------------
     * CREATE TEST
     * ---------------------------------------------------------
     */

    const testId =
      `test-${Date.now()}`;

    /*
     * ---------------------------------------------------------
     * SAVE TEST
     * ---------------------------------------------------------
     */

    const client =
      await pool.connect();

    try {
      await client.query(
        "BEGIN"
      );

      await client.query(
        `
          INSERT INTO tests (
            id,
            exam,
            question_count,
            questions
          )
          VALUES (
            $1,
            $2,
            $3,
            $4::jsonb
          )
        `,
        [
          testId,
          exam,
          questions.length,
          JSON.stringify(
            questions
          ),
        ]
      );

      await client.query(
        `
          INSERT INTO student_tests (
            id,
            student_id,
            test_id
          )
          VALUES (
            $1,
            $2,
            $3
          )
          ON CONFLICT (
            student_id,
            test_id
          )
          DO NOTHING
        `,
        [
          `student-test-${Date.now()}`,
          studentId,
          testId,
        ]
      );

      await client.query(
        "COMMIT"
      );
    } catch (error) {
      await client.query(
        "ROLLBACK"
      );

      throw error;
    } finally {
      client.release();
    }

    /*
     * ---------------------------------------------------------
     * SUCCESS
     * ---------------------------------------------------------
     */

    console.log(
      "================================="
    );

    console.log(
      "TEST GENERATED SUCCESSFULLY"
    );

    console.log(
      "Test ID:",
      testId
    );

    console.log(
      "Questions:",
      questions.length
    );

    console.log(
      "================================="
    );

    return Response.json({
      success: true,

      testId,

      exam,

      questionCount:
        questions.length,

      configuration: {
        testId,

        course:
          body.course ||
          exam,

        subject:
          body.subject ||
          subjects[0] ||
          "",

        subjects,

        chapters,

        difficulty,

        questionCount:
          questions.length,

        duration,

        createdAt:
          new Date().toISOString(),
      },

      questions,
    });
  } catch (error: unknown) {
    console.error(
      "TEST GENERATION ERROR:",
      error
    );

    return Response.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to generate test",
      },
      { status: 500 }
    );
  }
}