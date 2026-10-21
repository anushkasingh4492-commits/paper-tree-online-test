import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import crypto from "crypto";
import XLSX from "xlsx";
import { parseSessionCookie } from "@/lib/session";
import { pool } from "@/lib/db";

export const runtime = "nodejs";

/* ============================================================
   DATASET UPLOAD
   ------------------------------------------------------------
   Lets a master admin upload a question-bank dataset together
   with course/subject metadata and import it into the questions
   table so students can see the new questions together with the
   existing ones.

   Accepts:
   1) multipart/form-data
      - file: .json | .csv | .xlsx | .xls
      - exam / course (e.g. MHT-CET, NEET, JEE, CAT)
      - subject (e.g. Physics, Chemistry, Biology, Maths)
      - standard (11 | 12), chapter, difficulty, releaseVersion (optional)
   2) application/json  (backward compatibility)
      { exam?, subject?, standard?, records: [...] }
   ============================================================ */

const EXAM_ALIASES: Record<string, string> = {
  "mht cet": "MHT-CET",
  mhtcet: "MHT-CET",
  "mht-cet": "MHT-CET",
  neet: "NEET",
  jee: "JEE",
  "jee main": "JEE",
  cat: "CAT",
};

function normalizeExam(value: unknown): string {
  const key = String(value ?? "").trim().toLowerCase();
  if (EXAM_ALIASES[key]) return EXAM_ALIASES[key];
  if (!key) return "MHT-CET";
  return String(value).trim();
}

function cleanText(value: unknown): string {
  return String(value ?? "").trim();
}

function safeStandard(value: unknown): number {
  if (value === null || value === undefined) return 11;
  const n = Number(String(value).trim());
  return Number.isFinite(n) ? Math.trunc(n) : 11;
}

function safeInt(value: unknown): number {
  if (value === null || value === undefined) return 0;
  const n = Number(String(value).trim());
  return Number.isFinite(n) ? Math.trunc(n) : 0;
}

function parseOptions(value: unknown): unknown {
  if (value === null || value === undefined) return {};
  if (typeof value === "string") {
    const trimmed = value.trim();
    if (!trimmed) return {};
    try {
      const parsed = JSON.parse(trimmed);
      return parsed === null || typeof parsed !== "object" ? {} : parsed;
    } catch {
      return {};
    }
  }
  if (Array.isArray(value)) {
    const obj: Record<string, string> = {};
    value.forEach((v, i) => {
      obj[String.fromCharCode(65 + i)] = String(v ?? "").trim();
    });
    return obj;
  }
  if (typeof value === "object") return value;
  return {};
}

function buildOptionsFromColumns(
  record: Record<string, unknown>
): Record<string, string> {
  const letters = ["A", "B", "C", "D", "E", "F"];
  const obj: Record<string, string> = {};

  for (const letter of letters) {
    const direct = cleanText(record[letter]);
    const alt = cleanText(record[`option_${letter}`]);
    const alt2 = cleanText(record[`option${letter}`]);
    const lower = cleanText(record[letter.toLowerCase()]);
    const value = direct || alt || alt2 || lower;
    if (value) obj[letter] = value;
  }

  return Object.keys(obj).length ? obj : {};
}

function normalizeQuestion(
  record: Record<string, unknown>,
  defaults: {
    exam: string;
    subject: string;
    standard: number;
    chapter?: string;
    difficulty?: string;
    releaseVersion?: string;
  }
): {
  id: string;
  exam: string;
  subject: string;
  standard: number;
  chapterNumber: number;
  chapterName: string;
  majorTopic: string;
  subtopic: string;
  conceptTested: string;
  stem: string;
  options: unknown;
  correctOption: string;
  correctAnswerText: string;
  solution: string;
  formulaPrinciple: string;
  difficulty: string;
  estimatedTime: string;
  questionType: string;
  figureAsset: string;
  syllabusScopeStatus: string;
  syllabusVersion: string;
  releaseVersion: string;
  rawData: Record<string, unknown>;
} {
  const id = cleanText(record.id || record.question_id || crypto.randomUUID());
  const exam = normalizeExam(
    defaults.exam ||
      record.exam ||
      record.exam_name ||
      record.course
  );
  const subject = cleanText(
    defaults.subject || record.subject || record.subject_name || ""
  );
  const standard = safeStandard(
    defaults.standard !== undefined
      ? defaults.standard
      : record.standard ?? record.standard_class ?? record.class
  );
  const chapterNumber = safeInt(
    record.chapter_number ?? record.chapterNumber ?? record.unit_number
  );
  const chapterName = cleanText(
    defaults.chapter ||
      record.chapter_name ||
      record.chapterName ||
      record.chapter ||
      record.unit ||
      ""
  );
  const majorTopic = cleanText(
    record.major_topic ?? record.majorTopic ?? record.topic ?? ""
  );
  const subtopic = cleanText(record.subtopic ?? record.subTopic ?? "");
  const conceptTested = cleanText(
    record.concept_tested ??
    record.conceptTested ??
    record.cognitive_level ??
    record.tags ??
    ""
  );
  const stem = cleanText(
    record.stem ?? record.question ?? record.text ?? record.statement ?? ""
  );
  const options =
    record.options !== undefined && record.options !== null
      ? parseOptions(record.options)
      : buildOptionsFromColumns(record);
  const correctOption = cleanText(
    record.correct_option ??
    record.correctOption ??
    record.answer ??
    record.correctAnswer ??
    ""
  ).toUpperCase();
  const correctAnswerText = cleanText(
    record.correct_answer_text ??
    record.correctAnswerText ??
    record.correct_answer ??
    record.correctAnswer ??
    record.explanation ??
    ""
  );
  const solution = cleanText(
    record.solution ?? record.explanation ?? record.solution_text ?? ""
  );
  const formulaPrinciple = cleanText(
    record.formula_principle ?? record.formulaPrinciple ?? ""
  );
  const difficulty = cleanText(defaults.difficulty ?? record.difficulty) || "Medium";
  const estimatedTime = cleanText(
    record.estimated_time ?? record.estimatedTime ?? record.time ?? ""
  );
  const questionType = cleanText(
    record.question_type ?? record.questionType ?? "MCQ"
  );
  const figureAsset = cleanText(record.figure_asset ?? record.figureAsset ?? "");
  const syllabusScopeStatus = cleanText(
    record.syllabus_scope_status ?? record.syllabusScopeStatus ?? ""
  );
  const syllabusVersion = cleanText(
    defaults.releaseVersion ??
      record.syllabus_version ??
      record.syllabusVersion ??
      record.release_version ??
      record.releaseVersion ??
      ""
  );
  const releaseVersion = cleanText(
    record.release_version ??
      record.releaseVersion ??
      defaults.releaseVersion ??
      ""
  );

  return {
    id,
    exam,
    subject,
    standard,
    chapterNumber,
    chapterName,
    majorTopic,
    subtopic,
    conceptTested,
    stem,
    options,
    correctOption,
    correctAnswerText,
    solution,
    formulaPrinciple,
    difficulty,
    estimatedTime,
    questionType,
    figureAsset,
    syllabusScopeStatus,
    syllabusVersion,
    releaseVersion,
    rawData: record,
  };
}
async function ensureImportHistoryTable(): Promise<void> {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS dataset_imports (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      file_name TEXT NOT NULL,
      file_type TEXT,
      exam VARCHAR(50),
      subject VARCHAR(100),
      standard INTEGER,
      total_records INTEGER NOT NULL DEFAULT 0,
      inserted INTEGER NOT NULL DEFAULT 0,
      updated INTEGER NOT NULL DEFAULT 0,
      skipped INTEGER NOT NULL DEFAULT 0,
      errors JSONB NOT NULL DEFAULT '[]'::jsonb,
      imported_by UUID REFERENCES users(id) ON DELETE SET NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )
  `);

  await pool.query(`
    CREATE INDEX IF NOT EXISTS dataset_imports_created_at_idx
    ON dataset_imports(created_at DESC)
  `);

  await pool.query(`
    CREATE INDEX IF NOT EXISTS dataset_imports_exam_subject_idx
    ON dataset_imports(exam, subject)
  `);
}

function parseJsonFile(text: string): Record<string, unknown>[] {
  const parsed = JSON.parse(text);

  if (Array.isArray(parsed)) {
    return parsed.filter(
      (item) => item && typeof item === "object"
    ) as Record<string, unknown>[];
  }

  if (parsed && typeof parsed === "object") {
    const obj = parsed as Record<string, unknown>;

    if (Array.isArray(obj.records)) {
      return obj.records.filter(
        (item) => item && typeof item === "object"
      ) as Record<string, unknown>[];
    }

    if (Array.isArray(obj.questions)) {
      return obj.questions.filter(
        (item) => item && typeof item === "object"
      ) as Record<string, unknown>[];
    }

    return [obj];
  }

  throw new Error("JSON dataset must contain an array of questions or a { records } object.");
}

/* Very small CSV parser that handles quoted fields with embedded commas. */
function parseCsvText(text: string): Record<string, unknown>[] {
  const lines: string[] = [];
  let current = "";
  inQuotes: for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (ch === "\"") {
      current += ch;
      i++;
      while (i < text.length) {
        current += text[i];
        if (text[i] === "\"") {
          if (i + 1 < text.length && text[i + 1] === "\"") {
            current += text[i + 1];
            i++;
            continue;
          }
          break;
        }
      }
      continue;
    }
    if (ch === "\n") {
      lines.push(current);
      current = "";
      continue;
    }
    if (ch === "\r") continue;
    current += ch;
  }
  if (current.trim()) lines.push(current);

  if (lines.length === 0) return [];

  const headerLine = lines[0];
  const headers = parseCsvRow(headerLine).map((h) => h.trim());

  const rows: Record<string, unknown>[] = [];
  for (let i = 1; i < lines.length; i++) {
    if (!lines[i].trim()) continue;
    const values = parseCsvRow(lines[i]);
    const row: Record<string, unknown> = {};
    headers.forEach((header, index) => {
      if (header) row[header] = values[index] ?? "";
    });
    rows.push(row);
  }

  return rows;
}

function parseCsvRow(line: string): string[] {
  const fields: string[] = [];
  let current = "";
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const ch = line[i];

    if (inQuotes) {
      if (ch === "\"") {
        if (i + 1 < line.length && line[i + 1] === "\"") {
          current += "\"";
          i++;
          continue;
        }
        inQuotes = false;
        continue;
      }
      current += ch;
      continue;
    }

    if (ch === "\"") {
      inQuotes = true;
      continue;
    }

    if (ch === ",") {
      fields.push(current);
      current = "";
      continue;
    }

    current += ch;
  }

  fields.push(current);
  return fields;
}
function parseXlsxBuffer(buffer: Buffer): Record<string, unknown>[] {
  const workbook = XLSX.read(buffer, { type: "buffer", cellDates: true });
  const firstSheet = workbook.SheetNames[0];
  const worksheet = workbook.Sheets[firstSheet];
  const rows = XLSX.utils.sheet_to_json(worksheet, {
    defval: "",
    raw: false,
  }) as Record<string, unknown>[];

  return rows.filter((row) => row && typeof row === "object");
}

function detectFileType(fileName: string, contentType?: string): string {
  const name = fileName.toLowerCase();
  if (name.endsWith(".json")) return "application/json";
  if (name.endsWith(".csv")) return "text/csv";
  if (name.endsWith(".xlsx"))
    return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
  if (name.endsWith(".xls")) return "application/vnd.ms-excel";
  return contentType || "application/octet-stream";
}

async function parseUploadedFile(
  file: File
): Promise<Record<string, unknown>[]> {
  const arrayBuffer = await file.arrayBuffer();
  const buffer = Buffer.from(arrayBuffer);
  const fileType = detectFileType(file.name, file.type);

  switch (fileType) {
    case "application/json":
      return parseJsonFile(buffer.toString("utf8"));
    case "text/csv":
      return parseCsvText(buffer.toString("utf8"));
    case "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
    case "application/vnd.ms-excel":
      return parseXlsxBuffer(buffer);
    default:
      throw new Error(
        `Unsupported file type: ${fileType}. Please upload .json, .csv, or .xlsx/.xls.`
      );
  }
}
export async function POST(request: Request): Promise<NextResponse> {
  try {
    const cookieStore = await cookies();
    const sessionCookie = cookieStore.get("master_session")?.value;

    if (!sessionCookie) {
      return NextResponse.json(
        { success: false, error: "Admin is not logged in." },
        { status: 401 }
      );
    }

    let session: { id?: string; role?: string };

    try {
      session =
        parseSessionCookie<{ id?: string; role?: string }>(sessionCookie) || {};
    } catch {
      return NextResponse.json(
        { success: false, error: "Invalid admin session." },
        { status: 401 }
      );
    }

    if (session.role !== "ADMIN") {
      return NextResponse.json(
        { success: false, error: "Admin access required." },
        { status: 403 }
      );
    }

    await ensureImportHistoryTable();

    let metadata: {
      exam: string;
      subject: string;
      standard: number;
      chapter?: string;
      difficulty?: string;
      releaseVersion?: string;
    };
    let fileName: string;
    let records: Record<string, unknown>[];

    const contentType = request.headers.get("content-type") ?? "";

    if (contentType.includes("multipart/form-data")) {
      const formData = await request.formData();
      const file = formData.get("file") as File | null;

      if (!file) {
        return NextResponse.json(
          { success: false, error: "No file was uploaded." },
          { status: 400 }
        );
      }

      const exam = normalizeExam(
        formData.get("exam") ?? formData.get("course")
      );
      const subject = cleanText(formData.get("subject"));
      if (!subject) {
        return NextResponse.json(
          { success: false, error: "Subject is required." },
          { status: 400 }
        );
      }

      metadata = {
        exam,
        subject,
        standard: safeStandard(formData.get("standard")),
        chapter: cleanText(formData.get("chapter")) || undefined,
        difficulty: cleanText(formData.get("difficulty")) || undefined,
        releaseVersion: cleanText(
          formData.get("releaseVersion") ?? formData.get("release_version")
        ) || undefined,
      };

      fileName = file.name;
      records = await parseUploadedFile(file);
    } else {
      // Backward-compatible JSON body: { exam?, subject?, standard?, records: [...] }
      let body: unknown;

      try {
        body = await request.json();
      } catch {
        return NextResponse.json(
          { success: false, error: "Invalid JSON body." },
          { status: 400 }
        );
      }

      if (!body || typeof body !== "object") {
        return NextResponse.json(
          { success: false, error: "Invalid dataset payload." },
          { status: 400 }
        );
      }

      const obj = body as Record<string, unknown>;

      if (!Array.isArray(obj.records)) {
        return NextResponse.json(
          { success: false, error: 'Dataset must contain a "records" array.' },
          { status: 400 }
        );
      }

      metadata = {
        exam: normalizeExam(obj.exam),
        subject: cleanText(obj.subject),
        standard: safeStandard(obj.standard),
        chapter: cleanText(obj.chapter) || undefined,
        difficulty: cleanText(obj.difficulty) || undefined,
        releaseVersion: cleanText(obj.releaseVersion) || undefined,
      };

      if (!metadata.subject) {
        return NextResponse.json(
          { success: false, error: "Subject is required." },
          { status: 400 }
        );
      }

      fileName = "json-upload";
      records = obj.records.filter(
        (item) => item && typeof item === "object"
      ) as Record<string, unknown>[];
    }

    const totalRecords = records.length;
    const errors: Array<{ row?: number; reason: string }> = [];
    let inserted = 0;
    let updated = 0;
    let skipped = 0;

    const client = await pool.connect();

    try {
      await client.query("BEGIN");

      const upsertSql = `
        INSERT INTO questions (
          id, exam, subject, standard, chapter_number, chapter_name,
          major_topic, subtopic, concept_tested, stem, options,
          correct_option, correct_answer_text, solution,
          formula_principle, difficulty, estimated_time, question_type,
          figure_asset, syllabus_scope_status, syllabus_version,
          release_version, raw_data
        )
        VALUES (
          $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11::jsonb,$12,$13,$14,$15,
          $16,$17,$18,$19,$20,$21,$22,$23::jsonb
        )
        ON CONFLICT (id) DO UPDATE SET
          exam = EXCLUDED.exam,
          subject = EXCLUDED.subject,
          standard = EXCLUDED.standard,
          chapter_number = EXCLUDED.chapter_number,
          chapter_name = EXCLUDED.chapter_name,
          major_topic = EXCLUDED.major_topic,
          subtopic = EXCLUDED.subtopic,
          concept_tested = EXCLUDED.concept_tested,
          stem = EXCLUDED.stem,
          options = EXCLUDED.options,
          correct_option = EXCLUDED.correct_option,
          correct_answer_text = EXCLUDED.correct_answer_text,
          solution = EXCLUDED.solution,
          formula_principle = EXCLUDED.formula_principle,
          difficulty = EXCLUDED.difficulty,
          estimated_time = EXCLUDED.estimated_time,
          question_type = EXCLUDED.question_type,
          figure_asset = EXCLUDED.figure_asset,
          syllabus_scope_status = EXCLUDED.syllabus_scope_status,
          syllabus_version = EXCLUDED.syllabus_version,
          release_version = EXCLUDED.release_version,
          raw_data = EXCLUDED.raw_data
      `;
      for (let i = 0; i < records.length; i++) {
        const record = records[i];
        const rowNumber = i + 2;

        try {
          const normalized = normalizeQuestion(record, metadata);

          if (!normalized.stem) {
            skipped++;
            errors.push({
              row: rowNumber,
              reason: "Missing stem/question text.",
            });
            continue;
          }

          const existedBefore = await client.query(
            `SELECT 1 FROM questions WHERE id = $1 LIMIT 1`,
            [normalized.id]
          );

          const rawPayload = {
            ...normalized.rawData,
            _import: {
              fileName,
              importedAt: new Date().toISOString(),
              importedBy: session.id,
            },
          };

          await client.query(upsertSql, [
            normalized.id,
            normalized.exam,
            normalized.subject,
            normalized.standard,
            normalized.chapterNumber,
            normalized.chapterName,
            normalized.majorTopic,
            normalized.subtopic,
            normalized.conceptTested,
            normalized.stem,
            JSON.stringify(normalized.options),
            normalized.correctOption,
            normalized.correctAnswerText,
            normalized.solution,
            normalized.formulaPrinciple,
            normalized.difficulty,
            normalized.estimatedTime,
            normalized.questionType,
            normalized.figureAsset,
            normalized.syllabusScopeStatus,
            normalized.syllabusVersion,
            normalized.releaseVersion,
            JSON.stringify(rawPayload),
          ]);

          if (existedBefore.rows.length > 0) {
            updated++;
          } else {
            inserted++;
          }
        } catch (error) {
          skipped++;
          errors.push({
            row: rowNumber,
            reason:
              error instanceof Error ? error.message : "Import failed.",
          });
        }
      }

      await client.query(
        `
        INSERT INTO dataset_imports (
          file_name, file_type, exam, subject, standard,
          total_records, inserted, updated, skipped, errors, imported_by
        )
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)
        RETURNING id
      `,
        [
          fileName,
          detectFileType(
            fileName,
            contentType.includes("multipart/form-data")
              ? undefined
              : "application/json"
          ),
          metadata.exam,
          metadata.subject,
          metadata.standard,
          totalRecords,
          inserted,
          updated,
          skipped,
          JSON.stringify(errors.slice(0, 50)),
          session.id ?? null,
        ]
      );

      await client.query("COMMIT");
    } catch (error) {
      await client.query("ROLLBACK");
      throw error;
    } finally {
      client.release();
    }

    return NextResponse.json({
      success: true,
      message: `Dataset imported: ${inserted} added, ${updated} updated, ${skipped} skipped.`,
      import: {
        fileName,
        exam: metadata.exam,
        subject: metadata.subject,
        totalRecords,
        inserted,
        updated,
        skipped,
        errors: errors.slice(0, 10),
      },
    });
  } catch (error) {
    console.error("DATASET UPLOAD ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error
            ? error.message
            : "Dataset upload failed.",
      },
      { status: 500 }
    );
  }
}
export async function GET(request: Request): Promise<NextResponse> {
  try {
    const cookieStore = await cookies();
    const sessionCookie = cookieStore.get("master_session")?.value;

    if (!sessionCookie) {
      return NextResponse.json(
        { success: false, error: "Admin is not logged in." },
        { status: 401 }
      );
    }

    let session: { id?: string; role?: string };

    try {
      session =
        parseSessionCookie<{ id?: string; role?: string }>(sessionCookie) || {};
    } catch {
      return NextResponse.json(
        { success: false, error: "Invalid admin session." },
        { status: 401 }
      );
    }

    if (session.role !== "ADMIN") {
      return NextResponse.json(
        { success: false, error: "Admin access required." },
        { status: 403 }
      );
    }

    await ensureImportHistoryTable();

    const { searchParams } = new URL(request.url);
    const limit = Math.min(
      Math.max(Number(searchParams.get("limit")) || 20, 1),
      100
    );
    const offset = Math.max(Number(searchParams.get("offset")) || 0, 0);

    const [rows, countResult] = await Promise.all([
      pool.query(
        `
        SELECT
          id, file_name, file_type, exam, subject, standard,
          total_records, inserted, updated, skipped, errors,
          imported_by, created_at
        FROM dataset_imports
        ORDER BY created_at DESC
        LIMIT $1 OFFSET $2
      `,
        [limit, offset]
      ),
      pool.query(`SELECT COUNT(*)::int AS count FROM dataset_imports`),
    ]);

    return NextResponse.json({
      success: true,
      imports: rows.rows,
      total: countResult.rows[0].count,
      limit,
      offset,
    });
  } catch (error) {
    console.error("DATASET LIST ERROR:", error);

    return NextResponse.json(
      {
        success: false,
        error:
          error instanceof Error ? error.message : "Could not list imports.",
      },
      { status: 500 }
    );
  }
}