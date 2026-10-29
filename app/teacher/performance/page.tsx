 "use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import StudentBadgeModal from "@/components/StudentBadgeModal";

type StudentPerformance = {
  id: string;
  name: string;
  email: string;
  batches: string;
  testsTaken: number;
  averagePercentage: number;
  bestPercentage: number;
  correctAnswers: number;
  wrongAnswers: number;
  unansweredQuestions: number;
  accuracy: number;
  parentPhone?: string | null;
  level: number;
  levelName: string;
  currentStreak: number;
  lastActiveDate: string | null;
  badgesEarned: number;
};

type StudentAttempt = {
  id: string;
  test_id: string;
  scheduled_test_id?: string | null;
  score: number | null;
  total_marks: number | null;
  correct_count: number | null;
  incorrect_count: number | null;
  unanswered_count: number | null;
  status: string | null;
  started_at: string | null;
  submitted_at: string | null;
  test_title: string;
  exam?: string | null;
  question_count?: number;
  subjects?: string[];
  chapters?: string[];
  difficulties?: string[];
  question_types?: string[];
  percentage?: number;
};

export default function TeacherPerformancePage() {
  const router = useRouter();
  const [students, setStudents] = useState<StudentPerformance[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [batchFilter, setBatchFilter] = useState("ALL");
  const [sortBy, setSortBy] = useState("name");
  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("asc");
  const [sending, setSending] = useState<string | null>(null);
  const [report, setReport] = useState<{ studentId: string; text: string } | null>(null);
  const [badgeStudent, setBadgeStudent] = useState<StudentPerformance | null>(null);
  const [attemptStudent, setAttemptStudent] = useState<StudentPerformance | null>(null);
  const [attempts, setAttempts] = useState<StudentAttempt[]>([]);
  const [attemptLoading, setAttemptLoading] = useState(false);
  const [attemptError, setAttemptError] = useState("");
  const [features, setFeatures] = useState<{ aiPerformanceSummaries: boolean; parentWhatsAppReports: boolean } | null>(null);

  useEffect(() => {
    void fetch("/api/academy/tier", { cache: "no-store", credentials: "include" })
      .then((response) => response.json())
      .then((data) => { if (data?.success) setFeatures(data.features); })
      .catch(() => undefined);
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const response = await fetch("/api/teacher/performance", {
          cache: "no-store",
        });
        const data = await response.json();

        if (!response.ok || !data.success) {
          throw new Error(data.error || "Could not load student performance.");
        }

        if (!cancelled) setStudents(data.students || []);
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Could not load student performance."
          );
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    void load();
    return () => {
      cancelled = true;
    };
  }, []);

  const batchOptions = useMemo(() => {
    const values = new Set<string>();

    for (const student of students) {
      student.batches
        .split(",")
        .map((batch) => batch.trim())
        .filter(Boolean)
        .forEach((batch) => values.add(batch));
    }

    return Array.from(values).sort((a, b) =>
      a.localeCompare(b, undefined, { sensitivity: "base" })
    );
  }, [students]);

  // Default to the first batch instead of loading all batches together.
  useEffect(() => {
    if (batchOptions.length > 0 && batchFilter === "ALL") {
      setBatchFilter(batchOptions[0]);
    }
  }, [batchOptions]);

  const filteredStudents = useMemo(() => {
    const query = search.trim().toLowerCase();

    const filtered = students.filter((student) => {
      const matchesSearch =
        !query ||
        [student.name, student.email, student.batches].some((value) =>
          value.toLowerCase().includes(query)
        );

      const matchesBatch =
        batchFilter === "ALL" ||
        student.batches
          .split(",")
          .map((batch) => batch.trim())
          .includes(batchFilter);

      return matchesSearch && matchesBatch;
    });

    const valueForSort = (student: StudentPerformance): string | number => {
      switch (sortBy) {
        case "batch":
          return student.batches;
        case "level":
          return student.level;
        case "streak":
          return student.currentStreak;
        case "tests":
          return student.testsTaken;
        case "average":
          return student.averagePercentage;
        case "best":
          return student.bestPercentage;
        case "accuracy":
          return student.accuracy;
        case "correct":
          return student.correctAnswers;
        case "wrong":
          return student.wrongAnswers;
        case "unanswered":
          return student.unansweredQuestions;
        case "badges":
          return student.badgesEarned;
        case "lastActive":
          return student.lastActiveDate
            ? new Date(student.lastActiveDate).getTime()
            : 0;
        case "name":
        default:
          return student.name;
      }
    };

    return [...filtered].sort((a, b) => {
      const first = valueForSort(a);
      const second = valueForSort(b);
      const direction = sortDirection === "asc" ? 1 : -1;

      if (typeof first === "string" && typeof second === "string") {
        return (
          first.localeCompare(second, undefined, {
            sensitivity: "base",
          }) * direction
        );
      }

      return (Number(first) - Number(second)) * direction;
    });
  }, [students, search, batchFilter, sortBy, sortDirection]);

  async function openAttempts(student: StudentPerformance) {
    setAttemptStudent(student);
    setAttempts([]);
    setAttemptError("");
    setAttemptLoading(true);

    try {
      const response = await fetch(
        `/api/teacher/performance?studentId=${encodeURIComponent(student.id)}`,
        { cache: "no-store" }
      );
      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || "Could not load attempted tests.");
      }

      setAttempts(data.attempts || []);
    } catch (error) {
      setAttemptError(
        error instanceof Error
          ? error.message
          : "Could not load attempted tests."
      );
    } finally {
      setAttemptLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.15em] text-[#315bea]">
              Teacher Portal
            </p>
            <h1 className="mt-2 text-3xl font-extrabold tracking-tight">
              Student Performance
            </h1>
            <p className="mt-2 text-sm text-[#697386]">
              View performance across all students in your academy.
            </p>
          </div>

          <button
            onClick={() => router.push("/teacher")}
            className="rounded-xl border border-[#e2e6ee] bg-white px-4 py-2.5 text-sm font-bold text-[#697386] hover:bg-[#f7f8fb]"
          >
            ← Back to Teacher Portal
          </button>
        </header>

        {!loading && !error && filteredStudents.length > 0 && (
          <section className="mb-6 rounded-2xl border border-[#e3e8f5] bg-white p-5 shadow-sm sm:p-6">
            <div className="mb-5">
              <h2 className="text-lg font-extrabold">Performance at a glance</h2>
              <p className="mt-1 text-sm text-[#8a93a5]">A separate visual summary of the students currently shown by your filters.</p>
            </div>
            {[
              { label: "Average score", value: Math.round(filteredStudents.reduce((sum, student) => sum + student.averagePercentage, 0) / filteredStudents.length), color: "bg-indigo-500" },
              { label: "Average accuracy", value: Math.round(filteredStudents.reduce((sum, student) => sum + student.accuracy, 0) / filteredStudents.length), color: "bg-emerald-500" },
              { label: "Students with 5+ tests", value: Math.round((filteredStudents.filter((student) => student.testsTaken >= 5).length / filteredStudents.length) * 100), color: "bg-amber-500" },
            ].map((metric) => (
              <div key={metric.label} className="mb-4 last:mb-0">
                <div className="mb-2 flex items-center justify-between gap-3 text-sm">
                  <span className="font-semibold text-[#465064]">{metric.label}</span>
                  <span className="font-extrabold text-[#172033]">{metric.value}%</span>
                </div>
                <div className="h-3 overflow-hidden rounded-full bg-[#edf0f6]">
                  <div className={`h-full rounded-full ${metric.color}`} style={{ width: `${Math.max(0, Math.min(100, metric.value))}%` }} />
                </div>
              </div>
            ))}
          </section>
        )}

        <section className="rounded-2xl border border-[#e3e8f5] bg-white shadow-sm">
          <div className="border-b border-[#eef0f4] px-6 py-5">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <h2 className="text-lg font-extrabold">All Students</h2>
                <p className="mt-1 text-sm text-[#8a93a5]">
                  Filter by batch and sort by any available performance metric.
                </p>
              </div>

              <input
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Search student or batch"
                className="w-full max-w-xs rounded-xl border border-[#dfe4ee] px-4 py-2.5 text-sm outline-none focus:border-[#315bea]"
              />
            </div>

            <div className="mt-4 flex flex-wrap items-center gap-3">
              <select
                value={batchFilter}
                onChange={(event) => setBatchFilter(event.target.value)}
                className="rounded-xl border border-[#dfe4ee] bg-white px-3 py-2.5 text-sm font-semibold outline-none focus:border-[#315bea]"
              >
                {batchOptions.map((batch) => (
                  <option key={batch} value={batch}>
                    {batch}
                  </option>
                ))}
                <option value="ALL">All batches</option>
              </select>

              <select
                value={sortBy}
                onChange={(event) => setSortBy(event.target.value)}
                className="rounded-xl border border-[#dfe4ee] bg-white px-3 py-2.5 text-sm font-semibold outline-none focus:border-[#315bea]"
              >
                <option value="name">Sort: Name</option>
                <option value="batch">Sort: Batch</option>
                <option value="level">Sort: Level</option>
                <option value="streak">Sort: Streak</option>
                <option value="tests">Sort: Number of tests</option>
                <option value="average">Sort: Average marks</option>
                <option value="best">Sort: Best marks</option>
                <option value="accuracy">Sort: Accuracy</option>
                <option value="correct">Sort: Correct answers</option>
                <option value="wrong">Sort: Wrong answers</option>
                <option value="unanswered">Sort: Unanswered</option>
                <option value="badges">Sort: Badges</option>
                <option value="lastActive">Sort: Last active</option>
              </select>

              <button
                type="button"
                onClick={() =>
                  setSortDirection((current) =>
                    current === "asc" ? "desc" : "asc"
                  )
                }
                className="rounded-xl border border-[#dfe4ee] bg-white px-4 py-2.5 text-sm font-bold text-[#315bea] hover:bg-[#f7f9ff]"
              >
                {sortDirection === "asc" ? "↑ Ascending" : "↓ Descending"}
              </button>

              <span className="text-xs font-semibold text-[#8a93a5]">
                Showing {filteredStudents.length} of {students.length}
              </span>
            </div>
          </div>

          {loading && (
            <div className="p-8 text-sm text-[#697386]">
              Loading performance...
            </div>
          )}

          {error && (
            <div className="p-8 text-sm font-semibold text-red-600">
              {error}
            </div>
          )}

          {!loading && !error && filteredStudents.length === 0 && (
            <div className="p-10 text-center text-sm text-[#697386]">
              No students found.
            </div>
          )}

          {!loading && !error && filteredStudents.length > 0 && (
            <div className="w-full min-w-0 max-w-full">
              <p className="mb-2 flex items-center gap-2 px-4 text-xs font-semibold text-[#697386] sm:px-6">
                <span aria-hidden="true">↔</span> Scroll horizontally to view all performance columns
              </p>
              <div className="w-full max-w-full overflow-x-scroll overscroll-x-contain rounded-b-xl border-t border-[#e7ebf3] [scrollbar-gutter:stable]">
              <table className="min-w-[1280px] w-full text-left">
                <thead className="bg-[#fafbfe] text-[11px] uppercase tracking-wider text-[#8a93a5]">
                  <tr>
                    <th className="px-6 py-4 font-bold">Student</th>
                    <th className="px-4 py-4 font-bold">Batch</th>
                    <th className="px-4 py-4 text-center font-bold">Level</th>
                    <th className="px-4 py-4 text-center font-bold">Streak</th>
                    <th className="px-4 py-4 text-center font-bold">Tests</th>
                    <th className="px-4 py-4 text-center font-bold">Average</th>
                    <th className="px-4 py-4 text-center font-bold">Best</th>
                    <th className="px-4 py-4 text-center font-bold">Accuracy</th>
                    <th className="px-4 py-4 text-center font-bold">Correct</th>
                    <th className="px-4 py-4 text-center font-bold">Wrong</th>
                    <th className="px-4 py-4 text-center font-bold">Badges</th>
                    <th className="px-4 py-4 text-center font-bold">Last Active</th>
                    <th className="px-4 py-4 text-center font-bold">Parent</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#eef0f4]">
                  {filteredStudents.map((student) => (
                    <tr key={student.id} className="hover:bg-[#fafbfe]">
                      <td className="px-6 py-5">
                        <button
                          type="button"
                          onClick={() => void openAttempts(student)}
                          className="text-left"
                        >
                          <p className="font-bold text-[#172033] hover:text-[#315bea]">
                            {student.name}
                          </p>
                          <p className="mt-1 text-xs text-[#8a93a5]">
                            {student.email}
                          </p>
                          <p className="mt-1 text-[10px] font-bold text-[#315bea]">
                            View attempted tests →
                          </p>
                        </button>
                      </td>
                      <td className="px-4 py-5 text-sm text-[#697386]">
                        {student.batches}
                      </td>
                      <td className="px-4 py-5 text-center">
                        <div className="font-black text-indigo-600">L{student.level}</div>
                        <div className="text-[10px] text-slate-400">{student.levelName}</div>
                      </td>
                      <td className="px-4 py-5 text-center font-black text-orange-500">🔥 {student.currentStreak}</td>
                      <td className="px-4 py-5 text-center font-semibold">{student.testsTaken}</td>
                      <td className="px-4 py-5 text-center font-bold">
                        {student.averagePercentage}%
                      </td>
                      <td className="px-4 py-5 text-center font-bold">
                        {student.bestPercentage}%
                      </td>
                      <td className="px-4 py-5 text-center font-bold text-[#315bea]">
                        {student.accuracy}%
                      </td>
                      <td className="px-4 py-5 text-center text-sm">
                        {student.correctAnswers}
                      </td>
                      <td className="px-4 py-5 text-center text-sm">
                        {student.wrongAnswers}
                      </td>
                      <td className="px-4 py-5 text-center">
                        <button type="button" onClick={() => setBadgeStudent(student)} className="rounded-lg bg-violet-50 px-2.5 py-1.5 font-bold text-violet-700 transition hover:bg-violet-100">🏆 {student.badgesEarned}</button>
                      </td>
                      <td className="px-4 py-5 text-center text-xs font-medium text-slate-500">{student.lastActiveDate || "—"}</td>
                      <td className="px-4 py-5 text-center">
                        <div className="flex justify-center gap-2">
                          {features?.aiPerformanceSummaries && <button type="button" onClick={async () => {
                            setSending(student.id);
                            try {
                              const response = await fetch(`/api/ai/parent-summary?studentId=${encodeURIComponent(student.id)}`, { cache: "no-store" });
                              const data = await response.json();
                              if (!response.ok || !data.success) throw new Error(data.error || "Could not create summary.");
                              setReport({ studentId: student.id, text: data.summary });
                            } catch (error) { setError(error instanceof Error ? error.message : "Could not create summary."); } finally { setSending(null); }
                          }} className="rounded-lg border border-violet-200 bg-violet-50 px-2.5 py-1.5 text-[10px] font-bold text-violet-700">{sending === student.id ? "..." : "View Feedback"}</button>}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              </div>
            </div>
          )}
        </section>

        {attemptStudent && (
          <div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 p-5"
            onClick={() => setAttemptStudent(null)}
          >
            <div
              className="max-h-[85vh] w-full max-w-4xl overflow-hidden rounded-2xl bg-white shadow-2xl"
              onClick={(event) => event.stopPropagation()}
            >
              <div className="flex items-center justify-between border-b border-[#eef0f4] px-6 py-5">
                <div>
                  <h3 className="text-lg font-extrabold">
                    {attemptStudent.name}
                  </h3>
                  <p className="mt-1 text-sm text-[#8a93a5]">
                    Attempted tests
                  </p>
                </div>

                <button
                  type="button"
                  onClick={() => setAttemptStudent(null)}
                  className="rounded-lg border border-[#e2e6ee] px-3 py-1.5 text-sm font-bold text-[#697386]"
                >
                  Close
                </button>
              </div>

              <div className="max-h-[65vh] overflow-y-auto p-6">
                {attemptLoading ? (
                  <p className="text-sm text-[#697386]">
                    Loading attempted tests...
                  </p>
                ) : attemptError ? (
                  <p className="rounded-xl bg-red-50 px-4 py-3 text-sm font-semibold text-red-600">
                    {attemptError}
                  </p>
                ) : attempts.length === 0 ? (
                  <p className="rounded-xl bg-[#f7f8fc] px-4 py-5 text-center text-sm text-[#697386]">
                    No completed tests found for this student.
                  </p>
                ) : (
                  <div className="space-y-3">
                    {attempts.map((attempt, index) => {
                      const score = Number(attempt.score || 0);
                      const total = Number(attempt.total_marks || 0);
                      const correct = Number(attempt.correct_count ?? 0);
                      const wrong = Number(attempt.incorrect_count ?? 0);
                      const unanswered = Number(attempt.unanswered_count ?? 0);
                      const percentage =
                        typeof attempt.percentage === "number"
                          ? attempt.percentage.toFixed(1)
                          : total > 0
                            ? ((score / total) * 100).toFixed(1)
                            : "0.0";

                      const subjects = attempt.subjects?.length
                        ? attempt.subjects.join(", ")
                        : attempt.exam || "Subject unavailable";
                      const chapters = attempt.chapters?.length
                        ? attempt.chapters.join(", ")
                        : "Chapter unavailable";
                      const difficultyOrder = ["Easy", "Medium", "Hard", "Challenging"];

const normalizedDifficulties = [
  ...new Set(
    (attempt.difficulties ?? [])
      .flatMap((value: string) => value.split(","))
      .map((value: string) => value.trim().toLowerCase())
      .filter(Boolean)
  ),
];

const difficulties = difficultyOrder.filter((level) =>
  normalizedDifficulties.includes(level.toLowerCase())
);

const otherDifficulties = normalizedDifficulties
  .filter(
    (level) =>
      !difficultyOrder.some(
        (known) => known.toLowerCase() === level
      )
  )
  .map((level) => level.charAt(0).toUpperCase() + level.slice(1));

                      return (
                        <div
                          key={attempt.id}
                          className="rounded-xl border border-[#e7eaf0] p-4"
                        >
                          <div className="flex flex-wrap items-start justify-between gap-3">
                            <div>
                              <p className="font-bold flex items-center gap-2">
                                #{index + 1} {attempt.test_title} &middot; {subjects}
                                <span className={`inline-block rounded-full px-2 py-0.5 text-[10px] font-bold ${difficulties.length ? (difficulties.includes("Easy") ? "bg-green-100 text-green-800" : difficulties.includes("Medium") ? "bg-amber-100 text-amber-800" : difficulties.includes("Hard") ? "bg-red-100 text-red-800" : "bg-purple-100 text-purple-800") : "bg-slate-200 text-slate-700"}`}>
                                  {difficulties.length ? difficulties.join(", ") : otherDifficulties.length ? otherDifficulties.join(", ") : "—"}
                                </span>
                              </p>
                              <p className="mt-1 text-xs text-[#8a93a5]">
                                {attempt.submitted_at
                                  ? new Date(
                                      attempt.submitted_at
                                    ).toLocaleString("en-IN")
                                  : "Submission time unavailable"}
                              </p>
                            </div>

                            <div className="text-right">
                              <p className="text-lg font-black text-[#315bea]">
                                {score.toFixed(1)} / {total.toFixed(1)}
                              </p>
                              <p className="text-xs font-bold text-[#697386]">
                                {percentage}%
                              </p>
                            </div>
                          </div>

                          <div className="mt-4 grid grid-cols-1 gap-2 sm:grid-cols-2">
                            <div className="rounded-lg bg-[#f7f8fc] px-3 py-2">
                              <p className="text-[10px] font-bold uppercase tracking-wide text-[#8a93a5]">Subject</p>
                              <p className="mt-1 text-xs font-bold text-[#172033]">{subjects}</p>
                            </div>
                            <div className="rounded-lg bg-[#f7f8fc] px-3 py-2">
                              <p className="text-[10px] font-bold uppercase tracking-wide text-[#8a93a5]">Chapter</p>
                              <p className="mt-1 text-xs font-bold text-[#172033]">{chapters}</p>
                            </div>
                            <div className="rounded-lg bg-[#f7f8fc] px-3 py-2">
  <p className="text-[10px] font-bold uppercase tracking-wide text-[#8a93a5]">
    Difficulty levels
  </p>

  {difficulties.length === 0 && otherDifficulties.length === 0 ? (
    <p className="mt-2 text-xs font-medium text-[#697386]">
      Difficulty unavailable
    </p>
  ) : (
    <div className="mt-2 flex flex-wrap gap-1.5">
      {difficulties.map((level) => (
        <span
          key={level}
          className={`rounded-full px-2 py-1 text-[11px] font-bold ${
            level === "Easy"
              ? "bg-green-100 text-green-800"
              : level === "Medium"
                ? "bg-amber-100 text-amber-800"
                : level === "Hard"
                  ? "bg-red-100 text-red-800"
                  : "bg-purple-100 text-purple-800"
          }`}
        >
          {level}
        </span>
      ))}

      {otherDifficulties.map((level) => (
        <span
          key={level}
          className="rounded-full bg-slate-200 px-2 py-1 text-[11px] font-bold text-slate-700"
        >
          {level}
        </span>
      ))}
    </div>
  )}
</div>
                            <div className="rounded-lg bg-[#f7f8fc] px-3 py-2">
                              <p className="text-[10px] font-bold uppercase tracking-wide text-[#8a93a5]">Questions</p>
                              <p className="mt-1 text-xs font-bold text-[#172033]">{attempt.question_count ?? "—"}</p>
                            </div>
                          </div>

                          <div className="mt-3 flex flex-wrap gap-4 text-xs font-semibold text-[#697386]">
                            <span>✓ Correct: {correct}</span>
                            <span>✕ Wrong: {wrong}</span>
                            <span>— Unanswered: {unanswered}</span>
                            {attempt.question_types?.length ? (
                              <span>Type: {attempt.question_types.join(", ")}</span>
                            ) : null}
                          </div>

                          <div className="mt-4 flex justify-end">
                            <button
                              type="button"
                              onClick={() => router.push(`/test/${attempt.test_id}`)}
                              className="rounded-lg border border-[#315bea] px-3 py-1.5 text-xs font-bold text-[#315bea] hover:bg-[#315bea] hover:text-white transition"
                            >
                              View Test
                            </button>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {badgeStudent && (
          <StudentBadgeModal
            studentId={badgeStudent.id}
            studentName={badgeStudent.name}
            onClose={() => setBadgeStudent(null)}
          />
        )}

        {report && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 p-5" onClick={() => setReport(null)}>
            <div className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl" onClick={(event) => event.stopPropagation()}>
              <div className="flex items-center justify-between"><h3 className="text-lg font-extrabold">AI Parent Summary</h3><button onClick={() => setReport(null)} className="text-sm font-bold text-[#697386]">Close</button></div>
              <p className="mt-5 whitespace-pre-wrap rounded-xl bg-[#f7f8fc] p-4 text-sm leading-6 text-[#475168]">{report.text}</p>
              <div className="mt-4 flex items-center gap-3">
                <button type="button" onClick={() => navigator.clipboard?.writeText(report.text)} className="rounded-xl bg-[#315bea] px-4 py-2.5 text-sm font-bold text-white">Copy Summary</button>
                <button type="button" onClick={() => {
                  const text = encodeURIComponent(report.text || "");
                  window.open(`https://wa.me/?text=${text}`, "_blank", "noopener,noreferrer");
                }} className="rounded-xl bg-[#25D366] px-4 py-2.5 text-sm font-bold text-white">Share via WhatsApp</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
