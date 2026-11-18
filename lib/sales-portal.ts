import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";

export type SalesSession = {
  id: string;
  role: "SALES";
  name: string;
  email: string;
};

const leadStatuses = [
  "DEMO_SET_UP",
  "REJECTED",
  "FOLLOW_UP",
  "INTERESTED",
  "CONVERTED",
] as const;

export type SalesLeadStatus = (typeof leadStatuses)[number];

export function isSalesPortalHost(host: string | null) {
  if (process.env.NODE_ENV !== "production") return true;

  const hostname = (host || "").split(":")[0].toLowerCase();
  const allowedHost = (process.env.DEMO_CBT_HOST || process.env.NEXT_PUBLIC_DEMO_CBT_HOST || "demo.cbt")
    .split(":")[0]
    .toLowerCase();

  return hostname === allowedHost;
}

export function salesPortalDisabled() {
  return NextResponse.json(
    { success: false, error: "Not found." },
    { status: 404 },
  );
}

export async function ensureSalesSchema() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS sales_users (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      name VARCHAR(150) NOT NULL,
      email VARCHAR(255) NOT NULL UNIQUE,
      password_hash TEXT NOT NULL,
      active BOOLEAN NOT NULL DEFAULT TRUE,
      created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )
  `);

  await pool.query(`
    CREATE TABLE IF NOT EXISTS sales_leads (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      institute_name VARCHAR(255) NOT NULL,
      contact_name VARCHAR(150) NOT NULL,
      email VARCHAR(255),
      phone VARCHAR(50),
      status VARCHAR(30) NOT NULL DEFAULT 'DEMO_SET_UP'
        CHECK (status IN ('DEMO_SET_UP', 'REJECTED', 'FOLLOW_UP', 'INTERESTED', 'CONVERTED')),
      follow_up_at DATE,
      students_converted INTEGER NOT NULL DEFAULT 0 CHECK (students_converted >= 0),
      sale_amount NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (sale_amount >= 0),
      notes TEXT,
      sales_user_id UUID NOT NULL REFERENCES sales_users(id) ON DELETE RESTRICT,
      created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )
  `);

  await pool.query(`
    CREATE INDEX IF NOT EXISTS sales_leads_sales_user_created_idx
    ON sales_leads (sales_user_id, created_at DESC)
  `);
}

export async function getSalesSession() {
  const value = (await cookies()).get("sales_session")?.value;
  if (!value) return null;

  const session = parseSessionCookie<SalesSession>(value);
  if (session?.role !== "SALES" || !session.id) return null;
  return session;
}

export async function getSalesUserFromRequest(request: Request) {
  const value = request.headers
    .get("cookie")
    ?.match(/(?:^|;\s*)sales_session=([^;]+)/)?.[1];
  if (!value) return null;

  const session = parseSessionCookie<SalesSession>(value);
  if (session?.role !== "SALES" || !session.id) return null;
  return session;
}

export function isSalesLeadStatus(status: unknown): status is SalesLeadStatus {
  return typeof status === "string" && leadStatuses.includes(status as SalesLeadStatus);
}
