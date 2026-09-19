import { readFile } from "node:fs/promises";
import path from "node:path";
import { NextResponse } from "next/server";

const DATA_ROOT = path.join(process.cwd(), "data");
const MIME_TYPES: Record<string, string> = {
  ".gif": "image/gif",
  ".jpeg": "image/jpeg",
  ".jpg": "image/jpeg",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".webp": "image/webp",
};

export const runtime = "nodejs";

export async function GET(request: Request) {
  const assetPath = new URL(request.url).searchParams.get("path")?.trim();
  if (!assetPath || assetPath.includes("\\") || assetPath.includes("..")) {
    return new NextResponse("Not found", { status: 404 });
  }

  const matches = await Promise.all([
    readFile(path.join(DATA_ROOT, "mht-cet", "biology", assetPath)).catch(() => null),
    readFile(path.join(DATA_ROOT, "mht-cet", "chemistry", assetPath)).catch(() => null),
    readFile(path.join(DATA_ROOT, "mht-cet", "maths", assetPath)).catch(() => null),
    readFile(path.join(DATA_ROOT, "mht-cet", "physics", assetPath)).catch(() => null),
    readFile(path.join(DATA_ROOT, "neet", "biology", assetPath)).catch(() => null),
    readFile(path.join(DATA_ROOT, "neet", "chemistry", assetPath)).catch(() => null),
    readFile(path.join(DATA_ROOT, "neet", "physics", assetPath)).catch(() => null),
  ]);

  const file = matches.find((candidate) => candidate !== null);
  if (!file) return new NextResponse("Not found", { status: 404 });

  const extension = path.extname(assetPath).toLowerCase();
  return new NextResponse(new Uint8Array(file), {
    headers: {
      "Cache-Control": "public, max-age=3600",
      "Content-Type": MIME_TYPES[extension] || "application/octet-stream",
    },
  });
}