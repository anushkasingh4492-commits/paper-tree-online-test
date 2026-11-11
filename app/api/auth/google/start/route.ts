import { createHash, randomBytes } from "node:crypto";
import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const STATE_COOKIE = "google_oauth_state";
const VERIFIER_COOKIE = "google_oauth_verifier";

export async function GET(request: NextRequest) {
  const clientId = process.env.GOOGLE_CLIENT_ID;
  const clientSecret = process.env.GOOGLE_CLIENT_SECRET;
  if (!clientId || !clientSecret) {
    return NextResponse.redirect(
      new URL("/login?error=google_not_configured", request.url)
    );
  }

  const state = randomBytes(32).toString("base64url");
  const verifier = randomBytes(32).toString("base64url");
  const challenge = createHash("sha256").update(verifier).digest("base64url");
  const redirectUri =
    process.env.GOOGLE_REDIRECT_URI ||
    new URL("/api/auth/google/callback", request.url).toString();
  const authorizeUrl = new URL("https://accounts.google.com/o/oauth2/v2/auth");
  authorizeUrl.search = new URLSearchParams({
    client_id: clientId,
    redirect_uri: redirectUri,
    response_type: "code",
    scope: "openid email profile",
    state,
    code_challenge: challenge,
    code_challenge_method: "S256",
    prompt: "select_account",
  }).toString();

  const response = NextResponse.redirect(authorizeUrl);
  const cookieOptions = {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax" as const,
    path: "/api/auth/google",
    maxAge: 10 * 60,
  };
  response.cookies.set(STATE_COOKIE, state, cookieOptions);
  response.cookies.set(VERIFIER_COOKIE, verifier, cookieOptions);
  return response;
}
