import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

export async function GET() {
  try {
    const cookieStore = await cookies();
    const sessionCookie =
      cookieStore.get("master_session")?.value;

    if (!sessionCookie) {
      return NextResponse.json(
        { success: false, error: "Unauthorized" },
        { status: 401 }
      );
    }

    let session: {
      role?: string;
      academyId?: string;
    };

    try {
      session = JSON.parse(sessionCookie);
    } catch {
      return NextResponse.json(
        { success: false, error: "Invalid session." },
        { status: 401 }
      );
    }

    if (session.role !== "TEACHER" || !session.academyId) {
      return NextResponse.json(
        { success: false, error: "Teacher access required." },
        { status: 403 }
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
      [session.academyId]
    );

    return NextResponse.json({
      success: true,
      papers: result.rows,
    });
  } catch (error) {
    console.error("TEACHER PAPERS ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to load papers.",
      },
      { status: 500 }
    );
  }
}