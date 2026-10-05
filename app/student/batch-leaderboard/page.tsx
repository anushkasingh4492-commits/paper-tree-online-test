"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import StudentBadgeModal from "@/components/StudentBadgeModal";

 type LeaderboardStudent = {
  id: string;
  name: string;
  average: number;
  testsTaken: number;
  questionsSeen: number;
  rank: number;
  isCurrent: boolean;
};

type LeaderboardResponse = {
  success?: boolean;
  error?: string;
  batch?: { id: string; name: string; size: number } | null;
  students?: LeaderboardStudent[];
  currentStudent?: LeaderboardStudent | null;
};

export default function BatchLeaderboardPage() {
  const router = useRouter();
  const [data, setData] = useState<LeaderboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [badgeStudent, setBadgeStudent] = useState<LeaderboardStudent | null>(null);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const response = await fetch("/api/student/batch-leaderboard", { cache: "no-store" });
        const payload = (await response.json()) as LeaderboardResponse;
        if (!response.ok || payload.success === false) throw new Error(payload.error || "Could not load leaderboard.");
        if (active) setData(payload);
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Could not load leaderboard.");
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => { active = false; };
  }, []);

  const students = data?.students ?? [];
  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    if (!needle) return students;
    return students.filter((student) => student.name.toLowerCase().includes(needle));
  }, [students, query]);

  const topThree = [1, 2, 3]
    .map((rank) => students.find((student) => student.rank === rank))
    .filter((student): student is LeaderboardStudent => Boolean(student));
  const current = data?.currentStudent ?? null;

  return (
    <main className="min-h-screen bg-[#070b18] text-white overflow-hidden">
      <div className="fixed inset-0 pointer-events-none bg-[radial-gradient(circle_at_20%_10%,rgba(99,102,241,.20),transparent_30%),radial-gradient(circle_at_85%_20%,rgba(14,165,233,.16),transparent_28%),radial-gradient(circle_at_50%_90%,rgba(168,85,247,.13),transparent_32%)]" />

      <div className="relative min-h-screen max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 lg:py-10">
        <header className="flex items-center justify-between gap-4 mb-8">
          <div>
            <button onClick={() => router.push("/dashboard")} className="text-xs text-white/50 hover:text-white mb-3 transition">← Back to dashboard</button>
            <div className="flex items-center gap-3">
              <div className="h-12 w-12 rounded-2xl bg-gradient-to-br from-yellow-300 via-orange-400 to-pink-500 flex items-center justify-center text-2xl shadow-[0_0_35px_rgba(251,146,60,.35)]">🏆</div>
              <div>
                <h1 className="text-2xl sm:text-3xl font-black tracking-tight">Batch Leaderboard</h1>
                <p className="text-sm text-white/50">Compete, improve, and climb your batch.</p>
              </div>
            </div>
          </div>
          {data?.batch && (
            <div className="hidden sm:block rounded-2xl border border-white/10 bg-white/[.06] px-4 py-3 text-right backdrop-blur-xl">
              <div className="text-[10px] uppercase tracking-[.18em] text-white/40">Your Batch</div>
              <div className="font-bold mt-1">{data.batch.name}</div>
              <div className="text-xs text-white/40">{data.batch.size} students</div>
            </div>
          )}
        </header>

        {loading ? (
          <div className="grid gap-4 md:grid-cols-3">
            {[1,2,3].map((i) => <div key={i} className="h-48 rounded-3xl bg-white/[.06] animate-pulse" />)}
          </div>
        ) : error ? (
          <div className="rounded-3xl border border-red-400/20 bg-red-500/10 p-6 text-sm text-red-200">{error}</div>
        ) : !data?.batch ? (
          <div className="rounded-3xl border border-white/10 bg-white/[.05] p-10 text-center">
            <div className="text-5xl mb-4">🎮</div>
            <h2 className="text-xl font-black">No batch assigned yet</h2>
            <p className="text-sm text-white/45 mt-2">Your leaderboard will appear here once you are added to a batch.</p>
          </div>
        ) : (
          <>
            {current && (
              <section className="relative overflow-hidden rounded-[30px] border border-indigo-300/15 bg-gradient-to-r from-indigo-500/20 via-purple-500/15 to-cyan-500/10 p-5 sm:p-7 mb-7 shadow-[0_25px_80px_rgba(30,41,100,.25)]">
                <div className="absolute -right-16 -top-20 h-52 w-52 rounded-full bg-indigo-400/15 blur-3xl" />
                <div className="relative flex flex-col sm:flex-row sm:items-center justify-between gap-5">
                  <div>
                    <div className="text-[10px] uppercase tracking-[.2em] font-black text-indigo-200/70">Your position</div>
                    <div className="flex items-end gap-3 mt-1">
                      <span className="text-5xl font-black">#{current.rank}</span>
                      <span className="text-sm text-white/45 mb-2">of {students.length}</span>
                    </div>
                    <div className="mt-3 text-sm text-white/65">Average score <b className="text-white">{current.average}%</b> across {current.testsTaken} completed tests.</div>
                  </div>
                  <div className="flex gap-3">
                    <Stat label="Average" value={`${current.average}%`} />
                    <Stat label="Tests" value={String(current.testsTaken)} />
                  </div>
                </div>
              </section>
            )}

            <section className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end mb-8">
              {[1, 2, 3].map((rank) => {
                const student = topThree.find((item) => item.rank === rank);
                if (!student) return <div key={rank} className="hidden md:block" />;
                return <Podium key={student.id} student={student} place={rank} onViewBadges={() => setBadgeStudent(student)} />;
              })}
            </section>

            <section className="rounded-[28px] border border-white/10 bg-white/[.045] backdrop-blur-xl overflow-hidden">
              <div className="p-5 sm:p-6 border-b border-white/10 flex flex-col sm:flex-row gap-4 sm:items-center justify-between">
                <div>
                  <h2 className="font-black text-lg">All Players</h2>
                  <p className="text-xs text-white/40 mt-1">Rank is based on average completed-test percentage.</p>
                </div>
                <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search student..." className="w-full sm:w-56 h-10 rounded-xl bg-white/[.06] border border-white/10 px-3 text-sm outline-none focus:border-indigo-400/50 placeholder:text-white/25" />
              </div>

              <div className="divide-y divide-white/[.06]">
                {filtered.map((student) => (
                  <div key={student.id} className={`grid grid-cols-[52px_1fr_auto] sm:grid-cols-[64px_1fr_110px_90px] gap-3 items-center px-4 sm:px-6 py-4 transition ${student.isCurrent ? "bg-indigo-500/[.12]" : "hover:bg-white/[.025]"}`}>
                    <div className={`text-center font-black ${student.rank <= 3 ? "text-xl" : "text-sm text-white/45"}`}>{student.rank <= 3 ? ["🥇","🥈","🥉"][student.rank-1] : `#${student.rank}`}</div>
                    <div className="min-w-0 flex items-center justify-between gap-2">
                      <div className="min-w-0">
                        <div className="font-bold truncate">{student.name} {student.isCurrent && <span className="ml-2 text-[9px] uppercase tracking-wider text-indigo-300 bg-indigo-400/10 px-2 py-1 rounded-full">You</span>}</div>
                        <div className="text-[11px] text-white/35 mt-1">{student.testsTaken} tests · {student.questionsSeen} questions</div>
                      </div>
                      <button type="button" onClick={() => setBadgeStudent(student)} className="shrink-0 rounded-lg bg-violet-400/10 px-2 py-1 text-[10px] font-bold text-violet-200 sm:hidden">🏆</button>
                    </div>
                    <div className="hidden sm:block text-right"><div className="font-black">{student.average}%</div><div className="text-[10px] text-white/30">average</div></div>
                    <div className="hidden sm:flex items-center justify-end gap-3 text-xs text-white/40">
                      <button type="button" onClick={() => setBadgeStudent(student)} className="rounded-lg bg-violet-400/10 px-2.5 py-1.5 font-bold text-violet-200 transition hover:bg-violet-400/20">🏆 Badges</button>
                      <span>Rank {student.rank}</span>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </>
        )}
        {badgeStudent && (
          <StudentBadgeModal
            studentId={badgeStudent.id}
            studentName={badgeStudent.name}
            onClose={() => setBadgeStudent(null)}
          />
        )}
      </div>
    </main>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return <div className="min-w-[88px] rounded-2xl border border-white/10 bg-black/10 px-4 py-3"><div className="text-[9px] uppercase tracking-widest text-white/35">{label}</div><div className="font-black text-lg mt-1">{value}</div></div>;
}

function Podium({ student, place, onViewBadges }: { student: LeaderboardStudent; place: number; onViewBadges: () => void }) {
  const medal = place === 1 ? "🥇" : place === 2 ? "🥈" : "🥉";
  const height = place === 1 ? "h-52" : place === 2 ? "h-44" : "h-40";
  return (
    <div className={`relative ${height} rounded-[28px] border ${student.isCurrent ? "border-indigo-300/40" : "border-white/10"} bg-white/[.06] p-5 flex flex-col justify-end text-center overflow-hidden ${place === 1 ? "shadow-[0_0_50px_rgba(250,204,21,.12)]" : ""}`}>
      <div className="absolute inset-x-0 top-0 h-20 bg-gradient-to-b from-white/[.06] to-transparent" />
      <div className="relative text-4xl mb-2">{medal}</div>
      <div className="relative font-black truncate">{student.name?.trim() || "Student"}</div>
      <div className="relative text-2xl font-black mt-1">{student.average}%</div>
      <div className="relative text-[10px] uppercase tracking-widest text-white/35 mt-1">#{student.rank} · {student.testsTaken} tests</div>
      <button type="button" onClick={onViewBadges} className="relative mx-auto mt-3 rounded-lg bg-violet-400/10 px-3 py-1.5 text-[10px] font-black text-violet-200 hover:bg-violet-400/20">🏆 View badges</button>
    </div>
  );
}
