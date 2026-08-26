import { cookies } from "next/headers";
import { pool } from "@/lib/db";
import {
  getPreset,
  type Preset,
  type PresetSubject,
} from "@/lib/test-presets";

export const runtime = "nodejs";

type GenerateRequest = {
  exam?: string;
  course?: string;

  subject?: string;
  subjects?: string[];

  chapters?: string[];
  chaptersBySubject?: Record<string, string[]>;

  difficulty?: string;

  // Preset system
  presetId?: string;

  // Kept for backward compatibility
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

function clean(value: unknown): string {
  return String(value ?? "").trim();
}

function normalize(value: unknown): string {
  return clean(value)
    .toLowerCase()
    .replace(/[_-]+/g, " ")
    .replace(/\s+/g, " ");
}

/*
 * ---------------------------------------------------------
 * CONVERT DATABASE SUBJECT → PRESET SUBJECT
 * ---------------------------------------------------------
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
 * ---------------------------------------------------------
 * SUBJECT DISPLAY NAME
 * ---------------------------------------------------------
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
 * ---------------------------------------------------------
 * DIFFICULTY FILTER
 * ---------------------------------------------------------
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
  }

  /*
   * Challenging
   *
   * Medium + Hard
   */

  if (
    normalizedDifficulty ===
    "challenging"
  ) {
    conditions.push(`
      LOWER(TRIM(difficulty)) IN (
        'medium',
        'hard'
      )
    `);
  }

  /*
   * Difficult
   *
   * Hard only
   */

  if (
    normalizedDifficulty ===
    "difficult"
  ) {
    conditions.push(`
      LOWER(TRIM(difficulty)) = 'hard'
    `);
  }

  /*
   * Balanced
   *
   * No difficulty restriction.
   */
}

/*
 * ---------------------------------------------------------
 * BUILD SUBJECT + CHAPTER CONDITIONS
 * ---------------------------------------------------------
 */

function addSubjectChapterFilters(
  values: unknown[],
  conditions: string[],
  chaptersBySubject:
    | Record<string, string[]>
    | undefined,
  subjects: string[]
) {
  /*
   * If chapters were selected separately
   * for each subject, preserve that relationship.
   *
   * Example:
   *
   * Physics → Current Electricity
   * Chemistry → Chemical Bonding
   *
   * This prevents:
   *
   * Physics → Chemical Bonding
   * Chemistry → Current Electricity
   */

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
                ) = $${subjectParam}

                AND

                LOWER(
                  REGEXP_REPLACE(
                    TRIM(chapter_name),
                    '[_-]+',
                    ' ',
                    'g'
                  )
                ) = $${chapterParam}
              )
            `;
          }
        );

      conditions.push(`
        (
          ${pairConditions.join(
            " OR "
          )}
        )
      `);

      return;
    }
  }

  /*
   * No chapter-specific selection.
   *
   * Filter only by subjects.
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
 * ---------------------------------------------------------
 * MAIN POST
 * ---------------------------------------------------------
 */

export async function POST(
  request: Request
) {
  try {
    /*
     * -------------------------------------------------------
     * DATABASE
     * -------------------------------------------------------
     */

    if (!process.env.DATABASE_URL) {
      return Response.json(
        {
          success: false,
          error:
            "DATABASE_URL is not configured",
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
     * REQUEST
     * -------------------------------------------------------
     */

    const body =
      (await request.json()) as GenerateRequest;

    const exam =
      clean(body.exam) ||
      clean(body.course) ||
      "MHT-CET";

    const subjects =
      Array.isArray(body.subjects)
        ? body.subjects
            .map(clean)
            .filter(Boolean)
        : body.subject
          ? [clean(body.subject)]
          : [];

    const chapters =
      Array.isArray(body.chapters)
        ? body.chapters
            .map(clean)
            .filter(Boolean)
        : [];

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
     *
     * If a preset exists, NEVER trust the
     * client-provided question count/duration.
     *
     * Calculate them from the preset.
     * -------------------------------------------------------
     */

    let questionCount: number;
    let duration: number;

    if (preset) {
      const totalQuestions =
        Object.values(
          preset.subjects
        ).reduce(
          (sum, count) =>
            sum + (count || 0),
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
            /*
             * Maths = 2 marks
             * Other subjects = 1 mark
             */

            const marksPerQuestion =
              subject === "maths"
                ? 2
                : 1;

            return (
              sum +
              (count || 0) *
                marksPerQuestion
            );
          },
          0
        );

      const rawMinutes =
        totalMarks * 0.9;

      duration =
        Math.ceil(
          rawMinutes / 5
        ) * 5;

      questionCount =
        totalQuestions;
    } else {
      /*
       * Backward compatibility
       */

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
     * LOG
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
        );

      /*
       * Convert selected UI subjects
       * into preset subject names.
       */

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

      /*
       * Every preset subject must be
       * available in the selected subjects.
       */
const missingSubjects =
  presetSubjects.filter(
    (presetSubject) =>
      !selectedPresetSubjects.includes(
        presetSubject as PresetSubject
      )
  ) as PresetSubject[];
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
     * BUILD BASE CONDITIONS
     * -------------------------------------------------------
     */

    const conditions: string[] = [
      `
        LOWER(TRIM(exam))
        =
        LOWER(TRIM($1))
      `,
    ];

    const values: unknown[] = [
      exam,
    ];

    /*
     * -------------------------------------------------------
     * DIFFICULTY
     * -------------------------------------------------------
     */

    addDifficultyFilter(
      difficulty,
      conditions
    );

    /*
     * -------------------------------------------------------
     * NON-PRESET SUBJECT FILTER
     * -------------------------------------------------------
     *
     * If there is no preset, use the normal
     * subject/chapter filtering.
     *
     * With a preset, subject quotas are handled
     * separately below.
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
     * PRESET MODE
     * -------------------------------------------------------
     *
     * Each subject gets its exact quota.
     *
     * Example PCM-150:
     *
     * Physics    → 50
     * Chemistry  → 50
     * Mathematics → 50
     */

    const selectedQuestions: QuestionRow[] =
      [];

    if (preset) {
      /*
       * -----------------------------------------------------
       * GET QUESTIONS SUBJECT BY SUBJECT
       * -----------------------------------------------------
       */

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

        /*
         * Convert preset subject name
         * into database subject name.
         */

        const databaseSubject =
          displaySubject(
            presetSubject as PresetSubject
          );

        /*
         * Clone base conditions.
         */

        const subjectConditions =
          [...conditions];

        const subjectValues =
          [...values];

        /*
         * Add exact subject.
         */

        const subjectParam =
          subjectValues.length + 1;

        subjectValues.push(
          normalize(
            databaseSubject
          )
        );

        subjectConditions.push(`
          LOWER(
            REGEXP_REPLACE(
              TRIM(subject),
              '[_-]+',
              ' ',
              'g'
            )
          )
          =
          $${subjectParam}
        `);

        /*
         * ---------------------------------------------------
         * CHAPTER FILTER FOR THIS SUBJECT
         * ---------------------------------------------------
         */

        const selectedSubjectChapters =
          body.chaptersBySubject
            ? Object.entries(
                body.chaptersBySubject
              ).find(
                ([subject]) =>
                  normalize(
                    subject
                  ) ===
                  normalize(
                    databaseSubject
                  )
              )?.[1] || []
            : [];

        if (
          selectedSubjectChapters.length >
          0
        ) {
          const chapterParams =
            selectedSubjectChapters.map(
              (chapter) => {
                const param =
                  subjectValues.length +
                  1;

                subjectValues.push(
                  normalize(chapter)
                );

                return `$${param}`;
              }
            );

          subjectConditions.push(`
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
                ${chapterParams.join(
                  ", "
                )}
              ]::text[]
            )
          `);
        }

        /*
         * ---------------------------------------------------
         * COUNT AVAILABLE FOR THIS SUBJECT
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
          `${databaseSubject}: ${availableForSubject} available, ${count} required`
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
                `Only ${availableForSubject} ${databaseSubject} question${availableForSubject === 1 ? "" : "s"} available for the selected criteria, but the "${preset.name}" preset requires ${count}.`,
              details: {
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
              },
            },
            { status: 400 }
          );
        }

        /*
         * ---------------------------------------------------
         * GET RANDOM QUESTIONS FOR SUBJECT
         * ---------------------------------------------------
         */

        const questionValues =
          [
            ...subjectValues,
            count,
          ];

        const questionQuery = `
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
         * Safety check.
         */

        if (
          subjectQuestions.length <
          count
        ) {
          return Response.json(
            {
              success: false,
              error:
                `Unable to collect the required number of ${databaseSubject} questions.`,
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
       * -----------------------------------------------------
       * NORMAL NON-PRESET MODE
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
        "Matching questions:",
        available
      );

      if (available === 0) {
        return Response.json(
          {
            success: false,
            error:
              "No questions are available for the selected criteria.",
            details: {
              exam,
              subjects,
              chapters,
              difficulty,
              availableQuestions: 0,
            },
          },
          { status: 404 }
        );
      }

      if (
        available <
        questionCount
      ) {
        return Response.json(
          {
            success: false,
            error:
              `Only ${available} question${available === 1 ? "" : "s"} available for the selected criteria. You requested ${questionCount}.`,
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

      const questionValues = [
        ...values,
        questionCount,
      ];

      const questionQuery = `
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
     * -------------------------------------------------------
     * FINAL QUESTION SAFETY CHECK
     * -------------------------------------------------------
     */

    if (
      selectedQuestions.length <
      questionCount
    ) {
      return Response.json(
        {
          success: false,
          error:
            "Unable to collect enough questions for this test.",
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
     * -------------------------------------------------------
     * SHUFFLE FINAL QUESTIONS
     * -------------------------------------------------------
     *
     * Subject quotas are already satisfied.
     * Now randomize their final order.
     * -------------------------------------------------------
     */

    for (
      let i =
        selectedQuestions.length - 1;
      i > 0;
      i--
    ) {
      const j =
        Math.floor(
          Math.random() *
            (i + 1)
        );

      [
        selectedQuestions[i],
        selectedQuestions[j],
      ] = [
        selectedQuestions[j],
        selectedQuestions[i],
      ];
    }

    /*
     * -------------------------------------------------------
     * CREATE TEST ID
     * -------------------------------------------------------
     */

    const testId =
      `test-${Date.now()}`;

    /*
     * -------------------------------------------------------
     * SAVE TEST
     * -------------------------------------------------------
     */

    const client =
      await pool.connect();

    try {
      await client.query(
        "BEGIN"
      );

      /*
       * Save test.
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
  exam,
  selectedQuestions.length,
  JSON.stringify(
    selectedQuestions
  ),
  difficulty,
]
      );

      /*
       * Connect test to student.
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
          `student-test-${Date.now()}`,
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
     * -------------------------------------------------------
     * SUCCESS
     * -------------------------------------------------------
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

    return Response.json({
      success: true,

      testId,

      exam,

      questionCount:
        selectedQuestions.length,

      duration,

      preset: preset
        ? {
            id: preset.id,
            name: preset.name,
            subjects:
              preset.subjects,
          }
        : null,

      configuration: {
        testId,

        course:
          body.course ||
          exam,

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

        questionCount:
          selectedQuestions.length,

        duration,

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
            : "Failed to generate test",
      },
      { status: 500 }
    );
  }
}