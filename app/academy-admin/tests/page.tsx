"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type Paper = {
  id: string;
  code?: string;
  exam?: string;
  description?: string;
  duration_minutes?: number;
};

type Batch = {
  id: string;
  name: string;
  class_name?: string;
};

type ScheduledTest = {
  id: string;
  title: string;
  paper_id: string;
  batch_id: string;
  batch_name?: string;
  start_time: string;
  end_time: string;
  duration_minutes: number;
  status: string;
};

export default function AcademyAdminTestsPage() {
  const router = useRouter();

  const [papers, setPapers] = useState<Paper[]>([]);
  const [batches, setBatches] = useState<Batch[]>([]);
  const [tests, setTests] = useState<ScheduledTest[]>([]);

  const [paperId, setPaperId] = useState("");
  const [batchId, setBatchId] = useState("");
  const [title, setTitle] = useState("");
  const [startTime, setStartTime] = useState("");
  const [duration, setDuration] = useState(60);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  async function loadData() {
    try {
      setLoading(true);

      const [papersRes, batchesRes, testsRes] = await Promise.all([
        fetch("/api/academy-admin/papers"),
        fetch("/api/academy-admin/batches"),
        fetch("/api/academy-admin/tests"),
      ]);

      const papersData = await papersRes.json();
      const batchesData = await batchesRes.json();
      const testsData = await testsRes.json();

      if (!papersRes.ok) {
        throw new Error(papersData.error || "Failed to load papers");
      }

      if (!batchesRes.ok) {
        throw new Error(batchesData.error || "Failed to load batches");
      }

      if (!testsRes.ok) {
        throw new Error(testsData.error || "Failed to load scheduled tests");
      }

      setPapers(papersData.papers || []);
      setBatches(Array.isArray(batchesData) ? batchesData : []);
      setTests(Array.isArray(testsData) ? testsData : []);
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Failed to load data."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  function handlePaperChange(id: string) {
    setPaperId(id);

    const paper = papers.find((p) => p.id === id);

    if (paper?.description) {
      setTitle(paper.description);
    } else if (paper?.exam) {
      setTitle(`${paper.exam} Test`);
    }

    if (paper?.duration_minutes) {
      setDuration(Number(paper.duration_minutes));
    }
  }

  async function scheduleTest() {
    setMessage("");

    if (!paperId || !batchId || !title.trim() || !startTime) {
      setMessage("Please fill all required fields.");
      return;
    }

    const start = new Date(startTime);

    if (Number.isNaN(start.getTime())) {
      setMessage("Please select a valid start time.");
      return;
    }

    const end = new Date(
      start.getTime() + Number(duration) * 60 * 1000
    );

    if (end <= start) {
      setMessage("Duration must be greater than 0.");
      return;
    }

    try {
      setSaving(true);

      const response = await fetch("/api/academy-admin/tests", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          paperId,
          batchId,
          title: title.trim(),
          startTime: start.toISOString(),
          endTime: end.toISOString(),
          durationMinutes: Number(duration),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to schedule test.");
      }

      setMessage("Test scheduled successfully.");

      setPaperId("");
      setBatchId("");
      setTitle("");
      setStartTime("");
      setDuration(60);

      await loadData();
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Failed to schedule test."
      );
    } finally {
      setSaving(false);
    }
  }

  function formatDate(value: string) {
    return new Date(value).toLocaleString("en-IN", {
      dateStyle: "medium",
      timeStyle: "short",
    });
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc]">
      <div className="mx-auto max-w-6xl px-6 py-10">
        <button
          onClick={() => router.push("/academy-admin")}
          className="mb-6 text-sm font-semibold text-[#315bea]"
        >
          ← Back to Academy Admin
        </button>

        <div className="mb-8">
          <p className="text-sm font-bold uppercase tracking-wider text-[#315bea]">
            Academy Admin
          </p>

          <h1 className="mt-2 text-3xl font-bold text-gray-900">
            Scheduled Tests
          </h1>

          <p className="mt-2 text-gray-500">
            Schedule papers for your academy batches.
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-[1fr_1.2fr]">
          {/* Schedule form */}
          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <h2 className="text-xl font-bold text-gray-900">
              Schedule New Test
            </h2>

            <div className="mt-6 space-y-5">
              <div>
                <label className="mb-2 block text-sm font-semibold">
                  Select Paper
                </label>

                <select
                  value={paperId}
                  onChange={(e) => handlePaperChange(e.target.value)}
                  className="w-full rounded-xl border px-4 py-3"
                  disabled={loading}
                >
                  <option value="">Select a paper</option>

                  {papers.map((paper) => (
                    <option key={paper.id} value={paper.id}>
                      {paper.code ||
                        paper.description ||
                        paper.exam ||
                        "Paper"}
                    </option>
                  ))}
                </select>

                {papers.length === 0 && !loading && (
                  <p className="mt-2 text-sm text-gray-500">
                    No papers are available for this academy yet.
                  </p>
                )}
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold">
                  Select Batch
                </label>

                <select
                  value={batchId}
                  onChange={(e) => setBatchId(e.target.value)}
                  className="w-full rounded-xl border px-4 py-3"
                  disabled={loading}
                >
                  <option value="">Select a batch</option>

                  {batches.map((batch) => (
                    <option key={batch.id} value={batch.id}>
                      {batch.name}
                      {batch.class_name
                        ? ` — ${batch.class_name}`
                        : ""}
                    </option>
                  ))}
                </select>

                {batches.length === 0 && !loading && (
                  <p className="mt-2 text-sm text-gray-500">
                    No batches are available yet.
                  </p>
                )}
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold">
                  Test Title
                </label>

                <input
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. NEET Physics Weekly Test"
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
                  onChange={(e) => setStartTime(e.target.value)}
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

              {message && (
                <div className="rounded-xl bg-blue-50 p-4 text-sm text-blue-700">
                  {message}
                </div>
              )}

              <button
                onClick={scheduleTest}
                disabled={
                  saving ||
                  loading ||
                  papers.length === 0 ||
                  batches.length === 0
                }
                className="w-full rounded-xl bg-[#315bea] px-5 py-4 font-bold text-white hover:bg-[#264ac7] disabled:cursor-not-allowed disabled:opacity-50"
              >
                {saving ? "Scheduling..." : "Schedule Test"}
              </button>
            </div>
          </div>

          {/* Existing tests */}
          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900">
                Scheduled Tests
              </h2>

              <button
                onClick={loadData}
                className="rounded-lg border px-3 py-2 text-sm font-semibold hover:bg-gray-50"
              >
                Refresh
              </button>
            </div>

            {loading ? (
              <div className="py-12 text-center text-gray-500">
                Loading...
              </div>
            ) : tests.length === 0 ? (
              <div className="py-12 text-center text-gray-500">
                No tests scheduled yet.
              </div>
            ) : (
              <div className="mt-6 space-y-4">
                {tests.map((test) => (
                  <div
                    key={test.id}
                    className="rounded-xl border p-5"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <h3 className="font-bold text-gray-900">
                          {test.title}
                        </h3>

                        <p className="mt-1 text-sm text-gray-500">
                          Batch:{" "}
                          <span className="font-medium text-gray-700">
                            {test.batch_name || "Unknown"}
                          </span>
                        </p>
                      </div>

                      <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-bold text-blue-700">
                        {test.status}
                      </span>
                    </div>

                    <div className="mt-4 grid gap-2 text-sm text-gray-600">
                      <p>
                        <span className="font-semibold">
                          Starts:
                        </span>{" "}
                        {formatDate(test.start_time)}
                      </p>

                      <p>
                        <span className="font-semibold">
                          Ends:
                        </span>{" "}
                        {formatDate(test.end_time)}
                      </p>

                      <p>
                        <span className="font-semibold">
                          Duration:
                        </span>{" "}
                        {test.duration_minutes} minutes
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
