"use client";

import { useEffect, useMemo, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  AlertTriangle,
  ArrowRight,
  Award,
  BookOpenCheck,
  CalendarDays,
  Check,
  Clock3,
  Layers3,
  LockKeyhole,
  Target,
  TrendingUp,
  Trophy,
} from "lucide-react";
import { LeftSidebar } from "@/components/LeftSidebar";
import { TopNavbar } from "@/components/TopNavbar";
import { fetchStudentData } from "@/components/student/student-api";
import type {
  DashboardInsights,
  DashboardLeaderboard,
  DashboardMistakeStats,
  DashboardPayload,
  MetricCard,
  RecentTest,
  ScoreDistribution,
  SubjectScore,
  TrendPoint,
  WeakArea,
} from "@/types/dashboard";
import styles from "./dashboard.module.css";

type DashboardData = {
  dashboard: DashboardPayload;
  insights: DashboardInsights | null;
  insightsError: string | null;
  leaderboard: DashboardLeaderboard | null;
  leaderboardError: string | null;
  mistakeStats: DashboardMistakeStats | null;
  mistakeStatsError: string | null;
};

function getErrorMessage(reason: unknown, fallback: string) {
  return reason instanceof Error && reason.message ? reason.message : fallback;
}

function formatPercent(value: number) {
  return `${Number(value || 0).toFixed(1)}%`;
}

function formatDate(value: string) {
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? value
    : date.toLocaleDateString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
      });
}

function saveStudentTheme(enabled: boolean) {
  try {
    window.localStorage.setItem("paperTreeStudentDarkMode", String(enabled));
    window.dispatchEvent(new Event("paperTreeStudentThemeChange"));
  } catch (error) {
    console.error("Could not save the student theme preference.", error);
  }
}

function getActivityWeek(activityDays: string[]) {
  const todayKey = new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Kolkata" }).format(new Date());
  const today = new Date(`${todayKey}T12:00:00+05:30`);
  const saturdayOffset = (today.getUTCDay() + 1) % 7;
  today.setUTCDate(today.getUTCDate() - saturdayOffset);

  return Array.from({ length: 7 }, (_, index) => {
    const date = new Date(today);
    date.setUTCDate(today.getUTCDate() + index);
    const dateKey = new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Kolkata" }).format(date);
    return {
      dateKey,
      day: new Intl.DateTimeFormat("en", { timeZone: "Asia/Kolkata", weekday: "short" }).format(date),
      active: activityDays.includes(dateKey),
      isToday: dateKey === todayKey,
      isFuture: dateKey > todayKey,
    };
  });
}

function getWeeklyTestCounts(trend: DashboardPayload["performanceTrend"]) {
  const todayKey = new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Kolkata" }).format(new Date());
  const today = new Date(`${todayKey}T12:00:00+05:30`);
  const monday = new Date(today);
  monday.setUTCDate(today.getUTCDate() - ((today.getUTCDay() + 6) % 7));
  const counts = Array(7).fill(0) as number[];

  trend.forEach((test) => {
    const parsedDate = new Date(test.date);
    if (Number.isNaN(parsedDate.getTime())) return;
    const dateKey = new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Kolkata" }).format(parsedDate);
    const date = new Date(`${dateKey}T12:00:00+05:30`);
    if (Number.isNaN(date.getTime()) || date < monday || date > today) return;
    counts[(date.getUTCDay() + 6) % 7] += 1;
  });
  return counts;
}

function getChartPoints(data: TrendPoint[]) {
  const width = 560;
  const points = data.slice(-7).map((point, index, list) => {
    const x = list.length === 1 ? width / 2 : 41 + (index / (list.length - 1)) * 491;
    const score = Math.max(0, Math.min(100, point.score));
    return { x, y: 17 + ((100 - score) / 100) * 116, date: point.date, score };
  });
  const line = points.map((point, index) => `${index ? "L" : "M"}${point.x},${point.y}`).join(" ");
  const area = points.length > 1
    ? `${line} L${points[points.length - 1].x},133 L${points[0].x},133 Z`
    : "";
  return { points, line, area };
}

export default function DashboardPage() {
  const router = useRouter();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [darkMode, setDarkMode] = useState(() => {
    if (typeof window === "undefined") return false;
    try {
      return window.localStorage.getItem("paperTreeStudentDarkMode") === "true";
    } catch {
      return false;
    }
  });

  useEffect(() => {
    const syncTheme = () => {
      try {
        setDarkMode(window.localStorage.getItem("paperTreeStudentDarkMode") === "true");
      } catch {
        setDarkMode(false);
      }
    };

    window.addEventListener("storage", syncTheme);
    return () => window.removeEventListener("storage", syncTheme);
  }, []);

  useEffect(() => {
    let active = true;

    Promise.allSettled([
      fetchStudentData<DashboardPayload>("/api/dashboard"),
      fetchStudentData<DashboardInsights>("/api/student/insights"),
      fetchStudentData<DashboardLeaderboard>("/api/student/batch-leaderboard"),
      fetchStudentData<{ stats: DashboardMistakeStats }>(
        "/api/student/mistakes?limit=1"
      ),
    ])
      .then(([dashboardResult, insightsResult, leaderboardResult, mistakesResult]) => {
        if (active) {
          if (dashboardResult.status === "rejected") {
            throw dashboardResult.reason;
          }
          const insights = insightsResult.status === "fulfilled" ? insightsResult.value : null;
          const leaderboard = leaderboardResult.status === "fulfilled" ? leaderboardResult.value : null;
          const mistakes = mistakesResult.status === "fulfilled" ? mistakesResult.value : null;
          setData({
            dashboard: dashboardResult.value,
            insights,
            leaderboard,
            insightsError: insightsResult.status === "rejected"
              ? getErrorMessage(insightsResult.reason, "Could not load your progress.")
              : null,
            leaderboardError: leaderboardResult.status === "rejected"
              ? getErrorMessage(leaderboardResult.reason, "Could not load your batch leaderboard.")
              : null,
            mistakeStats: mistakes?.stats ?? null,
            mistakeStatsError: mistakesResult.status === "rejected"
              ? getErrorMessage(mistakesResult.reason, "Could not load your mistake data.")
              : null,
          });
        }
      })
      .catch((cause: unknown) => {
        if (active) {
          if (
            cause instanceof Error &&
            /^(Student login required|Student session not found|Invalid student session)\.?$/.test(cause.message)
          ) {
            router.replace("/student-login");
            return;
          }
          setError(cause instanceof Error ? cause.message : "Could not load your dashboard.");
        }
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, [router]);

  useEffect(() => {
    document.body.classList.toggle("student-dashboard-dark", darkMode);
    return () => document.body.classList.remove("student-dashboard-dark");
  }, [darkMode]);

  // All hooks must run unconditionally every render. Guard inside for null data.
  const dashboard = data?.dashboard;
  const insights = data?.insights;

  const metrics = useMemo<MetricCard[]>(() => {
    if (!dashboard) return [];
    const { statistics } = dashboard;
    return [
      { label: "Tests Taken", value: statistics.testsTaken, subtitle: "Completed assessments", icon: "test-tube" },
      { label: "Average Score", value: formatPercent(statistics.averageScore), subtitle: "Across completed tests", icon: "analytics" },
      { label: "Best Score", value: formatPercent(statistics.bestScore), subtitle: "Personal best", icon: "trophy" },
      { label: "Attempts", value: statistics.totalAttempts, subtitle: "All test attempts", icon: "analytics" },
      { label: "Assessment Time", value: statistics.studyTime, subtitle: "Time spent learning", icon: "clock" },
    ];
  }, [dashboard]);

  const trend: TrendPoint[] = useMemo(
    () => {
      if (!dashboard) return [];
      return (dashboard.performanceTrend ?? []).slice(-7).map((point) => ({
        date: point.formattedDate || formatDate(point.date),
        score: point.score,
      }));
    },
    [dashboard]
  );

  const distribution: ScoreDistribution[] = useMemo(() => {
    if (!dashboard) return [];
    const sd = dashboard.scoreDistribution;
    const total = sd.above90 + sd.between70and89 + sd.between50and69 + sd.below50;
    const pct = (n: number) => (total ? Math.round((n / total) * 100) : 0);
    const rangeColor = (range: string) => {
      if (range === "90% - 100%") return "green";
      if (range === "70% - 89%") return "blue";
      if (range === "50% - 69%") return "amber";
      return "red";
    };
    return [
      { range: "90% - 100%", percentage: pct(sd.above90), count: sd.above90, color: rangeColor("90% - 100%") },
      { range: "70% - 89%", percentage: pct(sd.between70and89), count: sd.between70and89, color: rangeColor("70% - 89%") },
      { range: "50% - 69%", percentage: pct(sd.between50and69), count: sd.between50and69, color: rangeColor("50% - 69%") },
      { range: "Below 50%", percentage: pct(sd.below50), count: sd.below50, color: rangeColor("Below 50%") },
    ];
  }, [dashboard]);

  const subjects: SubjectScore[] = useMemo(() => {
    if (!dashboard) return [];
    const subjectColor = (score: number) =>
      score >= 70 ? "text-emerald-500" : score >= 50 ? "text-amber-500" : "text-rose-500";
    return (dashboard.subjectPerformance ?? []).map((subject) => ({
      subject: subject.subject,
      score: subject.score,
      color: subjectColor(subject.score),
    }));
  }, [dashboard]);

  const recentTests: RecentTest[] = useMemo(() => {
    if (!dashboard) return [];
    return (dashboard.results ?? []).slice(0, 5).map((test, index) => ({
      id: test.attemptId || `test-${index}`,
      name: test.name,
      score: test.score,
      accuracy: test.accuracy,
      date: test.date || formatDate(test.rawDate),
    }));
  }, [dashboard]);

  const weakAreas: WeakArea[] = useMemo(() => {
    if (!dashboard) return [];
    return (dashboard.weakAreas ?? []).map((area) => ({
      topic: `${area.subject}: ${area.chapter}`,
      flagged: area.accuracy < 50,
      accuracy: area.accuracy,
    }));
  }, [dashboard]);

  const studentName = dashboard?.student.name || "Student";
  const [nameFirstPart, ...nameRest] = studentName.trim().split(/\s+/);
  const firstName = nameFirstPart || "Student";
  const lastName = nameRest.join(" ");
  const courseName = dashboard?.assignment?.courseName || "No course assigned";
  if (loading) {
    return (
      <div className={styles.loading}>
        <div className={styles.loadingCard}>Loading your dashboard…</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.loading}>
        <div role="alert" className={styles.errorCard}>
          <strong>Couldn’t load your dashboard</strong>
          <p>{error}</p>
          <button type="button" onClick={() => window.location.reload()}>Try again</button>
        </div>
      </div>
    );
  }

  if (!dashboard) return null;

  // dashboard existing implies data (and thus insights/leaderboard/mistakeStats) exists
  const currentStudent = data.leaderboard?.currentStudent ?? null;
  const activityWeek = insights ? getActivityWeek(insights.activityDays) : [];
  const weeklyTests = getWeeklyTestCounts(dashboard.performanceTrend);
  const maxWeeklyTests = Math.max(...weeklyTests, 1);
  const chart = getChartPoints(trend);
  const completedTests = dashboard.statistics.testsTaken;
  const mistakeTotal = data.mistakeStats?.total ?? null;
  const unresolvedMistakes = data.mistakeStats?.unresolved ?? null;
  const resolvedMistakes = mistakeTotal === null || unresolvedMistakes === null
    ? null
    : Math.max(0, mistakeTotal - unresolvedMistakes);
  const weakestChapters = dashboard.chapterPerformance
    .filter((chapter) => chapter.attempted > 0)
    .sort((left, right) => left.accuracy - right.accuracy)
    .slice(0, 4);
  const badges = insights?.badges ?? [];
  const earnedBadges = badges.filter((badge) => badge.earned).length;
  const avgSecondsPerQuestion = dashboard.statistics.totalAttempted
    ? Math.round((dashboard.statistics.studyTimeMinutes * 60) / dashboard.statistics.totalAttempted)
    : null;

  return (
    <div className={`${styles.root} ${darkMode ? styles.dark : ""}`}>
      <div className={styles.appLayout}>
        <LeftSidebar
          className="hidden xl:flex"
          onCollapsedChange={setSidebarCollapsed}
          student={{
            firstName,
            lastName,
            courseName,
            avatarKey: currentStudent?.avatarKey,
          }}
        />
        <main className={`${styles.main} ${sidebarCollapsed ? styles.collapsed : ""}`}>
          <TopNavbar
            student={{
              firstName,
              lastName,
              courseName,
              avatarKey: currentStudent?.avatarKey,
            }}
            darkMode={darkMode}
            onDarkModeChange={(enabled) => {
              setDarkMode(enabled);
              saveStudentTheme(enabled);
            }}
            unreadNotifications={
              dashboard.notifications?.filter((notification) => !notification.isRead).length ?? 0
            }
          />

          <div className={styles.content}>
            <section className={styles.hero} aria-label="Player progress and streak">
              <div className={styles.heroProgress}>
                <div className={styles.heroLabel}><TrendingUp size={15} /> Player progress</div>
                <Link href="/achievements" className={styles.levelLink}>Tap to view level <ArrowRight size={12} /></Link>
                <div className={styles.levelLine}>
                  <span className={styles.levelNumber}><small>Level</small>{insights?.level ?? "—"}</span>
                  <span className={styles.heroDivider} />
                  <span className={styles.levelName}>{insights?.levelName ?? "Progress unavailable"}</span>
                  <Image src="/images/login/Level Two Bar Chart with Golden Arrow.png" alt="" width={100} height={80} className={styles.levelArt} />
                </div>
                <div className={styles.progressMeta}>
                  <span>Level progress</span>
                  <span>{insights ? insights.nextLevelAt === null ? "Max level reached" : `${Math.max(0, insights.nextLevelAt - insights.testsCompleted)} more tests to go` : "Progress data unavailable"}</span>
                </div>
                <div className={styles.progressRail} role={insights ? "progressbar" : undefined} aria-label="Level progress" aria-valuemin={insights ? 0 : undefined} aria-valuemax={insights ? 100 : undefined} aria-valuenow={insights ? insights.levelProgress : undefined}>
                  {insights && <span style={{ width: `${Math.min(100, Math.max(0, insights.levelProgress))}%` }} />}
                </div>
                <div className={styles.heroStats}>
                  <span><Award size={17} />{insights ? `${insights.points} XP` : "XP unavailable"}</span>
                  <span><Trophy size={17} />{insights ? `${earnedBadges} badges` : "Badges unavailable"}</span>
                  <span><TrendingUp size={16} />{completedTests ? formatPercent(dashboard.statistics.averageScore) : "—"} avg.</span>
                </div>
              </div>
              <div className={styles.heroStreak}>
                <div className={styles.heroLabel}>Day streak</div>
                <div className={styles.streakTotal}>
                  <div><strong>{insights?.streak ?? "—"}</strong><span>streak days</span></div>
                  <Image
                    src={insights?.streak ? "/images/login/Vibrant Gradient Flame with Sparkles.png" : "/images/login/Glowing Blue Layered Flame.png"}
                    alt=""
                    width={76}
                    height={76}
                    className={styles.flameArt}
                  />
                </div>
                {insights ? <div className={styles.streakWeek} aria-label="Activity for the current week">
                    {activityWeek.map((day) => (
                      <div className={`${styles.streakDay} ${day.active ? styles.streakComplete : ""} ${day.isToday ? styles.streakToday : ""}`} key={day.dateKey}>
                        <span>{day.active ? <Check size={15} /> : day.isFuture ? "○" : "–"}</span>
                        <small>{day.day}</small>
                      </div>
                    ))}
                  </div> : <p className={styles.heroDataError}>{data.insightsError}</p>}
              </div>
            </section>

            <section className={styles.metrics} aria-label="Performance overview">
              {metrics.map((metric, index) => (
                <article className={styles.metric} key={metric.label}>
                  <span className={`${styles.metricIcon} ${styles[`metricTone${index}`]}`}>
                    {index === 0 ? <CalendarDays size={18} /> : index === 1 ? <TrendingUp size={18} /> : index === 2 ? <Trophy size={18} /> : index === 3 ? <BookOpenCheck size={18} /> : <Clock3 size={18} />}
                  </span>
                  <span className={styles.metricLabel}>{metric.label}</span>
                  <strong>{metric.value}</strong>
                  <small>{metric.subtitle}</small>
                </article>
              ))}
            </section>

            <section className={`${styles.card} ${styles.batch}`} id="batch">
              <div className={`${styles.batchColumn} ${styles.rankPanel}`}>
                <h2>Your batch</h2>
                <p>{data.leaderboard?.batch?.name ?? (data.leaderboardError ? "Leaderboard unavailable" : "Batch ranking")}</p>
                <span className={styles.eyebrow}>Batch rank</span>
                <strong className={styles.rankNumber}>{currentStudent ? `#${currentStudent.rank}` : "—"}</strong>
                <span className={styles.rankCaption}>
                  {currentStudent && data.leaderboard?.batch
                    ? `Rank ${currentStudent.rank} of ${data.leaderboard.batch.size}`
                    : data.leaderboardError
                      ? "Your rank is temporarily unavailable"
                      : "Complete an assigned test to see your rank"}
                </span>
                <Image src="/images/login/Glossy Purple Trophy with Stars.png" alt="" width={150} height={155} className={styles.trophyArt} />
              </div>
              <div className={`${styles.batchColumn} ${styles.weekPanel}`}>
                <div className={styles.batchHeading}>
                  <div><span className={styles.eyebrow}>Tests this week</span><strong>{weeklyTests.reduce((sum, count) => sum + count, 0)}</strong><span>completed</span></div>
                  <CalendarDays size={26} />
                </div>
                <div className={styles.weekBars} aria-label="Completed tests by weekday">
                  {weeklyTests.map((count, index) => (
                    <div className={styles.weekBar} key={index}>
                      <span style={{ height: `${count ? Math.max(8, (count / maxWeeklyTests) * 100) : 5}%` }} title={`${count} tests`} />
                      <small>{["M", "T", "W", "T", "F", "S", "S"][index]}</small>
                    </div>
                  ))}
                </div>
                <div className={styles.batchStats}>
                  <span><b>{dashboard.statistics.studyTime}</b><small>Study time</small></span>
                  <span><b>{currentStudent ? formatPercent(currentStudent.average) : "—"}</b><small>Batch average</small></span>
                  <span><b>{currentStudent?.completionPercent == null ? "—" : `${currentStudent.completionPercent.toFixed(0)}%`}</b><small>Assigned completion</small></span>
                </div>
              </div>
              <div className={`${styles.batchColumn} ${styles.leaderPanel}`}>
                <div className={styles.panelHeading}><h2>Batch leaderboard</h2><Link href="/student/batch-leaderboard">View scoreboard <ArrowRight size={13} /></Link></div>
                {data.leaderboard?.students.length ? (
                  <div className={styles.leaderList}>
                    {data.leaderboard.students.slice(0, 3).map((member) => (
                      <div className={styles.leader} key={member.id}>
                        <span className={styles.avatar}>{member.name.split(/\s+/).map((part) => part[0]).join("").slice(0, 2)}</span>
                        <span className={styles.leaderInfo}><b>{member.name}{member.isCurrent ? " (You)" : ""}</b><small>Rank #{member.rank} · {formatPercent(member.average)} avg.</small></span>
                        <span className={styles.leaderRank}>#{member.rank}</span>
                      </div>
                    ))}
                  </div>
                ) : <p className={styles.emptyInline}>{data.leaderboardError ?? (data.leaderboard?.batch ? "Leaderboard data will appear after students complete tests." : "You are not assigned to a batch yet.")}</p>}
              </div>
            </section>

            <section className={`${styles.card} ${styles.trophyPanel}`} id="achievements">
              <div className={styles.sectionHeading}>
                <div className={styles.sectionTitleWrap}><Trophy size={22} /><div><h2>Trophy wall</h2><p>{insights ? `${earnedBadges} of ${badges.length} earned · Milestones from your account` : "Badge progress is unavailable right now."}</p></div></div>
                <Link href="/achievements" className={styles.textLink}>View all <ArrowRight size={14} /></Link>
              </div>
              {badges.length ? (
                <div className={styles.badgeGrid}>
                  {badges.slice(0, 4).map((badge) => (
                    <article className={styles.badgeCard} key={badge.id}>
                      <span className={`${styles.badgeImage} ${badge.earned ? "" : styles.badgeLocked}`}>
                        {badge.asset ? <Image src={badge.asset} alt="" width={64} height={64} unoptimized /> : badge.earned ? <Trophy size={30} /> : <LockKeyhole size={25} />}
                      </span>
                      <span className={styles.badgeInfo}><b>{badge.name}</b><small>{badge.earned ? "Earned" : `${badge.progress} / ${badge.target} progress`}</small><span><i style={{ width: `${badge.target > 0 ? Math.min(100, badge.progress / badge.target * 100) : 0}%` }} /></span></span>
                    </article>
                  ))}
                </div>
              ) : <p className={styles.emptyInline}>{data.insightsError ?? "Your achievement progress will appear here."}</p>}
            </section>

            <section className={`${styles.card} ${styles.questionPanel}`} id="question-overview">
              <div className={styles.sectionHeading}>
                <div><h2>Question overview</h2><p>{dashboard.statistics.totalAttempted} of {dashboard.statistics.totalQuestions} questions attempted across your completed tests.</p></div>
                <Link href="/stats" className={styles.textLink}>Detailed analysis <ArrowRight size={14} /></Link>
              </div>
              {data.mistakeStats ? <div className={styles.mistakeGrid}>
                {[
                  { label: "Total mistakes", value: mistakeTotal, color: styles.mistakeRed, icon: <AlertTriangle size={20} />, percent: mistakeTotal ? 100 : 0 },
                  { label: "Unresolved", value: unresolvedMistakes, color: styles.mistakeAmber, icon: <Clock3 size={20} />, percent: mistakeTotal ? Math.round((unresolvedMistakes ?? 0) / mistakeTotal * 100) : 0 },
                  { label: "Mastered", value: resolvedMistakes, color: styles.mistakeGreen, icon: <Check size={20} />, percent: mistakeTotal ? Math.round((resolvedMistakes ?? 0) / mistakeTotal * 100) : 0 },
                ].map((item) => (
                  <article className={`${styles.mistakeCard} ${item.color}`} key={item.label}>
                    <span className={styles.mistakeIcon}>{item.icon}</span>
                    <span><small>{item.label}</small><strong>{item.value}</strong></span>
                    <span className={styles.ring} style={{ background: `conic-gradient(currentColor ${item.percent}%, #e8ebf4 ${item.percent}% 100%)` }}><b>{item.percent}%</b></span>
                  </article>
                ))}
              </div> : <p className={styles.emptyInline}>{data.mistakeStatsError ?? "Mistake data will appear as you complete tests."}</p>}
            </section>

            <section className={`${styles.card} ${styles.chapters}`}>
              <span className={styles.chapterLabel}>Chapter mastery</span>
              <h2>Chapters to focus on</h2>
              {weakestChapters.length ? <div className={styles.chapterGrid}>
                {weakestChapters.map((chapter) => (
                  <div className={styles.chapterItem} key={`${chapter.subject}-${chapter.chapter}`}>
                    <div><span title={`${chapter.subject}: ${chapter.chapter}`}>{chapter.subject}: {chapter.chapter}</span><b>{formatPercent(chapter.accuracy)} accuracy</b></div>
                    <span className={styles.chapterRail}><i style={{ width: `${Math.max(0, Math.min(100, chapter.accuracy))}%` }} /></span>
                  </div>
                ))}
              </div> : <p className={styles.emptyInline}>Chapter-level progress will appear after you complete tests.</p>}
            </section>

            <section className={styles.targets} id="targets">
              <h2>Target your weak areas</h2>
              <p>Use your actual practice history to choose what to work on next.</p>
              <div className={styles.targetGrid}>
                <article className={`${styles.targetCard} ${styles.targetBlue}`}>
                  <Image src="/images/login/Curled Checklist with Sparkling Pen.png" alt="" width={115} height={84} />
                  <h3>Practice weak areas</h3>
                  <p>{dashboard.weakAreas.length ? `${dashboard.weakAreas.length} focus ${dashboard.weakAreas.length === 1 ? "area" : "areas"} found from your tests.` : "Complete tests to identify topics that need practice."}</p>
                  <Link href="/student/mistakes">Review mistakes <ArrowRight size={14} /></Link>
                </article>
                <article className={`${styles.targetCard} ${styles.targetLavender}`}>
                  <Image src="/images/login/Level Two Bar Chart with Golden Arrow.png" alt="" width={115} height={84} />
                  <h3>{insights ? `Level ${insights.level} · ${insights.levelName}` : "Level progress"}</h3>
                  <p>{insights ? insights.nextLevelAt === null ? "You have reached the highest available level." : `${Math.max(0, insights.nextLevelAt - insights.testsCompleted)} tests to your next level.` : data.insightsError ?? "Level progress is unavailable right now."}</p>
                  <Link href="/achievements">View progress <ArrowRight size={14} /></Link>
                </article>
                <article className={`${styles.targetCard} ${styles.targetNavy}`}>
                  <Image src="/images/login/Stacked Books with Floating Question Tiles.png" alt="" width={115} height={84} />
                  <h3>Personalized test</h3>
                  <p>{dashboard.weakAreas.length ? `Build a practice test around your ${dashboard.weakAreas.length} identified focus areas.` : "Create a practice test from your assigned course."}</p>
                  <Link href="/tests/generate">Generate test <ArrowRight size={14} /></Link>
                </article>
                <article className={`${styles.targetCard} ${styles.targetWhite}`}>
                  <Image src="/images/login/Glossy Gradient Badge Trio.png" alt="" width={115} height={84} />
                  <h3>{insights ? `${earnedBadges} badges earned` : "Badge progress"}</h3>
                  <p>{insights ? "See earned badges and the real achievement progress on your account." : data.insightsError ?? "Achievement progress is unavailable right now."}</p>
                  <Link href="/achievements">View badges <ArrowRight size={14} /></Link>
                </article>
              </div>
            </section>

            <section className={styles.analytics} id="performance">
              <article className={`${styles.card} ${styles.trendPanel}`}>
                <div className={styles.panelHeading}><div><h2>Performance trend</h2><p>Your latest completed assessments</p></div><span className={styles.eyebrow}>All tests</span></div>
                {chart.points.length > 1 ? (
                  <div className={styles.chart}>
                    <svg viewBox="0 0 560 165" role="img" aria-label="Your scores across recent completed tests">
                      <defs><linearGradient id="studentTrendFill" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopColor="#663aff" stopOpacity=".22" /><stop offset="1" stopColor="#663aff" stopOpacity=".01" /></linearGradient></defs>
                      {[17, 46, 75, 104, 133].map((y) => <line key={y} x1="41" x2="545" y1={y} y2={y} />)}
                      <path d={chart.area} className={styles.chartArea} fill="url(#studentTrendFill)" />
                      <path d={chart.line} className={styles.chartLine} />
                      {chart.points.map((point, index) => <circle key={`${point.date}-${index}`} cx={point.x} cy={point.y} r="4" />)}
                      {chart.points.map((point, index) => <text key={`label-${point.date}-${index}`} x={point.x} y="154">{point.date}</text>)}
                    </svg>
                  </div>
                ) : <p className={styles.emptyChart}>Complete at least two tests to see your performance trend.</p>}
                <div className={styles.trendSummary}>
                  <span><small>Best score</small><b>{completedTests ? formatPercent(dashboard.statistics.bestScore) : "—"}</b></span>
                  <span><small>Average score</small><b>{completedTests ? formatPercent(dashboard.statistics.averageScore) : "—"}</b></span>
                  <span><small>Accuracy</small><b>{dashboard.statistics.totalAttempted ? formatPercent(dashboard.statistics.accuracy) : "—"}</b></span>
                </div>
              </article>
              <div className={styles.analyticsSide}>
                <article className={`${styles.card} ${styles.scorePanel}`}>
                  <h2>Score distribution</h2>
                  <p>Based on {distribution.reduce((sum, range) => sum + range.count, 0)} completed tests</p>
                  {distribution.some((range) => range.count) ? (
                    <div className={styles.scoreContent}>
                      <div className={styles.donut} style={{ background: `conic-gradient(#ff315e 0 ${distribution[3].percentage}%, #ffa700 ${distribution[3].percentage}% ${distribution[3].percentage + distribution[2].percentage}%, #19bd72 ${distribution[3].percentage + distribution[2].percentage}% ${distribution[3].percentage + distribution[2].percentage + distribution[1].percentage}%, #1c74ff ${distribution[3].percentage + distribution[2].percentage + distribution[1].percentage}% 100%)` }}>
                        <span><b>{distribution.reduce((sum, range) => sum + range.count, 0)}</b><small>Tests</small></span>
                      </div>
                      <div className={styles.scoreLegend}>
                        {[
                          { label: "0% – 49%", range: distribution[3], color: styles.dotRed },
                          { label: "50% – 69%", range: distribution[2], color: styles.dotAmber },
                          { label: "70% – 89%", range: distribution[1], color: styles.dotGreen },
                          { label: "90% – 100%", range: distribution[0], color: styles.dotBlue },
                        ].map((item) => <div key={item.label}><span><i className={item.color} />{item.label}</span><b>{item.range.percentage}%</b></div>)}
                      </div>
                    </div>
                  ) : <p className={styles.emptyInline}>Score ranges will appear after a test is completed.</p>}
                </article>
                <article className={`${styles.card} ${styles.subjectPanel}`}>
                  <h2>Subject performance</h2>
                  {subjects.length ? subjects.slice(0, 5).map((subject) => (
                    <div className={styles.subjectRow} key={subject.subject}>
                      <span>{subject.subject}</span><i><b style={{ width: `${Math.max(0, Math.min(100, subject.score))}%` }} /></i><strong>{formatPercent(subject.score)}</strong>
                    </div>
                  )) : <p className={styles.emptyInline}>Subject scores will appear after you complete tests.</p>}
                </article>
              </div>
            </section>

            <section className={styles.quickStats} aria-label="Learning statistics">
              {[
                { icon: <Check size={19} />, value: completedTests, label: "Tests completed" },
                { icon: <Layers3 size={19} />, value: dashboard.statistics.totalQuestions, label: "Total questions" },
                { icon: <Clock3 size={19} />, value: avgSecondsPerQuestion === null ? "—" : `${avgSecondsPerQuestion}s`, label: "Avg. time per question" },
                { icon: <Target size={19} />, value: dashboard.statistics.totalAttempted ? formatPercent(dashboard.statistics.accuracy) : "—", label: "Accuracy" },
              ].map((item) => <article className={`${styles.card} ${styles.quickCard}`} key={item.label}><span>{item.icon}</span><div><b>{item.value}</b><small>{item.label}</small></div></article>)}
            </section>

            <section className={styles.bottomGrid} id="recent-tests">
              <article className={`${styles.card} ${styles.bottomPanel}`}>
                <div className={styles.panelHeading}><div><h2>Recent tests</h2><p>Your latest completed tests</p></div><Link href="/tests" className={styles.textLink}>View all <ArrowRight size={14} /></Link></div>
                {recentTests.length ? (
                  <div className={styles.tableWrap}><table><thead><tr><th>Test name</th><th>Score</th><th>Accuracy</th><th>Date</th></tr></thead><tbody>
                    {recentTests.slice(0, 5).map((test) => <tr key={test.id}><td title={test.name}>{test.name}</td><td>{formatPercent(test.score)}</td><td>{formatPercent(test.accuracy)}</td><td>{test.date}</td></tr>)}
                  </tbody></table></div>
                ) : <p className={styles.emptyInline}>Completed tests will appear here.</p>}
              </article>
              <article className={`${styles.card} ${styles.bottomPanel}`}>
                <div className={styles.panelHeading}><div><h2>Weak areas</h2><p>Topics to revisit from your own tests</p></div><Link href="/tests/weak-areas" className={styles.textLink}>Practice <ArrowRight size={14} /></Link></div>
                {weakAreas.length ? <ul className={styles.weakList}>{weakAreas.slice(0, 5).map((area) => <li key={area.topic}><span>{area.topic}</span>{area.accuracy == null ? null : <b>{formatPercent(area.accuracy)}</b>}</li>)}</ul> : <p className={styles.emptyInline}>Weak topics will appear as you complete tests.</p>}
              </article>
            </section>
          </div>
          <nav className={styles.mobileNav} aria-label="Student quick navigation">
            <Link href="/dashboard"><CalendarDays size={18} /><span>Home</span></Link>
            <Link href="/tests"><BookOpenCheck size={18} /><span>Tests</span></Link>
            <Link href="/test-summary"><TrendingUp size={18} /><span>Summary</span></Link>
            <Link href="/student/mistakes"><AlertTriangle size={18} /><span>Mistakes</span></Link>
            <Link href="/achievements"><Trophy size={18} /><span>Badges</span></Link>
          </nav>
        </main>
      </div>
    </div>
  );
}
