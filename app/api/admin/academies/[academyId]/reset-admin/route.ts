import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import bcrypt from "bcryptjs";
import { pool } from "@/lib/db";

async function isMasterAdmin() {
  const value = (await cookies()).get("master_session")?.value;
  if (!value) return false;

  try {
    const session = JSON.parse(value);
    return session.role === "ADMIN" || session.role === "MASTER_ADMIN";
  } catch {
    return false;
  }
}

export async function POST(
  request: Request,
  { params }: { params: Promise<{ academyId: string }> }
) {
  if (!(await isMasterAdmin())) {
    return NextResponse.json({ success: false, error: "Unauthorized" }, { status: 401 });
  }

  const { academyId } = await params;
  const body = await request.json();
  const password = String(body.password || "");

  if (password.length < 6) {
    return NextResponse.json(
      { success: false, error: "Password must be at least 6 characters." },
      { status: 400 }
    );
  }

  const admin = await pool.query(
    `
    SELECT ad.id, ad.name, ad.email, ac.name AS academy_name
    FROM admins ad
    INNER JOIN academies ac ON ac.id = ad.academy_id
    WHERE ad.academy_id = $1 AND ad.is_master = FALSE
    ORDER BY ad.created_at ASC
    LIMIT 1
    `,
    [academyId]
  );

  if (!admin.rows.length) {
    return NextResponse.json(
      { success: false, error: "No academy administrator was found." },
      { status: 404 }
    );
  }

  const passwordHash = await bcrypt.hash(password, 12);
  await pool.query(
    `UPDATE admins SET password_hash = $1 WHERE id = $2`,
    [passwordHash, admin.rows[0].id]
  );

  return NextResponse.json({
    success: true,
    credentials: {
      academy: admin.rows[0].academy_name,
      email: admin.rows[0].email,
      password,
    },
  });
}