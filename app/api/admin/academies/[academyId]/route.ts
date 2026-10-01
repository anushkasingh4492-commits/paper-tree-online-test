import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";
export async function PATCH(
  req: Request,
  { params }: { params: Promise<{ academyId: string }> }
) {
  try {
    const { academyId } = await params;

    const cookieStore = await cookies();
    const masterCookie =
      cookieStore.get("master_session")?.value;

    if (!masterCookie) {
      return NextResponse.json(
        {
          success: false,
          error: "Unauthorized",
        },
        { status: 401 }
      );
    }

    const session =
      parseSessionCookie<Record<string, unknown>>(
        masterCookie
      );

    const role = String(session?.role || "").toUpperCase();

    if (
      role !== "ADMIN" &&
      role !== "MASTER_ADMIN"
    ) {
      return NextResponse.json(
        {
          success: false,
          error: "Only master admin can update academy details.",
        },
        { status: 403 }
      );
    }

    const body = await req.json();

    // Make sure branding columns exist.
    await pool.query(`
      ALTER TABLE academies
      ADD COLUMN IF NOT EXISTS logo_data TEXT,
      ADD COLUMN IF NOT EXISTS domain VARCHAR(255)
    `);

    const updates: string[] = [];
    const values: unknown[] = [];

    if (body.academyName !== undefined) {
      updates.push(`name = $${values.length + 1}`);
      values.push(String(body.academyName).trim());
    }

    if (body.logoData !== undefined) {
      updates.push(`logo_data = $${values.length + 1}`);
      values.push(
        body.logoData
          ? String(body.logoData)
          : null
      );
    }

    if (body.domain !== undefined) {
      const domain = String(body.domain || "")
        .trim()
        .toLowerCase();

      updates.push(`domain = $${values.length + 1}`);
      values.push(domain || null);
    }

    if (body.studentLimit !== undefined) {
      const studentLimit = Number(body.studentLimit);

      if (
        !Number.isInteger(studentLimit) ||
        studentLimit < 1
      ) {
        return NextResponse.json(
          {
            success: false,
            error: "Invalid student limit.",
          },
          { status: 400 }
        );
      }

      updates.push(`student_limit = $${values.length + 1}`);
      values.push(studentLimit);
    }

    if (body.subscriptionEnd !== undefined) {
      updates.push(
        `subscription_end = $${values.length + 1}`
      );
      values.push(
        body.subscriptionEnd
          ? String(body.subscriptionEnd)
          : null
      );
    }

    if (!updates.length) {
      return NextResponse.json(
        {
          success: false,
          error: "No changes provided.",
        },
        { status: 400 }
      );
    }

    values.push(academyId);

    const result = await pool.query(
      `
      UPDATE academies
      SET ${updates.join(", ")}
      WHERE id = $${values.length}
      RETURNING
        id,
        name,
        code,
        logo_data,
        domain,
        status,
        student_limit,
        subscription_end
      `,
      values
    );

    if (!result.rows.length) {
      return NextResponse.json(
        {
          success: false,
          error: "Academy not found.",
        },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      academy: result.rows[0],
    });
  } catch (error) {
    console.error(
      "ACADEMY PATCH ERROR:",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to update academy.",
      },
      { status: 500 }
    );
  }
}
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