"use client";

import { useEffect, useMemo, useState } from "react";
import { LeftSidebar } from "@/components/LeftSidebar";
import { TopNavbar } from "@/components/TopNavbar";
import { HeroCard } from "@/components/dashboard/HeroCard";
import { StatsGrid, BatchRankingCard } from "@/components/dashboard/StatsGrid";
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
      fetchStudentData<{ stats: DashboardMistakeStats }>("/api/student/mistakes?limit=1"),
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

  const metrics = useMemo<MetricCard[]>(() => {
    if (!data) return [];
    const { statistics } = data.dashboard;
    return [
      { label: "Tests Completed", value: statistics.testsTaken, icon: "test-tube", subtitle: "Completed assessments" },
      { label: "Average Score", value: formatPercent(statistics.averageScore), icon: "analytics", subtitle: "Across completed tests" },
      { label: "Best Score", value: formatPercent(statistics.bestScore), icon: "trophy", subtitle: "Highest test score" },
      { label: "Questions Attempted", value: statistics.totalAttempted, icon: "test-tube", subtitle: "Across all completed tests" },
      { label: "Study Time", value: statistics.studyTime, icon: "clock", subtitle: "Total assessment time" },
    ];
  }, [data]);

  const trend: TrendPoint[] = useMemo(
    () =>
      (data?.dashboard.performanceTrend ?? []).slice(-7).map((point) => ({
        date: point.formattedDate || formatDate(point.date),
        score: point.score,
      })),
    [data],
  );

  const distribution: ScoreDistribution[] = useMemo(() => {
    const source = data?.dashboard.scoreDistribution;
    if (!source) return [];
    const ranges = [
      { range: "0% – 49%", count: source.below50, color: "red" },
      { range: "50% – 69%", count: source.between50and69, color: "orange" },
      { range: "70% – 89%", count: source.between70and89, color: "yellow" },
      { range: "90% – 100%", count: source.above90, color: "green" },
    ];
    const total = ranges.reduce((sum, item) => sum + item.count, 0);
    return ranges.map((item) => ({
      ...item,
      percentage: total ? Number(((item.count / total) * 100).toFixed(1)) : 0,
    }));
  }, [data]);

  const subjects: SubjectScore[] = useMemo(
    () =>
      (data?.dashboard.subjectPerformance ?? []).filter((subject) => subject.total > 0).map((subject) => ({
        subject: subject.subject,
        score: subject.score,
        color: subject.score >= 70 ? "green" : "blue",
      })),
    [data],
  );

  const recentTests: RecentTest[] = useMemo(
    () =>
      [...(data?.dashboard.results ?? [])]
        .sort((a, b) => new Date(b.rawDate).getTime() - new Date(a.rawDate).getTime())
        .slice(0, 5)
        .map((test) => ({
          id: test.attemptId,
          name: test.name,
          score: test.score,
          accuracy: test.accuracy,
          date: test.date || formatDate(test.rawDate),
        })),
    [data],
  );

  const weakAreas: WeakArea[] = useMemo(
    () =>
      (data?.dashboard.weakAreas ?? []).map((area) => ({
        topic: `${area.subject}: ${area.chapter}`,
        flagged: area.accuracy < 50,
        accuracy: area.accuracy,
      })),
    [data],
  );

  const studentName = data?.dashboard.student.name || "Student";
  const [nameFirstPart, ...lastNameParts] = studentName.trim().split(/\s+/);
  const firstName = nameFirstPart || "Student";
  const lastName = lastNameParts.join(" ");
  const courseName = data?.dashboard.assignment?.courseName || "No course assigned";
  const currentStudent = data?.leaderboard.currentStudent;

  return (
    <div className={`min-h-screen w-full overflow-x-hidden ${darkMode ? "bg-[#10182B] text-white" : "bg-surface-app-bg text-text-primary"}`}>
      <div className="flex min-h-screen w-full">
        <LeftSidebar
          className="hidden xl:flex"
          student={{ firstName, lastName, courseName, avatarKey: currentStudent?.avatarKey }}
        />
        <main className="flex-1 w-full min-w-0">
          <TopNavbar
            student={{ firstName, lastName, courseName, avatarKey: currentStudent?.avatarKey }}
            darkMode={darkMode}
            onDarkModeChange={setDarkMode}
            unreadNotifications={data?.dashboard.notifications?.filter((notification) => !notification.isRead).length ?? 0}
          />

          <div className="px-5 py-6 lg:px-8 lg:py-8">
            {loading ? (
              <div role="status" className="rounded-2xl bg-surface-surface p-8 text-center text-text-body">
                Loading your dashboard…
              </div>
            ) : error ? (
              <div role="alert" className="rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700">
                {error}
              </div>
            ) : data ? (
              <>
                <HeroCard dashboard={data.dashboard} insights={data.insights} />
                <div className="mt-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
                  <div className="lg:col-span-7">
                    <StatsGrid cards={metrics} />
                  </div>
                  <div className="lg:col-span-5">
                    <BatchRankingCard
                      batch={data.leaderboard.batch}
                      students={data.leaderboard.students}
                      currentStudent={data.leaderboard.currentStudent}
                      performanceTrend={data.dashboard.performanceTrend}
                      statistics={data.dashboard.statistics}
                    />
                  </div>
                </div>
                <div className="mt-6">
                  <TrophyWall badges={data.insights.badges} />
                </div>
                <div className="mt-6">
                  <QuestionOverview
                    statistics={data.dashboard.statistics}
                    chapters={data.dashboard.chapterPerformance}
                    mistakeStats={data.mistakeStats}
                  />
                </div>
                <div className="mt-6">
                  <WeakAreasBanner
                    weakAreas={data.dashboard.weakAreas}
                    levelName={data.insights.levelName}
                    badgesEarned={data.insights.badges.filter((badge) => badge.earned).length}
                  />
                </div>
                <div className="mt-6">
                  <PerformanceTrendsSection
                    trend={trend}
                    distribution={distribution}
                    subjects={subjects}
                    recentTests={recentTests}
                    weakAreas={weakAreas}
                    accuracy={data.dashboard.statistics.accuracy}
                  />
                </div>
              </>
            ) : null}
          </div>
        </main>
      </div>
    </div>
  );
}
