"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";


type Insights = {
  level: number;
  levelName: string;
  points: number;
  testsCompleted: number;
  badges: Array<{ id: string; earned: boolean }>;
};

export default function StudentTestHub() {
  const router = useRouter();
  const [data, setData] = useState<Insights | null>(null);
  const [revisionLoading, setRevisionLoading] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("/api/student/insights", {
      cache: "no-store",
      credentials: "include",
    })
      .then((response) => response.json())
      .then((value) => {
        if (value?.success) setData(value);
      })
      .catch(() => undefined);
  }, []);

  async function createRevisionTest() {
    setRevisionLoading(true);
    setMessage("");
    try {
      const response = await fetch("/api/student/revision-test", {
        method: "POST",
        credentials: "include",
      });
      const value = await response.json();
      if (!response.ok || !value.success) {
        throw new Error(value.error || "Could not create AI test.");
      }
      router.push(`/test/${value.testId}`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Could not create AI test.");
    } finally {
      setRevisionLoading(false);
    }
  }

  const earnedBadges = data?.badges?.filter((badge) => badge.earned).length ?? 0;
  const totalBadges = data?.badges?.length ?? 0;

  return (
    <section className="relative overflow-hidden rounded-[20px] border border-indigo-100 bg-gradient-to-br from-white via-indigo-50/80 to-cyan-50 px-4 py-4 shadow-[0_8px_24px_rgba(83,65,220,.08)] sm:px-5 sm:py-5">
      <div className="pointer-events-none absolute -right-20 -top-24 h-48 w-48 rounded-full bg-indigo-200/40 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-24 left-1/3 h-40 w-40 rounded-full bg-cyan-200/30 blur-3xl" />

      <div className="relative">
        <div>
          <div className="text-[10px] font-black uppercase tracking-[.22em] text-indigo-600">Test</div>
          <h2 className="mt-1 text-xl font-black tracking-tight text-slate-950 sm:text-2xl">
            Target your weak areas
          </h2>
          <p className="mt-1 max-w-2xl text-xs font-semibold text-slate-500 sm:text-sm">
            Check your level, open your badges, or build an AI-generated test from your weakest areas.
          </p>
        </div>

        <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
          <button
            type="button"
            onClick={() => router.push("/tests")}
            className="group min-h-[112px] rounded-2xl bg-indigo-600 p-4 text-left text-white shadow-sm transition hover:-translate-y-0.5 hover:bg-indigo-700 hover:shadow-md"
          >
            <div className="flex items-center justify-between">
              <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/15 text-lg">📝</span>
              <span className="text-[10px] font-black uppercase tracking-wider text-indigo-100">Practice</span>
            </div>
            <div className="mt-3 text-sm font-black">Self Practice</div>
            <div className="mt-1 text-[11px] font-semibold text-indigo-100">
              Choose your exam, subjects and chapters, then start a test.
            </div>
          </button>

          <button
            type="button"
            onClick={() => document.getElementById("student-level")?.scrollIntoView({ behavior: "smooth", block: "start" })}
            className="group min-h-[112px] rounded-2xl border border-indigo-100 bg-white p-4 text-left shadow-sm transition hover:-translate-y-0.5 hover:border-indigo-200 hover:shadow-md"
          >
            <div className="flex items-center justify-between">
              <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-50 text-lg">⭐</span>
              <span className="text-[10px] font-black uppercase tracking-wider text-indigo-500">View level</span>
            </div>
            <div className="mt-3 text-sm font-black text-slate-900">
              Level {data?.level ?? "—"}{data?.levelName ? ` · ${data.levelName}` : ""}
            </div>
            <div className="mt-1 text-[11px] font-semibold text-slate-500">
              {data ? `${data.testsCompleted} tests · ${data.points.toLocaleString()} XP` : "Loading progress…"}
            </div>
          </button>

          <button
            type="button"
            onClick={() => document.getElementById("trophy-wall")?.scrollIntoView({ behavior: "smooth", block: "start" })}
            className="group min-h-[112px] rounded-2xl border border-amber-100 bg-white p-4 text-left shadow-sm transition hover:-translate-y-0.5 hover:border-amber-200 hover:shadow-md"
          >
            <div className="flex items-center justify-between">
              <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 text-lg">🏆</span>
              <span className="text-[10px] font-black uppercase tracking-wider text-amber-600">View badges</span>
            </div>
            <div className="mt-3 text-sm font-black text-slate-900">Badges</div>
            <div className="mt-1 text-[11px] font-semibold text-slate-500">
              {data ? `${earnedBadges} unlocked · ${totalBadges} achievements` : "Loading achievements…"}
            </div>
          </button>

          <button
            type="button"
            onClick={() => void createRevisionTest()}
            disabled={revisionLoading}
            className="group min-h-[112px] rounded-2xl bg-slate-950 p-4 text-left text-white shadow-sm transition hover:-translate-y-0.5 hover:bg-slate-900 hover:shadow-md disabled:cursor-wait disabled:opacity-60"
          >
            <div className="flex items-center justify-between">
              <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/10 text-lg">🤖</span>
              <span className="text-[10px] font-black uppercase tracking-wider text-cyan-300">AI Test</span>
            </div>
            <div className="mt-3 text-sm font-black">
              {revisionLoading ? "Building your test…" : "AI Generated Test"}
            </div>
            <div className="mt-1 text-[11px] font-semibold text-white/55">
              Personalised questions from your weakest areas.
            </div>
          </button>
        </div>

        {message && <p className="mt-3 text-xs font-bold text-red-600">{message}</p>}
      </div>
    </section>
  );
}
