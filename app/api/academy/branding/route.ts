import { NextResponse } from "next/server";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

function getHostname(request: Request) {
  const forwardedHost = request.headers.get("x-forwarded-host");

  if (forwardedHost) {
    return forwardedHost.split(",")[0].trim().split(":")[0].toLowerCase();
  }

  const host = request.headers.get("host");

  if (host) {
    return host.split(":")[0].toLowerCase();
  }

  return "";
}

export async function GET(request: Request) {
  try {
    await pool.query(`
      ALTER TABLE academies
      ADD COLUMN IF NOT EXISTS domain VARCHAR(255)
    `);

    const hostname = getHostname(request);

    if (!hostname) {
      return NextResponse.json({
        success: true,
        academy: null,
      });
    }

    const result = await pool.query(
      `
      SELECT
        id,
        name,
        code,
        domain,
        logo_data
      FROM academies
      WHERE LOWER(domain) = LOWER($1)
      LIMIT 1
      `,
      [hostname]
    );

    if (!result.rowCount) {
      return NextResponse.json({
        success: true,
        academy: null,
      });
    }

    return NextResponse.json({
      success: true,
      academy: result.rows[0],
    });
  } catch (error) {
    console.error("PUBLIC ACADEMY BRANDING ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error: "Could not load academy branding.",
      },
      { status: 500 }
    );
  }
}