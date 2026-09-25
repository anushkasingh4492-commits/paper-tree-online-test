import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export async function GET(req: Request) {
  try {
    const url = new URL(req.url);

    const forwardedHost =
      req.headers.get("x-forwarded-host");

    const host =
      forwardedHost ||
      req.headers.get("host") ||
      url.host;

    const hostname =
      host
        .split(":")[0]
        .trim()
        .toLowerCase();

    console.log(
      "ACADEMY BRANDING HOST:",
      hostname
    );

    /*
     * 1. DOMAIN FIRST
     *
     * Example:
     * web.infinityclasses.net
     *       ↓
     * academies.domain
     *       ↓
     * Infinity Classes
     */
    const domainResult = await pool.query(
      `
      SELECT
        id,
        name,
        logo_data,
        domain
      FROM academies
      WHERE LOWER(TRIM(domain)) = LOWER($1)
      LIMIT 1
      `,
      [hostname]
    );

    if (domainResult.rows.length) {
      const academy = domainResult.rows[0];

      console.log(
        "ACADEMY BRANDING FOUND BY DOMAIN:",
        academy.name,
        academy.domain
      );

      return NextResponse.json({
        success: true,
        academy: {
          id: academy.id,
          name: academy.name || "Paper Tree",
          logo_data: academy.logo_data || null,
          domain: academy.domain || null,
          subtitle: "COMPUTER BASED TESTING",
        },
      });
    }

    /*
     * 2. If domain isn't configured,
     *    try logged-in session.
     */
    const cookieStore = await cookies();

    let academyId: string | null = null;

    const studentCookie =
      cookieStore.get("student_session")?.value;

    if (studentCookie) {
      const session =
        parseSessionCookie<Record<string, unknown>>(
          studentCookie
        );

      if (session?.academyId) {
        academyId = String(session.academyId);
      }
    }

    if (!academyId) {
      const masterCookie =
        cookieStore.get("master_session")?.value;

      if (masterCookie) {
        const session =
          parseSessionCookie<Record<string, unknown>>(
            masterCookie
          );

        if (session?.academyId) {
          academyId = String(session.academyId);
        }
      }
    }

    /*
     * 3. Session fallback
     */
    if (academyId) {
      const result = await pool.query(
        `
        SELECT
          id,
          name,
          logo_data,
          domain
        FROM academies
        WHERE id = $1
        LIMIT 1
        `,
        [academyId]
      );

      if (result.rows.length) {
        const academy = result.rows[0];

        return NextResponse.json({
          success: true,
          academy: {
            id: academy.id,
            name: academy.name || "Paper Tree",
            logo_data: academy.logo_data || null,
            domain: academy.domain || null,
            subtitle: "COMPUTER BASED TESTING",
          },
        });
      }
    }

    /*
     * 4. Final fallback
     */
    return NextResponse.json({
      success: true,
      academy: {
        name: "Paper Tree",
        logo_data: null,
        subtitle: "COMPUTER BASED TESTING",
      },
    });
  } catch (error) {
    console.error(
      "ACADEMY BRANDING ERROR:",
      error
    );

    return NextResponse.json({
      success: false,
      academy: {
        name: "Paper Tree",
        logo_data: null,
        subtitle: "COMPUTER BASED TESTING",
      },
    });
  }
}