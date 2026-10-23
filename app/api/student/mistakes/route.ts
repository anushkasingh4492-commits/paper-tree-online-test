import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

async function ensureMistakesTable(): Promise<void> {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS student_mistakes (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      student_id UUID NOT NULL,
      question_id VARCHAR(100) NOT NULL,
      test_id UUID NOT NULL,
      attempt_id TEXT NOT NULL,
      selected_answer TEXT,
      correct_answer TEXT,
      subject VARCHAR(100),
      exam VARCHAR(50),
      chapter_name VARCHAR(255),
      difficulty VARCHAR(20),
      question_text TEXT,
      options JSONB,
      is_resolved BOOLEAN NOT NULL DEFAULT FALSE,
      resolved_at TIMESTAMPTZ,
      attempt_count INTEGER NOT NULL DEFAULT 1,
      first_made TIMESTAMPTZ NOT NULL DEFAULT NOW(),
      last_made TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )
  `);

  await pool.query(`
    CREATE INDEX IF NOT EXISTS idx_student_mistakes_student
    ON student_mistakes(student_id, is_resolved)
  `);

  await pool.query(`
    CREATE INDEX IF NOT EXISTS idx_student_mistakes_resolved
    ON student_mistakes(is_resolved, last_made DESC)
  `);
}

function parseOptions(raw: unknown): string[] {
  try {
    if (Array.isArray(raw)) return raw.map((o) => String(o ?? ""));
    if (typeof raw === "string") {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) return parsed.map((o) => String(o ?? ""));
      if (parsed && typeof parsed === "object")
        return Object.values(parsed).map((o) => String(o ?? ""));
      return [];
    }
    if (raw && typeof raw === "object")
      return Object.values(raw).map((o) => String(o ?? ""));
    return [];
  } catch {
    return [];
  }
}

export async function GET(request: Request): Promise<NextResponse> {
  try {
    const raw = (await cookies()).get("student_session")?.value;
    const session = raw ? parseSessionCookie<Record<string, unknown>>(raw) : null;
    const studentId = String(session?.studentId ?? "").trim();
    const academyId = String(session?.academyId ?? "").trim();

    if (!studentId || !academyId) {
      return NextResponse.json(
        { success: false, error: "Student login required." },
        { status: 401 }
      );
    }

    await ensureMistakesTable();

    const { searchParams } = new URL(request.url);
    const subject = searchParams.get("subject");
    const unresolvedOnly = searchParams.get("unresolved") === "true";
    const limit = Math.min(Math.max(Number(searchParams.get("limit")) || 50, 1), 200);
    const offset = Math.max(Number(searchParams.get("offset")) || 0, 0);

    const backfillConditions: string[] = [
      "ta.is_correct = false",
      "t.student_id::text = $1::text",
      "t.test_id IS NOT NULL",
    ];
    const backfillValues: unknown[] = [studentId];
    let bi = 2;
    if (subject) {
      backfillConditions.push(`q.subject = $${bi}`);
      backfillValues.push(subject);
      bi++;
    }

    const backfillQuery = `
      INSERT INTO student_mistakes (
        student_id, question_id, test_id, attempt_id,
        selected_answer, correct_answer, subject, exam,
        chapter_name, difficulty, question_text, options
      )
      SELECT
        $1,
        ta.question_id,
        t.test_id,
        ta.attempt_id,
        ta.selected_answer::text,
        q.correct_option::text,
        q.subject,
        COALESCE(ts.exam, '') AS exam,
        q.chapter_name,
        q.difficulty,
        q.stem,
        q.options::jsonb
      FROM test_answers ta
      INNER JOIN test_attempts t
        ON ta.attempt_id::text = t.id::text
      INNER JOIN questions q
        ON ta.question_id::text = q.id::text
      LEFT JOIN tests ts
        ON ts.id::text = t.test_id::text
      WHERE ${backfillConditions.join(" AND ")}
        AND NOT EXISTS (
          SELECT 1 FROM student_mistakes sm
          WHERE sm.student_id::text = $1::text
            AND sm.question_id::text = ta.question_id::text
            AND sm.test_id::text = t.test_id::text
            AND sm.attempt_id::text = ta.attempt_id::text
        )
      ON CONFLICT DO NOTHING
    `;

    await pool.query(backfillQuery, backfillValues);

    const conditions: string[] = ["sm.student_id = $1"];
    const values: unknown[] = [studentId];
    let ci = 2;

    if (unresolvedOnly) {
      conditions.push(`sm.is_resolved = false`);
    }

    if (subject) {
      conditions.push(`sm.subject = $${ci}`);
      values.push(subject);
      ci++;
    }

    const countConditions: string[] = ["sm.student_id = $1"];
    const countValues: unknown[] = [studentId];
    if (subject) {
      countConditions.push(`sm.subject = $${countValues.length + 1}`);
      countValues.push(subject);
    }

    const query = `
      SELECT
        id, student_id, question_id, test_id, attempt_id,
        selected_answer, correct_answer, subject, exam,
        chapter_name, difficulty, question_text, options,
        is_resolved, resolved_at, attempt_count,
        first_made, last_made
      FROM student_mistakes sm
      WHERE ${conditions.join(" AND ")}
      ORDER BY sm.last_made DESC
      LIMIT $${ci} OFFSET $${ci + 1}
    `;

    values.push(limit, offset);

    const result = await pool.query(query, values);

    const countResult = await pool.query(
      `
      SELECT
        COUNT(*) FILTER (WHERE is_resolved = false) AS unresolved_count,
        COUNT(*) AS total_count
      FROM student_mistakes sm
      WHERE ${countConditions.join(" AND ")}
      `,
      countValues
    );

    const mistakes = result.rows.map((row) => {
      const options = parseOptions(row.options);

      let selectedIndex: number | null = null;
      let correctIndex: number | null = null;

      if (row.selected_answer != null) {
        const s = String(row.selected_answer).trim();
        if (/^[A-F]$/i.test(s)) {
          selectedIndex = s.toUpperCase().charCodeAt(0) - 65;
        } else {
          const n = Number(s);
          if (!Number.isNaN(n)) selectedIndex = n;
        }
      }

      if (row.correct_answer != null) {
        const c = String(row.correct_answer).trim();
        if (/^[A-F]$/i.test(c)) {
          correctIndex = c.toUpperCase().charCodeAt(0) - 65;
        }
      }

      return {
        mistakeId: String(row.id),
        questionId: String(row.question_id),
        testId: String(row.test_id),
        attemptId: String(row.attempt_id),
        subject: String(row.subject || ""),
        exam: String(row.exam || ""),
        chapter: String(row.chapter_name || ""),
        difficulty: String(row.difficulty || ""),
        stem: String(row.question_text || ""),
        options,
        selectedAnswer: row.selected_answer ?? "",
        correctAnswer: row.correct_answer ?? "",
        selectedIndex,
        correctIndex,
        isResolved: Boolean(row.is_resolved),
        resolvedAt: row.resolved_at,
        attemptCount: Number(row.attempt_count ?? 1),
        firstMade: row.first_made,
        lastMade: row.last_made,
      };
    });

    return NextResponse.json({
      success: true,
      mistakes,
      stats: {
        total: Number(countResult.rows[0]?.total_count ?? 0),
        unresolved: Number(countResult.rows[0]?.unresolved_count ?? 0),
      },
      limit,
      offset,
    });
  } catch (error) {
    console.error("STUDENT MISTAKES ERROR:", error);
    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error ? error.message : "Could not load mistakes.",
      },
      { status: 500 }
    );
  }
}