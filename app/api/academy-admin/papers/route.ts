import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";

async function getAcademyAdmin() {
  const cookieStore = await cookies();
  const session = cookieStore.get("master_session");

  if (!session) return null;

  try {
    const data = JSON.parse(session.value);

    if (data.role !== "ACADEMY_ADMIN" || !data.academyId) {
      return null;
    }

    return data;
  } catch {
    return null;
  }
}

export async function GET() {
  try {
    const admin = await getAcademyAdmin();

    if (!admin) {
      return NextResponse.json(
        { error: "Unauthorized" },
        { status: 401 }
      );
    }

    const result = await pool.query(
      `
      SELECT
        id,
        code,
        exam,
        description,
        duration_minutes,
        created_by,
        created_at,
        updated_at,
        status,
        custom_section
      FROM papers
      WHERE academy_id = $1
      ORDER BY created_at DESC
      `,
      [admin.academyId]
    );

    return NextResponse.json({
      success: true,
      papers: result.rows,
    });
  } catch (error) {
    console.error("ACADEMY PAPERS ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error: "Failed to load academy papers.",
      },
      { status: 500 }
    );
  }
}
