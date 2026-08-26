"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

const subjects = [
  {
    name: "Physics",
    code: "PH",
    description: "Mechanics, electricity, optics & more",
  },
  {
    name: "Chemistry",
    code: "CH",
    description: "Physical, organic & inorganic chemistry",
  },
  {
    name: "Mathematics",
    code: "MA",
    description: "Algebra, calculus, geometry & more",
  },
  {
    name: "Biology",
    code: "BI",
    description: "Botany, zoology & human biology",
  },
];

const difficulties = [
  "Easy",
  "Challenging",
  "Balanced",
  "Difficult",
];

const questionOptions = [10, 20, 30, 40, 50, 60];

const durationOptions = [
  { value: 15, label: "15 minutes" },
  { value: 30, label: "30 minutes" },
  { value: 45, label: "45 minutes" },
  { value: 60, label: "60 minutes" },
  { value: 90, label: "90 minutes" },
  { value: 120, label: "120 minutes" },
];

function DashboardIcon() {
  return (
    <span className="grid h-5 w-5 grid-cols-2 gap-1">
      <span className="rounded-[3px] bg-current" />
      <span className="rounded-[3px] bg-current" />
      <span className="rounded-[3px] bg-current" />
      <span className="rounded-[3px] bg-current" />
    </span>
  );
}

function TestIcon() {
  return (
    <span className="relative block h-5 w-5 rounded-md border-2 border-current">
      <span className="absolute left-1 top-1 h-0.5 w-2 rounded bg-current" />
      <span className="absolute left-1 top-2.5 h-0.5 w-3 rounded bg-current" />
      <span className="absolute left-1 top-4 h-0.5 w-2 rounded bg-current" />
    </span>
  );
}

function ChartIcon() {
  return (
    <span className="relative block h-5 w-5">
      <span className="absolute bottom-0 left-0 h-2 w-1.5 rounded-t bg-current" />
      <span className="absolute bottom-0 left-2.5 h-4 w-1.5 rounded-t bg-current" />
      <span className="absolute bottom-0 left-5 h-5 w-1.5 rounded-t bg-current" />
    </span>
  );
}

function SettingsIcon() {
  return (
    <span className="flex h-5 w-5 items-center justify-center rounded-full border-2 border-current">
      <span className="h-1.5 w-1.5 rounded-full bg-current" />
    </span>
  );
}

function ArrowRight() {
  return <span className="text-base">→</span>;
}

export default function GenerateTestPage() {
  const router = useRouter();

  const [studentName, setStudentName] = useState("Student");

  const [selectedSubjects, setSelectedSubjects] = useState<string[]>([
    "Physics",
  ]);

  const [selectedChapters, setSelectedChapters] = useState<string[]>([]);

  const [difficulty, setDifficulty] = useState("Mixed");
  const [questionCount, setQuestionCount] = useState(10);
  const [duration, setDuration] = useState(60);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const storedName =
      localStorage.getItem("studentName") ||
      localStorage.getItem("name");

    if (storedName) {
      setStudentName(storedName);
    }
  }, []);

  const firstName =
    studentName.split(" ")[0] || "Student";

  const initials =
    studentName
      .split(" ")
      .map((word) => word[0])
      .join("")
      .slice(0, 2)
      .toUpperCase() || "S";

  const subjectLabel = useMemo(() => {
    if (selectedSubjects.length === 0) {
      return "No subject selected";
    }

    if (selectedSubjects.length === 1) {
      return selectedSubjects[0];
    }

    return `${selectedSubjects.length} subjects`;
  }, [selectedSubjects]);

function toggleSubject(subject: string) {
  setSelectedSubjects((current) => {
    if (current.includes(subject)) {
      return current.filter((item) => item !== subject);
    }

    if (subject === "Mathematics") {
      return [
        ...current.filter((item) => item !== "Biology"),
        "Mathematics",
      ];
    }

    if (subject === "Biology") {
      return [
        ...current.filter((item) => item !== "Mathematics"),
        "Biology",
      ];
    }

    return [...current, subject];
  });
}
  async function generateTest() {
    setError("");

    if (selectedSubjects.length === 0) {
      setError("Please select at least one subject.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("/api/tests/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          exam: "MHT-CET",
          course: "MHT-CET",
          subjects: selectedSubjects,
          chapters: selectedChapters,
          difficulty,
          questionCount,
          duration,
        }),
      });

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(
          result.error || "Failed to generate test."
        );
      }

      if (!result.testId) {
        throw new Error(
          "Test was generated but no test ID was returned."
        );
      }

  router.push(`/test/${result.testId}/result`);
    } catch (err) {
      console.error("Generate test error:", err);

      setError(
        err instanceof Error
          ? err.message
          : "Failed to generate test."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <div className="flex min-h-screen">
        {/* SIDEBAR */}

        <aside className="hidden w-[245px] shrink-0 border-r border-[#e8ebf1] bg-white lg:flex lg:flex-col">
          <div className="flex h-[82px] items-center border-b border-[#eef0f4] px-7">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-[12px] bg-[#315bea] text-lg font-extrabold text-white shadow-sm">
                P
              </div>

              <div>
                <p className="text-[16px] font-extrabold tracking-[-0.02em] text-[#172033]">
                  Paper Tree
                </p>

                <p className="mt-0.5 text-[9px] font-bold tracking-[0.18em] text-[#98a1b2]">
                  ONLINE TEST
                </p>
              </div>
            </div>
          </div>

          <div className="flex-1 px-4 py-7">
            <p className="mb-3 px-3 text-[10px] font-bold uppercase tracking-[0.14em] text-[#a3aaba]">
              Workspace
            </p>

            <nav className="space-y-1">
              <button
                onClick={() => router.push("/dashboard")}
                className="flex w-full items-center gap-3 rounded-xl px-3.5 py-3 text-sm font-medium text-[#697386] transition hover:bg-[#f7f8fb] hover:text-[#172033]"
              >
                <DashboardIcon />
                Dashboard
              </button>

              <button
                className="flex w-full items-center gap-3 rounded-xl bg-[#eef2ff] px-3.5 py-3 text-sm font-bold text-[#315bea]"
              >
                <TestIcon />
                Create Test
              </button>

              <button
                onClick={() => router.push("/tests")}
                className="flex w-full items-center gap-3 rounded-xl px-3.5 py-3 text-sm font-medium text-[#697386] transition hover:bg-[#f7f8fb] hover:text-[#172033]"
              >
                <ChartIcon />
                My Tests
              </button>

              <button
                onClick={() => router.push("/tests/generate")}
                className="flex w-full items-center gap-3 rounded-xl px-3.5 py-3 text-sm font-medium text-[#697386] transition hover:bg-[#f7f8fb] hover:text-[#172033]"
              >
                <ChartIcon />
                Practice
              </button>
            </nav>

            <p className="mb-3 mt-9 px-3 text-[10px] font-bold uppercase tracking-[0.14em] text-[#a3aaba]">
              Account
            </p>

            <nav>
              <button className="flex w-full items-center gap-3 rounded-xl px-3.5 py-3 text-sm font-medium text-[#697386] transition hover:bg-[#f7f8fb] hover:text-[#172033]">
                <SettingsIcon />
                Settings
              </button>
            </nav>
          </div>

          <div className="border-t border-[#eef0f4] p-4">
            <div className="flex items-center gap-3 rounded-2xl bg-[#f7f8fb] p-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#dfe7ff] text-sm font-bold text-[#315bea]">
                {initials}
              </div>

              <div className="min-w-0">
                <p className="truncate text-sm font-bold text-[#263044]">
                  {studentName}
                </p>

                <p className="truncate text-[11px] text-[#919aaa]">
                  MHT-CET Preparation
                </p>
              </div>
            </div>
          </div>
        </aside>

        {/* MAIN */}

        <section className="min-w-0 flex-1">
          {/* TOPBAR */}

          <header className="flex h-[82px] items-center justify-between border-b border-[#e8ebf1] bg-white px-5 sm:px-8 lg:px-10">
            <div>
              <p className="text-xs font-medium text-[#99a1b0]">
                Student Dashboard
              </p>

              <h1 className="mt-1 text-lg font-bold tracking-[-0.02em] text-[#172033] sm:text-xl">
                Create a Test
              </h1>
            </div>

            <div className="flex items-center gap-3">
              <button
                onClick={() => router.push("/dashboard")}
                className="hidden rounded-xl border border-[#e4e7ed] bg-white px-4 py-2.5 text-xs font-bold text-[#5d6677] transition hover:border-[#cfd5df] hover:text-[#172033] sm:block"
              >
                Dashboard
              </button>

              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[#dfe7ff] text-sm font-bold text-[#315bea]">
                {initials}
              </div>
            </div>
          </header>

          <div className="mx-auto max-w-[1180px] px-5 py-7 sm:px-8 sm:py-9 lg:px-10 lg:py-10">
            {/* PAGE INTRO */}

            <div className="mb-8">
              <div className="inline-flex items-center gap-2 rounded-full bg-[#eef2ff] px-3 py-1.5 text-[10px] font-bold uppercase tracking-[0.12em] text-[#315bea]">
                <span className="h-1.5 w-1.5 rounded-full bg-[#315bea]" />
                MHT-CET · 2026
              </div>

              <h2 className="mt-4 text-[30px] font-extrabold tracking-[-0.04em] text-[#172033] sm:text-[36px]">
                Build your practice test
              </h2>

              <p className="mt-2 max-w-2xl text-sm leading-6 text-[#7f899b]">
                Choose your subjects, difficulty, number of questions and
                duration. Paper Tree will generate a fresh test from the
                MHT-CET question bank.
              </p>
            </div>

            <div className="grid gap-6 lg:grid-cols-[1fr_330px]">
              {/* LEFT CONFIGURATION */}

              <div className="space-y-6">
                {/* SUBJECT */}

                <section className="rounded-[20px] border border-[#e7eaf0] bg-white p-6 shadow-[0_4px_20px_rgba(20,30,55,0.025)] sm:p-7">
                  <div className="mb-5">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-base font-extrabold text-[#172033]">
                          Select subjects
                        </h3>

                      <p className="mt-1 text-xs text-[#929aaa]">
  Choose one or more subjects. Select either Mathematics or Biology.
</p>
                      </div>

                      <span className="rounded-lg bg-[#f7f8fb] px-3 py-1.5 text-[10px] font-bold text-[#697386]">
                        {subjectLabel}
                      </span>
                    </div>
                  </div>

                  <div className="grid gap-3 sm:grid-cols-2">
                    {subjects.map((subject) => {
                      const selected =
                        selectedSubjects.includes(subject.name);
                        const isOtherScienceSelected =
  (subject.name === "Mathematics" &&
    selectedSubjects.includes("Biology")) ||
  (subject.name === "Biology" &&
    selectedSubjects.includes("Mathematics"));

                      return (
                        <button
                          key={subject.name}
                          type="button"
onClick={() => toggleSubject(subject.name)}
                          className={`group rounded-[16px] border p-4 text-left transition ${
                            selected
                              ? "border-[#315bea] bg-[#eef2ff]"
                              : "border-[#e7eaf0] bg-white hover:border-[#cfd7f7] hover:bg-[#fafbff]"
                          }`}
                        >
                          <div className="flex items-start justify-between">
                            <div
                              className={`flex h-10 w-10 items-center justify-center rounded-xl text-[10px] font-extrabold ${
                                selected
                                  ? "bg-[#315bea] text-white"
                                  : "bg-[#f0f3f8] text-[#687386]"
                              }`}
                            >
                              {subject.code}
                            </div>

                            <div
                              className={`flex h-5 w-5 items-center justify-center rounded-full border-2 ${
                                selected
                                  ? "border-[#315bea] bg-[#315bea] text-white"
                                  : "border-[#d7dce5]"
                              }`}
                            >
                              {selected && (
                                <span className="text-[10px] font-bold">
                                  ✓
                                </span>
                              )}
                            </div>
                          </div>

                          <h4 className="mt-4 text-sm font-extrabold text-[#263044]">
                            {subject.name}
                          </h4>

                          <p className="mt-1 text-[11px] leading-5 text-[#9aa2b0]">
                            {subject.description}
                          </p>
                        </button>
                      );
                    })}
                  </div>
                </section>

                {/* CHAPTERS */}

                <section className="rounded-[20px] border border-[#e7eaf0] bg-white p-6 shadow-[0_4px_20px_rgba(20,30,55,0.025)] sm:p-7">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-base font-extrabold text-[#172033]">
                        Chapters
                      </h3>

                      <p className="mt-1 text-xs text-[#929aaa]">
                        Leave empty to include all chapters.
                      </p>
                    </div>

                    <span className="rounded-lg bg-[#f7f8fb] px-3 py-1.5 text-[10px] font-bold text-[#8b94a4]">
                      All chapters
                    </span>
                  </div>

                  <div className="mt-5 rounded-xl border border-dashed border-[#dfe3ea] bg-[#fafbfc] p-5 text-center">
                    <p className="text-sm font-bold text-[#697386]">
                      All available chapters
                    </p>

                    <p className="mt-1 text-[11px] leading-5 text-[#a1a8b5]">
                      No chapter filter is selected. Questions will be
                      picked from all available chapters for the selected
                      subjects.
                    </p>
                  </div>
                </section>

                {/* DIFFICULTY */}

                <section className="rounded-[20px] border border-[#e7eaf0] bg-white p-6 shadow-[0_4px_20px_rgba(20,30,55,0.025)] sm:p-7">
                  <div>
                    <h3 className="text-base font-extrabold text-[#172033]">
                      Difficulty
                    </h3>

                    <p className="mt-1 text-xs text-[#929aaa]">
                      Choose the difficulty of your test.
                    </p>
                  </div>

                  <div className="mt-5 grid grid-cols-2 gap-2 sm:grid-cols-4">
                    {difficulties.map((item) => {
                      const selected = difficulty === item;

                      return (
                        <button
                          key={item}
                          type="button"
                          onClick={() => setDifficulty(item)}
                          className={`rounded-xl border px-4 py-3 text-xs font-bold transition ${
                            selected
                              ? "border-[#315bea] bg-[#315bea] text-white"
                              : "border-[#e3e6ec] bg-white text-[#697386] hover:border-[#cbd3eb] hover:bg-[#fafbff]"
                          }`}
                        >
                          {item}
                        </button>
                      );
                    })}
                  </div>
                </section>

                {/* QUESTION + DURATION */}

                <section className="grid gap-6 sm:grid-cols-2">
                  <div className="rounded-[20px] border border-[#e7eaf0] bg-white p-6 shadow-[0_4px_20px_rgba(20,30,55,0.025)]">
                    <h3 className="text-base font-extrabold text-[#172033]">
                      Questions
                    </h3>

                    <p className="mt-1 text-xs text-[#929aaa]">
                      Number of questions
                    </p>

                    <div className="mt-5 grid grid-cols-3 gap-2">
                      {questionOptions.map((count) => {
                        const selected =
                          questionCount === count;

                        return (
                          <button
                            key={count}
                            type="button"
                            onClick={() =>
                              setQuestionCount(count)
                            }
                            className={`rounded-xl border py-3 text-xs font-bold transition ${
                              selected
                                ? "border-[#315bea] bg-[#315bea] text-white"
                                : "border-[#e3e6ec] text-[#697386] hover:border-[#cbd3eb]"
                            }`}
                          >
                            {count}
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  <div className="rounded-[20px] border border-[#e7eaf0] bg-white p-6 shadow-[0_4px_20px_rgba(20,30,55,0.025)]">
                    <h3 className="text-base font-extrabold text-[#172033]">
                      Duration
                    </h3>

                    <p className="mt-1 text-xs text-[#929aaa]">
                      Test time limit
                    </p>

                    <select
                      value={duration}
                      onChange={(event) =>
                        setDuration(
                          Number(event.target.value)
                        )
                      }
                      className="mt-5 h-11 w-full rounded-xl border border-[#dfe3ea] bg-white px-3 text-sm font-semibold text-[#394255] outline-none transition focus:border-[#315bea] focus:ring-4 focus:ring-[#315bea]/10"
                    >
                      {durationOptions.map((option) => (
                        <option
                          key={option.value}
                          value={option.value}
                        >
                          {option.label}
                        </option>
                      ))}
                    </select>
                  </div>
                </section>
              </div>

              {/* RIGHT SUMMARY */}

              <aside className="lg:sticky lg:top-7 lg:h-fit">
                <div className="overflow-hidden rounded-[22px] border border-[#dfe5ff] bg-[#315bea] shadow-[0_18px_45px_rgba(49,91,234,0.12)]">
                  <div className="p-6">
                    <p className="text-[10px] font-bold uppercase tracking-[0.14em] text-blue-100">
                      Test summary
                    </p>

                    <h3 className="mt-2 text-xl font-extrabold text-white">
                      MHT-CET Practice
                    </h3>

                    <p className="mt-2 text-xs leading-5 text-blue-100">
                      Your test will be generated from the live question
                      bank.
                    </p>

                    <div className="mt-6 space-y-2">
                      <div className="flex items-center justify-between rounded-xl bg-white/10 px-4 py-3">
                        <span className="text-xs text-blue-100">
                          Subjects
                        </span>

                        <span className="text-xs font-bold text-white">
                          {selectedSubjects.length}
                        </span>
                      </div>

                      <div className="flex items-center justify-between rounded-xl bg-white/10 px-4 py-3">
                        <span className="text-xs text-blue-100">
                          Questions
                        </span>

                        <span className="text-xs font-bold text-white">
                          {questionCount}
                        </span>
                      </div>

                      <div className="flex items-center justify-between rounded-xl bg-white/10 px-4 py-3">
                        <span className="text-xs text-blue-100">
                          Difficulty
                        </span>

                        <span className="text-xs font-bold text-white">
                          {difficulty}
                        </span>
                      </div>

                      <div className="flex items-center justify-between rounded-xl bg-white/10 px-4 py-3">
                        <span className="text-xs text-blue-100">
                          Duration
                        </span>

                        <span className="text-xs font-bold text-white">
                          {duration} min
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="border-t border-white/10 bg-[#2b51d2] p-5">
                    {error && (
                      <div className="mb-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-xs font-semibold leading-5 text-red-600">
                        {error}
                      </div>
                    )}

                    <button
                      type="button"
                      onClick={generateTest}
                      disabled={loading}
                      className="flex h-12 w-full items-center justify-center gap-3 rounded-xl bg-white text-sm font-extrabold text-[#315bea] shadow-lg transition hover:-translate-y-0.5 hover:bg-[#f8faff] disabled:cursor-not-allowed disabled:opacity-70"
                    >
                      {loading ? (
                        <>
                          <span className="h-4 w-4 animate-spin rounded-full border-2 border-[#315bea]/30 border-t-[#315bea]" />
                          Generating test...
                        </>
                      ) : (
                        <>
                          Generate Test
                          <ArrowRight />
                        </>
                      )}
                    </button>

                    <p className="mt-3 text-center text-[10px] leading-4 text-blue-100">
                      Questions are randomly selected from the MHT-CET
                      question bank.
                    </p>
                  </div>
                </div>

                {/* INFO CARD */}

                <div className="mt-4 rounded-[18px] border border-[#e7eaf0] bg-white p-5">
                  <div className="flex gap-3">
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-[#ecfdf3] text-sm font-bold text-[#19a463]">
                      ✓
                    </div>

                    <div>
                      <p className="text-xs font-extrabold text-[#394255]">
                        Ready when you are
                      </p>

                      <p className="mt-1 text-[11px] leading-5 text-[#9aa2b0]">
                        Your answers and result will be saved automatically
                        when you complete the test.
                      </p>
                    </div>
                  </div>
                </div>
              </aside>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
