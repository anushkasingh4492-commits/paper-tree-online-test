import type { Question } from "@/types/question";

import physicsData from "../mht-cet/physics/question_bank_physics_with_figures_v1.3.0.json";
import chemistryData from "../mht-cet/chemistry/MHT-CET_Chemistry_question_bank_v2.0.0.json";
import biologyData from "../mht-cet/biology/MHT-CET_Biology_question_bank_v2.1.0.json";
import mathsData from "../mht-cet/maths/question_bank_maths_full_v2.0.1.json";

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
    exam: "MHT-CET",
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
    .map((item) =>
      convertQuestion(item as RawQuestion, subject)
    )
    .filter(
      (question): question is Question =>
        question !== null
    );
}

/*
 * REAL MHT-CET QUESTION DATA
 *
 * These questions come directly from:
 *
 * data/mht-cet/physics/
 * data/mht-cet/chemistry/
 * data/mht-cet/biology/
 * data/mht-cet/maths/
 *
 * No sample/demo questions are included here.
 */

export const mhtCetPhysicsQuestions = buildQuestions(
  physicsData,
  "Physics"
);

export const mhtCetChemistryQuestions = buildQuestions(
  chemistryData,
  "Chemistry"
);

export const mhtCetBiologyQuestions = buildQuestions(
  biologyData,
  "Biology"
);

export const mhtCetMathematicsQuestions = buildQuestions(
  mathsData,
  "Mathematics"
);

/*
 * ALL REAL MHT-CET QUESTIONS
 *
 * This is the export that existing code can use:
 *
 * import { mhtCetQuestions } from "@/data/questions/mht-cet";
 */

export const mhtCetQuestions: Question[] = [
  ...mhtCetPhysicsQuestions,
  ...mhtCetChemistryQuestions,
  ...mhtCetBiologyQuestions,
  ...mhtCetMathematicsQuestions,
];