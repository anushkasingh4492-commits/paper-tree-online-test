
import { neon } from "@neondatabase/serverless";
import fs from "fs";
import path from "path";

export const runtime = "nodejs";
export const maxDuration = 300;

const DATASETS = {
  physics: {
    subject: "Physics",
    file: "data/mht-cet/physics/question_bank_physics_with_figures_v1.3.0.json",
  },
  chemistry: {
    subject: "Chemistry",
    file: "data/mht-cet/chemistry/MHT-CET_Chemistry_question_bank_v2.0.0.json",
  },
  mathematics: {
    subject: "Mathematics",
    file: "data/mht-cet/maths/question_bank_maths_full_v2.0.1.json",
  },
  biology: {
    subject: "Biology",
    file: "data/mht-cet/biology/MHT-CET_Biology_question_bank_v2.1.0.json",
  },
} as const;

type SubjectKey = keyof typeof DATASETS;

const BATCH_SIZE = 100;

function normalizeQuestion(q: any, subject: string) {
  return {
    id: String(q.id),
    exam: "MHT-CET",
    subject,
    standard: Number(q.standard),
    chapter_number: Number(q.chapter_number),
    chapter_name: q.chapter_name ?? "",
    major_topic: q.major_topic ?? null,
    subtopic: q.subtopic ?? null,
    concept_tested: q.concept_tested ?? null,
    stem: q.stem ?? "",
    options: q.options ?? {},
    correct_option: q.correct_option ?? "",
    correct_answer_text: q.correct_answer_text ?? null,
    distractor_rationale: q.distractor_rationale ?? null,
    solution: q.solution ?? null,
    formula_principle: q.formula_principle ?? null,
    common_misconception: q.common_misconception ?? null,
    difficulty: q.difficulty ?? "Mixed",
    estimated_time: q.estimated_time ?? null,
    question_type: q.question_type ?? null,
    figure_asset: q.figure_asset ?? null,
    concept_family_id: q.concept_family_id ?? null,
    family_size:
      q.family_size == null ? null : Number(q.family_size),
    generator_eligible_strict_cet:
      q.generator_eligible_strict_cet === true,
    generator_eligible_extended_revision:
      q.generator_eligible_extended_revision === true,
    syllabus_scope_status: q.syllabus_scope_status ?? null,
    syllabus_version: q.syllabus_version ?? null,
    release_version: q.release_version ?? null,
    raw_data: q,
  };
}

function loadDataset(
  dataset: (typeof DATASETS)[SubjectKey]
) {
  const filePath = path.join(
    /* turbopackIgnore: true */
    process.cwd(),
    dataset.file
  );

  if (!fs.existsSync(filePath)) {
    throw new Error(`Dataset not found: ${filePath}`);
  }

  const data = JSON.parse(
    fs.readFileSync(filePath, "utf8")
  );

  if (!Array.isArray(data)) {
    throw new Error(
      `${dataset.file} does not contain a JSON array`
    );
  }

  return data;
}

async function insertQuestion(sql: any, q: any) {
  await sql`
    INSERT INTO questions (
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
      distractor_rationale,
      solution,
      formula_principle,
      common_misconception,
      difficulty,
      estimated_time,
      question_type,
      figure_asset,
      concept_family_id,
      family_size,
      generator_eligible_strict_cet,
      generator_eligible_extended_revision,
      syllabus_scope_status,
      syllabus_version,
      release_version,
      raw_data
    )
    VALUES (
      ${q.id},
      ${q.exam},
      ${q.subject},
      ${q.standard},
      ${q.chapter_number},
      ${q.chapter_name},
      ${q.major_topic},
      ${q.subtopic},
      ${q.concept_tested},
      ${q.stem},
      ${JSON.stringify(q.options)}::jsonb,
      ${q.correct_option},
      ${q.correct_answer_text},
      ${
        q.distractor_rationale
          ? JSON.stringify(q.distractor_rationale)
          : null
      }::jsonb,
      ${q.solution},
      ${q.formula_principle},
      ${q.common_misconception},
      ${q.difficulty},
      ${q.estimated_time},
      ${q.question_type},
      ${q.figure_asset},
      ${q.concept_family_id},
      ${q.family_size},
      ${q.generator_eligible_strict_cet},
      ${q.generator_eligible_extended_revision},
      ${q.syllabus_scope_status},
      ${q.syllabus_version},
      ${q.release_version},
      ${JSON.stringify(q.raw_data)}::jsonb
    )
    ON CONFLICT (id) DO NOTHING
  `;
}

export async function GET(request: Request) {
  try {
    const url = new URL(request.url);

    const secret = url.searchParams.get("secret");

    if (!process.env.IMPORT_SECRET) {
      return Response.json(
        {
          success: false,
          error: "IMPORT_SECRET is not configured",
        },
        { status: 500 }
      );
    }

    if (secret !== process.env.IMPORT_SECRET) {
      return Response.json(
        {
          success: false,
          error: "Unauthorized",
        },
        { status: 401 }
      );
    }

    if (!process.env.DATABASE_URL) {
      return Response.json(
        {
          success: false,
          error: "DATABASE_URL is not configured",
        },
        { status: 500 }
      );
    }

    const subjectParam =
      url.searchParams.get("subject")?.toLowerCase() || "";

    const startParam =
      url.searchParams.get("start") || "0";

    const start = Number(startParam);

    if (!Number.isInteger(start) || start < 0) {
      return Response.json(
        {
          success: false,
          error: "start must be a non-negative integer",
        },
        { status: 400 }
      );
    }

    if (
      !subjectParam ||
      !(subjectParam in DATASETS)
    ) {
      return Response.json(
        {
          success: false,
          error:
            "Invalid subject. Use physics, chemistry, mathematics, or biology.",
        },
        { status: 400 }
      );
    }

    const dataset =
      DATASETS[subjectParam as SubjectKey];

    const questions = loadDataset(dataset);

    const batch = questions.slice(
      start,
      start + BATCH_SIZE
    );

    const sql = neon(process.env.DATABASE_URL);

    let processed = 0;

    for (const rawQuestion of batch) {
      const question = normalizeQuestion(
        rawQuestion,
        dataset.subject
      );

      await insertQuestion(sql, question);

      processed++;
    }

    const nextStart = start + processed;
    const complete = nextStart >= questions.length;

    return Response.json({
      success: true,
      subject: dataset.subject,

      // IMPORTANT:
      // This is ALL questions in the source JSON.
      totalQuestions: questions.length,

      batchStart: start,
      batchSize: processed,
      nextStart,
      complete,

      nextUrl: complete
        ? null
        : `/api/import-mht-cet?subject=${subjectParam}&start=${nextStart}`,
    });
  } catch (error: any) {
    console.error("MHT-CET IMPORT ERROR:", error);

    return Response.json(
      {
        success: false,
        error: error?.message ?? String(error),
      },
      { status: 500 }
    );
  }
}
