"use client";

import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  useParams,
  useRouter,
} from "next/navigation";

type ScheduledTest = {
  id: string;
  scheduledTestId: string;
  paperId: string | null;
  batchId: string | null;

  title: string;
  exam: string;
  description: string;

  startTime: string;
  endTime: string;

  durationMinutes: number;
  questionCount: number;

  subjects: string[];
  chapters: string[];

  status: string;
};

function formatCountdown(
  milliseconds: number
) {
  const totalSeconds = Math.max(
    0,
    Math.floor(milliseconds / 1000)
  );

  const days = Math.floor(
    totalSeconds / 86400
  );

  const hours = Math.floor(
    (totalSeconds % 86400) / 3600
  );

  const minutes = Math.floor(
    (totalSeconds % 3600) / 60
  );

  const seconds =
    totalSeconds % 60;

  return {
    days,
    hours,
    minutes,
    seconds,
  };
}

function pad(value: number) {
  return String(value).padStart(2, "0");
}

export default function ScheduledTestPage() {
  const params = useParams();
  const router = useRouter();

  const scheduledTestId = String(
    params.scheduledTestId
  );

  const [test, setTest] =
    useState<ScheduledTest | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [now, setNow] =
    useState(Date.now());

  /*
   * Load scheduled test
   */

  useEffect(() => {
    async function loadTest() {
      try {
        setLoading(true);
        setError("");

        const response =
          await fetch(
            `/api/scheduled-tests/${scheduledTestId}`,
            {
              cache: "no-store",
              credentials: "include",
            }
          );

        const data =
          await response.json();

        if (!response.ok || !data?.success) {
          throw new Error(
            data?.error ||
              "Failed to load scheduled test."
          );
        }

        setTest(data.test);
      } catch (error) {
        console.error(
          "Scheduled test loading error:",
          error
        );

        setError(
          error instanceof Error
            ? error.message
            : "Failed to load scheduled test."
        );
      } finally {
        setLoading(false);
      }
    }

    loadTest();
  }, [scheduledTestId]);

  /*
   * Live clock
   */

  useEffect(() => {
    const interval =
      window.setInterval(() => {
        setNow(Date.now());
      }, 1000);

    return () => {
      window.clearInterval(interval);
    };
  }, []);

  const timing = useMemo(() => {
    if (!test) {
      return {
        started: false,
        ended: false,
        remaining: 0,
      };
    }

    const start =
      new Date(
        test.startTime
      ).getTime();

    const end =
      new Date(
        test.endTime
      ).getTime();

    return {
      started: now >= start,
      ended: now >= end,
      remaining: Math.max(
        0,
        start - now
      ),
    };
  }, [test, now]);

  const countdown =
    formatCountdown(
      timing.remaining
    );

  async function handleStart() {
    if (!test) return;

    if (!timing.started) {
      return;
    }

    if (timing.ended) {
      return;
    }

    try {
      const response = await fetch(
        `/api/scheduled-tests/${test.scheduledTestId}/start`,
        {
          method: "GET",
          cache: "no-store",
          credentials: "include",
        }
      );

      const data = await response.json();

      if (!response.ok || !data?.success || !data.testId) {
        throw new Error(
          data?.error || "Could not start this test."
        );
      }

      localStorage.setItem(
        `test-config-${data.testId}`,
        JSON.stringify({
          testId: data.testId,
          scheduledTestId: data.scheduledTestId,
          course: data.exam,
          duration: data.duration,
          startTime: data.startTime,
          endTime: data.endTime,
          reattempt: localStorage.getItem(`reattempt-${data.scheduledTestId}`) === "true",
          createdAt: new Date().toISOString(),
        })
      );
      localStorage.removeItem(`reattempt-${data.scheduledTestId}`);

      router.push(`/test/${data.testId}`);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Could not start this test."
      );
    }
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-surface-app-bg flex items-center justify-center">
        <div className="text-sm text-text-tertiary">
          Loading scheduled test...
        </div>
      </main>
    );
  }

  if (error || !test) {
    return (
      <main className="min-h-screen bg-surface-app-bg flex items-center justify-center p-6">
        <div className="bg-white rounded-2xl border border-border-default p-6 max-w-md w-full text-center">
          <h1 className="text-lg font-extrabold text-text-primary">
            Unable to load test
          </h1>

          <p className="mt-2 text-sm text-text-tertiary">
            {error || "Scheduled test not found."}
          </p>

          <button
            onClick={() =>
              router.push("/dashboard")
            }
            className="mt-5 h-10 px-5 rounded-lg bg-brand-primary text-white text-sm font-bold"
          >
            Back to Dashboard
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-surface-app-bg text-text-primary">
      <div className="max-w-5xl mx-auto px-5 py-8">

        {/* Back */}

        <button
          onClick={() =>
            router.push("/dashboard")
          }
          className="text-sm font-semibold text-text-tertiary hover:text-brand-primary"
        >
          ← Back to Dashboard
        </button>

        {/* Header */}

        <div className="mt-5 bg-white rounded-2xl border border-border-default shadow-[0_3px_12px_rgba(30,35,60,.035)] overflow-hidden">

          <div className="p-6 border-b border-border-default">
            <div className="flex items-start justify-between gap-4">

              <div>
                <p className="text-[10px] font-bold uppercase tracking-wider text-brand-primary">
                  {test.exam}
                </p>

                <h1 className="mt-2 text-2xl font-extrabold">
                  {test.title}
                </h1>

                {test.description && (
                  <p className="mt-2 text-sm text-text-tertiary">
                    {test.description}
                  </p>
                )}
              </div>

              <span className="shrink-0 px-3 py-1.5 rounded-lg bg-surface-subtle text-brand-primary text-xs font-bold">
                {timing.ended
                  ? "Ended"
                  : timing.started
                    ? "Live"
                    : "Upcoming"}
              </span>

            </div>
          </div>

          {/* Countdown */}

          <div className="p-6 bg-surface-app-bg border-b border-border-default">

            {!timing.started &&
              !timing.ended && (
                <div className="text-center">

                  <p className="text-xs font-bold text-text-tertiary">
                    Test starts in
                  </p>

                  <div className="mt-4 flex justify-center gap-3">

                    <div className="bg-white rounded-xl border border-border-default px-4 py-3 min-w-[70px]">
                      <div className="text-2xl font-extrabold text-brand-primary">
                        {countdown.days}
                      </div>
                      <div className="text-[9px] uppercase font-bold text-text-body">
                        Days
                      </div>
                    </div>

                    <div className="bg-white rounded-xl border border-border-default px-4 py-3 min-w-[70px]">
                      <div className="text-2xl font-extrabold text-brand-primary">
                        {pad(countdown.hours)}
                      </div>
                      <div className="text-[9px] uppercase font-bold text-text-body">
                        Hours
                      </div>
                    </div>

                    <div className="bg-white rounded-xl border border-border-default px-4 py-3 min-w-[70px]">
                      <div className="text-2xl font-extrabold text-brand-primary">
                        {pad(countdown.minutes)}
                      </div>
                      <div className="text-[9px] uppercase font-bold text-text-body">
                        Minutes
                      </div>
                    </div>

                    <div className="bg-white rounded-xl border border-border-default px-4 py-3 min-w-[70px]">
                      <div className="text-2xl font-extrabold text-brand-primary">
                        {pad(countdown.seconds)}
                      </div>
                      <div className="text-[9px] uppercase font-bold text-text-body">
                        Seconds
                      </div>
                    </div>

                  </div>
                </div>
              )}

            {timing.started &&
              !timing.ended && (
                <div className="text-center">

                  <p className="text-xs font-bold text-state-success">
                    Test is now live
                  </p>

                  <button
                    onClick={handleStart}
                    className="mt-4 h-12 px-10 rounded-xl bg-brand-primary text-white text-sm font-extrabold shadow-[0_8px_20px_rgba(49,91,234,.18)] hover:bg-brand-action-blue"
                  >
                    Start Test →
                  </button>

                </div>
              )}

            {timing.ended && (
              <div className="text-center">
                <p className="text-sm font-bold text-state-error">
                  This test has ended.
                </p>
              </div>
            )}

          </div>

          {/* Basic info */}

          <div className="p-6 grid grid-cols-2 md:grid-cols-4 gap-4">

            <div className="rounded-xl bg-surface-app-bg p-4">
              <p className="text-[10px] font-bold text-text-body">
                QUESTIONS
              </p>
              <p className="mt-1 text-lg font-extrabold">
                {test.questionCount}
              </p>
            </div>

            <div className="rounded-xl bg-surface-app-bg p-4">
              <p className="text-[10px] font-bold text-text-body">
                DURATION
              </p>
              <p className="mt-1 text-lg font-extrabold">
                {test.durationMinutes} min
              </p>
            </div>

            <div className="rounded-xl bg-surface-app-bg p-4">
              <p className="text-[10px] font-bold text-text-body">
                START
              </p>
              <p className="mt-1 text-sm font-extrabold">
                {new Date(
                  test.startTime
                ).toLocaleString()}
              </p>
            </div>

            <div className="rounded-xl bg-surface-app-bg p-4">
              <p className="text-[10px] font-bold text-text-body">
                END
              </p>
              <p className="mt-1 text-sm font-extrabold">
                {new Date(
                  test.endTime
                ).toLocaleString()}
              </p>
            </div>

          </div>

          {/* Subjects */}

          <div className="px-6 pb-6">

            <h2 className="text-sm font-extrabold">
              Subjects
            </h2>

            <div className="mt-3 flex flex-wrap gap-2">

              {test.subjects.length > 0 ? (
                test.subjects.map(
                  (subject) => (
                    <span
                      key={subject}
                      className="px-3 py-1.5 rounded-lg bg-surface-subtle text-brand-primary text-xs font-bold"
                    >
                      {subject}
                    </span>
                  )
                )
              ) : (
                <span className="text-xs text-text-body">
                  No subjects configured
                </span>
              )}

            </div>

          </div>

          {/* Chapters */}

          <div className="px-6 pb-7">

            <h2 className="text-sm font-extrabold">
              Chapters
            </h2>

            <div className="mt-3 flex flex-wrap gap-2">

              {test.chapters.length > 0 ? (
                test.chapters.map(
                  (chapter) => (
                    <span
                      key={chapter}
                      className="px-3 py-1.5 rounded-lg bg-surface-app-bg border border-border-default text-text-secondary text-xs font-semibold"
                    >
                      {chapter}
                    </span>
                  )
                )
              ) : (
                <span className="text-xs text-text-body">
                  No chapters configured
                </span>
              )}

            </div>

          </div>

        </div>
      </div>
    </main>
  );
}
