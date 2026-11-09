"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import {
  ArrowRight,
  ArrowUpRight,
  Award,
  BookOpenCheck,
  Brain,
  CalendarDays,
  ChartNoAxesCombined,
  ClipboardList,
  Clock3,
  Flame,
  LockKeyhole,
  Sparkles,
  Target,
  Trophy,
  Zap,
} from "lucide-react";
import StudentAvatar from "@/components/StudentAvatar";
import StudentWorkspace from "./StudentWorkspace";
import { fetchStudentData } from "./student-api";
import type {
  Badge,
  DashboardPayload,
  DashboardResult,
  LeaderboardPayload,
  StudentInsights,
} from "./student-types";

type MistakeStats = { success?: boolean; error?: string; stats?: { total?: number; unresolved?: number } };

function displayNumber(value: number | undefined, suffix = "") {
  return value === undefined || !Number.isFinite(value) ? "—" : `${value.toLocaleString()}${suffix}`;
}

function displayPercent(value: number | undefined) {
  return value === undefined || !Number.isFinite(value) ? "—" : `${value.toFixed(1)}%`;
}

function toDate(value?: string) {
  if (!value) return null;
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? null : parsed;
}

function dateKey(date: Date) {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
}

function relativeWeekDates() {
  const today = new Date();
  const start = new Date(today);
  start.setHours(0, 0, 0, 0);
  start.setDate(today.getDate() - ((today.getDay() + 1) % 7));
  return Array.from({ length: 5 }, (_, index) => {
    const date = new Date(start);
    date.setDate(start.getDate() + index);
    return date;
  });
}

const EMPTY_RESULTS: DashboardResult[] = [];
const EMPTY_BADGES: Badge[] = [];

function BadgeCard({ badge }: { badge: Badge }) {
  return (
    <article className={`dashboard-badge ${badge.earned ? "is-earned" : "is-locked"}`}>
      <div className="dashboard-badge__stack dashboard-badge__stack--back" />
      <div className="dashboard-badge__stack dashboard-badge__stack--middle" />
      <div className="dashboard-badge__face">
        <div className="dashboard-badge__art">
          {badge.asset ? (
            <Image src={badge.asset} alt="" width={63} height={63} unoptimized />
          ) : (
            <span aria-hidden="true">{badge.icon || <Trophy size={30} />}</span>
          )}
          {!badge.earned && <span className="dashboard-badge__lock"><LockKeyhole size={15} /></span>}
        </div>
        <p className="dashboard-badge__category">{badge.category}</p>
        <h3>{badge.name}</h3>
        <p className="dashboard-badge__progress">
          {displayNumber(badge.progress)} / {displayNumber(badge.target)}
        </p>
        <div className="dashboard-badge__meter" role="progressbar" aria-valuenow={badge.progress} aria-valuemax={badge.target}>
          <span style={{ width: `${badge.target > 0 ? Math.min(100, (badge.progress / badge.target) * 100) : 0}%` }} />
        </div>
      </div>
    </article>
  );
}

function LineChart({ results }: { results: DashboardResult[] }) {
  const chartWidth = 720;
  const chartHeight = 210;
  const points = results.map((item, index) => ({
    x: results.length === 1 ? chartWidth / 2 : 40 + (index * (chartWidth - 80)) / (results.length - 1),
    y: chartHeight - 22 - (Math.max(0, Math.min(100, item.score)) / 100) * (chartHeight - 48),
    score: item.score,
    label: item.date,
    id: item.id,
  }));
  const line = points.map((point, index) => `${index ? "L" : "M"}${point.x},${point.y}`).join(" ");

  if (!points.length) {
    return <div className="dashboard-chart-empty">Complete a test to see your performance trend.</div>;
  }

  return (
    <svg className="dashboard-line-chart" viewBox={`0 0 ${chartWidth} ${chartHeight}`} role="img" aria-label="Recent test scores">
      {[0, 25, 50, 75, 100].map((value) => {
        const y = chartHeight - 22 - (value / 100) * (chartHeight - 48);
        return <g key={value}><line x1="40" x2={chartWidth - 16} y1={y} y2={y} /><text x="0" y={y + 4}>{value}%</text></g>;
      })}
      {points.length > 1 && <path className="dashboard-line-chart__area" d={`${line} L${points[points.length - 1].x},${chartHeight - 22} L${points[0].x},${chartHeight - 22} Z`} />}
      {points.length > 1 && <path className="dashboard-line-chart__line" d={line} />}
      {points.map((point) => (
        <g key={point.id}>
          <circle cx={point.x} cy={point.y} r="4" />
          <text className="dashboard-line-chart__score" x={point.x} y={Math.max(14, point.y - 10)} textAnchor="middle">{point.score.toFixed(0)}%</text>
          <text className="dashboard-line-chart__date" x={point.x} y={chartHeight - 4} textAnchor="middle">{point.label}</text>
        </g>
      ))}
    </svg>
  );
}

export default function DashboardHome() {
  const [dashboard, setDashboard] = useState<DashboardPayload | null>(null);
  const [insights, setInsights] = useState<StudentInsights | null>(null);
  const [leaderboard, setLeaderboard] = useState<LeaderboardPayload | null>(null);
  const [mistakeStats, setMistakeStats] = useState<MistakeStats["stats"] | null>(null);
  const [loading, setLoading] = useState(true);
  const [dashboardError, setDashboardError] = useState("");
  const [insightsError, setInsightsError] = useState("");
  const [leaderboardError, setLeaderboardError] = useState("");
  const [mistakesError, setMistakesError] = useState("");
  const [badgeCategory, setBadgeCategory] = useState("All");
  const [trendRange, setTrendRange] = useState("all");
  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now()), 60000);
    let active = true;
    fetchStudentData<DashboardPayload>("/api/dashboard")
      .then((data) => { if (active) setDashboard(data); })
      .catch((error: unknown) => { if (active) setDashboardError(error instanceof Error ? error.message : "Could not load your dashboard."); })
      .finally(() => { if (active) setLoading(false); });
    fetchStudentData<StudentInsights>("/api/student/insights")
      .then((data) => { if (active) setInsights(data); })
      .catch((error: unknown) => { if (active) setInsightsError(error instanceof Error ? error.message : "Could not load achievements and streak data."); });
    fetchStudentData<LeaderboardPayload>("/api/student/batch-leaderboard")
      .then((data) => { if (active) setLeaderboard(data); })
      .catch((error: unknown) => { if (active) setLeaderboardError(error instanceof Error ? error.message : "Could not load your batch."); });
    fetchStudentData<MistakeStats>("/api/student/mistakes?limit=1")
      .then((data) => { if (active) setMistakeStats(data.stats ?? null); })
      .catch((error: unknown) => { if (active) setMistakesError(error instanceof Error ? error.message : "Could not load mistake counts."); });
    return () => {
      active = false;
      window.clearInterval(timer);
    };
  }, []);

  const results = dashboard?.results ?? EMPTY_RESULTS;
  const statistics = dashboard?.statistics;
  const badges = insights?.badges ?? EMPTY_BADGES;
  const categories = useMemo(() => ["All", ...new Set(badges.map((badge) => badge.category))], [badges]);
  const visibleBadges = badges.filter((badge) => badgeCategory === "All" || badge.category === badgeCategory);
  const performanceTrend = dashboard?.performanceTrend;
  const trendResults = (() => {
    const source = performanceTrend?.length
      ? performanceTrend.map((item) => ({
          id: item.attemptId,
          name: item.label || "Test",
          score: item.score,
          accuracy: item.score,
          date: item.formattedDate || item.date || "",
        }))
      : results;
    const cutoff = trendRange === "all" ? null : now - Number(trendRange) * 86400000;
    return source.filter((item) => {
      if (!cutoff) return true;
      const date = toDate(item.date);
      return date ? date.getTime() >= cutoff : false;
    });
  })();
  const [weekDates] = useState(relativeWeekDates);
  const weekResults = useMemo(() => {
    const today = new Date(now);
    today.setHours(23, 59, 59, 999);
    const start = weekDates[0];
    return results.filter((result) => {
      const date = toDate(result.date);
      return date && date >= start && date <= today;
    });
  }, [now, results, weekDates]);
  const activityDays = new Set(insights?.activityDays ?? []);
  const todayStart = new Date(now);
  todayStart.setHours(0, 0, 0, 0);
  const missedPastDay = weekDates.some((date) => date < todayStart && !activityDays.has(dateKey(date)));
  const streakMode = (insights?.streak ?? 0) >= 60 ? "supercharged" : missedPastDay ? "frozen" : "active";
  const topThree = (leaderboard?.students ?? []).filter((student) => student.rank <= 3).sort((a, b) => a.rank - b.rank);
  const currentStudent = leaderboard?.currentStudent;
  const scoreGroups = useMemo(() => {
    const groups = [
      { label: "90% and above", color: "#31b982", count: 0 },
      { label: "70%–89%", color: "#5386ed", count: 0 },
      { label: "50%–69%", color: "#f3b441", count: 0 },
      { label: "Below 50%", color: "#ed6c71", count: 0 },
    ];
    results.forEach((result) => {
      if (result.score >= 90) groups[0].count += 1;
      else if (result.score >= 70) groups[1].count += 1;
      else if (result.score >= 50) groups[2].count += 1;
      else groups[3].count += 1;
    });
    return groups;
  }, [results]);
  const scoreTotal = scoreGroups.reduce((total, group) => total + group.count, 0);
  const ringGradient = useMemo(() => {
    let offset = 0;
    const parts = scoreGroups.map((group) => {
      const from = offset;
      offset += scoreTotal ? (group.count / scoreTotal) * 100 : 0;
      return `${group.color} ${from}% ${offset}%`;
    });
    return `conic-gradient(${parts.join(", ")})`;
  }, [scoreGroups, scoreTotal]);
  const levelRemaining = insights?.nextLevelAt == null
    ? null
    : Math.max(0, insights.nextLevelAt - (insights.testsCompleted ?? 0));
  const weeklyBars = weekDates.map((date) => ({
    date,
    count: weekResults.filter((item) => dateKey(toDate(item.date) ?? new Date(0)) === dateKey(date)).length,
  }));
  const maxWeeklyTests = Math.max(...weeklyBars.map((day) => day.count), 1);
  const studentName = dashboard?.student?.name ?? "";
  const courseName = dashboard?.assignment?.courseName ?? "";
  const unreadCount = dashboard?.notifications?.filter((item) => !item.isRead).length ?? 0;

  if (loading) {
    return (
      <StudentWorkspace active="dashboard" studentName={studentName} courseName={courseName} unreadCount={unreadCount}>
        <div className="dashboard-loading" aria-live="polite">Loading your dashboard…</div>
      </StudentWorkspace>
    );
  }

  if (dashboardError) {
    return (
      <StudentWorkspace active="dashboard" studentName={studentName} courseName={courseName} unreadCount={unreadCount}>
        <div className="dashboard-error" role="alert">
          <h2>Unable to load your dashboard</h2>
          <p>{dashboardError}</p>
          <button type="button" onClick={() => window.location.reload()}>Try again</button>
        </div>
      </StudentWorkspace>
    );
  }

  return (
    <StudentWorkspace active="dashboard" studentName={studentName} courseName={courseName} unreadCount={unreadCount}>
      <div className="dashboard-page">
        <section className="dashboard-hero">
          <div className="dashboard-hero__player">
            <div className="dashboard-hero__eyebrow"><Zap size={14} /> YOUR PLAYER PROGRESS</div>
            <div className="dashboard-hero__level">
              <span className="dashboard-hero__level-number">{insights ? `Level ${insights.level}` : "—"}</span>
              <div><h2>{insights?.levelName ?? "Progress"}</h2><p>Keep learning. Keep leveling up.</p></div>
              <div className="dashboard-hero__avatar"><StudentAvatar name={studentName} size={56} /></div>
            </div>
            <div className="dashboard-level-progress">
              <div className="dashboard-level-progress__labels"><span>Next level</span><span>{levelRemaining == null ? "—" : `${levelRemaining} tests to go`}</span></div>
              <div className="dashboard-level-progress__track"><span style={{ width: `${insights?.levelProgress ?? 0}%` }} /></div>
            </div>
            <div className="dashboard-hero__stats">
              <div><Sparkles size={16} /><strong>{displayNumber(insights?.points)}</strong><span>XP</span></div>
              <div><Award size={16} /><strong>{displayNumber(badges.filter((badge) => badge.earned).length)}</strong><span>Badges</span></div>
              <div><ChartNoAxesCombined size={16} /><strong>{displayPercent(statistics?.averageScore)}</strong><span>Average</span></div>
            </div>
          </div>
          <div className={`dashboard-hero__streak dashboard-hero__streak--${streakMode}`}>
            <div className="dashboard-streak-heading"><div><p>DAY STREAK</p><h2>{displayNumber(insights?.streak)} <span>days</span></h2></div>
              <div className="dashboard-streak-flame" aria-label={`${streakMode} streak`}>
                {streakMode === "frozen" ? <span className="dashboard-frozen-flame"><Flame size={31} /><span>×</span></span> : <Flame size={34} fill="currentColor" />}
              </div>
            </div>
            <p className="dashboard-streak-caption">
              {streakMode === "supercharged" ? "Your streak is supercharged!" : streakMode === "frozen" ? "A missed study day. Start a fresh streak today." : "One test a day keeps your streak alive."}
            </p>
            <div className="dashboard-streak-days">
              {weekDates.map((date) => {
                const activeDay = activityDays.has(dateKey(date));
                const passed = date < new Date();
                return (
                  <div className={`dashboard-streak-day ${activeDay ? "is-active" : ""} ${passed && !activeDay ? "is-missed" : ""}`} key={dateKey(date)}>
                    <span>{date.toLocaleDateString("en-US", { weekday: "short" })}</span>
                    <i aria-label={activeDay ? "Activity recorded" : passed ? "No activity recorded" : "Upcoming day"}>
                      {activeDay ? <Flame size={14} fill="currentColor" /> : passed ? "×" : ""}
                    </i>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        <section className="dashboard-metrics" aria-label="Performance metrics">
          {[
            { label: "Tests Taken", value: displayNumber(statistics?.testsTaken), icon: ClipboardList, detail: "Completed tests" },
            { label: "Average Score", value: displayPercent(statistics?.averageScore), icon: ChartNoAxesCombined, detail: "Across completed tests" },
            { label: "Best Score", value: displayPercent(statistics?.bestScore), icon: Trophy, detail: "Personal best" },
            { label: "Attempts", value: displayNumber(statistics?.totalAttempts ?? statistics?.attempts), icon: Target, detail: "All test attempts" },
            { label: "Assessment Time", value: statistics?.studyTime || "—", icon: Clock3, detail: "Time spent learning" },
          ].map(({ label, value, icon: Icon, detail }) => (
            <article className="dashboard-metric" key={label}>
              <div className="dashboard-metric__top"><span>{label}</span><Icon size={17} /></div>
              <strong>{value}</strong><p>{detail}</p>
            </article>
          ))}
        </section>

        <section className="dashboard-batch">
          <div className="dashboard-batch__rank">
            <div className="dashboard-section-kicker">YOUR BATCH</div>
            <div className="dashboard-batch__rank-medal"><Trophy size={24} /></div>
            <strong>{currentStudent ? `#${currentStudent.rank}` : "—"}</strong>
            <span>{currentStudent ? "Batch rank" : leaderboard?.batch ? "Take a test to rank" : "No batch assigned"}</span>
            {currentStudent && <div className="dashboard-batch__trend"><ArrowUpRight size={14} /> {displayPercent(currentStudent.average)} average</div>}
            {leaderboardError && <p className="dashboard-inline-error" role="alert">{leaderboardError}</p>}
          </div>
          <div className="dashboard-batch__week">
            <div className="dashboard-card-heading"><div><h2>Tests this week</h2><p>Recent activity in your batch</p></div><CalendarDays size={18} /></div>
            <div className="dashboard-week-chart">
              {weeklyBars.map(({ date, count }) => (
                <div className="dashboard-week-column" key={dateKey(date)}>
                  <span>{count || ""}</span><i style={{ height: `${Math.max(count ? 15 : 4, (count / maxWeeklyTests) * 72)}px` }} />
                  <small>{date.toLocaleDateString("en-US", { weekday: "short" })}</small>
                </div>
              ))}
            </div>
            <div className="dashboard-week-summary">
              <span><b>{weekResults.length}</b> tests</span>
              <span><b>{statistics?.studyTime || "—"}</b> study time</span>
              <span><b>{displayNumber(weekResults.reduce((total, item) => total + (item.attempted ?? 0), 0))}</b> questions attempted</span>
            </div>
          </div>
          <div className="dashboard-batch__leaders">
            <div className="dashboard-card-heading"><div><h2>Top performers</h2><p>{leaderboard?.batch?.name ?? "Your batch"}</p></div></div>
            {topThree.length ? topThree.map((student) => (
              <div className="dashboard-mini-leader" key={student.id}>
                <span className="dashboard-mini-leader__rank">#{student.rank}</span>
                <StudentAvatar avatarKey={student.avatarKey} name={student.name} size={32} />
                <span className="dashboard-mini-leader__name">{student.name}</span>
                <strong>{displayPercent(student.average)}</strong>
              </div>
            )) : <p className="dashboard-empty-inline">{leaderboardError || "Your batch scores will appear here."}</p>}
            <Link href="/student/batch-leaderboard" className="dashboard-text-link">View scoreboard <ArrowRight size={14} /></Link>
          </div>
        </section>

        <section className="dashboard-section">
          <div className="dashboard-section-heading">
            <div><p className="dashboard-section-kicker">YOUR ACHIEVEMENTS</p><h2>Trophy wall</h2><p>Every milestone is another step forward.</p></div>
            <Link href="/achievements" className="dashboard-text-link">View all badges <ArrowRight size={14} /></Link>
          </div>
          {insightsError ? <p className="dashboard-inline-error" role="alert">{insightsError}</p> : (
            <>
              <div className="dashboard-badge-filters" role="tablist" aria-label="Achievement categories">
                {categories.map((category) => <button key={category} type="button" role="tab" aria-selected={badgeCategory === category} className={badgeCategory === category ? "is-selected" : ""} onClick={() => setBadgeCategory(category)}>{category}</button>)}
              </div>
              {visibleBadges.length ? <div className="dashboard-badge-grid">{visibleBadges.slice(0, 8).map((badge) => <BadgeCard key={badge.id} badge={badge} />)}</div> : <p className="dashboard-empty-inline">Your achievements will appear here as you complete tests.</p>}
            </>
          )}
        </section>

        <section className="dashboard-insights-grid">
          <article className="dashboard-card dashboard-mistakes-card">
            <div className="dashboard-card-heading"><div><p className="dashboard-section-kicker">QUESTION OVERVIEW</p><h2>Mistake notebook</h2></div><Link href="/student/mistakes" className="dashboard-card-icon"><BookOpenCheck size={17} /></Link></div>
            {mistakesError ? <p className="dashboard-inline-error" role="alert">{mistakesError}</p> : (
              <div className="dashboard-mistake-content">
                <div className="dashboard-mistake-donut" style={{ background: mistakeStats?.total ? `conic-gradient(#ef6a71 0% ${(mistakeStats.unresolved ?? 0) / mistakeStats.total * 100}%, #f1a34b ${(mistakeStats.unresolved ?? 0) / mistakeStats.total * 100}% ${(mistakeStats.unresolved ?? 0) / mistakeStats.total * 100 + ((mistakeStats.total - (mistakeStats.unresolved ?? 0)) / mistakeStats.total * 100)}%, #37b981 0)` : "conic-gradient(#e8edf5 0% 100%)" }}>
                  <div><strong>{mistakeStats ? displayNumber(mistakeStats.total) : "—"}</strong><span>Total mistakes</span></div>
                </div>
                <div className="dashboard-mistake-legend">
                  {[
                    { label: "Total mistakes", value: mistakeStats?.total, color: "#ef6a71" },
                    { label: "Unresolved", value: mistakeStats?.unresolved, color: "#f1a34b" },
                    { label: "Mastered", value: mistakeStats ? Math.max(0, (mistakeStats.total ?? 0) - (mistakeStats.unresolved ?? 0)) : undefined, color: "#37b981" },
                  ].map((item) => <div key={item.label}><i style={{ background: item.color }} /><span>{item.label}</span><strong>{displayNumber(item.value)}</strong></div>)}
                </div>
              </div>
            )}
            <Link href="/student/mistakes" className="dashboard-card-footer">Open mistake notebook <ArrowRight size={14} /></Link>
          </article>

          <article className="dashboard-card dashboard-chapters-card">
            <div className="dashboard-card-heading"><div><p className="dashboard-section-kicker">CHAPTER MASTERY</p><h2>Chapters to conquer</h2></div><Target size={18} /></div>
            {(insights?.weakAreas ?? []).length ? (
              <div className="dashboard-chapter-list">
                {(insights?.weakAreas ?? []).slice(0, 4).map((area) => {
                  const mastery = Math.max(0, Math.min(100, 100 - (area.rate ?? 0)));
                  return <div className="dashboard-chapter" key={`${area.subject}-${area.chapter}`}><div><span>{area.chapter}</span><b>{mastery.toFixed(0)}%</b></div><small>{area.subject}</small><div className="dashboard-chapter__bar"><i style={{ width: `${mastery}%` }} /></div></div>;
                })}
              </div>
            ) : <p className="dashboard-empty-inline">{insightsError || "Chapter insights will appear after you complete tests."}</p>}
            <Link href="/tests/generate" className="dashboard-card-footer">Practice weak areas <ArrowRight size={14} /></Link>
          </article>
        </section>

        <section className="dashboard-action-grid">
          {[
            { title: "Best practice", subtitle: "Build a focused practice routine", action: "Practise now", href: "/tests/generate", icon: BookOpenCheck, tone: "blue" },
            { title: `Level ${insights?.level ?? "—"} · ${insights?.levelName ?? "Your progress"}`, subtitle: levelRemaining == null ? "Keep building your skills" : `${levelRemaining} tests to the next level`, action: "View progress", href: "/achievements", icon: Zap, tone: "purple" },
            { title: "AI generated test", subtitle: "Create a test for your focus areas", action: "Generate test", href: "/tests/generate", icon: Brain, tone: "mint" },
            { title: `${badges.filter((badge) => badge.earned).length} badges unlocked`, subtitle: "Celebrate your achievements", action: "View badges", href: "/achievements", icon: Award, tone: "gold" },
          ].map(({ title, subtitle, action, href, icon: Icon, tone }) => (
            <Link href={href} key={action} className={`dashboard-action-card dashboard-action-card--${tone}`}><span className="dashboard-action-card__icon"><Icon size={21} /></span><strong>{title}</strong><p>{subtitle}</p><span className="dashboard-action-card__link">{action} <ArrowRight size={14} /></span></Link>
          ))}
        </section>

        <section className="dashboard-performance-grid">
          <article className="dashboard-card dashboard-performance-card">
            <div className="dashboard-card-heading"><div><p className="dashboard-section-kicker">PERFORMANCE TRENDS</p><h2>Your progress over time</h2></div>
              <select aria-label="Performance date range" value={trendRange} onChange={(event) => setTrendRange(event.target.value)}><option value="all">All time</option><option value="30">Last 30 days</option><option value="7">Last 7 days</option></select>
            </div>
            <LineChart results={trendResults} />
          </article>
          <article className="dashboard-card dashboard-score-card">
            <div className="dashboard-card-heading"><div><p className="dashboard-section-kicker">SCORE DISTRIBUTION</p><h2>Score breakdown</h2></div></div>
            <div className="dashboard-score-content">
              <div className="dashboard-score-donut" style={{ background: ringGradient }}><div><strong>{scoreTotal}</strong><span>tests</span></div></div>
              <div className="dashboard-score-legend">
                {scoreGroups.map((group) => <div key={group.label}><i style={{ background: group.color }} /><span>{group.label}</span><b>{group.count ? `${Math.round((group.count / (scoreTotal || 1)) * 100)}%` : "—"}</b></div>)}
              </div>
            </div>
          </article>
        </section>

        <section className="dashboard-data-grid">
          <article className="dashboard-card dashboard-subject-card">
            <div className="dashboard-card-heading"><div><p className="dashboard-section-kicker">SUBJECT DISTRIBUTION</p><h2>Subject performance</h2></div></div>
            {dashboard?.subjectPerformance?.length ? <div className="dashboard-subject-list">{dashboard.subjectPerformance.map((subject) => <div key={subject.subject}><div><span>{subject.subject}</span><b>{displayPercent(subject.score)}</b></div><div className="dashboard-subject-bar"><i style={{ width: `${Math.max(0, Math.min(100, subject.score))}%` }} /></div><small>{displayNumber(subject.attempted)} questions attempted</small></div>)}</div> : <p className="dashboard-empty-inline">Subject results will appear when tests are completed.</p>}
          </article>
          <article className="dashboard-card dashboard-recent-card">
            <div className="dashboard-card-heading"><div><p className="dashboard-section-kicker">RECENT ACTIVITY</p><h2>Recent tests</h2></div><Link href="/tests" className="dashboard-text-link">View all <ArrowRight size={14} /></Link></div>
            {results.length ? <div className="dashboard-table-wrap"><table className="dashboard-table"><thead><tr><th>Test name</th><th>Score</th><th>Accuracy</th><th>Date</th></tr></thead><tbody>{results.slice(0, 5).map((test) => <tr key={test.id}><td><span className="dashboard-test-name"><ClipboardList size={15} />{test.name}</span></td><td><strong>{displayPercent(test.score)}</strong></td><td>{displayPercent(test.accuracy)}</td><td>{test.date || "—"}</td></tr>)}</tbody></table></div> : <p className="dashboard-empty-inline">Your completed tests will appear here.</p>}
          </article>
        </section>

        <section className="dashboard-card dashboard-weak-topics">
          <div className="dashboard-card-heading"><div><p className="dashboard-section-kicker">FOCUS NEXT</p><h2>Weak areas</h2></div><Link href="/tests/generate" className="dashboard-text-link">Practice now <ArrowRight size={14} /></Link></div>
          {(insights?.weakAreas ?? []).length ? <ul>{(insights?.weakAreas ?? []).map((area) => <li key={`${area.subject}-${area.chapter}`}><span>{area.subject}</span><b>{area.chapter}</b><small>{area.rate?.toFixed(0)}% missed</small></li>)}</ul> : <p className="dashboard-empty-inline">{insightsError || "Your focus topics will appear here after you complete tests."}</p>}
        </section>
      </div>
    </StudentWorkspace>
  );
}
