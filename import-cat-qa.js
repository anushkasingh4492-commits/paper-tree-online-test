const fs = require("fs");
const { Pool } = require("pg");
require("dotenv").config({ path: ".env.local" });

const FILE =
  "data/cat/qa/CAT_QA_v1.0.0/cat_qa_v1.0.0.json";

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

function normalize(q) {
  const isTita = q.answer_format === "TITA";

  return {
    id: String(q.id),
    exam: "CAT",
    subject: "Quantitative Ability",
    standard: 0,
    chapter_number: Number(q.chapter_number),
    chapter_name: String(q.chapter),
    major_topic: String(q.area),
    subtopic: String(q.subtopic || q.topic || ""),
    concept_tested: String(q.concept_family || q.cognitive_level || ""),
    stem: String(q.question),
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
    raw_data: q,
  };
}

async function main() {
  const source = JSON.parse(fs.readFileSync(FILE, "utf8"));

  if (!Array.isArray(source) || source.length !== 3000) {
    throw new Error(
      `Expected 3000 CAT questions; found ${
        Array.isArray(source) ? source.length : "non-array data"
      }`
    );
  }

  const ids = new Set(source.map((q) => q.id));

  if (ids.size !== source.length) {
    throw new Error("Duplicate source IDs detected; import cancelled.");
  }

  for (const q of source) {
    if (
      !q.id ||
      !q.question ||
      !q.correct_answer ||
      !["MCQ", "TITA"].includes(q.answer_format)
    ) {
      throw new Error(`Invalid CAT record: ${q.id || "(missing ID)"}`);
    }

    if (q.answer_format === "TITA" && !Number.isInteger(q.tita_answer)) {
      throw new Error(`Invalid TITA answer: ${q.id}`);
    }

    if (
      q.answer_format === "MCQ" &&
      (!q.options || !q.correct_option || !q.options[q.correct_option])
    ) {
      throw new Error(`Invalid MCQ options/key: ${q.id}`);
    }
  }

  const client = await pool.connect();

  try {
    const check = await client.query("SELECT NOW() AS time");
    console.log("Database connection OK:", check.rows[0].time);

    const existing = await client.query(
      "SELECT COUNT(*)::int AS count FROM questions WHERE exam = 'CAT'"
    );

    console.log("Existing CAT questions:", existing.rows[0].count);
    console.log("Validated source questions:", source.length);
    console.log("No database writes have happened yet.");

    if (process.argv.includes("--dry-run")) {
      console.log("Dry run complete.");
      return;
    }

    await client.query("BEGIN");

    let written = 0;

    for (let i = 0; i < source.length; i += 50) {
      const batch = source.slice(i, i + 50);

      for (const original of batch) {
        const q = normalize(original);

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
        `Processed ${Math.min(i + batch.length, source.length)}/${source.length}`
      );
    }

    await client.query("COMMIT");
    console.log(`Import complete. Rows inserted or refreshed: ${written}`);

    const verify = await client.query(
      `SELECT question_type, COUNT(*)::int AS count
       FROM questions
       WHERE exam = 'CAT'
       GROUP BY question_type
       ORDER BY question_type`
    );

    console.table(verify.rows);
  } catch (error) {
    try {
      await client.query("ROLLBACK");
    } catch {}
    throw error;
  } finally {
    client.release();
  }
}

main()
  .catch((error) => {
    console.error("CAT import failed:", error);
    if (error instanceof Error && error.stack) {
      console.error(error.stack);
    }
    process.exitCode = 1;
  })
  .finally(() => pool.end());
