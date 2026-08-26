import { NextResponse } from "next/server";
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false,
  },
});

export async function GET() {
  try {
    /*
     * ---------------------------------------------------------
     * GET SUBJECTS + CHAPTERS FROM DATABASE
     * ---------------------------------------------------------
     */

    const result = await pool.query(`
      SELECT DISTINCT
        subject,
        chapter_name
      FROM questions
      WHERE
        subject IS NOT NULL
        AND TRIM(subject) <> ''
        AND chapter_name IS NOT NULL
        AND TRIM(chapter_name) <> ''
      ORDER BY
        subject,
        chapter_name;
    `);

    /*
     * ---------------------------------------------------------
     * FORMAT DATABASE DATA
     * ---------------------------------------------------------
     */

    const chapters = result.rows
      .map((row) => ({
        subject: String(row.subject).trim(),
        chapter: String(row.chapter_name).trim(),
      }))
      .filter(
        (item) =>
          item.subject &&
          item.chapter
      );

    /*
     * ---------------------------------------------------------
     * GET UNIQUE SUBJECTS
     * ---------------------------------------------------------
     */

    const subjects = Array.from(
      new Set(
        chapters.map(
          (item) => item.subject
        )
      )
    );

    /*
     * ---------------------------------------------------------
     * GET DIFFICULTIES
     * ---------------------------------------------------------
     */

    const difficultyResult =
      await pool.query(`
        SELECT DISTINCT difficulty
        FROM questions
        WHERE
          difficulty IS NOT NULL
          AND TRIM(difficulty) <> ''
        ORDER BY difficulty;
      `);

    const difficulties =
      difficultyResult.rows
        .map((row) =>
          String(row.difficulty).trim()
        )
        .filter(Boolean);

    /*
     * ---------------------------------------------------------
     * SUCCESS
     * ---------------------------------------------------------
     */

    return NextResponse.json({
      success: true,

      subjects,

      chapters,

      difficulties,
    });
  } catch (error) {
    console.error(
      "DB SCHEMA ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : String(error),
      },
      {
        status: 500,
      }
    );
  }
}