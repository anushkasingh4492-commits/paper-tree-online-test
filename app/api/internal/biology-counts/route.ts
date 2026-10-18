import { NextResponse } from "next/server";
import { pool } from "@/lib/db";
import { productionDisabledResponse } from "@/lib/internal-route";

export const runtime = "nodejs";

export async function GET() {
  const blocked = productionDisabledResponse();
  if (blocked) return blocked;

  try {
    const result = await pool.query(`
      SELECT
        exam,
        subject,
        chapter_name,
        COUNT(*)::int AS total
      FROM questions
      WHERE LOWER(subject) LIKE '%biology%'
         OR LOWER(COALESCE(chapter_name, '')) LIKE '%biology%'
      GROUP BY exam, subject, chapter_name
      ORDER BY exam, subject, chapter_name;
    `);

    return NextResponse.json({
      success: true,
      groups: result.rows,
    });
  } catch (error) {
    console.error("BIOLOGY COUNTS DIAGNOSTIC:", error);
    return NextResponse.json(
      {
        success: false,
        error: error instanceof Error ? error.message : String(error),
      },
      { status: 500 }
    );
  }
}
