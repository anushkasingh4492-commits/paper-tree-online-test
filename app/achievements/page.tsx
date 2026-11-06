"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type Achievement = {
  id: string;
  name: string;
  description: string;
  icon: string;
  tier: number;
  earned: boolean;
  earnedAt?: string;
  category: string;
};

export default function AchievementsPage() {
  const router = useRouter();
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch("/api/student/achievements", { cache: "no-store" });
        const data = await res.json();
        if (data.success) setAchievements(data.achievements || []);
      } catch {
        // silent
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const earnedCount = achievements.filter((a) => a.earned).length;

  return (
    <main className="min-h-screen bg-surface-app-bg text-text-primary">
      <div className="mx-auto max-w-4xl px-6 py-10">
        <div className="flex items-center justify-between mb-8">
          <div>
            <button
              onClick={() => router.push("/dashboard")}
              className="text-sm font-semibold text-brand-primary mb-2 inline-block transition hover:underline"
            >
              ← Back to Dashboard
            </button>
            <h1 className="text-2xl font-extrabold tracking-tight">
              My Achievements
            </h1>
            <p className="text-sm text-text-tertiary">
              Unlock badges and track your progress milestones.
            </p>
          </div>
          <div className="rounded-xl border border-border-default bg-white px-4 py-2 text-sm">
            <span className="font-bold text-text-primary">{earnedCount}</span>{" "}
            <span className="text-text-tertiary">of {achievements.length} unlocked</span>
          </div>
        </div>

        {loading ? (
          <div className="h-64 flex items-center justify-center">
            <div className="w-8 h-8 border-4 border-brand-primary/20 border-t-brand-primary rounded-full animate-spin" />
          </div>
        ) : (
          <div className="space-y-4">
            {achievements.map((a) => (
              <div
                key={a.id}
                className={`rounded-xl border p-4 flex items-center gap-4 ${
                  a.earned ? "border-brand-primary bg-surface-subtle" : "border-border-default bg-white"
                }`}
              >
                <div className="w-12 h-12 rounded-2xl flex items-center justify-center shrink-0">
                  <span className={`text-[20px] ${a.earned ? "" : "grayscale"}`}>
                    {a.icon}
                  </span>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="font-bold text-sm text-text-primary truncate">
                      {a.name}
                    </h3>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        a.tier === 1
                          ? "text-state-warning bg-state-warning/10"
                          : a.tier === 2
                            ? "text-silver-600 bg-silver-50"
                            : a.tier === 3
                              ? "text-bronze-600 bg-bronze-50"
                              : "text-brand-primary bg-surface-subtle"
                      }`}
                    >
                      Tier {a.tier}
                    </span>
                    {!a.earned && (
                      <span className="text-[10px] font-bold text-text-body">
                        Locked
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-text-tertiary leading-relaxed">
                    {a.description}
                  </p>
                  <div className="mt-2 flex items-center gap-2">
                    <span className="text-[10px] font-semibold text-text-body">
                      {a.category}
                    </span>
                    {a.earned && a.earnedAt && (
                      <span className="text-[10px] text-text-body">
                        • Earned {new Date(a.earnedAt).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                </div>
                {!a.earned ? (
                  <div className="w-8 h-8 rounded-full bg-border-default flex items-center justify-center text-[10px] text-text-body">
                    🔒
                  </div>
                ) : (
                  <div className="w-8 h-8 rounded-full bg-state-success flex items-center justify-center text-white text-[10px]">
                    ✓
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
