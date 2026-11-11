"use client";

import { TrendingUp, Trophy, Clock } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Icon } from "@/components/Icon";
import type { DashboardLeaderboard, DashboardPayload, MetricCard } from "@/types/dashboard";

const ICON_MAP: Record<string, React.ComponentType<{ size?: number; className?: string }>> = {
  "test-tube": () => <Icon name="test-tube" size={16} className="text-brand-purple" />,
  analytics: () => <TrendingUp size={16} className="text-brand-purple" />,
  trophy: () => <Trophy size={16} className="text-yellow-400" />,
  clock: () => <Clock size={16} className="text-blue-400" />,
};

export function StatCard({ card }: { card: MetricCard }) {
  const IconComp = ICON_MAP[card.icon ?? "analytics"] ?? ICON_MAP.analytics;
  const trendColor =
    card.trendDirection === "up" ? "text-state-success" : card.trendDirection === "down" ? "text-state-error" : "text-text-body";

  return (
    <Card variant="default" padding="none" radius="large" className="min-h-[104px] border border-border-default p-4 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
      <div className="mb-2 flex items-center justify-between gap-2">
        <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-brand-subtle-lavender/60">
          <IconComp />
        </span>
        <span className="min-w-0 text-right text-[10px] font-extrabold uppercase tracking-wider text-text-supporting-label">{card.label}</span>
      </div>
      <div className="truncate text-2xl font-black leading-none text-text-primary">{card.value}</div>
      {card.trend && <div className={`mt-1 flex items-center gap-1 text-[10px] font-semibold ${trendColor}`}>{card.trend}</div>}
      {card.subtitle && <div className="mt-1.5 text-[10px] leading-4 text-text-body">{card.subtitle}</div>}
    </Card>
  );
}

export function StatsGrid({ cards }: { cards: MetricCard[] }) {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 sm:gap-4 lg:grid-cols-5">
      {cards.map((card) => <StatCard key={card.label} card={card} />)}
    </div>
  );
}

function getWeeklyTestCounts(trend: DashboardPayload["performanceTrend"]) {
  const now = new Date();
  const monday = new Date(now);
  monday.setHours(0, 0, 0, 0);
  monday.setDate(now.getDate() - ((now.getDay() + 6) % 7));
  const counts = Array(7).fill(0) as number[];

  trend.forEach((test) => {
    const date = new Date(test.date);
    if (Number.isNaN(date.getTime()) || date < monday || date > now) return;
    counts[(date.getDay() + 6) % 7] += 1;
  });

  return counts;
}

export function BatchRankingCard({
  batch,
  students,
  currentStudent,
  performanceTrend,
  statistics,
}: {
  batch: DashboardLeaderboard["batch"];
  students: DashboardLeaderboard["students"];
  currentStudent: DashboardLeaderboard["currentStudent"];
  performanceTrend: DashboardPayload["performanceTrend"];
  statistics: DashboardPayload["statistics"];
}) {
  const weekCounts = getWeeklyTestCounts(performanceTrend);
  const maxCount = Math.max(...weekCounts, 1);
  const members = students.slice(0, 3);

  return (
    <Card variant="default" padding="none" radius="large" className="border border-border-default p-4 shadow-sm sm:p-5">
      <div className="mb-3 border-b border-border-default pb-2">
        <h2 className="text-[13px] font-black text-text-primary">Your Batch</h2>
        <p className="mt-0.5 text-[10px] text-text-body">{batch?.name ?? "Batch ranking and activity"}</p>
      </div>
      <div className="flex flex-col gap-5 lg:flex-row lg:items-start">
        <div className="min-w-0 flex-1 space-y-2">
          <div className="flex items-start gap-2.5">
            <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 shadow-md">
              <Trophy size={21} className="text-white" />
            </div>
            <div>
              <div className="text-xs font-bold uppercase tracking-wider text-text-supporting-label">{batch?.name ?? "Your Batch"}</div>
              <div className="text-3xl font-black text-text-primary">{currentStudent ? `#${currentStudent.rank}` : "—"}</div>
              <div className="text-[10px] font-semibold text-brand-purple">
                {currentStudent ? `Rank ${currentStudent.rank} of ${batch?.size ?? students.length}` : "No batch ranking available"}
              </div>
              <div className="mt-1 text-[10px] text-text-body">{batch?.courseName || "Batch performance"}</div>
            </div>
          </div>
        </div>

        <div className="flex flex-col items-center gap-2 lg:w-[220px]">
          <div className="mb-1 text-[9px] font-bold uppercase tracking-wider text-text-supporting-label">Tests this week</div>
          <div className="flex h-20 w-full items-end justify-between gap-1 px-2">
            {weekCounts.map((count, index) => (
              <div key={index} className="flex h-full flex-1 flex-col items-center justify-end gap-1">
                <div
                  className={`w-full rounded-t-md ${count ? "bg-brand-primary" : "bg-brand-primary/20"}`}
                  style={{ height: `${count ? Math.max(12, (count / maxCount) * 100) : 5}%` }}
                  title={`${count} tests`}
                />
                <span className="text-[9px] uppercase text-text-body">{["M", "T", "W", "T", "F", "S", "S"][index]}</span>
              </div>
            ))}
          </div>
          <div className="mt-1 grid w-full grid-cols-3 gap-2">
            <div className="text-center"><div className="text-xs font-black text-text-primary">{statistics.studyTime}</div><div className="text-[9px] text-text-body">Study time</div></div>
            <div className="text-center"><div className="text-xs font-black text-text-primary">{currentStudent?.testsTaken ? `${currentStudent.average.toFixed(1)}%` : "—"}</div><div className="text-[9px] text-text-body">Batch average</div></div>
            <div className="text-center">
              <div className="text-xs font-black text-text-primary">
                {currentStudent?.completionPercent != null ? `${currentStudent.completionPercent.toFixed(0)}%` : "—"}
              </div>
              <div className="text-[9px] text-text-body">Assigned completion</div>
            </div>
          </div>
        </div>

        <div className="min-w-0 flex-1 space-y-2 lg:w-[260px]">
          <div className="mb-2 flex items-center justify-between">
            <div className="text-[9px] font-bold uppercase tracking-wider text-text-supporting-label">Top batch members</div>
            <a href="/student/batch-leaderboard" className="flex items-center gap-1 text-[10px] font-bold text-brand-purple hover:underline transition">View Scoreboard →</a>
          </div>
          {members.length ? (
            <div className="space-y-2">
              {members.map((member) => (
                <div key={member.id} className="flex items-center gap-2.5 p-2 rounded-xl bg-surface-subtle">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center text-white font-bold text-[10px]">
                    {member.name.split(/\s+/).map((part) => part[0]).join("").slice(0, 2)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex justify-between gap-2">
                      <div className="text-xs font-bold text-text-primary truncate">{member.name}</div>
                      <div className="text-[9px] font-bold text-brand-purple">#{member.rank}</div>
                    </div>
                    <div className="text-[10px] text-text-body">{member.average.toFixed(1)}% avg. score</div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-text-body">{batch ? "No batch members to display yet." : "You are not assigned to a batch yet."}</p>
          )}
        </div>
      </div>
    </Card>
  );
}
