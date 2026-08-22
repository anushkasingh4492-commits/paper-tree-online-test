import {
  pgTable,
  uuid,
  varchar,
  text,
  integer,
  boolean,
  timestamp,
  jsonb,
  real,
  index,
  uniqueIndex,
} from "drizzle-orm/pg-core";

/* =========================================================
   USERS
   ========================================================= */

export const users = pgTable(
  "users",
  {
    id: uuid("id").defaultRandom().primaryKey(),

    name: varchar("name", { length: 150 }).notNull(),

    email: varchar("email", { length: 255 }).notNull(),

    passwordHash: text("password_hash").notNull(),

    createdAt: timestamp("created_at", { withTimezone: true })
      .defaultNow()
      .notNull(),

    updatedAt: timestamp("updated_at", { withTimezone: true })
      .defaultNow()
      .notNull(),
  },
  (table) => [
    uniqueIndex("users_email_unique").on(table.email),
  ],
);

/* =========================================================
   QUESTIONS
   ========================================================= */

export const questions = pgTable(
  "questions",
  {
    id: varchar("id", { length: 100 }).primaryKey(),

    exam: varchar("exam", { length: 50 })
      .notNull()
      .default("MHT-CET"),

    subject: varchar("subject", { length: 50 }).notNull(),

    standard: integer("standard").notNull(),

    chapterNumber: integer("chapter_number").notNull(),

    chapterName: varchar("chapter_name", { length: 255 }).notNull(),

    majorTopic: varchar("major_topic", { length: 255 }),

    subtopic: varchar("subtopic", { length: 255 }),

    conceptTested: text("concept_tested"),

    stem: text("stem").notNull(),

    options: jsonb("options").notNull(),

    correctOption: varchar("correct_option", { length: 5 }).notNull(),

    correctAnswerText: text("correct_answer_text"),

    distractorRationale: jsonb("distractor_rationale"),

    solution: text("solution"),

    formulaPrinciple: text("formula_principle"),

    commonMisconception: text("common_misconception"),

    difficulty: varchar("difficulty", { length: 20 }).notNull(),

    estimatedTime: varchar("estimated_time", { length: 100 }),

    questionType: varchar("question_type", { length: 100 }),

    figureAsset: text("figure_asset"),

    conceptFamilyId: varchar("concept_family_id", { length: 100 }),

    familySize: integer("family_size"),

    generatorEligibleStrictCet: boolean(
      "generator_eligible_strict_cet",
    )
      .notNull()
      .default(false),

    generatorEligibleExtendedRevision: boolean(
      "generator_eligible_extended_revision",
    )
      .default(false),

    syllabusScopeStatus: varchar("syllabus_scope_status", {
      length: 50,
    }),

    syllabusVersion: varchar("syllabus_version", { length: 100 }),

    releaseVersion: varchar("release_version", { length: 50 }),

    rawData: jsonb("raw_data"),

    createdAt: timestamp("created_at", { withTimezone: true })
      .defaultNow()
      .notNull(),
  },
  (table) => [
    index("questions_exam_subject_idx").on(
      table.exam,
      table.subject,
    ),

    index("questions_chapter_idx").on(
      table.subject,
      table.chapterNumber,
    ),

    index("questions_difficulty_idx").on(
      table.subject,
      table.difficulty,
    ),

    index("questions_generator_eligible_idx").on(
      table.generatorEligibleStrictCet,
    ),
  ],
);

/* =========================================================
   TESTS
   ========================================================= */

export const tests = pgTable(
  "tests",
  {
    id: uuid("id").defaultRandom().primaryKey(),

    userId: uuid("user_id")
      .notNull()
      .references(() => users.id, {
        onDelete: "cascade",
      }),

    exam: varchar("exam", { length: 50 })
      .notNull()
      .default("MHT-CET"),

    title: varchar("title", { length: 255 }).notNull(),

    subjects: jsonb("subjects").notNull(),

    chapters: jsonb("chapters"),

    difficulty: varchar("difficulty", {
      length: 20,
    }).notNull(),

    questionCount: integer("question_count").notNull(),

    durationMinutes: integer("duration_minutes").notNull(),

    status: varchar("status", {
      length: 30,
    })
      .notNull()
      .default("in_progress"),

    startedAt: timestamp("started_at", {
      withTimezone: true,
    }),

    submittedAt: timestamp("submitted_at", {
      withTimezone: true,
    }),

    createdAt: timestamp("created_at", {
      withTimezone: true,
    })
      .defaultNow()
      .notNull(),
  },
  (table) => [
    index("tests_user_idx").on(table.userId),

    index("tests_status_idx").on(
      table.userId,
      table.status,
    ),
  ],
);

/* =========================================================
   TEST QUESTIONS
   ========================================================= */

export const testQuestions = pgTable(
  "test_questions",
  {
    id: uuid("id").defaultRandom().primaryKey(),

    testId: uuid("test_id")
      .notNull()
      .references(() => tests.id, {
        onDelete: "cascade",
      }),

    questionId: varchar("question_id", {
      length: 100,
    })
      .notNull()
      .references(() => questions.id, {
        onDelete: "restrict",
      }),

    questionNumber: integer("question_number").notNull(),

    markedForReview: boolean("marked_for_review")
      .notNull()
      .default(false),

    visited: boolean("visited")
      .notNull()
      .default(false),

    createdAt: timestamp("created_at", {
      withTimezone: true,
    })
      .defaultNow()
      .notNull(),
  },
  (table) => [
    uniqueIndex("test_questions_unique").on(
      table.testId,
      table.questionId,
    ),

    uniqueIndex("test_questions_number_unique").on(
      table.testId,
      table.questionNumber,
    ),

    index("test_questions_test_idx").on(
      table.testId,
    ),
  ],
);

/* =========================================================
   ANSWERS
   ========================================================= */

export const answers = pgTable(
  "answers",
  {
    id: uuid("id").defaultRandom().primaryKey(),

    testId: uuid("test_id")
      .notNull()
      .references(() => tests.id, {
        onDelete: "cascade",
      }),

    testQuestionId: uuid("test_question_id")
      .notNull()
      .references(() => testQuestions.id, {
        onDelete: "cascade",
      }),

    selectedOption: varchar("selected_option", {
      length: 5,
    }),

    isCorrect: boolean("is_correct"),

    timeSpentSeconds: integer("time_spent_seconds")
      .default(0)
      .notNull(),

    answeredAt: timestamp("answered_at", {
      withTimezone: true,
    }),

    updatedAt: timestamp("updated_at", {
      withTimezone: true,
    })
      .defaultNow()
      .notNull(),
  },
  (table) => [
    uniqueIndex("answers_test_question_unique").on(
      table.testQuestionId,
    ),

    index("answers_test_idx").on(
      table.testId,
    ),
  ],
);

/* =========================================================
   ANTI-CHEATING / VIOLATIONS
   ========================================================= */

export const testViolations = pgTable(
  "test_violations",
  {
    id: uuid("id").defaultRandom().primaryKey(),

    testId: uuid("test_id")
      .notNull()
      .references(() => tests.id, {
        onDelete: "cascade",
      }),

    type: varchar("type", {
      length: 50,
    }).notNull(),

    description: text("description"),

    occurredAt: timestamp("occurred_at", {
      withTimezone: true,
    })
      .defaultNow()
      .notNull(),

    metadata: jsonb("metadata"),
  },
  (table) => [
    index("violations_test_idx").on(
      table.testId,
    ),
  ],
);

/* =========================================================
   TEST RESULTS
   ========================================================= */

export const testResults = pgTable(
  "test_results",
  {
    id: uuid("id").defaultRandom().primaryKey(),

    testId: uuid("test_id")
      .notNull()
      .references(() => tests.id, {
        onDelete: "cascade",
      }),

    totalQuestions: integer("total_questions").notNull(),

    attempted: integer("attempted").notNull(),

    correct: integer("correct").notNull(),

    wrong: integer("wrong").notNull(),

    unattempted: integer("unattempted").notNull(),

    score: real("score").notNull(),

    accuracy: real("accuracy").notNull(),

    totalTimeSeconds: integer(
      "total_time_seconds",
    ).notNull(),

    subjectAnalysis: jsonb("subject_analysis"),

    chapterAnalysis: jsonb("chapter_analysis"),

    difficultyAnalysis: jsonb("difficulty_analysis"),

    weakAreas: jsonb("weak_areas"),

    completedAt: timestamp("completed_at", {
      withTimezone: true,
    })
      .defaultNow()
      .notNull(),
  },
  (table) => [
    uniqueIndex("test_results_test_unique").on(
      table.testId,
    ),
  ],
);
