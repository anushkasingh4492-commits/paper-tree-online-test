"use client";

import {
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { useRouter } from "next/navigation";

/* ============================================================
   TYPES
============================================================ */

type TestResult = {
  id: string;
  attemptId?: string;
  difficulty?: string;
  name: string;
  score: number;
  accuracy: number;
  correct?: number;
  wrong?: number;
  unanswered?: number;
  attempted?: number;
  totalQuestions?: number;
  time: string;
  date: string;
  subject?: string;
  chapter?: string;
  exam?: string;
  status?: string;
};

type SubjectPerformance = {
  subject: string;
  score: number;
  accuracy: number;
  total: number;
  attempted: number;
  correct: number;
  wrong: number;
  unanswered: number;
};

type WeakArea = {
  topic: string;
  chapter: string;
  subject: string;
  score: number;
  accuracy: number;
  attempted: number;
  correct: number;
  wrong: number;
  unanswered: number;
};

type ScheduledTestItem = {
  id?: string;
  scheduledTestId?: string;
  paperId?: string | null;
  batchId?: string | null;
  name?: string;
  title?: string;
  exam?: string;
  description?: string;
  status?: string;
  startTime?: string;
  endTime?: string;
  startAt?: string | null;
  endAt?: string | null;
  startTimestamp?: number | null;
  endTimestamp?: number | null;
  duration?: string;
  durationMinutes?: number;
  questionCount?: number;
  questions?: number;
};

type DashboardPayload = {
  error?: string;
  success?: boolean;

  student?: {
    id?: string;
    name?: string;
    rollNumber?: string | null;
    email?: string | null;
  };

  statistics?: {
    testsTaken?: number;
    averageScore?: number;
    bestScore?: number;
    lowestScore?: number;
    attempts?: number;
    totalAttempts?: number;
    totalQuestions?: number;
    totalAttempted?: number;
    totalCorrect?: number;
    totalWrong?: number;
    totalUnanswered?: number;
    accuracy?: number;
    overallAccuracy?: number;
    studyTimeMinutes?: number;
    studyTime?: string;
    consistency?: number;
  };

  performanceTrend?: Array<{
    attemptId: string;
    testId: string;
    score: number;
    date?: string;
    formattedDate?: string;
    label?: string;
  }>;

  scoreDistribution?: {
    above90?: number;
    between70and89?: number;
    between50and69?: number;
    below50?: number;
  };

  subjectPerformance?: SubjectPerformance[];

  chapterPerformance?: Array<{
    subject: string;
    chapter: string;
    total: number;
    attempted: number;
    correct: number;
    wrong: number;
    unanswered: number;
    accuracy: number;
  }>;

  weakAreas?: WeakArea[];

  results?: TestResult[];

  myTests?: Array<{
    id: string;
    attemptId: string;
    difficulty?: string;
    name?: string;
    exam?: string;
    questionCount?: number;
    status?: string;
    score?: number | null;
    correct?: number;
    wrong?: number;
    unanswered?: number;
    duration?: string;
    durationMinutes?: number;
    startedAt?: string | null;
    submittedAt?: string | null;
  }>;

  testSummary?: {
    all?: ScheduledTestItem[];
    active?: ScheduledTestItem[];
    upcoming?: ScheduledTestItem[];
    completed?: ScheduledTestItem[];
    missed?: ScheduledTestItem[];

    counts?: {
      active?: number;
      upcoming?: number;
      completed?: number;
      missed?: number;
      total?: number;
    };
  };

  latestTest?: TestResult | null;
};

type IconType =
  | "home"
  | "tests"
  | "trend"
  | "chart"
  | "bookmark"
  | "target"
  | "user"
  | "settings"
  | "logout"
  | "bell"
  | "calendar";

/* ============================================================
   ICONS
============================================================ */

function MiniIcon({
  type,
  size = 20,
}: {
  type: IconType;
  size?: number;
}) {
  const paths: Record<
    IconType,
    React.ReactNode
  > = {
    home: (
      <>
        <path d="m3 9 6-5 6 5" />
        <path d="M5 8v7h8V8" />
        <path d="M8 15v-4h2v4" />
      </>
    ),

    tests: (
      <>
        <rect
          x="4"
          y="3"
          width="8"
          height="12"
          rx="1.5"
        />
        <path d="M6.5 7h3" />
        <path d="M6.5 10h3" />
        <path d="M6.5 13h2" />
      </>
    ),

    trend: (
      <>
        <path d="M3 13l3-3 3 2 5-6" />
        <path d="M11 6h3v3" />
      </>
    ),

    chart: (
      <>
        <path d="M4 14V9M8 14V6M12 14V4" />
        <path d="M3 15h10" />
      </>
    ),

    bookmark: (
      <path d="M5 3h6a1 1 0 0 1 1 1v11l-4-2.5L4 15V4a1 1 0 0 1 1-1Z" />
    ),

    target: (
      <>
        <circle
          cx="8"
          cy="8"
          r="5.5"
        />
        <circle
          cx="8"
          cy="8"
          r="2.3"
        />
        <path d="m12 4 2-2M13 2h1v1" />
      </>
    ),

    user: (
      <>
        <circle
          cx="8"
          cy="5"
          r="2.3"
        />
        <path d="M3.5 14c.7-2.4 2.2-3.6 4.5-3.6s3.8 1.2 4.5 3.6" />
      </>
    ),

    settings: (
      <>
        <circle
          cx="8"
          cy="8"
          r="2.3"
        />
        <path d="m8 2 .6 1.4 1.5.6 1.5-.4.9.9-.4 1.5.6 1.5L14 8l-1.4.6-.6 1.5.4 1.5-.9.9-1.5-.4-1.5.6L8 14l-.6-1.4-1.5-.6-1.5.4-.9-.9.4-1.5L3.3 8 4.7 7.4l.6-1.5-.4-1.5.9-.9 1.5.4L8 2Z" />
      </>
    ),

    logout: (
      <>
        <path d="M6 3H4.5A1.5 1.5 0 0 0 3 4.5v7A1.5 1.5 0 0 0 4.5 13H6" />
        <path d="M8 5l3 3-3 3" />
        <path d="M11 8H5" />
      </>
    ),

    bell: (
      <>
        <path d="M4 11h8l-1-1V7a3 3 0 0 0-6 0v3l-1 1Z" />
        <path d="M6.5 13h3" />
      </>
    ),

    calendar: (
      <>
        <rect
          x="3"
          y="4"
          width="10"
          height="9"
          rx="1.5"
        />
        <path d="M5 2v3" />
        <path d="M11 2v3" />
        <path d="M3 7h10" />
      </>
    ),
  };

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 18 18"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {paths[type]}
    </svg>
  );
}

/* ============================================================
   HELPERS
============================================================ */

function initials(name: string) {
  const parts = name
    .trim()
    .split(/\s+/)
    .filter(Boolean);

  if (!parts.length) {
    return "S";
  }

  if (parts.length === 1) {
    return parts[0][0].toUpperCase();
  }

  return `${parts[0][0]}${
    parts[parts.length - 1][0]
  }`.toUpperCase();
}

function scoreTone(score: number) {
  if (score >= 80) {
    return "text-emerald-600";
  }

  if (score >= 60) {
    return "text-blue-600";
  }

  if (score >= 50) {
    return "text-amber-500";
  }

  return "text-rose-500";
}

function subjectConfig(
  subject: string
) {
  const normalized =
    subject.toLowerCase();

  if (normalized === "physics") {
    return {
      bar: "bg-blue-500",
      text: "text-blue-600",
      iconBg: "bg-blue-50",
      icon: "",
    };
  }

  if (normalized === "chemistry") {
    return {
      bar: "bg-emerald-500",
      text: "text-emerald-600",
      iconBg: "bg-emerald-50",
      icon: "",
    };
  }

  if (
    normalized ===
      "mathematics" ||
    normalized === "maths"
  ) {
    return {
      bar: "bg-pink-500",
      text: "text-pink-600",
      iconBg: "bg-pink-50",
      icon: "∑",
    };
  }

  return {
    bar: "bg-violet-500",
    text: "text-violet-600",
    iconBg: "bg-violet-50",
    icon: "B",
  };
}

/* ============================================================
   PERFORMANCE CHART
============================================================ */

function PerformanceChart({
  results,
}: {
  results: TestResult[];
}) {
  const w = 760;
  const h = 210;
  const padX = 28;
  const padTop = 18;
  const padBottom = 28;

  const innerW =
    w - padX * 2;

  const innerH =
    h -
    padTop -
    padBottom;

  const points = results.map(
    (r, i) => {
      const x =
        padX +
        (i * innerW) /
          Math.max(
            results.length - 1,
            1
          );

      const y =
        padTop +
        innerH -
        (Math.max(
          0,
          Math.min(
            100,
            r.score
          )
        ) /
          100) *
          innerH;

      return {
        x,
        y,
        score: r.score,
        date: r.date,
      };
    }
  );

  const line = points
    .map(
      (p, i) =>
        `${i ? "L" : "M"} ${
          p.x
        } ${p.y}`
    )
    .join(" ");

  const area =
    points.length > 0
      ? `${line} L ${
          points[
            points.length - 1
          ].x
        } ${
          h - padBottom
        } L ${points[0].x} ${
          h - padBottom
        } Z`
      : "";

  return (
    <div className="mt-5 overflow-hidden">
      {points.length === 0 ? (
        <div className="h-[225px] flex items-center justify-center text-xs text-[#9aa1ae]">
          Complete a test to see your
          performance trend.
        </div>
      ) : (
        <svg
          viewBox={`0 0 ${w} ${h}`}
          className="w-full h-[225px]"
          preserveAspectRatio="none"
        >
          {[
            0,
            25,
            50,
            75,
            100,
          ].map((v) => {
            const y =
              padTop +
              innerH -
              (v / 100) *
                innerH;

            return (
              <g key={v}>
                <line
                  x1={padX}
                  x2={w - padX}
                  y1={y}
                  y2={y}
                  stroke="#edf0f5"
                  strokeWidth="1"
                />

                <text
                  x="0"
                  y={y + 4}
                  fontSize="10"
                  fill="#a3a9b5"
                >
                  {v}%
                </text>
              </g>
            );
          })}

          {points.length >
            1 && (
            <path
              d={area}
              fill="url(#areaFill)"
            />
          )}

          {points.length >
            1 && (
            <path
              d={line}
              fill="none"
              stroke="#6246e5"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          )}

          {points.map(
            (p, i) => (
              <g key={i}>
                <text
                  x={p.x}
                  y={Math.max(
                    12,
                    p.y - 10
                  )}
                  textAnchor="middle"
                  fontSize="9.5"
                  fontWeight="700"
                  fill="#34394a"
                >
                  {p.score.toFixed(
                    1
                  )}
                  %
                </text>

                <circle
                  cx={p.x}
                  cy={p.y}
                  r="4"
                  fill="#6246e5"
                  stroke="white"
                  strokeWidth="2"
                />

                <text
                  x={p.x}
                  y={h - 7}
                  textAnchor="middle"
                  fontSize="8.5"
                  fill="#9aa1ae"
                >
                  {p.date}
                </text>
              </g>
            )
          )}

          <defs>
            <linearGradient
              id="areaFill"
              x1="0"
              y1="0"
              x2="0"
              y2="1"
            >
              <stop
                offset="0%"
                stopColor="#7658ef"
                stopOpacity=".20"
              />

              <stop
                offset="100%"
                stopColor="#7658ef"
                stopOpacity=".02"
              />
            </linearGradient>
          </defs>
        </svg>
      )}
    </div>
  );
}

/* ============================================================
   DONUT
============================================================ */

function Donut({
  results,
}: {
  results: TestResult[];
}) {
  const counts = [
    results.filter(
      (r) => r.score >= 90
    ).length,

    results.filter(
      (r) =>
        r.score >= 70 &&
        r.score < 90
    ).length,

    results.filter(
      (r) =>
        r.score >= 50 &&
        r.score < 70
    ).length,

    results.filter(
      (r) => r.score < 50
    ).length,
  ];

  const total =
    results.length;

  const colors = [
    "#20b77a",
    "#3b73e9",
    "#f5a900",
    "#ee4c72",
  ];

  let start = 0;

  const polar = (
    angle: number,
    radius: number
  ) => {
    const a =
      ((angle - 90) *
        Math.PI) /
      180;

    return [
      60 +
        radius *
          Math.cos(a),

      60 +
        radius *
          Math.sin(a),
    ];
  };

  const arc = (
    startAngle: number,
    endAngle: number,
    color: string
  ) => {
    if (
      endAngle -
        startAngle >=
      359.9
    ) {
      return (
        <circle
          cx="60"
          cy="60"
          r="40"
          fill="none"
          stroke={color}
          strokeWidth="15"
        />
      );
    }

    const [x1, y1] =
      polar(
        startAngle,
        40
      );

    const [x2, y2] =
      polar(
        endAngle,
        40
      );

    const large =
      endAngle -
        startAngle >
      180
        ? 1
        : 0;

    return (
      <path
        d={`M ${x1} ${y1} A 40 40 0 ${large} 1 ${x2} ${y2}`}
        fill="none"
        stroke={color}
        strokeWidth="15"
        strokeLinecap="butt"
      />
    );
  };

  if (!total) {
    return (
      <div className="flex items-center justify-center h-[150px]">
        <div className="text-center">
          <div className="text-[22px] font-extrabold text-[#202638]">
            0
          </div>

          <div className="text-[10px] text-[#9299a8]">
            Tests
          </div>
        </div>
      </div>
    );
  }

  const segments =
    counts.map(
      (count, i) => {
        const end =
          start +
          (count / total) *
            360;

        const result = {
          start,
          end,
          color: colors[i],
          count,
        };

        start = end;

        return result;
      }
    );

  return (
    <div className="flex items-center gap-6">
      <div className="relative w-[150px] h-[150px] shrink-0">
        <svg
          viewBox="0 0 120 120"
          className="w-full h-full"
        >
          <circle
            cx="60"
            cy="60"
            r="40"
            fill="none"
            stroke="#f0f2f7"
            strokeWidth="15"
          />

          {segments.map(
            (
              segment,
              i
            ) => (
              <g key={i}>
                {segment.count >
                  0 &&
                  arc(
                    segment.start,
                    segment.end,
                    segment.color
                  )}
              </g>
            )
          )}
        </svg>

        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-[20px] font-extrabold text-[#202638]">
            {total}
          </span>

          <span className="text-[10px] text-[#9299a8]">
            Tests
          </span>
        </div>
      </div>

      <div className="space-y-3 text-xs flex-1">
        {[
          [
            "90% and above",
            counts[0],
            colors[0],
          ],
          [
            "70% - 89%",
            counts[1],
            colors[1],
          ],
          [
            "50% - 69%",
            counts[2],
            colors[2],
          ],
          [
            "Below 50%",
            counts[3],
            colors[3],
          ],
        ].map(
          (
            [
              label,
              count,
              color,
            ],
            i
          ) => (
            <div
              className="flex items-center gap-2"
              key={i}
            >
              <span
                className="w-2 h-2 rounded-full"
                style={{
                  background:
                    color as string,
                }}
              />

              <span className="text-[#697184] flex-1">
                {label}
              </span>

              <span className="font-semibold text-[#6b7280]">
                {count} (
                {Math.round(
                  (Number(
                    count
                  ) /
                    total) *
                    100
                )}
                %)
              </span>
            </div>
          )
        )}
      </div>
    </div>
  );
}

/* ============================================================
   DASHBOARD
============================================================ */

export default function DashboardPage() {
  const router =
    useRouter();

  /*
   * Prevent multiple dashboard requests from
   * running at the same time.
   */
  const dashboardLoadingRef =
    useRef(false);

  const [
    studentName,
    setStudentName,
  ] = useState(
    "Student"
  );

  const [
    results,
    setResults,
  ] = useState<
    TestResult[]
  >([]);

  const [
    subjectPerformance,
    setSubjectPerformance,
  ] = useState<
    SubjectPerformance[]
  >([]);

  const [
    weakAreas,
    setWeakAreas,
  ] = useState<
    WeakArea[]
  >([]);

  const [
    statistics,
    setStatistics,
  ] =
    useState<
      DashboardPayload["statistics"]
    >({});

  const [
    performanceTrend,
    setPerformanceTrend,
  ] = useState<
    NonNullable<
      DashboardPayload["performanceTrend"]
    >
  >([]);

  const [
    scoreDistribution,
    setScoreDistribution,
  ] = useState<
    NonNullable<
      DashboardPayload["scoreDistribution"]
    >
  >({});

  const [
    upcomingTests,
    setUpcomingTests,
  ] = useState<
    ScheduledTestItem[]
  >([]);

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState("");

  /* ==========================================================
     LOAD REAL STUDENT DASHBOARD
  ========================================================== */

  useEffect(() => {
    let active = true;

    async function loadDashboard(
      showLoader = false
    ) {
      /*
       * Ignore duplicate focus / visibility /
       * interval requests while one request is
       * already running.
       */
      if (
        dashboardLoadingRef.current
      ) {
        return;
      }

      dashboardLoadingRef.current =
        true;

      try {
        if (
          showLoader &&
          active
        ) {
          setLoading(true);
        }

        if (active) {
          setError("");
        }

        const response =
          await fetch(
            "/api/dashboard",
            {
              method: "GET",
              cache: "no-store",
              credentials:
                "include",
            }
          );

        const data: DashboardPayload =
          await response.json();

        if (
          !response.ok ||
          data.success ===
            false
        ) {
          if (
            response.status ===
            401
          ) {
            router.replace(
              "/"
            );
            return;
          }

          throw new Error(
            data.error ||
              "Failed to load dashboard."
          );
        }

        if (!active) {
          return;
        }

        setStudentName(
          data.student?.name?.trim() ||
            "Student"
        );

        setResults(
          Array.isArray(
            data.results
          )
            ? data.results
            : []
        );

        setSubjectPerformance(
          Array.isArray(
            data.subjectPerformance
          )
            ? data.subjectPerformance
            : []
        );

        setWeakAreas(
          Array.isArray(
            data.weakAreas
          )
            ? data.weakAreas
            : []
        );

        setPerformanceTrend(
          Array.isArray(
            data.performanceTrend
          )
            ? data.performanceTrend
            : []
        );

        setScoreDistribution(
          data.scoreDistribution ||
            {}
        );

        setUpcomingTests(
          Array.isArray(
            data.testSummary
              ?.upcoming
          )
            ? data
                .testSummary!
                .upcoming!
            : []
        );

        setStatistics(
          data.statistics ||
            {}
        );
      } catch (err) {
        console.error(
          "Dashboard loading error:",
          err
        );

        if (active) {
          setError(
            err instanceof
              Error
              ? err.message
              : "Failed to load dashboard."
          );
        }
      }finally {
  dashboardLoadingRef.current = false;

  if (showLoader) {
    setLoading(false);
  }
}
    }

    /*
     * Initial page load.
     */
    void loadDashboard(
      true
    );

    /*
     * Background refreshes do NOT put the
     * entire page back into the loading screen.
     */
    const handleFocus =
      () => {
        void loadDashboard(
          false
        );
      };

    const handleVisibilityChange =
      () => {
        if (
          document
            .visibilityState ===
          "visible"
        ) {
          void loadDashboard(
            false
          );
        }
      };

    const handleStorage = (
      event: StorageEvent
    ) => {
      if (
        event.key ===
        "paperTreeDashboardRefresh"
      ) {
        void loadDashboard(
          false
        );
      }
    };

    window.addEventListener(
      "focus",
      handleFocus
    );

    document.addEventListener(
      "visibilitychange",
      handleVisibilityChange
    );

    window.addEventListener(
      "storage",
      handleStorage
    );

    /*
     * Keep auto-refresh, but once every minute
     * instead of every 15 seconds.
     */
    const refreshInterval =
      window.setInterval(
        () => {
          if (
            document
              .visibilityState ===
            "visible"
          ) {
            void loadDashboard(
              false
            );
          }
        },
        60000
      );

    return () => {
      active = false;

      window.removeEventListener(
        "focus",
        handleFocus
      );

      document.removeEventListener(
        "visibilitychange",
        handleVisibilityChange
      );

      window.removeEventListener(
        "storage",
        handleStorage
      );

      window.clearInterval(
        refreshInterval
      );
    };
  }, [router]);

  /* ==========================================================
     DERIVED DATA
  ========================================================== */

  const average =
    Number(
      statistics
        ?.averageScore ??
        0
    );

  const best =
    Number(
      statistics
        ?.bestScore ??
        0
    );

  const lowest =
    Number(
      statistics
        ?.lowestScore ??
        0
    );

  const testsTaken =
    Number(
      statistics
        ?.testsTaken ??
        results.length
    );

  const attempts =
    Number(
      statistics
        ?.totalAttempts ??
        statistics
          ?.attempts ??
        0
    );

  const studyTime =
    statistics?.studyTime ||
    "0m";

  const consistency =
    Number(
      statistics
        ?.consistency ??
        0
    );

  const initialsText =
    initials(
      studentName
    );

  const highestTest =
    results.length
      ? results.reduce(
          (
            bestResult,
            current
          ) =>
            current.score >
            bestResult.score
              ? current
              : bestResult
        )
      : null;

  const lowestTest =
    results.length
      ? results.reduce(
          (
            lowestResult,
            current
          ) =>
            current.score <
            lowestResult.score
              ? current
              : lowestResult
        )
      : null;

  const trendResults =
    useMemo(() => {
      if (
        performanceTrend.length ===
        0
      ) {
        return results;
      }

      return performanceTrend.map(
        (item) => ({
          id: item.testId,

          name:
            item.label ||
            "Test",

          score:
            Number(
              item.score ||
                0
            ),

          accuracy:
            Number(
              item.score ||
                0
            ),

          time: "",

          date:
            item.formattedDate ||
            "",
        })
      );
    }, [
      performanceTrend,
      results,
    ]);

  const subjectRows =
    subjectPerformance.length
      ? subjectPerformance
      : [
          "Physics",
          "Chemistry",
          "Mathematics",
          "Biology",
        ].map(
          (subject) => ({
            subject,
            score: 0,
            accuracy: 0,
            total: 0,
            attempted: 0,
            correct: 0,
            wrong: 0,
            unanswered: 0,
          })
        );

  /* ==========================================================
     LOGOUT
  ========================================================== */

  function logout() {
    localStorage.removeItem(
      "studentName"
    );

    localStorage.removeItem(
      "username"
    );

    document.cookie =
      "student_session=; Max-Age=0; path=/";

    router.push("/");
  }

  /* ==========================================================
     LOADING
  ========================================================== */

  if (loading) {
    return (
      <main className="min-h-screen bg-[#f8f9fc] flex items-center justify-center">
        <div className="text-center">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#2563eb] to-[#6338e5] text-white flex items-center justify-center font-black text-lg mx-auto animate-pulse">
            P
          </div>

          <p className="mt-4 text-sm font-semibold text-[#4e596c]">
            Loading your
            dashboard...
          </p>

          <p className="mt-1 text-xs text-[#9aa1ae]">
            Preparing your
            personal performance
            data
          </p>
        </div>
      </main>
    );

  }

  /* ==========================================================
     ERROR
  ========================================================== */

  if (error) {
    return (
      <main className="min-h-screen bg-[#f8f9fc] flex items-center justify-center px-5">
        <div className="bg-white border border-[#e8eaf0] rounded-2xl p-7 max-w-md w-full text-center shadow-sm">
          <div className="w-12 h-12 rounded-full bg-rose-50 text-rose-500 flex items-center justify-center mx-auto text-xl">
            !
          </div>

          <h1 className="mt-4 text-lg font-extrabold text-[#202638]">
            Unable to load
            dashboard
          </h1>

          <p className="mt-2 text-xs text-[#858c9b]">
            {error}
          </p>

          <button
            onClick={() =>
              window.location.reload()
            }
            className="mt-5 h-9 px-5 rounded-lg bg-[#6246e5] text-white text-xs font-bold"
          >
            Try Again
          </button>
        </div>
      </main>
    );
  }

  /* ============================================================
     MAIN
  ============================================================ */

  return (
    <main className="min-h-screen bg-[#f8f9fc] text-[#1d2435]">

      <div className="flex min-h-screen">

        {/* =====================================================
            SIDEBAR
        ====================================================== */}

        <aside className="hidden xl:flex w-[220px] shrink-0 bg-white border-r border-[#e9ebf1] flex-col">

          <div className="h-[82px] px-5 flex items-center gap-3 border-b border-[#f0f1f5]">
            <div className="w-9 h-9 rounded-[11px] bg-gradient-to-br from-[#2563eb] to-[#6338e5] text-white flex items-center justify-center font-black text-lg shadow-sm">
              P
            </div>

            <div>
              <div className="font-extrabold text-[15px] leading-4">
                Paper Tree
              </div>

              <div className="text-[9px] font-semibold tracking-[.17em] text-[#9ba1ad] mt-1">
                ONLINE TEST
              </div>
            </div>
          </div>

          <div className="px-4 pt-5 flex-1">
            <p className="px-2 mb-2 text-[9px] uppercase tracking-[.16em] font-bold text-[#a1a7b3]">
              Workspace
            </p>

            <nav className="space-y-1">

              <button
                onClick={() =>
                  router.push(
                    "/dashboard"
                  )
                }
                className="w-full h-10 flex items-center gap-3 px-2.5 rounded-xl bg-[#f0efff] text-[#5640db] text-xs font-bold"
              >
                <span className="w-7 h-7 rounded-lg bg-white flex items-center justify-center">
                  <MiniIcon type="home" />
                </span>

                Dashboard
              </button>

              <button
                onClick={() =>
                  router.push(
                    "/tests"
                  )
                }
                className="w-full h-10 flex items-center gap-3 px-2.5 rounded-xl text-[#657083] hover:bg-[#f7f8fb] text-xs font-medium"
              >
                <span className="w-7 h-7 rounded-lg bg-[#f5f6f9] flex items-center justify-center">
                  <MiniIcon type="tests" />
                </span>

                My Tests
              </button>

              <button
                onClick={() =>
                  router.push(
                    "/test-summary"
                  )
                }
                className="w-full h-10 flex items-center gap-3 px-2.5 rounded-xl text-[#657083] hover:bg-[#f7f8fb] text-xs font-medium"
              >
                <span className="w-7 h-7 rounded-lg bg-[#f5f6f9] flex items-center justify-center">
                  <MiniIcon type="calendar" />
                </span>

                Test Summary
              </button>

            </nav>
          </div>

          <div className="px-4 pb-3">
            <div className="rounded-xl bg-gradient-to-br from-[#fff8e9] via-[#fff4fb] to-[#f2edff] border border-[#eee8ff] p-3.5">
              <div className="flex items-center gap-2 text-[#7357dc]">
                <span className="w-7 h-7 rounded-lg bg-white flex items-center justify-center">

                </span>

                <span className="text-xs font-extrabold">
                  Go Premium
                </span>
              </div>

              <p className="text-[9px] text-[#818898] leading-4 mt-2">
                Unlock unlimited
                tests, detailed
                analytics and more.
              </p>

              <button className="mt-2.5 w-full h-8 rounded-lg bg-gradient-to-r from-[#6744e8] to-[#7d31e8] text-white text-[10px] font-bold">
                Upgrade Now
              </button>
            </div>
          </div>

          <button
            className="mx-5 mb-5 mt-1 flex items-center gap-3 h-9 text-xs text-[#657083]"
            onClick={logout}
          >
            <MiniIcon type="logout" />
            Logout
          </button>

        </aside>

        {/* =====================================================
            MAIN CONTENT
        ====================================================== */}

        <div className="flex-1 min-w-0">

          {/* Header */}

          <header className="h-[82px] bg-white border-b border-[#e9ebf1] px-5 lg:px-8 flex items-center justify-between">

            <div>
              <h1 className="text-[20px] font-extrabold tracking-tight">
                Welcome back,{" "}
                <span className="text-[#315fea]">
                  {studentName}
                </span>{" "}
                <span className="text-[18px]">

                </span>
              </h1>

              <p className="mt-1 text-[11px] text-[#858c9b]">
                Here's your
                performance overview
                and test insights
              </p>
            </div>

            <div className="flex items-center gap-2.5">

              <button className="hidden sm:flex items-center gap-2 px-3.5 h-9 rounded-xl border border-[#e8eaf1] bg-white text-[11px] font-semibold text-[#33405a] shadow-[0_2px_8px_rgba(30,35,60,.03)]">
                <span className="text-[#6544e8]">
                  <MiniIcon
                    type="calendar"
                    size={15}
                  />
                </span>

                MHT-CET · 2026

                <span className="text-[#9da4b1]">
                  ⌄
                </span>
              </button>

              <button className="relative w-9 h-9 rounded-xl border border-[#eceef3] bg-white flex items-center justify-center text-[#596275]">
                <MiniIcon
                  type="bell"
                  size={17}
                />

                <span className="absolute -right-1 -top-1 w-4 h-4 rounded-full bg-[#ed4567] text-white text-[8px] font-bold flex items-center justify-center">
                  3
                </span>
              </button>

              <div className="w-9 h-9 rounded-full bg-gradient-to-br from-[#6944e8] to-[#4f2bd5] text-white flex items-center justify-center text-sm font-bold">
                {initialsText[0]}
              </div>

            </div>
          </header>

          {/* Dashboard body */}

          <div className="p-5 lg:p-6 xl:p-7 max-w-[1500px] mx-auto pb-24 xl:pb-7">

            {/* =================================================
                HERO
            ================================================== */}

            <section className="relative overflow-hidden rounded-[16px] min-h-[198px] bg-gradient-to-r from-[#2460ef] via-[#4b3fe8] to-[#8735ee] text-white px-7 py-6 shadow-[0_8px_24px_rgba(83,65,220,.14)]">

              <div className="absolute -right-16 -top-20 w-56 h-56 rounded-full bg-white/[.07]" />

              <div className="absolute right-10 -bottom-36 w-80 h-80 rounded-full bg-white/[.07]" />

              <div className="absolute right-[34%] -top-20 w-28 h-28 rounded-full bg-white/[.05]" />

              <div className="relative max-w-[53%]">

                <div className="flex items-center gap-2 text-[11px] font-semibold">
                  <span className="w-2 h-2 rounded-full bg-[#28d48a]" />

                  MHT-CET Preparation
                </div>

                <h2 className="mt-4 text-[24px] lg:text-[26px] font-extrabold tracking-tight">
                  Keep pushing
                  forward,{" "}
                  {studentName}!
                </h2>

                <p className="mt-1.5 text-[12px] text-white/85">
                  Consistency today
                  leads to success
                  tomorrow.
                </p>

                <button
                  onClick={() =>
                    router.push(
                      "/tests"
                    )
                  }
                  className="mt-5 h-9 px-4 rounded-lg bg-white text-[#2f58e8] text-[11px] font-bold shadow-sm"
                >
                  Start New Test
                  <span className="ml-2">
                    →
                  </span>
                </button>
              </div>

              {/* Illustration */}

              <div className="hidden md:flex absolute right-[23%] bottom-0 w-[245px] h-[145px] items-end">

                <div className="absolute left-0 bottom-5 w-[235px] h-4 rounded-full bg-[#58a8f3]/70 shadow-lg" />

                <div className="absolute left-8 bottom-9 w-10 h-9 rounded-sm bg-[#e9f1ff] border-4 border-[#3b5878] rotate-[-2deg]" />

                <div className="absolute left-15 bottom-9 w-28 h-5 rounded-sm bg-[#f0c6c6] border border-[#34465e]" />

                <div className="absolute left-[115px] bottom-9 w-[105px] h-[82px] rounded-md bg-[#dce7f9] border-[6px] border-[#283951] rotate-[2deg]">
                  <div className="m-3 space-y-2">
                    {[1, 2, 3].map(
                      (item) => (
                        <div
                          className="flex gap-2"
                          key={item}
                        >
                          <span className="text-[#26bd84]">

                          </span>

                          <span className="h-1.5 bg-white rounded w-14 mt-1.5" />
                        </div>
                      )
                    )}
                  </div>
                </div>

                <div className="absolute right-0 bottom-[91px] w-2 h-12 bg-[#26334a] rotate-[22deg]" />

                <div className="absolute right-[-5px] bottom-[101px] w-7 h-5 rounded-full bg-[#17263b] rotate-[22deg]" />

                <div className="absolute left-[55px] bottom-10 w-7 h-12 rounded-b-xl bg-[#6ac16c]" />

                <div className="absolute left-[51px] bottom-[57px] w-8 h-8 rounded-full bg-[#84d777]" />

              </div>

              <div className="hidden lg:block absolute right-7 top-8 w-[210px] text-right">

                <div className="text-4xl font-serif leading-none text-white/45">
                  “
                </div>

                <p className="text-[12px] leading-5 font-medium">
                  Success is the sum
                  of
                  <br />
                  small efforts
                  repeated
                  <br />
                  day in and day out.
                </p>

                <p className="mt-2 text-[10px] font-semibold text-white/80">
                  — Robert Collier
                </p>

              </div>
            </section>

            {/* =================================================
                STATS
            ================================================== */}

            <section className="grid grid-cols-2 xl:grid-cols-5 gap-4 mt-5">

              {[
                [
                  "Tests Taken",
                  String(
                    testsTaken
                  ),
                  `${
                    statistics
                      ?.totalQuestions ??
                    0
                  } questions analyzed`,
                  "bg-blue-50 text-blue-600",
                  "▣",
                ],

                [
                  "Average Score",
                  `${average.toFixed(
                    1
                  )}%`,
                  `${
                    statistics
                      ?.overallAccuracy ??
                    statistics
                      ?.accuracy ??
                    0
                  }% answer accuracy`,
                  "bg-pink-50 text-pink-600",
                  "▥",
                ],

                [
                  "Best Score",
                  `${best.toFixed(
                    1
                  )}%`,
                  highestTest
                    ?.date ||
                    "Highest completed score",
                  "bg-emerald-50 text-emerald-600",
                  "",
                ],

                [
                  "Attempts",
                  String(
                    attempts
                  ),
                  `${
                    statistics
                      ?.totalCorrect ??
                    0
                  } correct answers`,
                  "bg-violet-50 text-violet-600",
                  "↗",
                ],

                [
                  "Assesment Time",
                  studyTime,
                  `${
                    statistics
                      ?.totalAttempted ??
                    0
                  } questions attempted`,
                  "bg-orange-50 text-orange-500",
                  "◷",
                ],
              ].map(
                ([
                  label,
                  value,
                  sub,
                  iconBg,
                  icon,
                ]) => (
                  <div
                    key={label}
                    className="bg-white rounded-[14px] border border-[#e8eaf0] px-4 py-4 shadow-[0_3px_12px_rgba(30,35,60,.035)]"
                  >
                    <div className="flex justify-between gap-2">

                      <div className="min-w-0">
                        <p className="text-[10px] font-semibold text-[#858c9b]">
                          {label}
                        </p>

                        <p className="mt-2 text-[22px] font-extrabold text-[#202638]">
                          {value}
                        </p>

                        <p className="mt-1 text-[9px] text-[#858c9b] truncate">
                          {sub}
                        </p>
                      </div>

                      <span
                        className={`w-10 h-10 rounded-full ${iconBg} flex items-center justify-center text-base font-bold shrink-0`}
                      >
                        {icon}
                      </span>

                    </div>
                  </div>
                )
              )}

            </section>

            {/* =================================================
                PERFORMANCE + SCORE DISTRIBUTION
            ================================================== */}

            <section className="grid grid-cols-1 xl:grid-cols-[1.55fr_1fr] gap-5 mt-5">

              {/* Performance */}

              <div className="bg-white rounded-[14px] border border-[#e8eaf0] p-5 shadow-[0_3px_12px_rgba(30,35,60,.035)]">

                <div className="flex items-start justify-between">

                  <div>
                    <h2 className="text-[14px] font-extrabold">
                      Performance
                      Trend
                    </h2>

                    <p className="mt-1 text-[10px] text-[#939aa8]">
                      Your actual
                      score across
                      completed tests
                    </p>
                  </div>

                  <div className="h-8 px-3 rounded-lg border border-[#e7e9f0] text-[10px] font-semibold text-[#4e596c] flex items-center">
                    All Completed
                    Tests
                  </div>

                </div>

                <PerformanceChart
                  results={
                    trendResults
                  }
                />

                <div className="grid grid-cols-3 gap-3 mt-2">

                  <div className="rounded-xl border border-[#e9e2ff] bg-[#faf8ff] p-3">

                    <div className="flex items-center gap-2">

                      <span className="w-8 h-8 rounded-lg bg-[#eee7ff] text-[#7047e7] flex items-center justify-center">

                      </span>

                      <div>
                        <p className="text-[9px] text-[#7d8493]">
                          Highest Score
                        </p>

                        <p className="text-[17px] font-extrabold">
                          {best.toFixed(
                            1
                          )}
                          %
                        </p>

                        <p className="text-[8px] text-[#9aa0ad]">
                          {highestTest
                            ?.date ||
                            "—"}
                        </p>
                      </div>

                    </div>
                  </div>

                  <div className="rounded-xl border border-[#ffe5eb] bg-[#fff9fa] p-3">

                    <div className="flex items-center gap-2">

                      <span className="w-8 h-8 rounded-lg bg-[#ffeaf0] text-[#ec4f73] flex items-center justify-center">
                        ↘
                      </span>

                      <div>
                        <p className="text-[9px] text-[#7d8493]">
                          Lowest Score
                        </p>

                        <p className="text-[17px] font-extrabold">
                          {lowest.toFixed(
                            1
                          )}
                          %
                        </p>

                        <p className="text-[8px] text-[#9aa0ad]">
                          {lowestTest
                            ?.date ||
                            "—"}
                        </p>
                      </div>

                    </div>
                  </div>

                  <div className="rounded-xl border border-[#e4efff] bg-[#f8fbff] p-3">

                    <div className="flex items-center gap-2">

                      <span className="w-8 h-8 rounded-lg bg-[#eaf3ff] text-[#3673e9] flex items-center justify-center">
                        ⌁
                      </span>

                      <div>
                        <p className="text-[9px] text-[#7d8493]">
                          Consistency
                        </p>

                        <p className="text-[17px] font-extrabold">
                          {consistency}%
                        </p>

                        <p className="text-[8px] text-[#9aa0ad]">
                          {consistency >=
                          80
                            ? "Excellent"
                            : consistency >=
                                60
                              ? "Good"
                              : "Needs improvement"}
                        </p>
                      </div>

                    </div>
                  </div>

                </div>
              </div>

              {/* Right column */}

              <div className="space-y-5">

                {/* Score Distribution */}

                <div className="bg-white rounded-[14px] border border-[#e8eaf0] p-5 shadow-[0_3px_12px_rgba(30,35,60,.035)]">

                  <h2 className="text-[14px] font-extrabold">
                    Score
                    Distribution
                  </h2>

                  <p className="mt-1 text-[10px] text-[#939aa8]">
                    Based on your{" "}
                    {results.length}{" "}
                    completed tests
                  </p>

                  <div className="mt-4">
                    <Donut
                      results={
                        results
                      }
                    />
                  </div>

                </div>

                {/* Subject Performance */}

                <div className="bg-white rounded-[14px] border border-[#e8eaf0] p-5 shadow-[0_3px_12px_rgba(30,35,60,.035)]">

                  <h2 className="text-[14px] font-extrabold">
                    Subject
                    Performance
                  </h2>

                  <p className="mt-1 text-[10px] text-[#939aa8]">
                    Based on this
                    student's actual
                    answers
                  </p>

                  <div className="mt-5 space-y-4">

                    {subjectRows.map(
                      (item) => {
                        const c =
                          subjectConfig(
                            item.subject
                          );

                        return (
                          <button
                            key={
                              item.subject
                            }
                            className="w-full flex items-center gap-2.5 text-left"
                          >
                            <span
                              className={`w-6 h-6 rounded-md ${c.iconBg} ${c.text} flex items-center justify-center text-[11px] font-bold`}
                            >
                              {c.icon}
                            </span>

                            <span className="w-[68px] text-[10px] font-semibold text-[#4e596c]">
                              {
                                item.subject
                              }
                            </span>

                            <span className="flex-1 h-1.5 rounded-full bg-[#e9ebf1] overflow-hidden">
                              <span
                                className={`block h-full rounded-full ${c.bar}`}
                                style={{
                                  width: `${Math.min(
                                    100,
                                    Math.max(
                                      0,
                                      item.accuracy
                                    )
                                  )}%`,
                                }}
                              />
                            </span>

                            <span
                              className={`w-10 text-right text-[10px] font-extrabold ${c.text}`}
                            >
                              {item.accuracy.toFixed(
                                1
                              )}
                              %
                            </span>

                            <span className="text-[#a0a6b2]">
                              ›
                            </span>
                          </button>
                        );
                      }
                    )}

                  </div>
                </div>

              </div>
            </section>

            {/* =================================================
                UPCOMING SCHEDULED TESTS
            ================================================== */}

            {upcomingTests.length >
              0 && (
              <section className="mt-5">

                <div className="bg-white rounded-[14px] border border-[#e8eaf0] shadow-[0_3px_12px_rgba(30,35,60,.035)] overflow-hidden">

                  <div className="px-5 py-4 flex items-center justify-between border-b border-[#eff0f4]">

                    <div>
                      <h2 className="text-[14px] font-extrabold text-[#172033]">
                        Upcoming Tests
                      </h2>

                      <p className="mt-1 text-[10px] text-[#939aa8]">
                        Tests scheduled
                        for you
                      </p>
                    </div>

                    <span className="text-[10px] font-bold text-[#315bea] bg-[#eef2ff] px-2.5 py-1 rounded-full">
                      {
                        upcomingTests.length
                      }{" "}
                      scheduled
                    </span>

                  </div>

                  <div className="divide-y divide-[#eff0f4]">

                    {upcomingTests.map(
                      (test) => {
                        const scheduledId =
                          test.scheduledTestId ||
                          test.id;

                        return (
                          <button
                            key={
                              scheduledId
                            }
                            type="button"
                            disabled={
                              !scheduledId
                            }
                            onClick={() => {
                              if (
                                !scheduledId
                              ) {
                                return;
                              }

                              router.push(
                                `/scheduled-test/${scheduledId}`
                              );
                            }}
                            className="w-full px-5 py-4 flex items-center justify-between gap-4 text-left hover:bg-[#fafbff] transition disabled:cursor-default"
                          >

                            <div className="min-w-0">

                              <h3 className="text-[12px] font-extrabold text-[#172033] truncate">
                                {test.title ||
                                  test.name ||
                                  "Scheduled Test"}
                              </h3>

                              <div className="mt-1 flex flex-wrap items-center gap-3 text-[10px] text-[#939aa8]">

                                <span>
                                  {test.startTime ||
                                    "Start time not configured"}
                                </span>

                                {test.duration && (
                                  <span>
                                    {
                                      test.duration
                                    }
                                  </span>
                                )}

                              </div>

                            </div>

                            <div className="shrink-0 flex items-center gap-2">

                              <span className="text-[10px] font-bold text-[#315bea] bg-[#eef2ff] px-3 py-1.5 rounded-lg">
                                Upcoming
                              </span>

                              <span className="text-[#9ba1ad]">
                                ›
                              </span>

                            </div>

                          </button>
                        );
                      }
                    )}

                  </div>

                </div>

              </section>
            )}

            {/* =================================================
                RECENT TESTS + WEAK AREAS
            ================================================== */}

            <section className="grid grid-cols-1 xl:grid-cols-[1.55fr_1fr] gap-5 mt-5">

              {/* Recent Tests */}

              <div className="bg-white rounded-[14px] border border-[#e8eaf0] shadow-[0_3px_12px_rgba(30,35,60,.035)] overflow-hidden">

                <div className="px-5 py-4 flex items-center justify-between border-b border-[#eff0f4]">

                  <div>
                    <h2 className="text-[14px] font-extrabold">
                      Recent Tests
                    </h2>

                    <p className="mt-1 text-[10px] text-[#939aa8]">
                      Your latest
                      completed tests
                    </p>
                  </div>

                  <button
                    onClick={() =>
                      router.push(
                        "/tests"
                      )
                    }
                    className="h-8 px-3 rounded-lg border border-[#dedaff] text-[10px] font-bold text-[#5541dd]"
                  >
                    View All Tests

                    <span className="ml-1">
                      →
                    </span>
                  </button>

                </div>

                <div className="px-5">

                  <div className="grid grid-cols-[2fr_.8fr_.7fr_.7fr_.7fr_1fr_20px] gap-3 py-3 text-[9px] font-semibold text-[#9198a6] border-b border-[#f1f2f5]">
                    <span>
                      Test Name
                    </span>

                    <span>
                      Difficulty
                    </span>

                    <span>
                      Score
                    </span>

                    <span>
                      Accuracy
                    </span>

                    <span>
                      Time
                    </span>

                    <span>
                      Date
                    </span>

                    <span />
                  </div>

                  {[...results]
                    .reverse()
                    .slice(0, 5)
                    .map((test) => (
                      <button
                        key={`${test.id}-${test.attemptId || ""}`}
                        onClick={() =>
                          router.push(
                            `/test/result/${test.id}`
                          )
                        }
                        className="w-full grid grid-cols-[2fr_.8fr_.7fr_.7fr_.7fr_1fr_20px] gap-3 items-center py-3.5 text-left border-b border-[#f1f2f5] last:border-b-0 hover:bg-[#fbfbfe]"
                      >
                        <span className="min-w-0 flex items-center gap-2">

                          <span className="w-6 h-6 rounded-md bg-[#f1efff] text-[#5c45df] flex items-center justify-center text-[9px] font-bold">
                            ▣
                          </span>

                          <span className="truncate text-[10px] font-semibold text-[#3e4657]">
                            {test.name}
                          </span>

                        </span>

                        <span className="text-[10px] text-[#626b7b] capitalize">
                          {test.difficulty ||
                            "Balanced"}
                        </span>

                        <span
                          className={`text-[10px] font-extrabold ${scoreTone(
                            test.score
                          )}`}
                        >
                          {test.score.toFixed(
                            1
                          )}
                          %
                        </span>

                        <span className="text-[10px] text-[#626b7b]">
                          {test.accuracy.toFixed(
                            1
                          )}
                          %
                        </span>

                        <span className="text-[10px] text-[#626b7b]">
                          {test.time}
                        </span>

                        <span className="text-[10px] text-[#626b7b]">
                          {test.date}
                        </span>

                        <span className="text-[#9ba1ad]">
                          ›
                        </span>

                      </button>
                    ))}

                  {!results.length && (
                    <div className="py-12 text-center">

                      <div className="text-2xl">

                      </div>

                      <p className="mt-2 text-xs font-semibold text-[#596275]">
                        No completed tests
                        yet
                      </p>

                      <p className="mt-1 text-[10px] text-[#9aa1ae]">
                        Start your first
                        test to see your
                        results here.
                      </p>

                    </div>
                  )}

                </div>
              </div>

              {/* Weak Areas */}

              <div className="bg-white rounded-[14px] border border-[#e8eaf0] shadow-[0_3px_12px_rgba(30,35,60,.035)] overflow-hidden">

                <div className="px-5 py-4 flex items-center justify-between border-b border-[#eff0f4]">

                  <div>
                    <h2 className="text-[14px] font-extrabold">
                      Weak Areas
                    </h2>

                    <p className="mt-1 text-[10px] text-[#939aa8]">
                      Topics that need
                      more practice
                    </p>
                  </div>

                  <button className="h-8 px-3 rounded-lg border border-[#dedaff] text-[10px] font-bold text-[#5541dd]">
                    View All

                    <span className="ml-1">
                      →
                    </span>
                  </button>

                </div>

                <div className="p-5 space-y-3">

                  {weakAreas
                    .slice(0, 5)
                    .map((area) => (
                      <div
                        key={`${area.subject}-${area.chapter}`}
                        className="rounded-xl border border-[#edf0f4] p-3"
                      >

                        <div className="flex items-center gap-2">

                          <span className="w-7 h-7 rounded-lg bg-[#fff0f4] text-[#ed4e73] flex items-center justify-center text-[10px]">

                          </span>

                          <span className="text-[10px] font-bold text-[#3f4758] flex-1 truncate">
                            {area.topic ||
                              area.chapter}
                          </span>

                          <span className="text-[9px] text-[#858c99]">
                            {area.subject}
                          </span>

                          <span className="text-[11px] font-extrabold text-rose-500">
                            {area.accuracy.toFixed(
                              0
                            )}
                            %
                          </span>

                        </div>

                        <div className="mt-2.5 ml-9 h-1.5 rounded-full bg-[#e8eaf0] overflow-hidden">

                          <div
                            className="h-full rounded-full bg-rose-500"
                            style={{
                              width: `${Math.min(
                                100,
                                Math.max(
                                  0,
                                  area.accuracy
                                )
                              )}%`,
                            }}
                          />

                        </div>

                        <div className="mt-2 ml-9 text-[8px] text-[#9aa1ae]">
                          {area.correct}{" "}
                          correct ·{" "}
                          {area.wrong}{" "}
                          wrong ·{" "}
                          {
                            area.unanswered
                          }{" "}
                          unanswered
                        </div>

                      </div>
                    ))}

                  {!weakAreas.length && (
                    <div className="py-8 text-center">

                      <div className="text-xl">

                      </div>

                      <p className="mt-2 text-xs font-semibold text-[#596275]">
                        No weak areas yet
                      </p>

                      <p className="mt-1 text-[9px] text-[#9aa1ae]">
                        Complete more tests
                        to generate chapter
                        analysis.
                      </p>

                    </div>
                  )}

                </div>
              </div>

            </section>

            {/* =================================================
                EXTRA ACTUAL ANALYTICS
            ================================================== */}

            <section className="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-5">

              {[
                [
                  "Correct Answers",
                  statistics
                    ?.totalCorrect ??
                    0,
                  "text-emerald-600",
                  "bg-emerald-50",
                ],

                [
                  "Wrong Answers",
                  statistics
                    ?.totalWrong ??
                    0,
                  "text-rose-600",
                  "bg-rose-50",
                ],

                [
                  "Unanswered",
                  statistics
                    ?.totalUnanswered ??
                    0,
                  "text-amber-600",
                  "bg-amber-50",
                ],

                [
                  "Overall Accuracy",
                  `${
                    statistics
                      ?.overallAccuracy ??
                    statistics
                      ?.accuracy ??
                    0
                  }%`,
                  "text-violet-600",
                  "bg-violet-50",
                ],
              ].map(
                ([
                  label,
                  value,
                  text,
                  bg,
                ]) => (
                  <div
                    key={label}
                    className="bg-white rounded-[14px] border border-[#e8eaf0] p-4 flex items-center gap-3"
                  >

                    <div
                      className={`w-10 h-10 rounded-full ${bg} ${text} flex items-center justify-center font-extrabold`}
                    >
                      {label ===
                      "Correct Answers"
                        ? ""
                        : label ===
                            "Wrong Answers"
                          ? "×"
                          : label ===
                              "Unanswered"
                            ? "—"
                            : "%"}
                    </div>

                    <div>
                      <p className="text-[9px] text-[#858c9b] font-semibold">
                        {label}
                      </p>

                      <p
                        className={`text-[19px] font-extrabold ${text}`}
                      >
                        {value}
                      </p>
                    </div>

                  </div>
                )
              )}

            </section>

          </div>
        </div>

      </div>

      {/* =======================================================
          MOBILE NAVIGATION
      ======================================================== */}

      <nav className="xl:hidden fixed bottom-0 inset-x-0 z-40 bg-white/95 backdrop-blur border-t border-[#e8eaf0] px-5 py-2.5">

        <div className="max-w-lg mx-auto flex items-center justify-around">

          <button
            onClick={() =>
              router.push(
                "/dashboard"
              )
            }
            className="flex flex-col items-center gap-1 text-[#5b43df]"
          >
            <MiniIcon
              type="home"
              size={19}
            />

            <span className="text-[9px] font-bold">
              Dashboard
            </span>
          </button>

          <button
            onClick={() =>
              router.push(
                "/tests"
              )
            }
            className="flex flex-col items-center gap-1 text-[#7d8595]"
          >
            <MiniIcon
              type="tests"
              size={19}
            />

            <span className="text-[9px] font-semibold">
              My Tests
            </span>
          </button>

          <button className="flex flex-col items-center gap-1 text-[#7d8595]">

            <span className="w-5 h-5 rounded-full bg-gradient-to-br from-[#7044e8] to-[#4c2bd0] text-white text-[8px] font-bold flex items-center justify-center">
              {initialsText[0]}
            </span>

            <span className="text-[9px] font-semibold">
              Profile
            </span>

          </button>

        </div>

      </nav>

    </main>
  );
}