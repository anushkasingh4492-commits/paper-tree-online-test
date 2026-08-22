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
};