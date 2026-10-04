import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";

export async function GET() {
  try {
    const cookieStore = await cookies();
    const sessionCookie =
      cookieStore.get("master_session")?.value;

    if (!sessionCookie) {
      return NextResponse.json(
        { success: false, error: "Unauthorized" },
        { status: 401 }
      );
    }

    let session: {
      role?: string;
      academyId?: string;
    };

    const parsedSession = parseSessionCookie<Record<string, unknown>>(sessionCookie);

    if (!parsedSession) {
      return NextResponse.json(
        { success: false, error: "Invalid session." },
        { status: 401 }
      );
    }

    session = parsedSession;

  
    if (!session.academyId) {
  return NextResponse.json(
    { success: false, error: "Academy access required." },
    { status: 403 }
  );
}

    await pool.query(`
      ALTER TABLE tests
      ADD COLUMN IF NOT EXISTS academy_id UUID,
      ADD COLUMN IF NOT EXISTS created_by_teacher_id UUID
    `);

    const result = await pool.query(
      `
      SELECT *
      FROM (
        SELECT
          p.id::text AS id,
          p.code,
          p.exam,
          p.description,
          p.duration_minutes,
          p.created_by,
          p.created_at,
          p.updated_at,
          p.status,
          p.custom_section,
          COALESCE((SELECT COUNT(*)::int FROM paper_questions pq WHERE pq.paper_id::text = p.id::text), 0) AS question_count,
          'PAPER'::text AS source_type,
          NULL::text AS source_test_id
        FROM papers p
        WHERE p.academy_id::text = $1::text
           OR (
             p.academy_id IS NULL
             AND EXISTS (
               SELECT 1 FROM teachers t
               WHERE t.id::text = p.created_by::text
                 AND t.academy_id::text = $1::text
             )
           )
        UNION ALL
        SELECT
          ('TEST:' || t.id::text) AS id,
          ('GENERATED-' || RIGHT(t.id::text, 8)) AS code,
          t.exam,
          COALESCE(NULLIF(t.title, ''), t.exam || ' Teacher Test') AS description,
          COALESCE(t.duration_minutes, 60) AS duration_minutes,
          t.created_by_teacher_id AS created_by,
          t.created_at,
          t.created_at AS updated_at,
          COALESCE(t.status, 'generated') AS status,
          NULL::text AS custom_section,
          COALESCE(t.question_count, jsonb_array_length(COALESCE(t.questions, '[]'::jsonb)))::int AS question_count,
          'TEST'::text AS source_type,
          t.id::text AS source_test_id
        FROM tests t
        WHERE t.academy_id::text = $1::text
          AND t.created_by_teacher_id IS NOT NULL
      ) available_papers
      ORDER BY created_at DESC
      `,
      [session.academyId]
    );

    return NextResponse.json({
      success: true,
      papers: result.rows,
    });
  } catch (error) {
    console.error("TEACHER PAPERS ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to load papers.",
      },
      { status: 500 }
    );
  }
}