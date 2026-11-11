"use client";

import Image from "next/image";
import { ArrowRight, Trophy, TrendingUp, Info, Zap } from "lucide-react";
import Link from "next/link";
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
      <div className="relative w-full overflow-hidden rounded-[20px] border border-indigo-800/40 bg-gradient-to-br from-indigo-900 via-indigo-950 to-[#111942] p-4 text-white shadow-lg sm:p-5">
        <div className="pointer-events-none absolute -right-10 -top-20 h-56 w-56 rounded-full bg-purple-500/20 blur-[90px]" />
        <div className="relative z-10 grid gap-5 lg:grid-cols-[minmax(0,1.65fr)_minmax(230px,.8fr)] lg:items-center">
          <div className="min-w-0 space-y-3">
            <div className="flex justify-between items-start">
              <div>
                <div className="mb-1 text-[9px] font-bold uppercase tracking-[.16em] text-indigo-300">Player progress</div>
                <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
                  <span className="text-4xl font-black tracking-tight sm:text-[42px]">Level {insights.level}</span>
                  <span className="text-lg font-extrabold tracking-tight text-indigo-100 sm:text-xl">{insights.levelName}</span>
                </div>
              </div>
              <Image
                src="/images/login/Level Two Bar Chart with Golden Arrow.png"
                alt=""
                width={92}
                height={76}
                sizes="92px"
                className="mr-2 h-[68px] w-[82px] shrink-0 object-contain sm:h-[76px] sm:w-[92px]"
              />
              <Link href="/achievements" className="hidden items-center gap-1 rounded-full bg-indigo-800/60 px-3 py-1.5 text-[9px] font-bold text-indigo-100 transition hover:bg-indigo-700/80 sm:flex">
                Tap to view level <ArrowRight size={12} />
              </Link>
            </div>

            <div className="space-y-1.5">
              <div className="flex justify-between gap-3 text-[9px] font-bold uppercase tracking-wider text-indigo-300">
                <span>Level progress</span>
                <span>{testsRemaining ? `${testsRemaining} more tests to go` : "Max level reached"}</span>
              </div>
              <div className="h-2 w-full overflow-hidden rounded-full border border-white/10 bg-indigo-600/30">
                <div
                  className="h-full bg-gradient-to-r from-indigo-400 to-purple-400 transition-all duration-1000 ease-out"
                  style={{ width: `${insights.levelProgress}%` }}
                />
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-x-5 gap-y-2 border-t border-white/10 pt-3">
              <div className="flex items-center gap-2">
                <div className="flex h-7 w-7 items-center justify-center rounded-full bg-indigo-500/20 text-indigo-300"><Zap size={15} /></div>
                <div><div className="text-[11px] font-bold text-white">{insights.points} XP</div><div className="text-[9px] text-indigo-300/70">Experience points</div></div>
              </div>
              <div className="flex items-center gap-2">
                <div className="flex h-7 w-7 items-center justify-center rounded-full bg-yellow-400/20 text-yellow-300"><Trophy size={15} /></div>
                <div><div className="text-[11px] font-bold text-white">{earnedBadges} Badges</div><div className="text-[9px] text-indigo-300/70">Badges earned</div></div>
              </div>
              <div className="flex items-center gap-2">
                <div className="flex h-7 w-7 items-center justify-center rounded-full bg-green-400/20 text-green-300"><TrendingUp size={15} /></div>
                <div><div className="text-[11px] font-bold text-white">{dashboard.statistics.testsTaken ? `${dashboard.statistics.averageScore.toFixed(1)}%` : "—"} avg.</div><div className="text-[9px] text-indigo-300/70">Average score</div></div>
              </div>
              <div className="ml-auto hidden rounded-full bg-indigo-600/20 p-1.5 text-indigo-300 sm:block" title={`${insights.testsCompleted} completed tests`}>
                <Info size={16} />
              </div>
            </div>
          </div>

          <div className="min-w-0 space-y-2.5 border-t border-white/10 pt-3 lg:border-l lg:border-t-0 lg:pl-5 lg:pt-0">
            <div className="relative mx-auto mb-2 h-[112px] w-full max-w-[190px]">
              <Image
                src="/images/login/Glossy Purple Trophy with Stars.png"
                alt=""
                fill
                sizes="(max-width: 1024px) 190px, 190px"
                className="object-contain"
              />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <div className="mb-0.5 flex items-center gap-1 text-[9px] font-bold uppercase tracking-[.16em] text-indigo-300">
                  <Image
                    src="/images/login/Glowing Flame Streak Icon.png"
                    alt=""
                    width={20}
                    height={20}
                    sizes="20px"
                    className="h-5 w-5 object-contain"
                  />
                  Day streak
                </div>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-black tracking-tight">{insights.streak}</span>
                  <span className="text-[10px] font-bold text-white">Streak days</span>
                </div>
              </div>
              <Image
                src={
                  insights.streak
                    ? "/images/login/Vibrant Gradient Flame with Sparkles.png"
                    : "/images/login/Glowing Blue Layered Flame.png"
                }
                alt=""
                width={60}
                height={60}
                sizes="60px"
                className="h-[60px] w-[60px] object-contain"
              />
            </div>

            <div className="grid grid-cols-7 gap-1.5">
              {days.map((day) => (
                <div
                  key={day.dateKey}
                  className={`flex flex-col items-center gap-1 rounded-lg p-1 ${
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
