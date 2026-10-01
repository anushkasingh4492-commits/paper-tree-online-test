import { pool } from "@/lib/db";
import { ensureFeatureSchema } from "@/lib/feature-schema";

export const LEVELS = [
  { level: 1, name: "Rookie", tests: 0 },
  { level: 2, name: "Rising Player", tests: 5 },
  { level: 3, name: "Grinder", tests: 15 },
  { level: 4, name: "Challenger", tests: 30 },
  { level: 5, name: "Pro", tests: 50 },
  { level: 6, name: "Elite", tests: 80 },
  { level: 7, name: "Master", tests: 120 },
  { level: 8, name: "Grandmaster", tests: 170 },
  { level: 9, name: "Legend", tests: 240 },
  { level: 10, name: "Mythic", tests: 350 },
  { level: 11, name: "GOAT", tests: 500 },
] as const;

const COMPLETED = new Set(["submitted", "auto_submitted", "auto submitted", "completed", "complete"]);
const IST = "Asia/Kolkata";

function done(status: unknown) {
  return COMPLETED.has(String(status ?? "").trim().toLowerCase().replace(/-/g, "_"));
}

function istDay(value: unknown) {
  if (!value) return "";
  return new Intl.DateTimeFormat("en-CA", { timeZone: IST }).format(new Date(String(value)));
}

function daysBetween(a: string, b: string) {
  const aa = new Date(`${a}T00:00:00+05:30`).getTime();
  const bb = new Date(`${b}T00:00:00+05:30`).getTime();
  return Math.round(Math.abs(bb - aa) / 86400000);
}

function tierFor(count: number) {
  if (count >= 50) return 4;
  if (count >= 25) return 3;
  if (count >= 10) return 2;
  if (count >= 1) return 1;
  return 0;
}

function maxConsecutive(days: string[]) {
  const sorted = [...new Set(days)].sort();
  let best = 0;
  let run = 0;
  let previous = "";
  for (const day of sorted) {
    if (!previous || daysBetween(previous, day) === 1) run += 1;
    else run = 1;
    best = Math.max(best, run);
    previous = day;
  }
  return best;
}

function currentStreak(days: string[]) {
  const set = new Set(days);
  let cursor = istDay(new Date());
  if (!set.has(cursor)) {
    const d = new Date(`${cursor}T12:00:00+05:30`);
    d.setDate(d.getDate() - 1);
    cursor = d.toLocaleDateString("en-CA", { timeZone: IST });
  }
  let count = 0;
  while (set.has(cursor)) {
    count += 1;
    const d = new Date(`${cursor}T12:00:00+05:30`);
    d.setDate(d.getDate() - 1);
    cursor = d.toLocaleDateString("en-CA", { timeZone: IST });
  }
  return count;
}

function hasConsecutive(days: string[], target: number) {
  return maxConsecutive(days) >= target;
}

function pct(attempt: any) {
  return Number(attempt.total_marks) > 0 ? (Number(attempt.score) / Number(attempt.total_marks)) * 100 : 0;
}

export type BadgeView = {
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
  earnedAt?: string | null;
};

export async function getStudentGamification(studentId: string, academyId: string) {
  await ensureFeatureSchema();

  const attemptsResult = await pool.query(
    `SELECT
       ta.id, ta.test_id, ta.scheduled_test_id, ta.submitted_at, ta.started_at, ta.score, ta.total_marks,
       ta.correct_count, ta.incorrect_count, ta.unanswered_count,
       COALESCE(t.question_count, 0)::int AS question_count,
       COALESCE(t.difficulty, '') AS difficulty,
       t.questions,
       COUNT(CASE WHEN ans.selected_answer IS NOT NULL THEN 1 END)::int AS answered_count
     FROM test_attempts ta
     LEFT JOIN tests t ON t.id = COALESCE(ta.test_id, ta.scheduled_test_id)
     LEFT JOIN test_answers ans ON ans.attempt_id = ta.id
     WHERE ta.student_id = $1
       AND LOWER(REPLACE(COALESCE(ta.status,''),'-','_')) IN ('submitted','auto_submitted','auto submitted','completed','complete')
     GROUP BY ta.id, t.question_count, t.difficulty, t.questions
     ORDER BY COALESCE(ta.submitted_at, ta.started_at, ta.created_at) ASC`,
    [studentId]
  );
  const attempts = attemptsResult.rows.map((attempt) => {
    let parsed: any[] = [];
    if (Array.isArray(attempt.questions)) parsed = attempt.questions;
    else if (typeof attempt.questions === "string") { try { const value = JSON.parse(attempt.questions); if (Array.isArray(value)) parsed = value; } catch {} }
    const subjects = [...new Set(parsed.map((q: any) => String(q?.subject || q?.subject_name || "").trim()).filter(Boolean))];
    return { ...attempt, subject: subjects.length === 1 ? subjects[0] : null };
  });

  const qualifying = attempts.filter((a) =>
    Number(a.question_count) >= 20 &&
    ["medium", "hard", "mixed"].includes(String(a.difficulty).trim().toLowerCase()) &&
    Number(a.answered_count) >= Math.ceil(Number(a.question_count) * 0.5)
  );

  const capped: any[] = [];
  const perDay = new Map<string, number>();
  for (const a of qualifying) {
    const day = istDay(a.submitted_at || a.started_at);
    if (!day) continue;
    const count = perDay.get(day) ?? 0;
    if (count < 3) {
      perDay.set(day, count + 1);
      capped.push(a);
    }
  }

  // Streaks are based on ALL completed tests. The final catalogue says
  // “take at least one test every day”; it does not restrict streaks to
  // qualifying tests. Multiple tests on the same IST day count as one day.
  const allTestDays = attempts.map((a) => istDay(a.submitted_at || a.started_at)).filter(Boolean);
  const streak = currentStreak(allTestDays);
  const maxStreak = maxConsecutive(allTestDays);

  // Levels are based on every completed test. Qualifying-test rules are
  // reserved for XP/advanced metrics and do not block normal level progression.
  const levelTestCount = attempts.length;
  let levelIndex = 0;
  for (let i = 0; i < LEVELS.length; i++) {
    if (levelTestCount >= LEVELS[i].tests) levelIndex = i;
  }
  const currentLevel = LEVELS[levelIndex];
  const next = LEVELS[levelIndex + 1] ?? null;
  const progress = next
    ? Math.min(100, Math.max(0, ((levelTestCount - currentLevel.tests) / Math.max(1, next.tests - currentLevel.tests)) * 100))
    : 100;

  const answeredQualifying = qualifying.reduce((sum, a) => sum + Number(a.answered_count || 0), 0);
  const average = attempts.length
    ? attempts.reduce((sum, a) => sum + pct(a), 0) / attempts.length
    : 0;

  // Score badges: each test awards only its highest score badge.
  const scoreCounts = { crushing: 0, beast: 0, flawless: 0 };
  for (const a of attempts) {
    const score = pct(a);
    if (score >= 100) scoreCounts.flawless += 1;
    else if (score >= 90) scoreCounts.beast += 1;
    else if (score >= 75) scoreCounts.crushing += 1;
  }

  // Improvement: 15 percentage points over the previous five qualifying tests,
  // matching subject + difficulty. The current test itself is excluded from the five.
  const improvementCounts = new Map<string, number>();
  for (let i = 0; i < attempts.length; i++) {
    const current = attempts[i];
    const subject = String(current.subject || "").trim();
    const difficulty = String(current.difficulty || "").trim().toLowerCase();
    if (!subject || !difficulty) continue;
    const previous = attempts.slice(0, i).filter((a) => String(a.subject || "").trim() === subject && String(a.difficulty || "").trim().toLowerCase() === difficulty).slice(-5);
    if (previous.length === 5) {
      const avgPrev = previous.reduce((s, a) => s + pct(a), 0) / 5;
      if (pct(current) >= avgPrev + 15) improvementCounts.set(`${subject}::${difficulty}`, (improvementCounts.get(`${subject}::${difficulty}`) ?? 0) + 1);
    }
  }
  const improvementEarns = [...improvementCounts.values()].reduce((a, b) => a + b, 0);

  // Comeback: a qualifying test after at least 14 full calendar days without one.
  let comebackEarns = 0;
  for (let i = 1; i < attempts.length; i++) {
    const previous = istDay(attempts[i - 1].submitted_at || attempts[i - 1].started_at);
    const current = istDay(attempts[i].submitted_at || attempts[i].started_at);
    if (previous && current && daysBetween(previous, current) >= 15) comebackEarns += 1;
  }

  // Volume thresholds count answered questions from qualifying tests only.
  const volume = attempts.reduce((sum, a) => sum + Number(a.answered_count || 0), 0);

  // Full-chapter analysis. We use the actual question bank topics represented by
  // major_topic/subtopic and require the test to contain all topics available for
  // that subject/chapter in the question bank.
  const fullChapterAttempts: any[] = [];
  for (const a of attempts) {
    let questionIds: string[] = [];
    if (Array.isArray(a.questions)) questionIds = a.questions.map((q: any) => String(q?.id || q?.question_id || "")).filter(Boolean);
    else if (typeof a.questions === "string") {
      try {
        const parsed = JSON.parse(a.questions);
        if (Array.isArray(parsed)) questionIds = parsed.map((q: any) => String(q?.id || q?.question_id || "")).filter(Boolean);
      } catch {}
    }
    if (questionIds.length < 25) continue;
    const rows = await pool.query(
      `SELECT id, subject, chapter_name, major_topic, subtopic FROM questions WHERE id = ANY($1::text[])`,
      [questionIds]
    );
    const qs = rows.rows;
    if (!qs.length) continue;
    const chapters = new Set(qs.map((q) => String(q.chapter_name || "").trim()).filter(Boolean));
    const subjects = new Set(qs.map((q) => String(q.subject || "").trim()).filter(Boolean));
    if (chapters.size !== 1 || subjects.size !== 1) continue;
    const subject = [...subjects][0];
    const chapter = [...chapters][0];
    const topicsInTest = new Set(qs.map((q) => String(q.subtopic || q.major_topic || "").trim()).filter(Boolean));
    if (!topicsInTest.size) continue;
    const allTopicsResult = await pool.query(
      `SELECT DISTINCT COALESCE(NULLIF(subtopic,''), NULLIF(major_topic,'')) AS topic
       FROM questions
       WHERE subject = $1 AND chapter_name = $2 AND COALESCE(NULLIF(subtopic,''), NULLIF(major_topic,'')) IS NOT NULL`,
      [subject, chapter]
    );
    const allTopics = new Set(allTopicsResult.rows.map((r) => String(r.topic || "").trim()).filter(Boolean));
    const coversEveryTopic = allTopics.size === 0 || [...allTopics].every((topic) => topicsInTest.has(topic));
    if (coversEveryTopic) fullChapterAttempts.push({ ...a, subject, chapter, score: pct(a), date: a.submitted_at || a.started_at });
  }

  const chapterGroups = new Map<string, any[]>();
  for (const a of fullChapterAttempts) {
    const key = `${a.subject}::${a.chapter}`;
    if (!chapterGroups.has(key)) chapterGroups.set(key, []);
    chapterGroups.get(key)!.push(a);
  }

  const bossEarns = new Map<string, number>();
  for (const [key, list] of chapterGroups) {
    let i = 0;
    let earns = 0;
    while (i + 2 < list.length) {
      const window = list.slice(i, i + 3);
      if (window.every((x) => x.score >= 85)) {
        earns += 1;
        i += 3; // repeat earns may not reuse any test from the previous set
      } else {
        i += 1;
      }
    }
    if (earns) bossEarns.set(key, earns);
  }

  // Rank badges are based on teacher-assigned tests only. The catalogue does
  // not require these tests to be “qualifying”. Participants are the students
  // in the exact batch assigned to that scheduled test who actually submitted it.
  let podiumEarns = 0;
  let mvpEarns = 0;
  const rankTests = [...new Set(attempts.filter((a) => a.scheduled_test_id).map((a) => String(a.scheduled_test_id)))];
  for (const scheduledTestId of rankTests) {
    const rankResult = await pool.query(
      `SELECT student_id, score, total_marks
       FROM (
         SELECT DISTINCT ON (ta.student_id)
                ta.student_id, ta.score, ta.total_marks
         FROM test_attempts ta
         INNER JOIN scheduled_tests st ON st.id = ta.scheduled_test_id
         INNER JOIN batch_students bs
           ON bs.batch_id = st.batch_id
          AND bs.student_id = ta.student_id
         INNER JOIN batches b ON b.id = st.batch_id
         WHERE ta.scheduled_test_id = $1
           AND b.academy_id = $2
           AND COALESCE(ta.total_marks, 0) > 0
           AND LOWER(REPLACE(COALESCE(ta.status,''),'-','_')) IN ('submitted','auto_submitted','auto submitted','completed','complete')
         ORDER BY ta.student_id, COALESCE(ta.submitted_at, ta.started_at, ta.created_at) DESC
       ) participants`,
      [scheduledTestId, academyId]
    );
    const scores = rankResult.rows.map((r) => ({ studentId: String(r.student_id), pct: Number(r.total_marks) > 0 ? (Number(r.score) / Number(r.total_marks)) * 100 : 0 }));
    scores.sort((a, b) => b.pct - a.pct);
    const mine = scores.findIndex((r) => r.studentId === studentId);
    if (mine >= 0) {
      const myScore = scores[mine].pct;
      const rank = scores.filter((r) => r.pct > myScore).length + 1;
      if (rank === 1) mvpEarns += 1;
      else if (rank === 2 || rank === 3) podiumEarns += 1;
    }
  }

  const assignedSubjectResult = await pool.query(
    `SELECT DISTINCT q.subject
     FROM batch_students bs
     INNER JOIN batches b ON b.id = bs.batch_id
     INNER JOIN scheduled_tests st ON st.batch_id = bs.batch_id
     INNER JOIN paper_questions pq ON pq.paper_id = st.paper_id
     INNER JOIN questions q ON q.id = pq.question_id
     WHERE bs.student_id = $1 AND b.academy_id = $2
       AND q.subject IS NOT NULL AND TRIM(q.subject) <> ''`,
    [studentId, academyId]
  );
  const assignedSubjectsFromBatch = [...new Set(assignedSubjectResult.rows.map((r) => String(r.subject || '').trim()).filter(Boolean))];
  const allAssignedSubjects = assignedSubjectsFromBatch.length
    ? assignedSubjectsFromBatch
    : [...new Set(fullChapterAttempts.map((a) => String(a.subject).trim()).filter(Boolean))];
  const explorerSubjects = await Promise.all(allAssignedSubjects.map(async (subject) => {
    const allChapters = await pool.query(`SELECT DISTINCT chapter_name FROM questions WHERE subject = $1 AND chapter_name IS NOT NULL AND TRIM(chapter_name) <> ''`, [subject]);
    const covered = new Set(fullChapterAttempts.filter((a) => a.subject === subject).map((a) => a.chapter));
    const chapters = allChapters.rows.map((r) => String(r.chapter_name || '').trim()).filter(Boolean);
    return { subject, complete: chapters.length > 0 && chapters.every((chapter) => covered.has(chapter)), covered: covered.size, total: chapters.length };
  }));
  // Immortal: every subject the student studies must have at least 3
  // full-chapter tests, with the average across those full-chapter tests at 90%+.
  const subjectHistory = allAssignedSubjects;
  const immortalSubjects = subjectHistory.filter((subject) => {
    const list = fullChapterAttempts.filter((a) => a.subject === subject);
    return list.length >= 3 && list.reduce((s, a) => s + a.score, 0) / list.length >= 90;
  });
  const immortalEarned = subjectHistory.length > 0 && immortalSubjects.length === subjectHistory.length;

  const asset = (path: string) => `/badges/${path}`;
  const tierThresholds = [0, 1, 10, 25, 50] as const;

  const badge = (b: Omit<BadgeView, "tier"> & { count?: number; tier?: number; asset?: string | null }): BadgeView => {
    const count = Number(b.count ?? b.progress ?? 0);
    const tier = b.tier ?? 0;
    return {
      id: b.id,
      name: b.name,
      icon: b.icon,
      asset: b.asset ?? null,
      category: b.category,
      tier,
      earned: b.earned,
      progress: b.progress,
      target: b.target,
      detail: b.detail,
      subject: b.subject,
      earnedAt: b.earnedAt,
    };
  };

  const tieredBadge = (baseId: string, name: string, category: string, count: number, detail: string, folder: string, fileBase: string): BadgeView[] =>
    [1, 2, 3, 4].map((tier) => {
      const target = tierThresholds[tier];
      return badge({
        id: `${baseId}-t${tier}`,
        name,
        icon: "",
        asset: asset(`${folder}/${fileBase}_t${tier}.png`),
        category,
        tier,
        earned: count >= target,
        progress: Math.min(count, target),
        target,
        detail: `${detail} Earn this badge ${target === 1 ? "once" : `${target} times`}.`,
        count,
      });
    });

  const badges: BadgeView[] = [
    ...tieredBadge("crushing-it", "Crushing It", "Score", scoreCounts.crushing, "Score 75% to 89.99% in a test.", "Score-20260930T135946Z-1-001/Score", "crushing-it"),
    ...tieredBadge("beast-mode", "Beast Mode", "Score", scoreCounts.beast, "Score 90% to 99.99% in a test.", "Score-20260930T135946Z-1-001/Score", "beast-mode"),
    ...tieredBadge("flawless", "Flawless", "Score", scoreCounts.flawless, "Score a perfect 100% in a test.", "Score-20260930T135946Z-1-001/Score", "flawless"),
    badge({ id: "streak-7", name: "7-Day Streak", icon: "", asset: asset("Streak-20260930T135944Z-1-001/Streak/streak_007.png"), category: "Streak", earned: maxStreak >= 7, progress: Math.min(maxStreak, 7), target: 7, detail: "Take at least one test every day for 7 days in a row." }),
    badge({ id: "streak-30", name: "30-Day Streak", icon: "", asset: asset("Streak-20260930T135944Z-1-001/Streak/streak_030.png"), category: "Streak", earned: maxStreak >= 30, progress: Math.min(maxStreak, 30), target: 30, detail: "Take at least one test every day for 30 days in a row." }),
    badge({ id: "streak-100", name: "100-Day Streak", icon: "", asset: asset("Streak-20260930T135944Z-1-001/Streak/streak_100.png"), category: "Streak", earned: maxStreak >= 100, progress: Math.min(maxStreak, 100), target: 100, detail: "Take at least one test every day for 100 days in a row." }),
    badge({ id: "streak-200", name: "200-Day Streak", icon: "", asset: asset("Streak-20260930T135944Z-1-001/Streak/streak_200.png"), category: "Streak", earned: maxStreak >= 200, progress: Math.min(maxStreak, 200), target: 200, detail: "Take at least one test every day for 200 days in a row." }),
    badge({ id: "streak-365", name: "365-Day Streak", icon: "", asset: asset("Streak-20260930T135944Z-1-001/Streak/streak_365.png"), category: "Streak", earned: maxStreak >= 365, progress: Math.min(maxStreak, 365), target: 365, detail: "Take at least one test every day for a full year without missing a day." }),
    ...tieredBadge("glow-up", "Glow Up", "Improvement", improvementEarns, "Score at least 15 percentage points above your own average of your previous 5 tests in the same subject and difficulty.", "Improvement-20260930T140000Z-1-001/Improvement", "glow-up"),
    badge({ id: "1k-club", name: "1K Club", icon: "", asset: asset("Volume-20260930T135937Z-1-001/Volume/1k-club.png"), category: "Volume", earned: volume >= 1000, progress: Math.min(volume, 1000), target: 1000, detail: "Answer 1,000 questions in total." }),
    badge({ id: "5k-club", name: "5K Club", icon: "", asset: asset("Volume-20260930T135937Z-1-001/Volume/5k-club.png"), category: "Volume", earned: volume >= 5000, progress: Math.min(volume, 5000), target: 5000, detail: "Answer 5,000 questions in total." }),
    badge({ id: "10k-club", name: "10K Club", icon: "", asset: asset("Volume-20260930T135937Z-1-001/Volume/10k-club.png"), category: "Volume", earned: volume >= 10000, progress: Math.min(volume, 10000), target: 10000, detail: "Answer 10,000 questions in total." }),
    badge({ id: "25k-club", name: "25K Club", icon: "", asset: asset("Volume-20260930T135937Z-1-001/Volume/25k-club.png"), category: "Volume", earned: volume >= 25000, progress: Math.min(volume, 25000), target: 25000, detail: "Answer 25,000 questions in total." }),
    ...explorerSubjects.map((item) => badge({ id: `explorer-${item.subject.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`, name: "Explorer", icon: "", asset: asset("Mastery-20260930T135949Z-1-001/Mastery/explorer.png"), category: "Mastery", earned: item.complete, progress: item.covered, target: item.total, detail: `Take at least one full-chapter test in every chapter of ${item.subject}.`, subject: item.subject })),
    ...tieredBadge("boss-level", "Boss Level Cleared", "Mastery", [...bossEarns.values()].reduce((a, b) => a + b, 0), "Average 85% or more across 3 full-chapter tests of the same chapter.", "Mastery-20260930T135949Z-1-001/Mastery", "boss-level"),
    ...allAssignedSubjects.map((subject) => {
      const cleared = [...chapterGroups.entries()].filter(([key, earns]) => key.startsWith(`${subject}::`) && earns.length > 0).length;
      return badge({ id: `final-boss-${subject.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`, name: "Final Boss", icon: "", asset: asset("Mastery-20260930T135949Z-1-001/Mastery/final-boss.png"), category: "Mastery", earned: cleared >= 5, progress: cleared, target: 5, detail: `Clear Boss Level in 5 different chapters of ${subject}.`, subject });
    }),
    badge({ id: "immortal", name: "Immortal", icon: "", asset: asset("Mastery-20260930T135949Z-1-001/Mastery/immortal.png"), category: "Mastery", earned: immortalEarned, progress: immortalSubjects.length, target: Math.max(1, subjectHistory.length), detail: "Average 90% or more in full-chapter tests in every subject you study, with at least 3 tests per subject.", earnedAt: immortalEarned ? new Date(Math.max(...fullChapterAttempts.filter((a) => immortalSubjects.includes(a.subject)).map((a) => new Date(a.date).getTime()))).toISOString() : null }),
    ...tieredBadge("podium", "Podium", "Rank", podiumEarns, "Finish 2nd or 3rd in your batch in a teacher-assigned test.", "Rank-20260930T135947Z-1-001/Rank", "podium"),
    ...tieredBadge("mvp", "MVP", "Rank", mvpEarns, "Finish 1st in your batch in a teacher-assigned test.", "Rank-20260930T135947Z-1-001/Rank", "mvp"),
    badge({ id: "welcome-back", name: "Welcome Back", icon: "", asset: asset("Comeback-20260930T140006Z-1-001/Comeback/welcome-back.png"), category: "Comeback", earned: comebackEarns > 0, progress: Math.min(comebackEarns, 1), target: 1, detail: "Take a test after being away for 14 days or more." }),
  ];

  // Completionist: every badge in the catalogue except Rank and Welcome Back.
  // For tiered families this means all four tiers must have been earned at least once.
  const scoreComplete = scoreCounts.crushing >= 50 && scoreCounts.beast >= 50 && scoreCounts.flawless >= 50;
  const streakComplete = maxStreak >= 365;
  const improvementComplete = improvementEarns >= 50;
  const volumeComplete = volume >= 25000;
  const allSubjectsExplorer = allAssignedSubjects.length > 0 && explorerSubjects.every((x) => x.complete);
  const allSubjectsFinalBoss = allAssignedSubjects.length > 0 && allAssignedSubjects.every((subject) => {
    const cleared = [...chapterGroups.entries()].filter(([key, earns]) => key.startsWith(`${subject}::`) && earns.length > 0).length;
    return cleared >= 5;
  });
  const bossComplete = [...bossEarns.values()].reduce((a, b) => a + b, 0) >= 50;
  const masteryComplete = allSubjectsExplorer && bossComplete && allSubjectsFinalBoss && immortalEarned;
  const ultimateEarned = scoreComplete && streakComplete && improvementComplete && volumeComplete && masteryComplete;
  badges.push(badge({ id: "ultimate", name: "Completionist", icon: "", asset: asset("Ultimate-20260930T135942Z-1-001/Ultimate/completionist.png"), category: "Ultimate", earned: ultimateEarned, progress: ultimateEarned ? 1 : 0, target: 1, detail: "Earn every badge at least once, except rank badges and Welcome Back." }));

  const weak = await pool.query(
    `SELECT q.chapter_name, q.subject,
            COUNT(*) FILTER (WHERE ta.is_correct = false OR ta.selected_answer IS NULL)::int AS misses,
            COUNT(*)::int AS total
     FROM test_answers ta
     INNER JOIN test_attempts att ON att.id = ta.attempt_id
     INNER JOIN questions q ON q.id = ta.question_id
     WHERE att.student_id = $1
     GROUP BY q.chapter_name, q.subject
     HAVING COUNT(*) >= 2
     ORDER BY (COUNT(*) FILTER (WHERE ta.is_correct = false OR ta.selected_answer IS NULL)::numeric / COUNT(*)::numeric) DESC
     LIMIT 4`,
    [studentId]
  );

  const xp = attempts.length * 100 + Math.round(average * 2) + streak * 25 + badges.filter((b) => b.earned).length * 50;
  const lastActiveValue = attempts.length ? (attempts[attempts.length - 1].submitted_at || attempts[attempts.length - 1].started_at) : null;
  const lastActiveDate = lastActiveValue
    ? new Intl.DateTimeFormat("en-IN", {
        timeZone: IST,
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: true,
      }).format(new Date(String(lastActiveValue)))
    : null;

  return {
    rank: null as number | null,
    batchSize: 0,
    batchName: "",
    testsCompleted: attempts.length,
    qualifyingTests: capped.length,
    averagePercentage: Number(average.toFixed(1)),
    streak,
    maxStreak,
    lastActiveDate,
    points: xp,
    level: currentLevel.level,
    levelName: currentLevel.name,
    nextLevelName: next?.name ?? null,
    nextLevelAt: next?.tests ?? null,
    levelProgress: Number(progress.toFixed(1)),
    badges,
    weakAreas: weak.rows.map((row) => ({ chapter: row.chapter_name, subject: row.subject, misses: Number(row.misses), total: Number(row.total), rate: Number(((Number(row.misses) / Math.max(1, Number(row.total))) * 100).toFixed(1)) })),
    qualifying,
  };
}
