import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";

export async function GET() {
  const cookieStore = await cookies();
  const masterValue = cookieStore.get("master_session")?.value;
  const studentValue = cookieStore.get("student_session")?.value;
  let academyId = "";

  if (studentValue) {
    const session = parseSessionCookie<Record<string, unknown>>(studentValue);
    academyId = String(session?.academyId || "");
  } else if (masterValue) {
    const session = parseSessionCookie<Record<string, unknown>>(masterValue);
    academyId = String(session?.academyId || "");
  }

  if (!academyId) return NextResponse.json({ success: false, error: "Academy session required." }, { status: 401 });

  try {
    await pool.query("ALTER TABLE academies ADD COLUMN IF NOT EXISTS logo_data TEXT");
    const result = await pool.query("SELECT id, name, code, logo_data FROM academies WHERE id = $1 LIMIT 1", [academyId]);
    if (!result.rowCount) return NextResponse.json({ success: false, error: "Academy not found." }, { status: 404 });
    return NextResponse.json({ success: true, academy: result.rows[0] });
  } catch (error) {
    console.error("ACADEMY BRANDING ERROR:", error);
    return NextResponse.json({ success: false, error: "Could not load academy branding." }, { status: 500 });
  }
}
