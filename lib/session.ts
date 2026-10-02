import crypto from "crypto";

export type SessionPayload = Record<string, unknown>;

function getSessionSecret() {
  const secret = process.env.SESSION_SECRET;

  if (secret && secret.length >= 32) {
    return secret;
  }

  if (process.env.NODE_ENV !== "production") {
    return "paper-tree-local-development-session-secret-32chars";
  }

  throw new Error(
    "SESSION_SECRET must be configured and contain at least 32 characters."
  );
}

function sign(payload: string) {
  return crypto
    .createHmac("sha256", getSessionSecret())
    .update(payload)
    .digest("base64url");
}

export function createSessionCookie<T extends SessionPayload>(payload: T) {
  const encoded = Buffer.from(JSON.stringify(payload), "utf8").toString(
    "base64url"
  );
  return `${encoded}.${sign(encoded)}`;
}

export function parseSessionCookie<T extends SessionPayload>(value: string): T | null {
  const separator = value.lastIndexOf(".");

  if (separator <= 0 || separator === value.length - 1) {
    return null;
  }

  const encoded = value.slice(0, separator);
  const signature = value.slice(separator + 1);
  const expected = sign(encoded);

  const actualBuffer = Buffer.from(signature, "utf8");
  const expectedBuffer = Buffer.from(expected, "utf8");

  if (
    actualBuffer.length !== expectedBuffer.length ||
    !crypto.timingSafeEqual(actualBuffer, expectedBuffer)
  ) {
    return null;
  }

  try {
    const decoded = Buffer.from(encoded, "base64url").toString("utf8");
    const parsed = JSON.parse(decoded);

    if (parsed && typeof parsed === "object") {
      return parsed as T;
    }
  } catch {
    return null;
  }

  return null;
}
