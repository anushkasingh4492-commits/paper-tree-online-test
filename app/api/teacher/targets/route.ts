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
        {
          success: false,
          error: "Teacher is not logged in.",
        },
        { status: 401 }
      );
    }

    let session: {
      id?: string;
      role?: string;
      academyId?: string;
    };

    try {
      session = JSON.parse(sessionCookie);
    } catch {
      return NextResponse.json(
        {
          success: false,
          error: "Invalid teacher session.",
        },
        { status: 401 }
      );
    }

    if (
      session.role !== "TEACHER" ||
      !session.academyId
    ) {
      return NextResponse.json(
        {
          success: false,
          error: "Teacher access required.",
        },
        { status: 403 }
      );
    }

    const academyId = String(
      session.academyId
    );

    const [batchesResult, studentsResult] =
      await Promise.all([
        pool.query(
          `
          SELECT
            id,
            name,
            class_name
          FROM batches
          WHERE academy_id = $1
          ORDER BY name
          `,
          [academyId]
        ),

        pool.query(
          `
          SELECT
            id,
            name,
            email,
            roll_number,
            class_name
          FROM students
          WHERE academy_id = $1
          ORDER BY name
          `,
          [academyId]
        ),
      ]);

    return NextResponse.json({
      success: true,
      batches: batchesResult.rows,
      students: studentsResult.rows,
    });
  } catch (error) {
    console.error(
      "TEACHER TARGETS ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          "Failed to load batches and students.",
      },
      { status: 500 }
    );
  }
}
