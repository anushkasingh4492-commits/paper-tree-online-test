"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";

type Course = "MHT-CET" | "JEE" | "NEET";

type Subject =
  | "Physics"
  | "Chemistry"
  | "Mathematics"
  | "Biology";

const COURSE_CONFIG: Record<
  Course,
  {
    description: string;
    subjects: Subject[];
    available: boolean;
  }
> = {
  "MHT-CET": {
    description: "Maharashtra Common Entrance Test",
    subjects: [
      "Physics",
      "Chemistry",
      "Mathematics",
      "Biology",
    ],
    available: true,
  },

  JEE: {
    description: "Joint Entrance Examination",
    subjects: [
      "Physics",
      "Chemistry",
      "Mathematics",
    ],
    available: false,
  },

  NEET: {
    description:
      "National Eligibility cum Entrance Test",
    subjects: [
      "Physics",
      "Chemistry",
      "Biology",
    ],
    available: false,
  },
};

const SAMPLE_CHAPTERS: Record<Subject, string[]> = {
  Physics: [
    "Rotational Motion",
    "Thermodynamics",
    "Current Electricity",
    "Electrostatics",
    "Semiconductors",
  ],

  Chemistry: [
    "Some Basic Concepts of Chemistry",
    "Chemical Bonding",
    "Electrochemistry",
    "Chemical Kinetics",
    "Biomolecules",
  ],

  Mathematics: [
    "Trigonometry",
    "Straight Line",
    "Circle",
    "Probability",
    "Differentiation",
  ],

  Biology: [
    "Biomolecules",
    "Respiration and Energy Transfer",
    "Human Nutrition",
    "Inheritance and Variation",
    "Molecular Basis of Inheritance",
  ],
};

const DIFFICULTIES = [
  "Easy",
  "Medium",
  "Hard",
  "Mixed",
];

const QUESTION_COUNTS = [10, 20, 30, 50, 100];

const DURATIONS = [
  { label: "15 minutes", value: 15 },
  { label: "30 minutes", value: 30 },
  { label: "45 minutes", value: 45 },
  { label: "60 minutes", value: 60 },
  { label: "90 minutes", value: 90 },
];

export default function TestsPage() {
  const router = useRouter();

  const [course, setCourse] =
    useState<Course>("MHT-CET");

  const [subject, setSubject] =
    useState<Subject>("Physics");

  const [chapters, setChapters] = useState<string[]>([]);

  const [difficulty, setDifficulty] =
    useState("Mixed");

  const [questionCount, setQuestionCount] =
    useState(20);

  const [duration, setDuration] =
    useState(30);

  const [generating, setGenerating] =
    useState(false);

  const courseConfig = COURSE_CONFIG[course];

  const availableChapters = useMemo(
    () => SAMPLE_CHAPTERS[subject],
    [subject]
  );

  function changeCourse(nextCourse: Course) {
    setCourse(nextCourse);

    const config = COURSE_CONFIG[nextCourse];

    if (config.subjects.length > 0) {
      setSubject(config.subjects[0]);
    }

    setChapters([]);
  }

  function changeSubject(nextSubject: Subject) {
    setSubject(nextSubject);
    setChapters([]);
  }

  function toggleChapter(chapter: string) {
    setChapters((previous) => {
      if (previous.includes(chapter)) {
        return previous.filter(
          (item) => item !== chapter
        );
      }

      return [...previous, chapter];
    });
  }

  function selectAllChapters() {
    setChapters(availableChapters);
  }

  function clearChapters() {
    setChapters([]);
  }

  
  async function generateTest() {
  if (!courseConfig.available) {
    return;
  }

  setGenerating(true);

  try {
    const response = await fetch("/api/tests/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        exam: course,
        subjects: subject ? [subject] : [],
        chapters,
        difficulty,
        questionCount,
      }),
    });

    const data = await response.json();

    if (!response.ok || !data.success) {
      throw new Error(
        data.error || "Unable to generate test."
      );
    }

    const testId = data.testId;

    const testConfiguration = {
      testId,
      course,
      subject,
      chapters,
      difficulty,
      questionCount,
      duration,
      createdAt: new Date().toISOString(),
    };

    localStorage.setItem(
      `test-${testId}`,
      JSON.stringify({
        ...testConfiguration,
        questions: data.questions,
        startedAt: new Date().toISOString(),
      })
    );

    localStorage.setItem(
      `test-config-${testId}`,
      JSON.stringify(testConfiguration)
    );

    router.push(`/test/${testId}`);
  } catch (error) {
    console.error("GENERATE TEST ERROR:", error);

    alert(
      error instanceof Error
        ? error.message
        : "Unable to generate test."
    );
  } finally {
    setGenerating(false);
  }
}
  

  return (
    <main className="min-h-screen bg-[#f5f7fb] text-[#111827]">
      {/* HEADER */}

      <header className="h-16 bg-white border-b border-[#e5e7eb] flex items-center justify-between px-6">
        <div className="flex items-center gap-3">
          <button
            onClick={() => router.push("/dashboard")}
            className="w-9 h-9 rounded-xl bg-[#1d4ed8] text-white flex items-center justify-center font-bold"
          >
            P
          </button>

          <div>
            <div className="font-semibold">
              Paper Tree
            </div>

            <div className="text-xs text-[#6b7280]">
              Create Test
            </div>
          </div>
        </div>

        <button
          onClick={() => router.push("/dashboard")}
          className="text-sm text-[#6b7280] hover:text-[#111827]"
        >
          Dashboard
        </button>
      </header>

      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* PAGE TITLE */}

        <div className="mb-8">
          <div className="text-sm font-medium text-[#2563eb] mb-2">
            TEST GENERATOR
          </div>

          <h1 className="text-3xl font-bold tracking-tight">
            Create a New Test
          </h1>

          <p className="mt-2 text-sm text-[#6b7280]">
            Configure your test and start practising with
            questions from the Paper Tree question bank.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-[1fr_330px] gap-6">
          {/* MAIN CONFIGURATION */}

          <div className="space-y-6">
            {/* COURSE */}

            <section className="bg-white border border-[#e5e7eb] rounded-2xl shadow-sm p-6">
              <div className="mb-5">
                <h2 className="text-lg font-semibold">
                  1. Choose Exam
                </h2>

                <p className="text-sm text-[#6b7280] mt-1">
                  Select the entrance examination you are
                  preparing for.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {(
                  Object.keys(
                    COURSE_CONFIG
                  ) as Course[]
                ).map((item) => {
                  const config =
                    COURSE_CONFIG[item];

                  const selected =
                    course === item;

                  return (
                    <button
                      key={item}
                      disabled={!config.available}
                      onClick={() =>
                        changeCourse(item)
                      }
                      className={`relative text-left rounded-xl border-2 p-5 transition ${
                        selected
                          ? "border-[#2563eb] bg-[#eff6ff]"
                          : config.available
                          ? "border-[#e5e7eb] hover:border-[#bfdbfe]"
                          : "border-[#e5e7eb] bg-[#fafafa] opacity-60 cursor-not-allowed"
                      }`}
                    >
                      {selected && (
                        <div className="absolute top-4 right-4 w-5 h-5 rounded-full bg-[#2563eb] text-white flex items-center justify-center text-xs">
                          ✓
                        </div>
                      )}

                      {!config.available && (
                        <span className="absolute top-3 right-3 text-[10px] font-semibold uppercase tracking-wide bg-[#f3f4f6] text-[#6b7280] px-2 py-1 rounded-md">
                          Coming Soon
                        </span>
                      )}

                      <div className="text-lg font-bold">
                        {item}
                      </div>

                      <div className="text-xs text-[#6b7280] mt-2 pr-4">
                        {config.description}
                      </div>
                    </button>
                  );
                })}
              </div>
            </section>

            {/* SUBJECT */}

            <section className="bg-white border border-[#e5e7eb] rounded-2xl shadow-sm p-6">
              <div className="mb-5">
                <h2 className="text-lg font-semibold">
                  2. Choose Subject
                </h2>

                <p className="text-sm text-[#6b7280] mt-1">
                  Select the subject for this test.
                </p>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {courseConfig.subjects.map(
                  (item) => {
                    const selected =
                      subject === item;

                    return (
                      <button
                        key={item}
                        onClick={() =>
                          changeSubject(item)
                        }
                        className={`p-4 rounded-xl border-2 text-sm font-semibold transition ${
                          selected
                            ? "border-[#2563eb] bg-[#eff6ff] text-[#1d4ed8]"
                            : "border-[#e5e7eb] hover:border-[#bfdbfe]"
                        }`}
                      >
                        {item}
                      </button>
                    );
                  }
                )}
              </div>
            </section>

            {/* CHAPTERS */}

            <section className="bg-white border border-[#e5e7eb] rounded-2xl shadow-sm p-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-5">
                <div>
                  <h2 className="text-lg font-semibold">
                    3. Choose Chapters
                  </h2>

                  <p className="text-sm text-[#6b7280] mt-1">
                    Select specific chapters or use the
                    entire subject.
                  </p>
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={selectAllChapters}
                    className="text-xs font-semibold text-[#2563eb] hover:underline"
                  >
                    Select All
                  </button>

                  <span className="text-[#d1d5db]">
                    |
                  </span>

                  <button
                    onClick={clearChapters}
                    className="text-xs font-semibold text-[#6b7280] hover:underline"
                  >
                    Clear
                  </button>
                </div>
              </div>

              <div className="space-y-2">
                {availableChapters.map(
                  (chapter) => {
                    const selected =
                      chapters.includes(chapter);

                    return (
                      <button
                        key={chapter}
                        onClick={() =>
                          toggleChapter(
                            chapter
                          )
                        }
                        className={`w-full flex items-center justify-between p-3.5 rounded-xl border transition text-left ${
                          selected
                            ? "border-[#93c5fd] bg-[#eff6ff]"
                            : "border-[#e5e7eb] hover:bg-[#f9fafb]"
                        }`}
                      >
                        <span className="text-sm font-medium">
                          {chapter}
                        </span>

                        <span
                          className={`w-5 h-5 rounded-md border flex items-center justify-center text-xs ${
                            selected
                              ? "bg-[#2563eb] border-[#2563eb] text-white"
                              : "border-[#d1d5db]"
                          }`}
                        >
                          {selected
                            ? "✓"
                            : ""}
                        </span>
                      </button>
                    );
                  }
                )}
              </div>

              {chapters.length === 0 && (
                <div className="mt-4 rounded-xl bg-[#f9fafb] border border-[#e5e7eb] p-3 text-xs text-[#6b7280]">
                  No chapter selected — questions can
                  be taken from the entire subject.
                </div>
              )}
            </section>

            {/* DIFFICULTY */}

            <section className="bg-white border border-[#e5e7eb] rounded-2xl shadow-sm p-6">
              <div className="mb-5">
                <h2 className="text-lg font-semibold">
                  4. Difficulty
                </h2>

                <p className="text-sm text-[#6b7280] mt-1">
                  Choose the difficulty level.
                </p>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {DIFFICULTIES.map(
                  (item) => {
                    const selected =
                      difficulty === item;

                    return (
                      <button
                        key={item}
                        onClick={() =>
                          setDifficulty(item)
                        }
                        className={`p-3.5 rounded-xl border-2 text-sm font-semibold transition ${
                          selected
                            ? "border-[#2563eb] bg-[#eff6ff] text-[#1d4ed8]"
                            : "border-[#e5e7eb] hover:border-[#bfdbfe]"
                        }`}
                      >
                        {item}
                      </button>
                    );
                  }
                )}
              </div>
            </section>

            {/* QUESTIONS + DURATION */}

            <section className="bg-white border border-[#e5e7eb] rounded-2xl shadow-sm p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <h2 className="text-lg font-semibold">
                    5. Number of Questions
                  </h2>

                  <p className="text-sm text-[#6b7280] mt-1 mb-4">
                    How many questions should the test
                    contain?
                  </p>

                  <div className="flex flex-wrap gap-2">
                    {QUESTION_COUNTS.map(
                      (count) => (
                        <button
                          key={count}
                          onClick={() =>
                            setQuestionCount(
                              count
                            )
                          }
                          className={`px-5 py-3 rounded-xl border-2 text-sm font-semibold transition ${
                            questionCount ===
                            count
                              ? "border-[#2563eb] bg-[#eff6ff] text-[#1d4ed8]"
                              : "border-[#e5e7eb] hover:border-[#bfdbfe]"
                          }`}
                        >
                          {count}
                        </button>
                      )
                    )}
                  </div>
                </div>

                <div>
                  <h2 className="text-lg font-semibold">
                    6. Duration
                  </h2>

                  <p className="text-sm text-[#6b7280] mt-1 mb-4">
                    Set the maximum time for the test.
                  </p>

                  <select
                    value={duration}
                    onChange={(e) =>
                      setDuration(
                        Number(e.target.value)
                      )
                    }
                    className="w-full h-12 rounded-xl border border-[#d1d5db] px-4 text-sm outline-none focus:border-[#2563eb] focus:ring-4 focus:ring-blue-100 bg-white"
                  >
                    {DURATIONS.map(
                      (item) => (
                        <option
                          key={item.value}
                          value={item.value}
                        >
                          {item.label}
                        </option>
                      )
                    )}
                  </select>
                </div>
              </div>
            </section>
          </div>

          {/* SUMMARY */}

          <aside className="lg:sticky lg:top-6 h-fit">
            <div className="bg-white border border-[#e5e7eb] rounded-2xl shadow-sm overflow-hidden">
              <div className="p-6 border-b border-[#e5e7eb]">
                <div className="text-xs font-semibold uppercase tracking-wider text-[#6b7280]">
                  Test Summary
                </div>

                <h2 className="text-2xl font-bold mt-2">
                  {course}
                </h2>

                <p className="text-sm text-[#6b7280] mt-1">
                  {subject}
                </p>
              </div>

              <div className="p-6 space-y-5">
                <SummaryRow
                  label="Exam"
                  value={course}
                />

                <SummaryRow
                  label="Subject"
                  value={subject}
                />

                <SummaryRow
                  label="Chapters"
                  value={
                    chapters.length === 0
                      ? "Entire subject"
                      : `${chapters.length} selected`
                  }
                />

                <SummaryRow
                  label="Difficulty"
                  value={difficulty}
                />

                <SummaryRow
                  label="Questions"
                  value={`${questionCount}`}
                />

                <SummaryRow
                  label="Duration"
                  value={`${duration} min`}
                />

                <div className="pt-2">
                  <button
                    onClick={generateTest}
                    disabled={generating}
                    className="w-full h-12 rounded-xl bg-[#1d4ed8] text-white text-sm font-semibold hover:bg-[#1e40af] disabled:opacity-60 disabled:cursor-not-allowed transition"
                  >
                    {generating
                      ? "Generating Test..."
                      : "Generate Test →"}
                  </button>
                </div>

                <p className="text-[11px] leading-relaxed text-[#9ca3af] text-center">
                  Questions will be selected from the Paper
                  Tree question bank according to your
                  configuration.
                </p>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </main>
  );
}

function SummaryRow({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="flex items-center justify-between gap-4">
      <span className="text-sm text-[#6b7280]">
        {label}
      </span>

      <span className="text-sm font-semibold text-right">
        {value}
      </span>
    </div>
  );
}