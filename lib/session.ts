export function parseSessionCookie<T extends Record<string, unknown>>(
  value: string
): T | null {
  const candidates = [value];

  try {
    candidates.push(decodeURIComponent(value));
  } catch {
    // Keep the original value when it is not URI encoded.
  }

  for (const candidate of candidates) {
    try {
      const parsed = JSON.parse(candidate);

      if (parsed && typeof parsed === "object") {
        return parsed as T;
      }
    } catch {
      // Try the next representation.
    }
  }

  return null;
}
