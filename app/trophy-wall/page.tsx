"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Lock, CheckCircle2, Trophy } from "lucide-react";

type Badge = {
  name: string;
  icon: string;
  tier: number;
  category: string;
};

const BADGES: Badge[] = [
  { name: "Crushing It I", icon: "🔥", tier: 1, category: "score" },
  { name: "Crushing It II", icon: "🔥", tier: 2, category: "score" },
  { name: "Crushing It III", icon: "🔥", tier: 3, category: "score" },
  { name: "Crushing It IV", icon: "🔥", tier: 4, category: "score" },
  { name: "Beast Mode I", icon: "🐉", tier: 1, category: "streak" },
  { name: "Beast Mode II", icon: "🐉", tier: 2, category: "streak" },
  { name: "Beast Mode III", icon: "🐉", tier: 3, category: "streak" },
  { name: "Beast Mode IV", icon: "🐉", tier: 4, category: "streak" },
  { name: "Flawless I", icon: "💎", tier: 1, category: "mastery" },
  { name: "Flawless II", icon: "💎", tier: 2, category: "mastery" },
  { name: "Flawless III", icon: "💎", tier: 3, category: "mastery" },
  { name: "Flawless IV", icon: "💎", tier: 4, category: "mastery" },
  { name: "Glow Up I", icon: "✨", tier: 1, category: "improvement" },
  { name: "Glow Up II", icon: "✨", tier: 2, category: "improvement" },
  { name: "Glow Up III", icon: "✨", tier: 3, category: "improvement" },
  { name: "Glow Up IV", icon: "✨", tier: 4, category: "improvement" },
  { name: "7-Day Streak", icon: "🔥", tier: 1, category: "streak" },
  { name: "30-Day Streak", icon: "🔥", tier: 2, category: "streak" },
  { name: "100-Day Streak", icon: "🔥", tier: 3, category: "streak" },
  { name: "200-Day Streak", icon: "🔥", tier: 4, category: "streak" },
  { name: "365-Day Streak", icon: "🔥", tier: 5, category: "streak" },
  { name: "1K Club", icon: "💰", tier: 1, category: "volume" },
  { name: "5K Club", icon: "💰", tier: 2, category: "volume" },
  { name: "10K Club", icon: "💰", tier: 3, category: "volume" },
  { name: "Boss Level Cleared I", icon: "👑", tier: 1, category: "comeback" },
  { name: "Boss Level Cleared II", icon: "👑", tier: 2, category: "comeback" },
  { name: "Boss Level Cleared III", icon: "👑", tier: 3, category: "comeback" },
  { name: "Boss Level Cleared IV", icon: "👑", tier: 4, category: "comeback" },
  { name: "Immortal", icon: "🧟", tier: 5, category: "ultimate" },
  { name: "Podium I", icon: "🥇", tier: 1, category: "rank" },
  { name: "Podium II", icon: "🥈", tier: 2, category: "rank" },
  { name: "Podium III", icon: "🥉", tier: 3, category: "rank" },
  { name: "Podium IV", icon: "🏆", tier: 4, category: "rank" },
  { name: "MVP I", icon: "🌟", tier: 1, category: "rank" },
  { name: "MVP II", icon: "🌟", tier: 2, category: "rank" },
  { name: "MVP III", icon: "🌟", tier: 3, category: "rank" },
  { name: "MVP IV", icon: "🌟", tier: 4, category: "rank" },
  { name: "Completionist", icon: "🎯", tier: 5, category: "ultimate" },
];

export default function TrophyWallPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [unlockedBadges, setUnlockedBadges] = useState<Set<string>>(new Set());

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
      setUnlockedBadges(new Set(["Crushing It I", "Crushing It II", "7-Day Streak"]));
    }, 600);
    return () => clearTimeout(timer);
  }, []);

  const unlockedCount = unlockedBadges.size;

  return (
    <main className="min-h-screen bg-surface-app-bg text-text-primary">
      <div className="mx-auto max-w-5xl px-6 py-10">
        <div className="mb-8">
          <button
            onClick={() => router.push("/dashboard")}
            className="text-sm font-semibold text-brand-primary mb-2 inline-block transition hover:underline"
          >
            ← Back to Dashboard
          </button>
          <h1 className="text-2xl font-extrabold tracking-tight">
            Achievement Vault
          </h1>
          <p className="text-sm text-text-tertiary">
            View all your earned badges and trophies in one place.
          </p>
        </div>

        {loading ? (
          <div className="h-64 flex items-center justify-center">
            <div className="w-8 h-8 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin" />
          </div>
        ) : (
          <div className="rounded-2xl border border-border-default bg-white p-8 shadow-sm">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-extrabold text-text-primary">
                Trophy Wall
              </h2>
              <p className="text-sm text-text-tertiary">
                Collect achievements as you master chapters and ace tests.
              </p>
            </div>

            {/* Card Stack — locked cards grayed out, unlocked cards reveal */}
            <div className="relative h-[calc(100vh-260px)] flex items-center justify-center pb-20">
              {BADGES.map((badge, index) => {
                const isUnlocked = unlockedBadges.has(badge.name);
                const zIndex = BADGES.length - index;
                const stackOffset = index * 14;
                const translateY = `calc(${stackOffset}px * -1)`;

                return (
                  <div
                    key={badge.name}
                    className="absolute left-0 right-0 mx-auto w-full max-w-md transition-all duration-700 ease-out"
                    style={{
                      zIndex,
                      transform: `translateY(${translateY})`,
                      opacity: isUnlocked ? 1 : 0.45,
                      filter: isUnlocked ? "none" : "grayscale(100%)",
                      pointerEvents: isUnlocked ? "auto" : "none",
                    }}
                  >
                    <div
                      className={`rounded-2xl border p-5 shadow-lg flex flex-col items-center gap-3 text-center ${
                        isUnlocked
                          ? "bg-white border-brand-primary shadow-xl"
                          : "bg-surface-muted border-border-default"
                      }`}
                    >
                      {!isUnlocked && (
                        <div className="absolute inset-0 rounded-2xl bg-black/20 flex items-center justify-center pointer-events-none">
                          <Lock className="w-12 h-12 text-gray-500" />
                        </div>
                      )}
                      <div className="relative z-10 w-16 h-16 rounded-2xl flex items-center justify-center text-4xl mb-1">
                        {badge.icon}
                      </div>
                      <h3 className={`text-sm font-bold ${
                        isUnlocked ? "text-text-primary" : "text-text-tertiary"
                      }`}>
                        {badge.name}
                      </h3>
                      <p className={`text-[10px] uppercase tracking-wider font-semibold ${
                        isUnlocked ? "text-brand-primary" : "text-text-body"
                      }`}>
                        Tier {badge.tier} · {badge.category}
                      </p>
                      {isUnlocked && (
                        <CheckCircle2 className="w-4 h-4 text-state-success" />
                      )}
                    </div>
                  </div>
                );
              })}
              <div className="h-40" />
            </div>

            <div className="mt-8 text-center">
              <p className="text-xs text-text-supporting-label">
                Locked cards are grayed out. Complete milestones to unlock them.
              </p>
            </div>

          </div>
        )}
      </div>
    </main>
  );
}