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

function getQuestionText(q: any): string {
  return String(q?.stem ?? q?.question ?? q?.question_text ?? q?.text ?? "");
}

function getQuestionOptions(q: any): string[] {
  const raw = q?.options ?? q?.choices ?? [];
  if (Array.isArray(raw)) return raw.map((item: any) => typeof item === "string" ? item : String(item?.text ?? item?.label ?? item?.value ?? ""));
  if (raw && typeof raw === "object") return Object.entries(raw).map(([key, value]) => `${key}. ${String(value ?? "")}`);
  if (typeof raw === "string") {
    try { const parsed = JSON.parse(raw); if (Array.isArray(parsed)) return parsed.map((item: any) => typeof item === "string" ? item : String(item?.text ?? item?.label ?? "")); } catch {}
  }
  return [];
}

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
  const [allowReattempt, setAllowReattempt] = useState(false);

  const [targetType, setTargetType] =
    useState<"batch" | "student">("batch");

  const [batches, setBatches] = useState<Batch[]>([]);
  const [students, setStudents] = useState<Student[]>([]);

  const [academy, setAcademy] = useState<Academy | null>(null);
  const [teacher, setTeacher] = useState<Teacher | null>(null);

  const [batchId, setBatchId] = useState("");
  const [selectedStudentIds, setSelectedStudentIds] = useState<string[]>([]);

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

      // Honor the batch chosen on Generate Paper; otherwise use the first available batch.
      let requestedBatchId = "";
      try {
        const savedTest = JSON.parse(localStorage.getItem("teacherGeneratedTest") || "{}");
        requestedBatchId = String(savedTest.targetBatchId || "");
      } catch {
        requestedBatchId = "";
      }
      if (nextBatches.length > 0) {
        setTargetType("batch");

        setBatchId((current) => {
          const preferred = requestedBatchId || current;
          return nextBatches.some((batch) => batch.id === preferred)
            ? preferred
            : nextBatches[0].id;
        });

        setSelectedStudentIds([]);
      } else if (nextStudents.length > 0) {
        // If there are no batches, allow individual student assignment.
        setTargetType("student");

        setBatchId("");

        setSelectedStudentIds((current) => current.filter((id) => nextStudents.some((student) => student.id === id)).length > 0
          ? current.filter((id) => nextStudents.some((student) => student.id === id))
          : [nextStudents[0].id]);
      } else {
        setBatchId("");
        setSelectedStudentIds([]);
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

  const questionCount = Array.isArray(test?.questions)
    ? test.questions.length
    : Array.isArray(test?.data?.questions) ? test.data.questions.length : (Number(test?.questionCount) || 0);

  const reviewedQuestions: any[] = Array.isArray(test?.questions)
    ? test.questions
    : Array.isArray(test?.data?.questions) ? test.data.questions : [];

  function updateQuestion(index: number, patch: Record<string, any>) {
    setTest((current: any) => {
      if (!current) return current;
      const nested = !Array.isArray(current.questions) && Array.isArray(current.data?.questions);
      const list = nested ? current.data.questions : (Array.isArray(current.questions) ? current.questions : []);
      const next = list.map((q: any, i: number) => i === index ? { ...q, ...patch } : q);
      const updated = nested ? { ...current, data: { ...current.data, questions: next }, questions: next } : { ...current, questions: next };
      localStorage.setItem("teacherGeneratedTest", JSON.stringify(updated));
      return updated;
    });
  }

  function removeQuestion(index: number) {
    if (reviewedQuestions.length <= 1) {
      setError("A test must contain at least one question.");
      return;
    }
    setTest((current: any) => {
      if (!current) return current;
      const list = Array.isArray(current.questions) ? current.questions : (current.data?.questions || []);
      const next = list.filter((_: any, i: number) => i !== index);
      const updated = { ...current, questions: next, questionCount: next.length, ...(current.data ? { data: { ...current.data, questions: next } } : {}) };
      localStorage.setItem("teacherGeneratedTest", JSON.stringify(updated));
      return updated;
    });
    setError("");
  }

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

    if (targetType === "student" && selectedStudentIds.length === 0) {
      setError("Please select at least one student.");
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
            allowReattempt,
            test,
            batchId:
              targetType === "batch"
                ? batchId
                : null,
            studentIds:
              targetType === "student"
                ? selectedStudentIds
                : [],
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
      <main className="flex min-h-screen items-center justify-center bg-surface-subtle px-6">
        <div className="rounded-2xl border border-border-default bg-white px-8 py-7 text-center shadow-sm">
          <div className="mx-auto h-10 w-10 animate-spin rounded-full border-4 border-border-default border-t-brand-primary" />

          <p className="mt-4 font-semibold text-text-primary">
            Preparing your test…
          </p>

          <p className="mt-1 text-sm text-text-body">
            Loading the generated test.
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-surface-subtle text-text-primary">
      <div className="mx-auto w-full max-w-5xl px-3 py-5 sm:px-5 sm:py-8 md:px-8">

        {/* TOP BAR */}
        <div className="mb-5 flex flex-col items-stretch justify-between gap-3 sm:mb-6 sm:flex-row sm:items-center sm:gap-4">
          <button
            type="button"
            onClick={() =>
              router.push("/teacher/generate")
            }
            className="rounded-xl border border-border-default bg-white px-4 py-2.5 text-sm font-semibold text-text-secondary shadow-sm transition hover:bg-surface-subtle"
          >
            ← Back to Generator
          </button>

          <div className="text-left sm:text-right">
            <p className="text-xs font-bold uppercase tracking-wider text-brand-primary">
              Teacher Portal
            </p>

            <p className="mt-1 text-sm text-text-body">
              {teacher?.name || "Teacher"}

              {academy?.name
                ? ` • ${academy.name}`
                : ""}
            </p>
          </div>
        </div>

        {/* MAIN CARD */}
        <div className="overflow-hidden rounded-3xl border border-border-default bg-white hover:shadow-xl shadow-slate-200/50">

          {/* HEADER */}
          <div className="bg-gradient-to-r from-blue-700 to-indigo-700 px-4 py-5 text-white sm:px-6 sm:py-7 md:px-8">
            <div className="flex flex-wrap items-end justify-between gap-5">

              <div>
                <p className="text-sm font-semibold text-white/90">
                  READY TO PUBLISH
                </p>

                <h1 className="mt-1 text-2xl font-bold tracking-tight sm:text-3xl">
                  Schedule Test
                </h1>

                <p className="mt-2 max-w-2xl text-sm text-white/90">
                  Choose when the test starts and exactly who should receive it.
                </p>
              </div>

              <div className="w-full rounded-2xl bg-white/10 px-4 py-3 backdrop-blur sm:w-auto sm:px-5 sm:py-4">
                <p className="text-xs text-white/90">
                  Generated questions
                </p>

                <p className="mt-1 text-2xl font-bold">
                  {questionCount}
                </p>
              </div>

            </div>
          </div>

          {/* CONTENT */}
          <div className="p-4 sm:p-6 md:p-8">

            {/* MESSAGE */}
            {(error || success) && (
              <div
                className={`mb-7 rounded-2xl border px-4 py-3.5 text-sm font-medium ${
                  error
                    ? "border-state-error/20 bg-state-error/10 text-state-error"
                    : "border-state-success/20 bg-state-success/10 text-state-success"
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

                <p className="mt-1 text-sm text-text-body">
                  Set the title, start time and duration.
                </p>
              </div>

              <div className="grid gap-4 sm:gap-5 md:grid-cols-2">

                <label className="md:col-span-2">
                  <span className="mb-2 block text-sm font-semibold text-text-secondary">
                    Test title
                  </span>

                  <input
                    value={title}
                    onChange={(e) =>
                      setTitle(e.target.value)
                    }
                    className="w-full rounded-xl border border-border-default bg-white px-4 py-3.5 text-text-primary outline-none transition placeholder:text-text-supporting-label focus:border-brand-primary focus:ring-4 focus:ring-brand-primary/10"
                    placeholder="e.g. Physics Weekly Test"
                  />
                </label>

                <label>
                  <span className="mb-2 block text-sm font-semibold text-text-secondary">
                    Start date & time
                  </span>

                  <input
                    type="datetime-local"
                    value={startTime}
                    onChange={(e) =>
                      setStartTime(e.target.value)
                    }
                    className="w-full rounded-xl border border-border-default bg-white px-4 py-3.5 text-text-primary outline-none transition focus:border-brand-primary focus:ring-4 focus:ring-brand-primary/10"
                  />
                </label>

                <label className="md:col-span-2 flex cursor-pointer items-start gap-3 rounded-xl border border-state-warning/20 bg-state-warning/10 px-4 py-3.5">
                  <input type="checkbox" checked={allowReattempt} onChange={(e) => setAllowReattempt(e.target.checked)} className="mt-1 h-4 w-4 accent-blue-600" />
                  <span><strong className="block text-sm text-text-secondary">Allow reattempt after automatic submission</strong><span className="mt-1 block text-xs text-text-body">Students can start this test again only if it was auto-submitted because they changed tabs or the timer ended.</span></span>
                </label>

                <label>
                  <span className="mb-2 block text-sm font-semibold text-text-secondary">
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
                    className="w-full rounded-xl border border-border-default bg-white px-4 py-3.5 text-text-primary outline-none transition focus:border-brand-primary focus:ring-4 focus:ring-brand-primary/10"
                  />
                </label>

              </div>
            </section>

            <div className="my-8 border-t border-border-default" />

            {/* TARGET */}
            <section>

              <div className="mb-5 flex flex-wrap items-end justify-between gap-3">

                <div>
                  <h2 className="text-lg font-bold">
                    2. Who receives it?
                  </h2>

                  <p className="mt-1 text-sm text-text-body">
                    Use a whole batch or assign it to one student.
                  </p>
                </div>

                <button
                  type="button"
                  onClick={loadTargets}
                  disabled={loadingTargets}
                  className="rounded-lg border border-border-default px-3 py-2 text-xs font-semibold text-text-body transition hover:bg-surface-subtle disabled:opacity-50"
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
                    setSelectedStudentIds([]);

                    if (!batchId) {
                      setBatchId(batches[0].id);
                    }
                  }}
                  className={`rounded-2xl border-2 p-4 text-left transition sm:p-5 ${
                    targetType === "batch"
                      ? "border-brand-primary bg-brand-primary/10 shadow-sm"
                      : "border-border-default bg-white hover:border-border-default"
                  }`}
                >
                  <div className="text-2xl">
                    📚
                  </div>

                  <p className="mt-3 font-bold">
                    Assign to a batch
                  </p>

                  <p className="mt-1 text-sm text-text-body">
                    All students assigned to that batch receive the test.
                  </p>

                  <p className="mt-3 text-xs font-semibold text-brand-primary">
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
                    setSelectedStudentIds((current) => current.length > 0 ? current : [students[0].id]);
                  }}
                  className={`rounded-2xl border-2 p-4 text-left transition sm:p-5 ${
                    targetType === "student"
                      ? "border-brand-primary bg-brand-primary/10 shadow-sm"
                      : "border-border-default bg-white hover:border-border-default"
                  }`}
                >
                  <div className="text-2xl">
                    👨‍🎓
                  </div>

                  <p className="mt-3 font-bold">
                    Assign to selected students
                  </p>

                  <p className="mt-1 text-sm text-text-body">
                    Select one or more academy students to receive the test.
                  </p>

                  <p className="mt-3 text-xs font-semibold text-brand-primary">
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
                <div className="mt-5 rounded-2xl border border-border-default bg-surface-subtle p-5">
                  <div className="h-4 w-40 animate-pulse rounded bg-surface-muted" />

                  <div className="mt-3 h-12 animate-pulse rounded-xl bg-surface-muted" />
                </div>
              ) : targetType === "batch" ? (

                /* BATCH */
                <div className="mt-5">

                  <label className="mb-2 block text-sm font-semibold text-text-secondary">
                    Select batch
                  </label>

                  <select
                    value={batchId}
                    onChange={(e) =>
                      setBatchId(e.target.value)
                    }
                    disabled={batches.length === 0}
                    className="w-full rounded-xl border border-border-default bg-white px-4 py-3.5 text-text-primary outline-none transition focus:border-brand-primary focus:ring-4 focus:ring-brand-primary/10 disabled:bg-surface-subtle"
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
                    <div className="mt-3 flex flex-wrap items-center gap-2 rounded-xl bg-brand-primary/10 px-4 py-3 text-sm text-brand-primary">
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
                    <p className="mt-3 rounded-xl bg-state-warning/10 px-4 py-3 text-sm text-state-warning">
                      ⚠️ Create a batch and add students to it before publishing to a batch.
                    </p>
                  )}

                  {selectedBatch &&
                    Number(
                      selectedBatch.student_count || 0
                    ) === 0 && (
                      <p className="mt-3 rounded-xl bg-state-error/10 px-4 py-3 text-sm text-state-error">
                        ⚠️ This batch currently has no students.
                        Add students to the batch before publishing.
                      </p>
                    )}

                </div>
              ) : (

                /* STUDENT */
                <div className="mt-5">

                  <div className="mb-2 flex items-center justify-between">
                    <p className="text-sm font-semibold text-text-secondary">Select students</p>
                    <span className="text-xs font-semibold text-brand-primary">{selectedStudentIds.length} selected</span>
                  </div>

                  <div className="max-h-64 overflow-y-auto rounded-xl border border-border-default bg-white p-2">
                    {students.map((student) => <label key={student.id} className="flex cursor-pointer items-start gap-3 rounded-lg px-3 py-3 hover:bg-brand-primary/10"><input type="checkbox" checked={selectedStudentIds.includes(student.id)} onChange={() => setSelectedStudentIds((current) => current.includes(student.id) ? current.filter((id) => id !== student.id) : [...current, student.id])} className="mt-1 h-4 w-4 accent-blue-600" /><span><strong className="block text-sm text-text-secondary">{student.name}</strong><span className="text-xs text-text-body">{student.email}{student.class_name ? ` · ${student.class_name}` : ""}</span></span></label>)}
                  </div>

                  {!students.length && (
                    <p className="mt-3 rounded-xl bg-state-warning/10 px-4 py-3 text-sm text-state-warning">
                      ⚠️ No students are available in your academy.
                    </p>
                  )}

                </div>
              )}

            </section>

            <div className="my-8 border-t border-border-default" />

            {/* QUESTION REVIEW — must be checked before publishing */}
            <section className="mb-8">
              <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
                <div>
                  <h2 className="text-lg font-bold">3. Review your questions</h2>
                  <p className="mt-1 text-sm text-text-body">Check each question, edit wording/options/answer/explanation, or remove a question before students receive the paper.</p>
                </div>
                <span className="rounded-full bg-state-warning/20 px-3 py-1 text-xs font-bold text-state-warning">Professor review required</span>
              </div>
              <div className="space-y-4">
                {reviewedQuestions.map((q: any, index: number) => {
                  const text = getQuestionText(q);
                  const options = getQuestionOptions(q);
                  const answerValue = String(q?.correct_option ?? q?.correctOption ?? q?.correct_answer ?? q?.answer ?? "");
                  const explanation = String(q?.solution ?? q?.explanation ?? q?.correct_answer_text ?? "");
                  const figure = q?.figure_asset ?? q?.figureAsset ?? q?.figure_url ?? null;
                  return <article key={String(q?.id ?? index) + "-" + index} className="rounded-2xl border border-border-default bg-white p-4 shadow-sm sm:p-5">
                    <div className="mb-3 flex items-start justify-between gap-3">
                      <div><p className="text-xs font-bold uppercase tracking-wide text-brand-primary">Question {index + 1}</p><p className="mt-1 text-xs text-text-body">{q?.subject || "Subject"}{q?.chapter_name || q?.chapter ? ` · ${q.chapter_name || q.chapter}` : ""}{q?.difficulty ? ` · ${q.difficulty}` : ""}</p></div>
                      <button type="button" onClick={() => removeQuestion(index)} className="shrink-0 rounded-lg border border-state-error/20 px-3 py-2 text-xs font-bold text-state-error hover:bg-state-error/10">Remove</button>
                    </div>
                    <label className="block"><span className="mb-1 block text-xs font-semibold text-text-body">Question text</span><textarea rows={3} value={text} onChange={(e) => updateQuestion(index, { stem: e.target.value, question: e.target.value, question_text: e.target.value })} className="w-full rounded-xl border border-border-default px-3 py-2.5 text-sm text-text-primary focus:border-brand-action-blue focus:outline-none" /></label>
                    {figure && <div className="mt-3 rounded-lg bg-surface-subtle p-2 text-xs text-text-body">Diagram/figure attached: {String(figure).slice(0, 140)}</div>}
                    {options.length > 0 && <div className="mt-3 grid gap-3 sm:grid-cols-2">{options.map((option, oi) => <label key={oi} className="block"><span className="mb-1 block text-xs font-semibold text-text-body">Option {String.fromCharCode(65 + oi)}</span><input value={option} onChange={(e) => { const next = [...options]; next[oi] = e.target.value; updateQuestion(index, { options: next }); }} className="w-full rounded-xl border border-border-default px-3 py-2.5 text-sm text-text-primary focus:border-brand-action-blue focus:outline-none" /></label>)}</div>}
                    <div className="mt-3 grid gap-3 sm:grid-cols-2"><label className="block"><span className="mb-1 block text-xs font-semibold text-text-body">Correct answer (option letter or answer)</span><input value={answerValue} onChange={(e) => updateQuestion(index, { correct_option: e.target.value, correctOption: e.target.value, correct_answer: e.target.value })} className="w-full rounded-xl border border-border-default px-3 py-2.5 text-sm text-text-primary focus:border-brand-action-blue focus:outline-none" /></label><label className="block"><span className="mb-1 block text-xs font-semibold text-text-body">Explanation / solution</span><textarea rows={2} value={explanation} onChange={(e) => updateQuestion(index, { solution: e.target.value, explanation: e.target.value, correct_answer_text: e.target.value })} className="w-full rounded-xl border border-border-default px-3 py-2.5 text-sm text-text-primary focus:border-brand-action-blue focus:outline-none" /></label></div>
                  </article>;
                })}
              </div>
              <p className="mt-3 text-xs text-text-body">Changes are saved in this draft on your device. Review the correct answer carefully before publishing.</p>
            </section>

            {/* SUMMARY */}
            <section>
              <div className="rounded-2xl border border-border-default bg-surface-subtle p-5">

                <div className="flex flex-wrap items-center justify-between gap-4">

                  <div>
                    <p className="text-sm font-semibold text-text-secondary">
                      Test summary
                    </p>

                    <p className="mt-1 text-sm text-text-body">
                      {questionCount} questions •{" "}
                      {duration} minutes
                    </p>
                  </div>

                  <div className="text-left sm:text-right">

                    <p className="text-xs uppercase tracking-wide text-text-supporting-label">
                      Destination
                    </p>

                    <p className="mt-1 font-bold text-text-primary">
                      {targetType === "batch"
                        ? selectedBatch?.name ||
                          "Select a batch"
                        : selectedStudentIds.length > 0
                          ? `${selectedStudentIds.length} student${selectedStudentIds.length === 1 ? "" : "s"}`
                          : "Select students"}
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
                  selectedStudentIds.length === 0)
              }
              className="mt-7 w-full rounded-2xl bg-brand-primary px-5 py-4 text-base font-bold text-white shadow-lg shadow-brand-primary/20 transition hover:bg-brand-action-blue hover:shadow-xl disabled:cursor-not-allowed disabled:bg-surface-muted disabled:shadow-none"
            >
              {loading
                ? "Publishing test…"
                : "✓ Approve Questions & Publish Test"}
            </button>

          </div>
        </div>
      </div>
    </main>
  );
}
