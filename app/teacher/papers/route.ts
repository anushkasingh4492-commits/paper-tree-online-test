import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { pool } from "@/lib/db";

async function getTeacherSession() {
  const cookieStore = await cookies();
  const raw = cookieStore.get("master_session")?.value;

  if (!raw) return null;

  try {
    const session = JSON.parse(raw);

    if (session.role !== "TEACHER") {
      return null;
    }

    return session;
  } catch {
    return null;
  }
}

export async function GET() {
  try {
    const session = await getTeacherSession();

    if (!session) {
      return NextResponse.json(
        { success: false, error: "Teacher login required." },
        { status: 401 }
      );
    }

    const result = await pool.query(`
      SELECT
        p.id,
        p.code,
        p.exam,
        p.description,
        p.duration_minutes,
        p.status,
        p.created_at,
        COUNT(pq.id)::int AS question_count
      FROM papers p
      LEFT JOIN paper_questions pq
        ON pq.paper_id = p.id
      WHERE p.created_by = $1
      GROUP BY p.id
      ORDER BY p.created_at DESC
    `, [session.id]);

    return NextResponse.json({
      success: true,
      papers: result.rows,
    });
  } catch (error) {
    console.error("TEACHER PAPERS ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error: error instanceof Error
          ? error.message
          : "Failed to load papers.",
      },
      { status: 500 }
    );
  }
}