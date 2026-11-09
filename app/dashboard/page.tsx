"use client";

import { useEffect, useMemo, useState } from "react";
import { LeftSidebar } from "@/components/LeftSidebar";
import { TopNavbar } from "@/components/TopNavbar";
import { HeroCard } from "@/components/dashboard/HeroCard";
import { StatsGrid } from "@/components/dashboard/StatsGrid";
import { BatchRankingCard } from "@/components/dashboard/StatsGrid";
import { TrophyWall } from "@/components/dashboard/TrophyWall";
import { QuestionOverview } from "@/components/dashboard/QuestionOverview";
import { WeakAreasBanner } from "@/components/dashboard/WeakAreasBanner";
import { PerformanceTrendsSection } from "@/components/dashboard/PerformanceTrends";
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

type DashboardData = {
  dashboard: DashboardPayload;
  insights: DashboardInsights;
  leaderboard: DashboardLeaderboard;
  mistakeStats: DashboardMistakeStats;
};

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

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    let active = true;

    Promise.all([
      fetchStudentData<DashboardPayload>("/api/dashboard"),
      fetchStudentData<DashboardInsights>("/api/student/insights"),
      fetchStudentData<DashboardLeaderboard>("/api/student/batch-leaderboard"),
      fetchStudentData<{ stats: DashboardMistakeStats }>(
        "/api/student/mistakes?limit=1"
      ),
    ])
      .then(([dashboard, insights, leaderboard, mistakes]) => {
        if (active) {
          setData({
            dashboard,
            insights,
            leaderboard,
            mistakeStats: mistakes.stats,
          });
        }
      })
      .catch((cause: unknown) => {
        if (active) {
          setError(cause instanceof Error ? cause.message : "Could not load your dashboard.");
        }
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    document.body.classList.toggle("student-dashboard-dark", darkMode);
    return () => document.body.classList.remove("student-dashboard-dark");
  }, [darkMode]);

  // All hooks must run unconditionally every render. Guard inside for null data.
  const dashboard = data?.dashboard;
  const insights = data?.insights;
  const leaderboard = data?.leaderboard;
  const mistakeStats = data?.mistakeStats;

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
      <div className="min-h-screen w-full bg-surface-app-bg text-text-primary flex items-center justify-center">
        <div className="text-text-body">Loading your dashboard…</div>
      </div>
    );
  }

  if (error) {
    return (
      <div role="alert" className="rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700 max-w-md mx-auto mt-10">
        {error}
        <button
          type="button"
          onClick={() => window.location.reload()}
          className="mt-3 text-xs underline text-brand-purple"
        >
          Try again
        </button>
      </div>
    );
  }

  if (!dashboard) return null;

  // dashboard existing implies data (and thus insights/leaderboard/mistakeStats) exists
  const nonNullInsights = insights!;
  const nonNullLeaderboard = leaderboard!;
  const nonNullMistakeStats = mistakeStats!;
  const currentStudent = nonNullLeaderboard.currentStudent ?? null;

  return (
    <div className={`min-h-screen w-full overflow-x-hidden ${darkMode ? "bg-[#10182B] text-white" : "bg-surface-app-bg text-text-primary"}`}>
      <div className="flex min-h-screen w-full">
        <LeftSidebar
          className="hidden xl:flex"
          student={{
            firstName,
            lastName,
            courseName,
            avatarKey: currentStudent?.avatarKey,
          }}
        />
        <main className="flex-1 w-full min-w-0">
          <TopNavbar
            student={{
              firstName,
              lastName,
              courseName,
              avatarKey: currentStudent?.avatarKey,
            }}
            darkMode={darkMode}
            onDarkModeChange={setDarkMode}
            unreadNotifications={
              dashboard.notifications?.filter((notification) => !notification.isRead).length ?? 0
            }
          />

          <div className="mx-auto max-w-[1500px] px-3 py-4 sm:px-5 lg:px-7 lg:py-5">
            {/* Player progress + day streak hero */}
            <div className="mb-3">
              <HeroCard dashboard={dashboard} insights={nonNullInsights} />
            </div>

            {/* Student-specific performance metrics */}
            <div className="mb-3">
              <StatsGrid cards={metrics} />
            </div>

            {/* Batch: rank + tests this week + top batch members */}
            <div className="mb-3">
              <BatchRankingCard
                batch={nonNullLeaderboard.batch}
                students={nonNullLeaderboard.students}
                currentStudent={currentStudent}
                performanceTrend={dashboard.performanceTrend}
                statistics={dashboard.statistics}
              />
            </div>

            {/* Trophy Wall — compact card stacks grouped by badge category */}
            <div className="mb-3">
              <TrophyWall badges={nonNullInsights.badges} />
            </div>

            {/* Question overview + chapter mastery */}
            <div className="mb-3">
              <QuestionOverview
                statistics={dashboard.statistics}
                chapters={dashboard.chapterPerformance}
                mistakeStats={nonNullMistakeStats}
              />
            </div>

            {/* Target your weak areas */}
            <div className="mb-3">
              <WeakAreasBanner
                weakAreas={dashboard.weakAreas}
                levelName={nonNullInsights.levelName}
                badgesEarned={nonNullInsights.badges.filter((badge) => badge.earned).length}
                darkMode={darkMode}
              />
            </div>

            {/* Performance trends, score distribution, subjects, recent tests, weak areas */}
            <div className="mb-6">
              <PerformanceTrendsSection
                trend={trend}
                distribution={distribution}
                subjects={subjects}
                recentTests={recentTests}
                weakAreas={weakAreas}
                accuracy={dashboard.statistics.accuracy}
              />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
