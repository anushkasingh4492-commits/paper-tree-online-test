import { NextResponse } from "next/server";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function GET() {
  try {
    const result = await pool.query(`
      SELECT
        conname,
        pg_get_constraintdef(oid) AS definition
      FROM pg_constraint
      WHERE conname = 'scheduled_tests_status_check'
    `);

    return NextResponse.json({
      success: true,
      constraints: result.rows,
    });
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: error instanceof Error ? error.message : String(error),
    }, { status: 500 });
  }
}
