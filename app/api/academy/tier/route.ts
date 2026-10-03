import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { parseSessionCookie } from "@/lib/session";
import { getAcademySubscription } from "@/lib/subscription";

export const runtime = "nodejs";

export async function GET() {
  try {
    const cookieStore = await cookies();
    const studentRaw = cookieStore.get("student_session")?.value;
    const masterRaw = cookieStore.get("master_session")?.value;

    const student = studentRaw
      ? parseSessionCookie<Record<string, unknown>>(studentRaw)
      : null;
    const master = masterRaw
      ? parseSessionCookie<Record<string, unknown>>(masterRaw)
      : null;

    const academyId = String(
      student?.academyId ?? master?.academyId ?? ""
    ).trim();

    if (!academyId) {
      return NextResponse.json(
        { success: false, error: "Academy session required." },
        { status: 401 }
      );
    }

    const subscription = await getAcademySubscription(academyId);

    // Deliberately do not expose the tier name to students or teachers.
    return NextResponse.json({
      success: true,
      features: subscription.features,
      limits: {
        selfTestsPerStudentPerMonth: subscription.limits.selfTestsPerStudentPerMonth,
      },
    });
  } catch (error) {
    console.error("ACADEMY TIER ERROR", error);
    return NextResponse.json(
      { success: false, error: "Could not load academy features." },
      { status: 500 }
    );
  }
}
