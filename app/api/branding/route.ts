import { NextResponse } from "next/server";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

function getSubdomain(request: Request) {
  const host = request.headers.get("host") || "";

  const hostname = host.split(":")[0].toLowerCase();

  // Local development
  if (
    hostname === "localhost" ||
    hostname === "127.0.0.1"
  ) {
    return null;
  }

  // Vercel preview deployments
  if (hostname.endsWith(".vercel.app")) {
    return null;
  }

  const parts = hostname.split(".");

  /*
   * Expected:
   *
   * web.infinityclasses.net
   * web.xyzacademy.net
   *
   * We use the SECOND subdomain:
   *
   * web.infinityclasses.net
   *     ↓
   * infinityclasses
   */

  if (parts.length < 3) {
    return null;
  }

  // Your structure is:
  // web.<academy>.net
  //
  // So for:
  // web.infinityclasses.net
  //
  // parts = ["web", "infinityclasses", "net"]

  if (parts.length === 3 && parts[0] === "web") {
    return parts[1];
  }

  /*
   * Also support:
   *
   * infinityclasses.yourdomain.com
   *
   * if you ever use that structure.
   */

  if (parts.length >= 3) {
    return parts[0];
  }

  return null;
}

export async function GET(request: Request) {
  try {
    const subdomain = getSubdomain(request);

    /*
     * Root / development portal
     */
    if (!subdomain) {
      return NextResponse.json({
        success: true,
        academy: {
          name: "Paper Tree",
          logo_data: undefined,
          tagline: "Computer Based Testing",
          copyright: "Paper Tree Educational Studio",
        },
      });
    }

    /*
     * Normalize the subdomain.
     *
     * Example:
     *
     * infinity-classes
     * InfinityClasses
     *
     * become comparable.
     */
    const normalizedSubdomain = subdomain
      .toLowerCase()
      .replace(/[^a-z0-9]/g, "");

    /*
     * Find academy by its name.
     *
     * Example:
     *
     * Infinity Classes
     *        ↓
     * infinityclasses
     */
    const result = await pool.query(
      `
      SELECT
        id,
        name,
        logo_url,
        branding_enabled
      FROM academies
      WHERE LOWER(
        REGEXP_REPLACE(
          name,
          '[^a-zA-Z0-9]+',
          '',
          'g'
        )
      ) = $1
      LIMIT 1
      `,
      [normalizedSubdomain]
    );

    /*
     * Academy not found
     */
    if (!result.rowCount) {
      return NextResponse.json({
        success: true,
        academy: {
          name: "Paper Tree",
          logo_data: undefined,
          tagline: "Computer Based Testing",
          copyright: "Paper Tree Educational Studio",
        },
      });
    }

    const academy = result.rows[0];

    /*
     * If branding has been disabled,
     * fall back to Paper Tree.
     */
    if (academy.branding_enabled === false) {
      return NextResponse.json({
        success: true,
        academy: {
          id: academy.id,
          name: "Paper Tree",
          logo_data: undefined,
          tagline: "Computer Based Testing",
          copyright: "Paper Tree Educational Studio",
        },
      });
    }

    /*
     * Return the format expected by app/page.tsx
     */
    return NextResponse.json({
      success: true,
      academy: {
        id: academy.id,
        name: academy.name,
        logo_data: academy.logo_url || undefined,
        tagline: "Computer Based Testing",
        copyright: "Paper Tree Educational Studio",
      },
    });
  } catch (error) {
    console.error(
      "ACADEMY BRANDING ERROR:",
      error
    );

    /*
     * Never break the login page because
     * branding could not be loaded.
     */
    return NextResponse.json({
      success: true,
      academy: {
        name: "Paper Tree",
        logo_data: undefined,
        tagline: "Computer Based Testing",
        copyright: "Paper Tree Educational Studio",
      },
    });
  }
}