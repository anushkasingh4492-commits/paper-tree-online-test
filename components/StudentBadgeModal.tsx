"use client";

import { useEffect, useState } from "react";

type Badge = {
  id: string;
  name: string;
  icon?: string;
  asset?: string | null;
  category: string;
  tier: number;
  detail: string;
  subject?: string | null;
};

type Props = {
  studentId: string;
  studentName: string;
  onClose: () => void;
};

const TIER_NAMES = ["", "I", "II", "III", "IV"];

export default function StudentBadgeModal({ studentId, studentName, onClose }: Props) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [data, setData] = useState<{ level: number; levelName: string; streak: number; testsCompleted: number; badges: Badge[] } | null>(null);

  useEffect(() => {
    let active = true;
    fetch(`/api/gamification/student/${encodeURIComponent(studentId)}`, { cache: "no-store", credentials: "include" })
      .then(async (response) => {
        const value = await response.json();
        if (!response.ok || !value.success) throw new Error(value.error || "Could not load badges.");
        if (active) setData(value);
      })
      .catch((reason) => {
        if (active) setError(reason instanceof Error ? reason.message : "Could not load badges.");
      })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [studentId]);

  return (
    <div className="fixed inset-0 z-[70] flex items-center justify-center bg-slate-950/70 p-4 backdrop-blur-sm" onClick={onClose}>
      <section className="w-full max-w-3xl max-h-[85vh] overflow-hidden rounded-[28px] border border-white/10 bg-slate-950 text-white shadow-2xl" onClick={(event) => event.stopPropagation()}>
        <div className="flex items-center justify-between border-b border-white/10 px-6 py-5">
          <div>
            <p className="text-[10px] font-black uppercase tracking-[.2em] text-indigo-300">Achievements</p>
            <h2 className="mt-1 text-2xl font-black">{studentName}</h2>
            {data && <p className="mt-1 text-xs text-white/45">Level {data.level} · {data.levelName} · 🔥 {data.streak} day streak · {data.testsCompleted} tests</p>}
          </div>
          <button type="button" onClick={onClose} className="rounded-xl bg-white/10 px-3 py-2 text-sm font-bold text-white/70 hover:bg-white/15">Close</button>
        </div>

        <div className="max-h-[68vh] overflow-y-auto p-6">
          {loading ? <div className="py-16 text-center text-sm text-white/45">Loading achievements...</div> : error ? <div className="rounded-2xl border border-red-400/20 bg-red-500/10 p-5 text-sm text-red-200">{error}</div> : data && data.badges.length === 0 ? <div className="py-16 text-center"><div className="text-5xl">🏆</div><p className="mt-4 font-bold">No badges earned yet.</p><p className="mt-1 text-sm text-white/40">Keep completing tests to unlock achievements.</p></div> : (
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4">
              {data?.badges.map((badge) => (
                <article key={badge.id} className="rounded-2xl border border-white/10 bg-white/[.05] p-4 text-center transition hover:-translate-y-1 hover:bg-white/[.08]">
                  <div className="mx-auto flex h-24 w-24 items-center justify-center rounded-2xl bg-white/[.06]">
                    {badge.asset ? <img src={badge.asset} alt={badge.name} className="h-20 w-20 object-contain" /> : <span className="text-4xl">{badge.icon || "🏆"}</span>}
                  </div>
                  <h3 className="mt-3 text-sm font-black">{badge.name}{badge.tier ? ` ${TIER_NAMES[badge.tier]}` : ""}</h3>
                  <p className="mt-1 text-[10px] font-bold uppercase tracking-wider text-indigo-300">{badge.category}</p>
                  <p className="mt-2 text-[11px] leading-4 text-white/45">{badge.detail}</p>
                </article>
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
