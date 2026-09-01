import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import crypto from "crypto";

export const runtime = "nodejs";

export async function POST(request: Request) {
  try {
    const cookieStore = await cookies();
    const sessionCookie =
      cookieStore.get("master_session")?.value;

    if (!sessionCookie) {
      return NextResponse.json(
        {
          success: false,
          error: "Admin is not logged in.",
        },
        { status: 401 }
      );
    }

    let session: { id?: string; role?: string };

    try {
      session = JSON.parse(sessionCookie);
    } catch {
      return NextResponse.json(
        {
          success: false,
          error: "Invalid admin session.",
        },
        { status: 401 }
      );
    }

    if (session.role !== "ADMIN") {
      return NextResponse.json(
        {
          success: false,
          error: "Admin access required.",
        },
        { status: 403 }
      );
    }

    const dataset = await request.json();

    if (
      !dataset ||
      !Array.isArray(dataset.records)
    ) {
      return NextResponse.json(
        {
          success: false,
          error: 'Dataset must contain a "records" array.',
        },
        { status: 400 }
      );
    }

    let inserted = 0;

    for (const record of dataset.records) {
      if (!record || typeof record !== "object") {
        continue;
      }

      if (!record.stem) {
        continue;
      }

      const id = crypto.randomUUID();

      await pool.query(
        `
        INSERT INTO questions (
          id,
          exam,
          subject,
          standard,
          chapter_number,
          chapter_name,
          major_topic,
          subtopic,
          concept_tested,
          stem,
          options,
          correct_option,
          correct_answer_text,
          solution,
          formula_principle,
          difficulty,
          estimated_time,
          question_type,
          figure_asset
        )
        VALUES (
          $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,
          $11,$12,$13,$14,$15,$16,$17,$18,$19
        )
        `,
        [
          id,
          dataset.exam || record.exam || "",
          dataset.subject || record.subject || "",
          record.standard ?? null,
          record.chapter_number ?? null,
          record.chapter_name ?? "",
          record.major_topic ?? "",
          record.subtopic ?? "",
          record.concept_tested ?? "",
          record.stem,
          JSON.stringify(record.options ?? []),
          record.correct_option ?? "",
          record.correct_answer_text ?? "",
          record.solution ?? "",
          record.formula_principle ?? "",
          record.difficulty ?? "Medium",
          record.estimated_time ?? "",
          record.question_type ?? "MCQ",
          record.figure_asset ?? "",
        ]
      );

      inserted++;
    }

    return NextResponse.json({
      success: true,
      inserted,
    });
  } catch (error) {
    console.error("DATASET UPLOAD ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Dataset upload failed.",
      },
      { status: 500 }
    );
  }
}
