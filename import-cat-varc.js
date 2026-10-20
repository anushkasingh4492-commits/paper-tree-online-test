/* eslint @typescript-eslint/no-require-imports: off */
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
  ssl: { rejectUnauthorized: false },
  max: 5,
  connectionTimeoutMillis: 10000,
});

async function queryWithRetry(queryFn) {
  for (let attempt = 1; attempt <= 5; attempt++) {
    try {
      return await queryFn();
    } catch (error) {
      if (attempt === 5) throw error;
      console.log(`  DB retry ${attempt}/5...`);
      await sleep(attempt * 2000);
    }
  }
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const FILE = "data/cat/varc/CAT_VARC_v1.0.0/CAT_VARC_v1.0.0/cat_varc_v1.0.0.json";
const BATCH_SIZE = 50;

function loadQuestions(file) {
  const fullPath = path.resolve(file);
  if (!fs.existsSync(fullPath)) {
    throw new Error(`Dataset not found: ${file}`);
  }
  const parsed = JSON.parse(fs.readFileSync(fullPath, "utf8"));
  if (!parsed || !parsed.questions || !Array.isArray(parsed.questions)) {
    throw new Error(`${file} does not contain a questions array`);
  }
  if (!Array.isArray(parsed.sets)) {
    throw new Error(`${file} does not contain a sets array`);
  }

  const sets = new Map();
  for (const set of parsed.sets) {
    if (!set.set_id || sets.has(String(set.set_id))) {
      throw new Error("VARC source contains a missing or duplicate set ID.");
    }
    sets.set(String(set.set_id), set);
  }

  for (const question of parsed.questions) {
    if (question.set_id && !sets.has(String(question.set_id))) {
      throw new Error(
        `VARC question ${question.id} references missing set ${question.set_id}.`
      );
    }
  }

  return { questions: parsed.questions, sets };
}

function clean(value) {
  if (value === null || value === undefined) return null;
  return String(value).trim();
}

function safeInteger(value) {
  if (value === null || value === undefined) return null;
  const n = Number(String(value).trim());
  return Number.isInteger(n) ? n : null;
}

function normalizeQuestion(q, sets) {
  const isTita = q.answer_format === "TITA";
  const sourceSet = q.set_id
    ? sets.get(String(q.set_id))
    : undefined;
  const stem = [
    ...(Array.isArray(sourceSet?.paragraphs)
      ? sourceSet.paragraphs.map(clean)
      : []),
    clean(q.instructions),
    clean(q.question),
  ]
    .filter((part) => part)
    .join("\n\n");

  return {
    id: String(q.id),
    exam: "CAT",
    subject: clean(q.section) ?? "Verbal Ability",
    standard: 0,
    chapter_number: safeInteger(q.chapter_number) ?? 1,
    chapter_name: clean(q.chapter) ?? "General",
    major_topic: clean(q.area) ?? null,
    subtopic: clean(q.topic) ?? null,
    concept_tested: clean(q.concept_family) ?? null,
    stem,
    options: isTita ? {} : (q.options || {}),
    correct_option: isTita ? "" : String(q.correct_option || ""),
    correct_answer_text: isTita
      ? String(q.tita_answer)
      : String(q.correct_answer || ""),
    solution: String(q.explanation || ""),
    formula_principle: null,
    common_misconception: q.common_misconception || null,
    difficulty: String(q.difficulty || "Medium"),
    estimated_time: null,
    question_type: isTita ? "TITA" : "MCQ",
    figure_asset:
      Array.isArray(q.figures) && q.figures.length
        ? q.figures[0].file || null
        : null,
    concept_family_id: q.concept_family || null,
    family_size: null,
    generator_eligible_strict_cet: false,
    generator_eligible_extended_revision: false,
    syllabus_scope_status: "CAT",
    syllabus_version: null,
    release_version: String(q.release_version || "v1.0.0"),
    raw_data: sourceSet
      ? { ...q, source_set: sourceSet }
      : q,
  };
}

async function getExistingIds() {
  const result = await queryWithRetry(() =>
    pool.query(`SELECT id FROM questions WHERE exam = 'CAT'`)
  );
  return new Set(result.rows.map((row) => String(row.id)));
}

async function main() {
  console.log("========================================");
  console.log(" PAPER TREE ONLINE TEST");
  console.log(" CAT VARC QUESTION IMPORT");
  console.log("========================================");

  const check = await pool.query(`SELECT NOW() AS time`);
  console.log("Database connection OK:", check.rows[0].time);

  const { questions: source, sets } = loadQuestions(FILE);
  console.log("Validated source questions:", source.length);

  const ids = new Set(source.map((q) => q.id));
  if (ids.size !== source.length) {
    throw new Error("Duplicate source IDs detected; import cancelled.");
  }

  const existing = await getExistingIds();
  console.log("Existing CAT questions:", existing.size);

  const remaining = source.filter((q) => !existing.has(String(q.id)));
  console.log("Remaining to import:", remaining.length);

  if (remaining.length === 0) {
    console.log("CAT VARC: COMPLETE");
    return;
  }

  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    let written = 0;
    for (let i = 0; i < remaining.length; i += BATCH_SIZE) {
      const batch = remaining.slice(i, i + BATCH_SIZE);
      for (const original of batch) {
        const q = normalizeQuestion(original, sets);
        const result = await client.query(
          `INSERT INTO questions (
            id, exam, subject, standard, chapter_number, chapter_name,
            major_topic, subtopic, concept_tested, stem, options,
            correct_option, correct_answer_text, solution,
            formula_principle, common_misconception, difficulty,
            estimated_time, question_type, figure_asset,
            concept_family_id, family_size,
            generator_eligible_strict_cet,
            generator_eligible_extended_revision,
            syllabus_scope_status, syllabus_version, release_version,
            raw_data
          ) VALUES (
            $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11::jsonb,
            $12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,
            $23,$24,$25,$26,$27,$28::jsonb
          )
          ON CONFLICT (id) DO UPDATE
          SET raw_data = EXCLUDED.raw_data
          WHERE questions.raw_data IS DISTINCT FROM EXCLUDED.raw_data`,
          [
            q.id, q.exam, q.subject, q.standard, q.chapter_number,
            q.chapter_name, q.major_topic, q.subtopic, q.concept_tested,
            q.stem, JSON.stringify(q.options), q.correct_option,
            q.correct_answer_text, q.solution, q.formula_principle,
            q.common_misconception, q.difficulty, q.estimated_time,
            q.question_type, q.figure_asset, q.concept_family_id,
            q.family_size, q.generator_eligible_strict_cet,
            q.generator_eligible_extended_revision, q.syllabus_scope_status,
            q.syllabus_version, q.release_version, JSON.stringify(q.raw_data),
          ]
        );
        written += result.rowCount;
      }
      console.log(
        `Processed ${Math.min(i + batch.length, remaining.length)}/${remaining.length}`
      );
    }
    await client.query("COMMIT");
    console.log(`Import complete. Rows inserted/refreshed: ${written}`);
  } catch (error) {
    try { await client.query("ROLLBACK"); } catch {}
    throw error;
  } finally {
    client.release();
  }

  const verify = await pool.query(
    `SELECT question_type, COUNT(*)::int AS count FROM questions WHERE exam = 'CAT' GROUP BY question_type ORDER BY question_type`
  );
  console.table(verify.rows);
}

main()
  .catch((error) => {
    console.error("CAT VARC import failed:", error);
    if (error instanceof Error && error.stack) console.error(error.stack);
    process.exitCode = 1;
  })
  .finally(() => pool.end());
