"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type TestRecord = {
  attemptId: string; testId: string | null; title: string; score: number; totalMarks: number;
  percentage: number; status: string; startedAt?: string | null; submittedAt?: string | null;
  correct: number; incorrect: number; unanswered: number;
};

export default function TestSummaryPage() {
  const router = useRouter();
  const [tests, setTests] = useState<TestRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/student/test-history", { cache: "no-store" })
      .then(async (r) => {
        const data = await r.json();
        if (!r.ok || data.success === false) throw new Error(data.error || "Could not load past tests.");
        setTests(Array.isArray(data.tests) ? data.tests : []);
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Could not load past tests."))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="min-h-screen bg-[#f7f8fc] text-[#172033] px-4 py-5 sm:px-6 lg:px-10 pb-24 overflow-x-hidden">
      <div className="max-w-5xl mx-auto">
        <button onClick={() => router.push("/dashboard")} className="text-sm text-[#657083] mb-5">← Back to dashboard</button>
        <div className="flex items-center justify-between gap-3 mb-6">
          <div><h1 className="text-2xl sm:text-3xl font-black">My Tests</h1><p className="text-sm text-[#7a8495] mt-1">Your completed and past test records.</p></div>
          <button onClick={() => router.push("/tests")} className="rounded-xl bg-[#5b43df] text-white px-4 py-2.5 text-sm font-bold">Practice Test</button>
        </div>
        {loading ? <div className="rounded-2xl bg-white p-8 text-center">Loading your test records…</div> : error ? <div className="rounded-2xl bg-red-50 border border-red-100 p-5 text-red-700">{error}</div> : tests.length === 0 ? <div className="rounded-2xl bg-white p-10 text-center"><div className="text-4xl mb-3">📝</div><h2 className="font-black text-lg">No past tests yet</h2><p className="text-sm text-[#7a8495] mt-1">Your test records will appear here after you complete a test.</p></div> : (
          <div className="space-y-3">
            {tests.map((test) => (
              <button key={test.attemptId} type="button" onClick={() => test.testId && router.push(`/test/result/${test.testId}`)} className="w-full text-left rounded-2xl bg-white border border-[#e7e9ef] p-4 sm:p-5 shadow-sm hover:shadow-md transition active:scale-[.995]">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div className="min-w-0"><h2 className="font-black truncate">{test.title}</h2><p className="text-xs text-[#8a93a3] mt-1">{test.submittedAt ? new Date(test.submittedAt).toLocaleString() : "Completed test"}</p></div>
                  <div className="flex items-center gap-4"><div><div className="text-xs text-[#8a93a3]">Score</div><div className="font-black">{test.score}/{test.totalMarks}</div></div><div><div className="text-xs text-[#8a93a3]">Result</div><div className="font-black text-[#5b43df]">{test.percentage}%</div></div><span className="text-[#5b43df] font-black">→</span></div>
                </div>
                <div className="mt-3 flex flex-wrap gap-2 text-[11px] font-semibold"><span className="rounded-full bg-green-50 text-green-700 px-2.5 py-1">✓ {test.correct} correct</span><span className="rounded-full bg-red-50 text-red-700 px-2.5 py-1">✕ {test.incorrect} wrong</span><span className="rounded-full bg-gray-100 text-gray-600 px-2.5 py-1">{test.unanswered} unanswered</span></div>
              </button>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
