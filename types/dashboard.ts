/**
 * Paper Tree — Dashboard Data Types
 * Single source of truth for all dashboard, test generator, and leaderboard types.
 */

/* ============================================================
   Student Profile
============================================================ */
export type StudentProfile = {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  level: number;
  levelTitle: string;
  xp: number;
  testsRemainingToNextLevel: number;
  streakDays: number;
  totalBadges: number;
  averagePercentage: number;
  avatarKey?: string | null;
  courseName: string;
  courseGroup: string;
};

/* ============================================================
   Streak Data
============================================================ */
export type StreakDay = {
  day: string; // Sat, Sun, Mon, Tue, Wed, Thu, Fri
  date: string;
  active: boolean;
  missed: boolean;
  isToday: boolean;
};

export type StreakData = {
  currentStreak: number;
  status: "active" | "going-strong" | "missed";
  days: StreakDay[];
  testsToGo: number;
};

/* ============================================================
   Stats / Metrics
============================================================ */
export type MetricCard = {
  label: string;
  value: string | number;
  trend?: string;
  trendDirection?: "up" | "down" | "neutral";
  icon?: string;
  subtitle?: string;
};

/* ============================================================
   Batch
============================================================ */
export type BatchMember = {
  id: string;
  name: string;
  avatarKey?: string | null;
  level: number;
  averageScore: number;
  rank: number;
  isCurrent: boolean;
};

export type BatchRanking = {
  batchName: string;
  batchRank: string;
  rankLabel: string;
  trend: string;
  trendDirection: "up" | "down" | "neutral";
  trophyIcon: React.ReactNode;
  studyTime: string;
  averageScore: number;
  targetsAttempted: number;
  targetsAttemptedLabel: string;
  members: BatchMember[];
  viewScoreboardLink: string;
};

/* ============================================================
   Trophy
============================================================ */
export type Trophy = {
  id: string;
  name: string;
  category: string;
  tier: number; // I, II, III, IV...
  target: number;
  progress: number;
  unlocked: boolean;
  asset?: string | null;
  detail: string;
  color: string; // gradient class
};

/* ============================================================
   Question Overview / Chapter Mastery
============================================================ */
export type DonutMetric = {
  label: string;
  value: number;
  percentage: number;
  color: "red" | "amber" | "green";
  icon: React.ReactNode;
};

export type ChapterProgress = {
  chapter: string;
  subject: string;
  progress: number;
  color: string;
};

/* ============================================================
   Target Weak Areas
============================================================ */
export type ActionCard = {
  id: string;
  title: string;
  subtitle: string;
  cta: string;
  icon: string;
  color: string;
  onClick?: () => void;
};

/* ============================================================
   Performance Trends
============================================================ */
export type TrendPoint = {
  date: string;
  score: number;
};

export type ScoreDistribution = {
  range: string;
  percentage: number;
  count: number;
  color: string;
};

export type SubjectScore = {
  subject: string;
  score: number;
  color: string;
};

export type RecentTest = {
  id: string;
  name: string;
  score: number;
  accuracy: number;
  date: string;
};

export type WeakArea = {
  topic: string;
  flagged: boolean;
  accuracy?: number;
};

/* ============================================================
   Test Generator
============================================================ */
export type TestSubject = {
  id: string;
  name: string;
  code: string;
  description: string;
  chapters: TestChapter[];
};

export type TestChapter = {
  id: string;
  name: string;
  selected: boolean;
};

export type TestDifficulty = {
  id: string;
  label: string;
  subtitle: string;
  selected: boolean;
};

export type TestPreset = {
  id: string;
  name: string;
  description: string;
  questionSplit: string;
  totalMarks: number;
  duration: string;
  selected: boolean;
};

export type TestConfig = {
  subjects: string[];
  chapters: string[];
  difficulty: string;
  preset: TestPreset | null;
  totalQuestions: number;
  totalMarks: number;
  durationMinutes: number;
};

/* ============================================================
   Leaderboard
============================================================ */
export type LeaderboardStudent = {
  id: string;
  name: string;
  avatarKey?: string | null;
  average: number;
  testsTaken: number;
  questionsSeen: number;
  rank: number;
  isCurrent: boolean;
  avgScore: number;
  bestScore: number;
};

export type PodiumPlace = 1 | 2 | 3;

export type PodiumStudent = LeaderboardStudent & {
  place: PodiumPlace;
  completionPercentage: number;
};

export type DashboardPayload = {
  success: boolean;
  error?: string;
  student: {
    id: string;
    name: string;
    email?: string | null;
  };
  assignment: {
    batchId: string;
    batchName: string;
    courseName: string;
  } | null;
  statistics: {
    testsTaken: number;
    averageScore: number;
    bestScore: number;
    attempts: number;
    totalAttempts: number;
    totalQuestions: number;
    totalAttempted: number;
    totalCorrect: number;
    totalWrong: number;
    totalUnanswered: number;
    accuracy: number;
    studyTimeMinutes: number;
    studyTime: string;
  };
  performanceTrend: Array<{
    attemptId: string;
    score: number;
    date: string;
    formattedDate: string;
    label: string;
  }>;
  scoreDistribution: {
    above90: number;
    between70and89: number;
    between50and69: number;
    below50: number;
  };
  subjectPerformance: Array<{
    subject: string;
    score: number;
    accuracy: number;
    total: number;
    attempted: number;
    correct: number;
    wrong: number;
    unanswered: number;
  }>;
  chapterPerformance: Array<{
    subject: string;
    chapter: string;
    total: number;
    attempted: number;
    correct: number;
    wrong: number;
    unanswered: number;
    accuracy: number;
  }>;
  weakAreas: Array<{
    topic: string;
    chapter: string;
    subject: string;
    score: number;
    accuracy: number;
    attempted: number;
    correct: number;
    wrong: number;
    unanswered: number;
  }>;
  results: Array<{
    attemptId: string;
    name: string;
    score: number;
    accuracy: number;
    date: string;
    rawDate: string;
    totalQuestions: number;
    attempted: number;
  }>;
  notifications?: Array<{
    isRead: boolean;
  }>;
};

export type DashboardInsights = {
  testsCompleted: number;
  averagePercentage: number;
  streak: number;
  maxStreak: number;
  activityDays: string[];
  points: number;
  level: number;
  levelName: string;
  nextLevelAt: number | null;
  levelProgress: number;
  badges: Array<{
    id: string;
    name: string;
    icon: string;
    asset?: string | null;
    category: string;
    tier: number;
    earned: boolean;
    progress: number;
    target: number;
    detail: string;
    subject?: string | null;
  }>;
};

export type DashboardLeaderboard = {
  batch: {
    id: string;
    name: string;
    size: number;
    assignedTestCount: number;
    courseName?: string | null;
  } | null;
  students: Array<{
    id: string;
    name: string;
    avatarKey?: string | null;
    average: number;
    bestScore: number;
    completionPercent: number | null;
    testsTaken: number;
    questionsSeen: number;
    rank: number;
    isCurrent: boolean;
  }>;
  currentStudent: {
    id: string;
    name: string;
    avatarKey?: string | null;
    average: number;
    bestScore: number;
    completionPercent: number | null;
    testsTaken: number;
    questionsSeen: number;
    rank: number;
    isCurrent: boolean;
  } | null;
};

export type DashboardMistakeStats = {
  total: number;
  unresolved: number;
};