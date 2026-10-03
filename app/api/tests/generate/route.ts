import { cookies } from "next/headers";
import { parseSessionCookie } from "@/lib/session";
import { checkRateLimit } from "@/lib/rate-limit";
import { pool } from "@/lib/db";
import { getAcademySubscription } from "@/lib/subscription";
import { ensureFeatureSchema } from "@/lib/feature-schema";
import {
  getPreset,
  type Preset,
  type PresetSubject,
} from "@/lib/test-presets";

export const runtime = "nodejs";

/*
 * =========================================================
 * TYPES
 * =========================================================
 */

type GenerateRequest = {
  exam?: string;
  course?: string;

  subject?: string;
  subjects?: string[];

  chapters?: string[];
  chaptersBySubject?: Record<string, string[]>;

  difficulty?: string;

  presetId?: string;

  /*
   * Exact question selection from Teacher Generate page.
   */
  questionIds?: string[];

  /*
   * Used by Teacher Generate page to preview every
   * matching question without creating a test.
   */
  previewOnly?: boolean;
  previewOffset?: number;
  previewLimit?: number;

  // Backward compatibility
  questionCount?: number;
  duration?: number;
};

type QuestionRow = {
  id: string;
  exam: string;
  subject: string;
  standard?: string | null;
  chapter_number?: string | number | null;
  chapter_name?: string | null;
  major_topic?: string | null;
  subtopic?: string | null;
  concept_tested?: string | null;
  stem?: string | null;
  options?: unknown;
  correct_option?: string | number | null;
  correct_answer_text?: string | null;
  solution?: string | null;
  formula_principle?: string | null;
  difficulty?: string | null;
  estimated_time?: number | null;
  question_type?: string | null;
  figure_asset?: string | null;
};

/*
 * =========================================================
 * BASIC HELPERS
 * =========================================================
 */

function clean(value: unknown): string {
  return String(value ?? "").trim();
}

function normalize(value: unknown): string {
  return clean(value)
    .toLowerCase()
    .replace(/[_-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

/*
 * =========================================================
 * EXAM NORMALIZATION
 * =========================================================
 */

function normalizeExam(value: unknown): string {
  const exam = normalize(value);

  if (
    exam === "mht cet" ||
    exam === "mhtcet" ||
    exam === "mht cet exam" ||
    exam === "mht cet 2026"
  ) {
    return "MHT-CET";
  }

  if (
    exam === "neet" ||
    exam === "neet exam" ||
    exam === "neet 2026"
  ) {
    return "NEET";
  }

  if (!exam) {
    return "MHT-CET";
  }

  return clean(value);
}

/*
 * =========================================================
 * DATABASE EXAM CONDITION
 * =========================================================
 */

function addExamFilter(
  exam: string,
  conditions: string[],
  values: unknown[]
) {
  const normalizedExam = normalizeExam(exam);

  const examParam = values.length + 1;

  values.push(normalizedExam);

  /*
   * MHT-CET
   *
   * Matches:
   * MHT-CET
   * MHT CET
   * MHTCET
   */
  if (normalizedExam === "MHT-CET") {
    conditions.push(`
      LOWER(
        REGEXP_REPLACE(
          TRIM(exam),
          '[_ -]+',
          '',
          'g'
        )
      )
      =
      LOWER(
        REGEXP_REPLACE(
          $${examParam}::text,
          '[_ -]+',
          '',
          'g'
        )
      )
    `);

    return;
  }

  /*
   * NEET
   */
  if (normalizedExam === "NEET") {
    conditions.push(`
      LOWER(TRIM(exam))
      =
      LOWER($${examParam}::text)
    `);

    return;
  }

  /*
   * OTHER EXAMS
   */
  conditions.push(`
    LOWER(TRIM(exam))
    =
    LOWER($${examParam}::text)
  `);
}

/*
 * =========================================================
 * SUBJECT NORMALIZATION
 * =========================================================
 */

function normalizePresetSubject(
  value: unknown
): PresetSubject | null {
  const subject = normalize(value);

  if (subject === "physics") {
    return "physics";
  }

  if (subject === "chemistry") {
    return "chemistry";
  }

  if (
    subject === "maths" ||
    subject === "math" ||
    subject === "mathematics"
  ) {
    return "maths";
  }

  if (subject === "biology") {
    return "biology";
  }

  return null;
}

/*
 * =========================================================
 * DATABASE SUBJECT NAME
 * =========================================================
 */

function displaySubject(
  subject: PresetSubject
): string {
  switch (subject) {
    case "physics":
      return "Physics";

    case "chemistry":
      return "Chemistry";

    case "maths":
      return "Mathematics";

    case "biology":
      return "Biology";

    default:
      return subject;
  }
}

/*
 * =========================================================
 * SUBJECT DATABASE CONDITION
 * =========================================================
 */

function addSubjectFilter(
  subject: string,
  conditions: string[],
  values: unknown[]
) {
  const normalizedSubject =
    normalizePresetSubject(subject);

  let databaseSubject = clean(subject);

  if (normalizedSubject) {
    databaseSubject =
      displaySubject(normalizedSubject);
  }

  const subjectParam =
    values.length + 1;

  values.push(
    normalize(databaseSubject)
  );

  conditions.push(`
    LOWER(
      REGEXP_REPLACE(
        TRIM(subject),
        '[_-]+',
        ' ',
        'g'
      )
    ) =
    $${subjectParam}
  `);
}

/*
 * =========================================================
 * DIFFICULTY FILTER
 * =========================================================
 */

function addDifficultyFilter(
  difficulty: string,
  conditions: string[]
) {
  const normalizedDifficulty = normalize(difficulty);

  /*
   * Easy
   */
  if (normalizedDifficulty === "easy") {
    conditions.push(`
      LOWER(TRIM(difficulty)) = 'easy'
    `);

    return;
  }

  /*
   * Medium
   */
  if (normalizedDifficulty === "medium") {
    conditions.push(`
      LOWER(TRIM(difficulty)) = 'medium'
    `);

    return;
  }

  /*
   * Hard
   */
  if (
    normalizedDifficulty === "hard" ||
    normalizedDifficulty === "difficult"
  ) {
    conditions.push(`
      LOWER(TRIM(difficulty)) = 'hard'
    `);

    return;
  }

  /*
   * Challenging
   */
  if (normalizedDifficulty === "challenging") {
    conditions.push(`
      LOWER(TRIM(difficulty)) = 'challenging'
    `);

    return;
  }

  
}

/*
 * =========================================================
 * CHAPTER FILTER
 * =========================================================
 */

function addChapterFilter(
  chapters: string[],
  conditions: string[],
  values: unknown[]
) {
  const validChapters =
    chapters
      .map(clean)
      .filter(Boolean);

  if (validChapters.length === 0) {
    return;
  }

  const chapterParams =
    validChapters.map(
      (chapter) => {
        const param =
          values.length + 1;

        values.push(
          normalize(chapter)
        );

        return `$${param}`;
      }
    );

  conditions.push(`
    LOWER(
      REGEXP_REPLACE(
        TRIM(chapter_name),
        '[_-]+',
        ' ',
        'g'
      )
    )
    = ANY(
      ARRAY[
        ${chapterParams.join(", ")}
      ]::text[]
    )
  `);
}

/*
 * =========================================================
 * SUBJECT + CHAPTER FILTER
 * =========================================================
 *
 * Normal mode:
 *
 * subjects = Physics
 * chapters = Current Electricity
 *
 * => Physics + Current Electricity
 *
 * If chaptersBySubject is supplied, preserve the
 * subject/chapter relationship.
 * =========================================================
 */

function addSubjectChapterFilters(
  values: unknown[],
  conditions: string[],
  chaptersBySubject:
    | Record<string, string[]>
    | undefined,
  subjects: string[],
  chapters: string[]
) {
  /*
   * If subject-specific chapter selections are supplied, build
   * an OR group where each selected subject keeps its own
   * chapter filter. A subject with no selected chapters means
   * all chapters for that subject.
   */
  if (
    chaptersBySubject &&
    Object.keys(chaptersBySubject).length > 0 &&
    subjects.length > 0
  ) {
    const selectedSubjectPairs = subjects.map((subject) => {
      const entry = Object.entries(chaptersBySubject).find(
        ([entrySubject]) =>
          normalize(entrySubject) === normalize(subject)
      );

      const selectedChaptersForSubject =
        entry && Array.isArray(entry[1])
          ? entry[1].map(clean).filter(Boolean)
          : [];

      return {
        subject: normalize(subject),
        chapters: selectedChaptersForSubject,
      };
    });

    const subjectConditions = selectedSubjectPairs.map(
      ({ subject, chapters: subjectChapters }) => {
        const subjectParam = values.length + 1;
        values.push(subject);

        const subjectParts = [
          `
            LOWER(
              REGEXP_REPLACE(
                TRIM(subject),
                '[_-]+',
                ' ',
                'g'
              )
            ) = $${subjectParam}
          `,
        ];

        if (subjectChapters.length > 0) {
          const chapterParams = subjectChapters.map((chapter) => {
            const chapterParam = values.length + 1;
            values.push(normalize(chapter));
            return `$${chapterParam}`;
          });

          subjectParts.push(`
            LOWER(
              REGEXP_REPLACE(
                TRIM(chapter_name),
                '[_-]+',
                ' ',
                'g'
              )
            ) = ANY(
              ARRAY[
                ${chapterParams.join(", ")}
              ]::text[]
            )
          `);
        }

        return `(${subjectParts.join(" AND ")})`;
      }
    );

    if (subjectConditions.length > 0) {
      conditions.push(`
        (
          ${subjectConditions.join(" OR ")}
        )
      `);
      return;
    }
  }

  /*
   * Backward-compatible normal filtering.
   */
  if (subjects.length > 0) {
    const subjectValues = subjects.map(normalize);
    values.push(subjectValues);

    conditions.push(`
      LOWER(
        REGEXP_REPLACE(
          TRIM(subject),
          '[_-]+',
          ' ',
          'g'
        )
      )
      = ANY(
        $${values.length}::text[]
      )
    `);
  }

  addChapterFilter(chapters, conditions, values);
}

/*
 * =========================================================
 * QUESTION SELECT
 * =========================================================
 */

const QUESTION_SELECT = `
  SELECT
    id,
    exam,
    subject,
    standard,
    chapter_number,
    chapter_name,
    major_topic,
    subtopic,
    concept_tested,
    stem,
    options,
    correct_option,
    correct_answer_text,
    solution,
    formula_principle,
    difficulty,
    estimated_time,
    question_type,
    figure_asset
  FROM questions
`;

/*
 * =========================================================
 * MAIN POST
 * =========================================================
 */

export async function POST(
  request: Request
) {
  try {
    /*
     * -------------------------------------------------------
     * DATABASE CHECK
     * -------------------------------------------------------
     */

    if (!process.env.DATABASE_URL) {
      return Response.json(
        {
          success: false,
          error:
            "DATABASE_URL is not configured.",
        },
        { status: 500 }
      );
    }

    /*
     * -------------------------------------------------------
     * SESSION
     * -------------------------------------------------------
     *
     * Student sessions are still supported.
     *
     * master_session is now accepted regardless of role.
     *
     * Previously the route only accepted:
     *
     * parsed.role === "TEACHER"
     *
     * That restriction has been removed.
     * -------------------------------------------------------
     */

    const cookieStore =
      await cookies();

    const studentSession =
      cookieStore.get(
        "student_session"
      )?.value;

    const masterSession =
      cookieStore.get(
        "master_session"
      )?.value;

    let studentId = "";
    let masterUserId = "";
    let masterRole = "";
    let academyId = "";

    /*
     * Student session
     */
    if (studentSession) {
      try {
        const parsed =
          parseSessionCookie<Record<string, unknown>>(studentSession);

        studentId = String(
          parsed?.studentId ?? ""
        ).trim();
        academyId = String(
          parsed?.academyId ?? ""
        ).trim();
      } catch {
        studentId = "";
        academyId = "";
      }
    }

    /*
     * Master session
     *
     * NO ROLE CHECK.
     */
    if (
      !studentId &&
      masterSession
    ) {
      try {
        const parsed =
          parseSessionCookie<Record<string, unknown>>(masterSession);

        masterRole = String(parsed?.role ?? "").trim().toUpperCase();
        masterUserId = String(
          parsed?.id ??
          parsed?.userId ??
          parsed?.masterId ??
          "master"
        ).trim();
        academyId = String(
          parsed?.academyId ?? ""
        ).trim();
      } catch {
        masterUserId = "";
        academyId = "";
      }
    }

    /*
     * Authentication is still required.
     */
    if (
      !studentId &&
      !masterUserId
    ) {
      return Response.json(
        {
          success: false,
          error:
            "Please log in before generating a paper.",
        },
        { status: 401 }
      );
    }

    if (academyId) {
      const subscription = await getAcademySubscription(academyId);

      if (masterRole === "TEACHER" && !subscription.features.autoGeneratedPapers) {
        return Response.json(
          { success: false, error: "This paper generation feature is not available for this academy." },
          { status: 403 }
        );
      }

      if (studentId && subscription.limits.selfTestsPerStudentPerMonth !== null) {
        await ensureFeatureSchema();
        const usage = await pool.query(
          `SELECT COUNT(*)::int AS count
           FROM student_tests
           WHERE student_id = $1
             AND created_at >= date_trunc('month', NOW())`,
          [studentId]
        );
        const used = Number(usage.rows[0]?.count || 0);
        const limit = subscription.limits.selfTestsPerStudentPerMonth;

        if (used >= limit) {
          return Response.json(
            { success: false, error: "Your monthly self-test allowance has been reached." },
            { status: 429 }
          );
        }
      }
    }

    const requesterKey = studentId
      ? `student:${studentId}`
      : masterUserId
        ? `staff:${masterUserId}`
        : `ip:${request.headers.get("x-forwarded-for")?.split(",")[0]?.trim() || "unknown"}`;

    const rate = checkRateLimit(requesterKey, studentId ? 20 : 60, 10 * 60 * 1000);

    if (!rate.allowed) {
      return Response.json(
        {
          success: false,
          error: "Too many test-generation requests. Please try again later.",
          retryAfterSeconds: rate.retryAfterSeconds,
        },
        {
          status: 429,
          headers: {
            "Retry-After": String(rate.retryAfterSeconds),
          },
        }
      );
    }

    /*
     * -------------------------------------------------------
     * REQUEST BODY
     * -------------------------------------------------------
     */

    const body =
      (await request.json()) as GenerateRequest;

    /*
     * -------------------------------------------------------
     * EXAM
     * -------------------------------------------------------
     */

    const exam =
      normalizeExam(
        body.exam ||
          body.course ||
          "MHT-CET"
      );

    /*
     * -------------------------------------------------------
     * SUBJECTS
     * -------------------------------------------------------
     */

    const subjects =
      Array.isArray(body.subjects)
        ? body.subjects
            .map(clean)
            .filter(Boolean)
        : body.subject
          ? [clean(body.subject)]
          : [];

    /*
     * -------------------------------------------------------
     * CHAPTERS
     * -------------------------------------------------------
     */

    const chapters =
      Array.isArray(body.chapters)
        ? body.chapters
            .map(clean)
            .filter(Boolean)
        : [];

    /*
     * -------------------------------------------------------
     * DIFFICULTY
     * -------------------------------------------------------
     */

    const difficulty =
      clean(body.difficulty) ||
      "Balanced";

    /*
     * -------------------------------------------------------
     * PRESET
     * -------------------------------------------------------
     */

    const presetId =
      clean(body.presetId);

    let preset: Preset | undefined;

    if (presetId) {
      preset =
        getPreset(presetId);

      if (!preset) {
        return Response.json(
          {
            success: false,
            error:
              "Invalid test preset.",
          },
          { status: 400 }
        );
      }
    }

    /*
     * -------------------------------------------------------
     * EXACT QUESTION IDS
     * -------------------------------------------------------
     */

    const requestedQuestionIds =
      Array.isArray(body.questionIds)
        ? body.questionIds
            .map(clean)
            .filter(Boolean)
        : [];

    /*
     * If questionIds are provided, duplicates are invalid.
     */
    if (
      requestedQuestionIds.length > 0 &&
      new Set(
        requestedQuestionIds
      ).size !==
        requestedQuestionIds.length
    ) {
      return Response.json(
        {
          success: false,
          error:
            "Duplicate question IDs were selected.",
        },
        { status: 400 }
      );
    }

    /*
     * -------------------------------------------------------
     * QUESTION COUNT + DURATION
     * -------------------------------------------------------
     */

    let questionCount: number;
    let duration: number;

    let presetTotalMarks:
      | number
      | null = null;

    if (preset) {
      const totalQuestions =
        Object.values(
          preset.subjects
        ).reduce(
          (sum, count) =>
            sum +
            (Number(count) || 0),
          0
        );

      const totalMarks =
        Object.entries(
          preset.subjects
        ).reduce(
          (
            sum,
            [subject, count]
          ) => {
            const marksPerQuestion =
              subject === "maths"
                ? 2
                : 1;

            return (
              sum +
              (Number(count) || 0) *
                marksPerQuestion
            );
          },
          0
        );

      presetTotalMarks =
        totalMarks;

      const rawMinutes =
        totalMarks * 0.9;

      duration =
        Math.ceil(
          rawMinutes / 5
        ) * 5;

      questionCount =
        totalQuestions;
    } else {
      questionCount =
        Math.max(
          1,
          Math.min(
            Number(
              body.questionCount
            ) || 10,
            200
          )
        );

      duration =
        Number(body.duration) ||
        60;
    }

    /*
     * -------------------------------------------------------
     * EXACT QUESTION COUNT VALIDATION
     * -------------------------------------------------------
     */

    if (
      requestedQuestionIds.length > 0 &&
      requestedQuestionIds.length !==
        questionCount
    ) {
      return Response.json(
        {
          success: false,
          error:
            `You selected ${requestedQuestionIds.length} questions, but the test requires exactly ${questionCount}.`,
          details: {
            selected:
              requestedQuestionIds.length,
            required:
              questionCount,
          },
        },
        { status: 400 }
      );
    }

    /*
     * -------------------------------------------------------
     * LOG REQUEST
     * -------------------------------------------------------
     */

    console.log(
      "================================="
    );

    console.log(
      "GENERATE TEST REQUEST"
    );

    console.log(
      "Exam:",
      exam
    );

    console.log(
      "Subjects:",
      subjects
    );

    console.log(
      "Chapters:",
      chapters
    );

    console.log(
      "Difficulty:",
      difficulty
    );

    console.log(
      "Preset:",
      preset?.id || "none"
    );

    console.log(
      "Question Count:",
      questionCount
    );

    console.log(
      "Duration:",
      duration
    );

    console.log(
      "Exact Question IDs:",
      requestedQuestionIds.length
    );

    console.log(
      "Preview Only:",
      Boolean(body.previewOnly)
    );

    console.log(
      "================================="
    );

    /*
     * -------------------------------------------------------
     * PRESET SUBJECT VALIDATION
     * -------------------------------------------------------
     */

    if (preset) {
      const presetSubjects =
        Object.keys(
          preset.subjects
        ) as PresetSubject[];

      const selectedPresetSubjects =
        subjects
          .map(
            normalizePresetSubject
          )
          .filter(
            (
              subject
            ): subject is PresetSubject =>
              subject !== null
          );

      const missingSubjects =
        presetSubjects.filter(
          (presetSubject) =>
            !selectedPresetSubjects.includes(
              presetSubject
            )
        );

      if (
        missingSubjects.length > 0
      ) {
        return Response.json(
          {
            success: false,
            error:
              `The selected preset requires ${missingSubjects
                .map(displaySubject)
                .join(", ")}.`,
          },
          { status: 400 }
        );
      }
    }

    /*
     * =======================================================
     * BASE CONDITIONS
     * =======================================================
     */

    const conditions: string[] =
      [];

    const values: unknown[] =
      [];

    /*
     * EXAM
     */
    addExamFilter(
      exam,
      conditions,
      values
    );

    /*
     * DIFFICULTY
     */
    addDifficultyFilter(
      difficulty,
      conditions
    );

    /*
     * NORMAL MODE
     */
    if (!preset) {
      addSubjectChapterFilters(
        values,
        conditions,
        body.chaptersBySubject,
        subjects,
        chapters
      );
    }

    /*
     * =======================================================
     * SELECTED QUESTIONS
     * =======================================================
     */

    const selectedQuestions:
      QuestionRow[] = [];

    /*
     * =======================================================
     * PRESET MODE
     * =======================================================
     */

    if (preset) {
      for (
        const [
          presetSubject,
          requiredCount,
        ] of Object.entries(
          preset.subjects
        )
      ) {
        const count =
          Number(
            requiredCount
          ) || 0;

        if (count <= 0) {
          continue;
        }

        const databaseSubject =
          displaySubject(
            presetSubject as PresetSubject
          );

        /*
         * ---------------------------------------------------
         * SUBJECT CONDITIONS
         * ---------------------------------------------------
         */

        const subjectConditions =
          [...conditions];

        const subjectValues =
          [...values];

        addSubjectFilter(
          databaseSubject,
          subjectConditions,
          subjectValues
        );

        /*
         * ---------------------------------------------------
         * SUBJECT-SPECIFIC CHAPTERS
         * ---------------------------------------------------
         */

        let selectedSubjectChapters:
          string[] = [];

        if (
          body.chaptersBySubject
        ) {
          const chapterEntry =
            Object.entries(
              body.chaptersBySubject
            ).find(
              ([subject]) =>
                normalize(
                  subject
                ) ===
                  normalize(
                    databaseSubject
                  ) ||
                normalizePresetSubject(
                  subject
                ) ===
                  (presetSubject as PresetSubject)
            );

          if (
            chapterEntry &&
            Array.isArray(
              chapterEntry[1]
            )
          ) {
            selectedSubjectChapters =
              chapterEntry[1]
                .map(clean)
                .filter(Boolean);
          }
        }

        addChapterFilter(
          selectedSubjectChapters,
          subjectConditions,
          subjectValues
        );

        /*
         * ---------------------------------------------------
         * COUNT AVAILABLE QUESTIONS
         * ---------------------------------------------------
         */

        const countQuery = `
          SELECT COUNT(*)::int AS count
          FROM questions
          WHERE
            ${subjectConditions.join(
              " AND "
            )}
        `;

        const countResult =
          await pool.query(
            countQuery,
            subjectValues
          );

        const availableForSubject =
          Number(
            countResult.rows[0]
              ?.count || 0
          );

        console.log(
          `[${exam}] ${databaseSubject}: ${availableForSubject} available, ${count} required`
        );

        /*
         * ---------------------------------------------------
         * NOT ENOUGH QUESTIONS
         * ---------------------------------------------------
         */

        if (
          availableForSubject <
          count
        ) {
          return Response.json(
            {
              success: false,

              error:
                `Only ${availableForSubject} ${databaseSubject} question${
                  availableForSubject === 1
                    ? ""
                    : "s"
                } available for the selected ${exam} criteria, but the "${preset.name}" preset requires ${count}.`,

              details: {
                exam,

                presetId:
                  preset.id,

                presetName:
                  preset.name,

                subject:
                  databaseSubject,

                availableQuestions:
                  availableForSubject,

                requiredQuestions:
                  count,

                difficulty,

                chapters:
                  selectedSubjectChapters,

                message:
                  "Check the selected exam, difficulty, and chapter filters.",
              },
            },
            { status: 400 }
          );
        }

        /*
         * ---------------------------------------------------
         * RANDOM QUESTIONS
         * ---------------------------------------------------
         *
         * Preset behavior remains unchanged.
         */

        const questionValues: unknown[] = [...subjectValues];
        let orderBy = "RANDOM()";
        if (studentId) {
          questionValues.push(studentId);
          const studentParam = questionValues.length;
          orderBy = `CASE WHEN NOT EXISTS (
            SELECT 1 FROM test_answers seen_answer
            INNER JOIN test_attempts seen_attempt ON seen_attempt.id = seen_answer.attempt_id
            WHERE seen_attempt.student_id = $${studentParam}
              AND seen_answer.question_id = questions.id
          ) THEN 0 ELSE 1 END, RANDOM()`;
        }
        questionValues.push(count);

        const questionQuery = `
          ${QUESTION_SELECT}
          WHERE
            ${subjectConditions.join(
              " AND "
            )}
          ORDER BY ${orderBy}
          LIMIT $${questionValues.length}
        `;

        const result =
          await pool.query(
            questionQuery,
            questionValues
          );

        const subjectQuestions =
          result.rows as QuestionRow[];

        /*
         * Safety check
         */
        if (
          subjectQuestions.length <
          count
        ) {
          return Response.json(
            {
              success: false,

              error:
                `Unable to collect the required ${count} ${databaseSubject} questions from the ${exam} dataset.`,

              details: {
                exam,

                subject:
                  databaseSubject,

                required:
                  count,

                found:
                  subjectQuestions.length,
              },
            },
            { status: 500 }
          );
        }

        selectedQuestions.push(
          ...subjectQuestions
        );
      }
    } else {
      /*
       * =====================================================
       * NORMAL MODE
       * =====================================================
       */

      /*
       * -----------------------------------------------------
       * COUNT MATCHING QUESTIONS
       * -----------------------------------------------------
       */

      const countQuery = `
        SELECT COUNT(*)::int AS count
        FROM questions
        WHERE
          ${conditions.join(
            " AND "
          )}
      `;

      const countResult =
        await pool.query(
          countQuery,
          values
        );

      const available =
        Number(
          countResult.rows[0]
            ?.count || 0
        );

      console.log(
        `[${exam}] Matching questions:`,
        available
      );

      /*
       * -----------------------------------------------------
       * NO QUESTIONS
       * -----------------------------------------------------
       */

      if (available === 0) {
        return Response.json(
          {
            success: false,

            error:
              `No ${exam} questions are available for the selected criteria.`,

            details: {
              exam,
              subjects,
              chapters,
              difficulty,
              availableQuestions:
                0,
            },
          },
          { status: 404 }
        );
      }

      /*
       * -----------------------------------------------------
       * PREVIEW MODE
       * -----------------------------------------------------
       *
       * Used by:
       *
       * app/teacher/generate/page.tsx
       *
       * This returns EVERY matching question.
       *
       * It does NOT create a test.
       */

      if (body.previewOnly) {
        /*
         * Never send the entire matching question bank to the
         * browser. The old behavior could return hundreds or
         * thousands of questions at once, forcing Chrome to
         * render a huge DOM with KaTeX and images.
         *
         * Preview is paginated: 25 questions per request.
         */
        const requestedPreviewLimit = Number(body.previewLimit);
        const previewLimit = Number.isFinite(requestedPreviewLimit)
          ? Math.min(25, Math.max(1, Math.floor(requestedPreviewLimit)))
          : 25;

        const requestedPreviewOffset = Number(body.previewOffset);
        const previewOffset =
          Number.isFinite(requestedPreviewOffset) && requestedPreviewOffset >= 0
            ? Math.floor(requestedPreviewOffset)
            : 0;

        const previewValues = [...values, previewLimit, previewOffset];
        const limitParam = previewValues.length - 1;
        const offsetParam = previewValues.length;

        const previewQuery = `
          ${QUESTION_SELECT}
          WHERE
            ${conditions.join(" AND ")}
          ORDER BY id
          LIMIT $${limitParam}
          OFFSET $${offsetParam}
        `;

        const previewResult = await pool.query(
          previewQuery,
          previewValues
        );

        const availableQuestions =
          previewResult.rows as QuestionRow[];

        console.log(
          "PREVIEW QUESTIONS:",
          availableQuestions.length,
          "of",
          available,
          "offset",
          previewOffset
        );

        return Response.json({
          success: true,
          previewOnly: true,
          exam,
          availableQuestionCount: available,
          availableQuestions,
          previewOffset,
          previewLimit,
          requestedQuestionCount: questionCount,
          duration,
          configuration: {
            exam,
            course: body.course || exam,
            subject: body.subject || subjects[0] || "",
            subjects,
            chapters,
            chaptersBySubject: body.chaptersBySubject || {},
            difficulty,
            questionCount,
            duration,
          },
        });
      }

      /*
       * -----------------------------------------------------
       * EXACT QUESTION SELECTION
       * -----------------------------------------------------
       *
       * If the teacher selected question IDs:
       *
       * 1. Fetch ONLY those IDs.
       * 2. Apply ALL normal filters.
       * 3. Verify every requested ID exists.
       * 4. Preserve the teacher's selection order.
       */

      if (
        requestedQuestionIds.length > 0
      ) {
        const questionIdParam =
          values.length + 1;

        const exactConditions = [
          ...conditions,
          `id = ANY($${questionIdParam}::text[])`,
        ];

        const exactValues = [
          ...values,
          requestedQuestionIds,
        ];

        const exactQuestionQuery = `
          ${QUESTION_SELECT}
          WHERE
            ${exactConditions.join(
              " AND "
            )}
          ORDER BY ARRAY_POSITION(
            $${questionIdParam}::text[],
            id
          )
        `;

        const exactResult =
          await pool.query(
            exactQuestionQuery,
            exactValues
          );

        const exactQuestions =
          exactResult.rows as QuestionRow[];

        /*
         * Every selected ID must still satisfy
         * the currently selected filters.
         */
        if (
          exactQuestions.length !==
          requestedQuestionIds.length
        ) {
          const foundIds =
            new Set(
              exactQuestions.map(
                (question) =>
                  String(question.id)
              )
            );

          const invalidIds =
            requestedQuestionIds.filter(
              (id) =>
                !foundIds.has(id)
            );

          return Response.json(
            {
              success: false,

              error:
                "One or more selected questions no longer match the selected exam, subject, chapter, or difficulty.",

              details: {
                requestedQuestionCount:
                  requestedQuestionIds.length,

                matchedQuestionCount:
                  exactQuestions.length,

                invalidQuestionIds:
                  invalidIds,
              },
            },
            { status: 400 }
          );
        }

        /*
         * This is now EXACTLY the teacher's selection.
         */
        selectedQuestions.push(
          ...exactQuestions
        );
      } else {
        /*
         * -----------------------------------------------------
         * NORMAL RANDOM GENERATION
         * -----------------------------------------------------
         *
         * Multi-subject tests are generated in a fixed subject
         * order, while questions inside each subject are random.
         * Chapter selection is only a filter and never determines
         * question order.
         *
         * Physics -> Chemistry -> Biology -> Mathematics
         */

        const subjectOrder = [
          "Physics",
          "Chemistry",
          "Biology",
          "Mathematics",
        ];

        const normalizedSelectedSubjects = new Set(
          subjects.map((subject) => normalize(subject))
        );

        const orderedSubjects = subjectOrder.filter((subject) =>
          normalizedSelectedSubjects.has(normalize(subject))
        );

        if (orderedSubjects.length === 0) {
          return Response.json(
            {
              success: false,
              error: "Please select at least one subject.",
            },
            { status: 400 }
          );
        }

        const baseCount = Math.floor(
          questionCount / orderedSubjects.length
        );
        let remainder = questionCount % orderedSubjects.length;

        for (const databaseSubject of orderedSubjects) {
          const subjectCount =
            baseCount + (remainder > 0 ? 1 : 0);

          if (remainder > 0) remainder -= 1;

          const subjectConditions = [...conditions];
          const subjectValues = [...values];

          addSubjectFilter(
            databaseSubject,
            subjectConditions,
            subjectValues
          );

          let subjectChapters = chapters;

          if (body.chaptersBySubject) {
            const chapterEntry = Object.entries(
              body.chaptersBySubject as Record<string, string[]>
            ).find(
              ([subject]) => normalize(subject) === normalize(databaseSubject)
            );

            if (chapterEntry && Array.isArray(chapterEntry[1])) {
              subjectChapters = chapterEntry[1]
                .map(clean)
                .filter(Boolean);
            }
          }

          addChapterFilter(
            subjectChapters,
            subjectConditions,
            subjectValues
          );

          const countQuery = `
            SELECT COUNT(*)::int AS count
            FROM questions
            WHERE
              ${subjectConditions.join(" AND ")}
          `;

          const countResult = await pool.query(
            countQuery,
            subjectValues
          );

          const availableForSubject = Number(
            countResult.rows[0]?.count || 0
          );

          if (availableForSubject < subjectCount) {
            return Response.json(
              {
                success: false,
                error:
                  `Only ${availableForSubject} ${databaseSubject} questions are available for the selected criteria, but ${subjectCount} are required for this test.`,
                details: {
                  exam,
                  subject: databaseSubject,
                  requestedQuestions: subjectCount,
                  availableQuestions: availableForSubject,
                  selectedSubjects: orderedSubjects,
                  chapters: subjectChapters,
                  difficulty,
                },
              },
              { status: 400 }
            );
          }

          const questionValues: unknown[] = [...subjectValues];
          let orderBy = "RANDOM()";
          if (studentId) {
            questionValues.push(studentId);
            const studentParam = questionValues.length;
            orderBy = `CASE WHEN NOT EXISTS (
              SELECT 1 FROM test_answers seen_answer
              INNER JOIN test_attempts seen_attempt ON seen_attempt.id = seen_answer.attempt_id
              WHERE seen_attempt.student_id = $${studentParam}
                AND seen_answer.question_id = questions.id
            ) THEN 0 ELSE 1 END, RANDOM()`;
          }
          questionValues.push(subjectCount);

          const questionQuery = `
            ${QUESTION_SELECT}
            WHERE
              ${subjectConditions.join(" AND ")}
            ORDER BY ${orderBy}
            LIMIT $${questionValues.length}
          `;

          const result = await pool.query(
            questionQuery,
            questionValues
          );

          selectedQuestions.push(
            ...(result.rows as QuestionRow[])
          );
        }
      }
    }

    /*
     * =======================================================
     * FINAL SAFETY CHECK
     * =======================================================
     */

    if (
      selectedQuestions.length <
      questionCount
    ) {
      return Response.json(
        {
          success: false,

          error:
            `Unable to collect enough ${exam} questions for this test.`,

          details: {
            exam,

            requested:
              questionCount,

            found:
              selectedQuestions.length,
          },
        },
        { status: 500 }
      );
    }

    /*
     * =======================================================
     * EXACT COUNT SAFETY
     * =======================================================
     *
     * Especially important for questionIds.
     */

    if (
      selectedQuestions.length !==
      questionCount
    ) {
      return Response.json(
        {
          success: false,

          error:
            `The generated test contains ${selectedQuestions.length} questions, but exactly ${questionCount} were required.`,

          details: {
            requested:
              questionCount,

            found:
              selectedQuestions.length,
          },
        },
        { status: 500 }
      );
    }

    /*
     * =======================================================
     * CREATE TEST ID
     * =======================================================
     */

    const testId =
      `test-${Date.now()}-${Math.random()
        .toString(36)
        .slice(2, 8)}`;

    /*
     * =======================================================
     * SAVE TEST
     * =======================================================
     */

    const client =
      await pool.connect();

    try {
      await client.query(
        "BEGIN"
      );

      await client.query(`
        ALTER TABLE tests
        ADD COLUMN IF NOT EXISTS academy_id UUID,
        ADD COLUMN IF NOT EXISTS is_full_chapter BOOLEAN NOT NULL DEFAULT FALSE,
        ADD COLUMN IF NOT EXISTS full_chapter_subject VARCHAR(150),
        ADD COLUMN IF NOT EXISTS full_chapter_name VARCHAR(255)
      `);

      /*
       * Automatically tag a generated paper as a full-chapter test
       * when it contains 25+ questions from one subject/chapter and
       * covers every topic represented by the question bank for that chapter.
       */
      let isFullChapter = false;
      let fullChapterSubject: string | null = null;
      let fullChapterName: string | null = null;
      if (selectedQuestions.length >= 25) {
        const subjectsFound = new Set(selectedQuestions.map((q) => clean(q.subject)));
        const chaptersFound = new Set(selectedQuestions.map((q) => clean(q.chapter_name)));
        if (subjectsFound.size === 1 && chaptersFound.size === 1 && !chaptersFound.has("")) {
          fullChapterSubject = [...subjectsFound][0] || null;
          fullChapterName = [...chaptersFound][0] || null;
          if (fullChapterSubject && fullChapterName) {
            const topicResult = await client.query(
              `SELECT DISTINCT COALESCE(NULLIF(subtopic,''), NULLIF(major_topic,'')) AS topic
               FROM questions
               WHERE subject = $1 AND chapter_name = $2
                 AND COALESCE(NULLIF(subtopic,''), NULLIF(major_topic,'')) IS NOT NULL`,
              [fullChapterSubject, fullChapterName]
            );
            const selectedTopics = new Set(selectedQuestions.map((q) => clean(q.subtopic || q.major_topic)).filter(Boolean));
            const allTopics = topicResult.rows.map((r) => clean(r.topic)).filter(Boolean);
            isFullChapter = allTopics.length > 0 && allTopics.every((topic) => selectedTopics.has(topic));
          }
        }
      }

      /*
       * Save test
       */
      await client.query(
        `
          INSERT INTO tests (
            id, exam, question_count, questions, difficulty, academy_id,
            is_full_chapter, full_chapter_subject, full_chapter_name
          )
          VALUES ($1, $2, $3, $4::jsonb, $5, $6, $7, $8, $9)
        `,
        [
          testId,

          /*
           * Store normalized exam.
           */
          exam,

          selectedQuestions.length,

          JSON.stringify(
            selectedQuestions
          ),

          difficulty,
          academyId || null,
          isFullChapter,
          fullChapterSubject,
          fullChapterName,
        ]
      );

      /*
       * Connect test to student
       */
      if (studentId) {
        await client.query(
          `
            INSERT INTO student_tests (
              id,
              student_id,
              test_id
            )
            VALUES (
              $1,
              $2,
              $3
            )
            ON CONFLICT (
              student_id,
              test_id
            )
            DO NOTHING
          `,
          [
            `student-test-${Date.now()}-${Math.random()
              .toString(36)
              .slice(2, 8)}`,

            studentId,

            testId,
          ]
        );
      }

      await client.query(
        "COMMIT"
      );
    } catch (error) {
      await client.query(
        "ROLLBACK"
      );

      throw error;
    } finally {
      client.release();
    }

    /*
     * =======================================================
     * SUCCESS LOG
     * =======================================================
     */

    console.log(
      "================================="
    );

    console.log(
      "TEST GENERATED SUCCESSFULLY"
    );

    console.log(
      "Test ID:",
      testId
    );

    console.log(
      "Exam:",
      exam
    );

    console.log(
      "Preset:",
      preset?.id || "none"
    );

    console.log(
      "Questions:",
      selectedQuestions.length
    );

    console.log(
      "Exact Selection:",
      requestedQuestionIds.length > 0
    );

    console.log(
      "Duration:",
      duration
    );

    console.log(
      "================================="
    );

    /*
     * =======================================================
     * RESPONSE
     * =======================================================
     */

    return Response.json({
      success: true,

      testId,

      exam,

      questionCount:
        selectedQuestions.length,

      duration,

      totalMarks:
        presetTotalMarks,

      preset: preset
        ? {
            id: preset.id,

            name:
              preset.name,

            subjects:
              preset.subjects,
          }
        : null,

      configuration: {
        testId,

        /*
         * Store normalized exam.
         */
        exam,

        course:
          body.course ||
          exam,

        studentGroup:
          clean(
            (
              body as GenerateRequest & {
                studentGroup?: string;
              }
            ).studentGroup
          ),

        subject:
          body.subject ||
          subjects[0] ||
          "",

        subjects,

        chapters,

        chaptersBySubject:
          body.chaptersBySubject ||
          {},

        difficulty,

        presetId:
          preset?.id || null,

        presetName:
          preset?.name || null,

        questionCount:
          selectedQuestions.length,

        duration,

        totalMarks:
          presetTotalMarks,

        /*
         * Store the exact IDs selected by the teacher.
         */
        questionIds:
          selectedQuestions.map(
            (question) =>
              String(question.id)
          ),

        createdAt:
          new Date().toISOString(),
      },

      questions: studentId
        ? selectedQuestions.map((question) => {
            const {
              correct_option: _correctOption,
              correct_answer_text: _correctAnswerText,
              solution: _solution,
              answer: _answer,
              ...safeQuestion
            } = question as Record<string, unknown>;
            return safeQuestion;
          })
        : selectedQuestions,
    });
  } catch (error: unknown) {
    console.error(
      "TEST GENERATION ERROR:",
      error
    );

    return Response.json(
      {
        success: false,

        error:
          error instanceof Error
            ? error.message
            : "Failed to generate test.",
      },
      { status: 500 }
    );
  }
}