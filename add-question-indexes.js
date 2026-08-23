require("dotenv").config();

const { Pool } = require("pg");

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

async function main() {
  try {
    console.log("Creating question indexes...");

    await pool.query(`
      CREATE INDEX IF NOT EXISTS idx_questions_exam_subject
      ON questions (exam, subject);
    `);

    await pool.query(`
      CREATE INDEX IF NOT EXISTS idx_questions_exam_subject_chapter
      ON questions (exam, subject, chapter_name);
    `);

    await pool.query(`
      CREATE INDEX IF NOT EXISTS idx_questions_exam_subject_chapter_difficulty
      ON questions (exam, subject, chapter_name, difficulty);
    `);

    console.log("✅ All question indexes created successfully.");
  } catch (error) {
    console.error("❌ INDEX ERROR:");
    console.error(error);
  } finally {
    await pool.end();
  }
}

main();
