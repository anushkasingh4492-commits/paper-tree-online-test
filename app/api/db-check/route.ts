import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function GET() {
  try {
    const result = await pool.query(`
      SELECT
        exam,
        subject,
        COUNT(*)::int AS count
      FROM questions
      GROUP BY exam, subject
      ORDER BY exam, subject
    `);

    return Response.json({
      success: true,
      data: result.rows,
    });
  } catch (error) {
    console.error("DB CHECK ERROR:", error);

    return Response.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Database query failed",
      },
      { status: 500 }
    );
  }
}
