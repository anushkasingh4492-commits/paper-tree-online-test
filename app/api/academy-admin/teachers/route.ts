import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import bcrypt from "bcryptjs";
import { randomUUID } from "crypto";
import { pool } from "@/lib/db";

async function getAcademyAdmin() {
  const cookieStore = await cookies();
  const session = cookieStore.get("master_session")?.value;

  if (!session) return null;

  try {
    const data = JSON.parse(session);

    if (data.role !== "ACADEMY_ADMIN" || !data.academyId) {
      return null;
    }

    return data;
  } catch {
    return null;
  }
}

export async function GET() {
  const admin = await getAcademyAdmin();

  if (!admin) {
    return NextResponse.json(
      { success: false, error: "Unauthorized" },
      { status: 401 }
    );
  }

  const result = await pool.query(
    `
    SELECT
      id,
      name,
      email,
      academy_id
    FROM teachers
    WHERE academy_id = $1
    ORDER BY name
    `,
    [admin.academyId]
  );

  return NextResponse.json({
    success: true,
    teachers: result.rows,
  });
}

export async function POST(req: NextRequest) {
  const admin = await getAcademyAdmin();

  if (!admin) {
    return NextResponse.json(
      { success: false, error: "Unauthorized" },
      { status: 401 }
    );
  }

  const body = await req.json();

  const name = String(body.name || "").trim();
  const email = String(body.email || "").trim().toLowerCase();
  const password = String(body.password || "");

  if (!name || !email || !password) {
    return NextResponse.json(
      { success: false, error: "Name, email and password are required" },
      { status: 400 }
    );
  }

  const existing = await pool.query(
    `
    SELECT id
    FROM teachers
    WHERE LOWER(email) = LOWER($1)
    `,
    [email]
  );

  if (existing.rows.length) {
    return NextResponse.json(
      { success: false, error: "Teacher email already exists" },
      { status: 409 }
    );
  }

  const passwordHash = await bcrypt.hash(password, 10);

  const teacherId = randomUUID();

  await pool.query(
    `
    INSERT INTO teachers
      (id, name, email, password_hash, academy_id)
    VALUES
      ($1, $2, $3, $4, $5)
    `,
    [
      teacherId,
      name,
      email,
      passwordHash,
      admin.academyId,
    ]
  );

  return NextResponse.json({
    success: true,
    teacher: {
      id: teacherId,
      name,
      email,
      academyId: admin.academyId,
    },
  });
}
