import { pool } from "@/lib/db";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const tables = await pool.query(`
      SELECT table_name
      FROM information_schema.tables
      WHERE table_schema = 'public'
      ORDER BY table_name
    `);

    const questions = await pool.query(`
      SELECT column_name, data_type
      FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'questions'
      ORDER BY ordinal_position
    `);

    const tests = await pool.query(`
      SELECT column_name, data_type
      FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'tests'
      ORDER BY ordinal_position
    `);

    const examValues = await pool.query(`
      SELECT exam, COUNT(*)::int AS count
      FROM questions
      GROUP BY exam
      ORDER BY exam
    `);

    return Response.json({
      success: true,
      tables: tables.rows,
      questionsColumns: questions.rows,
      testsColumns: tests.rows,
      examValues: examValues.rows,
    });
  } catch (error) {
    console.error(error);
const statusCheck = await pool.query(`
  SELECT
    pg_get_constraintdef(oid) AS constraint_definition
  FROM pg_constraint
  WHERE conname = 'scheduled_tests_status_check'
`);

console.log("SCHEDULED TEST STATUS CONSTRAINT:", statusCheck.rows);
    return Response.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : String(error),
      },
      { status: 500 }
    );
  }
}
