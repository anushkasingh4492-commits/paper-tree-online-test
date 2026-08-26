import { NextResponse } from "next/server";
import { Pool } from "pg";

export const dynamic = "force-dynamic";

declare global {
  // eslint-disable-next-line no-var
  var __paperTreePool: Pool | undefined;
}

function getPool() {
  if (!process.env.DATABASE_URL) {
    throw new Error("DATABASE_URL is not configured.");
  }

  if (!global.__paperTreePool) {
    global.__paperTreePool = new Pool({
      connectionString: process.env.DATABASE_URL,
      ssl: {
        rejectUnauthorized: false,
      },
      max: 10,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 10000,
    });
  }

  return global.__paperTreePool;
}

export async function GET() {
  try {
    const pool = getPool();

    await pool.query(`
      ALTER TABLE test_attempts
      ALTER COLUMN scheduled_test_id DROP NOT NULL;
    `);

    return NextResponse.json({
      success: true,
      message:
        "scheduled_test_id is now nullable.",
    });
  } catch (error) {
    console.error(
      "FIX TEST ATTEMPTS ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to update database.",
      },
      { status: 500 }
    );
  }
}