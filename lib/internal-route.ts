import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { parseSessionCookie } from "@/lib/session";

export function productionDisabledResponse() {
  if (process.env.NODE_ENV === "production") {
    return NextResponse.json({ success: false, error: "Not found." }, { status: 404 });
  }
  return null;
}

export async function requireMasterAdmin() {
  const value = (await cookies()).get("master_session")?.value;
  if (!value) return false;
  const session = parseSessionCookie<Record<string, unknown>>(value);
  return session?.role === "ADMIN" || session?.role === "MASTER_ADMIN";
}
