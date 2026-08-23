const fs = require("fs");
const path = require("path");
const { neon } = require("@neondatabase/serverless");
require("dotenv").config({ path: ".env.local" });

if (!process.env.DATABASE_URL) {
  console.error("DATABASE_URL is missing from .env.local");
  process.exit(1);
}

const sql = neon(process.env.DATABASE_URL);

const DATASETS = [
  {
    subject: "Physics",
    file: "data/mht-cet/physics/question_bank_physics_with_figures_v1.3.0.json",
  },
  {
    subject: "Chemistry",
    file: "data/mht-cet/chemistry/MHT-CET_Chemistry_question_bank_v2.0.0.json",
  },
  {
    subject: "Mathematics",
    file: "data/mht-cet/maths/question_bank_maths_full_v2.0.1.json",
  },
  {
    subject: "Biology",
    file: "data/mht-cet/biology/MHT-CET_Biology_question_bank_v2.1.0.json",
  },
];

const BATCH_SIZE = 50;
const RETRIES = 5;

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function queryWithRetry(queryFn) {
  for (let attempt = 1; attempt <= RETRIES; attempt++) {
    try {
      return await queryFn();
    } catch (error) {
      if (attempt === RETRIES) throw error;

      console.log(
        `  Database error. Retry ${attempt}/${RETRIES}...`
      );

      await sleep(attempt * 2000);
    }
  }
}

function loadQuestions(file) {
  const fullPath = path.resolve(file);

  if (!fs.existsSync(fullPath)) {
    throw new Error(`Dataset not found: ${file}`);
  }

  const parsed = JSON.parse(
    fs.readFileSync(fullPath, "utf8")
  );

  if (!Array.isArray(parsed)) {
    throw new Error(
      `${file} does not contain a JSON array`
    );
  }

  return parsed;
}

function normalizeQuestion(q, subject) {
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
    syllabus_scope_status:
      q.syllabus_scope_status ?? null,
    syllabus_version:
      q.syllabus_version ?? null,
    release_version:
      q.release_version ?? null,
    raw_data: q,
  };
}

async function insertQuestion(q) {
  return queryWithRetry(() =>
    sql`
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
    `
  );
}

async function getExistingIds(subject) {
  const result = await queryWithRetry(() =>
    sql`
      SELECT id
      FROM questions
      WHERE exam = 'MHT-CET'
        AND subject = ${subject}
        AND generator_eligible_strict_cet = true
    `
  );

  return new Set(result.map((row) => String(row.id)));
}

async function main() {
  console.log("========================================");
  console.log(" PAPER TREE ONLINE TEST");
  console.log(" MHT-CET QUESTION IMPORT");
  console.log(" NEON HTTP RESUMABLE MODE");
  console.log("========================================\n");

  const connectionTest = await sql`
    SELECT NOW() AS time
  `;

  console.log("DATABASE HTTP CONNECTION: OK");
  console.log(`Database time: ${connectionTest[0].time}\n`);

  let totalSource = 0;
  let totalEligible = 0;
  let totalNew = 0;

  for (const dataset of DATASETS) {
    console.log(`\n========================================`);
    console.log(`${dataset.subject.toUpperCase()}`);
    console.log(`========================================`);

    const questions = loadQuestions(dataset.file);

    const eligible = questions.filter(
      (q) => q.generator_eligible_strict_cet === true
    );

    console.log(`Total questions: ${questions.length}`);
    console.log(`Strict CET eligible: ${eligible.length}`);

    const existingIds =
      await getExistingIds(dataset.subject);

    console.log(
      `Already in database: ${existingIds.size}`
    );

    const remaining = eligible.filter(
      (q) => !existingIds.has(String(q.id))
    );

    console.log(
      `Remaining to import: ${remaining.length}`
    );

    if (remaining.length === 0) {
      console.log(`${dataset.subject}: COMPLETE`);

      totalSource += questions.length;
      totalEligible += eligible.length;

      continue;
    }

    for (
      let batchStart = 0;
      batchStart < remaining.length;
      batchStart += BATCH_SIZE
    ) {
      const batch = remaining.slice(
        batchStart,
        batchStart + BATCH_SIZE
      );

      for (const rawQuestion of batch) {
        const normalized = normalizeQuestion(
          rawQuestion,
          dataset.subject
        );

        await insertQuestion(normalized);

        totalNew++;
      }

      const completed = Math.min(
        batchStart + batch.length,
        remaining.length
      );

      console.log(
        `${dataset.subject}: ${completed}/${remaining.length}`
      );
    }

    const finalIds =
      await getExistingIds(dataset.subject);

    console.log(
      `${dataset.subject}: ${finalIds.size}/${eligible.length} in database`
    );

    totalSource += questions.length;
    totalEligible += eligible.length;
  }

  console.log("\n========================================");
  console.log(" IMPORT COMPLETE");
  console.log("========================================");
  console.log(`Source questions: ${totalSource}`);
  console.log(`Strict CET eligible: ${totalEligible}`);
  console.log(`New questions inserted: ${totalNew}`);

  const counts = await queryWithRetry(() =>
    sql`
      SELECT
        subject,
        COUNT(*)::int AS count
      FROM questions
      WHERE exam = 'MHT-CET'
        AND generator_eligible_strict_cet = true
      GROUP BY subject
      ORDER BY subject
    `
  );

  console.log("\nDatabase counts:");
  console.table(counts);
}

main().catch((error) => {
  console.error("\nIMPORT FAILED");
  console.error(error);
  process.exitCode = 1;
});
