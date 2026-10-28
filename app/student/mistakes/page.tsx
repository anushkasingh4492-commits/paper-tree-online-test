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
  const [retryAnswers, setRetryAnswers] = useState<Record<string, string>>({});
  const [retryResults, setRetryResults] = useState<Record<string, "correct" | "wrong">>({});

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

  const retryAnswerChange = (questionId: string, value: string) => {
    setRetryAnswers((prev) => ({ ...prev, [questionId]: value }));
    setRetryResults((prev) => {
      const next = { ...prev };
      delete next[questionId];
      return next;
    });
  };

  const submitRetryAnswer = async (mistake: Mistake) => {
    const questionId = mistake.questionId;
    const userAnswer = retryAnswers[questionId]?.trim() || "";
    const correctAnswer = mistake.correctAnswer.trim();

    setRetrying((prev) => new Set([...prev, questionId]));

    try {
      const normalize = (s: string) =>
        s
          .toLowerCase()
          .replace(/\s+/g, " ")
          .trim()
          .replace(/[.,;:!?]$/, "");

      const correctLetter = mistake.correctIndex == null
        ? ""
        : String.fromCharCode(65 + mistake.correctIndex);
      const correctOption = mistake.correctIndex == null
        ? ""
        : mistake.options[mistake.correctIndex] ?? "";
      const isCorrect = [
        correctAnswer,
        correctLetter,
        correctOption,
      ].some((answer) => answer && normalize(userAnswer) === normalize(answer));

      setRetryResults((prev) => ({
        ...prev,
        [questionId]: isCorrect ? "correct" : "wrong",
      }));

      if (isCorrect) {
        const response = await fetch(
          `/api/student/mistakes/${mistake.mistakeId}`,
          { method: "DELETE" }
        );
        if (!response.ok) {
          throw new Error("Could not mark mistake as resolved.");
        }
      }

      await fetchMistakes();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Retry failed.");
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
      const results = await Promise.allSettled(
        unresolvedMistakes.map((m) =>
          fetch(`/api/student/mistakes/${m.mistakeId}`, {
            method: "DELETE",
          })
        )
      );

      const failed = results.filter(
        (r) => r.status === "rejected"
      ).length;

      if (failed > 0) {
        setError(`Failed to resolve ${failed} mistake(s).`);
      }

      await fetchMistakes();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not resolve mistakes.");
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

  const statusColor = (isResolved: boolean) =>
    isResolved
      ? "text-green-600 bg-green-50 border-green-100"
      : "text-amber-600 bg-amber-50 border-amber-100";

  const s = (n: number) => (n !== 1 ? "s" : "");

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <div className="mx-auto w-full max-w-4xl px-3 py-5 sm:px-6 sm:py-10">
        <header className="mb-8">
          <button
            onClick={() => router.push("/dashboard")}
            className="text-sm font-semibold text-[#315bea] mb-4 inline-flex items-center gap-1 transition hover:underline"
          >
            &#x2190; Back to Dashboard
          </button>
          <div className="flex items-center gap-3">
            <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-[#f0f9ff] text-2xl">
              &#x1F4D3;
            </div>
            <div>
              <h1 className="text-xl sm:text-2xl font-extrabold tracking-tight">
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
                  <span>&#x1F504;</span>
                  <span>
                    Mark All {unresolvedMistakes.length}{s(
                      unresolvedMistakes.length
                    )}
                    as Resolved
                  </span>
                </>
              )}
            </button>
          </div>
        )}

        <div className="flex flex-col sm:flex-row sm:flex-wrap items-stretch sm:items-center gap-3 mb-6">
          <div className="flex flex-wrap items-center gap-1.5 px-2 sm:px-3 py-2 rounded-xl border border-[#dfe4ee] bg-white text-sm">
            <span className="font-medium text-[#697386]">Filter:</span>
            <button
              onClick={() => setFilter("all")}
              className={`px-3 py-1 rounded-md text-sm font-medium transition ${filter === "all" ? "bg-[#315bea] text-white" : "text-[#697386] hover:bg-[#f0f2f6]"}`}
            >
              All
            </button>
            <button
              onClick={() => setFilter("unresolved")}
              className={`px-3 py-1 rounded-md text-sm font-medium transition ${filter === "unresolved" ? "bg-[#315bea] text-white" : "text-[#697386] hover:bg-[#f0f2f6]"}`}
            >
              Unresolved Only
            </button>
          </div>

          <div className="w-full sm:flex-1 min-w-0 flex items-center gap-2 px-3 py-2 rounded-xl border border-[#dfe4ee] bg-white text-sm">
            <span className="font-medium text-[#697386]">Subject:</span>
            <select
              value={subjectFilter}
              onChange={(e) => setSubjectFilter(e.target.value)}
              className="min-w-0 flex-1 bg-transparent border-none text-sm text-[#172033] focus:ring-0 sm:px-2"
            >
              <option value="">All Subjects</option>
              {subjects.map((sub) => (
                <option key={sub} value={sub}>
                  {sub}
                </option>
              ))}
            </select>
          </div>

          <div className="sm:ml-auto text-xs text-[#8a93a5]">
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
            <div className="text-4xl mb-4">&#x1F4D3;</div>
            {filter === "unresolved" && unresolvedMistakes.length === 0 ? (
              <>
                <h2 className="text-xl font-bold text-[#172033]">
                  No unresolved mistakes! &#x1F389;
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
          <>
          <div className="space-y-3 md:hidden">
            {filteredMistakes.map((m) => (
              <article key={m.mistakeId} className="min-w-0 rounded-2xl border border-[#e5e8ef] bg-white p-4 shadow-sm">
                <div className="flex items-start justify-between gap-2"><span className="rounded-lg bg-indigo-50 px-2 py-1 text-[10px] font-black text-indigo-700">{m.subject || "General"}</span><span className={`shrink-0 rounded-md border px-2 py-1 text-[10px] font-bold ${statusColor(m.isResolved)}`}>{m.isResolved ? "Resolved" : "Unresolved"}</span></div>
                <h2 className="mt-3 break-words text-sm font-bold leading-6 text-[#172033]">{m.stem}</h2>
                <p className="mt-1 break-words text-[11px] text-[#8a93a5]">{m.chapter || "No chapter"} · {m.exam || "Practice"} · {formatDate(m.lastMade)}</p>
                {m.options.length > 0 && <div className="mt-3 space-y-1.5">{m.options.map((opt, idx) => { const correct = idx === m.correctIndex; const selected = idx === m.selectedIndex; return <div key={idx} className={`break-words rounded-lg border px-3 py-2 text-xs ${correct ? "border-green-100 bg-green-50 text-green-700" : selected ? "border-rose-100 bg-rose-50 text-rose-700" : "border-[#f0f2f6] bg-[#f8fafc] text-[#697386]"}`}>{String.fromCharCode(65 + idx)}. {opt}</div>; })}</div>}
                <div className="mt-3 flex flex-wrap items-center justify-between gap-2 text-[11px] text-[#697386]"><span>{m.attemptCount} attempt{m.attemptCount === 1 ? "" : "s"}</span><span>Q#{m.questionId}</span></div>
                {!m.isResolved && <div className="mt-3">{retryResults[m.questionId] === "correct" ? <div className="rounded-lg bg-green-50 p-3 text-xs font-bold text-green-700">✓ Correct — resolved!</div> : retryResults[m.questionId] === "wrong" ? <p className="mb-2 text-xs font-bold text-rose-600">Not quite — try again.</p> : null}<div className="flex gap-2"><input type="text" value={retryAnswers[m.questionId] || ""} onChange={(e) => retryAnswerChange(m.questionId, e.target.value)} placeholder="Your answer" className="min-w-0 flex-1 rounded-xl border border-[#dfe4ee] px-3 py-2.5 text-sm focus:border-[#315bea] focus:outline-none" disabled={retrying.has(m.questionId)} /><button type="button" onClick={() => void submitRetryAnswer(m)} disabled={retrying.has(m.questionId) || !retryAnswers[m.questionId]?.trim()} className="shrink-0 rounded-xl bg-[#315bea] px-4 py-2.5 text-sm font-bold text-white disabled:opacity-50">{retrying.has(m.questionId) ? "…" : "Check"}</button></div></div>}
              </article>
            ))}
          </div>
          <div className="hidden md:block rounded-xl border border-[#e5e8ef] bg-white shadow-sm overflow-hidden">
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
                    Retry
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
                        Q#{m.questionId} &#x00B7; {m.exam} &#x00B7; {formatDate(m.lastMade)}
                      </div>
                      {m.options.length > 0 && (
                        <div className="mt-3 space-y-1">
                          {m.options.map((opt, idx) => {
                            const letter = String.fromCharCode(65 + idx);
                            const isCorrect = idx === m.correctIndex;
                            const isSelected = idx === m.selectedIndex;
                            return (
                              <div
                                key={idx}
                                className={`text-xs px-3 py-2 rounded border ${isCorrect ? "bg-green-50 text-green-700 border-green-100" : isSelected ? "bg-rose-50 text-rose-700 border-rose-100" : "bg-[#f8fafc] text-[#697386] border-[#f0f2f6]"}`}
                              >
                                {letter}. {opt}
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </td>
                    <td className="px-5 py-4">{m.subject}</td>
                    <td className="px-5 py-4 text-sm text-[#172033]">
                      {m.chapter || "\u2014"}
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
                      {!m.isResolved ? (
                        <>
                          {retryResults[m.questionId] === "correct" ? (
                            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[#16a34a] bg-[#f0fdf4] text-sm font-semibold text-[#16a34a]">
                              <span className="w-3 h-3 rounded-full bg-[#16a34a] text-white flex items-center justify-center text-[10px]">
                                &#x2713;
                              </span>
                              Correct &#x2014; resolved!
                            </div>
                          ) : retryResults[m.questionId] === "wrong" ? (
                            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[#dc2626] bg-[#fef2f2] text-sm font-semibold text-[#dc2626]">
                              <span className="w-3 h-3 rounded-full bg-[#dc2626] text-white flex items-center justify-center text-[10px]">
                                &#x2717;
                              </span>
                              Try again
                            </div>
                          ) : (
                            <>
                              <div className="flex items-center gap-2 mb-2">
                                <input
                                  type="text"
                                  value={retryAnswers[m.questionId] || ""}
                                  onChange={(e) =>
                                    retryAnswerChange(m.questionId, e.target.value)
                                  }
                                  placeholder="Your answer"
                                  className="flex-1 px-3 py-2 rounded-xl border border-[#dfe4ee] bg-white text-sm focus:border-[#315bea] focus:outline-none"
                                  disabled={retrying.has(m.questionId)}
                                />
                                <button
                                  onClick={() => submitRetryAnswer(m)}
                                  disabled={retrying.has(m.questionId) || !retryAnswers[m.questionId]?.trim()}
                                  className="px-3 py-2 rounded-xl border border-[#315bea] bg-[#315bea] text-white text-sm font-semibold hover:bg-[#264ac7] disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                  Check
                                </button>
                              </div>
                              {retrying.has(m.questionId) && (
                                <span className="text-xs text-[#697386]">
                                  Checking&#x2026;
                                </span>
                              )}
                            </>
                          )}
                        </>
                      ) : (
                        <span className="text-xs text-[#8a93a5]">Mastered</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
           </>
        )}
      </div>
    </main>
  );
}

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
