import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { randomUUID } from "crypto";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";
import { ensureFeatureSchema } from "@/lib/feature-schema";
import { getAcademySubscription } from "@/lib/subscription";

export const runtime = "nodejs";

export async function POST() {
  try {
    await ensureFeatureSchema();
    const raw = (await cookies()).get("student_session")?.value;
    const session = raw ? parseSessionCookie<Record<string, unknown>>(raw) : null;
    const studentId = String(session?.studentId ?? "").trim();
    const academyId = String(session?.academyId ?? "").trim();
    if (!studentId || !academyId) return NextResponse.json({ success: false, error: "Student login required." }, { status: 401 });

    const subscription = await getAcademySubscription(academyId);
    if (!subscription.features.personalizedWeakAreaTests) {
      return NextResponse.json({ success: false, error: "This personalised revision feature is not available for this academy." }, { status: 403 });
    }

    const examResult = await pool.query(`SELECT t.exam FROM test_attempts ta LEFT JOIN tests t ON t.id = COALESCE(ta.test_id, ta.scheduled_test_id) WHERE ta.student_id = $1 ORDER BY COALESCE(ta.submitted_at, ta.started_at, ta.created_at) DESC LIMIT 1`, [studentId]);
    const exam = String(examResult.rows[0]?.exam || "MHT-CET");

    const weak = await pool.query(
      `SELECT q.chapter_name, q.subject,
              COUNT(*) FILTER (WHERE ta.is_correct = false OR ta.selected_answer IS NULL)::int AS misses,
              COUNT(*)::int AS total
       FROM test_answers ta
       INNER JOIN test_attempts att ON att.id = ta.attempt_id
       INNER JOIN questions q ON q.id = ta.question_id
       WHERE att.student_id = $1
       GROUP BY q.chapter_name, q.subject
       HAVING COUNT(*) >= 2
       ORDER BY (COUNT(*) FILTER (WHERE ta.is_correct = false OR ta.selected_answer IS NULL)::numeric / COUNT(*)::numeric) DESC
       LIMIT 5`,
      [studentId]
    );

    const weakChapters = weak.rows.map((row) => String(row.chapter_name)).filter(Boolean);
    const selectFields = `id, exam, subject, standard, chapter_number, chapter_name, major_topic, subtopic, stem, options, correct_option, correct_answer_text, solution, difficulty, figure_asset`;
    const chapterCondition = weakChapters.length ? ` AND chapter_name = ANY($2::varchar[])` : "";
    const chapterValues: unknown[] = weakChapters.length ? [exam, weakChapters] : [exam];

    // The generator prioritises questions this student has never seen before.
    let questionResult = await pool.query(
      `SELECT ${selectFields}
       FROM questions q
       WHERE q.exam = $1${chapterCondition}
         AND NOT EXISTS (
           SELECT 1 FROM test_answers seen_answer
           INNER JOIN test_attempts seen_attempt ON seen_attempt.id = seen_answer.attempt_id
           WHERE seen_attempt.student_id = $${chapterValues.length + 1}
             AND seen_answer.question_id = q.id
         )
       ORDER BY random() LIMIT 20`,
      [...chapterValues, studentId]
    );

    if (questionResult.rows.length < 20) {
      const remaining = 20 - questionResult.rows.length;
      const seenQuery = `SELECT ${selectFields}
       FROM questions q
       WHERE q.exam = $1${chapterCondition}
       ORDER BY random() LIMIT $${chapterValues.length + 1}`;
      const seenResult = await pool.query(seenQuery, [...chapterValues, remaining]);
      const existing = new Set(questionResult.rows.map((q) => String(q.id)));
      questionResult.rows.push(...seenResult.rows.filter((q) => !existing.has(String(q.id))));
    }

    if (questionResult.rows.length < 10) {
      questionResult = await pool.query(
        `SELECT ${selectFields}
         FROM questions q
         WHERE q.exam = $1
         ORDER BY random() LIMIT 20`,
        [exam]
      );
    }

    if (!questionResult.rows.length) return NextResponse.json({ success: false, error: "There are not enough questions to create a revision test yet." }, { status: 400 });

    const testId = randomUUID();
    const questions = questionResult.rows.map((q, index) => ({
      id: String(q.id), number: index + 1, question: q.stem, options: q.options,
      answer: q.correct_option, correct_option: q.correct_option,
      subject: q.subject, chapter: q.chapter_name, chapter_name: q.chapter_name,
      difficulty: q.difficulty, solution: q.solution, figureAsset: q.figure_asset,
    }));

    await pool.query(
      `INSERT INTO tests (id, exam, question_count, questions, created_at, difficulty, academy_id)
       VALUES ($1, $2, $3, $4::jsonb, NOW(), $5, $6)`,
      [testId, exam, questions.length, JSON.stringify(questions), "Mixed", academyId]
    );

    await pool.query(
      `INSERT INTO student_tests (id, student_id, test_id)
       VALUES ($1, $2, $3)
       ON CONFLICT (student_id, test_id) DO NOTHING`,
      [`student-test-${Date.now()}-${randomUUID().slice(0, 8)}`, studentId, testId]
    );

    return NextResponse.json({ success: true, testId, questionCount: questions.length, weakChapters });
  } catch (error) {
    console.error("REVISION TEST ERROR", error);
    return NextResponse.json({ success: false, error: error instanceof Error ? error.message : "Could not create revision test." }, { status: 500 });
  }
}
