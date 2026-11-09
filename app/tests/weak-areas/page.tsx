"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowLeft, Sparkles } from "lucide-react";

type WeakArea = {
  chapter: string;
  subject: string;
  misses: number;
  total: number;
  rate: number;
};

type InsightsResponse = {
  success: boolean;
  error?: string;
  weakAreas: WeakArea[];
};

export default function WeakAreasTestPage() {
  const router = useRouter();
  const [weakAreas, setWeakAreas] = useState<WeakArea[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;

    fetch("/api/student/insights", { cache: "no-store", credentials: "include" })
      .then(async (response) => {
        const value: InsightsResponse = await response.json();
        if (!response.ok || !value.success) {
          throw new Error(value.error || "Could not load your weak areas.");
        }
        if (active) setWeakAreas(value.weakAreas ?? []);
      })
      .catch((cause: unknown) => {
        if (active) setError(cause instanceof Error ? cause.message : "Could not load your weak areas.");
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, []);

  async function createRevisionTest() {
    setGenerating(true);
    setError("");
    try {
      const response = await fetch("/api/student/revision-test", {
        method: "POST",
        credentials: "include",
      });
      const value: { success: boolean; error?: string; testId?: string } = await response.json();
      if (!response.ok || !value.success || !value.testId) {
        throw new Error(value.error || "Could not create your practice test.");
      }
      router.push(`/test/${value.testId}`);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Could not create your practice test.");
    } finally {
      setGenerating(false);
    }
  }

  return (
    <main className="min-h-screen bg-surface-app-bg text-text-primary">
      <div className="mx-auto max-w-4xl px-6 py-10">
        <button
          type="button"
          onClick={() => router.push("/dashboard")}
          className="mb-5 inline-flex items-center gap-2 text-sm font-semibold text-brand-primary transition hover:underline"
        >
          <ArrowLeft size={16} />
          Back to Dashboard
        </button>

        <section className="rounded-2xl border border-border-default bg-white p-6 shadow-sm sm:p-8">
          <div className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <p className="text-xs font-bold uppercase tracking-widest text-brand-primary">Personalized practice</p>
              <h1 className="mt-2 text-2xl font-extrabold tracking-tight">Your Weak Areas</h1>
              <p className="mt-2 max-w-xl text-sm text-text-body">
                Review the chapters that need more practice, then build a test focused on them.
              </p>
            </div>
            <button
              type="button"
              onClick={() => void createRevisionTest()}
              disabled={generating}
              className="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl bg-brand-primary px-5 py-3 text-sm font-bold text-white transition hover:opacity-90 disabled:cursor-wait disabled:opacity-60"
            >
              <Sparkles size={16} />
              {generating ? "Building your test…" : "Generate Practice Test"}
            </button>
          </div>

          {error && (
            <p role="alert" className="mt-5 rounded-xl border border-red-200 bg-red-50 p-3 text-sm font-medium text-red-700">
              {error}
            </p>
          )}

          {loading ? (
            <p role="status" className="mt-8 text-sm text-text-body">Loading your weak areas…</p>
          ) : weakAreas.length ? (
            <ul className="mt-8 space-y-3">
              {weakAreas.map((area) => (
                <li
                  key={`${area.subject}-${area.chapter}`}
                  className="flex items-center justify-between gap-4 rounded-xl border border-border-default bg-surface-app-bg p-4"
                >
                  <div className="min-w-0">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-text-supporting-label">{area.subject}</p>
                    <h2 className="mt-1 truncate text-sm font-bold">{area.chapter}</h2>
                    <p className="mt-1 text-xs text-text-body">{area.misses} missed out of {area.total} questions</p>
                  </div>
                  <span className="shrink-0 rounded-full bg-rose-50 px-3 py-1 text-xs font-bold text-rose-700">
                    {area.rate}% missed
                  </span>
                </li>
              ))}
            </ul>
          ) : !error ? (
            <p className="mt-8 rounded-xl bg-surface-app-bg p-4 text-sm text-text-body">
              No weak areas have been identified yet. Complete a few tests to get personalized chapter recommendations.
            </p>
          ) : null}
        </section>
      </div>
    </main>
  );
}
