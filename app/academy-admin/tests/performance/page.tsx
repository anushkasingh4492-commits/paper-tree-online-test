"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

type Student = {
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
  level: number;
  levelName: string;
  currentStreak: number;
  lastActiveDate: string | null;
  badgesEarned: number;
};

type Attempt = {
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
};

type SortKey =
  | "name"
  | "averagePercentage"
  | "testsTaken"
  | "bestPercentage"
  | "accuracy"
  | "correctAnswers"
  | "wrongAnswers"
  | "unansweredQuestions"
  | "level"
  | "currentStreak"
  | "badgesEarned"
  | "lastActiveDate";

export default function AcademyAdminPerformancePage() {
  const router = useRouter();
  const [students, setStudents] = useState<Student[]>([]);
  const [search, setSearch] = useState("");
  const [batch, setBatch] = useState("ALL");
  const [sortKey, setSortKey] = useState<SortKey>("name");
  const [direction, setDirection] = useState<"asc" | "desc">("asc");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [attemptStudent, setAttemptStudent] = useState<Student | null>(null);
  const [attempts, setAttempts] = useState<Attempt[]>([]);
  const [attemptLoading, setAttemptLoading] = useState(false);

  async function loadStudents() {
    setLoading(true);
    setError("");
    try {
      const response = await fetch("/api/academy-admin/performance", {
        cache: "no-store",
        credentials: "include",
      });
      const data = await response.json();
      if (!response.ok || !data.success) {
        throw new Error(data.error || "Could not load student performance.");
      }
      setStudents(data.students || []);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Could not load student performance.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadStudents();
  }, []);

  const batches = useMemo(() => {
    const values = new Set<string>();
    students.forEach((student) => {
      String(student.batches || "")
        .split(",")
        .map((value) => value.trim())
        .filter(Boolean)
        .forEach((value) => values.add(value));
    });
    return Array.from(values).sort((a, b) => a.localeCompare(b));
  }, [students]);

  const filtered = useMemo(() => {
    const query = search.trim().toLowerCase();
    const list = students.filter((student) => {
      const matchesSearch =
        !query ||
        [student.name, student.email, student.batches].some((value) =>
          String(value || "").toLowerCase().includes(query)
        );
      const matchesBatch =
        batch === "ALL" ||
        String(student.batches || "")
          .split(",")
          .map((value) => value.trim())
          .includes(batch);
      return matchesSearch && matchesBatch;
    });

    const valueForSort = (student: Student): string | number => {
      if (sortKey === "name") return student.name.toLowerCase();
      if (sortKey === "lastActiveDate") return student.lastActiveDate || "";
      return Number(student[sortKey] || 0);
    };

    return list.sort((a, b) => {
      const left = valueForSort(a);
      const right = valueForSort(b);
      const result =
        typeof left === "string" && typeof right === "string"
          ? left.localeCompare(right)
          : Number(left) - Number(right);
      return direction === "asc" ? result : -result;
    });
  }, [students, search, batch, sortKey, direction]);

  function changeSort(next: SortKey) {
    if (sortKey === next) {
      setDirection((current) => (current === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(next);
      setDirection("asc");
    }
  }

  async function openAttempts(student: Student) {
    setAttemptStudent(student);
    setAttempts([]);
    setAttemptLoading(true);
    try {
      const response = await fetch(
        `/api/academy-admin/performance?studentId=${encodeURIComponent(student.id)}`,
        { cache: "no-store", credentials: "include" }
      );
      const data = await response.json();
      if (!response.ok || !data.success) {
        throw new Error(data.error || "Could not load attempted tests.");
      }
      setAttempts(data.attempts || []);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Could not load attempted tests.");
    } finally {
      setAttemptLoading(false);
    }
  }

  useEffect(() => {
    void fetch("/api/academy/branding", { cache: "no-store", credentials: "include" })
      .then((response) => response.json())
      .then((data) => {
        const name = data?.success ? String(data?.academy?.name || "").trim() : "";
        document.title = name ? `${name} CBT` : "CBT";
      })
      .catch(() => undefined);
  }, []);

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <header className="border-b border-[#e7eaf0] bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-6 py-5">
          <div>
            <p className="text-xs font-black tracking-[.16em] text-[#315bea]">ACADEMY ADMIN</p>
            <h1 className="mt-1 text-2xl font-extrabold">Student Performance</h1>
            <p className="mt-1 text-sm text-[#697386]">Review every student&apos;s completed tests and performance in your academy.</p>
          </div>
          <button
            onClick={() => router.push("/academy-admin")}
            className="rounded-xl border border-[#e2e6ee] bg-white px-4 py-2.5 text-sm font-bold text-[#315bea]"
          >
            ← Dashboard
          </button>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-8">
        {error && (
          <div className="mb-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
            {error}
          </div>
        )}

        <section className="rounded-2xl border border-[#e3e8f5] bg-white p-5 shadow-sm">
          <div className="grid gap-3 lg:grid-cols-[1fr_220px_220px]">
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search student, email or batch"
              className="rounded-xl border border-[#dfe4ed] px-4 py-3 text-sm outline-none focus:border-[#315bea]"
            />
            <select
              value={batch}
              onChange={(event) => setBatch(event.target.value)}
              className="rounded-xl border border-[#dfe4ed] px-4 py-3 text-sm"
            >
              <option value="ALL">All batches</option>
              {batches.map((value) => <option key={value} value={value}>{value}</option>)}
            </select>
            <select
              value={sortKey}
              onChange={(event) => changeSort(event.target.value as SortKey)}
              className="rounded-xl border border-[#dfe4ed] px-4 py-3 text-sm"
            >
              <option value="name">Name</option>
              <option value="averagePercentage">Average %</option>
              <option value="testsTaken">Tests taken</option>
              <option value="bestPercentage">Best %</option>
              <option value="accuracy">Accuracy</option>
              <option value="correctAnswers">Correct</option>
              <option value="wrongAnswers">Wrong</option>
              <option value="unansweredQuestions">Unanswered</option>
              <option value="level">Level</option>
              <option value="currentStreak">Streak</option>
              <option value="badgesEarned">Badges</option>
              <option value="lastActiveDate">Last active</option>
            </select>
          </div>

          <div className="mt-4 flex items-center justify-between text-xs font-bold text-[#697386]">
            <span>{filtered.length} students shown</span>
            <button
              onClick={() => setDirection((current) => (current === "asc" ? "desc" : "asc"))}
              className="rounded-lg border border-[#e2e6ee] px-3 py-1.5 text-[#315bea]"
            >
              {direction === "asc" ? "Ascending ↑" : "Descending ↓"}
            </button>
          </div>
        </section>

        <section className="mt-5 overflow-hidden rounded-2xl border border-[#e3e8f5] bg-white shadow-sm">
          {loading ? (
            <div className="p-10 text-center text-sm font-semibold text-[#697386]">Loading performance…</div>
          ) : filtered.length === 0 ? (
            <div className="p-10 text-center text-sm font-semibold text-[#697386]">No students match the current filters.</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-[1250px] w-full text-left text-sm">
                <thead className="bg-[#f7f8fc] text-[11px] uppercase tracking-wider text-[#697386]">
                  <tr>
                    {[
                      ["name", "Student"],
                      ["testsTaken", "Tests"],
                      ["averagePercentage", "Avg %"],
                      ["bestPercentage", "Best %"],
                      ["accuracy", "Accuracy"],
                      ["correctAnswers", "Correct"],
                      ["wrongAnswers", "Wrong"],
                      ["unansweredQuestions", "Unanswered"],
                      ["level", "Level"],
                      ["currentStreak", "Streak"],
                      ["badgesEarned", "Badges"],
                      ["lastActiveDate", "Last active"],
                    ].map(([key, label]) => (
                      <th key={key} className="px-4 py-3">
                        <button onClick={() => changeSort(key as SortKey)} className="font-black hover:text-[#315bea]">
                          {label} {sortKey === key ? (direction === "asc" ? "↑" : "↓") : ""}
                        </button>
                      </th>
                    ))}
                    <th className="px-4 py-3">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((student) => (
                    <tr key={student.id} className="border-t border-[#eef0f4] hover:bg-[#fbfcff]">
                      <td className="px-4 py-4">
                        <button onClick={() => openAttempts(student)} className="text-left">
                          <p className="font-extrabold text-[#172033]">{student.name}</p>
                          <p className="mt-0.5 text-xs text-[#697386]">{student.email}</p>
                          <p className="mt-0.5 text-[11px] text-[#315bea]">{student.batches}</p>
                        </button>
                      </td>
                      <td className="px-4 py-4 font-bold">{student.testsTaken}</td>
                      <td className="px-4 py-4 font-bold">{student.averagePercentage.toFixed(2)}%</td>
                      <td className="px-4 py-4 font-bold">{student.bestPercentage.toFixed(2)}%</td>
                      <td className="px-4 py-4 font-bold">{student.accuracy.toFixed(2)}%</td>
                      <td className="px-4 py-4">{student.correctAnswers}</td>
                      <td className="px-4 py-4">{student.wrongAnswers}</td>
                      <td className="px-4 py-4">{student.unansweredQuestions}</td>
                      <td className="px-4 py-4">{student.level} · {student.levelName}</td>
                      <td className="px-4 py-4">{student.currentStreak}d</td>
                      <td className="px-4 py-4">{student.badgesEarned}</td>
                      <td className="px-4 py-4">{student.lastActiveDate ? new Date(student.lastActiveDate).toLocaleDateString("en-IN") : "—"}</td>
                      <td className="px-4 py-4">
                        <button onClick={() => openAttempts(student)} className="rounded-lg bg-[#315bea] px-3 py-2 text-xs font-bold text-white">
                          View tests
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>

      {attemptStudent && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" onClick={() => setAttemptStudent(null)}>
          <div className="max-h-[85vh] w-full max-w-5xl overflow-auto rounded-3xl bg-white p-6 shadow-2xl" onClick={(event) => event.stopPropagation()}>
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs font-black tracking-wider text-[#315bea]">COMPLETED TESTS</p>
                <h2 className="mt-1 text-2xl font-extrabold">{attemptStudent.name}</h2>
                <p className="text-sm text-[#697386]">{attemptStudent.email}</p>
              </div>
              <button onClick={() => setAttemptStudent(null)} className="rounded-xl border px-3 py-2 text-sm font-bold">Close</button>
            </div>

            {attemptLoading ? (
              <div className="py-12 text-center text-sm font-semibold text-[#697386]">Loading attempted tests…</div>
            ) : attempts.length === 0 ? (
              <div className="py-12 text-center text-sm font-semibold text-[#697386]">No completed tests found.</div>
            ) : (
              <div className="mt-6 overflow-x-auto">
                <table className="min-w-[850px] w-full text-left text-sm">
                  <thead className="bg-[#f7f8fc] text-[11px] uppercase tracking-wider text-[#697386]">
                    <tr>
                      <th className="px-3 py-3">Test</th>
                      <th className="px-3 py-3">Marks</th>
                      <th className="px-3 py-3">%</th>
                      <th className="px-3 py-3">Correct</th>
                      <th className="px-3 py-3">Wrong</th>
                      <th className="px-3 py-3">Unanswered</th>
                      <th className="px-3 py-3">Submitted</th>
                    </tr>
                  </thead>
                  <tbody>
                    {attempts.map((attempt) => {
                      const score = Number(attempt.score || 0);
                      const total = Number(attempt.total_marks || 0);
                      const percentage = total > 0 ? (score / total) * 100 : 0;
                      return (
                        <tr key={attempt.id} className="border-t border-[#eef0f4]">
                          <td className="px-3 py-3 font-bold">{attempt.test_title}</td>
                          <td className="px-3 py-3">{score} / {total}</td>
                          <td className="px-3 py-3 font-bold">{percentage.toFixed(2)}%</td>
                          <td className="px-3 py-3">{attempt.correct_count ?? 0}</td>
                          <td className="px-3 py-3">{attempt.incorrect_count ?? 0}</td>
                          <td className="px-3 py-3">{attempt.unanswered_count ?? 0}</td>
                          <td className="px-3 py-3">{attempt.submitted_at ? new Date(attempt.submitted_at).toLocaleString("en-IN") : "—"}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}
    </main>
  );
}
