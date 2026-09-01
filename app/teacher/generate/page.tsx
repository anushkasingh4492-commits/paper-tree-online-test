"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type SchemaRow = {
  exam: string;
  subject: string;
  chapter_name: string;
  difficulty: string;
  total: number;
};

export default function TeacherGeneratePage() {
  const router = useRouter();

  const [rows, setRows] = useState<SchemaRow[]>([]);
  const [exam, setExam] = useState("MHT-CET");
  const [subject, setSubject] = useState("Physics");
  const [chapter, setChapter] = useState("");
  const [difficulty, setDifficulty] = useState("Balanced");
  const [questionCount, setQuestionCount] = useState(10);
  const [duration, setDuration] = useState(30);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/db-schema")
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setRows(data.data || []);
        }
      })
      .catch(() => {
        setError("Could not load question database.");
      });
  }, []);

  const subjects = Array.from(
    new Set(
      rows
        .filter((r) => r.exam === exam)
        .map((r) => r.subject)
    )

  );
  console.log("EXAM:", exam);
console.log("ALL SUBJECTS:", subjects);
console.log("ROWS:", rows.length);

  const chapters = Array.from(
    new Set(
      rows
        .filter(
          (r) =>
            r.exam === exam &&
            r.subject === subject
        )
        .map((r) => r.chapter_name)
    )
  );

  async function generatePaper() {
    setError("");
    setLoading(true);

    try {
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
        }),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.error || "Failed to generate paper."
        );
      }

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
      <div className="mx-auto max-w-4xl px-6 py-10">
        <button
          onClick={() => router.push("/teacher")}
          className="mb-6 text-sm font-semibold text-[#315bea]"
        >
          ← Back to Teacher Portal
        </button>

        <div className="rounded-2xl bg-white p-8 shadow-sm">
          <div className="mb-8">
            <p className="text-sm font-bold uppercase tracking-wider text-[#315bea]">
              Teacher Portal
            </p>

            <h1 className="mt-2 text-3xl font-bold">
              Auto Generate Paper
            </h1>

            <p className="mt-2 text-gray-500">
              Select the requirements and generate a test
              from the question bank.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            <div>
              <label className="mb-2 block text-sm font-semibold">
                Exam
              </label>

              <select
                value={exam}
                onChange={(e) => {
                  setExam(e.target.value);
                  setSubject("");
                  setChapter("");
                }}
                className="w-full rounded-xl border px-4 py-3"
              >
                <option value="MHT-CET">MHT-CET</option>
                <option value="NEET">NEET</option>
              </select>
            </div>

            <div>
              <label className="mb-2 block text-sm font-semibold">
                Subject
              </label>

              <select
                value={subject}
                onChange={(e) => {
                  setSubject(e.target.value);
                  setChapter("");
                }}
                className="w-full rounded-xl border px-4 py-3"
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

            <div className="md:col-span-2">
              <label className="mb-2 block text-sm font-semibold">
                Chapter
              </label>

              <select
                value={chapter}
                onChange={(e) =>
                  setChapter(e.target.value)
                }
                className="w-full rounded-xl border px-4 py-3"
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

            <div>
              <label className="mb-2 block text-sm font-semibold">
                Difficulty
              </label>

              <select
                value={difficulty}
                onChange={(e) =>
                  setDifficulty(e.target.value)
                }
                className="w-full rounded-xl border px-4 py-3"
              >
                <option value="Balanced">
                  Balanced
                </option>
                <option value="Easy">Easy</option>
                <option value="Challenging">
                  Challenging
                </option>
                <option value="Difficult">
                  Difficult
                </option>
              </select>
            </div>

            <div>
              <label className="mb-2 block text-sm font-semibold">
                Questions
              </label>

              <input
                type="number"
                min={1}
                max={200}
                value={questionCount}
                onChange={(e) =>
                  setQuestionCount(
                    Number(e.target.value)
                  )
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
                  setDuration(
                    Number(e.target.value)
                  )
                }
                className="w-full rounded-xl border px-4 py-3"
              />
            </div>
          </div>

          {error && (
            <div className="mt-6 rounded-xl bg-red-50 p-4 text-sm text-red-600">
              {error}
            </div>
          )}

          <button
            onClick={generatePaper}
            disabled={loading || !subject}
            className="mt-8 w-full rounded-xl bg-[#315bea] px-5 py-4 font-bold text-white transition hover:bg-[#264ac7] disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading
              ? "Generating Paper..."
              : "Generate Paper"}
          </button>
        </div>
      </div>
    </main>
  );
}
