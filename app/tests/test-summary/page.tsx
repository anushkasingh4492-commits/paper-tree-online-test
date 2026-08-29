"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

/* ============================================================
   TYPES
============================================================ */

type TestSummaryItem = {
  id: string;
  attemptId?: string | null;

  name: string;
  exam?: string | null;

  status:
    | "Upcoming"
    | "Missed"
    | "Completed"
    | "In Progress"
    | string;

  questionCount: number;

  startTime?: string | null;
  endTime?: string | null;

  description?: string | null;
  comment?: string | null;

  score?: number | null;
  totalMarks?: number | null;

  correct?: number | null;
  incorrect?: number | null;
  unanswered?: number | null;

  durationMinutes?: number | null;
};

type SummaryResponse = {
  success?: boolean;
  error?: string;

  summary?: {
    total?: number;
    taken?: number;
    missed?: number;
    upcoming?: number;
  };

  tests?: TestSummaryItem[];
};

/* ============================================================
   ICONS
============================================================ */

type IconType =
  | "home"
  | "tests"
  | "calendar"
  | "clock"
  | "check"
  | "close"
  | "arrow"
  | "logout"
  | "user"
  | "file";

function MiniIcon({
  type,
  size = 18,
}: {
  type: IconType;
  size?: number;
}) {
  const paths: Record<
    IconType,
    React.ReactNode
  > = {
    home: (
      <>
        <path d="m3 9 5-5 5 5" />
        <path d="M5 8v7h6V8" />
        <path d="M7.5 15v-4h2v4" />
      </>
    ),

    tests: (
      <>
        <rect
          x="4"
          y="3"
          width="8"
          height="12"
          rx="1.5"
        />
        <path d="M6.5 7h3" />
        <path d="M6.5 10h3" />
        <path d="M6.5 13h2" />
      </>
    ),

    calendar: (
      <>
        <rect
          x="3"
          y="4"
          width="10"
          height="9"
          rx="1.5"
        />
        <path d="M5 2v3" />
        <path d="M11 2v3" />
        <path d="M3 7h10" />
      </>
    ),

    clock: (
      <>
        <circle cx="8" cy="8" r="5.5" />
        <path d="M8 5v3l2 1" />
      </>
    ),

    check: (
      <path d="m4 8 2.5 2.5L12 5" />
    ),

    close: (
      <>
        <path d="m5 5 6 6" />
        <path d="m11 5-6 6" />
      </>
    ),

    arrow: (
      <>
        <path d="M3 8h9" />
        <path d="m9 5 3 3-3 3" />
      </>
    ),

    logout: (
      <>
        <path d="M6 3H4.5A1.5 1.5 0 0 0 3 4.5v7A1.5 1.5 0 0 0 4.5 13H6" />
        <path d="M8 5l3 3-3 3" />
        <path d="M11 8H5" />
      </>
    ),

    user: (
      <>
        <circle cx="8" cy="5" r="2.3" />
        <path d="M3.5 14c.7-2.4 2.2-3.6 4.5-3.6s3.8 1.2 4.5 3.6" />
      </>
    ),

    file: (
      <>
        <path d="M5 2.5h5l3 3v10H5z" />
        <path d="M10 2.5v3h3" />
        <path d="M7 9h4" />
        <path d="M7 12h4" />
      </>
    ),
  };

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 16 16"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {paths[type]}
    </svg>
  );
}

/* ============================================================
   HELPERS
============================================================ */

function formatDateTime(
  value?: string | null
) {
  if (!value) return "—";

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatDate(
  value?: string | null
) {
  if (!value) return "—";

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

function formatTime(
  value?: string | null
) {
  if (!value) return "—";

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleTimeString("en-IN", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function initials(name: string) {
  const parts = name
    .trim()
    .split(/\s+/)
    .filter(Boolean);

  if (!parts.length) return "S";

  if (parts.length === 1) {
    return parts[0][0].toUpperCase();
  }

  return `${parts[0][0]}${
    parts[parts.length - 1][0]
  }`.toUpperCase();
}

/* ============================================================
   STATUS
============================================================ */

function statusConfig(status: string) {
  const normalized =
    status.toLowerCase();

  if (
    normalized === "completed" ||
    normalized === "submitted" ||
    normalized === "taken"
  ) {
    return {
      label: "Completed",
      bg: "bg-emerald-50",
      text: "text-emerald-600",
      dot: "bg-emerald-500",
      icon: "check" as IconType,
    };
  }

  if (
    normalized === "missed" ||
    normalized === "expired"
  ) {
    return {
      label: "Missed",
      bg: "bg-rose-50",
      text: "text-rose-600",
      dot: "bg-rose-500",
      icon: "close" as IconType,
    };
  }

  if (
    normalized === "in progress" ||
    normalized === "started"
  ) {
    return {
      label: "In Progress",
      bg: "bg-amber-50",
      text: "text-amber-600",
      dot: "bg-amber-500",
      icon: "clock" as IconType,
    };
  }

  return {
    label: "Upcoming",
    bg: "bg-blue-50",
    text: "text-blue-600",
    dot: "bg-blue-500",
    icon: "calendar" as IconType,
  };
}

/* ============================================================
   MAIN PAGE
============================================================ */

export default function TestSummaryPage() {
  const router = useRouter();

  const [studentName, setStudentName] =
    useState("Student");

  const [tests, setTests] =
    useState<TestSummaryItem[]>([]);

  const [summary, setSummary] =
    useState({
      total: 0,
      taken: 0,
      missed: 0,
      upcoming: 0,
    });

  const [activeFilter, setActiveFilter] =
    useState<
      "All" |
      "Completed" |
      "Missed" |
      "Upcoming"
    >("All");

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  /* ==========================================================
     LOAD DATA
  ========================================================== */

  useEffect(() => {
    let active = true;

    async function loadSummary() {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(
          "/api/test-summary",
          {
            method: "GET",
            cache: "no-store",
            credentials: "include",
          }
        );

        const data: SummaryResponse =
          await response.json();

        if (!response.ok) {
          if (
            response.status === 401
          ) {
            router.push("/login");
            return;
          }

          throw new Error(
            data.error ||
              "Failed to load test summary."
          );
        }

        if (!active) return;

        setTests(
          Array.isArray(data.tests)
            ? data.tests
            : []
        );

        setSummary({
          total:
            Number(
              data.summary?.total ?? 0
            ),
          taken:
            Number(
              data.summary?.taken ?? 0
            ),
          missed:
            Number(
              data.summary?.missed ?? 0
            ),
          upcoming:
            Number(
              data.summary?.upcoming ?? 0
            ),
        });

        const storedName =
          localStorage.getItem(
            "studentName"
          ) ||
          localStorage.getItem(
            "username"
          );

        if (storedName) {
          setStudentName(
            storedName
          );
        }
      } catch (err) {
        console.error(
          "Test summary loading error:",
          err
        );

        if (active) {
          setError(
            err instanceof Error
              ? err.message
              : "Failed to load test summary."
          );
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    loadSummary();

    return () => {
      active = false;
    };
  }, [router]);

  /* ==========================================================
     FILTER
  ========================================================== */

  const filteredTests = useMemo(() => {
    if (activeFilter === "All") {
      return tests;
    }

    return tests.filter((test) => {
      const status =
        statusConfig(
          test.status
        ).label;

      return (
        status === activeFilter
      );
    });
  }, [
    tests,
    activeFilter,
  ]);

  /* ==========================================================
     LOGOUT
  ========================================================== */

  function logout() {
    localStorage.removeItem(
      "studentName"
    );

    localStorage.removeItem(
      "username"
    );

    document.cookie =
      "student_session=; Max-Age=0; path=/";

    router.push("/login");
  }

  /* ==========================================================
     LOADING
  ========================================================== */

  if (loading) {
    return (
      <main className="min-h-screen bg-[#f8f9fc] flex items-center justify-center">
        <div className="text-center">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#2563eb] to-[#6338e5] text-white flex items-center justify-center font-black text-lg mx-auto animate-pulse">
            P
          </div>

          <p className="mt-4 text-sm font-semibold text-[#4e596c]">
            Loading test summary...
          </p>

          <p className="mt-1 text-xs text-[#9aa1ae]">
            Preparing your scheduled
            tests
          </p>
        </div>
      </main>
    );
  }

  /* ==========================================================
     ERROR
  ========================================================== */

  if (error) {
    return (
      <main className="min-h-screen bg-[#f8f9fc] flex items-center justify-center px-5">
        <div className="bg-white border border-[#e8eaf0] rounded-2xl p-7 max-w-md w-full text-center shadow-sm">
          <div className="w-12 h-12 rounded-full bg-rose-50 text-rose-500 flex items-center justify-center mx-auto text-xl font-bold">
            !
          </div>

          <h1 className="mt-4 text-lg font-extrabold text-[#202638]">
            Unable to load test summary
          </h1>

          <p className="mt-2 text-xs text-[#858c9b]">
            {error}
          </p>

          <button
            onClick={() =>
              window.location.reload()
            }
            className="mt-5 h-9 px-5 rounded-lg bg-[#6246e5] text-white text-xs font-bold"
          >
            Try Again
          </button>
        </div>
      </main>
    );
  }

  /* ==========================================================
     MAIN
  ========================================================== */

  return (
    <main className="min-h-screen bg-[#f8f9fc] text-[#1d2435]">
      <div className="flex min-h-screen">

        {/* =====================================================
            SIDEBAR
        ====================================================== */}

        <aside className="hidden xl:flex w-[220px] shrink-0 bg-white border-r border-[#e9ebf1] flex-col">

          {/* Logo */}

          <div className="h-[82px] px-5 flex items-center gap-3 border-b border-[#f0f1f5]">
            <div className="w-9 h-9 rounded-[11px] bg-gradient-to-br from-[#2563eb] to-[#6338e5] text-white flex items-center justify-center font-black text-lg shadow-sm">
              P
            </div>

            <div>
              <div className="font-extrabold text-[15px] leading-4">
                Paper Tree
              </div>

              <div className="text-[9px] font-semibold tracking-[.17em] text-[#9ba1ad] mt-1">
                ONLINE TEST
              </div>
            </div>
          </div>

          {/* Navigation */}

          <div className="px-4 pt-5 flex-1">
            <p className="px-2 mb-2 text-[9px] uppercase tracking-[.16em] font-bold text-[#a1a7b3]">
              Workspace
            </p>

            <nav className="space-y-1">

              {/* Dashboard */}

              <button
                onClick={() =>
                  router.push(
                    "/dashboard"
                  )
                }
                className="w-full h-10 flex items-center gap-3 px-2.5 rounded-xl text-[#657083] hover:bg-[#f7f8fb] text-xs font-medium"
              >
                <span className="w-7 h-7 rounded-lg bg-[#f5f6f9] flex items-center justify-center">
                  <MiniIcon type="home" />
                </span>

                Dashboard
              </button>

              {/* My Tests */}

              <button
                onClick={() =>
                  router.push("/tests")
                }
                className="w-full h-10 flex items-center gap-3 px-2.5 rounded-xl text-[#657083] hover:bg-[#f7f8fb] text-xs font-medium"
              >
                <span className="w-7 h-7 rounded-lg bg-[#f5f6f9] flex items-center justify-center">
                  <MiniIcon type="tests" />
                </span>

                My Tests
              </button>

              {/* Test Summary */}

              <button
                onClick={() =>
                  router.push(
                    "/test-summary"
                  )
                }
                className="w-full h-10 flex items-center gap-3 px-2.5 rounded-xl bg-[#f0efff] text-[#5640db] text-xs font-bold"
              >
                <span className="w-7 h-7 rounded-lg bg-white flex items-center justify-center">
                  <MiniIcon
                    type="calendar"
                  />
                </span>

                Test Summary
              </button>
            </nav>
          </div>

          {/* Premium */}

          <div className="px-4 pb-3">
            <div className="rounded-xl bg-gradient-to-br from-[#fff8e9] via-[#fff4fb] to-[#f2edff] border border-[#eee8ff] p-3.5">
              <div className="flex items-center gap-2 text-[#7357dc]">
                <span className="w-7 h-7 rounded-lg bg-white flex items-center justify-center">
                  ♛
                </span>

                <span className="text-xs font-extrabold">
                  Go Premium
                </span>
              </div>

              <p className="text-[9px] text-[#818898] leading-4 mt-2">
                Unlock unlimited tests,
                detailed analytics and
                more.
              </p>

              <button className="mt-2.5 w-full h-8 rounded-lg bg-gradient-to-r from-[#6744e8] to-[#7d31e8] text-white text-[10px] font-bold">
                Upgrade Now
              </button>
            </div>
          </div>

          {/* Logout */}

          <button
            className="mx-5 mb-5 mt-1 flex items-center gap-3 h-9 text-xs text-[#657083]"
            onClick={logout}
          >
            <MiniIcon type="logout" />

            Logout
          </button>
        </aside>

        {/* =====================================================
            CONTENT
        ====================================================== */}

        <div className="flex-1 min-w-0">

          {/* Header */}

          <header className="h-[82px] bg-white border-b border-[#e9ebf1] px-5 lg:px-8 flex items-center justify-between">
            <div>
              <h1 className="text-[20px] font-extrabold tracking-tight">
                Test Summary
              </h1>

              <p className="mt-1 text-[11px] text-[#858c9b]">
                Track your completed,
                missed and upcoming tests
              </p>
            </div>

            <div className="flex items-center gap-3">
              <button
                onClick={() =>
                  router.push("/tests")
                }
                className="hidden sm:flex items-center gap-2 h-9 px-3.5 rounded-xl border border-[#e8eaf1] bg-white text-[11px] font-semibold text-[#4e596c]"
              >
                <MiniIcon
                  type="tests"
                  size={15}
                />

                My Tests
              </button>

              <div className="w-9 h-9 rounded-full bg-gradient-to-br from-[#6944e8] to-[#4f2bd5] text-white flex items-center justify-center text-sm font-bold">
                {initials(
                  studentName
                )[0]}
              </div>
            </div>
          </header>

          {/* Body */}

          <div className="p-5 lg:p-6 xl:p-7 max-w-[1500px] mx-auto">

            {/* =================================================
                PAGE INTRO
            ================================================== */}

            <section className="relative overflow-hidden rounded-[16px] bg-gradient-to-r from-[#2460ef] via-[#4b3fe8] to-[#8735ee] text-white px-7 py-6 shadow-[0_8px_24px_rgba(83,65,220,.14)]">

              <div className="absolute -right-20 -top-24 w-64 h-64 rounded-full bg-white/[.07]" />

              <div className="absolute right-24 -bottom-40 w-80 h-80 rounded-full bg-white/[.06]" />

              <div className="relative">
                <div className="flex items-center gap-2 text-[11px] font-semibold">
                  <span className="w-2 h-2 rounded-full bg-[#28d48a]" />

                  MHT-CET · 2026
                </div>

                <h2 className="mt-3 text-[25px] font-extrabold">
                  Your Test Schedule
                </h2>

                <p className="mt-1.5 text-[12px] text-white/80 max-w-[600px]">
                  See all your tests in one
                  place — completed, missed
                  and upcoming.
                </p>
              </div>
            </section>

            {/* =================================================
                SUMMARY CARDS
            ================================================== */}

            <section className="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-5">

              {/* Total */}

              <div className="bg-white rounded-[14px] border border-[#e8eaf0] px-4 py-4 shadow-[0_3px_12px_rgba(30,35,60,.035)]">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-[10px] font-semibold text-[#858c9b]">
                      Total Tests
                    </p>

                    <p className="mt-2 text-[24px] font-extrabold text-[#202638]">
                      {summary.total}
                    </p>
                  </div>

                  <span className="w-10 h-10 rounded-full bg-violet-50 text-violet-600 flex items-center justify-center">
                    <MiniIcon type="file" />
                  </span>
                </div>
              </div>

              {/* Taken */}

              <div className="bg-white rounded-[14px] border border-[#e8eaf0] px-4 py-4 shadow-[0_3px_12px_rgba(30,35,60,.035)]">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-[10px] font-semibold text-[#858c9b]">
                      Tests Taken
                    </p>

                    <p className="mt-2 text-[24px] font-extrabold text-emerald-600">
                      {summary.taken}
                    </p>
                  </div>

                  <span className="w-10 h-10 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center">
                    <MiniIcon type="check" />
                  </span>
                </div>
              </div>

              {/* Missed */}

              <div className="bg-white rounded-[14px] border border-[#e8eaf0] px-4 py-4 shadow-[0_3px_12px_rgba(30,35,60,.035)]">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-[10px] font-semibold text-[#858c9b]">
                      Missed Tests
                    </p>

                    <p className="mt-2 text-[24px] font-extrabold text-rose-500">
                      {summary.missed}
                    </p>
                  </div>

                  <span className="w-10 h-10 rounded-full bg-rose-50 text-rose-600 flex items-center justify-center">
                    <MiniIcon type="close" />
                  </span>
                </div>
              </div>

              {/* Upcoming */}

              <div className="bg-white rounded-[14px] border border-[#e8eaf0] px-4 py-4 shadow-[0_3px_12px_rgba(30,35,60,.035)]">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-[10px] font-semibold text-[#858c9b]">
                      Upcoming Tests
                    </p>

                    <p className="mt-2 text-[24px] font-extrabold text-blue-600">
                      {summary.upcoming}
                    </p>
                  </div>

                  <span className="w-10 h-10 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center">
                    <MiniIcon type="calendar" />
                  </span>
                </div>
              </div>
            </section>

            {/* =================================================
                FILTERS
            ================================================== */}

            <section className="mt-5 bg-white rounded-[14px] border border-[#e8eaf0] p-4 shadow-[0_3px_12px_rgba(30,35,60,.035)]">

              <div className="flex flex-wrap items-center gap-2">

                {[
                  "All",
                  "Completed",
                  "Missed",
                  "Upcoming",
                ].map((filter) => (
                  <button
                    key={filter}
                    onClick={() =>
                      setActiveFilter(
                        filter as typeof activeFilter
                      )
                    }
                    className={`h-9 px-4 rounded-lg text-[10px] font-bold transition ${
                      activeFilter ===
                      filter
                        ? "bg-[#6246e5] text-white"
                        : "border border-[#e7e9ef] text-[#697184] hover:bg-[#f7f8fb]"
                    }`}
                  >
                    {filter}
                  </button>
                ))}
              </div>
            </section>

            {/* =================================================
                TEST LIST
            ================================================== */}

            <section className="mt-5 bg-white rounded-[14px] border border-[#e8eaf0] shadow-[0_3px_12px_rgba(30,35,60,.035)] overflow-hidden">

              <div className="px-5 py-4 border-b border-[#eff0f4]">
                <h2 className="text-[14px] font-extrabold">
                  Test Details
                </h2>

                <p className="mt-1 text-[10px] text-[#939aa8]">
                  Complete information about
                  your tests
                </p>
              </div>

              <div className="p-5 space-y-4">

                {filteredTests.map(
                  (test) => {
                    const config =
                      statusConfig(
                        test.status
                      );

                    return (
                      <div
                        key={`${test.id}-${test.attemptId || ""}`}
                        className="rounded-[14px] border border-[#e9ebf0] p-4 hover:border-[#ddd8ff] hover:shadow-[0_4px_16px_rgba(70,50,180,.05)] transition"
                      >

                        {/* Top */}

                        <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-4">

                          <div className="flex items-start gap-3 min-w-0">

                            <div className="w-10 h-10 rounded-xl bg-[#f0efff] text-[#6246e5] flex items-center justify-center shrink-0">
                              <MiniIcon
                                type="file"
                                size={19}
                              />
                            </div>

                            <div className="min-w-0">
                              <div className="flex flex-wrap items-center gap-2">

                                <h3 className="text-[13px] font-extrabold text-[#303749]">
                                  {test.name}
                                </h3>

                                <span
                                  className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full ${config.bg} ${config.text} text-[9px] font-bold`}
                                >
                                  <span
                                    className={`w-1.5 h-1.5 rounded-full ${config.dot}`}
                                  />

                                  {
                                    config.label
                                  }
                                </span>

                              </div>

                              <p className="mt-1 text-[10px] text-[#9299a7]">
                                {test.exam ||
                                  "MHT-CET"}
                              </p>
                            </div>
                          </div>

                          {/* Score */}

                          {test.score !==
                            null &&
                            test.score !==
                              undefined && (
                              <div className="text-left lg:text-right">
                                <p className="text-[9px] text-[#939aa8]">
                                  Score
                                </p>

                                <p className="text-[19px] font-extrabold text-[#6246e5]">
                                  {Number(
                                    test.score
                                  ).toFixed(
                                    1
                                  )}
                                  %
                                </p>
                              </div>
                            )}
                        </div>

                        {/* Details */}

                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-4">

                          {/* Start */}

                          <div className="rounded-xl bg-[#f8f9fc] border border-[#eef0f4] p-3">
                            <div className="flex items-center gap-2 text-[#6246e5]">
                              <MiniIcon
                                type="clock"
                                size={14}
                              />

                              <span className="text-[9px] font-bold text-[#858c9b]">
                                Start Time
                              </span>
                            </div>

                            <p className="mt-2 text-[10px] font-bold text-[#3f4758]">
                              {formatDateTime(
                                test.startTime
                              )}
                            </p>
                          </div>

                          {/* End */}

                          <div className="rounded-xl bg-[#f8f9fc] border border-[#eef0f4] p-3">
                            <div className="flex items-center gap-2 text-[#6246e5]">
                              <MiniIcon
                                type="clock"
                                size={14}
                              />

                              <span className="text-[9px] font-bold text-[#858c9b]">
                                End Time
                              </span>
                            </div>

                            <p className="mt-2 text-[10px] font-bold text-[#3f4758]">
                              {formatDateTime(
                                test.endTime
                              )}
                            </p>
                          </div>

                          {/* Questions */}

                          <div className="rounded-xl bg-[#f8f9fc] border border-[#eef0f4] p-3">
                            <div className="flex items-center gap-2 text-[#6246e5]">
                              <MiniIcon
                                type="file"
                                size={14}
                              />

                              <span className="text-[9px] font-bold text-[#858c9b]">
                                Questions
                              </span>
                            </div>

                            <p className="mt-2 text-[10px] font-bold text-[#3f4758]">
                              {
                                test.questionCount
                              }{" "}
                              Questions
                            </p>
                          </div>

                          {/* Date */}

                          <div className="rounded-xl bg-[#f8f9fc] border border-[#eef0f4] p-3">
                            <div className="flex items-center gap-2 text-[#6246e5]">
                              <MiniIcon
                                type="calendar"
                                size={14}
                              />

                              <span className="text-[9px] font-bold text-[#858c9b]">
                                Test Date
                              </span>
                            </div>

                            <p className="mt-2 text-[10px] font-bold text-[#3f4758]">
                              {formatDate(
                                test.startTime
                              )}
                            </p>
                          </div>
                        </div>

                        {/* Description */}

                        {(test.description ||
                          test.comment) && (
                          <div className="mt-3 rounded-xl bg-[#faf9ff] border border-[#ece8ff] p-3">
                            <div className="flex items-start gap-2">

                              <span className="w-7 h-7 rounded-lg bg-[#eeeaff] text-[#6246e5] flex items-center justify-center shrink-0">
                                <MiniIcon
                                  type="file"
                                  size={13}
                                />
                              </span>

                              <div>
                                <p className="text-[9px] font-bold text-[#6246e5]">
                                  Description
                                </p>

                                <p className="mt-1 text-[10px] leading-4 text-[#70798a]">
                                  {test.description ||
                                    test.comment}
                                </p>
                              </div>

                            </div>
                          </div>
                        )}

                        {/* Completed details */}

                        {config.label ===
                          "Completed" && (
                          <div className="mt-3 flex flex-wrap gap-4 text-[9px] text-[#7c8492]">

                            <span>
                              ✓{" "}
                              {
                                test.correct
                              }{" "}
                              correct
                            </span>

                            <span>
                              ×{" "}
                              {
                                test.incorrect
                              }{" "}
                              incorrect
                            </span>

                            <span>
                              —{" "}
                              {
                                test.unanswered
                              }{" "}
                              unanswered
                            </span>

                          </div>
                        )}

                        {/* Action */}

                        {config.label ===
                          "Upcoming" && (
                          <button
                           onClick={() =>
  router.push(
    `/test/result/${test.id}`
  )
}
                            className="mt-4 h-9 px-4 rounded-lg bg-[#6246e5] text-white text-[10px] font-bold inline-flex items-center gap-2"
                          >
                            Start Test

                            <MiniIcon
                              type="arrow"
                              size={13}
                            />
                          </button>
                        )}

                      </div>
                    );
                  }
                )}

                {/* Empty */}

                {!filteredTests.length && (
                  <div className="py-16 text-center">

                    <div className="w-12 h-12 rounded-full bg-[#f1efff] text-[#6246e5] flex items-center justify-center mx-auto">
                      <MiniIcon
                        type="calendar"
                        size={22}
                      />
                    </div>

                    <p className="mt-4 text-xs font-bold text-[#596275]">
                      No{" "}
                      {activeFilter ===
                      "All"
                        ? ""
                        : activeFilter.toLowerCase() +
                          " "}
                      tests found
                    </p>

                    <p className="mt-1 text-[10px] text-[#9aa1ae]">
                      Your test schedule will
                      appear here.
                    </p>
                  </div>
                )}

              </div>
            </section>

          </div>
        </div>
      </div>

      {/* =======================================================
          MOBILE NAV
      ======================================================== */}

      <nav className="xl:hidden fixed bottom-0 inset-x-0 z-40 bg-white/95 backdrop-blur border-t border-[#e8eaf0] px-4 py-2.5">
        <div className="max-w-lg mx-auto flex items-center justify-around">

          <button
            onClick={() =>
              router.push(
                "/dashboard"
              )
            }
            className="flex flex-col items-center gap-1 text-[#7d8595]"
          >
            <MiniIcon
              type="home"
              size={18}
            />

            <span className="text-[9px] font-semibold">
              Dashboard
            </span>
          </button>

          <button
            onClick={() =>
              router.push("/tests")
            }
            className="flex flex-col items-center gap-1 text-[#7d8595]"
          >
            <MiniIcon
              type="tests"
              size={18}
            />

            <span className="text-[9px] font-semibold">
              My Tests
            </span>
          </button>

          <button
            onClick={() =>
              router.push(
                "/test-summary"
              )
            }
            className="flex flex-col items-center gap-1 text-[#6246e5]"
          >
            <MiniIcon
              type="calendar"
              size={18}
            />

            <span className="text-[9px] font-bold">
              Summary
            </span>
          </button>

          <button
            onClick={() =>
              router.push("/profile")
            }
            className="flex flex-col items-center gap-1 text-[#7d8595]"
          >
            <span className="w-5 h-5 rounded-full bg-gradient-to-br from-[#7044e8] to-[#4c2bd0] text-white text-[8px] font-bold flex items-center justify-center">
              {initials(
                studentName
              )[0]}
            </span>

            <span className="text-[9px] font-semibold">
              Profile
            </span>
          </button>

        </div>
      </nav>
    </main>
  );
}