import { cookies } from "next/headers";
import { pool } from "@/lib/db";
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
 *
 * IMPORTANT:
 *
 * The database currently contains:
 *
 * MHT-CET
 *
 * The UI may send:
 *
 * MHT CET
 * MHTCET
 * mht-cet
 * mht cet
 *
 * All of these are converted to:
 *
 * MHT-CET
 *
 * NEET stays:
 *
 * NEET
 *
 * This prevents MHT-CET and NEET datasets
 * from getting mixed together.
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
 *
 * We normalize common database spellings as well.
 *
 * MHT-CET database rows can therefore be matched even if
 * they contain:
 *
 * MHT-CET
 * MHT CET
 * MHTCET
 *
 * NEET rows remain NEET-only.
 * =========================================================
 */function addExamFilter(
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
  const normalizedDifficulty =
    normalize(difficulty);

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
   * Challenging
   *
   * Medium + Difficult
   */
  if (
    normalizedDifficulty === "challenging"
  ) {
    conditions.push(`
      LOWER(TRIM(difficulty)) IN (
        'medium',
        'difficult'
      )
    `);

    return;
  }

  /*
   * Difficult
   *
   * Difficult only
   */
  if (
    normalizedDifficulty === "difficult"
  ) {
    conditions.push(`
      LOWER(TRIM(difficulty)) = 'difficult'
    `);

    return;
  }

  /*
   * Balanced / Mixed
   *
   * No difficulty filter.
   */
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
 * SUBJECT + CHAPTER FILTER FOR NORMAL MODE
 * =========================================================
 *
 * Keeps subject/chapter relationship intact.
 *
 * Example:
 *
 * Physics → Current Electricity
 * Chemistry → Chemical Bonding
 *
 * Physics cannot accidentally receive
 * Chemistry chapters.
 * =========================================================
 */

function addSubjectChapterFilters(
  values: unknown[],
  conditions: string[],
  chaptersBySubject:
    | Record<string, string[]>
    | undefined,
  subjects: string[]
) {
  if (
    chaptersBySubject &&
    Object.keys(chaptersBySubject).length > 0
  ) {
    const subjectChapterPairs: {
      subject: string;
      chapter: string;
    }[] = [];

    for (
      const [subject, chapterList] of
      Object.entries(chaptersBySubject)
    ) {
      if (!Array.isArray(chapterList)) {
        continue;
      }

      for (const chapter of chapterList) {
        if (
          clean(subject) &&
          clean(chapter)
        ) {
          subjectChapterPairs.push({
            subject: normalize(subject),
            chapter: normalize(chapter),
          });
        }
      }
    }

    if (
      subjectChapterPairs.length > 0
    ) {
      const pairConditions =
        subjectChapterPairs.map(
          (pair) => {
            const subjectParam =
              values.length + 1;

            const chapterParam =
              values.length + 2;

            values.push(
              pair.subject,
              pair.chapter
            );

            return `
              (
                LOWER(
                  REGEXP_REPLACE(
                    TRIM(subject),
                    '[_-]+',
                    ' ',
                    'g'
                  )
                ) =
                $${subjectParam}

                AND

                LOWER(
                  REGEXP_REPLACE(
                    TRIM(chapter_name),
                    '[_-]+',
                    ' ',
                    'g'
                  )
                ) =
                $${chapterParam}
              )
            `;
          }
        );

      conditions.push(`
        (
          ${pairConditions.join(" OR ")}
        )
      `);

      return;
    }
  }

  /*
   * No chapter-specific selection.
   * Filter only by selected subjects.
   */

  if (subjects.length > 0) {
    const subjectValues =
      subjects.map(normalize);

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
     * STUDENT SESSION
     * -------------------------------------------------------
     */

    const cookieStore =
      await cookies();

    const studentId =
      cookieStore.get(
        "student_session"
      )?.value;

    if (!studentId) {
      return Response.json(
        {
          success: false,
          error:
            "Student is not logged in.",
        },
        { status: 401 }
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
     *
     * IMPORTANT:
     *
     * Do not use course as the database dataset
     * when a proper exam value exists.
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
     * QUESTION COUNT + DURATION
     * -------------------------------------------------------
     */

    let questionCount: number;
    let duration: number;
    let presetTotalMarks: number | null =
      null;

    if (preset) {
      const totalQuestions =
        Object.values(
          preset.subjects
        ).reduce(
          (sum, count) =>
            sum + (Number(count) || 0),
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
     * -------------------------------------------------------
     * BASE CONDITIONS
     * -------------------------------------------------------
     */

    const conditions: string[] = [];

    const values: unknown[] = [];

    /*
     * EXAM FILTER
     */

    addExamFilter(
      exam,
      conditions,
      values
    );

    /*
     * DIFFICULTY FILTER
     */

    addDifficultyFilter(
      difficulty,
      conditions
    );

    /*
     * -------------------------------------------------------
     * NORMAL MODE
     * -------------------------------------------------------
     */

    if (!preset) {
      addSubjectChapterFilters(
        values,
        conditions,
        body.chaptersBySubject,
        subjects
      );
    }

    /*
     * -------------------------------------------------------
     * SELECTED QUESTIONS
     * -------------------------------------------------------
     */

    const selectedQuestions: QuestionRow[] =
      [];

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

        let selectedSubjectChapters: string[] =
          [];

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
                `Only ${availableForSubject} ${databaseSubject} question${availableForSubject === 1 ? "" : "s"} available for the selected ${exam} criteria, but the "${preset.name}" preset requires ${count}.`,

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
         */

        const questionValues =
          [
            ...subjectValues,
            count,
          ];

        const questionQuery = `
          ${QUESTION_SELECT}
          WHERE
            ${subjectConditions.join(
              " AND "
            )}
          ORDER BY RANDOM()
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
       * COUNT
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
       * NOT ENOUGH
       * -----------------------------------------------------
       */

      if (
        available <
        questionCount
      ) {
        return Response.json(
          {
            success: false,

            error:
              `Only ${available} ${exam} questions are available for the selected criteria. You requested ${questionCount}.`,

            details: {
              exam,
              subjects,
              chapters,
              difficulty,

              availableQuestions:
                available,

              requestedQuestions:
                questionCount,
            },
          },
          { status: 400 }
        );
      }

      /*
       * -----------------------------------------------------
       * RANDOM QUESTIONS
       * -----------------------------------------------------
       */

      const questionValues = [
        ...values,
        questionCount,
      ];

      const questionQuery = `
        ${QUESTION_SELECT}
        WHERE
          ${conditions.join(
            " AND "
          )}
        ORDER BY RANDOM()
        LIMIT $${questionValues.length}
      `;

      const result =
        await pool.query(
          questionQuery,
          questionValues
        );

      selectedQuestions.push(
        ...(result.rows as QuestionRow[])
      );
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

      /*
       * Save test
       */

      await client.query(
        `
          INSERT INTO tests (
            id,
            exam,
            question_count,
            questions,
            difficulty
          )
          VALUES (
            $1,
            $2,
            $3,
            $4::jsonb,
            $5
          )
        `,
        [
          testId,

          /*
           * Store the normalized exam.
           *
           * MHT CET becomes MHT-CET.
           * NEET remains NEET.
           */

          exam,

          selectedQuestions.length,

          JSON.stringify(
            selectedQuestions
          ),

          difficulty,
        ]
      );

      /*
       * Connect test to student
       */

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
         * Store normalized exam here too.
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

        createdAt:
          new Date().toISOString(),
      },

      questions:
        selectedQuestions,
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