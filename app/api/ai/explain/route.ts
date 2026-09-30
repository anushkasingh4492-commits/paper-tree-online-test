import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { parseSessionCookie } from "@/lib/session";
import { pool } from "@/lib/db";
import { ensureFeatureSchema } from "@/lib/feature-schema";

export const runtime = "nodejs";

function clean(value: unknown, max = 5000) {
  return String(value ?? "").slice(0, max);
}

export async function POST(request: Request) {
  try {
    await ensureFeatureSchema();
    const sessionRaw = (await cookies()).get("student_session")?.value;
    const session = sessionRaw ? parseSessionCookie<Record<string, unknown>>(sessionRaw) : null;
    if (!session?.studentId) return NextResponse.json({ success: false, error: "Student login required." }, { status: 401 });
    const body = await request.json();
    const questionId = clean(body.questionId, 150);
    let question = body.question;

    if (questionId) {
      const result = await pool.query(
        `SELECT stem, options, correct_option, solution, distractor_rationale, formula_principle, common_misconception, subject, chapter_name
         FROM questions WHERE id = $1 LIMIT 1`,
        [questionId]
      );
      if (result.rows[0]) question = result.rows[0];
    }

    if (!question) return NextResponse.json({ success: false, error: "Question is required." }, { status: 400 });

    const apiKey = process.env.OPENAI_API_KEY;
    const model = process.env.OPENAI_MODEL || "gpt-4o-mini";
    const options = Array.isArray(question.options) ? question.options : question.options;
    const prompt = `You are a patient competitive-exam tutor. Explain this question step by step.
Question: ${clean(question.stem ?? question.question)}
Options: ${clean(JSON.stringify(options))}
Correct option: ${clean(question.correct_option ?? question.answer)}
Student selected: ${clean(body.selectedAnswer)}
Stored solution: ${clean(question.solution, 3000)}
Stored distractor rationale: ${clean(JSON.stringify(question.distractor_rationale), 3000)}
Formula/principle: ${clean(question.formula_principle, 1500)}
Common misconception: ${clean(question.common_misconception, 1500)}

Return concise markdown with exactly these sections:
1. Correct answer
2. Step-by-step reasoning
3. Why the other options are wrong
4. Quick exam tip`;

    if (!apiKey) {
      return NextResponse.json({
        success: true,
        ai: false,
        explanation: question.solution || "AI explanation is not configured yet. Add OPENAI_API_KEY to your local environment to enable the full tutor.",
        tip: question.common_misconception || question.formula_principle || "Review the concept and retry the question without looking at the answer.",
      });
    }

    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${apiKey}` },
      body: JSON.stringify({ model, temperature: 0.2, messages: [{ role: "system", content: "You explain exam questions accurately and never invent missing facts." }, { role: "user", content: prompt }] }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data?.error?.message || "AI provider request failed.");
    return NextResponse.json({ success: true, ai: true, explanation: data?.choices?.[0]?.message?.content || "No explanation returned." });
  } catch (error) {
    console.error("AI EXPLAIN ERROR", error);
    return NextResponse.json({ success: false, error: error instanceof Error ? error.message : "Could not explain this question." }, { status: 500 });
  }
}
