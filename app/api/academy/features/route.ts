import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { parseSessionCookie } from "@/lib/session";
import { getAcademyTier, hasTierFeature, type TierFeature } from "@/lib/subscription";

const FEATURES: TierFeature[] = [
  "AI_PERFORMANCE_SUMMARIES",
  "AUTO_GENERATED_PAPERS",
  "COMPLETE_STUDENT_REPORTS",
  "TIME_PER_QUESTION",
  "AI_WEAK_AREA_TESTS",
  "BRANDED_APP",
  "CUSTOM_QUESTIONS",
  "WHATSAPP_PARENT_REPORTS",
];

export async function GET() {
  const cookieStore = await cookies();
  const student = cookieStore.get("student_session")?.value;
  const staff = cookieStore.get("master_session")?.value;

  let academyId = "";
  if (student) {
    const session = parseSessionCookie<Record<string, unknown>>(student);
    academyId = String(session?.academyId ?? "").trim();
  }
  if (!academyId && staff) {
    const session = parseSessionCookie<Record<string, unknown>>(staff);
    academyId = String(session?.academyId ?? "").trim();
  }

  if (!academyId) {
    return NextResponse.json(
      { success: false, error: "Academy session not found." },
      { status: 401 }
    );
  }

  try {
    const tier = await getAcademyTier(academyId);
    const features = Object.fromEntries(
      FEATURES.map((feature) => [feature, hasTierFeature(tier, feature)])
    );

    return NextResponse.json({ success: true, features });
  } catch (error) {
    console.error("ACADEMY FEATURES ERROR", error);
    return NextResponse.json(
      { success: false, error: "Could not load academy features." },
      { status: 500 }
    );
  }
}
