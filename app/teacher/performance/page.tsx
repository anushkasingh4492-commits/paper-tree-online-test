"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

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

export default function TeacherPerformancePage() {
  const router = useRouter();
  const [students, setStudents] = useState<StudentPerformance[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [sending, setSending] = useState<string | null>(null);
  const [report, setReport] = useState<{ studentId: string; text: string } | null>(null);

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

  const filteredStudents = useMemo(() => {
    const query = search.trim().toLowerCase();
    if (!query) return students;

    return students.filter((student) =>
      [student.name, student.email, student.batches].some((value) =>
        value.toLowerCase().includes(query)
      )
    );
  }, [students, search]);

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

        <section className="rounded-2xl border border-[#e3e8f5] bg-white shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#eef0f4] px-6 py-5">
            <div>
              <h2 className="text-lg font-extrabold">All Students</h2>
              <p className="mt-1 text-sm text-[#8a93a5]">
                Completed tests are used for the performance metrics.
              </p>
            </div>

            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search student or batch"
              className="w-full max-w-xs rounded-xl border border-[#dfe4ee] px-4 py-2.5 text-sm outline-none focus:border-[#315bea]"
            />
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
            <div className="overflow-x-auto">
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
                        <p className="font-bold">{student.name}</p>
                        <p className="mt-1 text-xs text-[#8a93a5]">
                          {student.email}
                        </p>
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
                      <td className="px-4 py-5 text-center font-bold text-violet-600">🏆 {student.badgesEarned}</td>
                      <td className="px-4 py-5 text-center text-xs text-slate-500">{student.lastActiveDate || "—"}</td>
                      <td className="px-4 py-5 text-center">
                        <div className="flex justify-center gap-2">
                          <button type="button" onClick={async () => {
                            setSending(student.id);
                            try {
                              const response = await fetch(`/api/ai/parent-summary?studentId=${encodeURIComponent(student.id)}`, { cache: "no-store" });
                              const data = await response.json();
                              if (!response.ok || !data.success) throw new Error(data.error || "Could not create summary.");
                              setReport({ studentId: student.id, text: data.summary });
                            } catch (error) { setError(error instanceof Error ? error.message : "Could not create summary."); } finally { setSending(null); }
                          }} className="rounded-lg border border-violet-200 bg-violet-50 px-2.5 py-1.5 text-[10px] font-bold text-violet-700">{sending === student.id ? "..." : "AI Summary"}</button>
                          <button type="button" onClick={async () => {
                            setSending(student.id);
                            try {
                              const response = await fetch("/api/whatsapp/report", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ studentId: student.id }) });
                              const data = await response.json();
                              if (!response.ok || !data.success) throw new Error(data.error || "Could not create report.");
                              if (data.sent) alert("WhatsApp report sent."); else window.open(data.clickToChat, "_blank", "noopener,noreferrer");
                            } catch (error) { setError(error instanceof Error ? error.message : "Could not create WhatsApp report."); } finally { setSending(null); }
                          }} className="rounded-lg bg-[#25D366] px-2.5 py-1.5 text-[10px] font-bold text-white">WhatsApp</button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        {report && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 p-5" onClick={() => setReport(null)}>
            <div className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl" onClick={(event) => event.stopPropagation()}>
              <div className="flex items-center justify-between"><h3 className="text-lg font-extrabold">AI Parent Summary</h3><button onClick={() => setReport(null)} className="text-sm font-bold text-[#697386]">Close</button></div>
              <p className="mt-5 whitespace-pre-wrap rounded-xl bg-[#f7f8fc] p-4 text-sm leading-6 text-[#475168]">{report.text}</p>
              <button type="button" onClick={() => navigator.clipboard?.writeText(report.text)} className="mt-4 rounded-xl bg-[#315bea] px-4 py-2.5 text-sm font-bold text-white">Copy Summary</button>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
