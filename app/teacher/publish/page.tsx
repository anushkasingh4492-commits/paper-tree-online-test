"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function TeacherPublishPage() {
  const router = useRouter();

  const [test, setTest] = useState<any>(null);
  const [title, setTitle] = useState("Scheduled Test");
  const [startTime, setStartTime] = useState("");
  const [duration, setDuration] = useState(60);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const saved = localStorage.getItem("teacherGeneratedTest");

    if (!saved) {
      router.push("/teacher/generate");
      return;
    }

    try {
      const data = JSON.parse(saved);
      setTest(data);

      if (data.questionCount) {
        setTitle(
          `Test - ${data.questionCount} Questions`
        );
      }

      if (data.duration) {
        setDuration(Number(data.duration));
      }
    } catch {
      router.push("/teacher/generate");
    }
  }, [router]);

  async function publishTest() {
    if (!startTime) {
      setMessage("Please select the test start time.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const start = new Date(startTime);
      const end = new Date(
        start.getTime() + duration * 60 * 1000
      );

      const response = await fetch(
        "/api/teacher/publish-test",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title,
            startTime: start.toISOString(),
            endTime: end.toISOString(),
            duration,
            test,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.error || "Could not publish test."
        );
      }

      localStorage.removeItem("teacherGeneratedTest");

      setMessage(
        "Test published successfully. Students will be notified."
      );

      setTimeout(() => {
        router.push("/teacher");
      }, 1500);
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Could not publish test."
      );
    } finally {
      setLoading(false);
    }
  }

  if (!test) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        Loading...
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc]">
      <div className="mx-auto max-w-4xl px-6 py-10">
        <button
          onClick={() => router.push("/teacher/generate")}
          className="mb-6 text-sm font-semibold text-[#315bea]"
        >
          ← Back
        </button>

        <div className="rounded-2xl bg-white p-8 shadow-sm">
          <p className="text-sm font-bold uppercase tracking-wider text-[#315bea]">
            Teacher Portal
          </p>

          <h1 className="mt-2 text-3xl font-bold">
            Publish Test
          </h1>

          <p className="mt-2 text-gray-500">
            Schedule this test for your students.
          </p>

          <div className="mt-8 space-y-6">
            <div>
              <label className="mb-2 block text-sm font-semibold">
                Test Title
              </label>

              <input
                value={title}
                onChange={(e) =>
                  setTitle(e.target.value)
                }
                className="w-full rounded-xl border px-4 py-3"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm font-semibold">
                Start Date & Time
              </label>

              <input
                type="datetime-local"
                value={startTime}
                onChange={(e) =>
                  setStartTime(e.target.value)
                }
                className="w-full rounded-xl border px-4 py-3"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm font-semibold">
                Duration (minutes)
              </label>

              <input
                type="number"
                min={1}
                value={duration}
                onChange={(e) =>
                  setDuration(Number(e.target.value))
                }
                className="w-full rounded-xl border px-4 py-3"
              />
            </div>
          </div>

          <div className="mt-8 rounded-xl bg-gray-50 p-5">
            <p className="font-semibold">
              Questions
            </p>

            <p className="mt-1 text-gray-600">
              {test.questionCount || "Generated"} questions
            </p>
          </div>

          {message && (
            <div className="mt-6 rounded-xl bg-blue-50 p-4 text-sm text-blue-700">
              {message}
            </div>
          )}

          <button
            onClick={publishTest}
            disabled={loading}
            className="mt-8 w-full rounded-xl bg-[#315bea] px-5 py-4 font-bold text-white hover:bg-[#264ac7] disabled:opacity-50"
          >
            {loading
              ? "Publishing..."
              : "Publish & Notify Students"}
          </button>
        </div>
      </div>
    </main>
  );
}
