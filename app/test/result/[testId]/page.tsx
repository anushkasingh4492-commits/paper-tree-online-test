"use client";
import { useEffect, useMemo, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import jsPDF from "jspdf";

type Question = {
  id: string;
  number: number;
  question: string;
  options: string[];
  answer: number;
  subject?: string;
  chapter?: string;
  difficulty?: string;
  solution?: string | null;
  figureAsset?: string | null;
};

type ResultData = {
  testId: string;
  total: number;
  correct: number;
  wrong: number;
  unattempted: number;
  answers: Record<string, number>;
  marked: Record<string, boolean>;
  questions: Question[];
  submittedAt?: string;
  automatic?: boolean;

  course?: string;
  subject?: string;
  chapters?: string[];
  difficulty?: string;
  duration?: number;
};

export default function TestResultPage() {
  const params = useParams();
  const router = useRouter();

  const testId = String(params.testId);

  const [result, setResult] = useState<ResultData | null>(null);
  const [loading, setLoading] = useState(true);

  /*
   * =========================================================
   * LOAD RESULT
   * =========================================================
   */

  useEffect(() => {
    try {
      const storedResult = localStorage.getItem(
        `test-${testId}-result`
      );

      if (!storedResult) {
        console.error(
          "No result found for test:",
          testId
        );

        setLoading(false);
        return;
      }

      const parsed: ResultData =
        JSON.parse(storedResult);

      setResult(parsed);
    } catch (error) {
      console.error(
        "Could not load result:",
        error
      );
    } finally {
      setLoading(false);
    }
  }, [testId]);

  /*
   * =========================================================
   * DERIVED DATA
   * =========================================================
   */

  const percentage = useMemo(() => {
    if (!result || result.total <= 0) {
      return 0;
    }

    return Math.round(
      (result.correct / result.total) * 100
    );
  }, [result]);

  const accuracy = useMemo(() => {
    if (!result) {
      return 0;
    }

    const attempted =
      result.correct + result.wrong;

    if (attempted === 0) {
      return 0;
    }

    return Math.round(
      (result.correct / attempted) * 100
    );
  }, [result]);

  const attempted = result
    ? result.correct + result.wrong
    : 0;

  /*
   * =========================================================
   * GRADE
   * =========================================================
   */

  const grade = useMemo(() => {
    if (percentage >= 90) return "Excellent";
    if (percentage >= 75) return "Very Good";
    if (percentage >= 60) return "Good";
    if (percentage >= 40) return "Needs Improvement";
    return "Keep Practicing";
  }, [percentage]);

  /*
   * =========================================================
   * DOWNLOAD COMPLETE RESULT PDF
   * =========================================================
   */

  function downloadResult() {
    if (!result) {
      return;
    }

    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 14;
    const contentWidth = pageWidth - margin * 2;
    let y = 18;

    const ensureSpace = (height: number) => {
      if (y + height > pageHeight - margin) {
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
      doc.setFont("helvetica", bold ? "bold" : "normal");
      doc.setFontSize(fontSize);

      const lines = doc.splitTextToSize(
        String(text ?? ""),
        contentWidth
      );

      const requiredHeight = lines.length * lineHeight;
      ensureSpace(requiredHeight + 3);
      doc.text(lines, margin, y);
      y += requiredHeight + 3;
    };

    doc.setTextColor(23, 32, 51);
    doc.setFont("helvetica", "bold");
    doc.setFontSize(20);
    doc.text(
      "Paper Tree • Test Result",
      margin,
      y
    );
    y += 8;

    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    doc.text(
      `Test ID: ${result.testId}`,
      margin,
      y
    );
    y += 5;

    if (result.submittedAt) {
      doc.text(
        `Submitted: ${new Date(result.submittedAt).toLocaleString()}`,
        margin,
        y
      );
      y += 5;
    }

    y += 3;
    doc.setDrawColor(220, 224, 232);
    doc.line(margin, y, pageWidth - margin, y);
    y += 8;

    addWrappedText(
      `Exam: ${result.course || "Mock Test"}`,
      11,
      5.5,
      true
    );
    addWrappedText(
      `Subject: ${result.subject || "Multiple Subjects"}`,
      11,
      5.5
    );
    addWrappedText(
      `Difficulty: ${result.difficulty || "Mixed"}`,
      11,
      5.5
    );
    addWrappedText(
      `Duration: ${result.duration ? `${result.duration} min` : "—"}`,
      11,
      5.5
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
    doc.setDrawColor(220, 224, 232);
    doc.line(margin, y, pageWidth - margin, y);
    y += 8;

    addWrappedText(
      "Question-by-Question Review",
      15,
      7,
      true
    );

    result.questions.forEach((question, index) => {
      const selected = result.answers[question.id];
      const hasAnswer =
        selected !== undefined &&
        selected !== null;

      const isCorrect =
        hasAnswer &&
        Number(selected) ===
          Number(question.answer);

      const status = isCorrect
        ? "Correct"
        : hasAnswer
        ? "Wrong"
        : "Unattempted";

      ensureSpace(18);

      addWrappedText(
        `${question.number || index + 1}. ${question.question}`,
        11,
        6,
        true
      );

      addWrappedText(
        `Status: ${status}`,
        10,
        5
      );

      question.options.forEach(
        (option, optionIndex) => {
          const isSelected =
            selected === optionIndex;
          const isCorrectOption =
            Number(question.answer) ===
            optionIndex;

          let suffix = "";

          if (isCorrectOption) {
            suffix = " [Correct Answer]";
          } else if (isSelected) {
            suffix = " [Your Answer]";
          }

          addWrappedText(
            `${String.fromCharCode(65 + optionIndex)}. ${option}${suffix}`,
            10,
            5
          );
        }
      );

      if (question.solution) {
        addWrappedText(
          `Solution: ${question.solution}`,
          10,
          5
        );
      }

      y += 4;
    });

    doc.save(
      `paper-tree-result-${result.testId}.pdf`
    );
  }

  /*
   * =========================================================
   * LOADING
   * =========================================================
   */

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

  /*
   * =========================================================
   * RESULT NOT FOUND
   * =========================================================
   */

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
            We could not find the saved result for
            this test.
          </p>

          <p className="mt-4 text-xs text-slate-400 break-all">
            {testId}
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

  /*
   * =========================================================
   * MAIN RESULT PAGE
   * =========================================================
   */

  return (
    <main className="min-h-screen bg-[#f5f7fb] text-slate-900">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <header className="sticky top-0 z-40 h-[72px] bg-white border-b border-slate-200 shadow-sm">

        <div className="max-w-[1400px] mx-auto h-full px-4 lg:px-6 flex items-center justify-between gap-4">

          <div className="flex items-center gap-3">

            <div className="w-10 h-10 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold text-lg">
              P
            </div>

            <div>

              <h1 className="font-bold text-sm sm:text-base">
                Paper Tree
              </h1>

              <p className="text-xs text-slate-400">
                Test Result
              </p>

            </div>

          </div>

          <div className="flex items-center gap-2">

            <button
              type="button"
              onClick={downloadResult}
              className="h-10 px-4 rounded-xl bg-blue-600 text-white text-sm font-semibold hover:bg-blue-700 transition"
            >
              ↓ Download Result
            </button>

            <button
              type="button"
              onClick={() =>
                router.push("/tests")
              }
              className="h-10 px-4 rounded-xl border border-slate-200 bg-white text-sm font-semibold text-slate-700 hover:bg-slate-50 transition"
            >
              Back to Tests
            </button>

          </div>

        </div>

      </header>

      {/* =====================================================
          CONTENT
      ===================================================== */}

      <div className="max-w-[1400px] mx-auto p-4 sm:p-6 lg:p-8">

        {/* ===================================================
            SUCCESS BANNER
        =================================================== */}

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

          {/* =================================================
              SCORE
          ================================================= */}

          <div className="border-t border-slate-100 bg-slate-50/60 p-6 sm:p-8">

            <div className="grid grid-cols-1 lg:grid-cols-[260px_1fr] gap-8 items-center">

              {/* SCORE CIRCLE */}

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

              {/* STAT CARDS */}

              <div className="grid grid-cols-2 xl:grid-cols-4 gap-3">

                {/* CORRECT */}

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

                {/* WRONG */}

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

                {/* UNATTEMPTED */}

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

                {/* ACCURACY */}

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

        {/* ===================================================
            TEST INFORMATION
        =================================================== */}

        <div className="mt-6 grid grid-cols-1 lg:grid-cols-3 gap-5">

          {/* TEST INFO */}

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

          {/* PERFORMANCE */}

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
                value={result.unattempted}
                total={result.total}
              />

            </div>

          </div>

        </div>

        {/* ===================================================
            QUESTION REVIEW
        =================================================== */}

        <div className="mt-6 bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">

          <div className="p-6 border-b border-slate-100">

            <h2 className="font-bold text-slate-900">
              Question Review
            </h2>

            <p className="mt-1 text-xs text-slate-400">
              Review your answers and correct answers
            </p>

          </div>

          <div className="divide-y divide-slate-100">

            {result.questions.map(
              (question, index) => {

                const selected =
                  result.answers[
                    question.id
                  ];

                const hasAnswer =
                  selected !==
                  undefined &&
                  selected !== null;

                const isCorrect =
                  hasAnswer &&
                  Number(selected) ===
                    Number(
                      question.answer
                    );

                return (
                  <div
                    key={
                      question.id ||
                      index
                    }
                    className="p-5 sm:p-6"
                  >

                    {/* QUESTION TOP */}

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
                              "px-2.5 py-1 rounded-md text-[10px] font-bold uppercase",
                              isCorrect
                                ? "bg-green-50 text-green-700"
                                : hasAnswer
                                ? "bg-red-50 text-red-700"
                                : "bg-slate-100 text-slate-500",
                            ].join(" ")}
                          >
                            {isCorrect
                              ? "Correct"
                              : hasAnswer
                              ? "Wrong"
                              : "Unattempted"}
                          </span>

                          {question.subject && (
                            <span className="text-[10px] font-semibold text-slate-400">
                              {question.subject}
                            </span>
                          )}

                          {question.difficulty && (
                            <span className="text-[10px] font-semibold text-slate-400">
                              •{" "}
                              {question.difficulty}
                            </span>
                          )}

                        </div>

                        <p className="mt-3 text-sm sm:text-base font-medium leading-7 text-slate-800 whitespace-pre-wrap">
                          {question.question}
                        </p>

                      </div>

                    </div>

                    {/* OPTIONS */}

                    <div className="mt-5 ml-0 sm:ml-14 space-y-2">

                      {question.options.map(
                        (
                          option,
                          optionIndex
                        ) => {

                          const isSelected =
                            selected ===
                            optionIndex;

                          const isCorrectOption =
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
                              "border-green-300 bg-green-50";
                          } else if (
                            isSelected
                          ) {
                            optionClass =
                              "border-red-300 bg-red-50";
                          }

                          return (
                            <div
                              key={
                                optionIndex
                              }
                              className={[
                                "rounded-xl border p-3.5 flex items-start gap-3",
                                optionClass,
                              ].join(
                                " "
                              )}
                            >

                              <span
                                className={[
                                  "w-8 h-8 shrink-0 rounded-lg flex items-center justify-center text-xs font-bold border",
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

                              <span className="pt-1 text-sm text-slate-700 leading-6 flex-1">
                                {option}
                              </span>

                              {isCorrectOption && (
                                <span className="text-xs font-bold text-green-700 pt-1">
                                  Correct
                                </span>
                              )}

                              {isSelected &&
                                !isCorrectOption && (
                                  <span className="text-xs font-bold text-red-700 pt-1">
                                    Your answer
                                  </span>
                                )}

                            </div>
                          );
                        }
                      )}

                    </div>

                    {/* SOLUTION */}

                    {question.solution && (
                      <div className="mt-5 ml-0 sm:ml-14 rounded-xl bg-blue-50 border border-blue-100 p-4">

                        <p className="text-xs font-bold text-blue-700 uppercase tracking-wide">
                          Solution
                        </p>

                        <p className="mt-2 text-sm leading-6 text-blue-900 whitespace-pre-wrap">
                          {question.solution}
                        </p>

                      </div>
                    )}

                  </div>
                );
              }
            )}

          </div>

        </div>

        {/* ===================================================
            BOTTOM ACTIONS
        =================================================== */}

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

          <button
            type="button"
            onClick={() =>
              router.push(
                `/test/${testId}`
              )
            }
            className="h-12 px-7 rounded-xl border border-blue-200 bg-blue-50 text-blue-700 text-sm font-semibold hover:bg-blue-100 transition"
          >
            View Test
          </button>

        </div>

      </div>

    </main>
  );
}

/*
 * =========================================================
 * INFO ITEM
 * =========================================================
 */

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

/*
 * =========================================================
 * PERFORMANCE BAR
 * =========================================================
 */

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