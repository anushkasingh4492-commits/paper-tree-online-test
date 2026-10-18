export type Question = {
  id: string;
  exam: string;
  subject: string;
  chapter: string;
  difficulty: string;
  question: string;
  options: string[];
  answer: number;
  explanation: string;
  question_type?: "MCQ" | "MULTI_SELECT" | "TITA";
  answer_format?: "MCQ" | "TITA";
  tita_answer?: number | null;
  marks_correct?: number;
  marks_incorrect?: number;
  marks_unattempted?: number;
};