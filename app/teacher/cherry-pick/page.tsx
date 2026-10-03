
"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

type Question = {
  id: string;
  exam: string;
  subject: string;
  standard?: number;
  chapter_number?: number;
  chapter_name?: string;
  major_topic?: string;
  subtopic?: string;
  concept_tested?: string;
  stem: string;
  options?: unknown;
  correct_option?: string;
  correct_answer_text?: string;
  solution?: string;
  formula_principle?: string;
  difficulty?: string;
  estimated_time?: string;
  question_type?: string;
  figure_asset?: string;
};

type SchemaRow = {
  exam: string;
  subject: string;
  chapter_name: string;
  difficulty: string;
  total: number;
};

function getOptions(options: unknown): string[] {
  if (!options) return [];
  if (Array.isArray(options)) return options.map((option) => String(option));

  if (typeof options === "object") {
    return Object.entries(options as Record<string, unknown>).map(
      ([key, value]) => `${key}. ${String(value)}`
    );
  }

  if (typeof options === "string") {
    try {
      return getOptions(JSON.parse(options));
    } catch {
      return [options];
    }
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

export default function CherryPickPage() {
  const router = useRouter();

  const [questions, setQuestions] = useState<Question[]>([]);
  const [schemaRows, setSchemaRows] = useState<SchemaRow[]>([]);
  const [selected, setSelected] = useState<string[]>([]);

  const [exam, setExam] = useState("MHT-CET");
  const [subject, setSubject] = useState("");
  const [chapter, setChapter] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [search, setSearch] = useState("");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showCustomForm, setShowCustomForm] = useState(false);
  const [customStem, setCustomStem] = useState("");
  const [customOptions, setCustomOptions] = useState(["", "", "", ""]);
  const [customCorrect, setCustomCorrect] = useState("A");
  const [customSubject, setCustomSubject] = useState("");
  const [customChapter, setCustomChapter] = useState("");
  const [customDifficulty, setCustomDifficulty] = useState("Medium");
  const [customSolution, setCustomSolution] = useState("");
  const [customSaving, setCustomSaving] = useState(false);
  const [canCustomQuestions, setCanCustomQuestions] = useState<boolean | null>(null);

  /*
   * Load the complete database schema.
   *
   * This gives us ALL available:
   * - exams
   * - subjects
   * - chapters
   * - difficulties
   *
   * It does NOT depend on the 200-question limit
   * of /api/teacher/questions.
   */
  useEffect(() => {
    void fetch("/api/academy/tier", { cache: "no-store", credentials: "include" })
      .then((response) => response.json())
      .then((data) => { if (data?.success) setCanCustomQuestions(Boolean(data.features?.customQuestions)); })
      .catch(() => undefined);
  }, []);

  useEffect(() => {
    async function loadSchema() {
      try {
        const response = await fetch("/api/db-schema");

        const data = await response.json();

        if (!response.ok || !data.success) {
          throw new Error(
            data.error || "Failed to load database schema."
          );
        }

        setSchemaRows(data.data || []);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load database schema."
        );
      }
    }

    loadSchema();
  }, []);

  /*
   * Subjects come from the COMPLETE schema,
   * not from the currently loaded questions.
   */
  const subjects = useMemo(() => {
    return Array.from(
      new Set(
        schemaRows
          .filter((row) => row.exam === exam)
          .map((row) => row.subject)
          .filter(Boolean)
      )
    );
  }, [schemaRows, exam]);

  /*
   * Chapters also come from the COMPLETE schema.
   */
  const chapters = useMemo(() => {
    return Array.from(
      new Set(
        schemaRows
          .filter(
            (row) =>
              row.exam === exam &&
              (!subject || row.subject === subject)
          )
          .map((row) => row.chapter_name)
          .filter(Boolean)
      )
    );
  }, [schemaRows, exam, subject]);

  /*
   * Load actual questions according to the selected filters.
   */
  async function loadQuestions() {
    try {
      setLoading(true);
      setError("");

      const params = new URLSearchParams();

      params.set("exam", exam);

      if (subject) {
        params.set("subject", subject);
      }

      if (chapter) {
        params.set("chapter", chapter);
      }

      if (difficulty) {
        params.set("difficulty", difficulty);
      }

      if (search.trim()) {
        params.set("search", search.trim());
      }

      const response = await fetch(
        `/api/teacher/questions?${params.toString()}`
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.error || "Failed to load questions."
        );
      }

      setQuestions(data.questions || []);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to load questions."
      );
    } finally {
      setLoading(false);
    }
  }

  /*
   * Reload questions when the main filters change.
   */
  useEffect(() => {
    loadQuestions();
  }, [exam, subject, chapter, difficulty]);

  function toggleQuestion(id: string) {
    setSelected((current) =>
      current.includes(id)
        ? current.filter((item) => item !== id)
        : [...current, id]
    );
  }

  function toggleAllQuestions() {
    const visibleIds = questions.map((question) => question.id);
    const everyVisibleQuestionIsSelected = visibleIds.every((id) =>
      selected.includes(id)
    );

    setSelected((current) =>
      everyVisibleQuestionIsSelected
        ? current.filter((id) => !visibleIds.includes(id))
        : Array.from(new Set([...current, ...visibleIds]))
    );
  }

  function continueToPublish() {
    if (selected.length === 0) {
      setError("Please select at least one question.");
      return;
    }

    const selectedQuestions = questions.filter((q) =>
      selected.includes(q.id)
    );

    localStorage.setItem(
      "teacherGeneratedTest",
      JSON.stringify({
        success: true,
        exam,
        difficulty: "Cherry Pick",
        questions: selectedQuestions,
        questionCount: selectedQuestions.length,
      })
    );

    router.push("/teacher/publish");
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <div className="mx-auto max-w-7xl px-6 py-10">

        <button
          onClick={() => router.push("/teacher")}
          className="mb-6 text-sm font-semibold text-[#315bea]"
        >
          ← Back to Teacher Portal
        </button>

        <div className="mb-8">
          <p className="text-sm font-bold uppercase tracking-wider text-[#315bea]">
            Teacher Portal
          </p>

          <h1 className="mt-2 text-3xl font-extrabold">
            Cherry Pick Questions
          </h1>

          <p className="mt-2 text-sm text-[#697386]">
            Select exactly which questions you want in the test.
          </p>
        </div>

        {canCustomQuestions !== false && (
        <section className="mb-6 rounded-2xl border border-[#dfe4ee] bg-white p-5 shadow-sm">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div><h2 className="font-extrabold">Create Your Own Question</h2><p className="mt-1 text-xs text-[#697386]">Write institute-specific questions and immediately add them to your question bank.</p></div>
            <button type="button" onClick={() => setShowCustomForm((v) => !v)} className="rounded-xl bg-[#315bea] px-4 py-2.5 text-sm font-bold text-white">{showCustomForm ? "Close" : "+ Add Your Own Question"}</button>
          </div>
          {showCustomForm && (
            <div className="mt-5 grid gap-3 md:grid-cols-2">
              <textarea value={customStem} onChange={(e) => setCustomStem(e.target.value)} placeholder="Question text" rows={4} className="md:col-span-2 rounded-xl border border-[#dfe4ee] px-4 py-3 text-sm" />
              {customOptions.map((value, index) => <input key={index} value={value} onChange={(e) => setCustomOptions((current) => current.map((item, i) => i === index ? e.target.value : item))} placeholder={`Option ${String.fromCharCode(65 + index)}`} className="rounded-xl border border-[#dfe4ee] px-4 py-3 text-sm" />)}
              <input value={customSubject} onChange={(e) => setCustomSubject(e.target.value)} placeholder="Subject" className="rounded-xl border border-[#dfe4ee] px-4 py-3 text-sm" />
              <input value={customChapter} onChange={(e) => setCustomChapter(e.target.value)} placeholder="Chapter" className="rounded-xl border border-[#dfe4ee] px-4 py-3 text-sm" />
              <select value={customCorrect} onChange={(e) => setCustomCorrect(e.target.value)} className="rounded-xl border border-[#dfe4ee] bg-white px-4 py-3 text-sm">{["A","B","C","D"].map((x) => <option key={x}>{x}</option>)}</select>
              <select value={customDifficulty} onChange={(e) => setCustomDifficulty(e.target.value)} className="rounded-xl border border-[#dfe4ee] bg-white px-4 py-3 text-sm"><option>Easy</option><option>Medium</option><option>Hard</option></select>
              <textarea value={customSolution} onChange={(e) => setCustomSolution(e.target.value)} placeholder="Solution / explanation (optional)" rows={3} className="md:col-span-2 rounded-xl border border-[#dfe4ee] px-4 py-3 text-sm" />
              <button type="button" disabled={customSaving} onClick={async () => {
                setCustomSaving(true); setError("");
                try {
                  const response = await fetch("/api/teacher/questions/create", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ stem: customStem, options: customOptions, correctOption: customCorrect, subject: customSubject, chapterName: customChapter, difficulty: customDifficulty, solution: customSolution, exam }) });
                  const data = await response.json();
                  if (!response.ok || !data.success) throw new Error(data.error || "Could not create question.");
                  setShowCustomForm(false); setCustomStem(""); setCustomOptions(["", "", "", ""]); setCustomSolution("");
                  await loadQuestions();
                  setError("Question added successfully.");
                } catch (err) { setError(err instanceof Error ? err.message : "Could not create question."); } finally { setCustomSaving(false); }
              }} className="md:col-span-2 rounded-xl bg-[#16a36a] px-4 py-3 text-sm font-bold text-white disabled:opacity-50">{customSaving ? "Saving..." : "Save to Question Bank"}</button>
            </div>
          )}
        </section>
        )}

        <section className="mb-6 rounded-2xl border border-[#e5e8ef] bg-white p-5 shadow-sm">

          <div className="grid gap-4 md:grid-cols-4">

            {/* EXAM */}

            <select
              value={exam}
              onChange={(e) => {
                setExam(e.target.value);
                setSubject("");
                setChapter("");
                setSelected([]);
              }}
              className="rounded-xl border px-4 py-3 text-sm"
            >
              <option value="MHT-CET">MHT-CET</option>
              <option value="NEET">NEET</option>
            </select>

            {/* SUBJECT */}

            <select
              value={subject}
              onChange={(e) => {
                setSubject(e.target.value);
                setChapter("");
                setSelected([]);
              }}
              className="rounded-xl border px-4 py-3 text-sm"
            >
              <option value="">
                All subjects
              </option>

              {subjects.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>

            {/* CHAPTER */}

            <select
              value={chapter}
              onChange={(e) => {
                setChapter(e.target.value);
                setSelected([]);
              }}
              className="rounded-xl border px-4 py-3 text-sm"
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

            {/* DIFFICULTY */}

            <select
              value={difficulty}
              onChange={(e) => {
                setDifficulty(e.target.value);
                setSelected([]);
              }}
              className="rounded-xl border px-4 py-3 text-sm"
            >
              <option value="">
                All difficulties
              </option>

              <option value="Easy">
                Easy
              </option>

              <option value="Medium">
                Medium
              </option>

              <option value="Hard">
                Hard
              </option>

              <option value="Challenging">
                Challenging
              </option>
            </select>

          </div>

          <input
            value={search}
            onChange={(e) =>
              setSearch(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                loadQuestions();
              }
            }}
            placeholder="Search question text..."
            className="mt-4 w-full rounded-xl border px-4 py-3 text-sm"
          />

        </section>

        <div className="mb-5 flex items-center justify-between">

          <div>
            <p className="text-sm font-extrabold">
              {selected.length} selected
            </p>

            <p className="mt-1 text-xs text-[#8a93a5]">
              Showing {questions.length} questions
            </p>
          </div>

          {selected.length > 0 && (
            <button
              onClick={() => setSelected([])}
              className="rounded-xl border bg-white px-4 py-2 text-sm font-bold text-[#697386]"
            >
              Clear selection
            </button>
          )}

          {questions.length > 0 && (
            <button
              type="button"
              onClick={toggleAllQuestions}
              className="rounded-xl border bg-white px-4 py-2 text-sm font-bold text-[#315bea]"
            >
              {questions.every((question) => selected.includes(question.id))
                ? "Deselect all"
                : "Select all shown"}
            </button>
          )}

        </div>

        {error && (
          <div className="mb-5 rounded-xl bg-red-50 p-4 text-sm font-semibold text-red-600">
            {error}
          </div>
        )}

        {loading && (
          <div className="rounded-2xl bg-white p-10 text-center text-sm text-[#697386]">
            Loading questions...
          </div>
        )}

        {!loading &&
          !error &&
          questions.length === 0 && (
            <div className="rounded-2xl bg-white p-10 text-center">
              <p className="font-bold">
                No questions found.
              </p>

              <p className="mt-2 text-sm text-[#8a93a5]">
                Try another subject, chapter or difficulty.
              </p>
            </div>
          )}

        {!loading && questions.length > 0 && (
          <div className="space-y-4 pb-28">

            {questions.map((question, index) => {

              const isSelected =
                selected.includes(question.id);
              const options = getOptions(question.options);
              const figureSrc = getFigureSrc(question.figure_asset);

              return (
                <button
                  key={question.id}
                  type="button"
                  onClick={() =>
                    toggleQuestion(question.id)
                  }
                  className={`w-full rounded-2xl border bg-white p-5 text-left shadow-sm transition ${
                    isSelected
                      ? "border-[#315bea] ring-2 ring-[#315bea]/10"
                      : "border-[#e5e8ef] hover:border-[#cbd3e5]"
                  }`}
                >

                  <div className="flex gap-4">

                    <div
                      className={`mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-md border text-xs font-bold ${
                        isSelected
                          ? "border-[#315bea] bg-[#315bea] text-white"
                          : "border-[#cbd3df] text-transparent"
                      }`}
                    >
                      {isSelected ? "✓" : ""}
                    </div>

                    <div className="min-w-0 flex-1">

                      <div className="mb-3 flex flex-wrap gap-2">

                        <span className="rounded-full bg-[#f0f3fa] px-2.5 py-1 text-xs font-bold text-[#697386]">
                          #{index + 1}
                        </span>

                        <span className="rounded-full bg-[#eef2ff] px-2.5 py-1 text-xs font-bold text-[#315bea]">
                          {question.subject}
                        </span>

                        {question.chapter_name && (
                          <span className="rounded-full bg-[#f5f6f8] px-2.5 py-1 text-xs font-semibold text-[#697386]">
                            {question.chapter_name}
                          </span>
                        )}

                        {question.difficulty && (
                          <span className="rounded-full bg-[#f5f6f8] px-2.5 py-1 text-xs font-semibold text-[#697386]">
                            {question.difficulty}
                          </span>
                        )}

                      </div>

                      <p className="text-sm font-semibold leading-7">
                        {question.stem}
                      </p>

                      {figureSrc && (
                        <img
                          src={figureSrc}
                          alt={`Figure for question ${index + 1}`}
                          className="mt-4 max-h-80 max-w-full rounded-xl border border-[#e5e8ef] bg-white object-contain"
                          onError={(event) => {
                            event.currentTarget.style.display = "none";
                          }}
                        />
                      )}

                      {options.length > 0 && (
                        <div className="mt-4 grid gap-2 md:grid-cols-2">

                          {options.map(
                            (option, optionIndex) => (
                              <div
                                key={optionIndex}
                                className="rounded-lg bg-[#f8f9fc] px-3 py-2 text-xs text-[#697386]"
                              >
                                {option}
                              </div>
                            )
                          )}

                        </div>
                      )}

                    </div>

                  </div>

                </button>
              );
            })}

          </div>
        )}

        <div className="fixed bottom-4 left-1/2 z-20 flex w-[calc(100%-2rem)] max-w-7xl -translate-x-1/2 items-center justify-between rounded-2xl border border-[#dfe4ef] bg-white p-4 shadow-xl">

          <div>
            <p className="text-sm font-extrabold">
              {selected.length} questions selected
            </p>

            <p className="text-xs text-[#8a93a5]">
              Select the questions you want to publish.
            </p>
          </div>

          <button
            onClick={continueToPublish}
            disabled={selected.length === 0}
            className="rounded-xl bg-[#315bea] px-6 py-3 text-sm font-bold text-white hover:bg-[#264ac7] disabled:cursor-not-allowed disabled:opacity-50"
          >
            Continue to Publish →
          </button>

        </div>

      </div>
    </main>
  );
}
