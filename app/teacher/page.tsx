"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type Paper = {
  id: string;
  code: string;
  exam: string;
  description: string;
  duration_minutes: number;
  status: string;
  created_at: string;
  question_count: number;
};

export default function TeacherPage() {
  const router = useRouter();

  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadPapers();
  }, []);

  async function loadPapers() {
    try {
      const response = await fetch("/api/teacher/papers");

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(result.error || "Failed to load papers.");
      }

      setPapers(result.papers || []);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to load papers."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <div className="mx-auto max-w-7xl px-6 py-10">

        <div className="mb-10 flex items-center justify-between">
          <div>
            <p className="mb-2 text-xs font-bold uppercase tracking-[0.15em] text-[#315bea]">
              Teacher Portal
            </p>

            <h1 className="text-3xl font-extrabold tracking-tight">
              Create & Publish Tests
            </h1>

            <p className="mt-2 text-sm text-[#697386]">
              Create papers automatically or select questions manually.
            </p>
          </div>

          <button
            onClick={() => router.push("/master-login")}
            className="rounded-xl border border-[#e2e6ee] bg-white px-4 py-2.5 text-sm font-bold text-[#697386] hover:bg-[#f7f8fb]"
          >
            Logout
          </button>
        </div>

        <div className="mb-10 grid gap-5 md:grid-cols-2">

          <button
            onClick={() => router.push("/teacher/generate")}
            className="rounded-2xl border border-[#e3e8f5] bg-white p-7 text-left shadow-sm transition hover:-translate-y-1 hover:shadow-md"
          >
            <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-[#eef2ff] text-2xl">

            </div>

            <h2 className="text-xl font-extrabold">
              Auto Generate Paper
            </h2>

            <p className="mt-2 text-sm leading-6 text-[#697386]">
              Generate a complete test from the existing question bank
              using subject, chapter, difficulty and question-count rules.
            </p>

            <div className="mt-5 text-sm font-bold text-[#315bea]">
              Generate paper →
            </div>
          </button>

          <button
            onClick={() => router.push("/teacher/cherry-pick")}
            className="rounded-2xl border border-[#e3e8f5] bg-white p-7 text-left shadow-sm transition hover:-translate-y-1 hover:shadow-md"
          >
            <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-[#eef8f2] text-2xl">

            </div>

            <h2 className="text-xl font-extrabold">
              Cherry Pick Questions
            </h2>

            <p className="mt-2 text-sm leading-6 text-[#697386]">
              Browse the question bank and manually choose exactly which
              questions should appear in the test.
            </p>

            <div className="mt-5 text-sm font-bold text-[#315bea]">
              Pick questions →
            </div>
          </button>

        </div>

        <section className="rounded-2xl border border-[#e5e8ef] bg-white shadow-sm">

          <div className="flex items-center justify-between border-b border-[#eef0f4] px-6 py-5">
            <div>
              <h2 className="text-lg font-extrabold">
                My Papers
              </h2>

              <p className="mt-1 text-sm text-[#8a93a5]">
                Papers created by you
              </p>
            </div>
          </div>

          {loading && (
            <div className="p-8 text-sm text-[#697386]">
              Loading papers...
            </div>
          )}

          {error && (
            <div className="p-8 text-sm font-semibold text-red-600">
              {error}
            </div>
          )}

          {!loading && !error && papers.length === 0 && (
            <div className="p-10 text-center">
              <p className="font-bold">
                No papers created yet.
              </p>

              <p className="mt-2 text-sm text-[#8a93a5]">
                Use Auto Generate or Cherry Pick to create your first paper.
              </p>
            </div>
          )}

          {!loading && papers.length > 0 && (
            <div className="divide-y divide-[#eef0f4]">
              {papers.map((paper) => (
                <div
                  key={paper.id}
                  className="flex items-center justify-between px-6 py-5"
                >
                  <div>
                    <p className="font-bold">
                      {paper.description || paper.code}
                    </p>

                    <p className="mt-1 text-xs text-[#8a93a5]">
                      {paper.exam} · {paper.question_count} questions ·{" "}
                      {paper.duration_minutes} minutes
                    </p>
                  </div>


                </div>
              ))}
            </div>
          )}

        </section>
      </div>
    </main>
  );
}