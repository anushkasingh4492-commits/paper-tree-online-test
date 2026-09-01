import { NextResponse } from "next/server";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function GET() {
  try {
    const result = await pool.query(`
      SELECT
        st.id,
        st.paper_id,
        st.batch_id,
        st.title,
        st.start_time,
        st.end_time,
        st.duration_minutes,
        st.status,
        st.created_at
      FROM scheduled_tests st
      ORDER BY st.created_at DESC
      LIMIT 20;
    `);

    return NextResponse.json({
      success: true,
      scheduledTests: result.rows,
    });
  } catch (error: unknown) {
    console.error("SCHEDULED TEST DEBUG ERROR:", error);

    return NextResponse.json(
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
