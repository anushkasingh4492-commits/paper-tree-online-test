"use client";

import { Book, Trophy, Sparkles, Star } from "lucide-react";
import { Card } from "@/components/ui/Card";
import type { DashboardPayload } from "@/types/dashboard";

const ACTION_ICONS: Record<string, React.ReactNode> = {
  book: <Book size={32} className="text-white/90" />,
  trophy: <Trophy size={32} className="text-white/90" />,
  sparkles: <Sparkles size={32} className="text-white/90" />,
  star: <Star size={32} className="text-white/90" />,
};

type DashboardAction = {
  id: string;
  title: string;
  subtitle: string;
  cta: string;
  icon: string;
  color: string;
  href: string;
};

export function ActionCard({ card }: { card: DashboardAction }) {
  return (
    <Card
      variant="default"
      padding="none"
      radius="large"
      className={`
        group relative min-h-[150px] overflow-hidden border border-white/20 p-3
        ${card.color}
        text-white
        shadow-md transition-all duration-300 hover:-translate-y-0.5 hover:shadow-lg
      `}
    >
      {/* Decorative glow */}
      <div className="absolute top-0 right-0 -mb-4 -mr-4 w-48 h-48 bg-white/10 rounded-full blur-[100px] pointer-events-none group-hover:blur-[120px] transition-blur duration-500" />

      <div className="relative z-10 flex h-full flex-col items-start gap-1.5">
        <div className="flex items-center justify-between w-full">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-white/20 backdrop-blur-sm">
            {ACTION_ICONS[card.icon] ?? ACTION_ICONS.book}
          </div>
        </div>

        <h3 className="text-[12px] font-black leading-tight">{card.title}</h3>
        <p className="line-clamp-2 text-[9px] leading-relaxed text-white/80">{card.subtitle}</p>

        <a
          href={card.href}
          className="mt-auto flex w-full items-center justify-center gap-2 rounded-lg border border-white/10 bg-white/20 px-3 py-2 text-[9px] font-black text-white backdrop-blur-md transition-all hover:bg-white/30"
        >
          {card.cta}
          <span className="text-xs">→</span>
        </a>
      </div>
    </Card>
  );
}

export function WeakAreasBanner({
  weakAreas,
  levelName,
  badgesEarned,
  darkMode,
}: {
  weakAreas: DashboardPayload["weakAreas"];
  levelName: string;
  badgesEarned: number;
  darkMode: boolean;
}) {
  const topicSummary = weakAreas.slice(0, 3).map((area) => `${area.subject}: ${area.chapter}`).join(", ");
  const actionCards: DashboardAction[] = [
    {
      id: "practice",
      title: "Practice weak areas",
      subtitle: weakAreas.length
        ? `${weakAreas.length} focus ${weakAreas.length === 1 ? "area" : "areas"}: ${topicSummary}`
        : "Complete a test to identify topics that need more practice.",
      cta: "Review Mistakes",
      icon: "book",
      color: "bg-gradient-to-br from-indigo-600 to-blue-700",
      href: "/student/mistakes",
    },
    {
      id: "level",
      title: `Level: ${levelName}`,
      subtitle: "Your level progress updates as you complete tests.",
      cta: "View Progress",
      icon: "trophy",
      color: "bg-gradient-to-br from-purple-500 to-fuchsia-600",
      href: "/achievements",
    },
    {
      id: "test",
      title: "Personalized test",
      subtitle: weakAreas.length
        ? `Build a practice test around ${weakAreas.length} identified focus ${weakAreas.length === 1 ? "area" : "areas"}.`
        : "Generate a practice test based on your course.",
      cta: "Generate Test",
      icon: "sparkles",
      color: "bg-gradient-to-br from-violet-600 to-indigo-700",
      href: "/tests/generate",
    },
    {
      id: "badges",
      title: `${badgesEarned} Badges Earned`,
      subtitle: "See your earned badges and the achievements you can unlock next.",
      cta: "View Badges",
      icon: "star",
      color: "bg-gradient-to-br from-yellow-400 to-orange-500",
      href: "/achievements",
    },
  ];

  return (
    <section className="w-full">
      <div className={`relative overflow-hidden rounded-2xl border p-4 ${
        darkMode
          ? "border-[#303B5C] bg-[#1C2942]"
          : "border-transparent bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50"
      }`}>
        {/* Decorative stars */}
        {!darkMode && (
          <>
            <div className="absolute top-1/4 left-1/4 w-3 h-3 rounded-full bg-yellow-400/50" />
            <div className="absolute top-1/6 right-1/5 w-2 h-2 rounded-full bg-purple-400/50" />
            <div className="absolute bottom-1/3 left-1/5 w-4 h-4 rounded-full bg-blue-400/30" />
          </>
        )}

        <div className="relative z-10">
          <div className="mb-3 flex items-start justify-between">
            <div>
              <h2 className={`text-[15px] font-black ${darkMode ? "text-white" : "text-text-primary"}`}>Target your weak areas</h2>
              <p className={`text-[11px] ${darkMode ? "text-slate-300" : "text-text-body"}`}>
                Check your level, power up badges, or build an AI-generated test from your weak areas.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 xl:grid-cols-4">
            {actionCards.map((card) => (
              <ActionCard key={card.id} card={card} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}