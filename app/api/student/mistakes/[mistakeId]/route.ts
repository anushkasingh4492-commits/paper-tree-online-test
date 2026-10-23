import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function DELETE(
  request: Request,
  { params }: { params: Promise<{ mistakeId: string }> }
): Promise<NextResponse> {
  try {
    const raw = (await cookies()).get("student_session")?.value;
    const session = raw ? parseSessionCookie<Record<string, unknown>>(raw) : null;
    const studentId = String(session?.studentId ?? "").trim();
    const academyId = String(session?.academyId ?? "").trim();

    if (!studentId || !academyId) {
      return NextResponse.json(
        { success: false, error: "Student login required." },
        { status: 401 }
      );
    }

    const { mistakeId } = await params;

    if (!mistakeId) {
      return NextResponse.json(
        { success: false, error: "Mistake ID is required." },
        { status: 400 }
      );
    }

    const result = await pool.query(
      `
      UPDATE student_mistakes
      SET is_resolved = true, resolved_at = NOW()
      WHERE id = $1 AND student_id = $2 AND is_resolved = false
      RETURNING id
      `,
      [mistakeId, studentId]
    );

    if (result.rowCount === 0) {
      return NextResponse.json(
        { success: false, error: "Mistake not found or already resolved." },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      message: "Mistake marked as resolved.",
      mistakeId,
    });
  } catch (error) {
    console.error("DELETE MISTAKE ERROR:", error);
    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error ? error.message : "Could not resolve mistake.",
      },
      { status: 500 }
    );
  }
}
