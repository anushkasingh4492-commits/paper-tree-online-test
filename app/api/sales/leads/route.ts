import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";
import { ensureSalesSchema, isSalesPortalHost, salesPortalDisabled } from "@/lib/sales-portal";
import { ensureSubscriptionSchema, normalizeSubscriptionTier } from "@/lib/subscription";
import { ensureAcademyUsernameSchema } from "@/lib/academy-admin-login";
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
              l.sales_user_id,
              l.institute_name, l.contact_name, l.alternate_contact_numbers,
              l.status, l.reaction, l.follow_up_at, l.total_students,
              l.proposed_selling_price, l.duration_days, l.sale_amount, l.notes, l.created_at,
              u.name AS sales_person,
              CASE WHEN l.status = 'CONVERTED' THEN l.sale_amount * u.commission_percentage / 100 ELSE 0 END::numeric AS commission
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
    const alternateContactNumbers: string[] = Array.isArray(body.alternateContactNumbers)
      ? body.alternateContactNumbers.map((value: unknown) => String(value).trim()).filter(Boolean)
      : String(body.alternateContactNumbers || "").split(/[,;\n]/).map((value: string) => value.trim()).filter(Boolean);
    const notes = String(body.notes || "").trim() || null;
    const adminName = String(body.adminName || "").trim();
    const adminUsername = String(body.adminUsername || "").trim().toLowerCase();
    const adminPassword = String(body.adminPassword || "");
    const totalStudents = Number(body.totalStudents);
    const proposedSellingPrice = Number(body.proposedSellingPrice);
    const durationDays = Number(body.durationDays);
    const subscriptionStart = String(body.subscriptionStart || "").trim();
    const subscriptionTier = normalizeSubscriptionTier(body.subscriptionTier);
    const reaction = String(body.reaction || "WARM").trim().toUpperCase();
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
      !adminUsername ||
      !adminPassword ||
      instituteName.length > 255 ||
      academyCode.length > 100 ||
      contactName.length > 150 ||
      adminName.length > 150 ||
      !/^[A-Z0-9][A-Z0-9_-]{1,99}$/.test(academyCode) ||
      !/^[a-z0-9._-]{3,80}$/.test(adminUsername) ||
      !Number.isInteger(totalStudents) ||
      totalStudents < 0 ||
      !Number.isFinite(proposedSellingPrice) ||
      proposedSellingPrice < 0 ||
      !Number.isInteger(durationDays) ||
      durationDays < 1 ||
      durationDays > 3650 ||
      !["HOT", "WARM", "COLD", "REJECTED"].includes(reaction) ||
      adminPassword.length < 6
    ) {
      return NextResponse.json(
        { success: false, error: "Check institute, academy code, contact, username, password (at least 6 characters), student count, proposed price, reaction, duration, and subscription values." },
        { status: 400 },
      );
    }
    if (alternateContactNumbers.some((number) => number.length > 50)) {
      return NextResponse.json({ success: false, error: "Alternate contact numbers must be 50 characters or fewer." }, { status: 400 });
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
    subscriptionEndDate.setUTCDate(subscriptionEndDate.getUTCDate() + durationDays);
    const subscriptionEnd = subscriptionEndDate.toISOString().slice(0, 10);

    await ensureSubscriptionSchema();
    await ensureAcademyUsernameSchema();
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
        `SELECT email FROM admins WHERE LOWER(email) = $1 OR LOWER(username) = $2
         UNION ALL SELECT email FROM teachers WHERE LOWER(email) = $1
         UNION ALL SELECT email FROM students WHERE LOWER(email) = $1
         UNION ALL SELECT email FROM sales_users WHERE LOWER(email) = $1
         LIMIT 1`,
        [`${adminUsername}@demo.papertree.invalid`, adminUsername],
      );
      if (existingAccount.rowCount) throw new Error("That academy admin username is already in use.");

      const academyId = crypto.randomUUID();
      const adminId = crypto.randomUUID();
      const passwordHash = await bcrypt.hash(adminPassword, 12);
      const plan = `${subscriptionTier} · ${totalStudents} Students · ${durationDays} Days`;
      const saleAmount = totalStudents * proposedSellingPrice;

      await client.query(
        `INSERT INTO academies (
           id, name, code, status, subscription_plan, subscription_tier,
           student_limit, subscription_start, subscription_end, assigned_courses
         )
         VALUES ($1, $2, $3, 'ACTIVE', $4, $5, $6, $7, $8, $9)`,
        [academyId, instituteName, academyCode, plan, subscriptionTier, totalStudents, subscriptionStart, subscriptionEnd, assignedCourses],
      );
      await client.query(
        `INSERT INTO admins (id, name, email, username, password_hash, academy_id, is_master)
         VALUES ($1, $2, $3, $4, $5, $6, FALSE)`,
        [adminId, adminName, `${adminUsername}@demo.papertree.invalid`, adminUsername, passwordHash, academyId],
      );
      const result = await client.query(
        `INSERT INTO sales_leads (
           academy_id, institute_name, contact_name, alternate_contact_numbers,
           notes, status, reaction, total_students, proposed_selling_price,
           duration_days, sale_amount, sales_user_id
         )
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
         RETURNING id, academy_id, institute_name, contact_name, alternate_contact_numbers,
                   status, reaction, follow_up_at, total_students, proposed_selling_price,
                   duration_days, sale_amount, notes, created_at`,
        [academyId, instituteName, contactName, alternateContactNumbers, notes, reaction === "REJECTED" ? "REJECTED" : "DEMO_SET_UP", reaction, totalStudents, proposedSellingPrice, durationDays, saleAmount, actor.id],
      );
      await client.query("COMMIT");
      transactionStarted = false;

      return NextResponse.json(
        {
          success: true,
          lead: result.rows[0],
          academy: { id: academyId, name: instituteName, code: academyCode },
          admin: { id: adminId, name: adminName, username: adminUsername },
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
      if (error instanceof Error && (error.message === "Academy code already exists." || error.message === "That academy admin username is already in use.")) {
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
