/**
 * Paper Tree CAT mock patterns.
 *
 * CAT 2025 baseline supplied in the Paper Tree CBT CAT Mock Test Developer
 * Specification. Treat this as a configurable reference pattern, not as a
 * claim that all settings are verified against the official candidate UI.
 */
export type CatSectionKey = 'VARC' | 'DILR' | 'QA';
export type CatQuestionType = 'MCQ' | 'TITA';

export interface CatSectionPattern {
  key: CatSectionKey;
  name: string;
  questionCount: number;
  durationSeconds: number;
}

export interface CatScoringRule {
  correct: number;
  incorrectMcq: number;
  incorrectTita: number;
  unanswered: number;
}

export interface CatPattern {
  id: string;
  exam: 'CAT';
  year: number;
  label: string;
  status: 'reference' | 'verified';
  verifiedAt: string | null;
  totalDurationSeconds: number;
  sections: readonly CatSectionPattern[];
  scoring: CatScoringRule;
  sectionLocking: boolean;
  allowQuestionNavigationWithinSection: boolean;
  calculator: {
    enabled: boolean;
    kind: 'basic';
    pausesTimer: false;
  };
}

export const CAT_2025_PATTERN: CatPattern = {
  id: 'cat-2025-reference-v1',
  exam: 'CAT',
  year: 2025,
  label: 'CAT 2025 Reference Pattern',
  status: 'reference',
  verifiedAt: null,
  totalDurationSeconds: 120 * 60,
  sections: [
    { key: 'VARC', name: 'Verbal Ability and Reading Comprehension (8 VA + 16 RC across 4 passages)', questionCount: 24, durationSeconds: 40 * 60 },
    { key: 'DILR', name: 'Data Interpretation and Logical Reasoning (4–5 sets; target 24 questions)', questionCount: 24, durationSeconds: 40 * 60 },
    { key: 'QA', name: 'Quantitative Aptitude', questionCount: 24, durationSeconds: 40 * 60 },
  ],
  scoring: { correct: 3, incorrectMcq: -1, incorrectTita: 0, unanswered: 0 },
  sectionLocking: true,
  allowQuestionNavigationWithinSection: true,
  calculator: { enabled: true, kind: 'basic', pausesTimer: false },
};

/** Keep older published patterns immutable; create a new ID for each revision. */
export const CAT_PATTERNS: Readonly<Record<string, CatPattern>> = {
  [CAT_2025_PATTERN.id]: CAT_2025_PATTERN,
};

export function getCatPattern(patternId: string): CatPattern | undefined {
  return CAT_PATTERNS[patternId];
}

export function scoreCatResponse(input: {
  isAnswered: boolean;
  isCorrect: boolean;
  questionType: CatQuestionType;
  rule?: CatScoringRule;
}): number {
  const rule = input.rule ?? CAT_2025_PATTERN.scoring;
  if (!input.isAnswered) return rule.unanswered;
  if (input.isCorrect) return rule.correct;
  return input.questionType === 'MCQ' ? rule.incorrectMcq : rule.incorrectTita;
}

export function validateCatPattern(pattern: CatPattern): string[] {
  const errors: string[] = [];
  const sectionKeys = new Set<string>();
  for (const section of pattern.sections) {
    if (sectionKeys.has(section.key)) errors.push(`Duplicate section key: ${section.key}`);
    sectionKeys.add(section.key);
    if (!Number.isInteger(section.questionCount) || section.questionCount < 1) {
      errors.push(`${section.key}: questionCount must be a positive integer`);
    }
    if (!Number.isInteger(section.durationSeconds) || section.durationSeconds < 1) {
      errors.push(`${section.key}: durationSeconds must be a positive integer`);
    }
  }
  const questions = pattern.sections.reduce((sum, section) => sum + section.questionCount, 0);
  const duration = pattern.sections.reduce((sum, section) => sum + section.durationSeconds, 0);
  if (questions < 68 || questions > 72) errors.push(`CAT mock pattern should contain approximately 68–72 questions; configured ${questions}`);
  if (duration !== pattern.totalDurationSeconds) errors.push('Section durations must sum to totalDurationSeconds');
  if (pattern.sections.some(section => section.durationSeconds !== 40 * 60)) {
    errors.push('Reference CAT 2025 pattern expects 40 minutes per section');
  }
  if (pattern.scoring.correct < 0) errors.push('Correct-answer score cannot be negative');
  if (pattern.scoring.incorrectTita !== 0) errors.push('Default CAT TITA incorrect-answer score must be zero');
  return errors;
}
