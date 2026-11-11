"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui/Card";
import { Clock2, FileText, Trophy, User } from "lucide-react";

type Test = {
  id: string;
  name: string;
  exam?: string | null;
  status: string;
  questionCount: number;
  score?: number | null;
  totalMarks?: number | null;
  date?: string | null;
  duration?: string | null;
};

type BrandingResponse = {
  success?: boolean;
  academy?: { name?: string | null; logo_data?: string | null } | null;
};

type SummaryResponse = {
  success: boolean;
  error?: string;
  student?: { name?: string | null };
  summary?: { total: number; taken: number; missed: number; upcoming: number };
  tests?: Test[];
};

const statusClass: Record<string, string> = {
  Completed: "summary-status summary-status-completed",
  Missed: "summary-status summary-status-missed",
  Upcoming: "summary-status summary-status-upcoming",
  "In Progress": "summary-status summary-status-progress",
};

type IconComp = React.ComponentType<React.SVGProps<SVGSVGElement> & { size?: number }>;

const STAT_ICONS: Record<string, IconComp> = {
  total: FileText,
  taken: Trophy,
  upcoming: Clock2,
  missed: User,
};

export default function TestSummaryPage() {
  const [data, setData] = useState<SummaryResponse | null>(null);
  const [branding, setBranding] = useState<BrandingResponse["academy"]>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      fetch("/api/test-summary", { cache: "no-store" }),
      fetch("/api/academy/branding", { cache: "no-store", credentials: "include" }),
    ])
      .then(async ([response, brandingResponse]) => {
        const result = (await response.json()) as SummaryResponse;
        const brand = (await brandingResponse.json().catch(() => null)) as BrandingResponse | null;
        if (!response.ok || !result.success) {
          throw new Error(result.error || "Unable to load test summary.");
        }
        setData(result);
        if (brand?.success && brand.academy) setBranding(brand.academy);
      })
      .catch((reason: unknown) => {
        setError(reason instanceof Error ? reason.message : "Unable to load test summary.");
      });
  }, []);

  if (!data && !error) {
    return <main className="summary-shell"><p className="summary-state">Loading your test summary...</p></main>;
  }

  if (error) {
    return (
      <main className="summary-shell">
        <section className="summary-panel summary-state">
          <h1>Test summary</h1>
          <p>{error}</p>
          <Link className="summary-link" href="/student-login">Return to login</Link>
        </section>
      </main>
    );
  }

  const summary = data?.summary ?? { total: 0, taken: 0, missed: 0, upcoming: 0 };

  const statCards = [
    { key: "total", label: "Total Tests", value: summary.total, icon: STAT_ICONS.total, color: "bg-brand-primary/10 text-brand-primary border-brand-primary/20" },
    { key: "taken", label: "Completed", value: summary.taken, icon: STAT_ICONS.taken, color: "bg-green-50 text-green-600 border-green-100" },
    { key: "upcoming", label: "Upcoming", value: summary.upcoming, icon: STAT_ICONS.upcoming, color: "bg-blue-50 text-blue-600 border-blue-100" },
    { key: "missed", label: "Missed", value: summary.missed, icon: STAT_ICONS.missed, color: "bg-red-50 text-red-600 border-red-100" },
  ];

  return (
    <main className="summary-shell">
      <div className="summary-heading px-4 pt-6 pb-4 max-w-3xl">
        <div className="mb-6">
          <p className="summary-kicker">{branding?.name?.trim() || "Paper Tree"}</p>
          <h1 className="text-3xl font-black tracking-tight text-text-primary mb-2">Test summary</h1>
          <p className="summary-subtitle text-lg leading-relaxed">{data?.student?.name ? `Welcome back, ${data.student.name}.` : "Review your testing activity."}</p>
        </div>
        <Link className="summary-link" href="/dashboard">
          <span className="flex items-center gap-1.5 font-semibold text-brand-primary">← Back to Dashboard</span>
        </Link>
      </div>

      <section className="summary-stats px-4 pb-6 max-w-3xl" aria-label="Test totals">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {statCards.map((card) => (
            <Card
              key={card.key}
              variant="default"
              padding="md"
              radius="card"
              className={`border border-border-default bg-surface-surface flex flex-col items-center justify-center text-center p-6 ${card.color}`}
            >
              <div className="w-10 h-10 rounded-lg flex items-center justify-center mb-3 bg-white/50 shadow-sm">
                <card.icon size={20} className={card.key === "total" ? "text-brand-primary" : card.key === "taken" ? "text-green-600" : card.key === "upcoming" ? "text-blue-600" : "text-red-600"} />
              </div>
              <strong className="text-2xl font-black text-text-primary">{card.value}</strong>
              <span className="text-[10px] font-medium uppercase tracking-wider text-text-body">{card.label}</span>
            </Card>
          ))}
        </div>
      </section>

      <section className="summary-panel px-4 pb-8 max-w-3xl">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h2 className="text-xl font-black text-text-primary">Your tests</h2>
          </div>
        </div>
        {data?.tests?.length ? (
          <div className="summary-list space-y-3">
            {data.tests.map((test) => (
              <Card
                key={`${test.id}-${test.status}`}
                variant="default"
                padding="md"
                radius="card"
                className="border border-border-default bg-surface-surface p-5 flex flex-col gap-3 hover:border-brand-primary/50 transition-all duration-200"
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1 min-w-0">
                    <h3 className="font-black text-text-primary leading-tight">{test.name}</h3>
                    <p className="text-[10px] text-text-body mt-1">{test.exam || "Test"} · {test.questionCount} questions{test.date ? ` · ${test.date}` : ""}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`summary-status ${statusClass[test.status].split(" ")[1]} px-3 py-1 text-[10px] font-bold`}>{test.status}</span>
                    {test.status === "Completed" && <span className="text-[10px] font-bold text-brand-purple">{test.score ?? 0}{test.totalMarks ? ` / ${test.totalMarks}` : ""}</span>}
                  </div>
                </div>
              </Card>
            ))}
          </div>
        ) : (
          <Card
            variant="default"
            padding="lg"
            radius="card"
            className="border border-border-default bg-surface-surface flex flex-col items-center justify-center py-16"
          >
            <FileText size={32} className="text-text-body/40 mb-4" />
            <p className="text-sm text-text-body">No tests to show yet.</p>
          </Card>
        )}
      </section>
    </main>
  );
}
