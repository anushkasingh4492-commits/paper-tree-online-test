"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function UploadDatasetPage() {
  const router = useRouter();

  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function uploadDataset() {
    if (!file) {
      setError("Please select a JSON dataset.");
      return;
    }

    setLoading(true);
    setError("");
    setMessage("");

    try {
      const text = await file.text();

      let dataset;

      try {
        dataset = JSON.parse(text);
      } catch {
        throw new Error("The selected file is not valid JSON.");
      }

      if (!dataset || !Array.isArray(dataset.records)) {
        throw new Error(
          'Dataset must contain a "records" array.'
        );
      }

      const response = await fetch("/api/datasets/upload", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dataset),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.error || "Dataset upload failed."
        );
      }

      setMessage(
        `Dataset uploaded successfully. ${data.inserted} questions added.`
      );

      setFile(null);
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
            Upload a JSON question-bank dataset into the Paper Tree
            question database.
          </p>

          <div className="mt-8 rounded-2xl border-2 border-dashed border-[#dfe4ee] bg-[#fafbfc] p-10 text-center">

            <div className="text-4xl">↑</div>

            <p className="mt-4 font-bold">
              Select JSON dataset
            </p>

            <p className="mt-2 text-xs text-[#8a93a5]">
              Dataset must contain a records array.
            </p>

            <input
              type="file"
              accept=".json,application/json"
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
            onClick={uploadDataset}
            disabled={loading || !file}
            className="mt-8 w-full rounded-xl bg-[#315bea] px-5 py-4 font-bold text-white hover:bg-[#264ac7] disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? "Uploading..." : "Upload Dataset"}
          </button>

        </div>
      </div>
    </main>
  );
}
