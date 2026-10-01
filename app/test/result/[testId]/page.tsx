"use client";

import "katex/dist/katex.min.css";

import katex from "katex";
import { useEffect, useMemo, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import jsPDF from "jspdf";
import StudentAccountMenu from "@/components/StudentAccountMenu";

type Question = {
  id: string;
  number: number;
  question: string;
  options: string[];
  answer: number | null;
  subject?: string;
  chapter?: string;
  difficulty?: string;
  solution?: string | null;
  figureAsset?: string | null;
};

type ResultData = {
  testId: string;
  scheduledTestId?: string;
  allowReattempt?: boolean;
  total: number;
  correct: number;
  wrong: number;
  unattempted: number;
  answers: Record<string, number | string | null>;
  timeSpent?: Record<string, number>;
  marked: Record<string, boolean>;
  questions: Question[];
  submittedAt?: string;
  automatic?: boolean;
  course?: string;
  subject?: string;
  chapters?: string[];
  difficulty?: string;
  duration?: number;
  score: number;
  accuracy: number;
};

type AcademyBranding = {
  name?: string | null;
  logo_data?: string | null;
  subtitle?: string | null;
};

function normalizeAnswer(value: unknown): number | null {
  if (value === undefined || value === null || value === "") {
    return null;
  }

  if (
    typeof value === "number" &&
    Number.isFinite(value) &&
    Number.isInteger(value)
  ) {
    return value;
  }

  if (typeof value === "string") {
    const trimmed = value.trim();

    if (!trimmed) {
      return null;
    }

    const upper = trimmed.toUpperCase();

    if (/^[A-Z]$/.test(upper)) {
      return upper.charCodeAt(0) - 65;
    }

    const numeric = Number(trimmed);

    if (Number.isFinite(numeric) && Number.isInteger(numeric)) {
      return numeric;
    }
  }

  return null;
}

function normalizeOptions(question: any): string[] {
  let options =
    question?.options ??
    question?.choices ??
    question?.answer_options ??
    question?.answerOptions ??
    null;

  if (typeof options === "string") {
    const trimmed = options.trim();

    if (trimmed) {
      try {
        options = JSON.parse(trimmed);
      } catch {
        options = [trimmed];
      }
    }
  }

  if (
    options &&
    typeof options === "object" &&
    !Array.isArray(options)
  ) {
    const optionObject = options as Record<string, unknown>;
    const orderedLetters = ["A", "B", "C", "D", "E", "F"];

    const ordered = orderedLetters
      .filter((letter) =>
        Object.prototype.hasOwnProperty.call(optionObject, letter)
      )
      .map((letter) => optionObject[letter]);

    options =
      ordered.length > 0
        ? ordered
        : Object.values(optionObject);
  }

  if (!Array.isArray(options)) {
    const possibleOptions = [
      question?.option_a,
      question?.option_b,
      question?.option_c,
      question?.option_d,
      question?.option_e,
      question?.optionA,
      question?.optionB,
      question?.optionC,
      question?.optionD,
      question?.optionE,
    ].filter(
      (value) =>
        value !== undefined &&
        value !== null &&
        String(value).trim() !== ""
    );

    options = possibleOptions;
  }

  if (!Array.isArray(options)) {
    return [];
  }

  return options.map((option) => String(option ?? ""));
}

function getCorrectAnswer(question: any): number | null {
  const possibleAnswers = [
    question?.answer,
    question?.correct_option,
    question?.correctOption,
    question?.correct_answer,
    question?.correctAnswer,
  ];

  for (const value of possibleAnswers) {
    const normalized = normalizeAnswer(value);

    if (normalized !== null) {
      return normalized;
    }
  }

  return null;
}

function normalizeResultQuestion(
  question: any,
  index: number
): Question {
  return {
    id:
      String(
        question?.id ??
          question?.question_id ??
          question?.questionId ??
          `question-${index + 1}`
      ) || `question-${index + 1}`,

    number:
      Number(question?.number) ||
      Number(question?.question_number) ||
      index + 1,

    question: String(
      question?.question ??
        question?.stem ??
        question?.text ??
        question?.question_text ??
        ""
    ),

    options: normalizeOptions(question),

    answer: getCorrectAnswer(question),

    subject:
      question?.subject ??
      question?.subject_name ??
      undefined,

    chapter:
      question?.chapter ??
      question?.chapter_name ??
      undefined,

    difficulty:
      question?.difficulty ?? undefined,

    solution:
      question?.solution ??
      question?.explanation ??
      question?.answer_explanation ??
      null,

    figureAsset:
      question?.figureAsset ??
      question?.figure_asset ??
      question?.figure ??
      null,
  };
}

function normalizeQuestions(questions: any): Question[] {
  if (!Array.isArray(questions)) {
    return [];
  }

  return questions.map((question, index) =>
    normalizeResultQuestion(question, index)
  );
}

function extractQuestions(data: any): Question[] {
  const possibleSources = [
    data?.questions,
    data?.result?.questions,
    data?.test?.questions,
    data?.data?.questions,
  ];

  for (const source of possibleSources) {
    let parsed = source;

    if (typeof parsed === "string") {
      try {
        parsed = JSON.parse(parsed);
      } catch {
        continue;
      }
    }

    const normalized = normalizeQuestions(parsed);

    if (normalized.length > 0) {
      return normalized;
    }
  }

  return [];
}

async function fetchJsonSafely(
  url: string
): Promise<{
  ok: boolean;
  status: number;
  data: any | null;
}> {
  try {
    const response = await fetch(url, {
      method: "GET",
      cache: "no-store",
      credentials: "include",
    });

    const contentType =
      response.headers.get("content-type") || "";

    if (!contentType.includes("application/json")) {
      return {
        ok: false,
        status: response.status,
        data: null,
      };
    }

    const data = await response.json();

    return {
      ok: response.ok,
      status: response.status,
      data,
    };
  } catch (error) {
    console.error(`Failed to fetch ${url}:`, error);

    return {
      ok: false,
      status: 0,
      data: null,
    };
  }
}

function getSelectedAnswer(
  answers:
    | Record<string, number | string | null>
    | undefined,
  question: Question,
  index: number
): number | null {
  if (!answers) {
    return null;
  }

  const possibleKeys = [
    question.id,
    String(question.id),
    `question-${index + 1}`,
    String(index),
    String(index + 1),
  ];

  for (const key of possibleKeys) {
    if (
      Object.prototype.hasOwnProperty.call(
        answers,
        key
      )
    ) {
      return normalizeAnswer(answers[key]);
    }
  }

  return null;
}

function mergeResultQuestions(
  result: ResultData,
  questions: Question[]
): ResultData {
  if (
    Array.isArray(result.questions) &&
    result.questions.length > 0
  ) {
    return {
      ...result,
      questions: result.questions.map(
        (question, index) =>
          normalizeResultQuestion(question, index)
      ),
    };
  }

  return {
    ...result,
    questions,
  };
}

function MathText({
  text,
  className = "",
}: {
  text: string;
  className?: string;
}) {
  if (!text) {
    return null;
  }

  const parts = String(text).split(
    /(\$\$[\s\S]*?\$\$|\$[\s\S]*?\$)/
  );

  return (
    <span className={className}>
      {parts.map((part, index) => {
        if (
          part.startsWith("$$") &&
          part.endsWith("$$")
        ) {
          const latex = part.slice(2, -2);

          try {
            return (
              <span
                key={index}
                className="block my-3 overflow-x-auto"
                dangerouslySetInnerHTML={{
                  __html: katex.renderToString(
                    latex,
                    {
                      throwOnError: false,
                      displayMode: true,
                    }
                  ),
                }}
              />
            );
          } catch {
            return (
              <span key={index}>
                {latex}
              </span>
            );
          }
        }

        if (
          part.startsWith("$") &&
          part.endsWith("$")
        ) {
          const latex = part.slice(1, -1);

          try {
            return (
              <span
                key={index}
                dangerouslySetInnerHTML={{
                  __html: katex.renderToString(
                    latex,
                    {
                      throwOnError: false,
                      displayMode: false,
                    }
                  ),
                }}
              />
            );
          } catch {
            return (
              <span key={index}>
                {latex}
              </span>
            );
          }
        }

        return (
          <span key={index}>
            {part}
          </span>
        );
      })}
    </span>
  );
}

function formatMathForPdf(value: string) {
  return String(value || "")
    .replace(/\$\$?/g, "")
    .replace(/\\displaystyle\s*/g, "")
    .replace(
      /\\frac\{([^{}]+)\}\{([^{}]+)\}/g,
      "($1)/($2)"
    )
    .replace(
      /\\sqrt\{([^{}]+)\}/g,
      "sqrt($1)"
    )
    .replace(
      /\\(to|times|cdot|leq|geq|neq)/g,
      (_, command: string) =>
        ({
          to: "->",
          times: "x",
          cdot: ".",
          leq: "<=",
          geq: ">=",
          neq: "!=",
        }[command] || command)
    )
    .replace(
      /\\(text|mathrm|mathbf)\{([^{}]+)\}/g,
      "$2"
    )
    .replace(/[{}]/g, "")
    .replace(/\^(-?\d+)/g, "^$1")
    .replace(/\s+/g, " ")
    .trim();
}

export default function TestResultPage() {
  const params = useParams();
  const router = useRouter();

  const testId = String(params.testId ?? "");

  const [result, setResult] =
    useState<ResultData | null>(null);

  const [loading, setLoading] =
    useState(true);

  // Academy-specific branding
  const [academyBranding, setAcademyBranding] =
    useState<AcademyBranding | null>(null);

  const [gameProgress, setGameProgress] = useState<any>(null);
  const [studentName, setStudentName] = useState("Student");
  const [celebrationBadge, setCelebrationBadge] = useState<any>(null);
  const [levelUp, setLevelUp] = useState<{ level: number; levelName: string } | null>(null);

  useEffect(() => {
    setStudentName(localStorage.getItem("studentName") || "Student");
    fetch("/api/student/insights", { cache: "no-store", credentials: "include" })
      .then((r) => r.json())
      .then((data) => {
        if (!data?.success) return;
        setGameProgress(data);
        const earned = (data.badges || []).filter((b: any) => b.earned).map((b: any) => b.id);
        try {
          const studentKey = localStorage.getItem("studentId") || "current";
          const key = `paper-tree-earned-badges-${studentKey}`;
          const previous = JSON.parse(localStorage.getItem(key) || "[]");
          const newlyEarned = (data.badges || []).find((b: any) => b.earned && !previous.includes(b.id));
          if (newlyEarned) setCelebrationBadge(newlyEarned);
          localStorage.setItem(key, JSON.stringify(earned));

          // A test result is loaded immediately after submission, so a level
          // threshold hit is a reliable signal that the student just levelled up.
          const levelThresholds: Record<number, number> = { 2: 5, 3: 15, 4: 30, 5: 50, 6: 80, 7: 120, 8: 170, 9: 240, 10: 350, 11: 500 };
          const completedTests = Number(data.testsCompleted || 0);
          const currentLevel = Number(data.level || 1);
          if (currentLevel > 1 && levelThresholds[currentLevel] === completedTests) {
            setLevelUp({ level: currentLevel, levelName: String(data.levelName || "New Level") });
          }
        } catch {}
      })
      .catch(() => undefined);
  }, []);

  /*
   * Load academy branding.
   *
   * The API checks the current hostname first,
   * so:
   *
   * web.infinityclasses.net
   * -> Infinity Classes
   *
   * web.vigyanacademy.net
   * -> Vigyan Academy
   */
  useEffect(() => {
    let active = true;

    fetch("/api/academy/branding", {
      cache: "no-store",
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        if (!active) {
          return;
        }

        if (
          data?.success &&
          data?.academy
        ) {
          setAcademyBranding(
            data.academy
          );
        }
      })
      .catch((error) => {
        console.error(
          "Failed to load academy branding:",
          error
        );
      });

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function loadResult() {
      try {
        setLoading(true);

        const storageKey =
          `test-${testId}-result`;

        const storedResult =
          localStorage.getItem(
            storageKey
          );

        let loadedResult:
          | ResultData
          | null = null;

        if (storedResult) {
          try {
            const parsed =
              JSON.parse(
                storedResult
              );

            loadedResult = {
              ...parsed,
              testId:
                parsed?.testId ??
                testId,

              score: Number(parsed?.score ?? parsed?.correct ?? 0),
              accuracy: Number(parsed?.accuracy ?? (Number(parsed?.total ?? 0) > 0 ? (Number(parsed?.correct ?? 0) / Number(parsed?.total ?? 0)) * 100 : 0)),

              answers:
                parsed?.answers &&
                typeof parsed.answers ===
                  "object"
                  ? parsed.answers
                  : {},

              marked:
                parsed?.marked &&
                typeof parsed.marked ===
                  "object"
                  ? parsed.marked
                  : {},

              questions:
                normalizeQuestions(
                  parsed?.questions
                ),
            };
          } catch (error) {
            console.error(
              "Invalid stored result:",
              error
            );
          }
        }

        if (!loadedResult) {
          const serverResult =
            await fetchJsonSafely(
              `/api/test-result/${encodeURIComponent(
                testId
              )}`
            );

          if (
            serverResult.ok &&
            serverResult.data
          ) {
            const raw =
              serverResult.data?.result ??
              serverResult.data;

            if (
              raw &&
              typeof raw === "object"
            ) {
              loadedResult = {
                ...raw,

                testId:
                  raw.testId ??
                  testId,

                score: Number(raw.score ?? raw.correct ?? 0),
                accuracy: Number(raw.accuracy ?? (Number(raw.total ?? 0) > 0 ? (Number(raw.correct ?? 0) / Number(raw.total ?? 0)) * 100 : 0)),

                answers:
                  raw.answers &&
                  typeof raw.answers ===
                    "object"
                    ? raw.answers
                    : {},

                marked:
                  raw.marked &&
                  typeof raw.marked ===
                    "object"
                    ? raw.marked
                    : {},

                questions:
                  normalizeQuestions(
                    raw.questions
                  ),
              };
            }
          }
        }

        if (!loadedResult) {
          const summaryResult =
            await fetchJsonSafely(
              `/api/test-summary?testId=${encodeURIComponent(
                testId
              )}`
            );

          if (
            summaryResult.ok &&
            summaryResult.data
          ) {
            const raw =
              summaryResult.data?.result ??
              summaryResult.data?.summary ??
              summaryResult.data;

            if (
              raw &&
              typeof raw === "object"
            ) {
              loadedResult = {
                ...raw,

                testId:
                  raw.testId ??
                  testId,

                score: Number(raw.score ?? raw.correct ?? 0),
                accuracy: Number(raw.accuracy ?? (Number(raw.total ?? 0) > 0 ? (Number(raw.correct ?? 0) / Number(raw.total ?? 0)) * 100 : 0)),

                answers:
                  raw.answers &&
                  typeof raw.answers ===
                    "object"
                    ? raw.answers
                    : {},

                marked:
                  raw.marked &&
                  typeof raw.marked ===
                    "object"
                    ? raw.marked
                    : {},

                questions:
                  normalizeQuestions(
                    raw.questions
                  ),
              };
            }
          }
        }

        const existingQuestions =
          loadedResult?.questions ?? [];

        if (
          existingQuestions.length === 0
        ) {
          const testResponse =
            await fetchJsonSafely(
              `/api/tests/${encodeURIComponent(
                testId
              )}`
            );

          if (
            testResponse.ok &&
            testResponse.data
          ) {
            const testQuestions =
              extractQuestions(
                testResponse.data
              );

            if (
              testQuestions.length > 0
            ) {
              if (loadedResult) {
                loadedResult =
                  mergeResultQuestions(
                    loadedResult,
                    testQuestions
                  );
              } else {
                const test =
                  testResponse.data?.test ??
                  testResponse.data;

                loadedResult = {
                  testId,
                  total:
                    testQuestions.length,
                  correct: 0,
                  wrong: 0,
                  unattempted:
                    testQuestions.length,
                  answers: {},
                  marked: {},
                  questions:
                    testQuestions,

                  course:
                    test?.course ??
                    test?.title ??
                    undefined,

                  subject:
                    test?.subject ??
                    undefined,

                  difficulty:
                    test?.difficulty ??
                    undefined,

                  duration:
                    Number(
                      test?.duration
                    ) || undefined,
                  score: 0,
                  accuracy: 0,
                };
              }
            }
          }
        }

        if (loadedResult) {
          const normalizedQuestions =
            normalizeQuestions(
              loadedResult.questions
            );

          const normalizedAnswers: Record<
            string,
            number | string | null
          > = {};

          if (
            loadedResult.answers &&
            typeof loadedResult.answers ===
              "object"
          ) {
            Object.entries(
              loadedResult.answers
            ).forEach(
              ([key, value]) => {
                normalizedAnswers[key] =
                  normalizeAnswer(
                    value
                  );
              }
            );
          }

          const rawCorrect =
            Number(
              loadedResult.correct
            ) || 0;

          const rawWrong =
            Number(
              loadedResult.wrong
            ) || 0;

          const total =
            Number(
              loadedResult.total
            ) ||
            normalizedQuestions.length;

          const calculatedUnattempted =
            Math.max(
              0,
              total -
                rawCorrect -
                rawWrong
            );

          const finalResult:
            ResultData = {
            ...loadedResult,

            testId:
              loadedResult.testId ||
              testId,

            total,

            correct:
              rawCorrect,

            wrong:
              rawWrong,

            unattempted:
              Number.isFinite(
                Number(
                  loadedResult.unattempted
                )
              )
                ? Number(
                    loadedResult.unattempted
                  )
                : calculatedUnattempted,

            answers:
              normalizedAnswers,

            marked:
              loadedResult.marked &&
              typeof loadedResult.marked ===
                "object"
                ? loadedResult.marked
                : {},

            questions:
              normalizedQuestions,
          };

          if (!cancelled) {
            setResult(finalResult);
          }

          try {
            localStorage.setItem(
              storageKey,
              JSON.stringify(
                finalResult
              )
            );
          } catch {
            // Ignore storage failures.
          }
        }
      } catch (error) {
        console.error(
          "Could not load result:",
          error
        );
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    if (testId) {
      loadResult();
    } else {
      setLoading(false);
    }

    return () => {
      cancelled = true;
    };
  }, [testId]);

  const percentage = useMemo(() => {
    if (
      !result ||
      result.total <= 0
    ) {
      return 0;
    }

    return Math.round(
      (result.correct /
        result.total) *
        100
    );
  }, [result]);

  const accuracy = useMemo(() => {
    if (!result) {
      return 0;
    }

    const attempted =
      result.correct +
      result.wrong;

    if (attempted === 0) {
      return 0;
    }

    return Math.round(
      (result.correct /
        attempted) *
        100
    );
  }, [result]);

  const attempted = result
    ? result.correct + result.wrong
    : 0;

  const grade = useMemo(() => {
    if (percentage >= 90) {
      return "Excellent";
    }

    if (percentage >= 75) {
      return "Very Good";
    }

    if (percentage >= 60) {
      return "Good";
    }

    if (percentage >= 40) {
      return "Needs Improvement";
    }

    return "Keep Practicing";
  }, [percentage]);

  /*
   * Academy name used everywhere in the
   * downloaded result PDF.
   */
  const academyName =
    academyBranding?.name?.trim() ||
    "Academy";

  function downloadResult() {
    if (!result) {
      return;
    }

    const doc = new jsPDF();

    const pageWidth =
      doc.internal.pageSize.getWidth();

    const pageHeight =
      doc.internal.pageSize.getHeight();

    const margin = 14;

    const contentWidth =
      pageWidth - margin * 2;

    let y = 18;

    const ensureSpace = (
      height: number
    ) => {
      if (
        y + height >
        pageHeight - margin
      ) {
        doc.addPage();
        y = margin;
      }
    };

    const addWrappedText = (
      text: string,
      fontSize = 10.5,
      lineHeight = 5.5,
      bold = false
    ) => {
      doc.setFont(
        "helvetica",
        bold
          ? "bold"
          : "normal"
      );

      doc.setFontSize(
        fontSize
      );

      const lines =
        doc.splitTextToSize(
          String(text ?? ""),
          contentWidth
        );

      const requiredHeight =
        lines.length *
        lineHeight;

      ensureSpace(
        requiredHeight + 3
      );

      doc.text(
        lines,
        margin,
        y
      );

      y +=
        requiredHeight + 3;
    };

    /*
     * RESULT PDF HEADER
     *
     * Uses academy name instead of
     * hardcoded product branding.
     */
    doc.setTextColor(
      23,
      32,
      51
    );

    /*
     * Add academy logo to PDF if the
     * academy has a base64/data-url logo.
     */
    if (
      academyBranding?.logo_data
    ) {
      try {
        const logo =
          academyBranding.logo_data;

        let format:
          | "PNG"
          | "JPEG" =
          logo
            .toLowerCase()
            .startsWith(
              "data:image/jpeg"
            )
            ? "JPEG"
            : "PNG";

        doc.addImage(
          logo,
          format,
          margin,
          y - 8,
          18,
          18
        );

        doc.setFont(
          "helvetica",
          "bold"
        );

        doc.setFontSize(20);

        doc.text(
          `${academyName} • Test Result`,
          margin + 23,
          y
        );
      } catch (error) {
        console.error(
          "Could not add academy logo to PDF:",
          error
        );

        doc.setFont(
          "helvetica",
          "bold"
        );

        doc.setFontSize(20);

        doc.text(
          `${academyName} • Test Result`,
          margin,
          y
        );
      }
    } else {
      doc.setFont(
        "helvetica",
        "bold"
      );

      doc.setFontSize(20);

      doc.text(
        `${academyName} • Test Result`,
        margin,
        y
      );
    }

    y += 8;

    doc.setFont(
      "helvetica",
      "normal"
    );

    doc.setFontSize(10);

    if (result.submittedAt) {
      doc.text(
        `Submitted: ${new Date(
          result.submittedAt
        ).toLocaleString()}`,
        margin,
        y
      );

      y += 5;
    }

    y += 3;

    doc.setDrawColor(
      220,
      224,
      232
    );

    doc.line(
      margin,
      y,
      pageWidth - margin,
      y
    );

    y += 8;

    addWrappedText(
      `Exam: ${
        result.course ||
        "Mock Test"
      }`,
      11,
      5.5,
      true
    );

    addWrappedText(
      `Subject: ${
        result.subject ||
        "Multiple Subjects"
      }`,
      11
    );

    addWrappedText(
      `Difficulty: ${
        result.difficulty ||
        "Mixed"
      }`,
      11
    );

    addWrappedText(
      `Duration: ${
        result.duration
          ? `${result.duration} min`
          : "—"
      }`,
      11
    );

    y += 2;

    addWrappedText(
      `Score: ${percentage}%`,
      14,
      7,
      true
    );

    addWrappedText(
      `Correct: ${result.correct}    Wrong: ${result.wrong}    Unattempted: ${result.unattempted}`,
      11,
      6,
      true
    );

    addWrappedText(
      `Attempted: ${attempted}/${result.total}    Accuracy: ${accuracy}%    Grade: ${grade}`,
      11,
      6,
      true
    );

    y += 4;

    doc.setDrawColor(
      220,
      224,
      232
    );

    doc.line(
      margin,
      y,
      pageWidth - margin,
      y
    );

    y += 8;

    addWrappedText(
      "Question-by-Question Review",
      15,
      7,
      true
    );

    result.questions.forEach(
      (question, index) => {
        const selected =
          getSelectedAnswer(
            result.answers,
            question,
            index
          );

        const hasAnswer =
          selected !== null;

        const isCorrect =
          hasAnswer &&
          question.answer !== null &&
          selected ===
            question.answer;

        const status = isCorrect
          ? "Correct"
          : hasAnswer
            ? "Wrong"
            : "Unattempted";

        ensureSpace(18);

        addWrappedText(
          `${question.number || index + 1}. ${formatMathForPdf(
            question.question
          )}`,
          11,
          6,
          true
        );

        addWrappedText(
          `Status: ${status}`,
          10,
          5
        );

        if (
          question.options.length ===
          0
        ) {
          addWrappedText(
            "Options unavailable",
            10,
            5
          );
        } else {
          question.options.forEach(
            (
              option,
              optionIndex
            ) => {
              const isSelected =
                selected ===
                optionIndex;

              const isCorrectOption =
                question.answer !==
                  null &&
                question.answer ===
                  optionIndex;

              const labels: string[] =
                [];

              if (
                isCorrectOption
              ) {
                labels.push(
                  "Correct Answer"
                );
              }

              if (isSelected) {
                labels.push(
                  "Your Answer"
                );
              }

              if (
                labels.length > 0
              ) {
                ensureSpace(16);

                doc.setDrawColor(
                  210,
                  214,
                  224
                );

                doc.setFillColor(
                  248,
                  249,
                  252
                );

                doc.roundedRect(
                  margin,
                  y - 4,
                  contentWidth,
                  12,
                  2,
                  2,
                  "FD"
                );

                doc.setFont(
                  "helvetica",
                  "bold"
                );

                doc.setFontSize(9);

                doc.setTextColor(
                  80,
                  88,
                  105
                );

                doc.text(
                  labels.join(
                    " • "
                  ),
                  margin + 4,
                  y + 1
                );

                doc.setFont(
                  "helvetica",
                  "normal"
                );

                doc.setFontSize(
                  10
                );

                doc.setTextColor(
                  23,
                  32,
                  51
                );

                const optionLines =
                  doc.splitTextToSize(
                    `${String.fromCharCode(
                      65 +
                        optionIndex
                    )}. ${formatMathForPdf(
                      option
                    )}`,
                    contentWidth -
                      8
                  );

                doc.text(
                  optionLines,
                  margin + 4,
                  y + 6
                );

                y += Math.max(
                  16,
                  optionLines.length *
                    5 +
                    10
                );
              } else {
                addWrappedText(
                  `${String.fromCharCode(
                    65 +
                      optionIndex
                  )}. ${formatMathForPdf(
                    option
                  )}`,
                  10,
                  5
                );
              }
            }
          );
        }

        if (
          question.answer !== null &&
          !question.options[
            question.answer
          ]
        ) {
          addWrappedText(
            `Correct Answer: ${String.fromCharCode(
              65 +
                question.answer
            )}`,
            10,
            5,
            true
          );
        }

        if (question.solution) {
          addWrappedText(
            `Solution: ${formatMathForPdf(
              question.solution
            )}`,
            10,
            5
          );
        }

        y += 4;
      }
    );

    /*
     * Academy-specific filename.
     *
     * Example:
     * infinity-classes-result-123.pdf
     */
    const safeAcademyName =
      academyName
        .toLowerCase()
        .replace(
          /[^a-z0-9]+/g,
          "-"
        )
        .replace(
          /^-+|-+$/g,
          ""
        );

    doc.save(
      `${
        safeAcademyName ||
        "academy"
      }-result-${result.testId}.pdf`
    );
  }

  function startReattempt() {
    if (
      !result?.scheduledTestId ||
      !result.allowReattempt ||
      !result.automatic
    ) {
      return;
    }

    localStorage.removeItem(
      `test-${testId}-answers`
    );

    localStorage.removeItem(
      `test-${testId}-marked`
    );

    localStorage.removeItem(
      `test-${testId}-visited`
    );

    localStorage.removeItem(
      `test-${testId}-result`
    );

    localStorage.removeItem(
      `submitted-${testId}`
    );

    localStorage.setItem(
      `reattempt-${result.scheduledTestId}`,
      "true"
    );

    router.push(
      `/scheduled-test/${result.scheduledTestId}`
    );
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-[#f5f7fb] flex items-center justify-center">
        <div className="text-center">
          <div className="w-11 h-11 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin mx-auto" />

          <p className="mt-4 text-sm font-semibold text-slate-600">
            Loading your result...
          </p>

          <p className="mt-1 text-xs text-slate-400">
            Please wait
          </p>
        </div>
      </main>
    );
  }

  if (!result) {
    return (
      <main className="min-h-screen bg-[#f5f7fb] flex items-center justify-center p-6">
        <div className="w-full max-w-md bg-white border border-slate-200 rounded-3xl shadow-sm p-8 text-center">
          <div className="w-16 h-16 mx-auto rounded-2xl bg-red-50 text-red-600 flex items-center justify-center text-2xl font-bold">
            !
          </div>

          <h1 className="mt-5 text-xl font-bold text-slate-900">
            Result not found
          </h1>

          <p className="mt-2 text-sm leading-6 text-slate-500">
            We could not find the saved
            result for this test.
          </p>

          <button
            type="button"
            onClick={() =>
              router.push("/tests")
            }
            className="mt-6 h-11 px-6 rounded-xl bg-blue-600 text-white text-sm font-semibold hover:bg-blue-700 transition"
          >
            Back to Tests
          </button>
        </div>
      </main>
    );
  }
async function shareResultCard() {
  if (!result) return;

  const canvas = document.createElement("canvas");

  // Portrait format works beautifully for WhatsApp + Instagram
  canvas.width = 1080;
  canvas.height = 1350;


const context = canvas.getContext("2d");

if (!context) {
  console.error("Could not create canvas context");
  return;
}

const ctx: CanvasRenderingContext2D = context;
if (ctx === null) {
  console.error("Could not create 2D canvas context");
  return;
}

  const W = canvas.width;
  const H = canvas.height;

  const studentName =
    localStorage.getItem("studentName") || "Student";

  const score = Number(result.score || 0);
  const accuracy = Number(result.accuracy || 0);

  const subject =
    result.subject ||
    result.course ||
    "Practice Test";

  const level = gameProgress?.level || 1;
  const levelName =
    gameProgress?.levelName || "Rookie";

  const streak = gameProgress?.streak || 0;
  const xp = gameProgress?.points || 0;

  const rank =
    gameProgress?.rank !== null &&
    gameProgress?.rank !== undefined
      ? gameProgress.rank
      : null;

  const batchSize =
    gameProgress?.batchSize || null;

  const badge =
    gameProgress?.badges?.find(
      (b: any) => b.earned
    )?.name || null;

  /* ---------------------------------------
     Helpers
  --------------------------------------- */

  function roundedRect(
    x: number,
    y: number,
    width: number,
    height: number,
    radius: number
  ) {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(
      x + width,
      y,
      x + width,
      y + radius
    );
    ctx.lineTo(
      x + width,
      y + height - radius
    );
    ctx.quadraticCurveTo(
      x + width,
      y + height,
      x + width - radius,
      y + height
    );
    ctx.lineTo(
      x + radius,
      y + height
    );
    ctx.quadraticCurveTo(
      x,
      y + height,
      x,
      y + height - radius
    );
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(
      x,
      y,
      x + radius,
      y
    );
    ctx.closePath();
  }

  function fillRoundRect(
    x: number,
    y: number,
    width: number,
    height: number,
    radius: number,
    fill: string
  ) {
    roundedRect(
      x,
      y,
      width,
      height,
      radius
    );

    ctx.fillStyle = fill;
    ctx.fill();
  }

  function strokeRoundRect(
    x: number,
    y: number,
    width: number,
    height: number,
    radius: number,
    stroke: string
  ) {
    roundedRect(
      x,
      y,
      width,
      height,
      radius
    );

    ctx.strokeStyle = stroke;
    ctx.lineWidth = 2;
    ctx.stroke();
  }

  function drawText(
    text: string,
    x: number,
    y: number,
    size: number,
    weight = "600",
    color = "#ffffff",
    align: CanvasTextAlign = "left"
  ) {
    ctx.font = `${weight} ${size}px Arial, sans-serif`;
    ctx.fillStyle = color;
    ctx.textAlign = align;
    ctx.textBaseline = "middle";
    ctx.fillText(text, x, y);
  }

  function drawWrappedText(
    text: string,
    x: number,
    y: number,
    maxWidth: number,
    lineHeight: number,
    size: number,
    color: string
  ) {
    ctx.font = `600 ${size}px Arial, sans-serif`;
    ctx.fillStyle = color;
    ctx.textAlign = "left";

    const words = text.split(" ");
    let line = "";
    let currentY = y;

    for (const word of words) {
      const testLine =
        line.length > 0
          ? `${line} ${word}`
          : word;

      if (
        ctx.measureText(testLine).width >
          maxWidth &&
        line
      ) {
        ctx.fillText(
          line,
          x,
          currentY
        );

        line = word;
        currentY += lineHeight;
      } else {
        line = testLine;
      }
    }

    if (line) {
      ctx.fillText(
        line,
        x,
        currentY
      );
    }

    return currentY;
  }

  /* ---------------------------------------
     Background
  --------------------------------------- */

  const background =
    ctx.createLinearGradient(
      0,
      0,
      W,
      H
    );

  background.addColorStop(
    0,
    "#07152f"
  );

  background.addColorStop(
    0.45,
    "#10275a"
  );

  background.addColorStop(
    1,
    "#24134b"
  );

  ctx.fillStyle = background;
  ctx.fillRect(
    0,
    0,
    W,
    H
  );

  /* Soft decorative glow */

  const glow1 =
    ctx.createRadialGradient(
      150,
      180,
      10,
      150,
      180,
      430
    );

  glow1.addColorStop(
    0,
    "rgba(72,187,255,0.28)"
  );

  glow1.addColorStop(
    1,
    "rgba(72,187,255,0)"
  );

  ctx.fillStyle = glow1;
  ctx.fillRect(
    0,
    0,
    W,
    H
  );

  const glow2 =
    ctx.createRadialGradient(
      920,
      980,
      10,
      920,
      980,
      450
    );

  glow2.addColorStop(
    0,
    "rgba(214,92,255,0.25)"
  );

  glow2.addColorStop(
    1,
    "rgba(214,92,255,0)"
  );

  ctx.fillStyle = glow2;
  ctx.fillRect(
    0,
    0,
    W,
    H
  );

  /* ---------------------------------------
     Academy header
  --------------------------------------- */

  if (academyBranding?.logo_data) {
    try {
      const logo =
        new Image();

      logo.src =
        academyBranding.logo_data;

      await new Promise<void>(
        (resolve) => {
          logo.onload = () =>
            resolve();

          logo.onerror = () =>
            resolve();
        }
      );

      if (
        logo.complete &&
        logo.naturalWidth > 0
      ) {
        ctx.save();

        fillRoundRect(
          55,
          48,
          92,
          92,
          24,
          "rgba(255,255,255,0.96)"
        );

        ctx.drawImage(
          logo,
          69,
          62,
          64,
          64
        );

        ctx.restore();
      }
    } catch {}
  } else {
    fillRoundRect(
      55,
      48,
      92,
      92,
      24,
      "rgba(255,255,255,0.12)"
    );

    drawText(
      academyName
        .charAt(0)
        .toUpperCase(),
      101,
      94,
      38,
      "800",
      "#ffffff",
      "center"
    );
  }

  drawText(
    academyName,
    170,
    76,
    27,
    "800",
    "#ffffff"
  );

  drawText(
    "LEARN  •  PRACTICE  •  EXCEL",
    170,
    111,
    13,
    "600",
    "#9fb6df"
  );

  /* ---------------------------------------
     Small top-right label
  --------------------------------------- */

  fillRoundRect(
    W - 300,
    55,
    245,
    52,
    26,
    "rgba(255,255,255,0.09)"
  );

  drawText(
    "✦  ACHIEVEMENT UNLOCKED",
    W - 177,
    81,
    13,
    "800",
    "#d8e5ff",
    "center"
  );

  /* ---------------------------------------
     Main achievement
  --------------------------------------- */

  drawText(
    "YOU DID IT!",
    70,
    210,
    19,
    "800",
    "#7ee7ff"
  );

  drawText(
    `${score.toFixed(0)}%`,
    70,
    290,
    92,
    "900",
    "#ffffff"
  );

  drawText(
    "TEST SCORE",
    77,
    350,
    15,
    "800",
    "#91a8d2"
  );

  /* Decorative score circle */

  ctx.save();

  ctx.beginPath();
  ctx.arc(
    865,
    275,
    125,
    0,
    Math.PI * 2
  );

  ctx.strokeStyle =
    "rgba(255,255,255,0.08)";
  ctx.lineWidth = 24;
  ctx.stroke();

  ctx.beginPath();

  ctx.arc(
    865,
    275,
    125,
    -Math.PI / 2,
    -Math.PI / 2 +
      Math.PI * 2 *
        Math.min(
          1,
          score / 100
        )
  );

  const scoreGradient =
    ctx.createLinearGradient(
      740,
      275,
      990,
      275
    );

  scoreGradient.addColorStop(
    0,
    "#62f5c7"
  );

  scoreGradient.addColorStop(
    1,
    "#8d7cff"
  );

  ctx.strokeStyle =
    scoreGradient;

  ctx.lineWidth = 24;
  ctx.lineCap = "round";
  ctx.stroke();

  drawText(
    `${accuracy.toFixed(0)}%`,
    865,
    265,
    38,
    "900",
    "#ffffff",
    "center"
  );

  drawText(
    "ACCURACY",
    865,
    305,
    12,
    "800",
    "#aabce0",
    "center"
  );

  ctx.restore();

  /* ---------------------------------------
     Student identity
  --------------------------------------- */

  fillRoundRect(
    55,
    405,
    W - 110,
    130,
    28,
    "rgba(255,255,255,0.075)"
  );

  /* Avatar */

  ctx.beginPath();
  ctx.arc(
    120,
    470,
    42,
    0,
    Math.PI * 2
  );

  const avatarGradient =
    ctx.createLinearGradient(
      80,
      430,
      160,
      510
    );

  avatarGradient.addColorStop(
    0,
    "#64e8ff"
  );

  avatarGradient.addColorStop(
    1,
    "#9b72ff"
  );

  ctx.fillStyle =
    avatarGradient;

  ctx.fill();

  drawText(
    studentName
      .charAt(0)
      .toUpperCase(),
    120,
    470,
    30,
    "900",
    "#ffffff",
    "center"
  );

  drawText(
    studentName,
    185,
    452,
    28,
    "800",
    "#ffffff"
  );

  drawText(
    `${subject}  •  ${grade}`,
    185,
    490,
    15,
    "600",
    "#a9bddf"
  );

  /* Level pill */

  fillRoundRect(
    W - 330,
    433,
    240,
    58,
    29,
    "rgba(124,92,255,0.22)"
  );

  drawText(
    `LEVEL ${level}  •  ${levelName}`,
    W - 210,
    462,
    14,
    "800",
    "#d9d2ff",
    "center"
  );

  /* ---------------------------------------
     Stats
  --------------------------------------- */

  const statY = 575;
  const statWidth =
    (W - 110 - 36) / 4;

  const stats = [
    {
      label: "CORRECT",
      value: String(
        result.correct
      ),
      icon: "✓",
    },
    {
      label: "WRONG",
      value: String(
        result.wrong
      ),
      icon: "×",
    },
    {
      label: "STREAK",
      value: `${streak}d`,
      icon: "🔥",
    },
    {
      label: "XP EARNED",
      value: `+${xp}`,
      icon: "✦",
    },
  ];

  stats.forEach(
    (stat, index) => {
      const x =
        55 +
        index *
          (statWidth + 12);

      fillRoundRect(
        x,
        statY,
        statWidth,
        112,
        24,
        "rgba(255,255,255,0.065)"
      );

      drawText(
        stat.icon,
        x + 25,
        statY + 31,
        20,
        "800",
        "#ffffff"
      );

      drawText(
        stat.value,
        x + 25,
        statY + 67,
        25,
        "900",
        "#ffffff"
      );

      drawText(
        stat.label,
        x + 25,
        statY + 93,
        10,
        "800",
        "#8ea5cd"
      );
    }
  );

  /* ---------------------------------------
     Rank / badge section
  --------------------------------------- */

  fillRoundRect(
    55,
    715,
    W - 110,
    125,
    28,
    "rgba(255,255,255,0.075)"
  );

  if (rank !== null) {
    drawText(
      "🏆",
      90,
      765,
      28,
      "800"
    );

    drawText(
      `#${rank}`,
      135,
      755,
      32,
      "900",
      "#ffffff"
    );

    drawText(
      batchSize
        ? `in your batch of ${batchSize}`
        : "in your batch",
      137,
      790,
      13,
      "600",
      "#91a8d2"
    );
  } else {
    drawText(
      "✦",
      90,
      765,
      28,
      "900",
      "#8d7cff"
    );

    drawText(
      "KEEP CLIMBING",
      135,
      755,
      22,
      "900",
      "#ffffff"
    );

    drawText(
      "Your next achievement is waiting.",
      137,
      790,
      13,
      "600",
      "#91a8d2"
    );
  }

  /* Badge */

  if (badge) {
    fillRoundRect(
      W - 390,
      740,
      285,
      70,
      35,
      "rgba(255,194,77,0.13)"
    );

    drawText(
      "★",
      W - 350,
      775,
      24,
      "900",
      "#ffd166"
    );

    drawText(
      badge,
      W - 315,
      775,
      16,
      "800",
      "#ffe3a1"
    );
  }

  /* ---------------------------------------
     Motivation card
  --------------------------------------- */

  fillRoundRect(
    55,
    870,
    W - 110,
    205,
    30,
    "rgba(255,255,255,0.055)"
  );

  drawText(
    "YOUR NEXT STEP",
    90,
    915,
    12,
    "800",
    "#75e8d0"
  );

  let message =
    "Every test makes you stronger. Keep going!";

  if (score >= 90) {
    message =
      "Outstanding work! You're building serious momentum. Keep pushing your limits.";
  } else if (score >= 75) {
    message =
      "Great progress! One more focused round and you'll be even closer to the top.";
  } else if (score >= 50) {
    message =
      "You're getting there. Review your weak areas, practise again, and level up.";
  }

  drawWrappedText(
    message,
    90,
    970,
    W - 180,
    34,
    24,
    "#ffffff"
  );

  drawText(
    "Small steps today. Big dreams tomorrow. ✦",
    90,
    1035,
    14,
    "600",
    "#9eb4d7"
  );

  /* ---------------------------------------
     Footer
  --------------------------------------- */

  const footerGradient =
    ctx.createLinearGradient(
      0,
      1115,
      W,
      1115
    );

  footerGradient.addColorStop(
    0,
    "#56e0c1"
  );

  footerGradient.addColorStop(
    1,
    "#8c78ff"
  );

  ctx.fillStyle =
    footerGradient;

  ctx.fillRect(
    55,
    1120,
    W - 110,
    3
  );

  drawText(
    academyName,
    55,
    1180,
    17,
    "800",
    "#ffffff"
  );

  drawText(
    "Powered by your academy",
    W - 55,
    1180,
    13,
    "600",
    "#8199c2",
    "right"
  );

  drawText(
    "PROGRESS  •  PRACTICE  •  ACHIEVE",
    W / 2,
    1260,
    12,
    "800",
    "#7188ae",
    "center"
  );

  /* ---------------------------------------
     Convert to image
  --------------------------------------- */

  const blob =
    await new Promise<Blob | null>(
      (resolve) =>
        canvas.toBlob(
          resolve,
          "image/png",
          1
        )
    );

  if (!blob) return;

  const safeAcademyName =
    academyName
      .replace(
        /[^a-zA-Z0-9]+/g,
        "-"
      )
      .replace(
        /^-+|-+$/g,
        ""
      );

  const file =
    new File(
      [blob],
      `${safeAcademyName || "academy"}-achievement-${result.testId}.png`,
      {
        type: "image/png",
      }
    );

  /* ---------------------------------------
     Native share
  --------------------------------------- */

  try {
    if (
      navigator.share &&
      navigator.canShare?.({
        files: [file],
      })
    ) {
      await navigator.share({
        title: `${academyName} Achievement`,
        text: `🏆 ${studentName} scored ${score.toFixed(
          0
        )}% in ${subject}!`,
        files: [file],
      });

      return;
    }
  } catch {
    // User cancelled sharing.
  }

  /* ---------------------------------------
     Desktop fallback
  --------------------------------------- */

  const url =
    URL.createObjectURL(blob);

  const anchor =
    document.createElement("a");

  anchor.href = url;

  anchor.download =
    file.name;

  document.body.appendChild(
    anchor
  );

  anchor.click();

  anchor.remove();

  URL.revokeObjectURL(url);
}

  return (
    <main className="min-h-screen bg-[#f5f7fb] text-slate-900">
      <style jsx>{`@keyframes ptBadgePop {0%{transform:scale(.2) rotate(-12deg);opacity:0}70%{transform:scale(1.12) rotate(3deg);opacity:1}100%{transform:scale(1) rotate(0)}} @keyframes ptLevelPop {0%{transform:scale(.55);opacity:0}65%{transform:scale(1.08);opacity:1}100%{transform:scale(1);opacity:1}} @keyframes ptConfetti {0%{transform:translateY(-20px) rotate(0deg);opacity:0}15%{opacity:1}100%{transform:translateY(180px) rotate(540deg);opacity:0}}`}</style>
      <header className="sticky top-0 z-40 h-[72px] bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-[1400px] mx-auto h-full px-4 lg:px-6 flex items-center justify-between gap-4">
          {/* Academy branding */}
          <div className="flex items-center gap-3 min-w-0">
            <div className="w-10 h-10 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold text-lg overflow-hidden shrink-0">
              {academyBranding?.logo_data ? (
                <img
                  src={
                    academyBranding.logo_data
                  }
                  alt={`${academyName} logo`}
                  className="w-full h-full object-contain bg-white"
                />
              ) : (
                academyName
                  .charAt(0)
                  .toUpperCase()
              )}
            </div>

            <div className="min-w-0">
              <h1 className="font-bold text-sm sm:text-base truncate">
                {academyName}
              </h1>

              <p className="text-xs text-slate-400">
                Test Result
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => router.push("/dashboard")}
              className="hidden sm:block h-10 px-4 rounded-xl border border-slate-200 bg-white text-sm font-semibold text-slate-700 hover:bg-slate-50 transition"
            >
              Dashboard
            </button>
            <StudentAccountMenu studentName={studentName} />
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={downloadResult}
              className="h-10 px-4 rounded-xl bg-blue-600 text-white text-sm font-semibold hover:bg-blue-700 transition"
            >
              ↓ Download Result
            </button>

            <button type="button" onClick={() => void shareResultCard()} className="h-10 px-4 rounded-xl bg-violet-600 text-white text-sm font-semibold hover:bg-violet-700 transition">
            🏆 Share Achievement
            </button>

            {result.allowReattempt &&
              result.automatic &&
              result.scheduledTestId && (
                <button
                  type="button"
                  onClick={startReattempt}
                  className="h-10 px-4 rounded-xl border border-amber-200 bg-amber-50 text-sm font-semibold text-amber-800 hover:bg-amber-100 transition"
                >
                  Reattempt Test
                </button>
              )}

            <button
              type="button"
              onClick={() =>
                router.push("/tests")
              }
              className="hidden sm:block h-10 px-4 rounded-xl border border-slate-200 bg-white text-sm font-semibold text-slate-700 hover:bg-slate-50 transition"
            >
              Back to Tests
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-[1400px] mx-auto p-4 sm:p-6 lg:p-8">
        {gameProgress && (
          <div className="mb-6 relative overflow-hidden rounded-[30px] bg-gradient-to-r from-slate-950 via-indigo-950 to-purple-950 p-6 text-white shadow-2xl">
            <div className="absolute -right-10 -top-16 h-44 w-44 rounded-full bg-fuchsia-500/20 blur-3xl" />
            <div className="relative flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
              <div><div className="text-[10px] font-black uppercase tracking-[.25em] text-indigo-200">⚡ Mission Complete</div><div className="mt-1 text-2xl font-black">Level {gameProgress.level} • {gameProgress.levelName}</div><div className="mt-1 text-sm font-semibold text-slate-300">+{gameProgress.points.toLocaleString()} XP • 🔥 {gameProgress.streak} day streak</div></div>
              <div className="min-w-[240px]"><div className="flex justify-between text-[10px] font-black uppercase tracking-wider text-slate-400"><span>Next level</span><span>{gameProgress.nextLevelName ? `${Math.max(0,(gameProgress.nextLevelAt||0)-gameProgress.qualifyingTests)} tests to ${gameProgress.nextLevelName}` : "GOAT"}</span></div><div className="mt-2 h-3 rounded-full bg-white/10 p-0.5"><div className="h-full rounded-full bg-gradient-to-r from-cyan-300 via-indigo-400 to-fuchsia-400" style={{width:`${gameProgress.levelProgress}%`}}/></div></div>
            </div>
          </div>
        )}
        <div className="bg-white border border-slate-200 rounded-3xl shadow-sm overflow-hidden">
          <div className="p-6 sm:p-8 lg:p-10">
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
              <div>
                <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-50 border border-green-100 text-green-700 text-xs font-bold">
                  <span className="w-2 h-2 rounded-full bg-green-500" />
                  TEST COMPLETED
                </div>

                <h1 className="mt-4 text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight">
                  Your Test Result
                </h1>

                <p className="mt-2 text-sm text-slate-500">
                  {result.automatic
                    ? "Your test was automatically submitted due to exam security or time expiry."
                    : "Your test has been successfully submitted and evaluated."}
                </p>
              </div>

              <div className="text-left lg:text-right">
                <p className="text-xs uppercase tracking-wider font-bold text-slate-400">
                  Performance
                </p>

                <p className="mt-1 text-xl font-bold text-blue-600">
                  {grade}
                </p>
              </div>
            </div>
          </div>

          <div className="border-t border-slate-100 bg-slate-50/60 p-6 sm:p-8">
            <div className="grid grid-cols-1 lg:grid-cols-[260px_1fr] gap-8 items-center">
              <div className="flex justify-center">
                <div className="relative w-52 h-52">
                  <svg
                    viewBox="0 0 200 200"
                    className="w-full h-full -rotate-90"
                  >
                    <circle
                      cx="100"
                      cy="100"
                      r="78"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="16"
                      className="text-slate-200"
                    />

                    <circle
                      cx="100"
                      cy="100"
                      r="78"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="16"
                      strokeLinecap="round"
                      className="text-blue-600"
                      strokeDasharray={
                        2 *
                        Math.PI *
                        78
                      }
                      strokeDashoffset={
                        2 *
                        Math.PI *
                        78 *
                        (1 -
                          percentage /
                            100)
                      }
                    />
                  </svg>

                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-4xl font-bold text-slate-900">
                      {percentage}%
                    </span>

                    <span className="mt-1 text-xs font-semibold text-slate-400">
                      SCORE
                    </span>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 xl:grid-cols-4 gap-3">
                <div className="rounded-2xl bg-white border border-green-100 p-5">
                  <div className="w-10 h-10 rounded-xl bg-green-50 text-green-600 flex items-center justify-center font-bold">
                    ✓
                  </div>

                  <p className="mt-4 text-2xl font-bold text-green-700">
                    {result.correct}
                  </p>

                  <p className="mt-1 text-xs font-semibold text-slate-400">
                    Correct
                  </p>
                </div>

                <div className="rounded-2xl bg-white border border-red-100 p-5">
                  <div className="w-10 h-10 rounded-xl bg-red-50 text-red-600 flex items-center justify-center font-bold">
                    ×
                  </div>

                  <p className="mt-4 text-2xl font-bold text-red-700">
                    {result.wrong}
                  </p>

                  <p className="mt-1 text-xs font-semibold text-slate-400">
                    Wrong
                  </p>
                </div>

                <div className="rounded-2xl bg-white border border-slate-200 p-5">
                  <div className="w-10 h-10 rounded-xl bg-slate-100 text-slate-600 flex items-center justify-center font-bold">
                    —
                  </div>

                  <p className="mt-4 text-2xl font-bold text-slate-700">
                    {result.unattempted}
                  </p>

                  <p className="mt-1 text-xs font-semibold text-slate-400">
                    Unattempted
                  </p>
                </div>

                <div className="rounded-2xl bg-white border border-blue-100 p-5">
                  <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center font-bold">
                    %
                  </div>

                  <p className="mt-4 text-2xl font-bold text-blue-700">
                    {accuracy}%
                  </p>

                  <p className="mt-1 text-xs font-semibold text-slate-400">
                    Accuracy
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6 grid grid-cols-1 lg:grid-cols-3 gap-5">
          <div className="lg:col-span-2 bg-white border border-slate-200 rounded-2xl shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-bold text-slate-900">
                  Test Overview
                </h2>

                <p className="mt-1 text-xs text-slate-400">
                  Summary of this attempt
                </p>
              </div>

              <div className="px-3 py-1.5 rounded-lg bg-blue-50 text-blue-700 text-xs font-bold">
                {result.total} Questions
              </div>
            </div>

            <div className="mt-6 grid grid-cols-2 sm:grid-cols-3 gap-4">
              <InfoItem
                label="Exam"
                value={
                  result.course ||
                  "Mock Test"
                }
              />

              <InfoItem
                label="Subject"
                value={
                  result.subject ||
                  "Multiple Subjects"
                }
              />

              <InfoItem
                label="Attempted"
                value={`${attempted}/${result.total}`}
              />

              <InfoItem
                label="Duration"
                value={
                  result.duration
                    ? `${result.duration} min`
                    : "—"
                }
              />

              <InfoItem
                label="Difficulty"
                value={
                  result.difficulty ||
                  "Mixed"
                }
              />

              <InfoItem
                label="Status"
                value={
                  result.automatic
                    ? "Auto Submitted"
                    : "Submitted"
                }
              />
            </div>
          </div>

          <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6">
            <h2 className="font-bold text-slate-900">
              Performance
            </h2>

            <p className="mt-1 text-xs text-slate-400">
              Your answer breakdown
            </p>

            <div className="mt-6 space-y-5">
              <PerformanceBar
                label="Correct"
                value={result.correct}
                total={result.total}
              />

              <PerformanceBar
                label="Wrong"
                value={result.wrong}
                total={result.total}
              />

              <PerformanceBar
                label="Unattempted"
                value={
                  result.unattempted
                }
                total={result.total}
              />
            </div>
          </div>
        </div>

        <div className="mt-6 bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
          <div className="p-6 border-b border-slate-100">
            <h2 className="font-bold text-slate-900">
              Question Review
            </h2>

            <p className="mt-1 text-xs text-slate-400">
              Review your answers and correct
              answers
            </p>
          </div>

          <div className="divide-y divide-slate-100">
            {result.questions.length ===
            0 ? (
              <div className="p-10 text-center">
                <p className="text-sm font-semibold text-slate-700">
                  Questions are not
                  available for this result.
                </p>

                <p className="mt-2 text-xs text-slate-400">
                  Your score was saved, but
                  the question data could not
                  be loaded.
                </p>
              </div>
            ) : (
              result.questions.map(
                (
                  question,
                  index
                ) => {
                  const selected =
                    getSelectedAnswer(
                      result.answers,
                      question,
                      index
                    );

                  const hasAnswer =
                    selected !== null;

                  const isCorrect =
                    hasAnswer &&
                    question.answer !==
                      null &&
                    selected ===
                      question.answer;

                  const status =
                    isCorrect
                      ? "Correct"
                      : hasAnswer
                        ? "Wrong"
                        : "Unattempted";

                  return (
                    <div
                      key={
                        question.id ||
                        index
                      }
                      className="p-5 sm:p-7"
                    >
                      <div className="flex items-start gap-4">
                        <div
                          className={[
                            "w-10 h-10 shrink-0 rounded-xl flex items-center justify-center font-bold text-sm",
                            isCorrect
                              ? "bg-green-50 text-green-700"
                              : hasAnswer
                                ? "bg-red-50 text-red-700"
                                : "bg-slate-100 text-slate-600",
                          ].join(" ")}
                        >
                          {question.number ||
                            index + 1}
                        </div>

                        <div className="flex-1 min-w-0">
                          <div className="flex flex-wrap items-center gap-2">
                            <span
                              className={[
                                "px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-wide",
                                isCorrect
                                  ? "bg-green-50 text-green-700"
                                  : hasAnswer
                                    ? "bg-red-50 text-red-700"
                                    : "bg-slate-100 text-slate-500",
                              ].join(" ")}
                            >
                              {status}
                            </span>

                            {question.subject && (
                              <span className="px-2.5 py-1 rounded-md bg-slate-50 text-[10px] font-semibold text-slate-500">
                                {
                                  question.subject
                                }
                              </span>
                            )}

                            {question.chapter && (
                              <span className="px-2.5 py-1 rounded-md bg-slate-50 text-[10px] font-semibold text-slate-500">
                                {
                                  question.chapter
                                }
                              </span>
                            )}

                            {question.difficulty && (
                              <span className="px-2.5 py-1 rounded-md bg-slate-50 text-[10px] font-semibold text-slate-500">
                                {
                                  question.difficulty
                                }
                              </span>
                            )}

                            <span className="px-2.5 py-1 rounded-md bg-blue-50 text-[10px] font-semibold text-blue-700">
                              ⏱ {Math.floor(Number(result.timeSpent?.[question.id] || 0) / 60)}m {Number(result.timeSpent?.[question.id] || 0) % 60}s
                            </span>
                          </div>

                          <div className="mt-4 rounded-2xl bg-slate-50 border border-slate-100 p-5">
                            <div className="text-sm sm:text-base font-medium leading-7 text-slate-800">
                              <MathText
                                text={
                                  question.question
                                }
                              />
                            </div>
                          </div>
                        </div>
                      </div>

                      <div className="mt-5 ml-0 sm:ml-14 space-y-2">
                        {question.options
                          .length > 0 ? (
                          question.options.map(
                            (
                              option,
                              optionIndex
                            ) => {
                              const isSelected =
                                hasAnswer &&
                                Number(
                                  selected
                                ) ===
                                  optionIndex;

                              const isCorrectOption =
                                question.answer !==
                                  null &&
                                Number(
                                  question.answer
                                ) ===
                                  optionIndex;

                              let optionClass =
                                "border-slate-200 bg-white";

                              if (
                                isCorrectOption
                              ) {
                                optionClass =
                                  "border-green-300 bg-green-50/70";
                              } else if (
                                isSelected
                              ) {
                                optionClass =
                                  "border-red-300 bg-red-50/70";
                              }

                              return (
                                <div
                                  key={
                                    optionIndex
                                  }
                                  className={[
                                    "rounded-xl border-2 p-4 flex items-start gap-3 transition",
                                    optionClass,
                                  ].join(
                                    " "
                                  )}
                                >
                                  <span
                                    className={[
                                      "w-9 h-9 shrink-0 rounded-lg flex items-center justify-center text-sm font-bold border",
                                      isCorrectOption
                                        ? "bg-green-600 text-white border-green-600"
                                        : isSelected
                                          ? "bg-red-600 text-white border-red-600"
                                          : "bg-slate-50 text-slate-500 border-slate-200",
                                    ].join(
                                      " "
                                    )}
                                  >
                                    {String.fromCharCode(
                                      65 +
                                        optionIndex
                                    )}
                                  </span>

                                  <div className="flex-1 min-w-0 pt-1">
                                    <MathText
                                      text={String(
                                        option ??
                                          ""
                                      )}
                                      className="text-sm sm:text-[15px] text-slate-700 leading-7"
                                    />
                                  </div>

                                  <div className="shrink-0 pt-1">
                                    {isCorrectOption && (
                                      <span className="inline-flex items-center rounded-full bg-green-100 px-2.5 py-1 text-[10px] font-bold text-green-700">
                                        Correct Answer
                                      </span>
                                    )}

                                    {isSelected &&
                                      !isCorrectOption && (
                                        <span className="inline-flex items-center rounded-full bg-red-100 px-2.5 py-1 text-[10px] font-bold text-red-700">
                                          Your Answer
                                        </span>
                                      )}
                                  </div>
                                </div>
                              );
                            }
                          )
                        ) : (
                          <div className="rounded-xl border border-amber-200 bg-amber-50 p-4">
                            <p className="text-xs font-semibold text-amber-800">
                              Options are not available for this question.
                            </p>
                          </div>
                        )}
                      </div>

                      <div className="mt-5 ml-0 sm:ml-14 grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div
                          className={[
                            "rounded-xl border p-4",
                            hasAnswer
                              ? isCorrect
                                ? "border-green-200 bg-green-50"
                                : "border-red-200 bg-red-50"
                              : "border-slate-200 bg-slate-50",
                          ].join(" ")}
                        >
                          <p className="text-[10px] uppercase tracking-wide font-bold text-slate-400">
                            Your Answer
                          </p>

                          {hasAnswer ? (
                            <div
                              className={[
                                "mt-2 text-sm font-bold",
                                isCorrect
                                  ? "text-green-700"
                                  : "text-red-700",
                              ].join(" ")}
                            >
                              <div className="flex items-start gap-2">
                                <span className="shrink-0">
                                  {String.fromCharCode(
                                    65 +
                                      Number(
                                        selected
                                      )
                                  )}
                                  .
                                </span>

                                <MathText
                                  text={
                                    question
                                      .options[
                                      Number(
                                        selected
                                      )
                                    ]
                                      ? String(
                                          question
                                            .options[
                                            Number(
                                              selected
                                            )
                                          ]
                                        )
                                      : ""
                                  }
                                  className="leading-7"
                                />
                              </div>
                            </div>
                          ) : (
                            <p className="mt-2 text-sm font-bold text-slate-500">
                              Not Attempted
                            </p>
                          )}
                        </div>

                        <div className="rounded-xl border border-green-200 bg-green-50 p-4">
                          <p className="text-[10px] uppercase tracking-wide font-bold text-green-600">
                            Correct Answer
                          </p>

                          {question.answer !==
                            null &&
                          question.answer !==
                            undefined &&
                          Number.isFinite(
                            Number(
                              question.answer
                            )
                          ) ? (
                            <div className="mt-2 text-sm font-bold text-green-800">
                              <div className="flex items-start gap-2">
                                <span className="shrink-0">
                                  {String.fromCharCode(
                                    65 +
                                      Number(
                                        question.answer
                                      )
                                  )}
                                  .
                                </span>

                                <MathText
                                  text={
                                    question
                                      .options[
                                      Number(
                                        question.answer
                                      )
                                    ]
                                      ? String(
                                          question
                                            .options[
                                            Number(
                                              question.answer
                                            )
                                          ]
                                        )
                                      : ""
                                  }
                                  className="leading-7"
                                />
                              </div>
                            </div>
                          ) : (
                            <p className="mt-2 text-sm font-bold text-green-800">
                              Correct answer unavailable
                            </p>
                          )}
                        </div>
                      </div>

                      {question.solution && (
                        <div className="mt-5 ml-0 sm:ml-14 rounded-2xl bg-blue-50 border border-blue-100 p-5">
                          <div className="flex items-center gap-2">
                            <div className="w-7 h-7 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center text-xs font-bold">
                              i
                            </div>

                            <p className="text-xs font-bold text-blue-700 uppercase tracking-wide">
                              Solution
                            </p>
                          </div>

                          <div className="mt-3 text-sm leading-7 text-blue-900">
                            <MathText
                              text={String(
                                question.solution
                              )}
                            />
                          </div>
                        </div>
                      )}
                    </div>
                  );
                }
              )
            )}
          </div>
        </div>

        <div className="mt-6 flex flex-col sm:flex-row gap-3 justify-center">
          <button
            type="button"
            onClick={downloadResult}
            className="h-12 px-7 rounded-xl bg-blue-600 text-white text-sm font-semibold hover:bg-blue-700 transition"
          >
            ↓ Download Complete Result
          </button>

          <button
            type="button"
            onClick={() =>
              router.push("/tests")
            }
            className="h-12 px-7 rounded-xl border border-slate-200 bg-white text-sm font-semibold text-slate-700 hover:bg-slate-50 transition"
          >
            ← Back to Tests
          </button>
        </div>
      </div>

      {celebrationBadge && (
        <div className="fixed inset-0 z-[120] flex items-center justify-center bg-slate-950/80 p-4 backdrop-blur-md" onClick={() => setCelebrationBadge(null)}>
          <div className="relative w-full max-w-md overflow-hidden rounded-[32px] bg-white shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="pointer-events-none absolute inset-0 overflow-hidden">
              {[0,1,2,3,4,5,6,7,8,9].map((piece) => <span key={piece} className="absolute top-8 left-1/2 h-2 w-1.5 rounded-full bg-indigo-400" style={{left:`${10 + piece * 9}%`, animation:`ptConfetti ${1.1 + piece * .08}s ease-out ${piece * .04}s both`}} />)}
            </div>
            <div className="relative bg-gradient-to-br from-slate-950 via-indigo-950 to-purple-950 px-8 py-10 text-center text-white">
              <div className="text-xs font-black uppercase tracking-[.28em] text-indigo-200">🎉 NEW ACHIEVEMENT</div>
              <div className="mx-auto mt-6 flex h-36 w-36 items-center justify-center rounded-[36px] bg-gradient-to-br from-amber-300 via-yellow-400 to-orange-500 shadow-2xl" style={{animation:"ptBadgePop .7s cubic-bezier(.2,.8,.2,1) both"}}>
                {celebrationBadge.asset ? <img src={celebrationBadge.asset} alt={celebrationBadge.name} className="h-32 w-32 object-contain drop-shadow-2xl" /> : <span className="text-7xl">{celebrationBadge.icon || "🏆"}</span>}
              </div>
              <h2 className="mt-6 text-3xl font-black">{celebrationBadge.name}{celebrationBadge.tier ? ` ${["I","II","III","IV"][celebrationBadge.tier-1]}` : ""}</h2>
              <p className="mt-2 text-sm font-semibold text-slate-300">{celebrationBadge.detail}</p>
            </div>
            <div className="p-5">
              <div className="grid grid-cols-2 gap-3">
                <button type="button" onClick={() => { const text = `🏆 I unlocked ${celebrationBadge.name}! 🔥 ${gameProgress?.streak || 0} day streak • Level ${gameProgress?.level || 1} ${gameProgress?.levelName || "Rookie"}.`; window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, "_blank", "noopener,noreferrer"); }} className="rounded-xl bg-[#25D366] px-4 py-3 text-xs font-black text-white">WhatsApp</button>
                <button type="button" onClick={() => setCelebrationBadge(null)} className="rounded-xl bg-slate-950 px-4 py-3 text-xs font-black text-white">Continue</button>
              </div>
              <p className="mt-3 text-center text-[10px] font-semibold text-slate-400">Your new achievement is now visible in the Trophy Wall.</p>
            </div>
          </div>
        </div>
      )}

      {levelUp && (
        <div className="fixed inset-0 z-[130] flex items-center justify-center bg-slate-950/85 p-4 backdrop-blur-md" onClick={() => setLevelUp(null)}>
          <div className="relative w-full max-w-md overflow-hidden rounded-[32px] bg-gradient-to-br from-indigo-950 via-purple-950 to-slate-950 p-8 text-center text-white shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="pointer-events-none absolute inset-0 overflow-hidden">
              {[0,1,2,3,4,5,6,7].map((piece) => <span key={piece} className="absolute top-0 left-1/2 text-2xl" style={{left:`${8 + piece * 12}%`, animation:`ptConfetti ${1.2 + piece * .1}s ease-out ${piece * .05}s both`}}>✦</span>)}
            </div>
            <div className="relative" style={{animation:"ptLevelPop .75s cubic-bezier(.2,.8,.2,1) both"}}>
              <div className="text-xs font-black uppercase tracking-[.3em] text-cyan-200">⭐ LEVEL UP!</div>
              <div className="mx-auto mt-7 flex h-32 w-32 items-center justify-center rounded-full border-4 border-cyan-300/30 bg-white/10 text-6xl shadow-[0_0_70px_rgba(103,232,249,.28)]">⭐</div>
              <div className="mt-6 text-6xl font-black tracking-tight">LEVEL {levelUp.level}</div>
              <div className="mt-2 text-xl font-black text-cyan-200">{levelUp.levelName}</div>
              <p className="mt-3 text-sm font-semibold text-white/60">You just reached a new milestone. Keep going!</p>
              <button type="button" onClick={() => setLevelUp(null)} className="mt-7 w-full rounded-xl bg-white px-5 py-3 text-xs font-black text-slate-950">Continue</button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}

function InfoItem({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl bg-slate-50 border border-slate-100 p-4">
      <p className="text-[10px] uppercase tracking-wide font-bold text-slate-400">
        {label}
      </p>

      <p className="mt-1 text-sm font-bold text-slate-800 truncate">
        {value}
      </p>
    </div>
  );
}

function PerformanceBar({
  label,
  value,
  total,
}: {
  label: string;
  value: number;
  total: number;
}) {
  const percentage =
    total > 0
      ? Math.round(
          (value / total) * 100
        )
      : 0;

  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-semibold text-slate-600">
          {label}
        </span>

        <span className="text-xs font-bold text-slate-800">
          {value}{" "}
          <span className="text-slate-400 font-medium">
            ({percentage}%)
          </span>
        </span>
      </div>

      <div className="h-2.5 rounded-full bg-slate-100 overflow-hidden">
        <div
          className="h-full bg-blue-500 rounded-full transition-all"
          style={{
            width: `${percentage}%`,
          }}
        />
      </div>
    </div>
  );
}