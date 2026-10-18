import type { Question } from "@/types/question";

import catData from "../cat/qa/CAT_QA_v1.0.0/cat_qa_v1.0.0.json";

type RawCatQuestion = {
  id?: string;
  section?: string;
  area?: string;
  chapter?: string;
  topic?: string;
  subtopic?: string;
  chapter_number?: number;
  question?: string;
  stem?: string;
  answer_format?: "MCQ" | "TITA";
  options?: Record<string, string>;
  correct_option?: string;
  correct_answer?: string;
  tita_answer?: number | null;
  explanation?: string;
  solution?: string;
  difficulty?: string;
  difficulty_reason?: string;
  cognitive_level?: string;
  question_type?: string;
  concept_family?: string;
  figures?: Array<{ file?: string } | string>;
  figure_required?: boolean;
  marks_correct?: number;
  marks_incorrect?: number;
  marks_unattempted?: number;
  release_version?: string;
};

function normalizeDifficulty(difficulty?: string): "Easy" | "Medium" | "Hard" {
  const value = String(difficulty ?? "").toLowerCase();

  if (value.includes("hard") || value.includes("difficult")) {
    return "Hard";
  }

  if (value.includes("medium") || value.includes("moderate")) {
    return "Medium";
  }

  return "Easy";
}

function convertQuestion(raw: RawCatQuestion): Question | null {
  const questionText = raw.stem ?? raw.question;

  if (!questionText) {
    return null;
  }

  const isTita = raw.answer_format === "TITA";

  const options: string[] = isTita
    ? []
    : Object.values(raw.options ?? {}).filter(
        (option): option is string =>
          typeof option === "string" && option.trim().length > 0
      );

  // For MCQ, correct_option is a letter (A/B/C/D). Convert to index.
  let answer = -1;
  if (!isTita && raw.correct_option) {
    const letter = String(raw.correct_option).trim().toUpperCase();
    const index = "ABCD".indexOf(letter);
    if (index >= 0 && index < options.length) {
      answer = index;
    }
  }

  return {
    id: raw.id ?? `cat-${Math.random().toString(36).slice(2)}`,
    exam: "CAT",
    subject: raw.section ?? "Quantitative Ability",
    chapter: raw.chapter ?? "General",
    difficulty: normalizeDifficulty(raw.difficulty),
    question: questionText,
    options,
    answer: isTita ? raw.tita_answer ?? -1 : answer,
    explanation:
      raw.solution ??
      raw.explanation ??
      raw.correct_answer ??
      "",
    question_type: isTita ? "TITA" : "MCQ",
    answer_format: isTita ? "TITA" : "MCQ",
    tita_answer: raw.tita_answer,
    marks_correct: raw.marks_correct ?? 3,
    marks_incorrect: raw.marks_incorrect ?? 0,
    marks_unattempted: raw.marks_unattempted ?? 0,
  };
}

function buildQuestions(data: unknown): Question[] {
  if (!Array.isArray(data)) {
    return [];
  }

  return data
    .map((item) => convertQuestion(item as RawCatQuestion))
    .filter((question): question is Question => question !== null);
}

/*
 * REAL CAT QUESTION DATA
 *
 * These questions come directly from:
 * data/cat/qa/CAT_QA_v1.0.0/cat_qa_v1.0.0.json
 *
 * Contains 3000 CAT-style questions (1950 MCQ, 1050 TITA).
 * No sample/demo questions are included here.
 */

export const catQuestions: Question[] = buildQuestions(catData);
