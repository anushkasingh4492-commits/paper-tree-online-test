"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

type TestResult = {
  id: string;
  name: string;
  score: number;
  accuracy: number;
  time: string;
  date: string;
  subject: string;
  chapter: string;
};

type DashboardPayload = {
  student?: { name?: string };
  results?: TestResult[];
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

const adityaFallback: TestResult[] = [
  {
    id: "test-01",
    name: "MHT-CET Physics Chapter Test - 01",
    score: 52,
    accuracy: 64,
    time: "1h 42m",
    date: "12 Jul 2026",
    subject: "Physics",
    chapter: "Rotational Motion",
  },
  {
    id: "test-02",
    name: "MHT-CET Chemistry Practice - 02",
    score: 61,
    accuracy: 71,
    time: "1h 36m",
    date: "15 Jul 2026",
    subject: "Chemistry",
    chapter: "Chemical Bonding",
  },
  {
    id: "test-03",
    name: "MHT-CET Mathematics Practice - 03",
    score: 58,
    accuracy: 68,
    time: "1h 51m",
    date: "18 Jul 2026",
    subject: "Mathematics",
    chapter: "Trigonometry",
  },
  {
    id: "test-04",
    name: "MHT-CET Physics Chapter Test - 04",
    score: 72,
    accuracy: 79,
    time: "1h 48m",
    date: "21 Jul 2026",
    subject: "Physics",
    chapter: "Gravitation",
  },
  {
    id: "test-05",
    name: "MHT-CET Chemistry Practice - 05",
    score: 68,
    accuracy: 76,
    time: "1h 55m",
    date: "24 Jul 2026",
    subject: "Chemistry",
    chapter: "Thermodynamics",
  },
  {
    id: "test-06",
    name: "MHT-CET Mathematics Practice - 06",
    score: 75,
    accuracy: 82,
    time: "2h 02m",
    date: "27 Jul 2026",
    subject: "Mathematics",
    chapter: "Probability",
  },
  {
    id: "test-07",
    name: "MHT-CET Full Test - 01",
    score: 81,
    accuracy: 88,
    time: "2h 42m",
    date: "30 Jul 2026",
    subject: "Physics",
    chapter: "Mixed",
  },
  {
    id: "test-08",
    name: "MHT-CET Full Test - 02",
    score: 77,
    accuracy: 84,
    time: "2h 49m",
    date: "02 Aug 2026",
    subject: "Chemistry",
    chapter: "Mixed",
  },
  {
    id: "test-09",
    name: "MHT-CET Full Test - 03",
    score: 68,
    accuracy: 76,
    time: "2h 51m",
    date: "05 Aug 2026",
    subject: "Mathematics",
    chapter: "Mixed",
  },
  {
    id: "test-10",
    name: "MHT-CET Full Test - 04",
    score: 91.3,
    accuracy: 94,
    time: "2h 56m",
    date: "08 Aug 2026",
    subject: "Physics",
    chapter: "Mixed",
  },
  {
    id: "test-11",
    name: "MHT-CET Full Test - 05",
    score: 82,
    accuracy: 89,
    time: "2h 54m",
    date: "11 Aug 2026",
    subject: "Chemistry",
    chapter: "Mixed",
  },
  {
    id: "test-12",
    name: "MHT-CET Full Test - 06",
    score: 85,
    accuracy: 92,
    time: "2h 58m",
    date: "23 Aug 2026",
    subject: "Mathematics",
    chapter: "Mixed",
  },
];

const subjectColors: Record<
  string,
  {
    bar: string;
    text: string;
    iconBg: string;
    icon: string;
  }
> = {
  Physics: {
    bar: "bg-blue-500",
    text: "text-blue-600",
    iconBg: "bg-blue-50",
    icon: "⚛",
  },
  Chemistry: {
    bar: "bg-emerald-500",
    text: "text-emerald-600",
    iconBg: "bg-emerald-50",
    icon: "✦",
  },
  Mathematics: {
    bar: "bg-pink-500",
    text: "text-pink-600",
    iconBg: "bg-pink-50",
    icon: "∑",
  },
};

function initials(name: string) {
  const parts = name.trim().split(/\s+/).filter(Boolean);

  if (!parts.length) return "A";

  if (parts.length === 1) {
    return parts[0][0].toUpperCase();
  }

  return `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase();
}

function scoreTone(score: number) {
  if (score >= 80) return "text-emerald-600";
  if (score >= 60) return "text-blue-600";
  if (score >= 50) return "text-amber-500";
  return "text-rose-500";
}

function MiniIcon({
  type,
  size = 20,
}: {
  type: IconType;
  size?: number;
}) {
  const paths: Record<IconType, React.ReactNode> = {
    home: (
      <>
        <path d="m3 9 6-5 6 5" />
        <path d="M5 8v7h8V8" />
        <path d="M8 15v-4h2v4" />
      </>
    ),

    tests: (
      <>
        <rect x="4" y="3" width="8" height="12" rx="1.5" />
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
        <circle cx="8" cy="8" r="5.5" />
        <circle cx="8" cy="8" r="2.3" />
        <path d="m12 4 2-2M13 2h1v1" />
      </>
    ),

    user: (
      <>
        <circle cx="8" cy="5" r="2.3" />
        <path d="M3.5 14c.7-2.4 2.2-3.6 4.5-3.6s3.8 1.2 4.5 3.6" />
      </>
    ),

    settings: (
      <>
        <circle cx="8" cy="8" r="2.3" />
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
        <rect x="3" y="4" width="10" height="9" rx="1.5" />
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

function PerformanceChart({ results }: { results: TestResult[] }) {
  const w = 760;
  const h = 210;
  const padX = 28;
  const padTop = 18;
  const padBottom = 28;

  const innerW = w - padX * 2;
  const innerH = h - padTop - padBottom;

  const points = results.map((r, i) => {
    const x =
      padX +
      (i * innerW) / Math.max(results.length - 1, 1);

    const y =
      padTop +
      innerH -
      (r.score / 100) * innerH;

    return {
      x,
      y,
      score: r.score,
      date: r.date
        .replace(" 2026", "")
        .replace(" ", "\n"),
    };
  });

  const line = points
    .map(
      (p, i) =>
        `${i ? "L" : "M"} ${p.x} ${p.y}`
    )
    .join(" ");

  const area =
    points.length > 0
      ? `${line} L ${
          points[points.length - 1].x
        } ${h - padBottom} L ${
          points[0].x
        } ${h - padBottom} Z`
      : "";

  return (
    <div className="mt-5 overflow-hidden">
      <svg
        viewBox={`0 0 ${w} ${h}`}
        className="w-full h-[225px]"
        preserveAspectRatio="none"
      >
        {[0, 25, 50, 75, 100].map((v) => {
          const y =
            padTop +
            innerH -
            (v / 100) * innerH;

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

        {points.length > 1 && (
          <path
            d={area}
            fill="url(#areaFill)"
          />
        )}

        {points.length > 1 && (
          <path
            d={line}
            fill="none"
            stroke="#6246e5"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        )}

        {points.map((p, i) => (
          <g key={i}>
            <text
              x={p.x}
              y={Math.max(12, p.y - 10)}
              textAnchor="middle"
              fontSize="9.5"
              fontWeight="700"
              fill="#34394a"
            >
              {Number.isInteger(p.score)
                ? p.score
                : p.score.toFixed(1)}
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
              {p.date.split("\n")[0]}
            </text>
          </g>
        ))}

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
    </div>
  );
}

function Donut({ results }: { results: TestResult[] }) {
  const counts = [
    results.filter((r) => r.score >= 90).length,
    results.filter(
      (r) => r.score >= 70 && r.score < 90
    ).length,
    results.filter(
      (r) => r.score >= 50 && r.score < 70
    ).length,
    results.filter((r) => r.score < 50).length,
  ];

  const total = results.length || 1;

  const colors = [
    "#20b77a",
    "#3b73e9",
    "#f5a900",
    "#ee4c72",
  ];

  let start = 0;

  const segments = counts.map((count, i) => {
    const end =
      start + (count / total) * 360;

    const seg = {
      start,
      end,
      color: colors[i],
      count,
    };

    start = end;

    return seg;
  });

  const polar = (
    angle: number,
    radius: number
  ) => {
    const a =
      ((angle - 90) * Math.PI) / 180;

    return [
      60 + radius * Math.cos(a),
      60 + radius * Math.sin(a),
    ];
  };

  const arc = (
    startAngle: number,
    endAngle: number,
    color: string
  ) => {
    if (endAngle - startAngle >= 359.9) {
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

    const [x1, y1] = polar(
      startAngle,
      40
    );

    const [x2, y2] = polar(
      endAngle,
      40
    );

    const large =
      endAngle - startAngle > 180 ? 1 : 0;

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

          {segments.map((s, i) => (
            <g key={i}>
              {arc(
                s.start,
                s.end,
                s.color
              )}
            </g>
          ))}
        </svg>

        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-[20px] font-extrabold text-[#202638]">
            {results.length}
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
            "#20b77a",
          ],
          [
            "70% - 89%",
            counts[1],
            "#3b73e9",
          ],
          [
            "50% - 69%",
            counts[2],
            "#f5a900",
          ],
          [
            "Below 50%",
            counts[3],
            "#ee4c72",
          ],
        ].map(
          ([label, count, color], i) => (
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
                  (Number(count) / total) *
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

export default function DashboardPage() {
  const router = useRouter();

  const [studentName, setStudentName] =
    useState("aditya");

  const [results, setResults] =
    useState<TestResult[]>(adityaFallback);

  useEffect(() => {
    const saved =
      localStorage.getItem("studentName") ||
      localStorage.getItem("username");

    if (saved?.trim()) {
      setStudentName(saved.trim());
    }

    fetch("/api/dashboard", {
      cache: "no-store",
      credentials: "include",
    })
      .then(async (r) => {
        if (!r.ok) return null;

        const data: DashboardPayload =
          await r.json();

        if (data.student?.name?.trim()) {
          setStudentName(
            data.student.name.trim()
          );
        }

        if (
          Array.isArray(data.results) &&
          data.results.length
        ) {
          setResults(data.results);
        }

        return data;
      })
      .catch(() => undefined);
  }, []);

  const average = useMemo(
    () =>
      results.length
        ? results.reduce(
            (sum, r) => sum + r.score,
            0
          ) / results.length
        : 0,
    [results]
  );

  const best = useMemo(
    () =>
      results.length
        ? Math.max(
            ...results.map((r) => r.score)
          )
        : 0,
    [results]
  );

  const lowest = useMemo(
    () =>
      results.length
        ? Math.min(
            ...results.map((r) => r.score)
          )
        : 0,
    [results]
  );

  const subjectPerformance = useMemo(() => {
    return [
      "Physics",
      "Chemistry",
      "Mathematics",
    ].map((subject) => {
      const rows = results.filter(
        (r) => r.subject === subject
      );

      return {
        subject,
        score: rows.length
          ? rows.reduce(
              (s, r) => s + r.score,
              0
            ) / rows.length
          : 0,
      };
    });
  }, [results]);

  const initialsText = initials(
    studentName
  );

  const latest = results[results.length - 1];

  return (
    <main className="min-h-screen bg-[#f8f9fc] text-[#1d2435]">
      <div className="flex min-h-screen">

        {/* =====================================================
            SIDEBAR
            Only Dashboard + My Tests remain here
        ====================================================== */}

        <aside className="hidden xl:flex w-[220px] shrink-0 bg-white border-r border-[#e9ebf1] flex-col">

          {/* Logo */}

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

          {/* Sidebar navigation */}

          <div className="px-4 pt-5 flex-1">

            <p className="px-2 mb-2 text-[9px] uppercase tracking-[.16em] font-bold text-[#a1a7b3]">
              Workspace
            </p>

            <nav className="space-y-1">

              {/* Dashboard */}

              <button
                onClick={() =>
                  router.push("/dashboard")
                }
                className="w-full h-10 flex items-center gap-3 px-2.5 rounded-xl bg-[#f0efff] text-[#5640db] text-xs font-bold"
              >
                <span className="w-7 h-7 rounded-lg bg-white flex items-center justify-center">
                  <MiniIcon type="home" />
                </span>

                Dashboard
              </button>

              {/* My Tests */}

              <button
                onClick={() =>
                  router.push("/tests")
                }
                className="w-full h-10 flex items-center gap-3 px-2.5 rounded-xl text-[#657083] hover:bg-[#f7f8fb] text-xs font-medium"
              >
                <span className="w-7 h-7 rounded-lg bg-[#f5f6f9] flex items-center justify-center">
                  <MiniIcon type="tests" />
                </span>

                My Tests
              </button>

            </nav>
          </div>

          {/* Premium Card */}

          <div className="px-4 pb-3">
            <div className="rounded-xl bg-gradient-to-br from-[#fff8e9] via-[#fff4fb] to-[#f2edff] border border-[#eee8ff] p-3.5">

              <div className="flex items-center gap-2 text-[#7357dc]">
                <span className="w-7 h-7 rounded-lg bg-white flex items-center justify-center">
                  ♛
                </span>

                <span className="text-xs font-extrabold">
                  Go Premium
                </span>
              </div>

              <p className="text-[9px] text-[#818898] leading-4 mt-2">
                Unlock unlimited tests,
                detailed analytics and more.
              </p>

              <button className="mt-2.5 w-full h-8 rounded-lg bg-gradient-to-r from-[#6744e8] to-[#7d31e8] text-white text-[10px] font-bold">
                Upgrade Now
              </button>
            </div>
          </div>

          {/* Logout */}

          <button
            className="mx-5 mb-5 mt-1 flex items-center gap-3 h-9 text-xs text-[#657083]"
            onClick={() => {
              localStorage.removeItem(
                "studentName"
              );
              localStorage.removeItem(
                "username"
              );
              router.push("/login");
            }}
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
                  👋
                </span>
              </h1>

              <p className="mt-1 text-[11px] text-[#858c9b]">
                Here's your performance
                overview and test insights
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

          <div className="p-5 lg:p-6 xl:p-7 max-w-[1500px] mx-auto">

            {/* Hero */}

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
                  Keep pushing forward,{" "}
                  {studentName}!
                </h2>

                <p className="mt-1.5 text-[12px] text-white/85">
                  Consistency today leads to
                  success tomorrow.
                </p>

                <button
                  onClick={() =>
                    router.push("/tests")
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

                    <div className="flex gap-2">
                      <span className="text-[#26bd84]">
                        ✓
                      </span>

                      <span className="h-1.5 bg-white rounded w-14 mt-1.5" />
                    </div>

                    <div className="flex gap-2">
                      <span className="text-[#26bd84]">
                        ✓
                      </span>

                      <span className="h-1.5 bg-white rounded w-16 mt-1.5" />
                    </div>

                    <div className="flex gap-2">
                      <span className="text-[#26bd84]">
                        ✓
                      </span>

                      <span className="h-1.5 bg-white rounded w-12 mt-1.5" />
                    </div>

                  </div>
                </div>

                <div className="absolute right-0 bottom-[91px] w-2 h-12 bg-[#26334a] rotate-[22deg]" />

                <div className="absolute right-[-5px] bottom-[101px] w-7 h-5 rounded-full bg-[#17263b] rotate-[22deg]" />

                <div className="absolute left-[55px] bottom-10 w-7 h-12 rounded-b-xl bg-[#6ac16c]" />

                <div className="absolute left-[51px] bottom-[57px] w-8 h-8 rounded-full bg-[#84d777]" />

              </div>

              {/* Quote */}

              <div className="hidden lg:block absolute right-7 top-8 w-[210px] text-right">

                <div className="text-4xl font-serif leading-none text-white/45">
                  “
                </div>

                <p className="text-[12px] leading-5 font-medium">
                  Success is the sum of
                  <br />
                  small efforts repeated
                  <br />
                  day in and day out.
                </p>

                <p className="mt-2 text-[10px] font-semibold text-white/80">
                  — Robert Collier
                </p>

              </div>

            </section>

            {/* Stats */}

            <section className="grid grid-cols-2 xl:grid-cols-5 gap-4 mt-5">

              {[
                [
                  "Tests Taken",
                  String(results.length),
                  "↑ 33% vs last 30 days",
                  "bg-blue-50 text-blue-600",
                  "▣",
                ],
                [
                  "Average Score",
                  `${average.toFixed(1)}%`,
                  "↑ 8.7% improvement",
                  "bg-pink-50 text-pink-600",
                  "▥",
                ],
                [
                  "Best Score",
                  `${best.toFixed(1)}%`,
                  latest?.name ||
                    "Highest completed score",
                  "bg-emerald-50 text-emerald-600",
                  "★",
                ],
                [
                  "Attempts",
                  "48",
                  "Total test attempts",
                  "bg-violet-50 text-violet-600",
                  "↗",
                ],
                [
                  "Study Time",
                  "18h 42m",
                  "↑ 25% vs last 30 days",
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

                        <p
                          className={`mt-1 text-[9px] truncate ${
                            label === "Best Score"
                              ? "text-[#858c9b]"
                              : "text-emerald-500"
                          }`}
                        >
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

            {/* Performance + Score Distribution */}

            <section className="grid grid-cols-1 xl:grid-cols-[1.55fr_1fr] gap-5 mt-5">

              {/* Performance Trend */}

              <div className="bg-white rounded-[14px] border border-[#e8eaf0] p-5 shadow-[0_3px_12px_rgba(30,35,60,.035)]">

                <div className="flex items-start justify-between">

                  <div>
                    <h2 className="text-[14px] font-extrabold">
                      Performance Trend
                    </h2>

                    <p className="mt-1 text-[10px] text-[#939aa8]">
                      Your average score across
                      completed tests
                    </p>
                  </div>

                  <button className="h-8 px-3 rounded-lg border border-[#e7e9f0] text-[10px] font-semibold text-[#4e596c]">
                    Last 30 Days
                    <span className="ml-2">
                      ⌄
                    </span>
                  </button>

                </div>

                <PerformanceChart
                  results={results}
                />

                <div className="grid grid-cols-3 gap-3 mt-2">

                  <div className="rounded-xl border border-[#e9e2ff] bg-[#faf8ff] p-3">

                    <div className="flex items-center gap-2">

                      <span className="w-8 h-8 rounded-lg bg-[#eee7ff] text-[#7047e7] flex items-center justify-center">
                        ♜
                      </span>

                      <div>
                        <p className="text-[9px] text-[#7d8493]">
                          Highest Score
                        </p>

                        <p className="text-[17px] font-extrabold">
                          {best.toFixed(1)}%
                        </p>

                        <p className="text-[8px] text-[#9aa0ad]">
                          {
                            results.find(
                              (r) =>
                                r.score === best
                            )?.date
                          }
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
                          {lowest.toFixed(1)}%
                        </p>

                        <p className="text-[8px] text-[#9aa0ad]">
                          {
                            results.find(
                              (r) =>
                                r.score ===
                                lowest
                            )?.date
                          }
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
                          72%
                        </p>

                        <p className="text-[8px] text-[#9aa0ad]">
                          Good
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
                    Score Distribution
                  </h2>

                  <p className="mt-1 text-[10px] text-[#939aa8]">
                    Based on your last{" "}
                    {results.length} tests
                  </p>

                  <div className="mt-4">
                    <Donut
                      results={results}
                    />
                  </div>

                </div>

                {/* Subject Performance */}

                <div className="bg-white rounded-[14px] border border-[#e8eaf0] p-5 shadow-[0_3px_12px_rgba(30,35,60,.035)]">

                  <h2 className="text-[14px] font-extrabold">
                    Subject Performance
                  </h2>

                  <p className="mt-1 text-[10px] text-[#939aa8]">
                    Average score by subject
                  </p>

                  <div className="mt-5 space-y-4">

                    {subjectPerformance.map(
                      (item) => {
                        const c =
                          subjectColors[
                            item.subject
                          ];

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
                              {item.subject}
                            </span>

                            <span className="flex-1 h-1.5 rounded-full bg-[#e9ebf1] overflow-hidden">

                              <span
                                className={`block h-full rounded-full ${c.bar}`}
                                style={{
                                  width: `${item.score}%`,
                                }}
                              />

                            </span>

                            <span
                              className={`w-10 text-right text-[10px] font-extrabold ${c.text}`}
                            >
                              {item.score.toFixed(
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

            {/* Recent Tests + Weak Areas */}

            <section className="grid grid-cols-1 xl:grid-cols-[1.55fr_1fr] gap-5 mt-5">

              {/* Recent Tests */}

              <div className="bg-white rounded-[14px] border border-[#e8eaf0] shadow-[0_3px_12px_rgba(30,35,60,.035)] overflow-hidden">

                <div className="px-5 py-4 flex items-center justify-between border-b border-[#eff0f4]">

                  <div>
                    <h2 className="text-[14px] font-extrabold">
                      Recent Tests
                    </h2>

                    <p className="mt-1 text-[10px] text-[#939aa8]">
                      Your latest completed tests
                    </p>
                  </div>

                  <button
                    onClick={() =>
                      router.push("/tests")
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

                  <div className="grid grid-cols-[2fr_.7fr_.7fr_.7fr_1fr_20px] gap-3 py-3 text-[9px] font-semibold text-[#9198a6] border-b border-[#f1f2f5]">

                    <span>Test Name</span>
                    <span>Score</span>
                    <span>Accuracy</span>
                    <span>Time</span>
                    <span>Date</span>
                    <span />

                  </div>

                  {[...results]
                    .reverse()
                    .slice(0, 5)
                    .map((test) => (
                      <button
                        key={test.id}
                        onClick={() =>
                          router.push(
                            `/test/${test.id}`
                          )
                        }
                        className="w-full grid grid-cols-[2fr_.7fr_.7fr_.7fr_1fr_20px] gap-3 items-center py-3.5 text-left border-b border-[#f1f2f5] last:border-b-0 hover:bg-[#fbfbfe]"
                      >

                        <span className="min-w-0 flex items-center gap-2">

                          <span className="w-6 h-6 rounded-md bg-[#f1efff] text-[#5c45df] flex items-center justify-center text-[9px] font-bold">
                            ▣
                          </span>

                          <span className="truncate text-[10px] font-semibold text-[#3e4657]">
                            {test.name}
                          </span>

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
                          {test.accuracy}%
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
                      Topics that need more
                      practice
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

                  {[
                    [
                      "Rotational Motion",
                      "Physics",
                      42,
                      "bg-rose-500",
                    ],
                    [
                      "Thermodynamics",
                      "Chemistry",
                      49,
                      "bg-amber-500",
                    ],
                    [
                      "Probability",
                      "Mathematics",
                      54,
                      "bg-orange-400",
                    ],
                  ].map(
                    ([
                      topic,
                      subject,
                      score,
                      bar,
                    ]) => (
                      <div
                        key={topic}
                        className="rounded-xl border border-[#edf0f4] p-3"
                      >

                        <div className="flex items-center gap-2">

                          <span className="w-7 h-7 rounded-lg bg-[#fff0f4] text-[#ed4e73] flex items-center justify-center text-[10px]">
                            ♟
                          </span>

                          <span className="text-[10px] font-bold text-[#3f4758] flex-1">
                            {topic}
                          </span>

                          <span className="text-[9px] text-[#858c99]">
                            {subject}
                          </span>

                          <span className="text-[11px] font-extrabold text-rose-500">
                            {score}%
                          </span>

                        </div>

                        <div className="mt-2.5 ml-9 h-1.5 rounded-full bg-[#e8eaf0] overflow-hidden">

                          <div
                            className={`h-full rounded-full ${bar}`}
                            style={{
                              width: `${score}%`,
                            }}
                          />

                        </div>

                      </div>
                    )
                  )}

                </div>
              </div>

            </section>

          </div>
        </div>
      </div>

      {/* Mobile navigation */}

      <nav className="xl:hidden fixed bottom-0 inset-x-0 z-40 bg-white/95 backdrop-blur border-t border-[#e8eaf0] px-5 py-2.5">

        <div className="max-w-lg mx-auto flex items-center justify-around">

          <button
            onClick={() =>
              router.push("/dashboard")
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
              router.push("/tests")
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