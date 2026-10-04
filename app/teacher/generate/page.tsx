"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import "katex/dist/katex.min.css";
import { BlockMath, InlineMath } from "react-katex";

type SchemaRow = {
  exam: string;
  subject: string;
  chapter_name: string;
  difficulty: string;
  total: number;
};

type Question = {
  id: string | number;
  question?: string;
  question_text?: string;
  text?: string;
  stem?: string;

  options?: unknown;
  answer?: unknown;
  correct_answer?: unknown;

  difficulty?: string;
  subject?: string;
  chapter_name?: string;
  chapter?: string;
  exam?: string;
  question_type?: string;
  type?: string;

  explanation?: string;
  figure_asset?: string;
  figureAsset?: string;
};

type PreviewResponse = {
  success: boolean;
  availableQuestions?: Question[];
  availableQuestionCount?: number;
  previewOffset?: number;
  previewLimit?: number;
  error?: string;
};

type GenerateResponse = {
  success: boolean;
  testId?: string;
  questions?: Question[];
  error?: string;
};

function getQuestionText(question: Question) {
  return (
    question.question ??
    question.question_text ??
    question.text ??
    question.stem ??
    "Question text unavailable"
  );
}

function getOptions(options: unknown): string[] {
  if (!options) {
    return [];
  }

  if (Array.isArray(options)) {
    return options.map((option) => String(option));
  }

  if (typeof options === "object") {
    return Object.entries(options as Record<string, unknown>).map(
      ([key, value]) => `${key}. ${String(value)}`
    );
  }

  if (typeof options === "string") {
    try {
      const parsed = JSON.parse(options);

      if (Array.isArray(parsed)) {
        return parsed.map((option) => String(option));
      }

      if (parsed && typeof parsed === "object") {
        return Object.entries(parsed).map(
          ([key, value]) => `${key}. ${String(value)}`
        );
      }
    } catch {
      // Not JSON, so just show it as text.
    }

    return [options];
  }

  return [];
}

function getFigureSrc(value: unknown): string | null {
  if (typeof value !== "string" || !value.trim()) return null;
  const asset = value.trim();
  return /^(https?:|data:|blob:|\/)/.test(asset)
    ? asset
    : `/api/question-asset?path=${encodeURIComponent(asset)}`;
}

function MathText({ text }: { text: string }) {
  const parts = String(text || "").split(
    /(\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$[^$\n]+\$)/g
  );

  return (
    <>
      {parts.map((part, index) => {
        if (!part) return null;
        if (part.startsWith("$$") && part.endsWith("$$")) {
          return <span key={index} className="my-2 block overflow-x-auto"><BlockMath math={part.slice(2, -2)} errorColor="#64748b" /></span>;
        }
        if (part.startsWith("\\[") && part.endsWith("\\]")) {
          return <span key={index} className="my-2 block overflow-x-auto"><BlockMath math={part.slice(2, -2)} errorColor="#64748b" /></span>;
        }
        if (part.startsWith("\\(") && part.endsWith("\\)")) {
          return <InlineMath key={index} math={part.slice(2, -2)} errorColor="#64748b" />;
        }
        if (part.startsWith("$") && part.endsWith("$")) {
          return <InlineMath key={index} math={part.slice(1, -1)} errorColor="#64748b" />;
        }
        return <span key={index}>{part}</span>;
      })}
    </>
  );
}

export default function TeacherGeneratePage() {
  const router = useRouter();

  const [rows, setRows] = useState<SchemaRow[]>([]);

  const [exam, setExam] = useState("MHT-CET");
  const [selectedSubjects, setSelectedSubjects] = useState<string[]>([
    "Physics",
  ]);
  const [chaptersBySubject, setChaptersBySubject] = useState<
    Record<string, string[]>
  >({});
  const [difficulty, setDifficulty] = useState("Balanced");

  const [questionCount, setQuestionCount] = useState(10);
  const [duration, setDuration] = useState(30);

  const [questions, setQuestions] = useState<Question[]>([]);
  const [selectedQuestionIds, setSelectedQuestionIds] = useState<Set<string>>(
    new Set()
  );

  const [showCustomForm, setShowCustomForm] = useState(false);
  const [customStem, setCustomStem] = useState("");
  const [customOptions, setCustomOptions] = useState(["", "", "", ""]);
  const [customCorrect, setCustomCorrect] = useState("A");
  const [customSubject, setCustomSubject] = useState("Physics");
  const [customChapter, setCustomChapter] = useState("Custom Questions");
  const [customDifficulty, setCustomDifficulty] = useState("Medium");
  const [customSolution, setCustomSolution] = useState("");
  const [customSaving, setCustomSaving] = useState(false);

  const [loadingQuestions, setLoadingQuestions] = useState(false);
  const [loading, setLoading] = useState(false);

  const [schemaError, setSchemaError] = useState("");
  const [error, setError] = useState("");

  const PREVIEW_PAGE_SIZE = 25;
  const [previewPage, setPreviewPage] = useState(0);
  const [previewTotal, setPreviewTotal] = useState(0);
  const previewAbortRef = useRef<AbortController | null>(null);

  /*
   * Load the database schema used for the dropdowns.
   */
  useEffect(() => {
    fetch("/api/db-schema")
      .then(async (res) => {
        const data = await res.json();

        if (!res.ok || !data.success) {
          throw new Error(
            data.error || "Could not load question database."
          );
        }

        setRows(data.data || []);
      })
      .catch((err) => {
        setSchemaError(
          err instanceof Error
            ? err.message
            : "Could not load question database."
        );
      });
  }, []);

  /*
   * Subjects available for the selected exam.
   */
  const subjects = useMemo(() => {
    const values = rows
      .filter(
        (row) =>
          String(row.exam).trim().toLowerCase() ===
          String(exam).trim().toLowerCase()
      )
      .map((row) => row.subject)
      .filter(Boolean);

    const unique = Array.from(new Set(values));

    // NEET should not show Mathematics.
    return unique.filter(
      (item) =>
        exam !== "NEET" ||
        String(item).trim().toLowerCase() !== "mathematics"
    );
  }, [rows, exam]);

  useEffect(() => {
    if (selectedSubjects.length > 0) {
      const nextSubject = selectedSubjects.includes(customSubject)
        ? customSubject
        : selectedSubjects[0];
      setCustomSubject(nextSubject);

      const selectedChapters = chaptersBySubject[nextSubject] || [];
      if (selectedChapters.length > 0 && !selectedChapters.includes(customChapter)) {
        setCustomChapter(selectedChapters[0]);
      }
    }
  }, [selectedSubjects, chaptersBySubject, customSubject, customChapter]);

  /*
   * Chapters available for each selected subject.
   */
  const chaptersBySelectedSubject = useMemo(() => {
    const result: Record<string, string[]> = {};

    for (const selectedSubject of selectedSubjects) {
      const values = rows
        .filter(
          (row) =>
            String(row.exam).trim().toLowerCase() ===
              String(exam).trim().toLowerCase() &&
            String(row.subject).trim().toLowerCase() ===
              String(selectedSubject).trim().toLowerCase()
        )
        .map((row) => row.chapter_name)
        .filter(Boolean);

      result[selectedSubject] = Array.from(new Set(values));
    }

    return result;
  }, [rows, exam, selectedSubjects]);

  /*
   * Number of currently selected questions.
   */
  const selectedCount = selectedQuestionIds.size;

  /*
   * Whether the exact requested number has been selected.
   */
  const exactCountSelected = selectedCount === questionCount;

  /*
   * Load every question matching the currently selected filters.
   *
   * This expects /api/tests/generate to support:
   *
   * {
   *   previewOnly: true
   * }
   *
   * and return:
   *
   * {
   *   availableQuestions: [...]
   * }
   */
  async function loadQuestions(page = 0) {
    setError("");

    if (selectedSubjects.length === 0) {
      setQuestions([]);
      setPreviewTotal(0);
      return;
    }

    previewAbortRef.current?.abort();
    const controller = new AbortController();
    previewAbortRef.current = controller;

    setLoadingQuestions(true);

    try {
      const response = await fetch("/api/tests/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        signal: controller.signal,
        body: JSON.stringify({
          previewOnly: true,
          previewOffset: page * PREVIEW_PAGE_SIZE,
          previewLimit: PREVIEW_PAGE_SIZE,
          exam,
          subjects: selectedSubjects,
          chapters: [],
          chaptersBySubject,
          difficulty,
          questionCount,
          duration,
        }),
      });

      const data: PreviewResponse = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.error || "Failed to load matching questions."
        );
      }

      setQuestions(data.availableQuestions || []);
      setPreviewTotal(Number(data.availableQuestionCount || 0));
      setPreviewPage(page);
    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") {
        return;
      }

      setQuestions([]);
      setPreviewTotal(0);

      setError(
        err instanceof Error
          ? err.message
          : "Failed to load matching questions."
      );
    } finally {
      if (previewAbortRef.current === controller) {
        setLoadingQuestions(false);
      }
    }
  }

  /*
   * Reload only a small page of questions. The old implementation
   * downloaded every matching question into Chrome, which could
   * create a very large DOM and cause the browser to freeze.
   */
  useEffect(() => {
    setPreviewPage(0);

    const timer = window.setTimeout(() => {
      void loadQuestions(0);
    }, 300);

    return () => {
      window.clearTimeout(timer);
    };

    // loadQuestions intentionally uses the current filter state.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [exam, selectedSubjects, chaptersBySubject, difficulty]);

  function handleExamChange(value: string) {
    setExam(value);
    setSelectedSubjects([]);
    setChaptersBySubject({});
    setQuestions([]);
    setPreviewTotal(0);
    setPreviewPage(0);
    setSelectedQuestionIds(new Set());
  }

  function toggleSubject(value: string) {
    setSelectedSubjects((current) => {
      const alreadySelected = current.includes(value);

      if (alreadySelected) {
        setChaptersBySubject((previous) => {
          const next = { ...previous };
          delete next[value];
          return next;
        });
        return current.filter((item) => item !== value);
      }

      /*
       * MHT-CET can be PCM or PCB, so Mathematics and Biology
       * remain mutually exclusive, while multiple other subjects
       * can be selected together.
       */
      if (exam === "MHT-CET" && value === "Mathematics") {
        setChaptersBySubject((previous) => {
          const next = { ...previous };
          delete next.Biology;
          return next;
        });
        return [...current.filter((item) => item !== "Biology"), value];
      }

      if (exam === "MHT-CET" && value === "Biology") {
        setChaptersBySubject((previous) => {
          const next = { ...previous };
          delete next.Mathematics;
          return next;
        });
        return [...current.filter((item) => item !== "Mathematics"), value];
      }

      return [...current, value];
    });

    setSelectedQuestionIds(new Set());
  }

  function toggleChapter(subjectName: string, chapterName: string) {
    setChaptersBySubject((current) => {
      const currentChapters = current[subjectName] || [];
      const nextChapters = currentChapters.includes(chapterName)
        ? currentChapters.filter((chapter) => chapter !== chapterName)
        : [...currentChapters, chapterName];

      return {
        ...current,
        [subjectName]: nextChapters,
      };
    });

    setSelectedQuestionIds(new Set());
  }

  function goToPreviewPage(nextPage: number) {
    const maxPage = Math.max(
      0,
      Math.ceil(previewTotal / PREVIEW_PAGE_SIZE) - 1
    );

    const safePage = Math.max(0, Math.min(nextPage, maxPage));

    void loadQuestions(safePage);
  }

  /*
   * Toggle one question.
   */
  function toggleQuestion(questionId: string | number) {
    const id = String(questionId);

    setSelectedQuestionIds((previous) => {
      const next = new Set(previous);

      if (next.has(id)) {
        next.delete(id);
      } else {
        /*
         * Do not allow selecting more than the requested number.
         */
        if (next.size >= questionCount) {
          return next;
        }

        next.add(id);
      }

      return next;
    });
  }

  /*
   * Select every currently displayed question.
   *
   * If there are more questions than requested, only the first N
   * are selected because the test must contain exactly questionCount.
   */
  function selectAllRequired() {
    const ids = questions
      .slice(0, questionCount)
      .map((question) => String(question.id));

    setSelectedQuestionIds(new Set(ids));
  }

  /*
   * Clear all selections.
   */
  function clearSelection() {
    setSelectedQuestionIds(new Set());
  }

  async function createCustomQuestion() {
    setError("");

    if (!customStem.trim()) {
      setError("Write the custom question first.");
      return;
    }

    const options = customOptions.map((value) => value.trim()).filter(Boolean);

    if (options.length < 2) {
      setError("Add at least two answer options.");
      return;
    }

    const correctIndex = ["A", "B", "C", "D"].indexOf(customCorrect);
    if (correctIndex < 0 || correctIndex >= options.length) {
      setError("Choose a valid correct option.");
      return;
    }

    if (!customSubject.trim()) {
      setError("Choose a subject for the custom question.");
      return;
    }

    setCustomSaving(true);

    try {
      const response = await fetch("/api/teacher/questions/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          exam,
          subject: customSubject,
          chapterName: customChapter.trim() || "Custom Questions",
          difficulty: customDifficulty,
          stem: customStem.trim(),
          options,
          correctOption: customCorrect,
          solution: customSolution.trim(),
        }),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || "Could not create custom question.");
      }

      const created = data.question as Question | null;
      const createdId = String(data.questionId || created?.id || "");

      if (!createdId || !created) {
        throw new Error("Custom question was created but could not be loaded.");
      }

      setQuestions((current) => [created, ...current.filter((item) => String(item.id) !== createdId)]);
      setSelectedQuestionIds((current) => {
        const next = new Set(current);
        if (next.size < questionCount) next.add(createdId);
        return next;
      });
      setPreviewTotal((current) => current + 1);
      setCustomStem("");
      setCustomOptions(["", "", "", ""]);
      setCustomSolution("");
      setShowCustomForm(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not create custom question.");
    } finally {
      setCustomSaving(false);
    }
  }

  /*
   * Generate the actual test from the exact selected question IDs.
   */
  async function generatePaper() {
    setError("");

    if (selectedSubjects.length === 0) {
      setError("Please select at least one subject.");
      return;
    }

    if (questions.length === 0) {
      setError("No matching questions are available.");
      return;
    }

    if (!exactCountSelected) {
      setError(
        `Please select exactly ${questionCount} questions. You currently selected ${selectedCount}.`
      );
      return;
    }

    setLoading(true);

    try {
      const questionIds = Array.from(selectedQuestionIds);

      const response = await fetch("/api/tests/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          exam,

          subjects: selectedSubjects,

          chapters: [],

          chaptersBySubject,

          difficulty,

          questionCount,

          duration,

          /*
           * IMPORTANT:
           * These are the exact questions selected by the teacher.
           */
          questionIds,
        }),
      });

      const data: GenerateResponse = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.error || "Failed to generate paper."
        );
      }

      /*
       * Keep the existing publish flow.
       */
      localStorage.setItem(
        "teacherGeneratedTest",
        JSON.stringify(data)
      );

      router.push("/teacher/publish");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to generate paper."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <div className="mx-auto w-full max-w-6xl px-3 py-5 sm:px-6 sm:py-10">
        <button
          onClick={() => router.push("/teacher")}
          className="mb-6 text-sm font-semibold text-[#315bea]"
        >
          ← Back to Teacher Portal
        </button>

        <div className="rounded-2xl bg-white p-4 shadow-sm sm:p-8">
          {/* HEADER */}
          <div className="mb-8">
            <p className="text-sm font-bold uppercase tracking-wider text-[#315bea]">
              Teacher Portal
            </p>

            <h1 className="mt-2 text-3xl font-bold">
              Generate Paper
            </h1>

            <p className="mt-2 text-gray-500">
              Select multiple subjects and their chapters, review matching questions,
              and choose the exact questions for the test.
            </p>
          </div>

          <div className="sticky top-2 z-10 mb-6 flex flex-col items-stretch justify-between gap-3 sm:top-4 sm:mb-8 sm:flex-row sm:items-center sm:gap-4 rounded-2xl border border-blue-200 bg-blue-50/95 p-4 shadow-lg shadow-blue-900/10 backdrop-blur">
            <div>
              <p className="text-sm font-bold text-blue-950">{selectedCount} / {questionCount} questions selected</p>
              <p className="mt-1 text-xs text-blue-800">Choose questions below, then continue to publish.</p>
            </div>
            <button
              type="button"
              onClick={generatePaper}
              disabled={loading || loadingQuestions || selectedSubjects.length === 0 || !exactCountSelected}
              className="w-full rounded-xl bg-[#315bea] px-5 py-3 text-sm font-bold sm:w-auto text-white shadow-sm transition hover:bg-[#264ac7] disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Opening Publish..." : "Generate & Publish Paper"}
            </button>
          </div>

          {/* CUSTOM QUESTION */}
          <section className="mb-8 rounded-2xl border border-emerald-200 bg-emerald-50/60 p-4 sm:p-5">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-base font-extrabold text-emerald-950 sm:text-lg">Add a custom question</h2>
                <p className="mt-1 text-sm text-emerald-800">
                  Professors can write institute-specific questions and add them directly to this test.
                </p>
              </div>
              <button
                type="button"
                onClick={() => setShowCustomForm((value) => !value)}
                className="w-full rounded-xl bg-emerald-600 px-4 py-2.5 text-sm font-bold sm:w-auto text-white hover:bg-emerald-700"
              >
                {showCustomForm ? "Close" : "+ Add Custom Question"}
              </button>
            </div>

            {showCustomForm && (
              <div className="mt-5 grid gap-3 md:grid-cols-2">
                <textarea
                  value={customStem}
                  onChange={(e) => setCustomStem(e.target.value)}
                  placeholder="Write the question"
                  rows={4}
                  className="md:col-span-2 w-full rounded-xl border border-emerald-200 bg-white px-4 py-3 text-sm outline-none focus:border-emerald-500"
                />

                {customOptions.map((value, index) => (
                  <input
                    key={index}
                    value={value}
                    onChange={(e) =>
                      setCustomOptions((current) =>
                        current.map((item, itemIndex) =>
                          itemIndex === index ? e.target.value : item
                        )
                      )
                    }
                    placeholder={`Option ${String.fromCharCode(65 + index)}`}
                    className="rounded-xl border border-emerald-200 bg-white px-4 py-3 text-sm outline-none focus:border-emerald-500"
                  />
                ))}

                <select
                  value={customSubject}
                  onChange={(e) => setCustomSubject(e.target.value)}
                  className="rounded-xl border border-emerald-200 bg-white px-4 py-3 text-sm"
                >
                  <option value="">Select subject</option>
                  {subjects.map((item) => <option key={item} value={item}>{item}</option>)}
                </select>

                <input
                  value={customChapter}
                  onChange={(e) => setCustomChapter(e.target.value)}
                  placeholder="Chapter"
                  className="rounded-xl border border-emerald-200 bg-white px-4 py-3 text-sm"
                />

                <select
                  value={customCorrect}
                  onChange={(e) => setCustomCorrect(e.target.value)}
                  className="rounded-xl border border-emerald-200 bg-white px-4 py-3 text-sm"
                >
                  {['A','B','C','D'].map((option) => <option key={option} value={option}>Correct answer: {option}</option>)}
                </select>

                <select
                  value={customDifficulty}
                  onChange={(e) => setCustomDifficulty(e.target.value)}
                  className="rounded-xl border border-emerald-200 bg-white px-4 py-3 text-sm"
                >
                  <option>Easy</option>
                  <option>Medium</option>
                  <option>Hard</option>
                </select>

                <textarea
                  value={customSolution}
                  onChange={(e) => setCustomSolution(e.target.value)}
                  placeholder="Solution / explanation (optional)"
                  rows={3}
                  className="md:col-span-2 rounded-xl border border-emerald-200 bg-white px-4 py-3 text-sm outline-none focus:border-emerald-500"
                />

                <button
                  type="button"
                  onClick={() => void createCustomQuestion()}
                  disabled={customSaving || loading || selectedQuestionIds.size >= questionCount}
                  className="md:col-span-2 rounded-xl bg-emerald-600 px-4 py-3 text-sm font-bold text-white hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {customSaving ? "Saving..." : selectedQuestionIds.size >= questionCount ? "Question limit reached" : "Add Question to This Test"}
                </button>
              </div>
            )}
          </section>

          {/* FILTERS */}
          <div className="grid gap-6 md:grid-cols-2">
            {/* EXAM */}
            <div>
              <label className="mb-2 block text-sm font-semibold">
                Exam
              </label>

              <select
                value={exam}
                onChange={(e) =>
                  handleExamChange(e.target.value)
                }
                className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 outline-none focus:border-[#315bea]"
              >
                <option value="MHT-CET">MHT-CET</option>
                <option value="NEET">NEET</option>
              </select>
            </div>

            {/* SUBJECTS */}
            <div className="md:col-span-2">
              <label className="mb-2 block text-sm font-semibold">
                Subjects
              </label>

              <div className="grid gap-3 sm:grid-cols-2">
                {subjects.map((item) => {
                  const selected = selectedSubjects.includes(item);

                  return (
                    <label
                      key={item}
                      className={`flex cursor-pointer items-center gap-3 rounded-xl border px-4 py-3 transition ${
                        selected
                          ? "border-[#315bea] bg-blue-50"
                          : "border-gray-300 bg-white hover:border-blue-300"
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={selected}
                        onChange={() => toggleSubject(item)}
                        className="h-4 w-4 accent-[#315bea]"
                      />
                      <span className="text-sm font-semibold">{item}</span>
                    </label>
                  );
                })}
              </div>

              <p className="mt-2 text-xs text-gray-500">
                Select multiple subjects. For MHT-CET, Mathematics and Biology remain mutually exclusive (PCM or PCB).
              </p>
            </div>

            {/* CHAPTERS BY SUBJECT */}
            <div className="md:col-span-2">
              <p className="mb-2 text-sm font-semibold">Chapters by subject</p>

              {selectedSubjects.length === 0 ? (
                <div className="rounded-xl border border-dashed border-gray-300 bg-gray-50 p-5 text-sm text-gray-500">
                  Select at least one subject to choose chapters.
                </div>
              ) : (
                <div className="space-y-4">
                  {selectedSubjects.map((selectedSubject) => {
                    const availableChapters =
                      chaptersBySelectedSubject[selectedSubject] || [];
                    const chosenChapters =
                      chaptersBySubject[selectedSubject] || [];

                    return (
                      <div
                        key={selectedSubject}
                        className="rounded-xl border border-gray-200 bg-gray-50 p-4"
                      >
                        <div className="mb-3 flex items-center justify-between">
                          <p className="text-sm font-bold">{selectedSubject}</p>
                          <span className="text-xs text-gray-500">
                            {chosenChapters.length === 0
                              ? "All chapters"
                              : `${chosenChapters.length} selected`}
                          </span>
                        </div>

                        {availableChapters.length === 0 ? (
                          <p className="text-sm text-gray-500">
                            No chapters found for this subject.
                          </p>
                        ) : (
                          <div className="grid max-h-56 gap-2 overflow-y-auto sm:grid-cols-2">
                            {availableChapters.map((chapter) => (
                              <label
                                key={chapter}
                                className="flex cursor-pointer items-start gap-2 rounded-lg px-2 py-2 text-sm hover:bg-white"
                              >
                                <input
                                  type="checkbox"
                                  checked={chosenChapters.includes(chapter)}
                                  onChange={() =>
                                    toggleChapter(selectedSubject, chapter)
                                  }
                                  className="mt-0.5 h-4 w-4 accent-[#315bea]"
                                />
                                <span>{chapter}</span>
                              </label>
                            ))}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}

              <p className="mt-2 text-xs text-gray-500">
                Leave a subject's chapters unchecked to include all chapters for that subject.
              </p>
            </div>

            {/* DIFFICULTY */}
            <div>
              <label className="mb-2 block text-sm font-semibold">
                Difficulty
              </label>

              <select
                value={difficulty}
                onChange={(e) =>
                  setDifficulty(e.target.value)
                }
                className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 outline-none focus:border-[#315bea]"
              >
                <option value="Balanced">
                  Balanced
                </option>

                <option value="Easy">
                  Easy
                </option>

                <option value="Challenging">
                  Challenging
                </option>

                <option value="Difficult">
                  Difficult
                </option>
              </select>
            </div>

            {/* QUESTION COUNT */}
            <div>
              <label className="mb-2 block text-sm font-semibold">
                Questions
              </label>

              <input
                type="number"
                min={1}
                max={200}
                value={questionCount}
                onChange={(e) => {
                  const value = Math.max(
                    1,
                    Math.min(
                      200,
                      Number(e.target.value) || 1
                    )
                  );

                  setQuestionCount(value);

                  /*
                   * If the new requested count is smaller than
                   * the current selection, trim the selection.
                   */
                  setSelectedQuestionIds((previous) => {
                    if (previous.size <= value) {
                      return previous;
                    }

                    return new Set(
                      Array.from(previous).slice(0, value)
                    );
                  });
                }}
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-[#315bea]"
              />
            </div>

            {/* DURATION */}
            <div>
              <label className="mb-2 block text-sm font-semibold">
                Duration (minutes)
              </label>

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
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-[#315bea]"
              />
            </div>
          </div>

          {/* SCHEMA ERROR */}
          {schemaError && (
            <div className="mt-6 rounded-xl bg-red-50 p-4 text-sm text-red-600">
              {schemaError}
            </div>
          )}

          {/* ERROR */}
          {error && (
            <div className="mt-6 rounded-xl bg-red-50 p-4 text-sm text-red-600">
              {error}
            </div>
          )}

          {/* QUESTION SECTION */}
          <div className="mt-10 border-t pt-8">
            <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
              <div>
                <h2 className="text-xl font-bold">
                  Matching Questions
                </h2>

                <p className="mt-1 text-sm text-gray-500">
                  {loadingQuestions
                    ? "Loading a small page of matching questions..."
                    : `${previewTotal} question${
                        previewTotal === 1 ? "" : "s"
                      } match the selected filters.`}
                </p>
              </div>

              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  onClick={() => void loadQuestions(previewPage)}
                  disabled={
                    loadingQuestions || selectedSubjects.length === 0
                  }
                  className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-semibold transition hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {loadingQuestions
                    ? "Loading..."
                    : "Refresh Questions"}
                </button>

                <button
                  type="button"
                  onClick={selectAllRequired}
                  disabled={
                    questions.length === 0 ||
                    questionCount <= 0
                  }
                  className="rounded-lg bg-gray-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  Select Visible Questions
                </button>

                <button
                  type="button"
                  onClick={clearSelection}
                  disabled={selectedCount === 0}
                  className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-semibold transition hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  Clear
                </button>
              </div>
            </div>

            {/* SELECTION STATUS */}
            {questions.length > 0 && (
              <div
                className={`mt-6 rounded-xl border p-4 ${
                  exactCountSelected
                    ? "border-green-200 bg-green-50"
                    : "border-blue-200 bg-blue-50"
                }`}
              >
                <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                  <div>
                    <p className="font-bold">
                      {selectedCount} / {questionCount} selected
                    </p>

                    <p className="text-sm text-gray-600">
                      {exactCountSelected
                        ? "Perfect. You can generate the test."
                        : selectedCount < questionCount
                        ? `Select ${
                            questionCount - selectedCount
                          } more question${
                            questionCount - selectedCount === 1
                              ? ""
                              : "s"
                          }.`
                        : `Remove ${
                            selectedCount - questionCount
                          } question${
                            selectedCount - questionCount === 1
                              ? ""
                              : "s"
                          }.`}
                    </p>
                  </div>

                  <span className="text-sm font-semibold">
                    {previewTotal} available
                  </span>
                </div>
              </div>
            )}

            {/* LOADING */}
            {loadingQuestions && (
              <div className="mt-6 rounded-xl border bg-gray-50 p-8 text-center">
                <p className="font-semibold">
                  Loading questions...
                </p>

                <p className="mt-1 text-sm text-gray-500">
                  Loading only 25 questions at a time to keep the browser fast.
                </p>
              </div>
            )}

            {/* NO QUESTIONS */}
            {!loadingQuestions &&
              selectedSubjects.length > 0 &&
              questions.length === 0 && (
                <div className="mt-6 rounded-xl border border-dashed bg-gray-50 p-8 text-center">
                  <p className="font-semibold">
                    No matching questions found.
                  </p>

                  <p className="mt-1 text-sm text-gray-500">
                    Try another chapter or difficulty.
                  </p>
                </div>
              )}

            {/* QUESTIONS */}
            {!loadingQuestions &&
              questions.length > 0 && (
                <div className="mt-6 space-y-4">
                  {questions.map((question, index) => {
                    const id = String(question.id);

                    const selected =
                      selectedQuestionIds.has(id);

                    const options = getOptions(
                      question.options
                    );

                    const questionText =
                      getQuestionText(question);

                    const figureSrc = getFigureSrc(
                      question.figure_asset ?? question.figureAsset
                    );

                    return (
                      <label
                        key={id}
                        className={`block cursor-pointer rounded-2xl border p-3 transition sm:p-5 ${
                          selected
                            ? "border-[#315bea] bg-blue-50"
                            : "border-gray-200 bg-white hover:border-gray-300"
                        }`}
                      >
                        <div className="flex gap-4">
                          {/* CHECKBOX */}
                          <div className="pt-1">
                            <input
                              type="checkbox"
                              checked={selected}
                              onChange={() =>
                                toggleQuestion(
                                  question.id
                                )
                              }
                              className="h-5 w-5 cursor-pointer accent-[#315bea]"
                            />
                          </div>

                          {/* QUESTION */}
                          <div className="min-w-0 flex-1">
                            <div className="flex flex-wrap items-center gap-2">
                              <span className="text-sm font-bold text-[#315bea]">
                                Question {previewPage * PREVIEW_PAGE_SIZE + index + 1}
                              </span>

                              {question.difficulty && (
                                <span className="rounded-full bg-gray-100 px-2 py-1 text-xs font-semibold text-gray-600">
                                  {question.difficulty}
                                </span>
                              )}

                              {question.question_type && (
                                <span className="rounded-full bg-gray-100 px-2 py-1 text-xs font-semibold text-gray-600">
                                  {question.question_type}
                                </span>
                              )}

                              {question.type &&
                                !question.question_type && (
                                  <span className="rounded-full bg-gray-100 px-2 py-1 text-xs font-semibold text-gray-600">
                                    {question.type}
                                  </span>
                                )}
                            </div>

                            <p className="mt-3 whitespace-pre-wrap text-base font-medium leading-7 text-[#172033]">
                              <MathText text={questionText} />
                            </p>

                            {figureSrc && (
                              <img
                                src={figureSrc}
                                alt={`Figure for question ${index + 1}`}
                                className="mt-4 max-h-80 max-w-full rounded-xl border border-gray-200 bg-white object-contain"
                                onError={(event) => {
                                  event.currentTarget.style.display = "none";
                                }}
                              />
                            )}

                            {/* OPTIONS */}
                            {options.length > 0 && (
                              <div className="mt-4 grid gap-2 md:grid-cols-2">
                                {options.map(
                                  (option, optionIndex) => (
                                    <div
                                      key={`${id}-option-${optionIndex}`}
                                      className="rounded-lg border border-gray-200 bg-gray-50 px-3 py-2 text-sm text-gray-700"
                                    >
                                      <MathText text={option} />
                                    </div>
                                  )
                                )}
                              </div>
                            )}

                            {/* METADATA */}
                            <div className="mt-4 flex flex-wrap gap-x-5 gap-y-1 text-xs text-gray-500">
                              {question.subject && (
                                <span>
                                  Subject:{" "}
                                  <strong>
                                    {question.subject}
                                  </strong>
                                </span>
                              )}

                              {(question.chapter_name ||
                                question.chapter) && (
                                <span>
                                  Chapter:{" "}
                                  <strong>
                                    {question.chapter_name ??
                                      question.chapter}
                                  </strong>
                                </span>
                              )}

                              {question.exam && (
                                <span>
                                  Exam:{" "}
                                  <strong>
                                    {question.exam}
                                  </strong>
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                      </label>
                    );
                  })}
                </div>
              )}


            {!loadingQuestions && previewTotal > PREVIEW_PAGE_SIZE && (
              <div className="mt-6 flex items-center justify-between gap-2 rounded-xl border bg-white p-3 sm:p-4">
                <button
                  type="button"
                  onClick={() => goToPreviewPage(previewPage - 1)}
                  disabled={previewPage === 0}
                  className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-semibold disabled:cursor-not-allowed disabled:opacity-40"
                >
                  Previous
                </button>

                <span className="text-sm font-semibold text-gray-600">
                  Page {previewPage + 1} of {Math.ceil(previewTotal / PREVIEW_PAGE_SIZE)}
                </span>

                <button
                  type="button"
                  onClick={() => goToPreviewPage(previewPage + 1)}
                  disabled={
                    previewPage >=
                    Math.ceil(previewTotal / PREVIEW_PAGE_SIZE) - 1
                  }
                  className="rounded-lg bg-[#315bea] px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-40"
                >
                  Next
                </button>
              </div>
            )}
          </div>

        </div>
      </div>
    </main>
  );
}
