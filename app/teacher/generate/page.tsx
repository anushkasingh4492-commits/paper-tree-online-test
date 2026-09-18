"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

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
  return /^(https?:|data:|blob:|\/)/.test(asset) ? asset : `/${asset}`;
}

export default function TeacherGeneratePage() {
  const router = useRouter();

  const [rows, setRows] = useState<SchemaRow[]>([]);

  const [exam, setExam] = useState("MHT-CET");
  const [subject, setSubject] = useState("Physics");
  const [chapter, setChapter] = useState("");
  const [difficulty, setDifficulty] = useState("Balanced");

  const [questionCount, setQuestionCount] = useState(10);
  const [duration, setDuration] = useState(30);

  const [questions, setQuestions] = useState<Question[]>([]);
  const [selectedQuestionIds, setSelectedQuestionIds] = useState<Set<string>>(
    new Set()
  );

  const [loadingQuestions, setLoadingQuestions] = useState(false);
  const [loading, setLoading] = useState(false);

  const [schemaError, setSchemaError] = useState("");
  const [error, setError] = useState("");

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

  /*
   * Chapters available for the selected exam + subject.
   */
  const chapters = useMemo(() => {
    if (!subject) {
      return [];
    }

    const values = rows
      .filter(
        (row) =>
          String(row.exam).trim().toLowerCase() ===
            String(exam).trim().toLowerCase() &&
          String(row.subject).trim().toLowerCase() ===
            String(subject).trim().toLowerCase()
      )
      .map((row) => row.chapter_name)
      .filter(Boolean);

    return Array.from(new Set(values));
  }, [rows, exam, subject]);

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
  async function loadQuestions() {
    setError("");
    setSelectedQuestionIds(new Set());

    if (!subject) {
      setQuestions([]);
      return;
    }

    setLoadingQuestions(true);

    try {
      const response = await fetch("/api/tests/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          previewOnly: true,

          exam,

          subjects: [subject],

          chapters: chapter ? [chapter] : [],

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
    } catch (err) {
      setQuestions([]);

      setError(
        err instanceof Error
          ? err.message
          : "Failed to load matching questions."
      );
    } finally {
      setLoadingQuestions(false);
    }
  }

  /*
   * Automatically reload questions when the filtering options change.
   *
   * Question count and duration do not affect which questions match,
   * so they are intentionally not dependencies here.
   */
  useEffect(() => {
    if (!subject) {
      setQuestions([]);
      setSelectedQuestionIds(new Set());
      return;
    }

    const timer = window.setTimeout(() => {
      loadQuestions();
    }, 300);

    return () => {
      window.clearTimeout(timer);
    };

    // loadQuestions intentionally uses the current filter state.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [exam, subject, chapter, difficulty]);

  /*
   * Reset subject/chapter when exam changes.
   */
  function handleExamChange(value: string) {
    setExam(value);
    setSubject("");
    setChapter("");
    setQuestions([]);
    setSelectedQuestionIds(new Set());
  }

  /*
   * Reset chapter when subject changes.
   */
  function handleSubjectChange(value: string) {
    setSubject(value);
    setChapter("");
    setQuestions([]);
    setSelectedQuestionIds(new Set());
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
   * Select the first N currently displayed questions.
   */
  function selectRequiredQuestions() {
    const ids = questions
      .slice(0, questionCount)
      .map((question) => String(question.id));

    setSelectedQuestionIds(new Set(ids));
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

  /*
   * Generate the actual test from the exact selected question IDs.
   */
  async function generatePaper() {
    setError("");

    if (!subject) {
      setError("Please select a subject.");
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

          subjects: [subject],

          chapters: chapter ? [chapter] : [],

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
      <div className="mx-auto max-w-6xl px-6 py-10">
        <button
          onClick={() => router.push("/teacher")}
          className="mb-6 text-sm font-semibold text-[#315bea]"
        >
          ← Back to Teacher Portal
        </button>

        <div className="rounded-2xl bg-white p-8 shadow-sm">
          {/* HEADER */}
          <div className="mb-8">
            <p className="text-sm font-bold uppercase tracking-wider text-[#315bea]">
              Teacher Portal
            </p>

            <h1 className="mt-2 text-3xl font-bold">
              Generate Paper
            </h1>

            <p className="mt-2 text-gray-500">
              Select the requirements, review all matching questions,
              and choose the exact questions for the test.
            </p>
          </div>

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

            {/* SUBJECT */}
            <div>
              <label className="mb-2 block text-sm font-semibold">
                Subject
              </label>

              <select
                value={subject}
                onChange={(e) =>
                  handleSubjectChange(e.target.value)
                }
                className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 outline-none focus:border-[#315bea]"
              >
                <option value="">
                  Select subject
                </option>

                {subjects.map((item) => (
                  <option key={item} value={item}>
                    {item}
                  </option>
                ))}
              </select>
            </div>

            {/* CHAPTER */}
            <div className="md:col-span-2">
              <label className="mb-2 block text-sm font-semibold">
                Chapter
              </label>

              <select
                value={chapter}
                onChange={(e) =>
                  setChapter(e.target.value)
                }
                className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 outline-none focus:border-[#315bea]"
              >
                <option value="">
                  All chapters
                </option>

                {chapters.map((item) => (
                  <option key={item} value={item}>
                    {item}
                  </option>
                ))}
              </select>
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
                    ? "Loading matching questions..."
                    : `${questions.length} question${
                        questions.length === 1 ? "" : "s"
                      } match the selected filters.`}
                </p>
              </div>

              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  onClick={loadQuestions}
                  disabled={
                    loadingQuestions || !subject
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
                  Select First {questionCount}
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
                    {questions.length} available
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
                  Finding every question matching your selection.
                </p>
              </div>
            )}

            {/* NO QUESTIONS */}
            {!loadingQuestions &&
              subject &&
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
                        className={`block cursor-pointer rounded-2xl border p-5 transition ${
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
                                Question {index + 1}
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
                              {questionText}
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
                                      {option}
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
          </div>

          {/* GENERATE BUTTON */}
          <div className="mt-10 border-t pt-8">
            <button
              onClick={generatePaper}
              disabled={
                loading ||
                loadingQuestions ||
                !subject ||
                !exactCountSelected
              }
              className="w-full rounded-xl bg-[#315bea] px-5 py-4 font-bold text-white transition hover:bg-[#264ac7] disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading
                ? "Generating Paper..."
                : exactCountSelected
                ? `Generate Paper with ${questionCount} Selected Questions`
                : `Select Exactly ${questionCount} Questions`}
            </button>

            {!exactCountSelected &&
              questions.length > 0 && (
                <p className="mt-3 text-center text-sm text-gray-500">
                  You must select exactly {questionCount} questions
                  before generating the paper.
                </p>
              )}
          </div>
        </div>
      </div>
    </main>
  );
}
