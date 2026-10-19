const fs = require("fs");
const path = require("path");
const { Pool } = require("pg");
require("dotenv").config({ path: ".env.local" });

if (!process.env.DATABASE_URL) {
  console.error("DATABASE_URL is missing from .env.local");
  process.exit(1);
}

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false,
  },
  max: 10,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 10000,
});

async function sql(strings, ...values) {
  let text = strings[0];
  for (let i = 0; i < values.length; i++) {
    text += `$${i + 1}`;
    text += strings[i + 1];
  }
  const result = await pool.query(text, values);
  return result.rows;
}

const DATASETS = [
  {
    subject: "Physics",
    file:
      "data/JEE/physics/JEE_Main_Physics_v1.4.0/release_v1.4.0/jee_main_physics_questions.json",
  },
  {
    subject: "Chemistry",
    file:
      "data/JEE/chemistry/JEE_Main_Chemistry_v1.1.0_FIXED/release_v1.1.0/jee_main_chemistry_questions.json",
  },
  {
    subject: "Mathematics",
    file:
      "data/JEE/maths/JEE_Main_Maths_v1.0.1/release_v1.0.1/jee_main_maths_questions.json",
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
      if (attempt === RETRIES) {
        throw error;
      }
      console.log(`  Database error. Retry ${attempt}/${RETRIES}...`);
      await sleep(attempt * 2000);
    }
  }
}

function loadQuestions(file) {
  const fullPath = path.resolve(file);
  if (!fs.existsSync(fullPath)) {
    throw new Error(`Dataset not found: ${file}`);
  }
  const parsed = JSON.parse(fs.readFileSync(fullPath, "utf8"));
  if (!Array.isArray(parsed)) {
    throw new Error(`${file} does not contain a JSON array`);
  }
  return parsed;
}

function clean(value) {
  if (value === null || value === undefined) {
    return null;
  }
  return String(value).trim();
}

function safeInteger(value) {
  if (value === null || value === undefined) {
    return null;
  }
  const text = String(value).trim();
  if (!text) {
    return null;
  }
  const n = Number(text);
  return Number.isInteger(n) ? n : null;
}

function getChapterNumber(q) {
  if (q.chapter_number != null) {
    return safeInteger(q.chapter_number);
  }
  if (q.unit_number != null) {
    return safeInteger(q.unit_number);
  }
  return 1;
}

function normalizeQuestion(q, subject) {
  return {
    id: String(q.id),
    exam: "JEE",
    subject,
    standard: safeInteger(q.standard) ?? 12,
    chapter_number: getChapterNumber(q),
    chapter_name: clean(q.chapter_name) ?? "General",
    major_topic: clean(q.major_topic) ?? null,
    subtopic: clean(q.subtopic) ?? null,
    concept_tested: clean(q.concept_tested) ?? null,
    stem: clean(q.stem) ?? clean(q.question) ?? "",
    options: q.options ?? {},
    correct_option: clean(q.correct_option) ?? "",
    correct_answer_text: clean(q.correct_answer_text) ?? null,
    distractor_rationale: q.distractor_rationale ?? null,
    solution: clean(q.solution) ?? null,
    formula_principle: clean(q.formula_principle) ?? null,
    common_misconception: clean(q.common_misconception) ?? null,
    difficulty: clean(q.difficulty) ?? "Medium",
    estimated_time: clean(q.estimated_time) ?? null,
    question_type: clean(q.question_type) ?? null,
    figure_asset: clean(q.figure_asset) ?? null,
    concept_family_id: clean(q.concept_family_id) ?? null,
    family_size: safeInteger(q.family_size),
    generator_eligible_strict_cet:
      q.generator_eligible_strict_cet === true,
    generator_eligible_extended_revision:
      q.generator_eligible_extended_revision === true,
    syllabus_scope_status: clean(q.syllabus_scope_status) ?? null,
    syllabus_version: clean(q.syllabus_version) ?? null,
    release_version: clean(q.release_version) ?? null,
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
      ) VALUES (
        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10,
        $11::jsonb, $12, $13, $14, $15, $16, $17, $18,
        $19, $20, $21, $22, $23, $24, $25, $26, $27,
        $28::jsonb
      )
      ON CONFLICT (id) DO UPDATE
      SET raw_data = EXCLUDED.raw_data
      WHERE questions.raw_data IS DISTINCT FROM EXCLUDED.raw_data`,
    [
      q.id,
      q.exam,
      q.subject,
      q.standard,
      q.chapter_number,
      q.chapter_name,
      q.major_topic,
      q.subtopic,
      q.concept_tested,
      q.stem,
      JSON.stringify(q.options),
      q.correct_option,
      q.correct_answer_text,
      q.solution,
      q.formula_principle,
      q.common_misconception,
      q.difficulty,
      q.estimated_time,
      q.question_type,
      q.figure_asset,
      q.concept_family_id,
      q.family_size,
      q.generator_eligible_strict_cet,
      q.generator_eligible_extended_revision,
      q.syllabus_scope_status,
      q.syllabus_version,
      q.release_version,
      JSON.stringify(q.raw_data),
    ]
  );
}

async function getExistingIds(subject) {
  const result = await queryWithRetry(() =>
    sql`
      SELECT id
      FROM questions
      WHERE exam = 'JEE' AND subject = $1`,
    [subject]
  );

  return new Set(result.map((row) => String(row.id)));
}

async function main() {
  console.log("========================================");
  console.log(" PAPER TREE ONLINE TEST");
  console.log(" JEE QUESTION IMPORT");
  console.log("========================================");

  const connectionTest = await sql`
    SELECT NOW() AS time
  `;

  console.log("DATABASE CONNECTION: OK");
  console.log(`Database time: ${connectionTest[0].time}\n`);

  let totalSource = 0;
  let totalNew = 0;

  for (const dataset of DATASETS) {
    console.log(`\n========================================`);
    console.log(`${dataset.subject.toUpperCase()}`);
    console.log(`========================================`);

    const questions = loadQuestions(dataset.file);

    console.log(`Total questions: ${questions.length}`);

    const existingIds = await getExistingIds(dataset.subject);

    console.log(`Already in database: ${existingIds.size}`);

    const remaining = questions.filter(
      (q) => !existingIds.has(String(q.id))
    );

    console.log(`Remaining to import: ${remaining.length}`);

    if (remaining.length === 0) {
      console.log(`${dataset.subject}: COMPLETE`);
      totalSource += questions.length;
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

    const finalIds = await getExistingIds(dataset.subject);
    console.log(
      `${dataset.subject}: ${finalIds.size}/${questions.length} in database`
    );
    totalSource += questions.length;
  }

  console.log("\n========================================");
  console.log(" JEE IMPORT COMPLETE");
  console.log("========================================");

  console.log(`Source questions: ${totalSource}`);
  console.log(`New questions inserted: ${totalNew}`);

  const counts = await queryWithRetry(() =>
    sql`
      SELECT
        subject,
        COUNT(*)::int AS count
      FROM questions
      WHERE exam = 'JEE'
      GROUP BY subject
      ORDER BY subject
    `
  );

  console.log("\nJEE database counts:");
  console.table(counts);
}

main()
  .catch((error) => {
    console.error("\nIMPORT FAILED");
    console.error(error);
    process.exitCode = 1;
  })
  .finally(async () => {
    await pool.end();
  });
