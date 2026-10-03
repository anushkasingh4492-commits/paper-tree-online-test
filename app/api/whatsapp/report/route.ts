import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";
import { ensureFeatureSchema } from "@/lib/feature-schema";
import { getAcademySubscription } from "@/lib/subscription";

export const runtime = "nodejs";

export async function POST(request: Request) {
  try {
    await ensureFeatureSchema();
    const body = await request.json();
    const studentId = String(body.studentId || "").trim();
    if (!studentId) return NextResponse.json({ success: false, error: "Student is required." }, { status: 400 });

    const sessionRaw = (await cookies()).get("master_session")?.value;
    const session = sessionRaw ? parseSessionCookie<Record<string, unknown>>(sessionRaw) : null;
    if (!session || !["TEACHER", "ACADEMY_ADMIN", "ADMIN", "MASTER_ADMIN"].includes(String(session.role))) {
      return NextResponse.json({ success: false, error: "Staff login required." }, { status: 401 });
    }

    const student = (await pool.query(`SELECT id, name, parent_name, parent_phone, academy_id FROM students WHERE id = $1 LIMIT 1`, [studentId])).rows[0];
    if (!student) return NextResponse.json({ success: false, error: "Student not found." }, { status: 404 });
    if (session.academyId && String(student.academy_id) !== String(session.academyId)) return NextResponse.json({ success: false, error: "Student is outside your academy." }, { status: 403 });

    const subscription = await getAcademySubscription(String(student.academy_id));
    if (!subscription.features.parentWhatsAppReports) {
      return NextResponse.json({ success: false, error: "WhatsApp parent reports are not available for this academy." }, { status: 403 });
    }

    const summaryResponse = await fetch(new URL(`/api/ai/parent-summary?studentId=${encodeURIComponent(studentId)}`, request.url), {
      headers: { cookie: request.headers.get("cookie") || "" },
    });
    const summaryData = await summaryResponse.json();
    if (!summaryResponse.ok || !summaryData.success) throw new Error(summaryData.error || "Could not create report.");

    const badgesLine = summaryData.badgesThisMonth?.length ? `\n\n🏆 Badges this month: ${summaryData.badgesThisMonth.join(", ")}` : "";
    const levelLine = summaryData.level ? `\n🎮 Level ${summaryData.level.number} — ${summaryData.level.name}\n🔥 ${summaryData.level.streak} day streak` : "";
    const message = `*${student.name} — Performance Update*${levelLine}\n\n${summaryData.summary}${badgesLine}\n\n— ${student.parent_name ? `For ${student.parent_name}` : "Parent update"}`;
    const phone = String(student.parent_phone || "").replace(/\D/g, "");
    const clickToChat = phone ? `https://wa.me/${phone}?text=${encodeURIComponent(message)}` : `https://wa.me/?text=${encodeURIComponent(message)}`;

    let sent = false;
    if (process.env.WHATSAPP_ACCESS_TOKEN && process.env.WHATSAPP_PHONE_NUMBER_ID && phone) {
      const response = await fetch(`https://graph.facebook.com/v22.0/${process.env.WHATSAPP_PHONE_NUMBER_ID}/messages`, {
        method: "POST",
        headers: { Authorization: `Bearer ${process.env.WHATSAPP_ACCESS_TOKEN}`, "Content-Type": "application/json" },
        body: JSON.stringify({ messaging_product: "whatsapp", to: phone, type: "text", text: { body: message } }),
      });
      sent = response.ok;
      if (!sent) console.error("WhatsApp provider error", await response.text());
    }

    return NextResponse.json({ success: true, sent, phoneConfigured: Boolean(phone), message, clickToChat });
  } catch (error) {
    console.error("WHATSAPP REPORT ERROR", error);
    return NextResponse.json({ success: false, error: error instanceof Error ? error.message : "Could not create WhatsApp report." }, { status: 500 });
  }
}
