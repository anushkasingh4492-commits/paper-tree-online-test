import { NextRequest, NextResponse } from "next/server";
import { pool } from "@/lib/db";
import { createSessionCookie } from "@/lib/session";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const STATE_COOKIE = "google_oauth_state";
const VERIFIER_COOKIE = "google_oauth_verifier";
const COOKIE_PATH = "/api/auth/google";

type GoogleTokenResponse = {
  access_token?: string;
};

type GoogleUserInfo = {
  sub?: string;
  email?: string;
  email_verified?: boolean;
  name?: string;
};

type Account = {
  id: string;
  name: string;
  academy_id: string | null;
  role: "ADMIN" | "ACADEMY_ADMIN" | "TEACHER" | "STUDENT";
  is_master?: boolean;
  academy_status?: string | null;
  subscription_end?: string | Date | null;
  roll_number?: string | null;
  class_name?: string | null;
};

function clearOAuthCookies(response: NextResponse) {
  const cookieOptions = {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax" as const,
    path: COOKIE_PATH,
    maxAge: 0,
  };
  response.cookies.set(STATE_COOKIE, "", cookieOptions);
  response.cookies.set(VERIFIER_COOKIE, "", cookieOptions);
}

function loginError(request: NextRequest, error: string) {
  const response = NextResponse.redirect(new URL(`/login?error=${error}`, request.url));
  clearOAuthCookies(response);
  return response;
}

export async function GET(request: NextRequest) {
  const state = request.nextUrl.searchParams.get("state");
  const code = request.nextUrl.searchParams.get("code");
  const expectedState = request.cookies.get(STATE_COOKIE)?.value;
  const verifier = request.cookies.get(VERIFIER_COOKIE)?.value;

  if (
    request.nextUrl.searchParams.has("error") ||
    !state ||
    !code ||
    !expectedState ||
    !verifier ||
    state !== expectedState
  ) {
    return loginError(request, "google_failed");
  }

  const clientId = process.env.GOOGLE_CLIENT_ID;
  const clientSecret = process.env.GOOGLE_CLIENT_SECRET;
  if (!clientId || !clientSecret) {
    return loginError(request, "google_not_configured");
  }

  const redirectUri =
    process.env.GOOGLE_REDIRECT_URI ||
    new URL("/api/auth/google/callback", request.url).toString();

  try {
    const tokenResponse = await fetch("https://oauth2.googleapis.com/token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        client_id: clientId,
        client_secret: clientSecret,
        code,
        code_verifier: verifier,
        grant_type: "authorization_code",
        redirect_uri: redirectUri,
      }),
      cache: "no-store",
    });

    const tokenData = (await tokenResponse.json().catch(() => null)) as
      | GoogleTokenResponse
      | null;
    if (!tokenResponse.ok || !tokenData?.access_token) {
      console.error("GOOGLE TOKEN EXCHANGE FAILED:", tokenResponse.status);
      return loginError(request, "google_failed");
    }

    const userInfoResponse = await fetch(
      "https://openidconnect.googleapis.com/v1/userinfo",
      {
        headers: { Authorization: `Bearer ${tokenData.access_token}` },
        cache: "no-store",
      }
    );
    const userInfo = (await userInfoResponse.json().catch(() => null)) as
      | GoogleUserInfo
      | null;

    if (!userInfoResponse.ok || !userInfo?.sub || !userInfo.email) {
      console.error("GOOGLE USER INFO FAILED:", userInfoResponse.status);
      return loginError(request, "google_failed");
    }

    if (userInfo.email_verified !== true) {
      return loginError(request, "google_email_unverified");
    }

    const email = userInfo.email.trim().toLowerCase();
    const [admins, teachers, students] = await Promise.all([
      pool.query(
        `SELECT id, name, academy_id, is_master
         FROM admins
         WHERE LOWER(email) = $1`,
        [email]
      ),
      pool.query(
        `SELECT id, name, academy_id
         FROM teachers
         WHERE LOWER(email) = $1`,
        [email]
      ),
      pool.query(
        `SELECT
           s.id,
           s.name,
           s.academy_id,
           s.roll_number,
           s.class_name,
           a.status AS academy_status,
           a.subscription_end
         FROM students s
         INNER JOIN student_credentials c ON c.student_id = s.id
         LEFT JOIN academies a ON a.id = s.academy_id
         WHERE LOWER(s.email) = $1`,
        [email]
      ),
    ]);

    const accounts: Account[] = [
      ...admins.rows.map((row) => ({
        ...row,
        role: row.is_master ? "ADMIN" as const : "ACADEMY_ADMIN" as const,
      })),
      ...teachers.rows.map((row) => ({ ...row, role: "TEACHER" as const })),
      ...students.rows.map((row) => ({ ...row, role: "STUDENT" as const })),
    ];

    if (accounts.length === 0) {
      return loginError(request, "google_no_account");
    }
    if (accounts.length > 1) {
      return loginError(request, "google_account_ambiguous");
    }

    const account = accounts[0];
    if (account.role === "STUDENT") {
      if (account.academy_status && account.academy_status !== "ACTIVE") {
        return loginError(request, "google_account_inactive");
      }
      if (
        account.subscription_end &&
        new Date(account.subscription_end) < new Date()
      ) {
        return loginError(request, "google_subscription_expired");
      }
    }
    if (account.role === "TEACHER" && !account.academy_id) {
      return loginError(request, "google_account_inactive");
    }

    const destination =
      account.role === "STUDENT"
        ? "/dashboard"
        : account.role === "TEACHER"
          ? "/teacher"
          : account.role === "ACADEMY_ADMIN"
            ? "/academy-admin"
            : "/admin";
    const response = NextResponse.redirect(new URL(destination, request.url));
    clearOAuthCookies(response);

    const sessionCookieOptions = {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax" as const,
      path: "/",
    };

    if (account.role === "STUDENT") {
      response.cookies.delete("master_session");
      response.cookies.set(
        "student_session",
        createSessionCookie({
          studentId: account.id,
          name: account.name,
          email,
          academyId: account.academy_id,
        }),
        sessionCookieOptions
      );
    } else {
      response.cookies.delete("student_session");
      response.cookies.set(
        "master_session",
        createSessionCookie({
          id: account.id,
          role: account.role,
          academyId: account.academy_id || null,
        }),
        sessionCookieOptions
      );
    }

    return response;
  } catch (error) {
    console.error("GOOGLE SIGN-IN ERROR:", error);
    return loginError(request, "google_failed");
  }
}
