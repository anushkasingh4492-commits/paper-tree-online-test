"use client";

import { FormEvent, useEffect, useState } from "react";

type Batch = {
  id: string;
  name: string;
  class_name: string | null;
  created_at: string;
};

type Student = {
  id: string;
  name: string;
  email: string;
  roll_number: string | null;
  class_name: string | null;
};

export default function AcademyBatchesPage() {
  const [batches, setBatches] = useState<Batch[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [selectedBatch, setSelectedBatch] = useState<Batch | null>(null);
  const [assignedStudents, setAssignedStudents] = useState<string[]>([]);

  const [name, setName] = useState("");
  const [className, setClassName] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [studentLoading, setStudentLoading] = useState(false);

  async function loadBatches() {
    const res = await fetch("/api/academy-admin/batches");
    const data = await res.json();

    if (data.success) {
      setBatches(data.batches || []);
    }
  }

  async function loadStudents() {
    const res = await fetch("/api/academy-admin/students");
    const data = await res.json();

    if (data.success) {
      setStudents(data.students || []);
    }
  }

  useEffect(() => {
    loadBatches();
    loadStudents();
  }, []);

  async function openManageStudents(batch: Batch) {
    setSelectedBatch(batch);
    setStudentLoading(true);

    try {
      const res = await fetch(
        `/api/academy-admin/batches/students?batchId=${encodeURIComponent(
          batch.id
        )}`
      );

      const data = await res.json();

      if (data.success) {
        setAssignedStudents(
          (data.students || []).map((student: Student) =>
            String(student.id)
          )
        );
      } else {
        setAssignedStudents([]);
      }
    } catch {
      setAssignedStudents([]);
    } finally {
      setStudentLoading(false);
    }
  }

  async function toggleStudent(studentId: string) {
    if (!selectedBatch) return;

    const isAssigned = assignedStudents.includes(studentId);
    const action = isAssigned ? "remove" : "add";

    try {
      const res = await fetch(
        "/api/academy-admin/batches/students",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            batchId: selectedBatch.id,
            studentId,
            action,
          }),
        }
      );

      const data = await res.json();

      if (!data.success) {
        alert(data.error || "Failed to update student");
        return;
      }

      setAssignedStudents((current) =>
        isAssigned
          ? current.filter((id) => id !== studentId)
          : [...current, studentId]
      );
    } catch {
      alert("Something went wrong.");
    }
  }

  async function createBatch(e: FormEvent) {
    e.preventDefault();
    setMessage("");
    setLoading(true);

    try {
      const res = await fetch("/api/academy-admin/batches", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name,
          className,
        }),
      });

      const data = await res.json();

      if (!data.success) {
        setMessage(data.error || "Failed to create batch");
        return;
      }

      setMessage("Batch created successfully.");
      setName("");
      setClassName("");

      await loadBatches();
    } catch {
      setMessage("Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <header className="border-b border-[#e7eaf0] bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-xl font-extrabold">
              Batch Management
            </h1>

            <p className="mt-1 text-xs font-bold tracking-wider text-[#315bea]">
              ACADEMY ADMIN
            </p>
          </div>

          <button
            onClick={() => history.back()}
            className="rounded-xl border border-[#e2e6ee] bg-white px-4 py-2.5 text-sm font-bold text-[#697386]"
          >
            ← Back
          </button>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-10">
        <div className="mb-10">
          <p className="text-xs font-bold uppercase tracking-[0.15em] text-[#315bea]">
            Academy Management
          </p>

          <h2 className="mt-2 text-3xl font-extrabold">
            Batches
          </h2>

          <p className="mt-2 text-sm text-[#697386]">
            Create and manage classes and batches for your academy.
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-[360px_1fr]">
          {/* Create batch */}
          <form
            onSubmit={createBatch}
            className="h-fit rounded-2xl border border-[#e3e8f5] bg-white p-6 shadow-sm"
          >
            <h3 className="text-lg font-extrabold">
              Create Batch
            </h3>

            <input
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Batch name"
              className="mt-5 w-full rounded-xl border border-[#dfe4ee] px-4 py-3 text-sm outline-none focus:border-[#315bea]"
            />

            <select
              value={className}
              onChange={(e) => setClassName(e.target.value)}
              className="mt-3 w-full rounded-xl border border-[#dfe4ee] bg-white px-4 py-3 text-sm outline-none focus:border-[#315bea]"
            >
              <option value="">Select class</option>
              <option value="Class 11">Class 11</option>
              <option value="Class 12">Class 12</option>
              <option value="NEET">NEET</option>
              <option value="JEE">JEE</option>
              <option value="MHT-CET">MHT-CET</option>
            </select>

            <button
              disabled={loading}
              type="submit"
              className="mt-5 w-full rounded-xl bg-[#315bea] px-4 py-3 text-sm font-bold text-white disabled:opacity-50"
            >
              {loading ? "Creating..." : "Create Batch"}
            </button>

            {message && (
              <p className="mt-4 text-sm font-medium text-[#697386]">
                {message}
              </p>
            )}
          </form>

          {/* Batch list */}
          <section className="rounded-2xl border border-[#e3e8f5] bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-extrabold">
                Academy Batches
              </h3>

              <span className="rounded-full bg-[#f2f5ff] px-3 py-1 text-xs font-bold text-[#315bea]">
                {batches.length} batches
              </span>
            </div>

            <div className="mt-5 space-y-3">
              {batches.length === 0 ? (
                <div className="rounded-xl border border-dashed border-[#dfe4ee] p-8 text-center text-sm text-[#697386]">
                  No batches yet.
                </div>
              ) : (
                batches.map((batch) => (
                  <div
                    key={batch.id}
                    className="flex items-center justify-between rounded-xl border border-[#e7eaf0] p-4"
                  >
                    <div>
                      <p className="font-bold">
                        {batch.name}
                      </p>

                      {batch.class_name && (
                        <p className="mt-1 text-sm text-[#697386]">
                          {batch.class_name}
                        </p>
                      )}
                    </div>

                    <div className="flex items-center gap-3">
                      <button
                        onClick={() =>
                          openManageStudents(batch)
                        }
                        className="rounded-lg bg-[#eef2ff] px-3 py-1.5 text-xs font-bold text-[#315bea] hover:bg-[#e3e9ff]"
                      >
                        Manage Students
                      </button>

                      <span className="rounded-lg bg-[#f4f6fa] px-3 py-1.5 text-xs font-bold text-[#697386]">
                        Batch
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </section>
        </div>
      </div>

      {/* Manage students modal */}
      {selectedBatch && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
          <div className="max-h-[80vh] w-full max-w-2xl overflow-hidden rounded-2xl bg-white shadow-2xl">
            <div className="flex items-center justify-between border-b border-[#e7eaf0] px-6 py-5">
              <div>
                <h3 className="text-lg font-extrabold">
                  Manage Students
                </h3>

                <p className="mt-1 text-sm text-[#697386]">
                  {selectedBatch.name}
                </p>
              </div>

              <button
                onClick={() => {
                  setSelectedBatch(null);
                  setAssignedStudents([]);
                }}
                className="rounded-lg border border-[#e2e6ee] px-3 py-2 text-sm font-bold text-[#697386]"
              >
                ✕
              </button>
            </div>

            <div className="max-h-[60vh] overflow-y-auto p-6">
              {studentLoading ? (
                <div className="py-10 text-center text-sm text-[#697386]">
                  Loading students...
                </div>
              ) : students.length === 0 ? (
                <div className="rounded-xl border border-dashed border-[#dfe4ee] p-8 text-center text-sm text-[#697386]">
                  No students in this academy yet.
                </div>
              ) : (
                <div className="space-y-2">
                  {students.map((student) => {
                    const assigned = assignedStudents.includes(
                      String(student.id)
                    );

                    return (
                      <button
                        key={student.id}
                        onClick={() =>
                          toggleStudent(String(student.id))
                        }
                        className={`flex w-full items-center justify-between rounded-xl border p-4 text-left transition ${
                          assigned
                            ? "border-[#315bea] bg-[#f2f5ff]"
                            : "border-[#e7eaf0] bg-white hover:bg-[#fafbfe]"
                        }`}
                      >
                        <div>
                          <p className="font-bold">
                            {student.name}
                          </p>

                          <p className="mt-1 text-xs text-[#697386]">
                            {student.email}
                            {student.roll_number
                              ? ` • Roll No. ${student.roll_number}`
                              : ""}
                          </p>
                        </div>

                        <div
                          className={`flex h-6 w-6 items-center justify-center rounded-md border text-xs font-extrabold ${
                            assigned
                              ? "border-[#315bea] bg-[#315bea] text-white"
                              : "border-[#d8deea] bg-white text-transparent"
                          }`}
                        >
                          ✓
                        </div>
                      </button>
                    );
                  })}
                </div>
              )}
            </div>

            <div className="border-t border-[#e7eaf0] px-6 py-4">
              <div className="flex items-center justify-between">
                <p className="text-sm font-bold text-[#697386]">
                  {assignedStudents.length} student
                  {assignedStudents.length === 1 ? "" : "s"} assigned
                </p>

                <button
                  onClick={() => {
                    setSelectedBatch(null);
                    setAssignedStudents([]);
                  }}
                  className="rounded-xl bg-[#315bea] px-5 py-2.5 text-sm font-bold text-white"
                >
                  Done
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}