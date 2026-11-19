import { NextResponse } from "next/server";
import bcrypt from "bcryptjs";
import { requireMasterAdmin } from "@/lib/internal-route";
import { ensureSalesSchema, isSalesPortalHost, salesPortalDisabled } from "@/lib/sales-portal";
import { pool } from "@/lib/db";
import { sendEmail } from "@/lib/email";

export const runtime = "nodejs";

export async function GET(request: Request) {
  if (!isSalesPortalHost(request.headers.get("host"))) return salesPortalDisabled();
  if (!(await requireMasterAdmin())) {
    return NextResponse.json({ success: false, error: "Unauthorized." }, { status: 401 });
  }

  try {
    await ensureSalesSchema();
    const result = await pool.query(`
      SELECT
        u.id, u.name, u.email, u.active, u.created_at,
        u.commission_percentage,
        COUNT(l.id)::int AS institutes_set_up,
        COUNT(l.id) FILTER (WHERE l.status = 'REJECTED')::int AS rejected,
        COUNT(l.id) FILTER (WHERE l.status = 'FOLLOW_UP')::int AS follow_up,
        COUNT(l.id) FILTER (WHERE l.status = 'INTERESTED')::int AS interested,
        COUNT(l.id) FILTER (WHERE l.status = 'CONVERTED')::int AS converted,
        COALESCE(SUM(l.total_students) FILTER (WHERE l.status = 'CONVERTED'), 0)::int AS total_students,
        COALESCE(SUM(l.sale_amount) FILTER (WHERE l.status = 'CONVERTED'), 0)::numeric AS sales_amount,
        COALESCE(SUM(l.sale_amount) FILTER (WHERE l.status = 'CONVERTED'), 0) * u.commission_percentage / 100::numeric AS commission
      FROM sales_users u
      LEFT JOIN sales_leads l ON l.sales_user_id = u.id
      GROUP BY u.id
      ORDER BY u.created_at DESC
    `);
    return NextResponse.json({ success: true, salesUsers: result.rows });
  } catch (error) {
    console.error("GET SALES TEAM ERROR:", error);
    return NextResponse.json({ success: false, error: "Could not load sales team." }, { status: 500 });
  }
}

export async function POST(request: Request) {
  if (!isSalesPortalHost(request.headers.get("host"))) return salesPortalDisabled();
  if (!(await requireMasterAdmin())) {
    return NextResponse.json({ success: false, error: "Unauthorized." }, { status: 401 });
  }

  try {
    const body = await request.json();
    const name = String(body.name || "").trim();
    const email = String(body.email || "").trim().toLowerCase();
    const password = String(body.password || "");
    const commissionPercentage = Number(body.commissionPercentage ?? 0);
    if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || !password || !Number.isFinite(commissionPercentage) || commissionPercentage < 0 || commissionPercentage > 100) {
      return NextResponse.json(
        { success: false, error: "Enter a name, valid email, and password." },
        { status: 400 },
      );
    }

    await ensureSalesSchema();
    const existingAccount = await pool.query(
      `SELECT email FROM admins WHERE LOWER(email) = $1
       UNION ALL
       SELECT email FROM teachers WHERE LOWER(email) = $1
       UNION ALL
       SELECT email FROM students WHERE LOWER(email) = $1
       LIMIT 1`,
      [email],
    );
    if (existingAccount.rowCount) {
      return NextResponse.json(
        { success: false, error: "That email is already used by another account." },
        { status: 409 },
      );
    }
    const passwordHash = await bcrypt.hash(password, 12);
    const client = await pool.connect();
    try {
      await client.query("BEGIN");
      const result = await client.query(
        `INSERT INTO sales_users (name, email, password_hash, commission_percentage) VALUES ($1, $2, $3, $4)
         RETURNING id, name, email, active, created_at`,
        [name, email, passwordHash, commissionPercentage],
      );
      const escapeHtml = (value: string) =>
        value.replace(/[&<>"']/g, (character) => ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[character] || character);

      await sendEmail({
        to: email,
        subject: "Your Paper Tree sales account",
        html: `<p>Hello ${escapeHtml(name)},</p>
          <p>Your Paper Tree sales account is ready.</p>
          <p><strong>Login:</strong> <a href="https://demo.cbt.papertreestudio.in/login">Sales login</a></p>
          <p><strong>Email:</strong> ${escapeHtml(email)}<br />
          <strong>Temporary password:</strong> ${escapeHtml(password)}</p>
          <p>Please sign in and change your password after your first login.</p>`,
      });
      await client.query("COMMIT");
      return NextResponse.json({ success: true, salesUser: result.rows[0] }, { status: 201 });
    } catch (error) {
      await client.query("ROLLBACK");
      throw error;
    } finally {
      client.release();
    }
  } catch (error) {
    console.error("CREATE SALES USER ERROR:", error);
    const duplicate = error instanceof Error && "code" in error && error.code === "23505";
    return NextResponse.json(
      {
        success: false,
        error: duplicate
          ? "A sales account already uses that email."
          : error instanceof Error && error.message.startsWith("Email is not configured")
            ? error.message
            : error instanceof Error && error.message === "Email provider could not send the message."
              ? error.message
              : "Could not create sales account.",
      },
      { status: duplicate ? 409 : error instanceof Error && error.message.startsWith("Email is not configured") ? 503 : 500 },
    );
  }
}

export async function PATCH(request: Request) {
  if (!isSalesPortalHost(request.headers.get("host"))) return salesPortalDisabled();
  if (!(await requireMasterAdmin())) {
    return NextResponse.json({ success: false, error: "Unauthorized." }, { status: 401 });
  }

  try {
    const body = await request.json();
    const id = String(body.id || "");
    const commissionPercentage = Number(body.commissionPercentage);
    if (!/^[0-9a-f-]{36}$/i.test(id)) {
      return NextResponse.json({ success: false, error: "A valid account is required." }, { status: 400 });
    }
    await ensureSalesSchema();
    let result;
    if (typeof body.active === "boolean") {
      result = await pool.query(
        `UPDATE sales_users SET active = $1, updated_at = NOW() WHERE id = $2::uuid RETURNING id`,
        [body.active, id],
      );
    } else if (Number.isFinite(commissionPercentage) && commissionPercentage >= 0 && commissionPercentage <= 100) {
      result = await pool.query(
        `UPDATE sales_users SET commission_percentage = $1, updated_at = NOW() WHERE id = $2::uuid RETURNING id`,
        [commissionPercentage, id],
      );
    } else {
      return NextResponse.json({ success: false, error: "Provide an active state or commission amount." }, { status: 400 });
    }
    if (!result.rowCount) return NextResponse.json({ success: false, error: "Sales account not found." }, { status: 404 });
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("UPDATE SALES USER ERROR:", error);
    return NextResponse.json({ success: false, error: "Could not update sales account." }, { status: 500 });
  }
}
