import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import bcrypt from "bcryptjs";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

async function isMasterAdmin() {
  const value = (await cookies()).get("master_session")?.value;
  if (!value) return false;

  try {
    const session = parseSessionCookie<Record<string, unknown>>(value);

 return (
  session !== null &&
  (session.role === "ADMIN" ||
    session.role === "MASTER_ADMIN")
);
  } catch {
    return false;
  }
}

export async function POST(
  request: Request,
  { params }: { params: Promise<{ academyId: string }> }
) {
  if (!(await isMasterAdmin())) {
    return NextResponse.json(
      { success: false, error: "Unauthorized" },
      { status: 401 }
    );
  }

  try {
    const { academyId } = await params;
    const body = await request.json();

    const adminId = String(body.adminId || "").trim();
    const password = String(body.password || "");

    if (!adminId) {
      return NextResponse.json(
        { success: false, error: "Admin ID is required." },
        { status: 400 }
      );
    }

    if (password.length < 6) {
      return NextResponse.json(
        {
          success: false,
          error: "Password must be at least 6 characters.",
        },
        { status: 400 }
      );
    }

    const admin = await pool.query(
      `
      SELECT
        ad.id,
        ad.name,
        ad.email,
        ac.name AS academy_name
      FROM admins ad
      INNER JOIN academies ac
        ON ac.id = ad.academy_id
      WHERE ad.id = $1
        AND ad.academy_id = $2
        AND ad.is_master = FALSE
      LIMIT 1
      `,
      [adminId, academyId]
    );

    if (!admin.rows.length) {
      return NextResponse.json(
        {
          success: false,
          error: "Academy administrator not found.",
        },
        { status: 404 }
      );
    }

    const passwordHash = await bcrypt.hash(password, 12);

    await pool.query(
      `
      UPDATE admins
      SET password_hash = $1
      WHERE id = $2
        AND academy_id = $3
        AND is_master = FALSE
      `,
      [passwordHash, adminId, academyId]
    );

    return NextResponse.json({
      success: true,
      credentials: {
        academy: admin.rows[0].academy_name,
        name: admin.rows[0].name,
        email: admin.rows[0].email,
        password,
      },
    });
  } catch (error) {
    console.error("RESET ACADEMY ADMIN ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to reset academy admin password.",
      },
      { status: 500 }
    );
  }
}
