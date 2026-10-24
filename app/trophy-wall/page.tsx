"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function TrophyWallPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => setLoading(false), 500);
  }, []);

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <div className="mx-auto max-w-5xl px-6 py-10">
        <div className="mb-8">
          <button
            onClick={() => router.push("/dashboard")}
            className="text-sm font-semibold text-[#315bea] mb-2 inline-block transition hover:underline"
          >
            ← Back to Dashboard
          </button>
          <h1 className="text-2xl font-extrabold tracking-tight">
            Achievement Vault
          </h1>
          <p className="text-sm text-[#697386]">
            View all your earned badges and trophies in one place.
          </p>
        </div>

        {loading ? (
          <div className="h-64 flex items-center justify-center">
            <div className="w-8 h-8 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin" />
          </div>
        ) : (
          <div className="rounded-2xl border border-[#e5e8ef] bg-white p-8 shadow-sm">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-extrabold text-[#172033]">
                Trophy Wall
              </h2>
              <p className="text-sm text-[#697386]">
                Collect achievements as you master chapters and ace tests.
              </p>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
              {[
                { name: "Crushing It I", icon: "🔥", tier: 1 },
                { name: "Crushing It II", icon: "🔥", tier: 2 },
                { name: "Crushing It III", icon: "🔥", tier: 3 },
                { name: "Crushing It IV", icon: "🔥", tier: 4 },
                { name: "Beast Mode I", icon: "🐉", tier: 1 },
                { name: "Beast Mode II", icon: "🐉", tier: 2 },
                { name: "Beast Mode III", icon: "🐉", tier: 3 },
                { name: "Beast Mode IV", icon: "🐉", tier: 4 },
                { name: "Flawless I", icon: "💎", tier: 1 },
                { name: "Flawless II", icon: "💎", tier: 2 },
                { name: "Flawless III", icon: "💎", tier: 3 },
                { name: "Flawless IV", icon: "💎", tier: 4 },
                { name: "Glow Up I", icon: "✨", tier: 1 },
                { name: "Glow Up II", icon: "✨", tier: 2 },
                { name: "Glow Up III", icon: "✨", tier: 3 },
                { name: "Glow Up IV", icon: "✨", tier: 4 },
              ].map((badge) => (
                <div
                  key={badge.name}
                  className="rounded-xl border border-[#e5e8ef] bg-white p-4 flex flex-col items-center gap-2 text-center"
                >
                  <div className="w-14 h-14 rounded-2xl bg-[#f0f5ff] flex items-center justify-center text-3xl mb-1">
                    {badge.icon}
                  </div>
                  <h3 className="text-sm font-bold text-[#172033]">
                    {badge.name}
                  </h3>
                  <p className="text-[10px] text-[#8a93a5]">Tier {badge.tier}</p>
                </div>
              ))}
            </div>

            <div className="mt-8 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
              {[
                { name: "7-Day Streak", icon: "🔥", tier: 1 },
                { name: "30-Day Streak", icon: "🔥", tier: 2 },
                { name: "100-Day Streak", icon: "🔥", tier: 3 },
                { name: "200-Day Streak", icon: "🔥", tier: 4 },
                { name: "365-Day Streak", icon: "🔥", tier: 5 },
                { name: "1K Club", icon: "💰", tier: 1 },
                { name: "5K Club", icon: "💰", tier: 2 },
                { name: "10K Club", icon: "💰", tier: 3 },
              ].map((badge) => (
                <div
                  key={badge.name}
                  className="rounded-xl border border-[#e5e8ef] bg-white p-4 flex flex-col items-center gap-2 text-center"
                >
                  <div className="w-14 h-14 rounded-2xl bg-[#f0f5ff] flex items-center justify-center text-3xl mb-1">
                    {badge.icon}
                  </div>
                  <h3 className="text-sm font-bold text-[#172033]">
                    {badge.name}
                  </h3>
                  <p className="text-[10px] text-[#8a93a5]">Tier {badge.tier}</p>
                </div>
              ))}
            </div>

            <div className="mt-8 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
              {[
                { name: "Boss Level Cleared I", icon: "👑", tier: 1 },
                { name: "Boss Level Cleared II", icon: "👑", tier: 2 },
                { name: "Boss Level Cleared III", icon: "👑", tier: 3 },
                { name: "Boss Level Cleared IV", icon: "👑", tier: 4 },
                { name: "Immortal", icon: "🧟", tier: 5 },
                { name: "Podium I", icon: "🥇", tier: 1 },
                { name: "Podium II", icon: "🥈", tier: 2 },
                { name: "Podium III", icon: "🥉", tier: 3 },
              ].map((badge) => (
                <div
                  key={badge.name}
                  className="rounded-xl border border-[#e5e8ef] bg-white p-4 flex flex-col items-center gap-2 text-center"
                >
                  <div className="w-14 h-14 rounded-2xl bg-[#f0f5ff] flex items-center justify-center text-3xl mb-1">
                    {badge.icon}
                  </div>
                  <h3 className="text-sm font-bold text-[#172033]">
                    {badge.name}
                  </h3>
                  <p className="text-[10px] text-[#8a93a5]">Tier {badge.tier}</p>
                </div>
              ))}
            </div>

            <div className="mt-8 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
              {[
                { name: "Podium IV", icon: "🏆", tier: 4 },
                { name: "MVP I", icon: "🌟", tier: 1 },
                { name: "MVP II", icon: "🌟", tier: 2 },
                { name: "MVP III", icon: "🌟", tier: 3 },
                { name: "MVP IV", icon: "🌟", tier: 4 },
                { name: "Completionist", icon: "🎯", tier: 5 },
              ].map((badge) => (
                <div
                  key={badge.name}
                  className="rounded-xl border border-[#e5e8ef] bg-white p-4 flex flex-col items-center gap-2 text-center"
                >
                  <div className="w-14 h-14 rounded-2xl bg-[#f0f5ff] flex items-center justify-center text-3xl mb-1">
                    {badge.icon}
                  </div>
                  <h3 className="text-sm font-bold text-[#172033]">
                    {badge.name}
                  </h3>
                  <p className="text-[10px] text-[#8a93a5]">Tier {badge.tier}</p>
                </div>
              ))}
            </div>

          </div>
        )}
      </div>
    </main>
  );
}