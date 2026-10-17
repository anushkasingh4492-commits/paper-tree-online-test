
import { NextResponse } from "next/server";
import { pool } from "@/lib/db";
import {
  apiError,
  getCollaborativeTeacher,
} from "@/lib/collaborative-papers";

export const runtime = "nodejs";

export async function GET() {
  try {
    const teacher = await getCollaborativeTeacher();

    if (!teacher) {
      return apiError("Teacher login required.", 401);
    }

    const result = await pool.query(
      `SELECT id::text AS id, name, email
       FROM teachers
       WHERE LOWER(TRIM(academy_id::text)) =
             LOWER(TRIM($1::text))
         AND id::text <> $2::text
       ORDER BY name`,
      [teacher.academy_id, teacher.id],
    );

    return NextResponse.json({
      success: true,
      teachers: result.rows,
    });
  } catch (error) {
    console.error("Collaborative teachers lookup failed:", error);
    return apiError("Could not load academy professors.", 500);
  }
}
