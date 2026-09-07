import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import crypto from "crypto";
import bcrypt from "bcryptjs";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

async function isMasterAdmin() {
  const cookieStore = await cookies();
  const session = cookieStore.get("master_session")?.value;

  if (!session) return false;

  try {
    const data = JSON.parse(session);
    return data.role === "ADMIN" || data.role === "MASTER_ADMIN";
  } catch {
    return false;
  }
}

export async function GET() {
  if (!(await isMasterAdmin())) {
    return NextResponse.json(
      { success: false, error: "Unauthorized" },
      { status: 401 }
    );
  }

  const result = await pool.query(`
    SELECT
      a.id,
      a.name,
      a.code,
      a.created_at,
      a.status,
      a.student_limit,
      a.subscription_start,
      a.subscription_end,
      a.subscription_plan,
      COUNT(DISTINCT t.id)::int AS teacher_count,
      COUNT(DISTINCT s.id)::int AS student_count
    FROM academies a
    LEFT JOIN teachers t ON t.academy_id = a.id
    LEFT JOIN students s ON s.academy_id = a.id
    GROUP BY a.id
    ORDER BY a.created_at DESC
  `);

  return NextResponse.json({
    success: true,
    academies: result.rows,
  });
}

export async function POST(req: NextRequest) {
  if (!(await isMasterAdmin())) {
    return NextResponse.json(
      { success: false, error: "Unauthorized" },
      { status: 401 }
    );
  }

  const body = await req.json();

  const academyName = String(body.academyName || "").trim();
  const academyCode = String(body.academyCode || "")
    .trim()
    .toUpperCase();

  const adminName = String(body.adminName || "").trim();
  const adminEmail = String(body.adminEmail || "")
    .trim()
    .toLowerCase();
  const adminPassword = String(body.adminPassword || "");
  const subscriptionPlan = String(body.subscriptionPlan || "Custom").trim();
  const studentLimit = Number(body.studentLimit);
  const subscriptionStart = String(body.subscriptionStart || "").trim();
  const subscriptionEnd = String(body.subscriptionEnd || "").trim();

  if (
    !academyName ||
    !academyCode ||
    !adminName ||
    !adminEmail ||
    !adminPassword ||
    !Number.isInteger(studentLimit) ||
    studentLimit < 1 ||
    !subscriptionStart ||
    !subscriptionEnd
  ) {
    return NextResponse.json(
      { success: false, error: "All fields are required." },
      { status: 400 }
    );
  }

  if (adminPassword.length < 6) {
    return NextResponse.json(
      {
        success: false,
        error: "Admin password must be at least 6 characters.",
      },
      { status: 400 }
    );
  }

  const client = await pool.connect();

  try {
    await client.query("BEGIN");

    const academyId = crypto.randomUUID();

    const existingAcademy = await client.query(
      `SELECT id FROM academies WHERE code = $1`,
      [academyCode]
    );

    if (existingAcademy.rows.length) {
      throw new Error("Academy code already exists.");
    }

    const existingAdmin = await client.query(
      `SELECT id FROM admins WHERE LOWER(email) = LOWER($1)`,
      [adminEmail]
    );

    if (existingAdmin.rows.length) {
      throw new Error("An admin account with this email already exists.");
    }

    await client.query(
      `
      INSERT INTO academies (
        id,
        name,
        code,
        subscription_plan,
        student_limit,
        subscription_start,
        subscription_end
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7)
      `,
      [academyId, academyName, academyCode, subscriptionPlan, studentLimit, subscriptionStart, subscriptionEnd]
    );

    const adminId = crypto.randomUUID();
    const passwordHash = await bcrypt.hash(adminPassword, 12);

    await client.query(
      `
      INSERT INTO admins (
        id,
        name,
        email,
        password_hash,
        academy_id,
        is_master
      )
      VALUES ($1, $2, $3, $4, $5, FALSE)
      `,
      [
        adminId,
        adminName,
        adminEmail,
        passwordHash,
        academyId,
      ]
    );

    await client.query("COMMIT");

    return NextResponse.json({
      success: true,
      academy: {
        id: academyId,
        name: academyName,
        code: academyCode,
      },
      admin: {
        id: adminId,
        name: adminName,
        email: adminEmail,
      },
    });
  } catch (error) {
    await client.query("ROLLBACK");

    console.error("CREATE ACADEMY ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Failed to create academy.",
      },
      { status: 500 }
    );
  } finally {
    client.release();
  }
}
