"use client";

import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { useParams, useRouter } from "next/navigation";
import jsPDF from "jspdf";
import "katex/dist/katex.min.css";
import { InlineMath, BlockMath } from "react-katex";
import AcademyBranding from "@/components/AcademyBranding";
import StudentAccountMenu from "@/components/StudentAccountMenu";
import MotivationalLoader from "@/components/MotivationalLoader";
type Question = {
  id: string;
  number: number;
  question: string;
  options: string[];
  subject?: string;
  chapter?: string;
  difficulty?: string;
  figureAsset?: string | null;
  question_type?: "MCQ" | "MULTI_SELECT" | "TITA";
  answer_format?: string;
  max_selections?: number;
  accepted_answers?: string[];
};

type TestData = {
  id: string;
  exam?: string;
  question_count: number;
  questions: Question[] | string;
  created_at?: string;
  tab_switch_warnings?: number;
};

type Answers = Record<string, number | number[] | string>;
type Marked = Record<string, boolean>;
type Visited = Record<string, boolean>;
type QuestionTimes = Record<string, number>;
type CalculatorOperation = "+" | "-" | "*" | "/";
type CalculatorState = {
  display: string;
  accumulator: number | null;
  operation: CalculatorOperation | null;
  waitingForOperand: boolean;
  error: string | null;
};

/*
 * =========================================================
 * MATH / EQUATION RENDERER
 * =========================================================
 *
 * Supports:
 *
 * $v = u + at$
 * \(v = u + at\)
 * $$...$$
 * \[...\]
 *
 * It also converts common plain-text notation such as:
 *
 * m s^-1  -> m s⁻¹
 * x^2     -> x²
 * x^-1    -> x⁻¹
 * rho     -> ρ in common physics cases
 *
 * If your uploaded question contains proper LaTeX,
 * KaTeX renders it properly.
 */

function convertSimpleSuperscripts(
  text: string
): React.ReactNode {
  const superscriptMap: Record<
    string,
    string
  > = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
    "+": "⁺",
    "-": "⁻",
    "=": "⁼",
    "(": "⁽",
    ")": "⁾",
    n: "ⁿ",
    i: "ⁱ",
  };

  const parts = text.split(
    /(\^-?\d+|\^\([^)]+\))/g
  );

  return parts.map(
    (part, index) => {
      if (
        part.startsWith("^")
      ) {
        let value =
          part.slice(1);

        if (
          value.startsWith("(") &&
          value.endsWith(")")
        ) {
          value = value.slice(
            1,
            -1
          );
        }

        const converted =
          value
            .split("")
            .map(
              (char) =>
                superscriptMap[
                  char
                ] ?? char
            )
            .join("");

        return (
          <sup
            key={index}
            className="text-[0.72em] leading-none"
          >
            {converted}
          </sup>
        );
      }

      return (
        <span key={index}>
          {part}
        </span>
      );
    }
  );
}

function MathText({
  text,
  block = false,
}: {
  text: string;
  block?: boolean;
}) {
  const value = String(
    text ?? ""
  );

  /*
   * If the entire string is wrapped
   * in display math delimiters.
   */

  if (
    value.startsWith("$$") &&
    value.endsWith("$$")
  ) {
    const math = value.slice(
      2,
      -2
    );

    return (
      <div className="my-3 overflow-x-auto">
        <BlockMath
          math={math}
          errorColor="#64748b"
        />
      </div>
    );
  }

  if (
    value.startsWith("\\[") &&
    value.endsWith("\\]")
  ) {
    const math = value.slice(
      2,
      -2
    );

    return (
      <div className="my-3 overflow-x-auto">
        <BlockMath
          math={math}
          errorColor="#64748b"
        />
      </div>
    );
  }

  /*
   * Find inline/display LaTeX inside normal text.
   */

  const regex =
    /(\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$[^$\n]+\$)/g;

  const parts =
    value.split(regex);

  return (
    <>
      {parts.map(
        (part, index) => {
          if (!part) {
            return null;
          }

          if (
            part.startsWith("$$") &&
            part.endsWith("$$")
          ) {
            return (
              <span
                key={index}
                className="block overflow-x-auto my-3"
              >
                <BlockMath
                  math={part.slice(
                    2,
                    -2
                  )}
                  errorColor="#64748b"
                />
              </span>
            );
          }

          if (
            part.startsWith("\\[") &&
            part.endsWith("\\]")
          ) {
            return (
              <span
                key={index}
                className="block overflow-x-auto my-3"
              >
                <BlockMath
                  math={part.slice(
                    2,
                    -2
                  )}
                  errorColor="#64748b"
                />
              </span>
            );
          }

          if (
            part.startsWith("\\(") &&
            part.endsWith("\\)")
          ) {
            return (
              <InlineMath
                key={index}
                math={part.slice(
                  2,
                  -2
                )}
                errorColor="#64748b"
              />
            );
          }

          if (
            part.startsWith("$") &&
            part.endsWith("$")
          ) {
            return (
              <InlineMath
                key={index}
                math={part.slice(
                  1,
                  -1
                )}
                errorColor="#64748b"
              />
            );
          }

          return (
            <span key={index}>
              {convertSimpleSuperscripts(
                part
              )}
            </span>
          );
        }
      )}
    </>
  );
}
function getFigureSrc(value: unknown): string | null {
  if (typeof value !== "string" || !value.trim()) {
    return null;
  }

  const asset = value.trim();

  if (/^(https?:|data:|blob:)/i.test(asset)) {
    return asset;
  }

  if (asset.startsWith("/api/")) {
    return asset;
  }

  if (asset.startsWith("/figures/")) {
    return asset;
  }

  const relativeAsset = asset.replace(/^\/+/, "");

  return `/api/question-asset?path=${encodeURIComponent(
    relativeAsset
  )}`;
}

/*
 * =========================================================
 * MAIN COMPONENT
 * =========================================================
 */

export default function TestPage() {
  const params = useParams();
  const router = useRouter();

  const testId = String(
    params.testId
  );

  const [studentName, setStudentName] = useState("Student");

  useEffect(() => {
    setStudentName(localStorage.getItem("studentName") || "Student");
  }, []);

  const [test, setTest] =
    useState<TestData | null>(
      null
    );

  const [loading, setLoading] =
    useState(true);

  const [motivationDone, setMotivationDone] =
    useState(false);

  const [error, setError] =
    useState("");

  const [answers, setAnswers] =
    useState<Answers>({});

  const [marked, setMarked] =
    useState<Marked>({});

  const [visited, setVisited] =
    useState<Visited>({});

  const [
    currentQuestion,
    setCurrentQuestion,
  ] = useState(0);

  const [timeLeft, setTimeLeft] =
    useState(0);

  const [questionTimes, setQuestionTimes] = useState<QuestionTimes>({});
  const [showExplain, setShowExplain] = useState(false);


  const [
    showWarning,
    setShowWarning,
  ] = useState(false);

  const [showLeaveWarning, setShowLeaveWarning] = useState(false);

  const [
    submitting,
    setSubmitting,
  ] = useState(false);

  const [
    downloadingPaper,
    setDownloadingPaper,
  ] = useState(false);


  /* =========================================================
   * CAT-SPECIFIC STATE (calculator)
   * Only used when the exam is CAT.
   * ========================================================= */
  const [calculatorOpen, setCalculatorOpen] = useState(false);
  const [calculatorState, setCalculatorState] =
    useState<CalculatorState>({
      display: "0",
      accumulator: null,
      operation: null,
      waitingForOperand: false,
      error: null,
    });

  const isCAT =
    test != null &&
    (String(test.exam ?? "").trim().toLowerCase() === "cat" ||
      String(test.exam ?? "").trim().toLowerCase() === "cat 2025" ||
      String(test.exam ?? "").trim().toLowerCase() === "cat 2026");

  const [titaInputs, setTitaInputs] = useState<Record<string, string>>({});
  const [titaKeyboardShift, setTitaKeyboardShift] = useState(false);

  const submittedRef =
    useRef(false);

  const navigatingToResultRef =
    useRef(false);

  const leaveCountRef = useRef(0);

  const startedAtRef =
    useRef<number | null>(null);

  const scheduledEndAtRef =
    useRef<number | null>(null);

  /*
   * =========================================================
   * IMAGE HELPERS
   * =========================================================
   */

  function getImageFormatFromDataUrl(
    dataUrl: string
  ): "PNG" | "JPEG" {
    if (
      dataUrl.startsWith(
        "data:image/jpeg"
      ) ||
      dataUrl.startsWith(
        "data:image/jpg"
      )
    ) {
      return "JPEG";
    }

    return "PNG";
  }

  async function loadImageAsDataUrl(
    src: string
  ): Promise<string | null> {
    try {
      if (
        src.startsWith(
          "data:image/"
        )
      ) {
        return src;
      }

      const response =
        await fetch(src);

      if (!response.ok) {
        throw new Error(
          `Image request failed: ${response.status}`
        );
      }

      const blob =
        await response.blob();

      return await new Promise(
        (resolve) => {
          const reader =
            new FileReader();

          reader.onloadend = () => {
            resolve(
              typeof reader.result ===
                "string"
                ? reader.result
                : null
            );
          };

          reader.onerror = () =>
            resolve(null);

          reader.readAsDataURL(
            blob
          );
        }
      );
    } catch (error) {
      console.warn(
        "Could not load figure for PDF:",
        src,
        error
      );

      return null;
    }
  }

  async function addFigureToPdf(
    doc: jsPDF,
    src: string,
    margin: number,
    contentWidth: number,
    pageHeight: number,
    currentY: number
  ): Promise<number> {
    const dataUrl =
      await loadImageAsDataUrl(
        src
      );

    if (!dataUrl) {
      return currentY;
    }

    try {
      const image =
        new Image();

      image.src = dataUrl;

      await new Promise<void>(
        (resolve) => {
          if (image.complete) {
            resolve();
            return;
          }

          image.onload = () =>
            resolve();

          image.onerror = () =>
            resolve();
        }
      );

      const imageWidth =
        image.naturalWidth ||
        image.width ||
        800;

      const imageHeight =
        image.naturalHeight ||
        image.height ||
        500;

      const maxWidth =
        Math.min(
          contentWidth,
          170
        );

      const maxHeight =
        90;

      const scale =
        Math.min(
          maxWidth /
            imageWidth,
          maxHeight /
            imageHeight
        );

      const displayWidth =
        imageWidth * scale;

      const displayHeight =
        imageHeight * scale;

      let y = currentY;

      if (
        y +
          displayHeight +
          10 >
        pageHeight - margin
      ) {
        doc.addPage();
        y = margin;
      }

      const x =
        margin +
        (contentWidth -
          displayWidth) /
          2;

      doc.addImage(
        dataUrl,
        getImageFormatFromDataUrl(
          dataUrl
        ),
        x,
        y,
        displayWidth,
        displayHeight
      );

      return (
        y +
        displayHeight +
        7
      );
    } catch (error) {
      console.warn(
        "Could not add figure to PDF:",
        error
      );

      return currentY;
    }
  }

  /*
   * =========================================================
   * DOWNLOAD QUESTION PAPER
   * =========================================================
   */

  async function downloadQuestionPaper() {
    if (
      !questions.length ||
      downloadingPaper
    ) {
      return;
    }

    setDownloadingPaper(true);

    try {
      const doc = new jsPDF();

      const pageWidth =
        doc.internal.pageSize.getWidth();

      const pageHeight =
        doc.internal.pageSize.getHeight();

      const margin = 14;

      const contentWidth =
        pageWidth -
        margin * 2;

      let y = 18;

      const addWrappedText = (
        text: string,
        fontSize = 11,
        lineHeight = 6,
        bold = false
      ) => {
        doc.setFont(
          "helvetica",
          bold ? "bold" : "normal"
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

        if (
          y + requiredHeight >
          pageHeight - margin
        ) {
          doc.addPage();
          y = margin;
        }

        doc.text(
          lines,
          margin,
          y
        );

        y +=
          requiredHeight + 2;
      };

      doc.setTextColor(
        23,
        32,
        51
      );

      doc.setFont(
        "helvetica",
        "bold"
      );

      doc.setFontSize(20);

      doc.text(
        test?.exam ||
          "Mock Test",
        margin,
        y
      );

      y += 8;

      doc.setFont(
        "helvetica",
        "normal"
      );

      doc.setFontSize(10);

      doc.text(
        `Question Paper • ${questions.length} Questions`,
        margin,
        y
      );

      y += 5;

      doc.text(
        `Test ID: ${testId}`,
        margin,
        y
      );

      y += 10;

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

      for (
        let index = 0;
        index <
        questions.length;
        index++
      ) {
        const question =
          questions[index];

        addWrappedText(
          `${question.number || index + 1}. ${question.question}`,
          12,
          6.5,
          true
        );

        /*
         * IMPORTANT:
         *
         * figureAsset is defined in the
         * normalized question object.
         */

        if (
          question.figureAsset
        ) {
          y =
            await addFigureToPdf(
              doc,
              question.figureAsset,
              margin,
              contentWidth,
              pageHeight,
              y
            );
        }

        question.options.forEach(
          (
            option,
            optionIndex
          ) => {
            addWrappedText(
              `${String.fromCharCode(
                65 + optionIndex
              )}. ${option}`,
              10.5,
              5.5,
              false
            );
          }
        );

        y += 3;
      }

      doc.save(
        `paper-tree-question-paper-${testId}.pdf`
      );
    } catch (error) {
      console.error(
        "QUESTION PAPER DOWNLOAD ERROR:",
        error
      );

      alert(
        "Could not generate the question paper. Please try again."
      );
    } finally {
      setDownloadingPaper(
        false
      );
    }
  }

  /*
   * =========================================================
   * LOAD TEST
   * =========================================================
   */

  useEffect(() => {
    async function loadTest() {
      try {
        setLoading(true);
        setError("");

        const response =
          await fetch(
            `/api/tests/${testId}`,
            {
              cache: "no-store",
              credentials: "include",
            }
          );

        const data =
          await response.json();

        console.log(
          "TEST API RESPONSE:",
          data
        );

        if (!response.ok) {
          throw new Error(
            data?.error ||
              "Failed to load test"
          );
        }

        const dbTest =
          data?.test ?? data;
          console.log(
  "QUESTION WITH IMAGE DATA:",
  data?.test?.questions?.find(
    (q: any) =>
      q.figureAsset ||
      q.figure_asset ||
      q.image ||
      q.image_url ||
      q.imageUrl
  )
);

        if (!dbTest) {
          throw new Error(
            "Test not found"
          );
        }

        let rawQuestions =
          dbTest.questions;

        if (
          typeof rawQuestions ===
          "string"
        ) {
          rawQuestions =
            JSON.parse(
              rawQuestions
            );
        }

        if (
          !Array.isArray(
            rawQuestions
          )
        ) {
          throw new Error(
            "Questions are not in a valid format"
          );
        }

        /*
         * =====================================================
         * NORMALIZE QUESTIONS
         * =====================================================
         */

        const normalizedQuestions: Question[] =
          rawQuestions.map(
            (
              question: Record<string, unknown>,
              index: number
            ) => {
              /*
               * OPTIONS
               */

              let options: unknown =
                question.options;

              if (
                options &&
                !Array.isArray(
                  options
                ) &&
                typeof options ===
                  "object"
              ) {
                const optionRecord =
                  options as Record<string, unknown>;

                const orderedOptions =
                  [
                    "A",
                    "B",
                    "C",
                    "D",
                    "E",
                  ]
                    .filter(
                      (letter) =>
                        Object.prototype.hasOwnProperty.call(
                          optionRecord,
                          letter
                        )
                    )
                    .map(
                      (letter) =>
                        optionRecord[
                          letter
                        ]
                    );

                options =
                  orderedOptions.length
                    ? orderedOptions
                    : Object.values(
                        optionRecord
                      );
              }

              const normalizedOptions: string[] =
                Array.isArray(options)
                  ? options.map(
                      (
                        option: unknown
                      ) =>
                        String(
                          option ?? ""
                        )
                    )
                  : [];

              /*
               * =================================================
               * FIGURE
               * =================================================
               *
               * THIS IS THE IMPORTANT FIX.
               *
               * Define figureAsset BEFORE returning the
               * object. This prevents:
               *
               * "No value exists in scope for shorthand
               * property 'figureAsset'"
               */

            const rawFigureAsset =
  question.figureAsset ??
  question.figure_asset ??
  null;

const figureAsset =
  getFigureSrc(rawFigureAsset);

              /*
               * QUESTION TEXT
               */

              const questionText =
                String(
                  question.question ??
                    question.stem ??
                    ""
                );
              const questionType = String(
                question.question_type ??
                  question.answer_format ??
                  ""
              )
                .trim()
                .toUpperCase();

              /*
               * NORMALIZED QUESTION
               */

              return {
                id:
                  String(
                    question.id ??
                      ""
                  ) ||
                  `question-${index + 1}`,

                number:
                  Number(
                    question.number
                  ) ||
                  index + 1,

                question:
                  questionText,

                options: normalizedOptions,

                question_type:
                  questionType === "TITA"
                    ? "TITA"
                    : questionType === "MULTI_SELECT"
                      ? "MULTI_SELECT"
                      : questionType === "MCQ"
                        ? "MCQ"
                        : undefined,

                answer_format:
                  typeof question.answer_format === "string"
                    ? question.answer_format
                    : undefined,

                accepted_answers:
                  Array.isArray(question.accepted_answers)
                    ? question.accepted_answers.map((answer) =>
                        String(answer)
                      )
                    : undefined,

                max_selections:
                  typeof question.max_selections === "number"
                    ? question.max_selections
                    : undefined,

                subject:
                  typeof question.subject === "string"
                    ? question.subject
                    : undefined,

                chapter:
                  typeof question.chapter === "string"
                    ? question.chapter
                    : typeof question.chapter_name === "string"
                      ? question.chapter_name
                      : undefined,

                difficulty:
                  typeof question.difficulty === "string"
                    ? question.difficulty
                    : undefined,

                /*
                 * Correctly initialized.
                 */
                figureAsset,
              };
            }
          );

        console.log(
          "NORMALIZED QUESTIONS:",
          normalizedQuestions
        );

        console.log(
          "FIGURE QUESTIONS:",
          normalizedQuestions.filter(
            (question) =>
              Boolean(
                question.figureAsset
              )
          )
        );

        setTest({
          ...dbTest,
          questions:
            normalizedQuestions,
        });

        /*
         * RESTORE ANSWERS
         */

        try {
          const savedAnswers =
            localStorage.getItem(
              `test-${testId}-answers`
            );

          if (savedAnswers) {
            const parsed =
              JSON.parse(
                savedAnswers
              );

            if (
              parsed &&
              typeof parsed ===
                "object"
            ) {
              setAnswers(
                parsed
              );
            }
          }
        } catch (error) {
          console.warn(
            "Could not restore answers:",
            error
          );
        }

        /*
         * RESTORE MARKED
         */

        try {
          const savedMarked =
            localStorage.getItem(
              `test-${testId}-marked`
            );

          if (savedMarked) {
            const parsed =
              JSON.parse(
                savedMarked
              );

            if (
              parsed &&
              typeof parsed ===
                "object"
            ) {
              setMarked(
                parsed
              );
            }
          }
        } catch (error) {
          console.warn(
            "Could not restore marked questions:",
            error
          );
        }

        /*
         * RESTORE VISITED
         */

        try {
          const savedVisited =
            localStorage.getItem(
              `test-${testId}-visited`
            );

          if (savedVisited) {
            const parsed =
              JSON.parse(
                savedVisited
              );

            if (
              parsed &&
              typeof parsed ===
                "object"
            ) {
              setVisited(
                parsed
              );
            }
          }
        } catch (error) {
          console.warn(
            "Could not restore visited questions:",
            error
          );
        }

        /*
         * TIMER CONFIG
         */

        let durationMinutes = 30;
        let scheduledEndAt: number | null = null;

        try {
          const config =
            localStorage.getItem(
              `test-config-${testId}`
            );

          if (config) {
            const parsedConfig =
              JSON.parse(
                config
              );

            const configuredDuration =
              Number(
                parsedConfig?.duration
              );

            if (
              Number.isFinite(
                configuredDuration
              ) &&
              configuredDuration > 0
            ) {
              durationMinutes =
                configuredDuration;
            }

            const configuredEndTime =
              new Date(
                parsedConfig?.endTime
              ).getTime();

            if (
              Number.isFinite(
                configuredEndTime
              )
            ) {
              scheduledEndAt =
                configuredEndTime;
            }
          }
        } catch (error) {
          console.warn(
            "Could not read test config:",
            error
          );
        }

        /*
         * START TIME
         */

        const startedKey =
          `test-${testId}-startedAt`;

        let startedAt =
          Number(
            localStorage.getItem(
              startedKey
            )
          );

        if (
          !Number.isFinite(
            startedAt
          ) ||
          startedAt <= 0
        ) {
          startedAt =
            Date.now();

          localStorage.setItem(
            startedKey,
            String(
              startedAt
            )
          );
        }

        startedAtRef.current =
          startedAt;

        const totalSeconds =
          Math.max(
            1,
            Math.round(
              durationMinutes *
                60
            )
          );

        scheduledEndAtRef.current =
          scheduledEndAt;

        const scheduledRemainingSeconds =
          scheduledEndAt
            ? Math.floor(
                (scheduledEndAt -
                  Date.now()) /
                  1000
              )
            : totalSeconds;

        const elapsedSeconds =
          Math.floor(
            (Date.now() -
              startedAt) /
              1000
          );

        setTimeLeft(
          Math.max(
            0,
            Math.min(
              totalSeconds -
                elapsedSeconds,
              scheduledRemainingSeconds
            )
          )
        );
      } catch (err) {
        console.error(
          "LOAD TEST ERROR:",
          err
        );

        setError(
          err instanceof Error
            ? err.message
            : "Unable to load test"
        );
      } finally {
        setLoading(false);
      }
    }

    if (testId) {
      loadTest();
    }
  }, [testId]);

  /*
   * =========================================================
   * QUESTIONS
   * =========================================================
   */

  const questions =
    useMemo(
      () =>
        Array.isArray(
          test?.questions
        )
          ? test.questions
          : [],
      [test]
    );

  const current =
    questions[
      currentQuestion
    ];

  /*
   * =========================================================
   * PER-QUESTION TIME TRACKING
   * =========================================================
   */

  useEffect(() => {
    const question = questions[currentQuestion];
    if (!question) return;
    const interval = window.setInterval(() => {
      setQuestionTimes((previous) => ({ ...previous, [question.id]: (previous[question.id] || 0) + 1 }));
    }, 1000);
    return () => window.clearInterval(interval);
  }, [currentQuestion, questions]);

  /*
   * =========================================================
   * VISITED
   * =========================================================
   */

  useEffect(() => {
    const question =
      questions[
        currentQuestion
      ];

    if (!question) {
      return;
    }

    setVisited(
      (previous) => {
        if (
          previous[
            question.id
          ]
        ) {
          return previous;
        }

        return {
          ...previous,
          [question.id]:
            true,
        };
      }
    );
  }, [
    currentQuestion,
    questions,
  ]);

  /*
   * =========================================================
   * COUNTS
   * =========================================================
   */

  const answeredCount =
    useMemo(() => {
      return questions.filter(
        (question) =>
          answers[
            question.id
          ] !== undefined
      ).length;
    }, [
      answers,
      questions,
    ]);

  const remainingCount =
    Math.max(
      0,
      questions.length -
        answeredCount
    );

  /*
   * =========================================================
   * SAVE ANSWERS
   * =========================================================
   */

  useEffect(() => {
    if (!test) return;

    try {
      localStorage.setItem(
        `test-${testId}-answers`,
        JSON.stringify(
          answers
        )
      );
    } catch {}
  }, [
    answers,
    test,
    testId,
  ]);

  /*
   * =========================================================
   * SAVE MARKED
   * =========================================================
   */

  useEffect(() => {
    if (!test) return;

    try {
      localStorage.setItem(
        `test-${testId}-marked`,
        JSON.stringify(
          marked
        )
      );
    } catch {}
  }, [
    marked,
    test,
    testId,
  ]);

  /*
   * =========================================================
   * SAVE VISITED
   * =========================================================
   */

  useEffect(() => {
    if (!test) return;

    try {
      localStorage.setItem(
        `test-${testId}-visited`,
        JSON.stringify(
          visited
        )
      );
    } catch {}
  }, [
    visited,
    test,
    testId,
  ]);

  /*
   * =========================================================
   * TIMER DISPLAY
   * =========================================================
   */

  const formattedTime =
    useMemo(() => {
      const minutes =
        Math.floor(
          timeLeft / 60
        );

      const seconds =
        timeLeft % 60;

      return `${String(
        minutes
      ).padStart(
        2,
        "0"
      )}:${String(
        seconds
      ).padStart(
        2,
        "0"
      )}`;
    }, [timeLeft]);

  /*
   * =========================================================
   * SUBMIT TEST
   * =========================================================
   */

  async function submitTest(
    automatic = false
  ) {
    if (
      submittedRef.current ||
      submitting
    ) {
      return;
    }

    submittedRef.current =
      true;

    navigatingToResultRef.current =
      true;

    setSubmitting(true);

    const submittedAt =
      new Date().toISOString();

    const startedAt =
      startedAtRef.current
        ? new Date(
            startedAtRef.current
          ).toISOString()
        : new Date().toISOString();

    /*
     * SAVE PROGRESS
     */

    try {
      localStorage.setItem(
        `test-${testId}-answers`,
        JSON.stringify(
          answers
        )
      );

      localStorage.setItem(
        `test-${testId}-marked`,
        JSON.stringify(
          marked
        )
      );

      localStorage.setItem(
        `test-${testId}-visited`,
        JSON.stringify(
          visited
        )
      );
    } catch {}

    /*
     * CONFIG
     */

    let config: any = {};

    try {
      const storedConfig =
        localStorage.getItem(
          `test-config-${testId}`
        );

      if (storedConfig) {
        config =
          JSON.parse(
            storedConfig
          );
      }
    } catch {}

    /*
     * STUDENT ID
     */

    let studentId = "";

    try {
      const cookie =
        document.cookie
          .split(";")
          .map(
            (item) =>
              item.trim()
          )
          .find(
            (item) =>
              item.startsWith(
                "student_session="
              )
          );

      if (cookie) {
        const raw =
          decodeURIComponent(
            cookie.slice(
              "student_session="
                .length
            )
          );

        try {
          const parsed =
            JSON.parse(
              raw
            );

          studentId =
            String(
              parsed?.studentId ??
                ""
            ).trim();
        } catch {
          studentId =
            raw.trim();
        }
      }
    } catch {}

    /*
     * SERVER SUBMISSION
     */

    try {
      const response =
        await fetch(
          "/api/test/submit",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            credentials:
              "include",

            body: JSON.stringify({
              testId,
              scheduledTestId:
                typeof config?.scheduledTestId ===
                "string"
                  ? config.scheduledTestId
                  : undefined,
              reattempt: config?.reattempt === true,
              studentId,
              answers,
              marked,
              questionTimes,
              automatic,
              violationCount:
                automatic
                  ? 1
                  : 0,
              startedAt,
              submittedAt,
            }),
          }
        );

      const data =
        await response.json();

      console.log(
        "TEST SUBMIT RESPONSE:",
        data
      );

      if (
        !response.ok ||
        !data?.success
      ) {
        throw new Error(
          data?.error ||
            "Failed to save test submission."
        );
      }

      const total =
        Number(
          data.total ??
            questions.length
        );

      const correct =
        Number(
          data.correct ?? 0
        );

      const wrong =
        Number(
          data.wrong ?? 0
        );

      const unattempted =
        Number(
          data.unattempted ?? 0
        );

      const score =
        Number(
          data.score ?? 0
        );

      const accuracy =
        Number(
          data.accuracy ?? 0
        );

      const result = {
        testId,

        attemptId:
          data.attemptId ??
          null,

        scheduledTestId:
          data.scheduledTestId ??
          (typeof config?.scheduledTestId === "string" ? config.scheduledTestId : undefined),

        allowReattempt: data.allowReattempt === true,

        total,
        correct,
        wrong,
        unattempted,

        answers,
        timeSpent: questionTimes,
        marked,
        questions,

        submittedAt,
        automatic,

        score,
        accuracy,

        course:
          typeof config?.course ===
          "string"
            ? config.course
            : "",

        subject:
          typeof config?.subject ===
          "string"
            ? config.subject
            : "",

        chapters:
          Array.isArray(
            config?.chapters
          )
            ? config.chapters
            : [],

        difficulty:
          typeof config?.difficulty ===
          "string"
            ? config.difficulty
            : "",

        duration:
          Number.isFinite(
            Number(
              config?.duration
            )
          )
            ? Number(
                config.duration
              )
            : undefined,
      };

      localStorage.setItem(
        `test-${testId}-result`,
        JSON.stringify(
          result
        )
      );

      localStorage.setItem(
        `submitted-${testId}`,
        "true"
      );

      localStorage.setItem(
        "paperTreeDashboardRefresh",
        String(
          Date.now()
        )
      );

      window.dispatchEvent(
        new Event(
          "paperTreeDashboardRefresh"
        )
      );

      setShowWarning(false);

      router.replace(
        `/test/result/${testId}`
      );
    } catch (error) {
      console.error(
        "TEST SUBMISSION ERROR:",
        error
      );

      submittedRef.current =
        false;

      navigatingToResultRef.current =
        false;

      setSubmitting(false);

      setShowWarning(false);

      alert(
        error instanceof Error
          ? error.message
          : "Failed to submit test. Please try again."
      );
    }
  }

  /*
   * =========================================================
   * TIMER
   * =========================================================
   */

  useEffect(() => {
    if (
      !test ||
      loading
    ) {
      return;
    }

    const interval =
      window.setInterval(() => {
        if (
          !startedAtRef.current
        ) {
          return;
        }

        if (
          submittedRef.current
        ) {
          window.clearInterval(
            interval
          );

          return;
        }

        let durationMinutes =
          30;
        let scheduledEndAt =
          scheduledEndAtRef.current;

        try {
          const config =
            localStorage.getItem(
              `test-config-${testId}`
            );

          if (config) {
            const parsedConfig =
              JSON.parse(
                config
              );

            const configuredDuration =
              Number(
                parsedConfig?.duration
              );

            if (
              Number.isFinite(
                configuredDuration
              ) &&
              configuredDuration > 0
            ) {
              durationMinutes =
                configuredDuration;
            }

            const configuredEndTime =
              new Date(
                parsedConfig?.endTime
              ).getTime();

            if (
              Number.isFinite(
                configuredEndTime
              )
            ) {
              scheduledEndAt =
                configuredEndTime;
              scheduledEndAtRef.current =
                configuredEndTime;
            }
          }
        } catch {}

        const totalSeconds =
          Math.max(
            1,
            Math.round(
              durationMinutes *
                60
            )
          );

        const elapsed =
          Math.floor(
            (Date.now() -
              startedAtRef.current) /
              1000
          );

        const remaining =
          Math.max(
            0,
            totalSeconds -
              elapsed
          );

        const scheduledRemaining =
          scheduledEndAt
            ? Math.max(
                0,
                Math.floor(
                  (scheduledEndAt -
                    Date.now()) /
                    1000
                )
              )
            : remaining;

        setTimeLeft(
          Math.min(
            remaining,
            scheduledRemaining
          )
        );

        if (
          Math.min(
            remaining,
            scheduledRemaining
          ) <= 0 &&
          !submittedRef.current
        ) {
          window.clearInterval(
            interval
          );

          submitTest(
            true
          );
        }
      }, 1000);

    return () =>
      window.clearInterval(
        interval
      );
  }, [
    test,
    loading,
    testId,
  ]);

  /*
   * Best-effort browser screenshot deterrents. Websites cannot block
   * operating-system or external-camera screenshots, but we can disable
   * common browser shortcuts, context-menu capture and printing.
   */
  useEffect(() => {
    if (!test || loading) return;

    const blockContextMenu = (event: MouseEvent) => event.preventDefault();
    const blockPrintShortcuts = (event: KeyboardEvent) => {
      const key = event.key.toLowerCase();
      if (
        event.key === "PrintScreen" ||
        ((event.ctrlKey || event.metaKey) && ["p", "s"].includes(key))
      ) {
        event.preventDefault();
      }
    };
    const blockPrint = () => window.alert("Printing is disabled during a test.");

    document.addEventListener("contextmenu", blockContextMenu);
    document.addEventListener("keydown", blockPrintShortcuts, true);
    window.addEventListener("beforeprint", blockPrint);

    return () => {
      document.removeEventListener("contextmenu", blockContextMenu);
      document.removeEventListener("keydown", blockPrintShortcuts, true);
      window.removeEventListener("beforeprint", blockPrint);
    };
  }, [test, loading]);

  /*
   * =========================================================
   * TAB LEAVE / VISIBILITY WARNING
   * =========================================================
   *
   * This remains enabled.
   *
   * Switching browser tabs causes document.visibilityState
   * to become "hidden".
   *
   * The test is automatically submitted.
   */

  useEffect(() => {
    if (
      !test ||
      loading
    ) {
      return;
    }

    if (leaveCountRef.current === 0) {
      try {
        const savedLeaveCount = Number(localStorage.getItem(`test-${testId}-leave-count`) || 0);
        if (Number.isFinite(savedLeaveCount) && savedLeaveCount > 0) {
          leaveCountRef.current = Math.min(100, Math.floor(savedLeaveCount));
        }
      } catch {}
    }

    function saveProgress() {
      try {
        localStorage.setItem(
          `test-${testId}-answers`,
          JSON.stringify(
            answers
          )
        );

        localStorage.setItem(
          `test-${testId}-marked`,
          JSON.stringify(
            marked
          )
        );

        localStorage.setItem(
          `test-${testId}-visited`,
          JSON.stringify(
            visited
          )
        );
      } catch {}
    }

    function submitForLeavingTest() {
      if (
        submittedRef.current ||
        navigatingToResultRef.current ||
        submitting
      ) {
        return;
      }

      saveProgress();
      leaveCountRef.current += 1;
      try {
        localStorage.setItem(`test-${testId}-leave-count`, String(leaveCountRef.current));
      } catch {}

      const allowedWarnings = Math.max(
        0,
        Math.min(1, Number(test?.tab_switch_warnings ?? 0))
      );

      if (leaveCountRef.current <= allowedWarnings) {
        // First leave: warn but keep the test and answers intact.
        setShowLeaveWarning(true);
        return;
      }

      // Any leave after the configured warning count auto-submits.
      setShowWarning(true);
      submitTest(true);
    }

    function handleVisibilityChange() {
      if (document.visibilityState === "hidden") {
        submitForLeavingTest();
      }
    }

    /*
     * Browser refresh / close protection.
     */

    function handleBeforeUnload(
      event: BeforeUnloadEvent
    ) {
      if (
        submittedRef.current ||
        navigatingToResultRef.current
      ) {
        return;
      }

      saveProgress();

      event.preventDefault();

      event.returnValue = "";
    }

    document.addEventListener(
      "visibilitychange",
      handleVisibilityChange
    );
    window.addEventListener(
      "beforeunload",
      handleBeforeUnload
    );

    return () => {
      document.removeEventListener(
        "visibilitychange",
        handleVisibilityChange
      );
      window.removeEventListener(
        "beforeunload",
        handleBeforeUnload
      );
    };
  }, [
    test,
    loading,
    submitting,
    testId,
    answers,
    marked,
    visited,
  ]);


  /*
   * =========================================================
   * ANSWER
   * =========================================================
   */

  function selectAnswer(
    optionIndex: number
  ) {
    if (!current) {
      return;
    }

    /* CAT MULTI_SELECT: toggle instead of replace. */
    if (
      isCAT &&
      (current.question_type === "MULTI_SELECT" ||
        current.max_selections != null &&
        current.max_selections > 1)
    ) {
      toggleMultiSelectAnswer(optionIndex);
      return;
    }

    setAnswers(
      (previous) => ({
        ...previous,
        [current.id]:
          optionIndex,
      })
    );
  }

  function setTitaAnswer(value: string) {
    if (!current) return;
    setTitaInputs((previous) => ({
      ...previous,
      [current.id]: value,
    }));
    setAnswers((previous) => ({
      ...previous,
      [current.id]: value,
    }));
  }

  function pressTitaKey(key: string) {
    if (!current) return;

    const value = titaInputs[current.id] ?? "";

    if (key === "clear") {
      setTitaAnswer("");
    } else if (key === "backspace") {
      setTitaAnswer(value.slice(0, -1));
    } else if (value.length < 500) {
      setTitaAnswer(value + key);
    }
  }

  /* =========================================================
   * CAT CALCULATOR
   * ========================================================= */
  const calculatorPress = useCallback((key: string) => {
    setCalculatorState((previous) => {
      const initialState: CalculatorState = {
        display: "0",
        accumulator: null,
        operation: null,
        waitingForOperand: false,
        error: null,
      };

      if (key === "C") {
        return initialState;
      }

      if (/^\d$/.test(key)) {
        const display =
          previous.error || previous.waitingForOperand
            ? key
            : previous.display === "0"
              ? key
              : previous.display + key;

        return {
          ...previous,
          display,
          waitingForOperand: false,
          error: null,
        };
      }

      if (previous.error) {
        return previous;
      }

      const currentValue = Number(previous.display);

      if (key === ".") {
        return {
          ...previous,
          display: previous.waitingForOperand
            ? "0."
            : previous.display.includes(".")
              ? previous.display
              : `${previous.display}.`,
          waitingForOperand: false,
        };
      }

      if (key === "+/-") {
        return {
          ...previous,
          display: currentValue === 0 ? "0" : String(-currentValue),
          waitingForOperand: false,
        };
      }

      if (key === "%") {
        return {
          ...previous,
          display: String(currentValue / 100),
          waitingForOperand: false,
        };
      }

      if (key === "backspace") {
        const display = previous.waitingForOperand
          ? "0"
          : previous.display.slice(0, -1) || "0";
        return {
          ...previous,
          display: display === "-" ? "0" : display,
          waitingForOperand: false,
        };
      }

      const calculate = (
        left: number,
        operation: CalculatorOperation,
        right: number
      ): number | null => {
        if (operation === "+") return left + right;
        if (operation === "-") return left - right;
        if (operation === "*") return left * right;
        if (right === 0) return null;
        return left / right;
      };

      const formatResult = (value: number) =>
        String(Number(value.toPrecision(12)));

      if (key === "=") {
        if (
          !previous.operation ||
          previous.accumulator === null
        ) {
          return previous;
        }

        const result = calculate(
          previous.accumulator,
          previous.operation,
          currentValue
        );

        if (result === null || !Number.isFinite(result)) {
          return {
            ...previous,
            accumulator: null,
            operation: null,
            waitingForOperand: true,
            error: "Cannot divide by zero.",
          };
        }

        return {
          display: formatResult(result),
          accumulator: null,
          operation: null,
          waitingForOperand: true,
          error: null,
        };
      }

      if (["+", "-", "*", "/"].includes(key)) {
        const operation = key as CalculatorOperation;

        if (
          previous.operation &&
          previous.accumulator !== null &&
          !previous.waitingForOperand
        ) {
          const result = calculate(
            previous.accumulator,
            previous.operation,
            currentValue
          );

          if (result === null || !Number.isFinite(result)) {
            return {
              ...previous,
              accumulator: null,
              operation: null,
              waitingForOperand: true,
              error: "Cannot divide by zero.",
            };
          }

          return {
            display: formatResult(result),
            accumulator: result,
            operation,
            waitingForOperand: true,
            error: null,
          };
        }

        return {
          ...previous,
          accumulator: previous.waitingForOperand
            ? previous.accumulator ?? currentValue
            : currentValue,
          operation,
          waitingForOperand: true,
        };
      }

      return previous;
    });
  }, []);

  useEffect(() => {
    if (!calculatorOpen) return;

    function handleCalculatorKeydown(event: KeyboardEvent) {
      const key = event.key;
      const mappedKey =
        /^\d$/.test(key) ||
        ["+", "-", "*", "/", ".", "%"].includes(key)
          ? key
          : key === "×"
            ? "*"
            : key === "÷"
              ? "/"
          : key.toLowerCase() === "c"
            ? "C"
          : key === "Enter" || key === "="
            ? "="
            : key === "Backspace" || key === "Delete"
              ? "backspace"
              : null;

      if (key === "Escape") {
        event.preventDefault();
        setCalculatorOpen(false);
        return;
      }

      if (mappedKey) {
        event.preventDefault();
        calculatorPress(mappedKey);
      }
    }

    window.addEventListener("keydown", handleCalculatorKeydown);
    return () =>
      window.removeEventListener("keydown", handleCalculatorKeydown);
  }, [calculatorOpen, calculatorPress]);

  function toggleMultiSelectAnswer(optionIndex: number) {
  if (!current) return;

  setAnswers((previous) => {
    const existing = Array.isArray(previous[current.id])
      ? (previous[current.id] as number[])
      : [];

    const selected = existing.includes(optionIndex)
      ? existing.filter((index) => index !== optionIndex)
      : [...existing, optionIndex];

    return {
      ...previous,
      [current.id]: selected,
    };
  });
}

  /*
   * =========================================================
   * MARK
   * =========================================================
   */

  function toggleMarked() {
    if (!current) {
      return;
    }

    setMarked(
      (previous) => ({
        ...previous,
        [current.id]:
          !previous[
            current.id
          ],
      })
    );
  }

  /*
   * =========================================================
   * LOADING
   * =========================================================
   */

  if (loading || !motivationDone) {
    return (
      <MotivationalLoader
        durationSeconds={3}
        onComplete={() => setMotivationDone(true)}
      />
    );
  }

  /*
   * =========================================================
   * ERROR
   * =========================================================
   */

  if (error) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-[#f5f7fb] p-6">
        <div className="bg-white rounded-2xl border border-slate-200 p-8 max-w-md w-full text-center shadow-sm">
          <div className="w-14 h-14 mx-auto rounded-2xl bg-red-50 text-red-600 flex items-center justify-center text-2xl font-bold">
            !
          </div>

          <h1 className="mt-5 text-xl font-bold text-slate-900">
            Unable to load test
          </h1>

          <p className="mt-3 text-sm text-slate-500">
            {error}
          </p>

          <p className="mt-4 text-xs text-slate-400 break-all">
            {testId}
          </p>

          <button
            type="button"
            onClick={() =>
              router.push(
                "/tests"
              )
            }
            className="mt-6 px-5 h-11 rounded-xl bg-blue-600 text-white text-sm font-semibold hover:bg-blue-700 transition"
          >
            Back to Tests
          </button>
        </div>
      </main>
    );
  }

  /*
   * =========================================================
   * NO QUESTIONS
   * =========================================================
   */

  if (!questions.length) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-[#f5f7fb] p-6">
        <div className="bg-white rounded-2xl border border-slate-200 p-8 max-w-md w-full text-center shadow-sm">
          <h1 className="text-xl font-bold text-slate-900">
            No questions found
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            This test does not contain any
            questions.
          </p>

          <button
            type="button"
            onClick={() =>
              router.push(
                "/tests"
              )
            }
            className="mt-6 px-5 h-11 rounded-xl bg-blue-600 text-white text-sm font-semibold"
          >
            Back to Tests
          </button>
        </div>
      </main>
    );
  }

  /*
   * =========================================================
   * TIMER STATUS
   * =========================================================
   */

  const timerCritical =
    timeLeft <= 60;

  const timerWarning =
    timeLeft <= 300;

  const answered =
    current
      ? answers[
          current.id
        ] !== undefined
      : false;

  /*
   * =========================================================
   * MAIN CBT
   * =========================================================
   */

  return (
    <main className="min-h-screen bg-[#f5f7fb] text-slate-900">
      {/* HEADER */}

      <header className="sticky top-0 z-40 h-[72px] bg-white border-b border-slate-200 shadow-sm">
        <div className="h-full max-w-[1500px] mx-auto px-4 lg:px-6 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3 min-w-0">
            <AcademyBranding variant="compact" />
            <div className="min-w-0">
              <h1 className="font-bold text-sm sm:text-base truncate">
                {test?.exam || "Mock Test"}
              </h1>
            </div>
          </div>

          <div className="hidden md:flex items-center gap-2">
            <div className="px-4 py-2 rounded-xl bg-blue-50 border border-blue-100">
              <div className="text-[10px] uppercase tracking-wide font-bold text-blue-500">
                Total
              </div>

              <div className="text-sm font-bold text-blue-700">
                {questions.length}
              </div>
            </div>

            <div className="px-4 py-2 rounded-xl bg-green-50 border border-green-100">
              <div className="text-[10px] uppercase tracking-wide font-bold text-green-600">
                Answered
              </div>

              <div className="text-sm font-bold text-green-700">
                {answeredCount}
              </div>
            </div>

            <div className="px-4 py-2 rounded-xl bg-slate-50 border border-slate-200">
              <div className="text-[10px] uppercase tracking-wide font-bold text-slate-500">
                Left
              </div>

              <div className="text-sm font-bold text-slate-700">
                {remainingCount}
              </div>
            </div>
          </div>

          <div
            className={[
              "min-w-[125px] sm:min-w-[145px] px-4 py-2 rounded-xl border transition-all",
              timerCritical
                ? "bg-red-50 border-red-200 text-red-700 animate-pulse"
                : timerWarning
                ? "bg-amber-50 border-amber-200 text-amber-700"
                : "bg-slate-50 border-slate-200 text-slate-800",
            ].join(" ")}
          >
            <div className="flex items-center justify-center gap-2">
              <span className="text-base">
                ⏱
              </span>

              <span className="text-lg sm:text-xl font-bold tabular-nums tracking-tight">
                {formattedTime}
              </span>
            </div>

            <div className="text-[9px] uppercase tracking-wider font-bold text-center opacity-70">
              Time Remaining
            </div>
          </div>

          <StudentAccountMenu studentName={studentName} activeTest />
        </div>
      </header>

      {/* MOBILE STATS */}

      <div className="md:hidden bg-white border-b border-slate-200 px-4 py-3">
        <div className="grid grid-cols-3 gap-2">
          <div className="text-center rounded-lg bg-blue-50 py-2">
            <div className="text-sm font-bold text-blue-700">
              {questions.length}
            </div>

            <div className="text-[10px] text-blue-500">
              Total
            </div>
          </div>

          <div className="text-center rounded-lg bg-green-50 py-2">
            <div className="text-sm font-bold text-green-700">
              {answeredCount}
            </div>

            <div className="text-[10px] text-green-500">
              Answered
            </div>
          </div>

          <div className="text-center rounded-lg bg-slate-50 py-2">
            <div className="text-sm font-bold text-slate-700">
              {remainingCount}
            </div>

            <div className="text-[10px] text-slate-500">
              Left
            </div>
          </div>
        </div>
      </div>

      {/* CONTENT */}

      <div className="max-w-[1500px] mx-auto p-4 lg:p-6">
        <div className="grid grid-cols-1 lg:grid-cols-[1fr_300px] gap-5">
          <section>
            {/* PROGRESS */}

            <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm mb-5">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-xs font-semibold text-blue-600 uppercase tracking-wide">
                    Question{" "}
                    {currentQuestion + 1}{" "}
                    of{" "}
                    {questions.length}
                  </p>

                  <p className="mt-1 text-sm text-slate-500">
                    {answered
                      ? "Answer selected"
                      : "Not answered yet"}
                  </p>
                </div>

                <div className="text-right">
                  <div className="text-sm font-bold text-slate-800">
                    {Math.round(
                      (answeredCount /
                        questions.length) *
                        100
                    )}
                    %
                  </div>

                  <div className="text-[10px] text-slate-400">
                    Completed
                  </div>
                </div>
              </div>

              <div className="mt-3 h-2 bg-slate-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-blue-600 rounded-full transition-all duration-300"
                  style={{
                    width: `${Math.min(
                      100,
                      Math.max(
                        0,
                        (answeredCount /
                          questions.length) *
                          100
                      )
                    )}%`,
                  }}
                ></div>
              </div>
            </div>

            <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
              <div className="px-5 sm:px-7 py-5 border-b border-slate-100 flex items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-700 flex items-center justify-center font-bold">
                    {current.number}
                  </div>

                  <div>
                    <div className="font-bold text-slate-900">
                      Question{" "}
                      {current.number}
                    </div>

                    {current.subject && (
                      <div className="text-xs text-slate-400">
                        {current.subject}
                        {current.chapter
                          ? ` • ${current.chapter}`
                          : ""}
                      </div>
                    )}
                    <div className="mt-1 text-[11px] font-semibold text-slate-400">Time on question: {Math.floor((questionTimes[current.id] || 0) / 60)}m {(questionTimes[current.id] || 0) % 60}s</div>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={
                    toggleMarked
                  }
                  className={[
                    "px-3 py-2 rounded-lg border text-xs font-semibold transition",
                    marked[
                      current.id
                    ]
                      ? "bg-red-50 border-red-200 text-red-700"
                      : "bg-white border-slate-200 text-slate-500 hover:bg-slate-50",
                  ].join(" ")}
                >
                  {marked[
                    current.id
                  ]
                    ? "Marked"
                    : "Mark"}
                </button>
              </div>

              <div className="p-5 sm:p-7">
                {/* QUESTION */}

                <div className="text-[17px] sm:text-lg leading-8 font-medium text-slate-900 whitespace-pre-wrap">
                  <MathText
                    text={
                      current.question
                    }
                  />
                </div>

                {isCAT && (
                  <div className="mt-5">
                    <button
                      type="button"
                      onClick={() => setCalculatorOpen(true)}
                      className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
                    >
                      Open calculator
                    </button>
                  </div>
                )}

                {/* FIGURE */}

                {current.figureAsset && (
                  <div className="mt-7 mb-2 flex justify-center">
                    <div className="w-full flex justify-center">
                      <img
                        src={
                          current.figureAsset
                        }
                        alt={`Figure for question ${current.number}`}
                        className="max-w-full max-h-[450px] w-auto h-auto object-contain rounded-xl border border-slate-200 bg-white p-3 shadow-sm"
                        onError={(
                          event
                        ) => {
                          console.warn(
                            "Could not load question figure:",
                            current.figureAsset
                          );

                          event.currentTarget.style.display =
                            "none";
                        }}
                      />
                    </div>
                  </div>
                )}

                {/* OPTIONS / TITA INPUT */}

                {isCAT &&
                (current.question_type === "TITA" ||
                  current.answer_format === "TITA") ? (
                  <div className="mt-7 space-y-3">
                    <textarea
                      inputMode="text"
                      autoComplete="off"
                      maxLength={500}
                      rows={3}
                      value={titaInputs[current.id] ?? ""}
                      onChange={(e) => setTitaAnswer(e.target.value.slice(0, 500))}
                      placeholder="Type your answer"
                      aria-label="TITA answer"
                      className="w-full resize-y rounded-xl border border-slate-200 bg-white px-4 py-4 text-lg font-mono text-slate-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
                    />
                    <div className="space-y-2 rounded-xl border border-slate-200 bg-slate-50 p-3">
                      {[
                        ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
                        ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
                        ["shift", "z", "x", "c", "v", "b", "n", "m", "backspace"],
                      ].map((row, rowIndex) => (
                        <div key={rowIndex} className="flex justify-center gap-1.5">
                          {row.map((key) => (
                            <button
                              key={key}
                              type="button"
                              onClick={() =>
                                key === "shift"
                                  ? setTitaKeyboardShift((value) => !value)
                                  : pressTitaKey(
                                      key === "backspace"
                                        ? key
                                        : titaKeyboardShift
                                          ? key.toUpperCase()
                                          : key
                                    )
                              }
                              aria-label={
                                key === "backspace"
                                  ? "Delete last character"
                                  : key === "shift"
                                    ? "Toggle uppercase"
                                    : `Enter ${key}`
                              }
                              className="min-w-0 flex-1 rounded-lg border border-slate-200 bg-white px-1 py-2.5 text-sm font-semibold text-slate-700 shadow-sm hover:bg-blue-50 active:bg-blue-100"
                            >
                              {key === "backspace"
                                ? "⌫"
                                : key === "shift"
                                  ? "⇧"
                                  : titaKeyboardShift
                                    ? key.toUpperCase()
                                    : key}
                            </button>
                          ))}
                        </div>
                      ))}
                      <div className="grid grid-cols-7 gap-1.5">
                        {["1", "2", "3", "4", "5", "6", "7", "8", "9", "-", ".", "0", ",", "?", "!", "'", "clear"].map(
                        (key) => (
                          <button
                            key={key}
                            type="button"
                            onClick={() => pressTitaKey(key)}
                            aria-label={
                              key === "clear" ? "Clear answer" : `Enter ${key}`
                            }
                            className="rounded-lg border border-slate-200 bg-white py-2.5 font-semibold text-slate-700 hover:bg-slate-50"
                          >
                            {key === "clear" ? "Clear" : key}
                          </button>
                        )
                      )}
                        <button
                          type="button"
                          onClick={() => pressTitaKey(" ")}
                          className="col-span-7 rounded-lg border border-slate-200 bg-white py-2.5 font-semibold text-slate-700 hover:bg-slate-50"
                        >
                          Space
                        </button>
                    </div>
                    </div>
                    <p className="text-xs text-slate-400">
                      Enter a number or text answer using your device keyboard or the on-screen keyboard. If multiple answer forms are configured, any accepted form is graded correct.
                    </p>
                  </div>
                ) : (
                  <div className="mt-7 space-y-3">
                    {current.options.map(
                      (option, index) => {
                        const isMulti =
                          current.question_type === "MULTI_SELECT" ||
                          (current.max_selections != null &&
                            current.max_selections > 1);
                        const selected = isMulti
                          ? Array.isArray(answers[current.id]) &&
                            (answers[current.id] as number[]).includes(index)
                          : answers[current.id] === index;
                        return (
                          <button
                            type="button"
                            key={index}
                            onClick={() => selectAnswer(index)}
                            className={[
                              "w-full text-left rounded-xl border p-4 sm:p-5 flex items-start gap-4 transition-all",
                              selected
                                ? "border-blue-500 bg-blue-50 shadow-sm"
                                : "border-slate-200 bg-white hover:border-blue-300 hover:bg-slate-50",
                            ].join(" ")}
                          >
                            <span
                              className={[
                                "w-9 h-9 shrink-0 rounded-lg flex items-center justify-center font-bold text-sm border",
                                selected
                                  ? "bg-blue-600 text-white border-blue-600"
                                  : "bg-slate-50 text-slate-600 border-slate-200",
                              ].join(" ")}
                            >
                              {isMulti ? (
                                selected ? (
                                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                                ) : (
                                  String.fromCharCode(65 + index)
                                )
                              ) : (
                                String.fromCharCode(65 + index)
                              )}
                            </span>
                            <span
                              className={[
                                "pt-1 text-sm sm:text-base leading-6 flex-1",
                                selected
                                  ? "text-blue-900 font-semibold"
                                  : "text-slate-700",
                              ].join(" ")}
                            >
                              <MathText text={option} />
                            </span>
                            {selected && (
                              <span className="ml-auto text-blue-600 font-bold">
                                {isMulti ? "Selected" : ""}
                              </span>
                            )}
                          </button>
                        );
                      }
                    )}
                  </div>
                )
              }
              </div>

              {/* NAVIGATION */}

              <div className="px-5 sm:px-7 py-4 border-t border-slate-100 flex flex-col sm:flex-row gap-3 justify-between">
                <button
                  type="button"
                  disabled={
                    currentQuestion ===
                    0
                  }
                  onClick={() =>
                    setCurrentQuestion(
                      (value) =>
                        Math.max(
                          0,
                          value -
                            1
                        )
                    )
                  }
                  className="h-11 px-5 rounded-xl border border-slate-200 bg-white text-sm font-semibold text-slate-700 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-50 transition"
                >
                  ← Previous
                </button>

                {currentQuestion <
                questions.length -
                  1 ? (
                  <button
                    type="button"
                    onClick={() =>
                      setCurrentQuestion(
                        (value) =>
                          Math.min(
                            questions.length -
                              1,
                            value +
                              1
                          )
                      )
                    }
                    className="h-11 px-6 rounded-xl bg-blue-600 text-white text-sm font-semibold hover:bg-blue-700 transition"
                  >
                    Save & Next →
                  </button>
                ) : (
                  <button
                    type="button"
                    onClick={() =>
                      submitTest(
                        false
                      )
                    }
                    disabled={
                      submitting
                    }
                    className="h-11 px-7 rounded-xl bg-green-600 text-white text-sm font-semibold hover:bg-green-700 transition disabled:opacity-60"
                  >
                    {submitting
                      ? "Submitting..."
                      : "Submit Test"}
                  </button>
                )}
              </div>
            </div>
          </section>

          {/* CAT CALCULATOR OVERLAY */}
          {isCAT && calculatorOpen && (
            <div
              className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
              onClick={() => setCalculatorOpen(false)}
            >
              <div
                className="bg-white rounded-2xl p-6 shadow-2xl w-full max-w-md mx-4 border border-slate-200"
                role="dialog"
                aria-modal="true"
                aria-label="CAT calculator"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-bold text-slate-900">Calculator</h3>
                  <button
                    type="button"
                    onClick={() => setCalculatorOpen(false)}
                    className="text-slate-500 hover:text-slate-700"
                  >
                    &times;
                  </button>
                </div>

                <div className="mb-4">
                  <div
                    className="mb-1 min-h-5 text-right text-xs font-mono text-slate-500"
                    aria-live="polite"
                  >
                    {calculatorState.operation &&
                    calculatorState.accumulator !== null
                      ? `${calculatorState.accumulator} ${calculatorState.operation}`
                      : "\u00a0"}
                  </div>
                  <div
                    className="text-right text-2xl font-mono text-slate-900 bg-slate-50 rounded-xl p-3 border border-slate-200 min-h-[48px] flex items-end justify-end"
                    aria-live="polite"
                    aria-label={`Calculator display: ${calculatorState.display}`}
                  >
                    {calculatorState.display}
                  </div>
                  {calculatorState.error && (
                    <p role="alert" className="mt-2 text-right text-sm text-red-600">
                      {calculatorState.error}
                    </p>
                  )}
                </div>

                <div className="grid grid-cols-4 gap-2">
                  <button type="button" onClick={() => calculatorPress("C")} className="py-3 rounded-xl border border-slate-200 bg-slate-100 text-slate-700 font-semibold hover:bg-slate-200">C</button>
                  <button type="button" onClick={() => calculatorPress("+/-")} className="py-3 rounded-xl border border-slate-200 bg-slate-100 text-slate-700 font-semibold hover:bg-slate-200">+/-</button>
                  <button type="button" onClick={() => calculatorPress("%")} className="py-3 rounded-xl border border-slate-200 bg-slate-100 text-slate-700 font-semibold hover:bg-slate-200">%</button>
                  <button type="button" onClick={() => calculatorPress("/")} className="py-3 rounded-xl border border-slate-200 bg-blue-50 text-blue-600 font-semibold hover:bg-blue-100">&divide;</button>
                  <button type="button" onClick={() => calculatorPress("7")} className="py-3 rounded-xl border border-slate-200 bg-white text-slate-900 font-semibold hover:bg-slate-50">7</button>
                  <button type="button" onClick={() => calculatorPress("8")} className="py-3 rounded-xl border border-slate-200 bg-white text-slate-900 font-semibold hover:bg-slate-50">8</button>
                  <button type="button" onClick={() => calculatorPress("9")} className="py-3 rounded-xl border border-slate-200 bg-white text-slate-900 font-semibold hover:bg-slate-50">9</button>
                  <button type="button" onClick={() => calculatorPress("*")} className="py-3 rounded-xl border border-slate-200 bg-blue-50 text-blue-600 font-semibold hover:bg-blue-100">&times;</button>
                  <button type="button" onClick={() => calculatorPress("4")} className="py-3 rounded-xl border border-slate-200 bg-white text-slate-900 font-semibold hover:bg-slate-50">4</button>
                  <button type="button" onClick={() => calculatorPress("5")} className="py-3 rounded-xl border border-slate-200 bg-white text-slate-900 font-semibold hover:bg-slate-50">5</button>
                  <button type="button" onClick={() => calculatorPress("6")} className="py-3 rounded-xl border border-slate-200 bg-white text-slate-900 font-semibold hover:bg-slate-50">6</button>
                  <button type="button" onClick={() => calculatorPress("-")} className="py-3 rounded-xl border border-slate-200 bg-blue-50 text-blue-600 font-semibold hover:bg-blue-100">&#8722;</button>
                  <button type="button" onClick={() => calculatorPress("1")} className="py-3 rounded-xl border border-slate-200 bg-white text-slate-900 font-semibold hover:bg-slate-50">1</button>
                  <button type="button" onClick={() => calculatorPress("2")} className="py-3 rounded-xl border border-slate-200 bg-white text-slate-900 font-semibold hover:bg-slate-50">2</button>
                  <button type="button" onClick={() => calculatorPress("3")} className="py-3 rounded-xl border border-slate-200 bg-white text-slate-900 font-semibold hover:bg-slate-50">3</button>
                  <button type="button" onClick={() => calculatorPress("+")} className="py-3 rounded-xl border border-slate-200 bg-blue-50 text-blue-600 font-semibold hover:bg-blue-100">+</button>
                  <button type="button" onClick={() => calculatorPress("0")} className="py-3 rounded-xl border border-slate-200 bg-white text-slate-900 font-semibold hover:bg-slate-50 col-span-2">0</button>
                  <button type="button" onClick={() => calculatorPress(".")} className="py-3 rounded-xl border border-slate-200 bg-white text-slate-900 font-semibold hover:bg-slate-50">.</button>
                  <button type="button" onClick={() => calculatorPress("=")} className="py-3 rounded-xl border border-slate-200 bg-blue-600 text-white font-semibold hover:bg-blue-700">=</button>
                  <button type="button" onClick={() => calculatorPress("backspace")} className="py-3 rounded-xl border border-slate-200 bg-slate-100 text-slate-700 font-semibold hover:bg-slate-200 col-span-4" aria-label="Delete last calculator digit">⌫ Backspace</button>
                </div>

                <p className="mt-4 text-xs text-slate-400 text-center">Choose an operator, enter the next number, then press =. You can use the buttons or keyboard. Press Esc to close.</p>
              </div>
            </div>
          )}

          {/* SIDEBAR */}

          <aside className="lg:sticky lg:top-[92px] lg:self-start space-y-4">
            {/* TIMER */}

            <div
              className={[
                "rounded-2xl border p-5 shadow-sm",
                timerCritical
                  ? "bg-red-50 border-red-200"
                  : timerWarning
                  ? "bg-amber-50 border-amber-200"
                  : "bg-white border-slate-200",
              ].join(" ")}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Time Remaining
                  </p>

                  <p
                    className={[
                      "mt-1 text-3xl font-bold tabular-nums",
                      timerCritical
                        ? "text-red-700"
                        : timerWarning
                        ? "text-amber-700"
                        : "text-slate-900",
                    ].join(" ")}
                  >
                    {formattedTime}
                  </p>
                </div>

                <div
                  className={[
                    "w-12 h-12 rounded-xl flex items-center justify-center text-xl",
                    timerCritical
                      ? "bg-red-100"
                      : timerWarning
                      ? "bg-amber-100"
                      : "bg-blue-50",
                  ].join(" ")}
                >
                  ⏱
                </div>
              </div>

              {timerCritical && (
                <p className="mt-4 text-xs font-semibold text-red-600">
                  Time is almost over.
                  Your test will submit
                  automatically.
                </p>
              )}
            </div>

            {/* QUESTION PALETTE */}

            <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="font-bold text-slate-900">
                    Questions
                  </h2>

                  <p className="text-xs text-slate-400 mt-1">
                    Select a question
                  </p>
                </div>

                <div className="text-xs font-semibold text-slate-500">
                  {answeredCount}/
                  {questions.length}
                </div>
              </div>

              {/* LEGEND */}

              <div className="mt-4 flex flex-wrap gap-x-3 gap-y-2 text-[10px] text-slate-500">
                <span className="flex items-center gap-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-green-500" />
                  Answered
                </span>

                <span className="flex items-center gap-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-red-500" />
                  Visited
                </span>

                <span className="flex items-center gap-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-amber-400" />
                  Marked
                </span>

                <span className="flex items-center gap-1">
                  <span className="w-2.5 h-2.5 rounded-full bg-slate-200" />
                  Not visited
                </span>
              </div>

              {/* QUESTION NUMBERS */}

              <div className="mt-5 grid grid-cols-5 gap-2">
                {questions.map(
                  (
                    question,
                    index
                  ) => {
                    const isAnswered =
                      answers[
                        question.id
                      ] !==
                      undefined;

                    const isMarked =
                      marked[
                        question.id
                      ];

                    const isVisited =
                      visited[
                        question.id
                      ];

                    const isCurrent =
                      index ===
                      currentQuestion;

                    return (
                      <button
                        type="button"
                        key={
                          question.id
                        }
                        onClick={() =>
                          setCurrentQuestion(
                            index
                          )
                        }
                        className={[
                          "relative h-10 rounded-lg text-xs font-bold border transition-all",

                          isCurrent
                            ? "ring-2 ring-blue-500 ring-offset-1"
                            : "",

                          isAnswered
                            ? "bg-green-50 border-green-300 text-green-700"
                            : isMarked
                            ? "bg-amber-50 border-amber-300 text-amber-700"
                            : isVisited
                            ? "bg-red-50 border-red-300 text-red-700"
                            : "bg-slate-50 border-slate-200 text-slate-500 hover:bg-slate-100",
                        ].join(" ")}
                      >
                        {index + 1}

                        {isMarked && (
                          <span className="absolute -top-1 -right-1 w-3 h-3 rounded-full bg-amber-400 border-2 border-white" />
                        )}
                      </button>
                    );
                  }
                )}
              </div>

              {/* DOWNLOAD */}



              {/* SUBMIT */}

              <button
                type="button"
                onClick={() =>
                  submitTest(
                    false
                  )
                }
                disabled={
                  submitting
                }
                className="mt-3 w-full h-11 rounded-xl bg-blue-600 text-white text-sm font-semibold hover:bg-blue-700 transition disabled:opacity-60"
              >
                {submitting
                  ? "Submitting..."
                  : "Submit Test"}
              </button>

              <p className="mt-3 text-[10px] leading-4 text-slate-400 text-center">
                Leaving this test tab
                will automatically
                submit your test.
              </p>
            </div>
          </aside>
        </div>
      </div>

      {showLeaveWarning && (
        <div className="fixed inset-0 z-[100] bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-5">
          <div role="alertdialog" aria-modal="true" className="w-full max-w-md rounded-3xl bg-white p-7 text-center shadow-2xl">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-amber-100 text-amber-700 text-2xl">!</div>
            <h2 className="mt-4 text-xl font-bold text-slate-900">Stay on the test window</h2>
            <p className="mt-3 text-sm leading-6 text-slate-600">
              You left the test window. This is your one warning. Leaving the test window again will automatically submit your test.
            </p>
            <button
              type="button"
              onClick={() => setShowLeaveWarning(false)}
              className="mt-6 w-full rounded-xl bg-blue-600 px-5 py-3 text-sm font-bold text-white hover:bg-blue-700"
            >
              Return to test
            </button>
          </div>
        </div>
      )}

      {/* =====================================================
          AUTO SUBMISSION WARNING
          ===================================================== */}

      {showWarning && (
        <div className="fixed inset-0 z-[100] bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-5">
          <div className="w-full max-w-md bg-white rounded-3xl shadow-2xl p-7 text-center">
            <div className="w-16 h-16 mx-auto rounded-2xl bg-red-50 text-red-600 flex items-center justify-center text-3xl">

            </div>

            <h2 className="mt-5 text-xl font-bold text-slate-900">
              Test Automatically Submitted
            </h2>

            <p className="mt-3 text-sm leading-6 text-slate-500">
              You left the test
              window. For exam
              security, your test has
              been automatically
              submitted.
            </p>

            <div className="mt-5 rounded-xl bg-amber-50 border border-amber-100 p-4 text-left">
              <p className="text-xs font-bold text-amber-800">
                Exam Security Warning
              </p>

              <p className="mt-1 text-xs leading-5 text-amber-700">
                Switching tabs or
                leaving the test window
                is treated as a test
                violation.
              </p>
            </div>

            <div className="mt-5 text-xs text-slate-400">
              Preparing your result...
            </div>
          </div>
        </div>
      )}

      {/* SUBMITTING OVERLAY */}

      {submitting &&
        !showWarning && (
          <div className="fixed inset-0 z-[90] bg-slate-950/40 backdrop-blur-sm flex items-center justify-center p-5">
            <div className="bg-white rounded-2xl shadow-xl px-8 py-7 text-center">
              <div className="w-10 h-10 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin mx-auto" />

              <h2 className="mt-4 font-bold text-slate-900">
                Submitting your test
              </h2>

              <p className="mt-1 text-xs text-slate-500">
                Calculating your result...
              </p>
            </div>
          </div>
        )}
    </main>
  );
}
