export type DashboardResult = {
  id: string;
  name: string;
  score: number;
  accuracy: number;
  date: string;
  time?: string;
  totalQuestions?: number;
  attempted?: number;
  difficulty?: string;
  subject?: string;
};

export type DashboardSubject = {
  subject: string;
  score: number;
  accuracy: number;
  total: number;
  attempted: number;
  correct: number;
  wrong: number;
  unanswered: number;
};

export type DashboardWeakArea = {
  topic?: string;
  chapter: string;
  subject: string;
  accuracy?: number;
  rate?: number;
  misses?: number;
  total?: number;
};

export type DashboardPayload = {
  success?: boolean;
  error?: string;
  student?: { id?: string; name?: string };
  assignment?: { batchId: string; batchName: string; courseName: string } | null;
  statistics?: {
    testsTaken?: number;
    averageScore?: number;
    bestScore?: number;
    attempts?: number;
    totalAttempts?: number;
    totalQuestions?: number;
    totalAttempted?: number;
    accuracy?: number;
    studyTime?: string;
  };
  results?: DashboardResult[];
  performanceTrend?: Array<{
    attemptId: string;
    testId: string;
    score: number;
    date?: string;
    formattedDate?: string;
    label?: string;
  }>;
  scoreDistribution?: {
    above90?: number;
    between70and89?: number;
    between50and69?: number;
    below50?: number;
  };
  subjectPerformance?: DashboardSubject[];
  weakAreas?: DashboardWeakArea[];
  notifications?: Array<{ isRead: boolean }>;
};

export type Badge = {
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
  earnedAt?: string | null;
};

export type StudentInsights = {
  testsCompleted: number;
  averagePercentage: number;
  streak: number;
  maxStreak: number;
  activityDays: string[];
  points: number;
  level: number;
  levelName: string;
  nextLevelName: string | null;
  nextLevelAt: number | null;
  levelProgress: number;
  badges: Badge[];
  weakAreas: DashboardWeakArea[];
};

export type LeaderboardMember = {
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
};

export type LeaderboardPayload = {
  success?: boolean;
  error?: string;
  batch?: {
    id: string;
    name: string;
    size: number;
    courseName?: string | null;
  } | null;
  students?: LeaderboardMember[];
  currentStudent?: LeaderboardMember | null;
};

export type GeneratorChapter = {
  subject: string;
  chapter: string;
  questionCount: number;
};
