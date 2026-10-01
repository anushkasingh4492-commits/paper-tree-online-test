import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import bcrypt from "bcryptjs";
import { randomUUID } from "crypto";
import { pool } from "@/lib/db";

async function isMasterAdmin() {
  const value = (await cookies()).get("master_session")?.value;

  if (!value) return false;

  try {
    const session = JSON.parse(decodeURIComponent(value));

    return (
      session.role === "ADMIN" ||
      session.role === "MASTER_ADMIN"
    );
  } catch {
    return false;
  }
}

export async function GET(
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

    const result = await pool.query(
      `
      SELECT
        id,
        name,
        email,
        is_master,
        created_at
      FROM admins
      WHERE academy_id = $1
        AND is_master = FALSE
      ORDER BY created_at ASC
      `,
      [academyId]
    );

    return NextResponse.json({
      success: true,
      admins: result.rows,
    });
  } catch (error) {
    console.error("GET ACADEMY ADMINS ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to load academy admins.",
      },
      { status: 500 }
    );
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

    const name = String(body.name || "").trim();
    const email = String(body.email || "").trim().toLowerCase();
    const password = String(body.password || "");

    if (!name || !email || !password) {
      return NextResponse.json(
        {
          success: false,
          error: "Name, email and password are required.",
        },
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

    const academy = await pool.query(
      `
      SELECT id, name
      FROM academies
      WHERE id = $1
      LIMIT 1
      `,
      [academyId]
    );

    if (!academy.rows.length) {
      return NextResponse.json(
        {
          success: false,
          error: "Academy not found.",
        },
        { status: 404 }
      );
    }

    const existing = await pool.query(
      `
      SELECT id
      FROM admins
      WHERE LOWER(email) = $1
      LIMIT 1
      `,
      [email]
    );

    if (existing.rows.length) {
      return NextResponse.json(
        {
          success: false,
          error: "An admin with this email already exists.",
        },
        { status: 409 }
      );
    }

    const passwordHash = await bcrypt.hash(password, 12);
    const adminId = randomUUID();

    const result = await pool.query(
      `
      INSERT INTO admins
        (id, name, email, password_hash, academy_id, is_master)
      VALUES
        ($1, $2, $3, $4, $5, FALSE)
      RETURNING id, name, email, academy_id, is_master, created_at
      `,
      [
        adminId,
        name,
        email,
        passwordHash,
        academyId,
      ]
    );

    return NextResponse.json({
      success: true,
      admin: result.rows[0],
      credentials: {
        academy: academy.rows[0].name,
        email,
        password,
      },
    });
  } catch (error) {
    console.error("CREATE ACADEMY ADMIN ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to create academy admin.",
      },
      { status: 500 }
    );
  }
}
