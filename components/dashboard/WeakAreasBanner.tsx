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
      padding="md"
      radius="hero"
      className={`
        relative overflow-hidden group border border-white/20
        ${card.color}
        text-white
        hover:scale-[1.02] transition-all duration-300 shadow-lg
      `}
    >
      {/* Decorative glow */}
      <div className="absolute top-0 right-0 -mb-4 -mr-4 w-48 h-48 bg-white/10 rounded-full blur-[100px] pointer-events-none group-hover:blur-[120px] transition-blur duration-500" />

      <div className="relative z-10 flex flex-col items-start gap-2">
        <div className="flex items-center justify-between w-full">
          <div className="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center backdrop-blur-sm">
            {ACTION_ICONS[card.icon] ?? ACTION_ICONS.book}
          </div>
        </div>

        <h3 className="text-lg font-black leading-tight">{card.title}</h3>
        <p className="text-sm text-white/80 leading-relaxed">{card.subtitle}</p>

        <a
          href={card.href}
          className="mt-4 w-full flex items-center justify-center gap-2 rounded-xl bg-white/20 backdrop-blur-md px-4 py-2.5 text-xs font-black text-white hover:bg-white/30 transition-all border border-white/10"
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
}: {
  weakAreas: DashboardPayload["weakAreas"];
  levelName: string;
  badgesEarned: number;
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
      <div className="relative rounded-[24px] border border-transparent bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-6 overflow-hidden">
        {/* Decorative stars */}
        <div className="absolute top-1/4 left-1/4 w-3 h-3 rounded-full bg-yellow-400/50" />
        <div className="absolute top-1/6 right-1/5 w-2 h-2 rounded-full bg-purple-400/50" />
        <div className="absolute bottom-1/3 left-1/5 w-4 h-4 rounded-full bg-blue-400/30" />

        <div className="relative z-10">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h2 className="text-[18px] font-black text-text-primary">Target your weak areas</h2>
              <p className="text-[11px] text-text-body">
                Check your level, power up badges, or build an AI-generated test from your weak areas.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {actionCards.map((card) => (
              <ActionCard key={card.id} card={card} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}