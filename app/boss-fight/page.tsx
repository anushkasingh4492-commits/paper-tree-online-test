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
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <div className="mx-auto max-w-4xl px-6 py-10">
        <div className="flex items-center justify-between mb-8">
          <div>
            <button
              onClick={() => router.push("/dashboard")}
              className="text-sm font-semibold text-[#315bea] mb-2 inline-block transition hover:underline"
            >
              ← Back to Dashboard
            </button>
            <h1 className="text-2xl font-extrabold tracking-tight">
              Boss Fight Queue
            </h1>
            <p className="text-sm text-[#697386]">
              Chapters to Conquer — master your weakest areas first.
            </p>
          </div>
        </div>

        {loading ? (
          <div className="h-64 flex items-center justify-center">
            <div className="w-8 h-8 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin" />
          </div>
        ) : chapters.length === 0 ? (
          <div className="rounded-2xl border border-[#e5e8ef] bg-white p-16 text-center shadow-sm">
            <div className="text-4xl mb-4">👑</div>
            <h2 className="text-xl font-bold text-[#172033]">
              No chapters to conquer!
            </h2>
            <p className="mt-2 text-[#697386]">
              You've mastered all your weak areas. Keep testing to find new challenges.
            </p>
            <button
              onClick={() => router.push("/tests/generate")}
              className="mt-6 px-5 py-2.5 rounded-xl bg-[#315bea] text-white text-sm font-semibold hover:bg-[#264ac7] transition"
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
                    ? "border-[#fca5a5] bg-[#fef2f2]"
                    : c.status === "improving"
                      ? "border-[#fde047] bg-[#fefce8]"
                      : "border-[#86efac] bg-[#f0fdf4]"
                }`}
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-[10px] font-bold text-[#697386] uppercase tracking-[0.15em]">
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
                  <h3 className="font-bold text-sm text-[#172033] leading-tight">
                    {c.chapter}
                  </h3>
                  <div className="mt-1 flex items-center gap-2 text-xs text-[#697386]">
                    <span>Correct: {c.correct}</span>
                    <span>•</span>
                    <span>Wrong: {c.wrong}</span>
                    <span>•</span>
                    <span>Unanswered: {c.unanswered}</span>
                    <span>•</span>
                    <span>Accuracy: {c.accuracy.toFixed(0)}%</span>
                  </div>
                </div>
                <div className="mt-2 ml-9 h-1.5 rounded-full bg-[#e8eaf0] overflow-hidden w-48">
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
                  className="px-4 py-2 rounded-lg border border-[#dfe4ee] bg-white text-sm font-semibold text-[#315bea] hover:bg-[#f0f7ff] transition"
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
