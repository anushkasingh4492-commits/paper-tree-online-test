import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";
import { ensureSalesSchema, isSalesPortalHost, salesPortalDisabled } from "@/lib/sales-portal";
import { ensureSubscriptionSchema, normalizeSubscriptionTier } from "@/lib/subscription";
import bcrypt from "bcryptjs";
import crypto from "crypto";

export const runtime = "nodejs";

async function getActor() {
  const cookieStore = await cookies();
  const masterRaw = cookieStore.get("master_session")?.value;
  const master = masterRaw
    ? parseSessionCookie<{ role?: string }>(masterRaw)
    : null;
  if (master?.role === "ADMIN" || master?.role === "MASTER_ADMIN") return { id: null, isAdmin: true };

  const salesRaw = cookieStore.get("sales_session")?.value;
  const sales = salesRaw
    ? parseSessionCookie<{ id?: string; role?: string }>(salesRaw)
    : null;
  if (sales?.role === "SALES" && sales.id) return { id: sales.id, isAdmin: false };
  return null;
}

export async function GET(request: Request) {
  if (!isSalesPortalHost(request.headers.get("host"))) return salesPortalDisabled();
  const actor = await getActor();
  if (!actor) return NextResponse.json({ success: false, error: "Unauthorized." }, { status: 401 });

  try {
    await ensureSalesSchema();
    if (!actor.isAdmin) {
      const activeUser = await pool.query(
        "SELECT id FROM sales_users WHERE id = $1::uuid AND active = TRUE",
        [actor.id],
      );
      if (!activeUser.rowCount) return NextResponse.json({ success: false, error: "Sales account is inactive." }, { status: 403 });
    }
    const result = await pool.query(
      `SELECT l.id, l.academy_id, a.code AS academy_code,
              l.institute_name, l.contact_name, l.email, l.phone, l.status,
              l.follow_up_at, l.students_converted, l.sale_amount, l.notes, l.created_at,
              u.name AS sales_person,
              (l.sale_amount * 0.1)::numeric AS commission
       FROM sales_leads l
       JOIN sales_users u ON u.id = l.sales_user_id
       LEFT JOIN academies a ON a.id = l.academy_id
       WHERE ($1::uuid IS NULL OR l.sales_user_id = $1)
       ORDER BY l.created_at DESC`,
      [actor.id],
    );
    return NextResponse.json({ success: true, leads: result.rows });
  } catch (error) {
    console.error("GET SALES LEADS ERROR:", error);
    return NextResponse.json({ success: false, error: "Could not load institute demos." }, { status: 500 });
  }
}

export async function POST(request: Request) {
  if (!isSalesPortalHost(request.headers.get("host"))) return salesPortalDisabled();
  const actor = await getActor();
  if (!actor || actor.isAdmin || !actor.id) {
    return NextResponse.json({ success: false, error: "Sales team login required." }, { status: 401 });
  }

  try {
    await ensureSalesSchema();
    const activeUser = await pool.query(
      "SELECT id FROM sales_users WHERE id = $1::uuid AND active = TRUE",
      [actor.id],
    );
    if (!activeUser.rowCount) return NextResponse.json({ success: false, error: "Sales account is inactive." }, { status: 403 });
    const body = await request.json();
    const instituteName = String(body.instituteName || "").trim();
    const academyCode = String(body.academyCode || "").trim().toUpperCase();
    const contactName = String(body.contactName || "").trim();
    const email = String(body.email || "").trim().toLowerCase() || null;
    const phone = String(body.phone || "").trim() || null;
    const notes = String(body.notes || "").trim() || null;
    const adminName = String(body.adminName || "").trim();
    const adminEmail = String(body.adminEmail || "").trim().toLowerCase();
    const adminPassword = String(body.adminPassword || "");
    const studentLimit = Number(body.studentLimit);
    const subscriptionMonths = Number(body.subscriptionMonths);
    const subscriptionStart = String(body.subscriptionStart || "").trim();
    const subscriptionTier = normalizeSubscriptionTier(body.subscriptionTier);
    const courseOptions = ["MHT-CET PCM", "MHT-CET PCB", "NEET PCB", "CAT", "JEE PCM"];
    const assignedCourses = Array.isArray(body.assignedCourses)
      ? body.assignedCourses.filter(
          (course: unknown): course is string =>
            typeof course === "string" && courseOptions.includes(course),
        )
      : [];

    if (
      !instituteName ||
      !academyCode ||
      !contactName ||
      !adminName ||
      !adminEmail ||
      !adminPassword ||
      instituteName.length > 255 ||
      academyCode.length > 100 ||
      contactName.length > 150 ||
      adminName.length > 150 ||
      !/^[A-Z0-9][A-Z0-9_-]{1,99}$/.test(academyCode) ||
      !Number.isInteger(studentLimit) ||
      studentLimit < 1 ||
      !Number.isInteger(subscriptionMonths) ||
      subscriptionMonths < 1 ||
      subscriptionMonths > 120 ||
      adminPassword.length < 6
    ) {
      return NextResponse.json(
        { success: false, error: "Complete the institute, academy code, academy admin, password (at least 6 characters), seats, and subscription fields with valid values." },
        { status: 400 },
      );
    }
    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return NextResponse.json({ success: false, error: "Enter a valid contact email." }, { status: 400 });
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(adminEmail)) {
      return NextResponse.json({ success: false, error: "Enter a valid academy admin email." }, { status: 400 });
    }

    const parsedStart = new Date(`${subscriptionStart}T00:00:00.000Z`);
    if (
      !/^\d{4}-\d{2}-\d{2}$/.test(subscriptionStart) ||
      Number.isNaN(parsedStart.getTime()) ||
      parsedStart.toISOString().slice(0, 10) !== subscriptionStart
    ) {
      return NextResponse.json({ success: false, error: "Enter a valid subscription start date." }, { status: 400 });
    }
    const subscriptionEndDate = new Date(parsedStart);
    const day = subscriptionEndDate.getUTCDate();
    subscriptionEndDate.setUTCDate(1);
    subscriptionEndDate.setUTCMonth(subscriptionEndDate.getUTCMonth() + subscriptionMonths);
    const lastDay = new Date(Date.UTC(
      subscriptionEndDate.getUTCFullYear(),
      subscriptionEndDate.getUTCMonth() + 1,
      0,
    )).getUTCDate();
    subscriptionEndDate.setUTCDate(Math.min(day, lastDay));
    const subscriptionEnd = subscriptionEndDate.toISOString().slice(0, 10);

    await ensureSubscriptionSchema();
    await pool.query(`
      ALTER TABLE academies
        ADD COLUMN IF NOT EXISTS status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',
        ADD COLUMN IF NOT EXISTS student_limit INTEGER NOT NULL DEFAULT 10,
        ADD COLUMN IF NOT EXISTS subscription_plan VARCHAR(255),
        ADD COLUMN IF NOT EXISTS subscription_start DATE,
        ADD COLUMN IF NOT EXISTS subscription_end DATE,
        ADD COLUMN IF NOT EXISTS assigned_courses TEXT[] NOT NULL DEFAULT '{}'
    `);

    const client = await pool.connect();
    let transactionStarted = false;
    try {
      await client.query("BEGIN");
      transactionStarted = true;

      const existingAcademy = await client.query(
        "SELECT id FROM academies WHERE UPPER(code) = $1",
        [academyCode],
      );
      if (existingAcademy.rowCount) throw new Error("Academy code already exists.");

      const existingAccount = await client.query(
        `SELECT email FROM admins WHERE LOWER(email) = $1
         UNION ALL SELECT email FROM teachers WHERE LOWER(email) = $1
         UNION ALL SELECT email FROM students WHERE LOWER(email) = $1
         UNION ALL SELECT email FROM sales_users WHERE LOWER(email) = $1
         LIMIT 1`,
        [adminEmail],
      );
      if (existingAccount.rowCount) throw new Error("That academy admin email is already used by another account.");

      const academyId = crypto.randomUUID();
      const adminId = crypto.randomUUID();
      const passwordHash = await bcrypt.hash(adminPassword, 12);
      const plan = `${subscriptionTier} · ${studentLimit} Students · ${subscriptionMonths} Months`;

      await client.query(
        `INSERT INTO academies (
           id, name, code, status, subscription_plan, subscription_tier,
           student_limit, subscription_start, subscription_end, assigned_courses
         )
         VALUES ($1, $2, $3, 'ACTIVE', $4, $5, $6, $7, $8, $9)`,
        [academyId, instituteName, academyCode, plan, subscriptionTier, studentLimit, subscriptionStart, subscriptionEnd, assignedCourses],
      );
      await client.query(
        `INSERT INTO admins (id, name, email, password_hash, academy_id, is_master)
         VALUES ($1, $2, $3, $4, $5, FALSE)`,
        [adminId, adminName, adminEmail, passwordHash, academyId],
      );
      const result = await client.query(
        `INSERT INTO sales_leads (
           academy_id, institute_name, contact_name, email, phone, notes, sales_user_id
         )
         VALUES ($1, $2, $3, $4, $5, $6, $7)
         RETURNING id, academy_id, institute_name, contact_name, email, phone, status,
                   follow_up_at, students_converted, sale_amount, notes, created_at`,
        [academyId, instituteName, contactName, email, phone, notes, actor.id],
      );
      await client.query("COMMIT");
      transactionStarted = false;

      return NextResponse.json(
        {
          success: true,
          lead: result.rows[0],
          academy: { id: academyId, name: instituteName, code: academyCode },
          admin: { id: adminId, name: adminName, email: adminEmail },
        },
        { status: 201 },
      );
    } catch (error) {
      if (transactionStarted) await client.query("ROLLBACK");
      const duplicate = error instanceof Error && "code" in error && error.code === "23505";
      if (duplicate) {
        return NextResponse.json(
          { success: false, error: "Academy code or admin email is already in use." },
          { status: 409 },
        );
      }
      if (error instanceof Error && (error.message === "Academy code already exists." || error.message === "That academy admin email is already used by another account.")) {
        return NextResponse.json({ success: false, error: error.message }, { status: 409 });
      }
      throw error;
    } finally {
      client.release();
    }
  } catch (error) {
    console.error("CREATE SALES LEAD ERROR:", error);
    return NextResponse.json({ success: false, error: "Could not save institute demo." }, { status: 500 });
  }
}
