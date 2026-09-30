import { pool } from "@/lib/db";

let schemaPromise: Promise<void> | null = null;

export function ensureFeatureSchema() {
  if (!schemaPromise) {
    schemaPromise = (async () => {
      await pool.query(`
        ALTER TABLE students
        ADD COLUMN IF NOT EXISTS parent_phone VARCHAR(30),
        ADD COLUMN IF NOT EXISTS parent_name VARCHAR(150)
      `);

      await pool.query(`
        ALTER TABLE questions
        ADD COLUMN IF NOT EXISTS academy_id UUID,
        ADD COLUMN IF NOT EXISTS created_by_teacher_id UUID
      `);

      await pool.query(`
        ALTER TABLE tests
        ADD COLUMN IF NOT EXISTS is_full_chapter BOOLEAN NOT NULL DEFAULT FALSE,
        ADD COLUMN IF NOT EXISTS full_chapter_subject VARCHAR(150),
        ADD COLUMN IF NOT EXISTS full_chapter_name VARCHAR(255)
      `);

      await pool.query(`
        CREATE TABLE IF NOT EXISTS gamification_badge_defs (
          id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          category TEXT NOT NULL,
          icon TEXT,
          hidden BOOLEAN NOT NULL DEFAULT FALSE,
          config JSONB NOT NULL DEFAULT '{}'::jsonb,
          created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
      `);

      await pool.query(`
        CREATE TABLE IF NOT EXISTS student_badge_events (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          student_id UUID NOT NULL,
          badge_id TEXT NOT NULL,
          tier INTEGER NOT NULL DEFAULT 1,
          metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
          earned_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
      `);
      await pool.query(`CREATE INDEX IF NOT EXISTS idx_student_badge_events_student_month ON student_badge_events(student_id, earned_at)`);

      await pool.query(`
        CREATE TABLE IF NOT EXISTS student_tests (
          id TEXT PRIMARY KEY,
          student_id UUID NOT NULL,
          test_id TEXT NOT NULL,
          created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
      `);

      await pool.query(`
        CREATE UNIQUE INDEX IF NOT EXISTS student_tests_student_test_unique
        ON student_tests(student_id, test_id)
      `);

      await pool.query(`
        CREATE INDEX IF NOT EXISTS idx_student_tests_student
        ON student_tests(student_id)
      `);

      await pool.query(`
        CREATE INDEX IF NOT EXISTS idx_test_answers_attempt_question
        ON test_answers(attempt_id, question_id)
      `);

      await pool.query(`
        CREATE INDEX IF NOT EXISTS idx_batch_students_student
        ON batch_students(student_id)
      `);
    })().catch((error) => {
      schemaPromise = null;
      throw error;
    });
  }

  return schemaPromise;
}
