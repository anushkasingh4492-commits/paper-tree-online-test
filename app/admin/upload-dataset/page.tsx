"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function UploadDatasetPage() {
  const router = useRouter();

  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const [exam, setExam] = useState("MHT-CET");
  const [subject, setSubject] = useState("");
  const [standard, setStandard] = useState("11");
  const [chapter, setChapter] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [releaseVersion, setReleaseVersion] = useState("");

  type ImportRow = {
    id: string;
    file_name: string;
    file_type: string;
    exam: string;
    subject: string;
    standard: number | null;
    total_records: number;
    inserted: number;
    updated: number;
    skipped: number;
    errors: unknown;
    imported_by: string | null;
    created_at: string;
  };

  const [history, setHistory] = useState<ImportRow[]>([]);
  const [historyLoading, setHistoryLoading] = useState(false);

  async function fetchHistory() {
    setHistoryLoading(true);
    try {
      const response = await fetch(
        "/api/datasets/upload?limit=50",
        { cache: "no-store" }
      );
      const data = await response.json();
      if (response.ok && data.success) {
        setHistory(data.imports || []);
      }
    } catch {
      // History is optional; fail silently.
    } finally {
      setHistoryLoading(false);
    }
  }

  useEffect(() => {
    (async () => {
      await fetchHistory();
    })();
  }, []);

  function formatDate(value: string | null | undefined): string {
    if (!value) return "-";
    try {
      return new Date(value).toLocaleString();
    } catch {
      return value;
    }
  }

  async function uploadDataset() {
    if (!file) {
      setError("Please select a dataset file.");
      return;
    }
    if (!subject.trim()) {
      setError("Subject is required.");
      return;
    }

    setLoading(true);
    setError("");
    setMessage("");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("exam", exam);
    formData.append("subject", subject.trim());
    formData.append("standard", standard);
    if (chapter.trim()) formData.append("chapter", chapter.trim());
    if (difficulty.trim()) formData.append("difficulty", difficulty.trim());
    if (releaseVersion.trim())
      formData.append("releaseVersion", releaseVersion.trim());

    try {
      const response = await fetch("/api/datasets/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || "Dataset upload failed.");
      }

      const imp = data.import;
      setMessage(
        `Dataset imported: ${imp?.inserted ?? 0} added, ${
          imp?.updated ?? 0
        } updated, ${imp?.skipped ?? 0} skipped (${imp?.totalRecords ?? 0} total).`
      );
      setFile(null);
      await fetchHistory();
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Dataset upload failed."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <div className="mx-auto max-w-4xl px-6 py-10">

        <button
          onClick={() => router.push("/admin")}
          className="mb-6 text-sm font-semibold text-[#315bea]"
        >
          ← Back to Admin Panel
        </button>

        <div className="rounded-2xl border border-[#e5e8ef] bg-white p-8 shadow-sm">

          <p className="text-xs font-bold uppercase tracking-[0.15em] text-[#315bea]">
            Admin Panel
          </p>

          <h1 className="mt-2 text-3xl font-extrabold">
            Upload Dataset
          </h1>

          <p className="mt-2 text-sm leading-6 text-[#697386]">
            Import a question-bank dataset (JSON, CSV or Excel) into the
            Paper Tree question bank. Imported questions become available
            to students immediately, alongside existing questions.
          </p>

          {/* UPLOAD FORM */}
          <form onSubmit={(e) => { e.preventDefault(); uploadDataset(); }} className="mt-8 space-y-4">

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-[0.12em] text-[#697386] mb-1">
                  Course / Exam
                </label>
                <select
                  value={exam}
                  onChange={(e) => setExam(e.target.value)}
                  className="w-full rounded-xl border border-[#dfe4ee] bg-[#fafbfc] px-4 py-2.5 text-sm focus:border-[#315bea] focus:outline-none"
                >
                  <option value="MHT-CET">MHT-CET</option>
                  <option value="NEET">NEET</option>
                  <option value="JEE">JEE</option>
                  <option value="CAT">CAT</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-[0.12em] text-[#697386] mb-1">
                  Subject
                </label>
                <input
                  type="text"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  placeholder="e.g. Physics"
                  className="w-full rounded-xl border border-[#dfe4ee] bg-[#fafbfc] px-4 py-2.5 text-sm focus:border-[#315bea] focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-[0.12em] text-[#697386] mb-1">
                  Standard
                </label>
                <select
                  value={standard}
                  onChange={(e) => setStandard(e.target.value)}
                  className="w-full rounded-xl border border-[#dfe4ee] bg-[#fafbfc] px-4 py-2.5 text-sm focus:border-[#315bea] focus:outline-none"
                >
                  <option value="11">11th</option>
                  <option value="12">12th</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-[0.12em] text-[#697386] mb-1">
                  Difficulty (optional)
                </label>
                <select
                  value={difficulty}
                  onChange={(e) => setDifficulty(e.target.value)}
                  className="w-full rounded-xl border border-[#dfe4ee] bg-[#fafbfc] px-4 py-2.5 text-sm focus:border-[#315bea] focus:outline-none"
                >
                  <option value="">Any</option>
                  <option value="Easy">Easy</option>
                  <option value="Medium">Medium</option>
                  <option value="Hard">Hard</option>
                </select>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-[0.12em] text-[#697386] mb-1">
                  Chapter (optional)
                </label>
                <input
                  type="text"
                  value={chapter}
                  onChange={(e) => setChapter(e.target.value)}
                  placeholder="e.g. Kinematics"
                  className="w-full rounded-xl border border-[#dfe4ee] bg-[#fafbfc] px-4 py-2.5 text-sm focus:border-[#315bea] focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-[0.12em] text-[#697386] mb-1">
                  Release version (optional)
                </label>
                <input
                  type="text"
                  value={releaseVersion}
                  onChange={(e) => setReleaseVersion(e.target.value)}
                  placeholder="e.g. v1.0.0"
                  className="w-full rounded-xl border border-[#dfe4ee] bg-[#fafbfc] px-4 py-2.5 text-sm focus:border-[#315bea] focus:outline-none"
                />
              </div>
            </div>

            <div className="rounded-2xl border-2 border-dashed border-[#dfe4ee] bg-[#fafbfc] p-6 text-center">
              <div className="text-4xl">↑</div>
              <p className="mt-4 font-bold">Select dataset file</p>
              <p className="mt-2 text-xs text-[#8a93a5]">
                JSON (.json), CSV (.csv) or Excel (.xlsx / .xls)
              </p>
              <input
                type="file"
                accept=".json,.csv,.xlsx,.xls,application/json,text/csv"
                onChange={(e) =>
                  setFile(e.target.files?.[0] || null)
                }
                className="mx-auto mt-6 block text-sm"
              />
              {file && (
                <p className="mt-4 text-sm font-semibold text-[#315bea]">
                  {file.name}
                </p>
              )}
            </div>

            {error && (
              <div className="mt-6 rounded-xl bg-red-50 p-4 text-sm font-semibold text-red-600">
                {error}
              </div>
            )}

            {message && (
              <div className="mt-6 rounded-xl bg-green-50 p-4 text-sm font-semibold text-green-700">
                {message}
              </div>
            )}

            <button
              onClick={(e) => { e.preventDefault(); uploadDataset(); }}
              disabled={loading || !file}
              className="mt-8 w-full rounded-xl bg-[#315bea] px-5 py-4 font-bold text-white hover:bg-[#264ac7] disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Importing..." : "Import Dataset"}
            </button>

          </form>
          {/* IMPORT HISTORY */}
          <div className="mt-12">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-extrabold">Import History</h2>
              {historyLoading && <span className="text-xs text-[#697386]">Loading…</span>}
            </div>

            <div className="rounded-xl border border-[#e5e8ef] bg-white overflow-hidden shadow-sm">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-[#e5e8ef] bg-[#fafbfc]">
                    <th className="px-5 py-3 font-bold text-[#697386] uppercase text-[10px] tracking-[0.12em]">
                      File
                    </th>
                    <th className="px-5 py-3 font-bold text-[#697386] uppercase text-[10px] tracking-[0.12em]">
                      Exam
                    </th>
                    <th className="px-5 py-3 font-bold text-[#697386] uppercase text-[10px] tracking-[0.12em]">
                      Subject
                    </th>
                    <th className="px-5 py-3 font-bold text-[#697386] uppercase text-[10px] tracking-[0.12em]">
                      Std.
                    </th>
                    <th className="px-5 py-3 font-bold text-[#697386] uppercase text-[10px] tracking-[0.12em] text-right">
                      Total
                    </th>
                    <th className="px-5 py-3 font-bold text-[#697386] uppercase text-[10px] tracking-[0.12em] text-right">
                      Added
                    </th>
                    <th className="px-5 py-3 font-bold text-[#697386] uppercase text-[10px] tracking-[0.12em] text-right">
                      Updated
                    </th>
                    <th className="px-5 py-3 font-bold text-[#697386] uppercase text-[10px] tracking-[0.12em] text-right">
                      Skipped
                    </th>
                    <th className="px-5 py-3 font-bold text-[#697386] uppercase text-[10px] tracking-[0.12em]">
                      Imported at
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {history.length === 0 && (
                    <tr>
                      <td colSpan={9} className="px-5 py-8 text-center text-[#8a9386]">
                        No imports yet. Upload a dataset to get started.
                      </td>
                    </tr>
                  )}
                  {history.map((row) => (
                    <tr key={row.id} className="border-b border-[#f0f2f6]">
                      <td className="px-5 py-3 text-[#172033]">
                        {row.file_name}
                      </td>
                      <td className="px-5 py-3">{row.exam}</td>
                      <td className="px-5 py-3">{row.subject}</td>
                      <td className="px-5 py-3">
                        {row.standard ?? "-"}
                      </td>
                      <td className="px-5 py-3 text-right text-[#172033]">
                        {row.total_records}
                      </td>
                      <td className="px-5 py-3 text-right text-[#16a34a]">
                        +{row.inserted}
                      </td>
                      <td className="px-5 py-3 text-right text-[#ca8a04]">
                        {row.updated}
                      </td>
                      <td className="px-5 py-3 text-right text-[#697386]">
                        {row.skipped}
                      </td>
                      <td className="px-5 py-3 text-[#8a93a5]">
                        {formatDate(row.created_at)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </div>
    </main>
  );
}
