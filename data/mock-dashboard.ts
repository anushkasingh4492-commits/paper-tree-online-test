/**
 * Paper Tree — Mock Dashboard Data
 * Part 1: Imports, Student Profile, Streak Data
 */

import type {
  StudentProfile,
  StreakData,
  MetricCard,
  BatchRanking,
  Trophy,
  DonutMetric,
  ChapterProgress,
  ActionCard,
  TrendPoint,
  ScoreDistribution,
  SubjectScore,
  RecentTest,
  WeakArea,
  TestSubject,
  TestDifficulty,
  TestPreset,
  LeaderboardStudent,
  PodiumStudent,
} from "@/types/dashboard";

export const studentProfile: StudentProfile = {
  id: "stu_001",
  firstName: "Hazel",
  lastName: "V",
  email: "hazel.v@example.com",
  level: 2,
  levelTitle: "RISING PLAYER",
  xp: 403,
  testsRemainingToNextLevel: 3,
  streakDays: 12,
  totalBadges: 3,
  averagePercentage: 5.0,
  avatarKey: "girl-07",
  courseName: "NEET",
  courseGroup: "PCB",
};

export const streakData: StreakData = {
  currentStreak: 12,
  status: "active",
  testsToGo: 3,
  days: [
    { day: "Sat", date: "10 Oct", active: true, missed: false, isToday: false },
    { day: "Sun", date: "11 Oct", active: true, missed: false, isToday: false },
    { day: "Mon", date: "12 Oct", active: false, missed: true, isToday: false },
    { day: "Tue", date: "13 Oct", active: true, missed: false, isToday: true },
    { day: "Wed", date: "14 Oct", active: true, missed: false, isToday: false },
    { day: "Thu", date: "15 Oct", active: false, missed: false, isToday: false },
    { day: "Fri", date: "16 Oct", active: false, missed: false, isToday: false },
  ],
};

export const metricCards: MetricCard[] = [
  { label: "Tests Taken", value: "2", trend: "↑ 1 from last week", trendDirection: "up", icon: "test-tube", subtitle: "Assessments completed" },
  { label: "Average Score (%)", value: "5.0%", trend: "↑ 2% in average accuracy", trendDirection: "up", icon: "analytics", subtitle: "Overall performance" },
  { label: "Best Score (%)", value: "9.0%", trend: "↑ by 7%", trendDirection: "up", icon: "trophy", subtitle: "Highest score achieved" },
  { label: "Attempts", value: "6", trend: "→ 2 more attempts", trendDirection: "neutral", icon: "clock", subtitle: "Total test attempts" },
  { label: "Assessment Time", value: "7m", trend: "→ 3 minutes more time", trendDirection: "neutral", icon: "clock", subtitle: "Avg time per test" },
];

export const batchRanking: BatchRanking = {
  batchName: "Sample Academy",
  batchRank: "#3",
  rankLabel: "Top performer",
  trend: "↑ 2 ranks up from last month",
  trendDirection: "up",
  trophyIcon: "trophy",
  studyTime: "1h 32m",
  averageScore: 78,
  targetsAttempted: 2,
  targetsAttemptedLabel: "2 / 3",
  members: [
    { id: "bm_001", name: "Bhavesh L.", avatarKey: "boy-03", level: 4, averageScore: 78, rank: 1, isCurrent: false },
    { id: "bm_002", name: "Gopi G.", avatarKey: "girl-05", level: 5, averageScore: 82, rank: 2, isCurrent: false },
    { id: "bm_003", name: "Hazel V.", avatarKey: "girl-07", level: 5, averageScore: 85, rank: 3, isCurrent: true },
  ],
  viewScoreboardLink: "/student/batch-leaderboard",
};

export const trophies: Trophy[] = [
  { id: "trophy_001", name: "Crushing It I", category: "Score", tier: 1, target: 1, progress: 0, unlocked: true, asset: null, detail: "Score 50%+ on your first test.", color: "from-amber-300 via-yellow-400 to-orange-500" },
  { id: "trophy_002", name: "Crushing It II", category: "Score", tier: 2, target: 10, progress: 0, unlocked: false, asset: null, detail: "Score 50%+ on 10 tests.", color: "from-cyan-300 via-sky-500 to-indigo-600" },
  { id: "trophy_003", name: "Crushing It III", category: "Score", tier: 3, target: 25, progress: 0, unlocked: false, asset: null, detail: "Score 50%+ on 25 tests.", color: "from-violet-300 via-purple-500 to-fuchsia-600" },
  { id: "trophy_004", name: "Crushing It IV", category: "Score", tier: 4, target: 50, progress: 0, unlocked: false, asset: null, detail: "Score 50%+ on 50 tests.", color: "from-fuchsia-300 via-violet-500 to-indigo-700" },
  { id: "trophy_005", name: "Streak Starter", category: "Streak", tier: 1, target: 3, progress: 12, unlocked: true, asset: null, detail: "Maintain a 3-day streak.", color: "from-orange-400 via-red-500 to-pink-500" },
  { id: "trophy_006", name: "Streak Warrior", category: "Streak", tier: 2, target: 7, progress: 12, unlocked: true, asset: null, detail: "Maintain a 7-day streak.", color: "from-orange-400 via-red-500 to-pink-500" },
  { id: "trophy_007", name: "Improvement I", category: "Improvement", tier: 1, target: 5, progress: 2, unlocked: true, asset: null, detail: "Improve your score by 5%.", color: "from-cyan-300 via-sky-500 to-indigo-600" },
  { id: "trophy_008", name: "Mastery I", category: "Mastery", tier: 1, target: 10, progress: 0, unlocked: false, asset: null, detail: "Master 10 chapters.", color: "from-emerald-300 via-green-500 to-teal-600" },
  { id: "trophy_009", name: "Boss Fight", category: "Boss", tier: 1, target: 1, progress: 0, unlocked: false, asset: null, detail: "Complete a Boss Fight test.", color: "from-pink-300 via-rose-500 to-red-600" },
];

export const trophyCategories = ["All", "Score", "Streak", "Improvement", "Mastery", "Memory", "Boss", "Teamwork", "Ultimate"];

export const donutMetrics: DonutMetric[] = [
  { label: "Total Mistakes", value: 52, percentage: 52, color: "red", icon: "alert" },
  { label: "Unresolved", value: 50, percentage: 50, color: "amber", icon: "clock" },
  { label: "Mastered", value: 2, percentage: 2, color: "green", icon: "check" },
];

export const chapterProgress: ChapterProgress[] = [
  { chapter: "Motion", subject: "Physics", progress: 90, color: "red" },
  { chapter: "Animal Kingdom", subject: "Biology", progress: 86, color: "orange" },
  { chapter: "Factors, Processes and Events in Biological Sciences", subject: "Biology", progress: 92, color: "red" },
  { chapter: "Biodiversity and Conservation", subject: "Biology", progress: 90, color: "orange" },
];

export const actionCards: ActionCard[] = [
  { id: "action_best_practice", title: "Best Practice", subtitle: "Revisit questions from chapters where you've made mistakes and track your improvement.", cta: "Practise Now →", icon: "book", color: "bg-gradient-to-br from-indigo-600 to-blue-700" },
  { id: "action_level_progress", title: "Level 2 – Rising Player", subtitle: "Complete 3 more tests to reach Level 3 and continue your progress.", cta: "View Progress →", icon: "trophy", color: "bg-gradient-to-br from-purple-500 to-fuchsia-600" },
  { id: "action_ai_generated_test", title: "AI Generated Test", subtitle: "Generate a personalised test based on your performance and weaker areas.", cta: "Generate Test →", icon: "sparkles", color: "bg-gradient-to-br from-violet-600 to-indigo-700" },
  { id: "action_badges_unlocked", title: "7 Badges Unlocked", subtitle: "View your earned badges and explore the achievements you can unlock next.", cta: "View Badges →", icon: "star", color: "bg-gradient-to-br from-yellow-400 to-orange-500" },
];

export const performanceTrend: TrendPoint[] = [
  { date: "18 Oct", score: 50 }, { date: "19 Oct", score: 55 }, { date: "20 Oct", score: 45 },
  { date: "21 Oct", score: 60 }, { date: "22 Oct", score: 65 }, { date: "23 Oct", score: 70 },
  { date: "24 Oct", score: 75 },
];

export const scoreDistribution: ScoreDistribution[] = [
  { range: "0% – 25%", percentage: 52, count: 6, color: "red" },
  { range: "26% – 50%", percentage: 26, count: 3, color: "orange" },
  { range: "51% – 75%", percentage: 14, count: 2, color: "yellow" },
  { range: "76% – 100%", percentage: 8, count: 1, color: "green" },
];

export const subjectScores: SubjectScore[] = [
  { subject: "Physics", score: 85.4, color: "blue" },
  { subject: "Chemistry", score: 82.1, color: "blue" },
  { subject: "Botany", score: 74.8, color: "green" },
  { subject: "Zoology", score: 72.3, color: "green" },
];

export const recentTests: RecentTest[] = [
  { id: "rt_001", name: "NEET 2026 Mock Test 1", score: 5.2, accuracy: 5.4, date: "12 Oct 2026" },
  { id: "rt_002", name: "NEET 2026 Mock Test 2", score: 5.1, accuracy: 5.6, date: "12 Oct 2026" },
  { id: "rt_003", name: "NEET 2026 Mock Test 3", score: 5.2, accuracy: 5.6, date: "12 Oct 2026" },
  { id: "rt_004", name: "NEET 2026 Mock Test 4", score: 5.2, accuracy: 5.6, date: "12 Oct 2026" },
  { id: "rt_005", name: "NEET 2026 Mock Test 5", score: 5.1, accuracy: 5.6, date: "10 Oct 2026" },
];

export const weakAreas: WeakArea[] = [
  { topic: "Biodiversity and Conservation", flagged: true },
  { topic: "Plant Growth and Development", flagged: true },
  { topic: "Floral diagram", flagged: true },
  { topic: "Trap in Insecta", flagged: true },
  { topic: "Motion", flagged: true },
];

export const testSubjects: TestSubject[] = [
  { id: "physics", name: "Physics", code: "PH", description: "Mechanics, electricity, optics & more", chapters: [
    { id: "ch_001", name: "Basic Concepts of Chemistry", selected: false },
    { id: "ch_002", name: "Structure of Atom", selected: false },
    { id: "ch_003", name: "Classification of Elements and Periodicity in Properties", selected: false },
    { id: "ch_004", name: "Chemical Bonding and Molecular Structure", selected: false },
    { id: "ch_005", name: "States of Matter", selected: false },
    { id: "ch_006", name: "Thermodynamics", selected: false },
  ]},
  { id: "chemistry", name: "Chemistry", code: "CH", description: "Physical, organic & inorganic chemistry", chapters: [
    { id: "ch_007", name: "Basic Concepts of Chemistry", selected: false },
    { id: "ch_008", name: "Structure of Atom", selected: false },
    { id: "ch_009", name: "Classification of Elements", selected: false },
  ]},
  { id: "biology", name: "Biology", code: "BI", description: "Botany, zoology & human biology", chapters: [
    { id: "ch_010", name: "Diversity in Living World", selected: false },
    { id: "ch_011", name: "Structural Organisation in Animals", selected: false },
    { id: "ch_012", name: "Cell Structure and Function", selected: false },
  ]},
];

export const testDifficulties: TestDifficulty[] = [
  { id: "easy", label: "Easy", subtitle: "Gentle pace", selected: false },
  { id: "moderate", label: "Moderate", subtitle: "Steady challenge", selected: true },
  { id: "balanced", label: "Balanced", subtitle: "Mix of both", selected: false },
  { id: "hard", label: "Hard", subtitle: "High intensity", selected: false },
];

export const testPresets: TestPreset[] = [
  { id: "half_paper", name: "Half paper", description: "Physics 25 + Chemistry 25 + Biology 25 | 90 questions per subject", questionSplit: "Physics 25 + Chemistry 25 + Biology 25", totalMarks: 100, duration: "90 minutes", selected: true },
  { id: "custom_length", name: "Custom length", description: "Physics 25 + Chemistry 25 + Biology 40 questions per subject", questionSplit: "Physics 25 + Chemistry 25 + Biology 40", totalMarks: 90, duration: "85 minutes", selected: false },
  { id: "full_paper", name: "Full paper", description: "Physics 45 + Chemistry 45 + Biology 90 questions per subject", questionSplit: "Physics 45 + Chemistry 45 + Biology 90", totalMarks: 180, duration: "165 minutes", selected: false },
];

export const leaderboardStudents: LeaderboardStudent[] = [
  { id: "lb_001", name: "Hazel V.", avatarKey: "girl-07", average: 78, testsTaken: 12, questionsSeen: 530, rank: 1, isCurrent: true, avgScore: 78, bestScore: 92 },
  { id: "lb_002", name: "Bhavesh L.", avatarKey: "boy-03", average: 68, testsTaken: 8, questionsSeen: 300, rank: 2, isCurrent: false, avgScore: 68, bestScore: 85 },
  { id: "lb_003", name: "Gopi G.", avatarKey: "girl-05", average: 62, testsTaken: 6, questionsSeen: 210, rank: 3, isCurrent: false, avgScore: 62, bestScore: 80 },
];

export const podiumStudents: PodiumStudent[] = [
  { ...leaderboardStudents[0], place: 1, completionPercentage: 20 },
  { ...leaderboardStudents[1], place: 2, completionPercentage: 20 },
  { ...leaderboardStudents[2], place: 3, completionPercentage: 20 },
];