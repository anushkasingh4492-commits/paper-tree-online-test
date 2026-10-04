import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { randomUUID } from "crypto";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";
import { ensureFeatureSchema } from "@/lib/feature-schema";
import { getAcademySubscription } from "@/lib/subscription";

export const runtime = "nodejs";

export async function POST(request: Request) {
  try {
    await ensureFeatureSchema();
    const raw = (await cookies()).get("master_session")?.value;
    const session = raw ? parseSessionCookie<Record<string, unknown>>(raw) : null;
    if (session?.role !== "TEACHER" || !session.id) return NextResponse.json({ success: false, error: "Teacher login required." }, { status: 401 });

    const teacher = (await pool.query(`SELECT id, academy_id FROM teachers WHERE id = $1 LIMIT 1`, [session.id])).rows[0];
    if (!teacher?.academy_id) return NextResponse.json({ success: false, error: "Teacher academy not found." }, { status: 403 });

    const subscription = await getAcademySubscription(String(teacher.academy_id));
    if (!subscription.features.customQuestions) {
      return NextResponse.json({ success: false, error: "Custom question creation is not available for this academy." }, { status: 403 });
    }

    const body = await request.json();
    const stem = String(body.stem || "").trim();
    const options = Array.isArray(body.options) ? body.options.map((v: unknown) => String(v).trim()).filter(Boolean) : [];
    const correctOption = String(body.correctOption ?? "").trim().toUpperCase();
    if (!stem || options.length < 2 || !correctOption) return NextResponse.json({ success: false, error: "Question, at least two options and the correct option are required." }, { status: 400 });
    const index = correctOption.length === 1 ? correctOption.charCodeAt(0) - 65 : Number(correctOption);
    if (!Number.isInteger(index) || index < 0 || index >= options.length) return NextResponse.json({ success: false, error: "Correct option is invalid." }, { status: 400 });

    const id = `CUSTOM-${randomUUID()}`;
    const standard = Number(body.standard) || 12;
    await pool.query(
      `INSERT INTO questions (
        id, exam, subject, standard, chapter_number, chapter_name, major_topic, subtopic,
        concept_tested, stem, options, correct_option, correct_answer_text, solution,
        formula_principle, common_misconception, difficulty, estimated_time, question_type,
        generator_eligible_strict_cet, generator_eligible_extended_revision, academy_id, created_by_teacher_id, raw_data
      ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11::jsonb,$12,$13,$14,$15,$16,$17,$18,$19,false,true,$20,$21,$22::jsonb)`,
      [
        id,
        String(body.exam || "MHT-CET"),
        String(body.subject || "General"),
        standard,
        Number(body.chapterNumber) || 0,
        String(body.chapterName || "Custom Questions"),
        String(body.majorTopic || "") || null,
        String(body.subtopic || "") || null,
        String(body.conceptTested || "") || null,
        stem,
        JSON.stringify(options),
        String.fromCharCode(65 + index),
        options[index],
        String(body.solution || "") || null,
        String(body.formulaPrinciple || "") || null,
        String(body.commonMisconception || "") || null,
        String(body.difficulty || "Medium"),
        String(body.estimatedTime || "1-2 minutes"),
        "Teacher Created",
        teacher.academy_id,
        teacher.id,
        JSON.stringify({ source: "teacher", academyId: teacher.academy_id }),
      ]
    );
    const created = await pool.query(
      `
      SELECT
        id, exam, subject, standard, chapter_number, chapter_name,
        stem, options, correct_option, correct_answer_text, solution,
        difficulty, estimated_time, question_type, figure_asset
      FROM questions
      WHERE id = $1
      LIMIT 1
      `,
      [id]
    );

    return NextResponse.json({
      success: true,
      questionId: id,
      question: created.rows[0] || null,
    });
  } catch (error) {
    console.error("CREATE CUSTOM QUESTION ERROR", error);
    return NextResponse.json({ success: false, error: error instanceof Error ? error.message : "Could not create question." }, { status: 500 });
  }
}
