"use client";

import { ArrowRight, Flame, Trophy, TrendingUp, Info, Zap } from "lucide-react";
import type { DashboardInsights, DashboardPayload } from "@/types/dashboard";

const INDIA_DATE_FORMATTER = new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Kolkata" });

function getWeekActivity(activityDays: string[]) {
  const todayKey = INDIA_DATE_FORMATTER.format(new Date());
  const today = new Date(`${todayKey}T12:00:00+05:30`);
  const saturdayOffset = (today.getUTCDay() + 1) % 7;
  today.setUTCDate(today.getUTCDate() - saturdayOffset);

  return Array.from({ length: 7 }, (_, index) => {
    const date = new Date(today);
    date.setUTCDate(today.getUTCDate() + index);
    const dateKey = INDIA_DATE_FORMATTER.format(date);
    return {
      dateKey,
      day: new Intl.DateTimeFormat("en", { timeZone: "Asia/Kolkata", weekday: "short" }).format(date),
      active: activityDays.includes(dateKey),
      isToday: dateKey === todayKey,
      isFuture: dateKey > todayKey,
    };
  });
}

export function HeroCard({
  dashboard,
  insights,
}: {
  dashboard: DashboardPayload;
  insights: DashboardInsights;
}) {
  const testsRemaining = insights.nextLevelAt === null
    ? 0
    : Math.max(0, insights.nextLevelAt - insights.testsCompleted);
  const earnedBadges = insights.badges.filter((badge) => badge.earned).length;
  const days = getWeekActivity(insights.activityDays);

  return (
    <section className="w-full">
      <div className="relative w-full rounded-[24px] border border-transparent bg-gradient-to-br from-indigo-900 via-indigo-950 to-navy-900 p-6 text-white overflow-hidden shadow-xl">
        <div className="absolute top-0 right-0 -mb-6 -mr-6 w-64 h-64 bg-purple-500/20 rounded-full blur-[120px] pointer-events-none" />
        <div className="relative z-10 flex flex-col lg:flex-row lg:items-start gap-6">
          <div className="flex-1 space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <div className="text-[11px] uppercase tracking-widest text-indigo-300 font-semibold mb-1">PLAYER PROGRESS</div>
                <div className="flex flex-wrap items-baseline gap-2">
                  <span className="text-5xl font-black tracking-tight">Level {insights.level}</span>
                  <span className="text-3xl font-black tracking-tight">{insights.levelName}</span>
                </div>
              </div>
              <a href="/achievements" className="flex items-center gap-1.5 rounded-lg bg-indigo-800/50 px-3 py-1.5 text-[10px] font-bold text-indigo-200 hover:bg-indigo-800/80 transition">
                <ArrowRight size={14} className="text-indigo-300" />
                <span>VIEW ACHIEVEMENTS</span>
              </a>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-[10px] font-bold text-indigo-300 uppercase tracking-wider">
                <span>LEVEL PROGRESS</span>
                <span>{testsRemaining ? `${testsRemaining} more tests to go` : "Max level reached"}</span>
              </div>
              <div className="w-full h-3 rounded-full bg-indigo-600/30 overflow-hidden border border-white/10">
                <div
                  className="h-full bg-gradient-to-r from-indigo-400 to-purple-400 transition-all duration-1000 ease-out"
                  style={{ width: `${insights.levelProgress}%` }}
                />
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-5 border-t border-white/10 pt-4">
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 rounded-full bg-indigo-500/20 flex items-center justify-center text-indigo-300"><Zap size={16} /></div>
                <div><div className="text-xs font-bold text-white">{insights.points} XP</div><div className="text-[10px] text-indigo-300/70">Experience points</div></div>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 rounded-full bg-yellow-400/20 flex items-center justify-center text-yellow-300"><Trophy size={16} /></div>
                <div><div className="text-xs font-bold text-white">{earnedBadges} Badges</div><div className="text-[10px] text-indigo-300/70">Badges earned</div></div>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 rounded-full bg-green-400/20 flex items-center justify-center text-green-300"><TrendingUp size={16} /></div>
                <div><div className="text-xs font-bold text-white">{dashboard.statistics.testsTaken ? `${dashboard.statistics.averageScore.toFixed(1)}%` : "—"} avg.</div><div className="text-[10px] text-indigo-300/70">Average score</div></div>
              </div>
              <div className="ml-auto p-1.5 rounded-full bg-indigo-600/20 text-indigo-300" title={`${insights.testsCompleted} completed tests`}>
                <Info size={16} />
              </div>
            </div>
          </div>

          <div className="flex-1 lg:w-[300px] space-y-4">
            <div>
              <div className="text-[11px] uppercase tracking-widest text-indigo-300 font-semibold mb-1">DAY STREAK</div>
              <div className="flex items-baseline gap-2">
                <span className="text-4xl font-black tracking-tight">{insights.streak}</span>
                <span className="text-xs font-bold text-white">Streak Days</span>
              </div>
            </div>

            <div className="relative h-36 rounded-2xl overflow-hidden border border-white/10 bg-gradient-to-br from-indigo-800 to-navy-900">
              <div className="absolute inset-0 flex items-center justify-center">
                <Flame size={60} className={insights.streak ? "text-orange-400" : "text-indigo-400"} />
                {Boolean(insights.streak) && <div className="absolute inset-0 bg-orange-500/20 rounded-full blur-xl animate-pulse" />}
              </div>
            </div>

            <div className="grid grid-cols-7 gap-1.5">
              {days.map((day) => (
                <div
                  key={day.dateKey}
                  className={`flex flex-col items-center gap-1 p-1.5 rounded-lg ${
                    day.active
                      ? "bg-green-500/10 border border-green-500/30"
                      : day.isFuture
                        ? "bg-white/5 border border-white/10"
                        : "bg-blue-500/10 border border-blue-500/30"
                  } ${day.isToday ? "ring-2 ring-white ring-inset" : ""}`}
                >
                  <span className={`text-[10px] uppercase font-bold ${day.active ? "text-green-400" : day.isFuture ? "text-white/40" : "text-blue-400"}`}>
                    {day.active ? "✓" : day.isFuture ? "○" : "✕"}
                  </span>
                  <span className="text-[9px] font-medium text-white/70">{day.day}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
