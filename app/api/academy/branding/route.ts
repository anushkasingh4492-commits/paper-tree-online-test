import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export async function GET(req: Request) {
  try {
    const cookieStore = await cookies();

    /*
     * ---------------------------------------------------------
     * 1. Try authenticated academy session first
     * ---------------------------------------------------------
     */

    let academyId: string | null = null;

    const studentCookie =
      cookieStore.get("student_session")?.value;

    if (studentCookie) {
      const session =
        parseSessionCookie<Record<string, unknown>>(
          studentCookie
        );

      if (session?.academyId) {
        academyId = String(
          session.academyId
        );
      }
    }

    /*
     * Teacher / Academy Admin / Master Admin
     */

    if (!academyId) {
      const masterCookie =
        cookieStore.get("master_session")?.value;

      if (masterCookie) {
        const session =
          parseSessionCookie<Record<string, unknown>>(
            masterCookie
          );

        if (session?.academyId) {
          academyId = String(
            session.academyId
          );
        }
      }
    }

    /*
     * ---------------------------------------------------------
     * 2. If not logged in, identify academy from subdomain/domain
     * ---------------------------------------------------------
     */

    if (!academyId) {
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
          .toLowerCase();

      /*
       * Find academy whose configured domain matches
       * the current hostname.
       */
      const domainResult =
        await pool.query(
          `
          SELECT id
          FROM academies
          WHERE LOWER(domain) = LOWER($1)
          LIMIT 1
          `,
          [hostname]
        );

      if (domainResult.rows.length) {
        academyId = String(
          domainResult.rows[0].id
        );
      }
    }

    /*
     * ---------------------------------------------------------
     * 3. If academy still isn't known
     * ---------------------------------------------------------
     */

    if (!academyId) {
      return NextResponse.json({
        success: true,
        academy: {
          name: "Paper Tree",
          logo_data: null,
          subtitle:
            "COMPUTER BASED TESTING",
        },
      });
    }

    /*
     * ---------------------------------------------------------
     * 4. Load academy branding
     * ---------------------------------------------------------
     */

    const result =
      await pool.query(
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

    if (!result.rows.length) {
      return NextResponse.json({
        success: true,
        academy: {
          name: "Paper Tree",
          logo_data: null,
          subtitle:
            "COMPUTER BASED TESTING",
        },
      });
    }

    const academy =
      result.rows[0];

    return NextResponse.json({
      success: true,
      academy: {
        id: academy.id,
        name:
          academy.name ||
          "Paper Tree",
        logo_data:
          academy.logo_data ||
          null,
        domain:
          academy.domain ||
          null,
        subtitle:
          "COMPUTER BASED TESTING",
      },
    });
  } catch (error) {
    console.error(
      "ACADEMY BRANDING ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        academy: {
          name: "Paper Tree",
          logo_data: null,
          subtitle:
            "COMPUTER BASED TESTING",
        },
      },
      { status: 200 }
    );
  }
}