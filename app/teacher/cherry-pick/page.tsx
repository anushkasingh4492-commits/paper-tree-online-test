
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
                      ✓
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

                      {Array.isArray(question.options) && (
                        <div className="mt-4 grid gap-2 md:grid-cols-2">

                          {question.options.map(
                            (option, optionIndex) => (
                              <div
                                key={optionIndex}
                                className="rounded-lg bg-[#f8f9fc] px-3 py-2 text-xs text-[#697386]"
                              >
                                {String(option)}
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
