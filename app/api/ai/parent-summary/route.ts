import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";
import { ensureFeatureSchema } from "@/lib/feature-schema";
import { getStudentGamification } from "@/lib/gamification";
import { getAcademySubscription } from "@/lib/subscription";

export const runtime = "nodejs";

async function getActor(request: Request) {
  const raw = (await cookies()).get("master_session")?.value;
  const staff = raw ? parseSessionCookie<Record<string, unknown>>(raw) : null;
  if (staff?.role) {
    return { studentId: String(new URL(request.url).searchParams.get("studentId") || "").trim(), academyId: String(staff.academyId || "").trim(), staff: true, role: String(staff.role) };
  }
  const studentRaw = (await cookies()).get("student_session")?.value;
  const student = studentRaw ? parseSessionCookie<Record<string, unknown>>(studentRaw) : null;
  return { studentId: String(student?.studentId ?? "").trim(), academyId: String(student?.academyId ?? "").trim(), staff: false, role: "STUDENT" };
}

export async function GET(request: Request) {
  try {
    await ensureFeatureSchema();
    const actor = await getActor(request);
    const studentId = actor.studentId;
    if (!studentId) return NextResponse.json({ success: false, error: "Student is required." }, { status: 400 });
    if (actor.staff && !["TEACHER", "ACADEMY_ADMIN", "ADMIN", "MASTER_ADMIN"].includes(actor.role)) return NextResponse.json({ success: false, error: "Staff login required." }, { status: 401 });

    const studentResult = await pool.query(`SELECT id, name, parent_name, parent_phone, academy_id FROM students WHERE id = $1 LIMIT 1`, [studentId]);
    const student = studentResult.rows[0];
    if (!student) return NextResponse.json({ success: false, error: "Student not found." }, { status: 404 });
    if (actor.staff && actor.academyId && String(student.academy_id) !== actor.academyId) return NextResponse.json({ success: false, error: "Student is outside your academy." }, { status: 403 });

    const subscription = await getAcademySubscription(String(student.academy_id));
    if (!subscription.features.aiPerformanceSummaries) {
      return NextResponse.json({ success: false, error: "AI performance summaries are not available for this academy." }, { status: 403 });
    }

    const game = await getStudentGamification(studentId, String(student.academy_id));
    const monthStart = new Date();
    monthStart.setDate(1);
    monthStart.setHours(0, 0, 0, 0);
    const monthBadges = game.badges.filter((badge) => badge.earned && badge.earnedAt && new Date(badge.earnedAt) >= monthStart).map((badge) => `${badge.name}${badge.tier ? ` ${["I","II","III","IV"][badge.tier - 1]}` : ""}`);

    const result = await pool.query(
      `SELECT ta.score, ta.total_marks, ta.correct_count, ta.incorrect_count, ta.unanswered_count, ta.submitted_at, t.questions
       FROM test_attempts ta
       LEFT JOIN tests t ON t.id = COALESCE(ta.test_id, ta.scheduled_test_id)
       WHERE ta.student_id = $1
       AND LOWER(REPLACE(COALESCE(ta.status,''),'-','_')) IN ('submitted','auto_submitted','auto submitted','completed','complete')
       ORDER BY COALESCE(ta.submitted_at, ta.started_at, ta.created_at) DESC
       LIMIT 8`,
      [studentId]
    );

    const attempts = result.rows;
    const percentages = attempts.map((a) => Number(a.total_marks) > 0 ? (Number(a.score) / Number(a.total_marks)) * 100 : 0);
    const avg = percentages.length ? percentages.reduce((a, b) => a + b, 0) / percentages.length : 0;
    const correct = attempts.reduce((sum, a) => sum + Number(a.correct_count || 0), 0);
    const wrong = attempts.reduce((sum, a) => sum + Number(a.incorrect_count || 0), 0);

    const weak = await pool.query(
      `SELECT q.chapter_name, q.subject, COUNT(*)::int AS total,
              COUNT(*) FILTER (WHERE ta.is_correct = false OR ta.selected_answer IS NULL)::int AS misses
       FROM test_answers ta
       INNER JOIN test_attempts att ON att.id = ta.attempt_id
       INNER JOIN questions q ON q.id = ta.question_id
       WHERE att.student_id = $1
       GROUP BY q.chapter_name, q.subject
       HAVING COUNT(*) >= 2
       ORDER BY (COUNT(*) FILTER (WHERE ta.is_correct = false OR ta.selected_answer IS NULL)::numeric / COUNT(*)::numeric) DESC
       LIMIT 3`,
      [studentId]
    );

    const weakText = weak.rows.map((r) => `${r.chapter_name} (${Math.round(Number(r.misses) / Math.max(1, Number(r.total)) * 100)}% missed)`).join(", ") || "No clear weak chapter yet";
    const facts = `Student: ${student.name}. Current level: ${game.level} ${game.levelName}. Current streak: ${game.streak} days. Badges earned this month: ${monthBadges.join(", ") || "none yet"}. Recent tests: ${attempts.length}. Average score: ${avg.toFixed(1)}%. Correct answers: ${correct}. Wrong answers: ${wrong}. Weak areas: ${weakText}.`;
    const apiKey = process.env.OPENAI_API_KEY;
    let summary = `${student.name} is currently Level ${game.level} ${game.levelName} and has completed ${attempts.length} recent test${attempts.length === 1 ? "" : "s"} with an average score of ${avg.toFixed(1)}%.`;
    summary += ` The main areas needing attention are ${weakText}.`;
    summary += ` The immediate focus should be short daily practice on those chapters followed by a revision test. Current streak: ${game.streak} days${monthBadges.length ? `; badges earned this month: ${monthBadges.join(", ")}` : ""}.`;

    if (apiKey) {
      const response = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${apiKey}` },
        body: JSON.stringify({
          model: process.env.OPENAI_MODEL || "gpt-4o-mini",
          temperature: 0.2,
          messages: [
            { role: "system", content: "Write exactly three plain-English sentences for a parent. Be encouraging but factual. Do not exaggerate." },
            { role: "user", content: facts },
          ],
        }),
      });
      const data = await response.json();
      if (response.ok && data?.choices?.[0]?.message?.content) summary = String(data.choices[0].message.content).trim();
    }

    return NextResponse.json({ success: true, student: { id: student.id, name: student.name, parentName: student.parent_name, parentPhone: student.parent_phone }, level: { number: game.level, name: game.levelName, streak: game.streak }, badgesThisMonth: monthBadges, summary, averagePercentage: Number(avg.toFixed(1)), weakAreas: weak.rows });
  } catch (error) {
    console.error("PARENT SUMMARY ERROR", error);
    return NextResponse.json({ success: false, error: error instanceof Error ? error.message : "Could not create parent summary." }, { status: 500 });
  }
}
