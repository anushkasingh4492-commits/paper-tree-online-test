import type { Question } from "@/types/question";

/*
 * JEE question data loader.
 *
 * The JEE source data is supplied as zip archives in:
 *   data/JEE/physics/JEE_Main_Physics_v1.4.0.zip
 *   data/JEE/chemistry/JEE_Main_Chemistry_v1.1.0_FIXED.zip
 *   data/JEE/maths/JEE_Main_Maths_v1.0.1.zip
 *
 * Extract each zip to its subject folder and place the resulting
 * question_bank JSON file at the path expected below, then run
 *   node import-jee.js
 * to load the questions into the database.
 *
 * This module re-exports an empty array until data is extracted and imported.
 * The database-backed question loader (app/api/tests/generate/route.ts)
 * reads JEE questions directly from the `questions` table where exam = 'JEE'.
 */

type RawQuestion = {
  id?: string;
  standard?: number;
  chapter_number?: number;
  chapter_name?: string;
  major_topic?: string;
  subtopic?: string;
  stem?: string;
  question?: string;
  options?: {
    A?: string;
    B?: string;
    C?: string;
    D?: string;
  };
  correct_option?: string;
  correct_answer_text?: string;
  solution?: string;
  explanation?: string;
  difficulty?: string;
  question_type?: string;
  figure_asset?: string | null;
};

const LETTER_TO_INDEX: Record<string, number> = {
  A: 0,
  B: 1,
  C: 2,
  D: 3,
};

function normalizeDifficulty(
  difficulty?: string
): "Easy" | "Medium" | "Hard" {
  const value = String(difficulty ?? "").toLowerCase();

  if (value.includes("hard") || value.includes("difficult")) {
    return "Hard";
  }

  if (value.includes("medium") || value.includes("moderate")) {
    return "Medium";
  }

  return "Easy";
}

function convertQuestion(
  raw: RawQuestion,
  subject: string
): Question | null {
  const questionText = raw.stem ?? raw.question;

  if (!questionText) {
    return null;
  }

  const optionsObject = raw.options ?? {};

  const options = [
    optionsObject.A,
    optionsObject.B,
    optionsObject.C,
    optionsObject.D,
  ].filter(
    (option): option is string =>
      typeof option === "string" && option.trim().length > 0
  );

  if (options.length < 2) {
    return null;
  }

  const correctOption = String(raw.correct_option ?? "")
    .trim()
    .toUpperCase();

  const answer =
    correctOption in LETTER_TO_INDEX
      ? LETTER_TO_INDEX[correctOption]
      : -1;

  if (answer < 0 || answer >= options.length) {
    return null;
  }

  return {
    id: raw.id ?? `${subject.toLowerCase()}-${Math.random()}`,
    exam: "JEE",
    subject,
    chapter: raw.chapter_name ?? "General",
    difficulty: normalizeDifficulty(raw.difficulty),
    question: questionText,
    options,
    answer,
    explanation:
      raw.solution ??
      raw.explanation ??
      raw.correct_answer_text ??
      "",
  };
}

function buildQuestions(
  data: unknown,
  subject: string
): Question[] {
  if (!Array.isArray(data)) {
    return [];
  }

  return data
    .map((item) => convertQuestion(item as RawQuestion, subject))
    .filter(
      (question): question is Question =>
        question !== null
    );
}

/*
 * REAL JEE QUESTION DATA
 *
 * These questions come from the JEE Main zip archives in data/JEE/.
 * Extract the zips and run node import-jee.js to load them into the DB.
 *
 * No sample/demo questions are included here.
 */

export const jeePhysicsQuestions: Question[] = [];
export const jeeChemistryQuestions: Question[] = [];
export const jeeMathematicsQuestions: Question[] = [];

export const jeeQuestions: Question[] = [];
