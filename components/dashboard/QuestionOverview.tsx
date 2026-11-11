"use client";

import Image from "next/image";
import { AlertTriangle, Bookmark, Clock, CheckCircle2 } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Icon } from "@/components/Icon";
import type { DashboardMistakeStats, DashboardPayload, DonutMetric } from "@/types/dashboard";

const COLOR_MAP: Record<string, { bg: string; text: string; ring: string }> = {
  red: { bg: "bg-red-50", text: "text-red-600", ring: "text-red-600" },
  amber: { bg: "bg-amber-50", text: "text-amber-600", ring: "text-amber-600" },
  green: { bg: "bg-green-50", text: "text-green-600", ring: "text-green-600" },
};

function DonutMetricCard({ metric }: { metric: DonutMetric }) {
  const colors = COLOR_MAP[metric.color];
  const icons = {
    alert: <AlertTriangle size={20} className="text-red-500" />,
    clock: <Clock size={20} className="text-amber-500" />,
    check: <CheckCircle2 size={20} className="text-green-500" />,
  };
  const icon = icons[metric.label === "Unresolved" ? "clock" : metric.label === "Mastered" ? "check" : "alert"];

  return (
    <Card variant="default" padding="none" radius="large" className={`border border-border-default p-4 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md sm:p-5 ${colors.bg}`}>
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full flex items-center justify-center">{icon}</div>
        <div>
          <div className="text-[10px] font-bold uppercase tracking-wider text-text-supporting-label">{metric.label}</div>
          <div className="text-3xl font-black text-text-primary">{metric.value}</div>
        </div>
        <div className="ml-auto">
          <div className="relative w-16 h-16">
            <svg viewBox="0 0 80 80" className="h-full w-full -rotate-90">
              <circle cx="40" cy="40" r="34" stroke="currentColor" strokeWidth="8" fill="none" className="text-border-muted" />
              <circle
                cx="40"
                cy="40"
                r="34"
                stroke="currentColor"
                strokeWidth="8"
                fill="none"
                className={`${colors.ring} transition-all duration-1000`}
                strokeDasharray="213"
                strokeDashoffset={`${213 - (metric.percentage / 100) * 213}`}
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-xs font-black text-text-primary">{metric.percentage}%</span>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
}

function ChapterProgressBar({ chapter }: { chapter: DashboardPayload["chapterPerformance"][number] }) {
  const progress = Math.max(0, Math.min(100, chapter.accuracy));
  const isWeak = progress < 40;
  const isAverage = progress >= 40 && progress < 70;
  const isStrong = progress >= 70;

  const theme = isWeak
    ? { bg: "bg-red-50", border: "border-red-100", ring: "from-red-400 to-red-600", text: "text-red-600", icon: "text-red-500" }
    : isAverage
      ? { bg: "bg-amber-50", border: "border-amber-100", ring: "from-amber-400 to-amber-600", text: "text-amber-600", icon: "text-amber-500" }
      : { bg: "bg-emerald-50", border: "border-emerald-100", ring: "from-emerald-400 to-emerald-600", text: "text-emerald-600", icon: "text-emerald-500" };

  return (
    <Card variant="default" padding="md" radius="card" className={`border ${theme.border} bg-surface-surface p-4 transition-all duration-200 hover:border-brand-primary/50 hover:shadow-md`}>
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0">
          <Bookmark size={18} className={theme.icon} />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex justify-between items-baseline mb-1">
            <div className="text-[10px] font-black uppercase tracking-wider text-text-supporting-label truncate" title={chapter.chapter}>{chapter.chapter}</div>
            <span className={`text-[10px] font-bold ${theme.text}`}>{progress.toFixed(0)}%</span>
          </div>
          <div className="text-[9px] text-text-body truncate">{chapter.subject}</div>
        </div>
      </div>
      <div className="mt-3 h-2 rounded-full bg-surface-subtle overflow-hidden">
        <div className={`h-full rounded-full transition-all duration-1000 bg-gradient-to-r ${theme.ring}`} style={{ width: `${progress}%` }} />
      </div>
    </Card>
  );
}

export function QuestionOverview({
  statistics,
  chapters,
  mistakeStats,
}: {
  statistics: DashboardPayload["statistics"];
  chapters: DashboardPayload["chapterPerformance"];
  mistakeStats: DashboardMistakeStats;
}) {
  const resolved = Math.max(0, mistakeStats.total - mistakeStats.unresolved);
  const total = mistakeStats.total;
  const donutMetrics: DonutMetric[] = [
    { label: "Total Mistakes", value: total, percentage: total ? 100 : 0, color: "red", icon: <AlertTriangle /> },
    { label: "Unresolved", value: mistakeStats.unresolved, percentage: total ? Math.round((mistakeStats.unresolved / total) * 100) : 0, color: "amber", icon: <Clock /> },
    { label: "Mastered", value: resolved, percentage: total ? Math.round((resolved / total) * 100) : 0, color: "green", icon: <CheckCircle2 /> },
  ];
  const weakestChapters = [...chapters].filter((chapter) => chapter.attempted > 0).sort((a, b) => a.accuracy - b.accuracy).slice(0, 5);

  return (
    <section className="w-full space-y-4">
      <div className="relative mb-2 flex items-end justify-between gap-4">
        <div className="flex-1 min-w-0">
          <h2 className="text-xl font-black text-text-primary">Question Overview</h2>
          <p className="text-[11px] text-text-body">
            {statistics.totalAttempted} of {statistics.totalQuestions} questions attempted across your tests.
          </p>
        </div>
        <div className="hidden h-[110px] w-[160px] shrink-0 sm:block">
          <Image
            src="/images/login/Glossy Neon Checklist Scroll.png"
            alt=""
            width={160}
            height={110}
            sizes="160px"
            className="h-full w-full object-contain"
          />
        </div>
        <a href="/stats" className="text-[11px] font-bold text-brand-purple hover:underline flex items-center gap-1">View Detailed Analysis →</a>
      </div>

      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3 sm:gap-4">
        {donutMetrics.map((metric) => <DonutMetricCard key={metric.label} metric={metric} />)}
      </div>

      <div className="border-t border-border-default pt-4">
        <div className="mb-3 flex justify-between items-baseline">
          <div className="flex items-center gap-2">
            <Icon name="bookmark" size={16} className="text-brand-purple" />
            <div>
              <span className="block text-[9px] font-black uppercase tracking-wider text-state-error">Chapter Mastery</span>
              <span className="text-[13px] font-black text-text-primary">Chapters to conquer</span>
            </div>
          </div>
        </div>
        {weakestChapters.length
          ? <div className="grid grid-cols-1 gap-x-6 gap-y-3 md:grid-cols-2">{weakestChapters.map((chapter) => <ChapterProgressBar key={`${chapter.subject}-${chapter.chapter}`} chapter={chapter} />)}</div>
          : <p className="text-sm text-text-body">Chapter performance will appear after you complete tests.</p>}
      </div>
    </section>
  );
}
