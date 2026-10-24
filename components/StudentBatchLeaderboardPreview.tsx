"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import StudentBadgeModal from "@/components/StudentBadgeModal";

type LeaderboardStudent = {
  id: string;
  name: string;
  average: number;
  testsTaken: number;
  rank: number;
  isCurrent: boolean;
};

type LeaderboardData = {
  success?: boolean;
  error?: string;
  batch?: { id: string; name: string; size: number } | null;
  students?: LeaderboardStudent[];
  currentStudent?: LeaderboardStudent | null;
};

export default function StudentBatchLeaderboardPreview() {
  const router = useRouter();
  const [data, setData] = useState<LeaderboardData | null>(null);
  const [error, setError] = useState("");
  const [badgeStudent, setBadgeStudent] = useState<LeaderboardStudent | null>(
    null
  );

  useEffect(() => {
    let active = true;

    fetch("/api/student/batch-leaderboard", {
      cache: "no-store",
      credentials: "include",
    })
      .then(async (response) => {
        const payload = (await response.json()) as LeaderboardData;
        if (!response.ok || !payload.success) {
          throw new Error(payload.error || "Could not load your batch.");
        }
        if (active) setData(payload);
      })
      .catch((reason: unknown) => {
        if (active) {
          setError(
            reason instanceof Error
              ? reason.message
              : "Could not load your batch."
          );
        }
      });

    return () => {
      active = false;
    };
  }, []);

  const batch = data?.batch;
  const students = data?.students ?? [];
  const currentStudent = data?.currentStudent;
  const topThree = [1, 2, 3]
    .map((rank) => students.find((student) => student.rank === rank))
    .filter((student): student is LeaderboardStudent => Boolean(student));

  return (
    <section className="mt-5 overflow-hidden rounded-[14px] border border-[#e8eaf0] bg-white shadow-[0_3px_12px_rgba(30,35,60,.035)]">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[#eff0f4] px-5 py-4">
        <div>
          <h2 className="text-[14px] font-extrabold text-[#172033]">
            Your Batch
          </h2>
          <p className="mt-1 text-[10px] text-[#939aa8]">
            {batch
              ? `${batch.name} · ${batch.size} students`
              : "Your position and top performers"}
          </p>
        </div>
        <button
          type="button"
          onClick={() => router.push("/student/batch-leaderboard")}
          className="rounded-lg border border-[#dedaff] px-3 py-2 text-[10px] font-bold text-[#5541dd] transition hover:bg-[#f7f5ff]"
        >
          View leaderboard →
        </button>
      </div>

      {error ? (
        <p role="alert" className="px-5 py-4 text-xs font-semibold text-rose-600">
          {error}
        </p>
      ) : !data ? (
        <div className="grid gap-3 p-5 sm:grid-cols-3" aria-label="Loading batch leaderboard">
          {[1, 2, 3].map((item) => (
            <div
              key={item}
              className="h-20 animate-pulse rounded-xl bg-slate-100"
            />
          ))}
        </div>
      ) : !batch ? (
        <p className="px-5 py-6 text-center text-xs text-[#697386]">
          You haven&apos;t been assigned to a batch yet.
        </p>
      ) : (
        <>
          <div className="grid gap-3 border-b border-[#eff0f4] p-5 sm:grid-cols-3">
            <SummaryCard
              label="Your Position"
              value={currentStudent ? `#${currentStudent.rank}` : "—"}
              detail={
                currentStudent
                  ? `${currentStudent.average}% average`
                  : "Complete a test to appear"
              }
              tone="text-indigo-600"
            />
            <SummaryCard
              label="Completed Tests"
              value={String(currentStudent?.testsTaken ?? 0)}
              detail="In your batch"
              tone="text-emerald-600"
            />
            <SummaryCard
              label="Batch Students"
              value={String(batch.size)}
              detail={batch.name}
              tone="text-fuchsia-600"
            />
          </div>

          <div className="grid gap-3 p-5 md:grid-cols-3">
            {topThree.length ? (
              topThree.map((student) => (
                <article
                  key={student.id}
                  className={`flex items-center gap-3 rounded-xl border p-3 ${
                    student.isCurrent
                      ? "border-indigo-200 bg-indigo-50/70"
                      : "border-[#edf0f4] bg-[#fafbfc]"
                  }`}
                >
                  <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-white text-lg shadow-sm">
                    {["🥇", "🥈", "🥉"][student.rank - 1] ?? `#${student.rank}`}
                  </span>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-xs font-extrabold text-[#263148]">
                      {student.name}
                      {student.isCurrent ? " · You" : ""}
                    </p>
                    <p className="mt-1 text-[10px] text-[#7b8495]">
                      {student.average}% average · {student.testsTaken} tests
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={() => setBadgeStudent(student)}
                    className="shrink-0 text-[9px] font-bold text-[#5541dd] hover:underline"
                  >
                    View badges
                  </button>
                </article>
              ))
            ) : (
              <p className="text-xs text-[#697386] md:col-span-3">
                Complete a test to help your batch leaderboard take shape.
              </p>
            )}
          </div>
        </>
      )}

      {badgeStudent && (
        <StudentBadgeModal
          studentId={badgeStudent.id}
          studentName={badgeStudent.name}
          onClose={() => setBadgeStudent(null)}
        />
      )}
    </section>
  );
}

function SummaryCard({
  label,
  value,
  detail,
  tone,
}: {
  label: string;
  value: string;
  detail: string;
  tone: string;
}) {
  return (
    <div className="rounded-xl border border-[#edf0f4] bg-[#fafbfc] p-4">
      <p className="text-[9px] font-bold uppercase tracking-wider text-[#939aa8]">
        {label}
      </p>
      <p className={`mt-1 text-2xl font-extrabold ${tone}`}>{value}</p>
      <p className="mt-1 truncate text-[10px] text-[#7b8495]">{detail}</p>
    </div>
  );
}
