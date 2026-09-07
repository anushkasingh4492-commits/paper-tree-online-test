import { NextResponse } from "next/server";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function GET() {
  const client = await pool.connect();

  try {
    await client.query("BEGIN");

    /* =============================================
       ACADEMIES
    ============================================= */

    await client.query(`
      CREATE TABLE IF NOT EXISTS academies (
        id UUID PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        code VARCHAR(100) UNIQUE NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
      )
    `);

    /* =============================================
       ADD ACADEMY OWNERSHIP
    ============================================= */

    await client.query(`
      ALTER TABLE admins
      ADD COLUMN IF NOT EXISTS academy_id UUID
    `);

    await client.query(`
      ALTER TABLE teachers
      ADD COLUMN IF NOT EXISTS academy_id UUID
    `);

    await client.query(`
      ALTER TABLE students
      ADD COLUMN IF NOT EXISTS academy_id UUID
    `);

    await client.query(`
      ALTER TABLE students
      ADD COLUMN IF NOT EXISTS exam VARCHAR(50) DEFAULT 'JEE-MAINS'
    `);

    await client.query(`
      ALTER TABLE academies
      ADD COLUMN IF NOT EXISTS status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',
      ADD COLUMN IF NOT EXISTS student_limit INTEGER NOT NULL DEFAULT 10,
      ADD COLUMN IF NOT EXISTS subscription_start DATE,
      ADD COLUMN IF NOT EXISTS subscription_end DATE,
      ADD COLUMN IF NOT EXISTS subscription_plan VARCHAR(255)
    `);

    await client.query(`
      ALTER TABLE papers
      ADD COLUMN IF NOT EXISTS academy_id UUID
    `);

    await client.query(`
      ALTER TABLE scheduled_tests
      ADD COLUMN IF NOT EXISTS academy_id UUID
    `);

    /* =============================================
       MASTER FLAG

       academy admins → is_master = false
       Paper Tree owner → is_master = true
    ============================================= */

    await client.query(`
      ALTER TABLE admins
      ADD COLUMN IF NOT EXISTS is_master BOOLEAN
      NOT NULL DEFAULT FALSE
    `);

    /* =============================================
       INDIVIDUAL TEST ASSIGNMENTS
    ============================================= */

    await client.query(`
      CREATE TABLE IF NOT EXISTS scheduled_test_students (
        scheduled_test_id UUID NOT NULL,
        student_id UUID NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

        PRIMARY KEY (
          scheduled_test_id,
          student_id
        )
      )
    `);
    /* =============================================
       BATCHES
    ============================================= */

    await client.query(`
      CREATE TABLE IF NOT EXISTS batches (
        id UUID PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        class_name VARCHAR(100),
        created_by TEXT,
        academy_id UUID NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
      )
    `);

    /* =============================================
       BATCH STUDENTS
    ============================================= */

    await client.query(`
      CREATE TABLE IF NOT EXISTS batch_students (
        batch_id UUID NOT NULL,
        student_id UUID NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

        PRIMARY KEY (batch_id, student_id)
      )
    `);

    await client.query(`
      CREATE INDEX IF NOT EXISTS idx_batches_academy
      ON batches(academy_id)
    `);

    await client.query(`
      CREATE INDEX IF NOT EXISTS idx_batch_students_batch
      ON batch_students(batch_id)
    `);

    await client.query(`
      CREATE INDEX IF NOT EXISTS idx_batch_students_student
      ON batch_students(student_id)
    `);
    /* =============================================
       USEFUL INDEXES
    ============================================= */

    await client.query(`
      CREATE INDEX IF NOT EXISTS idx_students_academy
      ON students(academy_id)
    `);

    await client.query(`
      CREATE INDEX IF NOT EXISTS idx_teachers_academy
      ON teachers(academy_id)
    `);

    await client.query(`
      CREATE INDEX IF NOT EXISTS idx_admins_academy
      ON admins(academy_id)
    `);

    await client.query(`
      CREATE INDEX IF NOT EXISTS idx_papers_academy
      ON papers(academy_id)
    `);

    await client.query(`
      CREATE INDEX IF NOT EXISTS idx_scheduled_tests_academy
      ON scheduled_tests(academy_id)
    `);

    await client.query("COMMIT");

    return NextResponse.json({
      success: true,
      message: "Multi-academy database foundation created.",
    });
  } catch (error) {
    await client.query("ROLLBACK");

    console.error("MULTITENANCY SETUP ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Setup failed.",
      },
      { status: 500 }
    );
  } finally {
    client.release();
  }
}
