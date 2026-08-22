
"use client";

import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const router = useRouter();

  return (
    <main className="min-h-screen bg-[#f8fafc] text-[#0f172a]">
      {/* Top navigation */}
      <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/95 backdrop-blur">
        <div className="mx-auto flex h-[72px] max-w-[1400px] items-center justify-between px-6 lg:px-10">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#2563eb] text-lg font-bold text-white shadow-sm">
              P
            </div>

            <div>
              <div className="text-[17px] font-bold tracking-tight">
                Paper Tree
              </div>
              <div className="text-[11px] font-medium text-slate-400">
                ONLINE TEST
              </div>
            </div>
          </div>

          <nav className="hidden items-center gap-8 md:flex">
            <button className="text-sm font-semibold text-[#2563eb]">
              Dashboard
            </button>

            <button
              onClick={() => router.push("/history")}
              className="text-sm font-medium text-slate-500 transition hover:text-slate-900"
            >
              My Tests
            </button>
          </nav>

          <div className="flex items-center gap-3">
            <div className="hidden text-right sm:block">
              <p className="text-sm font-semibold text-slate-800">
                Student
              </p>
              <p className="text-xs text-slate-400">
                MHT-CET Preparation
              </p>
            </div>

            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 text-sm font-bold text-blue-700">
              S
            </div>
          </div>
        </div>
      </header>

      {/* Main */}
      <div className="mx-auto max-w-[1400px] px-6 py-10 lg:px-10 lg:py-14">
        {/* Welcome */}
        <section className="mb-10">
          <p className="mb-2 text-sm font-semibold text-[#2563eb]">
            Student Dashboard
          </p>

          <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Ready for your next test?
          </h1>

          <p className="mt-3 max-w-xl text-[15px] leading-7 text-slate-500">
            Build a practice test from the real MHT-CET question bank and
            challenge yourself with questions selected for your preparation.
          </p>
        </section>

        {/* Main test card */}
        <section className="relative overflow-hidden rounded-[28px] bg-[#2563eb] shadow-xl shadow-blue-100">
          <div className="absolute -right-24 -top-24 h-72 w-72 rounded-full bg-white/10" />
          <div className="absolute -bottom-32 right-32 h-80 w-80 rounded-full bg-white/5" />

          <div className="relative grid gap-10 p-7 sm:p-10 lg:grid-cols-[1fr_320px] lg:p-12">
            <div className="flex flex-col justify-center">
              <div className="mb-5 inline-flex w-fit items-center rounded-full bg-white/15 px-3 py-1.5 text-xs font-semibold text-white">
                MHT-CET • 2026
              </div>

              <h2 className="max-w-xl text-3xl font-bold tracking-tight text-white sm:text-4xl">
                Practice smarter.
                <br />
                Test yourself.
              </h2>

              <p className="mt-5 max-w-xl text-sm leading-7 text-blue-100 sm:text-[15px]">
                Create a custom CBT test by selecting subjects, chapters,
                difficulty, number of questions and duration.
              </p>

              <div className="mt-7 flex flex-wrap gap-2">
                {["Physics", "Chemistry", "Mathematics", "Biology"].map(
                  (subject) => (
                    <span
                      key={subject}
                      className="rounded-lg border border-white/20 bg-white/10 px-3 py-2 text-xs font-medium text-white"
                    >
                      {subject}
                    </span>
                  )
                )}
              </div>

              <button
                onClick={() => router.push("/create-test")}
                className="mt-9 flex h-12 w-fit items-center gap-3 rounded-xl bg-white px-6 text-sm font-bold text-[#1d4ed8] shadow-lg transition hover:bg-blue-50"
              >
                Create New Test
                <span className="text-lg">→</span>
              </button>
            </div>

            {/* Exam illustration/card */}
            <div className="hidden items-center justify-center lg:flex">
              <div className="w-full max-w-[280px] rounded-3xl border border-white/20 bg-white/10 p-5 backdrop-blur">
                <div className="rounded-2xl bg-white p-5 shadow-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
                        Practice
                      </p>
                      <p className="mt-1 text-lg font-bold text-slate-900">
                        MHT-CET
                      </p>
                    </div>

                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-sm font-bold text-blue-600">
                      MC
                    </div>
                  </div>

                  <div className="mt-6 space-y-3">
                    <div className="h-2 rounded-full bg-slate-100">
                      <div className="h-2 w-[72%] rounded-full bg-blue-500" />
                    </div>

                    <div className="flex justify-between text-[11px] text-slate-400">
                      <span>Question bank</span>
                      <span>Ready</span>
                    </div>
                  </div>

                  <div className="mt-6 grid grid-cols-2 gap-2">
                    <div className="rounded-xl bg-slate-50 p-3">
                      <p className="text-[10px] text-slate-400">
                        Subjects
                      </p>
                      <p className="mt-1 text-sm font-bold text-slate-800">
                        4
                      </p>
                    </div>

                    <div className="rounded-xl bg-slate-50 p-3">
                      <p className="text-[10px] text-slate-400">
                        Mode
                      </p>
                      <p className="mt-1 text-sm font-bold text-slate-800">
                        CBT
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Stats */}
        <section className="mt-8 grid gap-4 sm:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6">
            <p className="text-sm font-medium text-slate-400">
              Tests Attempted
            </p>
            <p className="mt-2 text-3xl font-bold">0</p>
            <p className="mt-1 text-xs text-slate-400">
              Start your first test
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6">
            <p className="text-sm font-medium text-slate-400">
              Average Score
            </p>
            <p className="mt-2 text-3xl font-bold">—</p>
            <p className="mt-1 text-xs text-slate-400">
              Based on completed tests
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6">
            <p className="text-sm font-medium text-slate-400">
              Best Score
            </p>
            <p className="mt-2 text-3xl font-bold">—</p>
            <p className="mt-1 text-xs text-slate-400">
              Your highest performance
            </p>
          </div>
        </section>

        {/* Recent tests */}
        <section className="mt-12">
          <div className="mb-5 flex items-end justify-between">
            <div>
              <h2 className="text-xl font-bold tracking-tight">
                Recent Tests
              </h2>

              <p className="mt-1 text-sm text-slate-400">
                Your latest test attempts will appear here.
              </p>
            </div>

            <button
              onClick={() => router.push("/history")}
              className="text-sm font-semibold text-[#2563eb] hover:text-blue-700"
            >
              View all →
            </button>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white">
            <div className="flex min-h-[150px] items-center justify-center p-8 text-center">
              <div>
                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-50 text-xl">
                  📝
                </div>

                <p className="mt-4 text-sm font-semibold text-slate-700">
                  No tests yet
                </p>

                <p className="mt-1 text-xs text-slate-400">
                  Create your first MHT-CET test to see it here.
                </p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
