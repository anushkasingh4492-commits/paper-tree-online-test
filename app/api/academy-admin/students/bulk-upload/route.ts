import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import bcrypt from "bcryptjs";
import { randomUUID } from "crypto";
import { pool } from "@/lib/db";
import { parseSessionCookie } from "@/lib/session";
import { ensureFeatureSchema } from "@/lib/feature-schema";

export const runtime = "nodejs";

function parseCsv(text: string) {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = "";
  let quote = false;

  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    const next = text[i + 1];

    if (ch === '"' && quote && next === '"') {
      cell += '"';
      i++;
      continue;
    }

    if (ch === '"') {
      quote = !quote;
      continue;
    }

    if (ch === "," && !quote) {
      row.push(cell.trim());
      cell = "";
      continue;
    }

    if ((ch === "\n" || ch === "\r") && !quote) {
      if (ch === "\r" && next === "\n") i++;

      row.push(cell.trim());
      cell = "";

      if (row.some(Boolean)) rows.push(row);

      row = [];
      continue;
    }

    cell += ch;
  }

  if (cell || row.length) {
    row.push(cell.trim());

    if (row.some(Boolean)) {
      rows.push(row);
    }
  }

  return rows;
}

async function getAdmin() {
  const raw = (await cookies()).get("master_session")?.value;
  const session = raw
    ? parseSessionCookie<Record<string, unknown>>(raw)
    : null;

  if (
    !session ||
    !["ACADEMY_ADMIN", "ADMIN", "MASTER_ADMIN"].includes(
      String(session.role)
    )
  ) {
    return null;
  }

  return session;
}

export async function POST(request: Request) {
  try {
    await ensureFeatureSchema();

    const admin = await getAdmin();

    if (!admin?.academyId) {
      return NextResponse.json(
        {
          success: false,
          error: "Academy admin login required.",
        },
        { status: 401 }
      );
    }

    const form = await request.formData();
    const file = form.get("file");
    const batchId = String(form.get("batchId") || "").trim();

    if (!(file instanceof File)) {
      return NextResponse.json(
        {
          success: false,
          error: "Upload an Excel/CSV file.",
        },
        { status: 400 }
      );
    }

    if (!batchId) {
      return NextResponse.json(
        {
          success: false,
          error: "Select a batch.",
        },
        { status: 400 }
      );
    }

    const batch = (
      await pool.query(
        `SELECT id
         FROM batches
         WHERE id = $1
           AND academy_id = $2
         LIMIT 1`,
        [batchId, admin.academyId]
      )
    ).rows[0];

    if (!batch) {
      return NextResponse.json(
        {
          success: false,
          error: "Batch not found.",
        },
        { status: 404 }
      );
    }

    const filename = file.name.toLowerCase();

    let rows: string[][];

    if (filename.endsWith(".csv")) {
      rows = parseCsv(await file.text());
    } else {
      try {
        const xlsx = await import("xlsx");
        const buffer = await file.arrayBuffer();

        const workbook = xlsx.read(buffer, {
          type: "array",
        });

        const first = workbook.Sheets[workbook.SheetNames[0]];

        rows = xlsx.utils.sheet_to_json(first, {
          header: 1,
          defval: "",
        }) as string[][];
      } catch {
        return NextResponse.json(
          {
            success: false,
            error:
              "Excel import needs the xlsx package. Run: npm install xlsx",
          },
          { status: 400 }
        );
      }
    }

    if (rows.length < 2) {
      return NextResponse.json(
        {
          success: false,
          error:
            "The file needs a header row and at least one student.",
        },
        { status: 400 }
      );
    }

    const headers = rows[0].map((h) =>
      String(h)
        .trim()
        .toLowerCase()
        .replace(/\s+/g, "_")
    );

    const idx = (names: string[]) =>
      names
        .map((name) => headers.indexOf(name))
        .find((index) => index >= 0) ?? -1;

    const nameIdx = idx(["name", "student_name"]);
    const emailIdx = idx(["email", "student_email"]);
    const passwordIdx = idx(["password", "student_password"]);

    const parentPhoneIdx = idx([
      "parent_phone",
      "parent_mobile",
      "parent_whatsapp",
    ]);

    const parentNameIdx = idx([
      "parent_name",
      "guardian_name",
    ]);

    // Password is mandatory for bulk upload.
    if (nameIdx < 0 || emailIdx < 0 || passwordIdx < 0) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Required columns: name, email, password. Optional: parent_phone, parent_name.",
        },
        { status: 400 }
      );
    }

    const created: string[] = [];
    const skipped: Array<{
      row: number;
      reason: string;
    }> = [];

    for (let i = 1; i < rows.length; i++) {
      const row = rows[i];

      const name = String(row[nameIdx] || "").trim();

      const email = String(row[emailIdx] || "")
        .trim()
        .toLowerCase();

      const password = String(row[passwordIdx] || "").trim();

      const parentPhone =
        parentPhoneIdx >= 0
          ? String(row[parentPhoneIdx] || "").trim()
          : "";

      const parentName =
        parentNameIdx >= 0
          ? String(row[parentNameIdx] || "").trim()
          : "";

      // Name, email and password are mandatory per student.
      if (!name || !email || !password) {
        skipped.push({
          row: i + 1,
          reason: "Missing name, email, or password",
        });
        continue;
      }

      const exists = await pool.query(
        `SELECT id
         FROM students
         WHERE LOWER(email) = $1
         LIMIT 1`,
        [email]
      );

      if (exists.rows[0]) {
        skipped.push({
          row: i + 1,
          reason: "Email already exists",
        });
        continue;
      }

      const studentId = randomUUID();

      const passwordHash = await bcrypt.hash(password, 10);

      await pool.query(
        `INSERT INTO students
          (id, name, email, academy_id)
         VALUES
          ($1, $2, $3, $4)`,
        [
          studentId,
          name,
          email,
          admin.academyId,
        ]
      );

      await pool.query(
        `INSERT INTO student_credentials
          (student_id, password_hash)
         VALUES
          ($1, $2)`,
        [
          studentId,
          passwordHash,
        ]
      );

      await pool.query(
        `UPDATE students
         SET parent_phone = $1,
             parent_name = $2
         WHERE id = $3`,
        [
          parentPhone || null,
          parentName || null,
          studentId,
        ]
      );

      await pool.query(
        `INSERT INTO batch_students
          (batch_id, student_id)
         VALUES
          ($1, $2)
         ON CONFLICT DO NOTHING`,
        [
          batchId,
          studentId,
        ]
      );

      created.push(email);
    }

    return NextResponse.json({
      success: true,
      createdCount: created.length,
      skippedCount: skipped.length,
      created,
      skipped,
    });
  } catch (error) {
    console.error(
      "BULK STUDENT UPLOAD ERROR",
      error
    );

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Bulk upload failed.",
      },
      { status: 500 }
    );
  }
}