"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

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

export default function TestSummaryPage() {
  const [data, setData] = useState<SummaryResponse | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/test-summary", { cache: "no-store" })
      .then(async (response) => {
        const result = (await response.json()) as SummaryResponse;
        if (!response.ok || !result.success) {
          throw new Error(result.error || "Unable to load test summary.");
        }
        setData(result);
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

  return (
    <main className="summary-shell">
      <div className="summary-heading">
        <div>
          <p className="summary-kicker">Paper Tree</p>
          <h1>Test summary</h1>
          <p className="summary-subtitle">{data?.student?.name ? `Welcome back, ${data.student.name}.` : "Review your testing activity."}</p>
        </div>
        <Link className="summary-link" href="/dashboard">Dashboard</Link>
      </div>

      <section className="summary-stats" aria-label="Test totals">
        <div><strong>{summary.total}</strong><span>Total tests</span></div>
        <div><strong>{summary.taken}</strong><span>Completed</span></div>
        <div><strong>{summary.upcoming}</strong><span>Upcoming</span></div>
        <div><strong>{summary.missed}</strong><span>Missed</span></div>
      </section>

      <section className="summary-panel">
        <h2>Your tests</h2>
        {data?.tests?.length ? (
          <div className="summary-list">
            {data.tests.map((test) => (
              <article className="summary-test" key={`${test.id}-${test.status}`}>
                <div>
                  <h3>{test.name}</h3>
                  <p>{test.exam || "Test"} · {test.questionCount} questions{test.date ? ` · ${test.date}` : ""}</p>
                </div>
                <div className="summary-test-meta">
                  <span className={statusClass[test.status] || "summary-status"}>{test.status}</span>
                  {test.status === "Completed" && <span>{test.score ?? 0}{test.totalMarks ? ` / ${test.totalMarks}` : ""}</span>}
                </div>
              </article>
            ))}
          </div>
        ) : <p className="summary-state">No tests to show yet.</p>}
      </section>
    </main>
  );
}
