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
    file: "data/neet/physics/NEET_2027_Physics_Full_Dataset_with_Figures_v1.0.0 (2)/release_v1.0.0/neet_2027_physics_questions_with_figures_v1.0.0.json",
  },
  {
    subject: "Chemistry",
    file: "data/neet/chemistry/NEET_2027_Chemistry_Full_Dataset_with_Figures_v1.1.0/release_v1.1.0/neet_2027_chemistry_full_dataset.json",
  },
  {
    subject: "Biology",
    file: "data/neet/biology/NEET_2027_Biology_Full_Dataset_with_Figures_v1.5.4/question_bank.json",
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
  // Chemistry: unit_number is already numeric
  if (q.unit_number != null) {
    return safeInteger(q.unit_number);
  }

  // Physics: "Unit 1: Physics and Measurement"
  // Biology: handle numeric unit if available
  if (q.unit != null) {
    const match = String(q.unit).match(/^\s*Unit\s+(\d+)/i);

    if (match) {
      return safeInteger(match[1]);
    }

    const unitNumber = safeInteger(q.unit);

    if (unitNumber != null) {
      return unitNumber;
    }
  }

  // Fallback if a dataset explicitly provides chapter_number
  if (q.chapter_number != null) {
    return safeInteger(q.chapter_number);
  }

  // Existing DB column is NOT NULL.
  return 0;
}

function getStandard(q) {
  const sourceClass = clean(q.source_class);

  if (sourceClass === "XI") return 11;
  if (sourceClass === "XII") return 12;

  return 11;
}

function getChapterName(q) {
  return clean(q.chapter ?? q.unit ?? "");
}

function getMajorTopic(q) {
  return clean(q.topic);
}

function getFigureAsset(q) {
  if (q.figure_asset) {
    return String(q.figure_asset);
  }

  if (Array.isArray(q.figures) && q.figures.length > 0) {
    return JSON.stringify(q.figures);
  }

  return null;
}

function normalizeQuestion(q, subject) {
  return {
    id: String(q.id),
    exam: "NEET",
    subject,

    standard: getStandard(q),

    chapter_number: getChapterNumber(q),
    chapter_name: getChapterName(q),

    major_topic: getMajorTopic(q),
    subtopic: clean(q.subtopic),

    concept_tested: clean(
      q.cognitive_level ??
      q.tags ??
      null
    ),

    stem: clean(
      q.question ??
      q.stem ??
      ""
    ),

    options: q.options ?? {},

    correct_option: clean(
      q.correct_option ??
      ""
    ),

    correct_answer_text: clean(
      q.correct_answer_text ??
      q.correct_answer ??
      null
    ),

    distractor_rationale: null,

    solution: clean(
      q.explanation ??
      q.solution ??
      null
    ),

    formula_principle: null,

    common_misconception: null,

    difficulty: clean(
      q.difficulty ??
      "Mixed"
    ),

    estimated_time: null,

    question_type: clean(
      q.question_type
    ),

    figure_asset: getFigureAsset(q),

    concept_family_id: null,
    family_size: null,

    /*
     * These two fields belong to the existing MHT-CET
     * schema. Keep them false for NEET so NEET questions
     * cannot accidentally enter CET generation.
     */
    generator_eligible_strict_cet: false,
    generator_eligible_extended_revision: false,

    syllabus_scope_status: clean(
      q.validation_status ??
      null
    ),

    syllabus_version: clean(
      q.syllabus_reference ??
      null
    ),

    release_version: clean(
      q.release_version ??
      null
    ),

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
      WHERE exam = 'NEET'
        AND subject = ${subject}
    `
  );

  return new Set(
    result.map((row) => String(row.id))
  );
}

async function main() {
  console.log("========================================");
  console.log(" PAPER TREE ONLINE TEST");
  console.log(" NEET QUESTION IMPORT");
  console.log(" NEON HTTP RESUMABLE MODE");
  console.log("========================================\n");

  const connectionTest = await sql`
    SELECT NOW() AS time
  `;

  console.log("DATABASE HTTP CONNECTION: OK");
  console.log(
    `Database time: ${connectionTest[0].time}\n`
  );

  let totalSource = 0;
  let totalEligible = 0;
  let totalNew = 0;

  for (const dataset of DATASETS) {
    console.log("\n========================================");
    console.log(dataset.subject.toUpperCase());
    console.log("========================================");

    const questions =
      loadQuestions(dataset.file);

    const eligible =
      questions.filter(
        (q) => q.generator_eligible === true
      );

    console.log(
      `Total questions: ${questions.length}`
    );

    console.log(
      `Generator eligible: ${eligible.length}`
    );

    const existingIds =
      await getExistingIds(dataset.subject);

    console.log(
      `Already in database: ${existingIds.size}`
    );

    const remaining =
      eligible.filter(
        (q) =>
          !existingIds.has(String(q.id))
      );

    console.log(
      `Remaining to import: ${remaining.length}`
    );

    if (remaining.length === 0) {
      console.log(
        `${dataset.subject}: COMPLETE`
      );

      totalSource += questions.length;
      totalEligible += eligible.length;

      continue;
    }

    for (
      let batchStart = 0;
      batchStart < remaining.length;
      batchStart += BATCH_SIZE
    ) {
      const batch =
        remaining.slice(
          batchStart,
          batchStart + BATCH_SIZE
        );

      for (const rawQuestion of batch) {
        const normalized =
          normalizeQuestion(
            rawQuestion,
            dataset.subject
          );

        await insertQuestion(
          normalized
        );

        totalNew++;
      }

      const completed =
        Math.min(
          batchStart + batch.length,
          remaining.length
        );

      console.log(
        `${dataset.subject}: ${completed}/${remaining.length}`
      );
    }

    const finalIds =
      await getExistingIds(
        dataset.subject
      );

    console.log(
      `${dataset.subject}: ${finalIds.size}/${eligible.length} in database`
    );

    totalSource += questions.length;
    totalEligible += eligible.length;
  }

  console.log("\n========================================");
  console.log(" NEET IMPORT COMPLETE");
  console.log("========================================");

  console.log(
    `Source questions: ${totalSource}`
  );

  console.log(
    `Generator eligible: ${totalEligible}`
  );

  console.log(
    `New questions inserted: ${totalNew}`
  );

  const counts =
    await queryWithRetry(() =>
      sql`
        SELECT
          subject,
          COUNT(*)::int AS count
        FROM questions
        WHERE exam = 'NEET'
        GROUP BY subject
        ORDER BY subject
      `
    );

  console.log("\nNEET database counts:");
  console.table(counts);
}

main().catch((error) => {
  console.error("\nIMPORT FAILED");
  console.error(error);
  process.exitCode = 1;
});
