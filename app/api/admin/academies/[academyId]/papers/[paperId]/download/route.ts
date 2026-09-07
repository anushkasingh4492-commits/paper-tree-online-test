import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";

async function isMasterAdmin() {
  const cookieStore = await cookies();
  const sessionCookie = cookieStore.get("master_session")?.value;

  if (!sessionCookie) return false;

  try {
    const session = JSON.parse(sessionCookie);
    return session.role === "ADMIN" || session.role === "MASTER_ADMIN";
  } catch {
    return false;
  }
}

export async function GET(
  _request: Request,
  {
    params,
  }: {
    params: Promise<{ academyId: string; paperId: string }>;
  }
) {
  if (!(await isMasterAdmin())) {
    return NextResponse.json(
      { success: false, error: "Unauthorized" },
      { status: 401 }
    );
  }

  const { academyId, paperId } = await params;

  try {
    const paperResult = await pool.query(
      `
      SELECT
        p.id,
        p.code,
        p.exam,
        p.description,
        p.duration_minutes,
        p.status,
        p.created_by,
        p.created_at,
        t.name AS creator_name,
        t.email AS creator_email
      FROM papers p
      LEFT JOIN teachers t ON t.id::text = p.created_by::text
      WHERE p.id = $1
        AND p.academy_id = $2
      LIMIT 1
      `,
      [paperId, academyId]
    );

    if (paperResult.rows.length === 0) {
      return NextResponse.json(
        { success: false, error: "Paper not found." },
        { status: 404 }
      );
    }

    const questionsResult = await pool.query(
      `
      SELECT
        pq.question_order,
        q.id,
        q.exam,
        q.subject,
        q.chapter_name,
        q.stem,
        q.options,
        q.correct_option,
        q.solution,
        q.difficulty,
        q.question_type
      FROM paper_questions pq
      INNER JOIN questions q ON q.id = pq.question_id
      WHERE pq.paper_id = $1
      ORDER BY pq.question_order
      `,
      [paperId]
    );

    const payload = {
      downloadedAt: new Date().toISOString(),
      paper: paperResult.rows[0],
      questions: questionsResult.rows,
    };

    return new NextResponse(JSON.stringify(payload, null, 2), {
      status: 200,
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Content-Disposition": `attachment; filename="${paperResult.rows[0].code || paperId}.json"`,
      },
    });
  } catch (error) {
    console.error("PAPER DOWNLOAD ERROR:", error);

    return NextResponse.json(
      { success: false, error: "Failed to download paper." },
      { status: 500 }
    );
  }
}