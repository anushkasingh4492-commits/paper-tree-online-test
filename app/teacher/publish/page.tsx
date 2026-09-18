"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

type Batch = {
  id: string;
  name: string;
  class_name?: string | null;
  student_count?: number;
};

type Student = {
  id: string;
  name: string;
  email: string;
  class_name?: string | null;
};

type Teacher = {
  id: string;
  name: string;
  email: string;
};

type Academy = {
  id: string;
  name: string;
  code?: string | null;
};

type TargetResponse = {
  success: boolean;
  error?: string;
  academyId?: string;
  academy?: Academy | null;
  teacher?: Teacher;
  batches?: Batch[];
  students?: Student[];
};

function toLocalDateTimeValue(date: Date) {
  const pad = (n: number) => String(n).padStart(2, "0");

  return (
    [
      date.getFullYear(),
      pad(date.getMonth() + 1),
      pad(date.getDate()),
    ].join("-") +
    `T${pad(date.getHours())}:${pad(date.getMinutes())}`
  );
}

export default function TeacherPublishPage() {
  const router = useRouter();

  const [test, setTest] = useState<any>(null);

  const [title, setTitle] = useState("Scheduled Test");
  const [startTime, setStartTime] = useState("");
  const [duration, setDuration] = useState(60);

  const [targetType, setTargetType] =
    useState<"batch" | "student">("batch");

  const [batches, setBatches] = useState<Batch[]>([]);
  const [students, setStudents] = useState<Student[]>([]);

  const [academy, setAcademy] = useState<Academy | null>(null);
  const [teacher, setTeacher] = useState<Teacher | null>(null);

  const [batchId, setBatchId] = useState("");
  const [studentId, setStudentId] = useState("");

  const [loadingTest, setLoadingTest] = useState(true);
  const [loadingTargets, setLoadingTargets] = useState(true);
  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    const saved = localStorage.getItem("teacherGeneratedTest");

    if (!saved) {
      router.push("/teacher/generate");
      return;
    }

    try {
      const data = JSON.parse(saved);

      setTest(data);

      if (data.title) {
        setTitle(String(data.title));
      } else if (data.questionCount) {
        setTitle(`Test - ${data.questionCount} Questions`);
      }

      if (data.duration) {
        setDuration(Math.max(1, Number(data.duration)));
      }

      // Give the teacher a usable default start time.
      const defaultStart = new Date(
        Date.now() + 10 * 60 * 1000
      );

      defaultStart.setSeconds(0, 0);

      setStartTime(toLocalDateTimeValue(defaultStart));
    } catch {
      router.push("/teacher/generate");
    } finally {
      setLoadingTest(false);
    }
  }, [router]);

  async function loadTargets() {
    setLoadingTargets(true);
    setError("");

    try {
      const response = await fetch("/api/teacher/targets", {
        method: "GET",
        credentials: "include",
        cache: "no-store",
      });

      const data: TargetResponse = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.error || "Could not load your academy data."
        );
      }

      const nextBatches = Array.isArray(data.batches)
        ? data.batches
        : [];

      const nextStudents = Array.isArray(data.students)
        ? data.students
        : [];

      setBatches(nextBatches);
      setStudents(nextStudents);

      setAcademy(data.academy || null);
      setTeacher(data.teacher || null);

      // Automatically select the first available batch.
      if (nextBatches.length > 0) {
        setTargetType("batch");

        setBatchId((current) =>
          nextBatches.some((batch) => batch.id === current)
            ? current
            : nextBatches[0].id
        );

        setStudentId("");
      } else if (nextStudents.length > 0) {
        // If there are no batches, allow individual student assignment.
        setTargetType("student");

        setBatchId("");

        setStudentId((current) =>
          nextStudents.some((student) => student.id === current)
            ? current
            : nextStudents[0].id
        );
      } else {
        setBatchId("");
        setStudentId("");
      }
    } catch (err) {
      console.error("LOAD TEACHER TARGETS ERROR:", err);

      setError(
        err instanceof Error
          ? err.message
          : "Could not load your academy data."
      );
    } finally {
      setLoadingTargets(false);
    }
  }

  useEffect(() => {
    loadTargets();
  }, []);

  const selectedBatch = useMemo(
    () =>
      batches.find((batch) => batch.id === batchId) || null,
    [batches, batchId]
  );

  const selectedStudent = useMemo(
    () =>
      students.find((student) => student.id === studentId) ||
      null,
    [students, studentId]
  );

  const questionCount =
    Number(test?.questionCount) ||
    (Array.isArray(test?.questions)
      ? test.questions.length
      : Array.isArray(test?.data?.questions)
        ? test.data.questions.length
        : 0);

  async function publishTest() {
    setError("");
    setSuccess("");

    if (!startTime) {
      setError("Please select the test start time.");
      return;
    }

    if (duration < 1) {
      setError("Duration must be at least 1 minute.");
      return;
    }

    if (questionCount < 1) {
      setError("This test does not contain any questions.");
      return;
    }

    if (targetType === "batch" && !batchId) {
      setError("Please select a batch.");
      return;
    }

    if (targetType === "student" && !studentId) {
      setError("Please select a student.");
      return;
    }

    if (
      targetType === "batch" &&
      selectedBatch &&
      Number(selectedBatch.student_count || 0) === 0
    ) {
      setError(
        "This batch has no students. Add students to the batch first."
      );
      return;
    }

    setLoading(true);

    try {
      const start = new Date(startTime);

      if (Number.isNaN(start.getTime())) {
        throw new Error("Invalid start date and time.");
      }

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
          credentials: "include",
          body: JSON.stringify({
            title: title.trim() || "Scheduled Test",
            startTime: start.toISOString(),
            endTime: end.toISOString(),
            duration,
            test,
            batchId:
              targetType === "batch"
                ? batchId
                : null,
            studentId:
              targetType === "student"
                ? studentId
                : null,
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

      setSuccess(
        `🚀 Test published! ${Number(data.notifiedStudents || 0)} student${
          Number(data.notifiedStudents || 0) === 1 ? "" : "s"
        } notified.`
      );

      setTimeout(() => {
        router.push("/teacher");
      }, 1400);
    } catch (err) {
      console.error("PUBLISH TEST ERROR:", err);

      setError(
        err instanceof Error
          ? err.message
          : "Could not publish test."
      );
    } finally {
      setLoading(false);
    }
  }

  if (loadingTest || !test) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-50 px-6">
        <div className="rounded-2xl border border-slate-200 bg-white px-8 py-7 text-center shadow-sm">
          <div className="mx-auto h-10 w-10 animate-spin rounded-full border-4 border-slate-200 border-t-blue-600" />

          <p className="mt-4 font-semibold text-slate-900">
            Preparing your test…
          </p>

          <p className="mt-1 text-sm text-slate-500">
            Loading the generated test.
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-5xl px-5 py-8 md:px-8">

        {/* TOP BAR */}
        <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
          <button
            type="button"
            onClick={() =>
              router.push("/teacher/generate")
            }
            className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 shadow-sm transition hover:bg-slate-50"
          >
            ← Back to Generator
          </button>

          <div className="text-right">
            <p className="text-xs font-bold uppercase tracking-wider text-blue-600">
              Teacher Portal
            </p>

            <p className="mt-1 text-sm text-slate-500">
              {teacher?.name || "Teacher"}

              {academy?.name
                ? ` • ${academy.name}`
                : ""}
            </p>
          </div>
        </div>

        {/* MAIN CARD */}
        <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-xl shadow-slate-200/50">

          {/* HEADER */}
          <div className="bg-gradient-to-r from-blue-700 to-indigo-700 px-6 py-7 text-white md:px-8">
            <div className="flex flex-wrap items-end justify-between gap-5">

              <div>
                <p className="text-sm font-semibold text-blue-100">
                  READY TO PUBLISH
                </p>

                <h1 className="mt-1 text-3xl font-bold tracking-tight">
                  Schedule Test
                </h1>

                <p className="mt-2 max-w-2xl text-sm text-blue-100">
                  Choose when the test starts and exactly who should receive it.
                </p>
              </div>

              <div className="rounded-2xl bg-white/10 px-5 py-4 backdrop-blur">
                <p className="text-xs text-blue-100">
                  Generated questions
                </p>

                <p className="mt-1 text-2xl font-bold">
                  {questionCount}
                </p>
              </div>

            </div>
          </div>

          {/* CONTENT */}
          <div className="p-6 md:p-8">

            {/* MESSAGE */}
            {(error || success) && (
              <div
                className={`mb-7 rounded-2xl border px-4 py-3.5 text-sm font-medium ${
                  error
                    ? "border-red-200 bg-red-50 text-red-700"
                    : "border-emerald-200 bg-emerald-50 text-emerald-700"
                }`}
              >
                {error || success}
              </div>
            )}

            {/* TEST DETAILS */}
            <section>
              <div className="mb-5">
                <h2 className="text-lg font-bold">
                  1. Test details
                </h2>

                <p className="mt-1 text-sm text-slate-500">
                  Set the title, start time and duration.
                </p>
              </div>

              <div className="grid gap-5 md:grid-cols-2">

                <label className="md:col-span-2">
                  <span className="mb-2 block text-sm font-semibold text-slate-700">
                    Test title
                  </span>

                  <input
                    value={title}
                    onChange={(e) =>
                      setTitle(e.target.value)
                    }
                    className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3.5 text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-600 focus:ring-4 focus:ring-blue-100"
                    placeholder="e.g. Physics Weekly Test"
                  />
                </label>

                <label>
                  <span className="mb-2 block text-sm font-semibold text-slate-700">
                    Start date & time
                  </span>

                  <input
                    type="datetime-local"
                    value={startTime}
                    onChange={(e) =>
                      setStartTime(e.target.value)
                    }
                    className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3.5 text-slate-900 outline-none transition focus:border-blue-600 focus:ring-4 focus:ring-blue-100"
                  />
                </label>

                <label>
                  <span className="mb-2 block text-sm font-semibold text-slate-700">
                    Duration (minutes)
                  </span>

                  <input
                    type="number"
                    min={1}
                    value={duration}
                    onChange={(e) =>
                      setDuration(
                        Math.max(
                          1,
                          Number(e.target.value) || 1
                        )
                      )
                    }
                    className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3.5 text-slate-900 outline-none transition focus:border-blue-600 focus:ring-4 focus:ring-blue-100"
                  />
                </label>

              </div>
            </section>

            <div className="my-8 border-t border-slate-200" />

            {/* TARGET */}
            <section>

              <div className="mb-5 flex flex-wrap items-end justify-between gap-3">

                <div>
                  <h2 className="text-lg font-bold">
                    2. Who receives it?
                  </h2>

                  <p className="mt-1 text-sm text-slate-500">
                    Use a whole batch or assign it to one student.
                  </p>
                </div>

                <button
                  type="button"
                  onClick={loadTargets}
                  disabled={loadingTargets}
                  className="rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-600 transition hover:bg-slate-50 disabled:opacity-50"
                >
                  {loadingTargets
                    ? "Refreshing…"
                    : "↻ Refresh"}
                </button>

              </div>

              {/* TARGET OPTIONS */}
              <div className="grid gap-3 md:grid-cols-2">

                <button
                  type="button"
                  onClick={() => {
                    if (batches.length === 0) {
                      setError(
                        "No batches exist in this academy yet."
                      );
                      return;
                    }

                    setError("");
                    setSuccess("");

                    setTargetType("batch");
                    setStudentId("");

                    if (!batchId) {
                      setBatchId(batches[0].id);
                    }
                  }}
                  className={`rounded-2xl border-2 p-5 text-left transition ${
                    targetType === "batch"
                      ? "border-blue-600 bg-blue-50 shadow-sm"
                      : "border-slate-200 bg-white hover:border-slate-300"
                  }`}
                >
                  <div className="text-2xl">
                    📚
                  </div>

                  <p className="mt-3 font-bold">
                    Assign to a batch
                  </p>

                  <p className="mt-1 text-sm text-slate-500">
                    All students assigned to that batch receive the test.
                  </p>

                  <p className="mt-3 text-xs font-semibold text-blue-700">
                    {batches.length}{" "}
                    {batches.length === 1
                      ? "batch"
                      : "batches"}{" "}
                    available
                  </p>
                </button>

                <button
                  type="button"
                  onClick={() => {
                    if (students.length === 0) {
                      setError(
                        "No students exist in this academy yet."
                      );
                      return;
                    }

                    setError("");
                    setSuccess("");

                    setTargetType("student");
                    setBatchId("");

                    if (!studentId) {
                      setStudentId(students[0].id);
                    }
                  }}
                  className={`rounded-2xl border-2 p-5 text-left transition ${
                    targetType === "student"
                      ? "border-blue-600 bg-blue-50 shadow-sm"
                      : "border-slate-200 bg-white hover:border-slate-300"
                  }`}
                >
                  <div className="text-2xl">
                    👨‍🎓
                  </div>

                  <p className="mt-3 font-bold">
                    Assign to one student
                  </p>

                  <p className="mt-1 text-sm text-slate-500">
                    Only the selected academy student receives the test.
                  </p>

                  <p className="mt-3 text-xs font-semibold text-blue-700">
                    {students.length}{" "}
                    {students.length === 1
                      ? "student"
                      : "students"}{" "}
                    available
                  </p>
                </button>

              </div>

              {/* LOADING */}
              {loadingTargets ? (
                <div className="mt-5 rounded-2xl border border-slate-200 bg-slate-50 p-5">
                  <div className="h-4 w-40 animate-pulse rounded bg-slate-200" />

                  <div className="mt-3 h-12 animate-pulse rounded-xl bg-slate-200" />
                </div>
              ) : targetType === "batch" ? (

                /* BATCH */
                <div className="mt-5">

                  <label className="mb-2 block text-sm font-semibold text-slate-700">
                    Select batch
                  </label>

                  <select
                    value={batchId}
                    onChange={(e) =>
                      setBatchId(e.target.value)
                    }
                    disabled={batches.length === 0}
                    className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3.5 text-slate-900 outline-none transition focus:border-blue-600 focus:ring-4 focus:ring-blue-100 disabled:bg-slate-100"
                  >
                    <option value="">
                      {batches.length
                        ? "Select a batch"
                        : "No batches available"}
                    </option>

                    {batches.map((batch) => (
                      <option
                        key={batch.id}
                        value={batch.id}
                      >
                        {batch.name}

                        {batch.class_name
                          ? ` — ${batch.class_name}`
                          : ""}

                        {typeof batch.student_count ===
                          "number"
                          ? ` (${batch.student_count} students)`
                          : ""}
                      </option>
                    ))}
                  </select>

                  {selectedBatch && (
                    <div className="mt-3 flex flex-wrap items-center gap-2 rounded-xl bg-blue-50 px-4 py-3 text-sm text-blue-800">
                      <span>📚</span>

                      <strong>
                        {selectedBatch.name}
                      </strong>

                      {selectedBatch.class_name && (
                        <span>
                          • {selectedBatch.class_name}
                        </span>
                      )}

                      <span>
                        •{" "}
                        {selectedBatch.student_count ||
                          0}{" "}
                        students
                      </span>
                    </div>
                  )}

                  {!batches.length && (
                    <p className="mt-3 rounded-xl bg-amber-50 px-4 py-3 text-sm text-amber-700">
                      ⚠️ Create a batch and add students to it before publishing to a batch.
                    </p>
                  )}

                  {selectedBatch &&
                    Number(
                      selectedBatch.student_count || 0
                    ) === 0 && (
                      <p className="mt-3 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700">
                        ⚠️ This batch currently has no students.
                        Add students to the batch before publishing.
                      </p>
                    )}

                </div>
              ) : (

                /* STUDENT */
                <div className="mt-5">

                  <label className="mb-2 block text-sm font-semibold text-slate-700">
                    Select student
                  </label>

                  <select
                    value={studentId}
                    onChange={(e) =>
                      setStudentId(e.target.value)
                    }
                    disabled={students.length === 0}
                    className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3.5 text-slate-900 outline-none transition focus:border-blue-600 focus:ring-4 focus:ring-blue-100 disabled:bg-slate-100"
                  >
                    <option value="">
                      {students.length
                        ? "Select a student"
                        : "No students available"}
                    </option>

                    {students.map((student) => (
                      <option
                        key={student.id}
                        value={student.id}
                      >
                        {student.name}
                        {" — "}
                        {student.email}

                        {student.class_name
                          ? ` — ${student.class_name}`
                          : ""}
                      </option>
                    ))}
                  </select>

                  {selectedStudent && (
                    <div className="mt-3 flex flex-wrap items-center gap-2 rounded-xl bg-emerald-50 px-4 py-3 text-sm text-emerald-800">
                      <span>👨‍🎓</span>

                      <strong>
                        {selectedStudent.name}
                      </strong>

                      <span>
                        • {selectedStudent.email}
                      </span>

                      {selectedStudent.class_name && (
                        <span>
                          • {selectedStudent.class_name}
                        </span>
                      )}
                    </div>
                  )}

                  {!students.length && (
                    <p className="mt-3 rounded-xl bg-amber-50 px-4 py-3 text-sm text-amber-700">
                      ⚠️ No students are available in your academy.
                    </p>
                  )}

                </div>
              )}

            </section>

            <div className="my-8 border-t border-slate-200" />

            {/* SUMMARY */}
            <section>
              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">

                <div className="flex flex-wrap items-center justify-between gap-4">

                  <div>
                    <p className="text-sm font-semibold text-slate-700">
                      Test summary
                    </p>

                    <p className="mt-1 text-sm text-slate-500">
                      {questionCount} questions •{" "}
                      {duration} minutes
                    </p>
                  </div>

                  <div className="text-right">

                    <p className="text-xs uppercase tracking-wide text-slate-400">
                      Destination
                    </p>

                    <p className="mt-1 font-bold text-slate-900">
                      {targetType === "batch"
                        ? selectedBatch?.name ||
                          "Select a batch"
                        : selectedStudent?.name ||
                          "Select a student"}
                    </p>

                  </div>

                </div>
              </div>
            </section>

            {/* PUBLISH */}
            <button
              type="button"
              onClick={publishTest}
              disabled={
                loading ||
                loadingTargets ||
                questionCount < 1 ||
                (targetType === "batch" &&
                  (!batchId ||
                    Number(
                      selectedBatch?.student_count || 0
                    ) === 0)) ||
                (targetType === "student" &&
                  !studentId)
              }
              className="mt-7 w-full rounded-2xl bg-blue-600 px-5 py-4 text-base font-bold text-white shadow-lg shadow-blue-600/20 transition hover:bg-blue-700 hover:shadow-xl disabled:cursor-not-allowed disabled:bg-slate-300 disabled:shadow-none"
            >
              {loading
                ? "Publishing test…"
                : "🚀 Publish & Notify Students"}
            </button>

          </div>
        </div>
      </div>
    </main>
  );
}
