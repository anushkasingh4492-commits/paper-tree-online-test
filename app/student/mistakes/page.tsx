"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

type Mistake = {
  mistakeId: string;
  questionId: string;
  testId: string;
  attemptId: string;
  subject: string;
  exam: string;
  chapter: string;
  difficulty: string;
  stem: string;
  options: string[];
  selectedAnswer: string;
  correctAnswer: string;
  selectedIndex: number | null;
  correctIndex: number | null;
  isResolved: boolean;
  resolvedAt: string | null;
  attemptCount: number;
  firstMade: string;
  lastMade: string;
};

type MistakesResponse = {
  success?: boolean;
  error?: string;
  mistakes?: Mistake[];
  stats?: { total: number; unresolved: number };
};

export default function MistakesPage() {
  const router = useRouter();
  const [mistakes, setMistakes] = useState<Mistake[]>([]);
  const [stats, setStats] = useState({ total: 0, unresolved: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState<"all" | "unresolved">("all");
  const [subjectFilter, setSubjectFilter] = useState("");
  const [retrying, setRetrying] = useState<Set<string>>(new Set());

  const fetchMistakes = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const params = new URLSearchParams();
      if (filter === "unresolved") params.set("unresolved", "true");
      if (subjectFilter) params.set("subject", subjectFilter);
      params.set("limit", "100");

      const response = await fetch(`/api/student/mistakes?${params}`, {
        cache: "no-store",
      });
      const payload = (await response.json()) as MistakesResponse;

      if (!response.ok || !payload.success) {
        throw new Error(payload.error || "Could not load mistakes.");
      }

      setMistakes(payload.mistakes ?? []);
      setStats(payload.stats ?? { total: 0, unresolved: 0 });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load mistakes.");
    } finally {
      setLoading(false);
    }
  }, [filter, subjectFilter]);

  useEffect(() => {
    (async () => {
      await fetchMistakes();
    })();
  }, [fetchMistakes]);

  const subjects = useMemo(
    () =>
      Array.from(new Set(mistakes.map((m) => m.subject).filter(Boolean))).sort(),
    [mistakes]
  );

  const filteredMistakes = useMemo(() => {
    return mistakes.filter((m) => {
      if (filter === "unresolved" && m.isResolved) return false;
      if (subjectFilter && m.subject !== subjectFilter) return false;
      return true;
    });
  }, [mistakes, filter, subjectFilter]);

  const unresolvedMistakes = mistakes.filter((m) => !m.isResolved);

  const resolveMistake = async (mistakeId: string) => {
    try {
      const response = await fetch(
        `/api/student/mistakes/${mistakeId}`,
        { method: "DELETE" }
      );
      if (!response.ok) {
        const payload = (await response.json()) as { error?: string };
        throw new Error(payload.error || "Could not resolve mistake.");
      }
      await fetchMistakes();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not resolve mistake.");
    }
  };

  const retryMistake = async (questionId: string) => {
    setRetrying((prev) => new Set([...prev, questionId]));
    try {
      const response = await fetch("/api/tests/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          questionIds: [questionId],
          questionCount: 1,
          duration: 10,
          difficulty: "Balanced",
        }),
      });
      const payload = (await response.json()) as {
        success?: boolean;
        testId?: string;
        error?: string;
      };
      if (!response.ok || !payload.success || !payload.testId) {
        throw new Error(payload.error || "Could not generate retry test.");
      }
      router.push(`/test/${payload.testId}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not start retry.");
    } finally {
      setRetrying((prev) => {
        const next = new Set(prev);
        next.delete(questionId);
        return next;
      });
    }
  };

  const retryAllUnresolved = async () => {
    if (unresolvedMistakes.length === 0) return;
    setRetrying(new Set(unresolvedMistakes.map((m) => m.questionId)));
    try {
      const questionIds = unresolvedMistakes.map((m) => m.questionId);
      const response = await fetch("/api/tests/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          questionIds,
          questionCount: questionIds.length,
          duration: Math.max(5, questionIds.length * 2),
          difficulty: "Balanced",
        }),
      });
      const payload = (await response.json()) as {
        success?: boolean;
        testId?: string;
        error?: string;
      };
      if (!response.ok || !payload.success || !payload.testId) {
        throw new Error(payload.error || "Could not generate retry test.");
      }
      router.push(`/test/${payload.testId}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not start retry.");
    } finally {
      setRetrying(new Set());
    }
  };

  const formatDate = (value: string | null | undefined) => {
    if (!value) return "-";
    try {
      return new Date(value).toLocaleDateString(undefined, {
        month: "short",
        day: "numeric",
        year: "numeric",
      });
    } catch {
      return value;
    }
  };

  const s = (n: number) => (n !== 1 ? "s" : "");

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <div className="mx-auto max-w-4xl px-6 py-10">
        <header className="mb-8">
          <button
            onClick={() => router.push("/dashboard")}
            className="text-sm font-semibold text-[#315bea] mb-4 inline-flex items-center gap-1 transition hover:underline"
          >
            ← Back to Dashboard
          </button>
          <div className="flex items-center gap-3">
            <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-[#f0f9ff] text-2xl">
              📓
            </div>
            <div>
              <h1 className="text-2xl font-extrabold tracking-tight">
                Mistake Notebook
              </h1>
              <p className="text-sm text-[#697386]">
                Review questions you got wrong and retry them to improve.
              </p>
            </div>
          </div>
        </header>
        {error && (
          <div className="mb-6 rounded-xl bg-red-50 border border-red-100 p-4 text-sm font-medium text-red-700">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
          <StatCard
            label="Total Mistakes"
            value={stats.total}
            color="text-red-600 bg-red-50 border-red-100"
          />
          <StatCard
            label="Unresolved"
            value={stats.unresolved}
            color="text-amber-600 bg-amber-50 border-amber-100"
          />
          <StatCard
            label="Mastered"
            value={stats.total - stats.unresolved}
            color="text-green-600 bg-green-50 border-green-100"
          />
        </div>

        {unresolvedMistakes.length > 0 && (
          <div className="mb-6">
            <button
              onClick={retryAllUnresolved}
              disabled={retrying.size > 0}
              className="w-full flex items-center justify-center gap-2 rounded-xl bg-[#16a34a] px-5 py-3 font-bold text-white hover:bg-[#15803d] disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              {retrying.size === unresolvedMistakes.length ? (
                <span className="flex items-center gap-1.5 animate-pulse">
                  <span className="w-3 h-3 rounded-full bg-white/30 animate-pulse" />
                  <span className="w-3 h-3 rounded-full bg-white/30 animate-pulse" style={{ animationDelay: "0.2s" }} />
                  <span className="w-3 h-3 rounded-full bg-white/30 animate-pulse" style={{ animationDelay: "0.4s" }} />
                </span>
              ) : (
                <>
                  <span>🔄</span>
                  <span>
                    Retry All {unresolvedMistakes.length}{s(
                      unresolvedMistakes.length
                    )}
                  </span>
                </>
              )}
            </button>
          </div>
        )}

        <div className="flex flex-wrap items-center gap-3 mb-6">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl border border-[#dfe4ee] bg-white text-sm">
            <span className="font-medium text-[#697386]">Filter:</span>
            <button
              onClick={() => setFilter("all")}
              className={`px-3 py-1 rounded-md text-sm font-medium transition ${
                filter === "all"
                  ? "bg-[#315bea] text-white"
                  : "text-[#697386] hover:bg-[#f0f2f6]"
              }`}
            >
              All
            </button>
            <button
              onClick={() => setFilter("unresolved")}
              className={`px-3 py-1 rounded-md text-sm font-medium transition ${
                filter === "unresolved"
                  ? "bg-[#315bea] text-white"
                  : "text-[#697386] hover:bg-[#f0f2f6]"
              }`}
            >
              Unresolved Only
            </button>
          </div>

          <div className="flex-1 flex items-center gap-2 px-3 py-1.5 rounded-xl border border-[#dfe4ee] bg-white text-sm">
            <span className="font-medium text-[#697386]">Subject:</span>
            <select
              value={subjectFilter}
              onChange={(e) => setSubjectFilter(e.target.value)}
              className="bg-transparent border-none text-sm text-[#172033] focus:ring-0 sm:px-2"
            >
              <option value="">All Subjects</option>
              {subjects.map((sub) => (
                <option key={sub} value={sub}>
                  {sub}
                </option>
              ))}
            </select>
          </div>

          <div className="ml-auto text-xs text-[#8a93a5]">
            {filteredMistakes.length} of {mistakes.length} mistake{s(
              mistakes.length
            )} showing
          </div>
        </div>
        {loading ? (
          <div className="h-64 flex items-center justify-center">
            <div className="w-8 h-8 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin" />
          </div>
        ) : filteredMistakes.length === 0 ? (
          <div className="rounded-2xl border border-[#e5e8ef] bg-white p-12 text-center shadow-sm">
            <div className="text-4xl mb-4">📓</div>
            {filter === "unresolved" && unresolvedMistakes.length === 0 ? (
              <>
                <h2 className="text-xl font-bold text-[#172033]">
                  No unresolved mistakes! 🎉
                </h2>
                <p className="mt-2 text-[#697386]">
                  You&apos;ve mastered all your past mistakes. Keep it up!
                </p>
              </>
            ) : (
              <>
                <h2 className="text-xl font-bold text-[#172033]">
                  No mistakes yet.
                </h2>
                <p className="mt-2 text-[#697386]">
                  Take some tests and your wrong answers will appear here
                  automatically.
                </p>
              </>
            )}
          </div>
        ) : (
          <div className="rounded-xl border border-[#e5e8ef] bg-white shadow-sm overflow-hidden">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-[#f0f2f6] bg-[#fafbfc]">
                  <th className="px-5 py-3 font-bold text-[#697386] uppercase text-[10px] tracking-[0.12em]">
                    Question
                  </th>
                  <th className="px-5 py-3 font-bold text-[#697386] uppercase text-[10px] tracking-[0.12em]">
                    Subject
                  </th>
                  <th className="px-5 py-3 font-bold text-[#697386] uppercase text-[10px] tracking-[0.12em]">
                    Chapter
                  </th>
                  <th className="px-5 py-3 font-bold text-[#697386] uppercase text-[10px] tracking-[0.12em] text-right">
                    Attempts
                  </th>
                  <th className="px-5 py-3 font-bold text-[#697386] uppercase text-[10px] tracking-[0.12em]">
                    Status
                  </th>
                  <th className="px-5 py-3 font-bold text-[#697386] uppercase text-[10px] tracking-[0.12em]">
                    Action
                  </th>
                </tr>
              </thead>
              <tbody>
                {filteredMistakes.map((m) => (
                  <tr
                    key={m.mistakeId}
                    className="border-b border-[#f5f7fb] hover:bg-[#f8fafc] transition"
                  >
                    <td className="px-5 py-4">
                      <div className="font-semibold text-[#172033] truncate max-w-[220px]">
                        {m.stem}
                      </div>
                      <div className="mt-1 text-xs text-[#8a93a5]">
                        Q#{m.questionId} · {m.exam} · {formatDate(m.lastMade)}
                      </div>
                    </td>
                    <td className="px-5 py-4">{m.subject}</td>
                    <td className="px-5 py-4 text-sm text-[#172033]">
                      {m.chapter || "—"}
                    </td>
                    <td className="px-5 py-4 text-right text-sm font-semibold text-[#697386]">
                      {m.attemptCount}
                    </td>
                    <td className="px-5 py-4">
                      <span
                        className={`px-2 py-1 rounded-md text-xs font-bold border ${statusColor(m.isResolved)}`}
                      >
                        {m.isResolved ? "Resolved" : "Unresolved"}
                      </span>
                    </td>
                    <td className="px-5 py-4">
                      {!m.isResolved && (
                        <button
                          onClick={() => retryMistake(m.questionId)}
                          disabled={retrying.has(m.questionId)}
                          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[#dfe4ee] bg-white text-sm font-semibold text-[#315bea] hover:bg-[#f0f7ff] transition disabled:opacity-50"
                        >
                          {retrying.has(m.questionId) ? (
                            <span className="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin" />
                          ) : (
                            "🔄 Retry"
                          )}
                        </button>
                      )}
                      {!m.isResolved && (
                        <button
                          onClick={() => resolveMistake(m.mistakeId)}
                          className="mt-2 flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[#dfe4ee] bg-white text-sm font-semibold text-[#16a34a] hover:bg-[#f0fdf4] transition"
                        >
                          ✅ Mark Resolved
                        </button>
                      )}
                      {m.isResolved && (
                        <span className="text-xs text-[#8a93a5]">Mastered</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </main>
  );
}

const statusColor = (isResolved: boolean) =>
  isResolved
    ? "text-green-600 bg-green-50 border-green-100"
    : "text-amber-600 bg-amber-50 border-amber-100";

function StatCard({
  label,
  value,
  color,
}: {
  label: string;
  value: number;
  color: string;
}) {
  return (
    <div className={`rounded-2xl border p-5 ${color}`}>
      <div className="text-[10px] uppercase tracking-widest font-bold">
        {label}
      </div>
      <div className="text-2xl font-black mt-1">{value}</div>
    </div>
  );
}

