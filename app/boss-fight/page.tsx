"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type WeakChapter = {
  chapter: string;
  subject: string;
  accuracy: number;
  correct: number;
  wrong: number;
  unanswered: number;
  status: "weak" | "improving" | "mastered";
};

export default function BossFightPage() {
  const router = useRouter();
  const [chapters, setChapters] = useState<WeakChapter[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch("/api/student/boss-fight", { cache: "no-store" });
        const data = await res.json();
        if (data.success) setChapters(data.chapters || []);
      } catch {
        // silent
      } finally {
        setLoading(false);
      }
    })();
  }, []);

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
              Boss Fight Queue
            </h1>
            <p className="text-sm text-text-tertiary">
              Chapters to Conquer — master your weakest areas first.
            </p>
          </div>
        </div>

        {loading ? (
          <div className="h-64 flex items-center justify-center">
            <div className="w-8 h-8 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin" />
          </div>
        ) : chapters.length === 0 ? (
          <div className="rounded-2xl border border-border-default bg-white p-16 text-center shadow-sm">
            <div className="text-4xl mb-4">👑</div>
            <h2 className="text-xl font-bold text-text-primary">
              No chapters to conquer!
            </h2>
            <p className="mt-2 text-text-tertiary">
              You've mastered all your weak areas. Keep testing to find new challenges.
            </p>
            <button
              onClick={() => router.push("/tests/generate")}
              className="mt-6 px-5 py-2.5 rounded-xl bg-brand-primary text-white text-sm font-semibold hover:bg-brand-primary transition"
            >
              Create a New Test
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            {chapters.map((c) => (
              <div
                key={`${c.subject}-${c.chapter}`}
                className={`rounded-xl border p-4 flex items-center justify-between ${
                  c.status === "weak"
                    ? "border-[#fca5a5] bg-state-error"
                    : c.status === "improving"
                      ? "border-[#fde047] bg-state-warning"
                      : "border-[#86efac] bg-state-success"
                }`}
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-[10px] font-bold text-text-tertiary uppercase tracking-[0.15em]">
                      {c.subject}
                    </span>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        c.status === "weak"
                          ? "text-rose-600 bg-rose-50"
                          : c.status === "improving"
                            ? "text-amber-600 bg-amber-50"
                            : "text-emerald-600 bg-emerald-50"
                      }`}
                    >
                      {c.status}
                    </span>
                  </div>
                  <h3 className="font-bold text-sm text-text-primary leading-tight">
                    {c.chapter}
                  </h3>
                  <div className="mt-1 flex items-center gap-2 text-xs text-text-tertiary">
                    <span>Correct: {c.correct}</span>
                    <span>•</span>
                    <span>Wrong: {c.wrong}</span>
                    <span>•</span>
                    <span>Unanswered: {c.unanswered}</span>
                    <span>•</span>
                    <span>Accuracy: {c.accuracy.toFixed(0)}%</span>
                  </div>
                </div>
                <div className="mt-2 ml-9 h-1.5 rounded-full bg-surface-app-bg overflow-hidden w-48">
                  <div
                    className="h-full rounded-full"
                    style={{
                      width: `${c.accuracy}%`,
                      backgroundColor:
                        c.status === "weak"
                          ? "#fca5a5"
                          : c.status === "improving"
                            ? "#fde047"
                            : "#86efac",
                    }}
                  />
                </div>
                <button
                  onClick={() => router.push(`/tests/generate?chapter=${encodeURIComponent(c.chapter)}&subject=${encodeURIComponent(c.subject)}`)}
                  className="px-4 py-2 rounded-lg border border-border-default bg-white text-sm font-semibold text-brand-primary hover:bg-[#f0f7ff] transition"
                >
                  Conquer
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
