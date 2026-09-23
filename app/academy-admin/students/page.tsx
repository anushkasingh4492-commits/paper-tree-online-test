"use client";

import { FormEvent, useEffect, useState } from "react";

type Student = {
  id: string;
  name: string;
  email: string;
};

type Batch = {
  id: string;
  name: string;
  course_name: string | null;
};

export default function AcademyStudentsPage() {
  const [students, setStudents] = useState<Student[]>([]);
  const [batches, setBatches] = useState<Batch[]>([]);
  const [batchId, setBatchId] = useState("");

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function loadStudents() {
    try {
      const res = await fetch("/api/academy-admin/students", {
        cache: "no-store",
      });

      const data = await res.json();

      if (data.success) {
        setStudents(data.students || []);
      }
    } catch {
      setMessage("Could not load students.");
    }
  }

  async function loadBatches() {
    try {
      const res = await fetch("/api/academy-admin/batches", {
        cache: "no-store",
      });

      const data = await res.json();

      if (data.success) {
        setBatches(data.batches || []);
      }
    } catch {
      setMessage("Could not load batches.");
    }
  }

  useEffect(() => {
    void loadStudents();
    void loadBatches();
  }, []);

  async function createStudent(e: FormEvent) {
    e.preventDefault();
    setMessage("");

    if (!batchId) {
      setMessage(
        "Please create and select a batch before adding a student."
      );
      return;
    }

    setLoading(true);

    try {
      const res = await fetch("/api/academy-admin/students", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name,
          email,
          password,
          batchId,
        }),
      });

      const data = await res.json();

      if (!data.success) {
        setMessage(data.error || "Failed to create student");
        return;
      }

      setMessage("Student created successfully.");

      setName("");
      setEmail("");
      setPassword("");
      setBatchId("");

      await loadStudents();
      await loadBatches();
    } catch {
      setMessage("Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  async function removeStudent(student: Student) {
    if (
      !window.confirm(
        `Remove ${student.name}? Their login, batch memberships and test history will be deleted.`
      )
    ) {
      return;
    }

    const response = await fetch(
      `/api/academy-admin/students?id=${encodeURIComponent(student.id)}`,
      {
        method: "DELETE",
      }
    );

    const data = await response.json();

    if (!response.ok || !data.success) {
      setMessage(data.error || "Could not remove student.");
      return;
    }

    setStudents((current) =>
      current.filter((item) => item.id !== student.id)
    );

    setMessage("Student removed.");
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <header className="border-b border-[#e7eaf0] bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-xl font-extrabold">
              Student Management
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
            Students
          </h2>

          <p className="mt-2 text-sm text-[#697386]">
            Create a batch first, then add students to their respective
            batch. Students automatically get access to the course assigned
            to their batch.
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-[360px_1fr]">
          {/* Create student */}
          <form
            onSubmit={createStudent}
            className="h-fit rounded-2xl border border-[#e3e8f5] bg-white p-6 shadow-sm"
          >
            <h3 className="text-lg font-extrabold">
              Add Student
            </h3>

            {batches.length === 0 && (
              <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-xs font-semibold leading-5 text-amber-700">
                No batches available. Please create a batch first before
                adding a student.
              </div>
            )}

            <input
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Student name"
              className="mt-5 w-full rounded-xl border border-[#dfe4ee] px-4 py-3 text-sm outline-none focus:border-[#315bea]"
            />

            {/* Batch selection */}
            <select
              required
              value={batchId}
              onChange={(e) => setBatchId(e.target.value)}
              disabled={batches.length === 0}
              className="mt-3 w-full rounded-xl border border-[#dfe4ee] bg-white px-4 py-3 text-sm outline-none focus:border-[#315bea] disabled:cursor-not-allowed disabled:bg-[#f5f6f8] disabled:text-[#9aa1ad]"
            >
              <option value="">Select batch</option>

              {batches.map((batch) => (
                <option key={batch.id} value={batch.id}>
                  {batch.name}
                  {batch.course_name
                    ? ` — ${batch.course_name}`
                    : ""}
                </option>
              ))}
            </select>

            <input
              required
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Student email"
              className="mt-3 w-full rounded-xl border border-[#dfe4ee] px-4 py-3 text-sm outline-none focus:border-[#315bea]"
            />

            <input
              required
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              className="mt-3 w-full rounded-xl border border-[#dfe4ee] px-4 py-3 text-sm outline-none focus:border-[#315bea]"
            />

            <button
              disabled={loading || batches.length === 0 || !batchId}
              type="submit"
              className="mt-5 w-full rounded-xl bg-[#315bea] px-4 py-3 text-sm font-bold text-white disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Creating..." : "Create Student"}
            </button>

            {message && (
              <p className="mt-4 text-sm font-medium text-[#697386]">
                {message}
              </p>
            )}
          </form>

          {/* Student list */}
          <section className="rounded-2xl border border-[#e3e8f5] bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-extrabold">
                Academy Students
              </h3>

              <span className="rounded-full bg-[#f2f5ff] px-3 py-1 text-xs font-bold text-[#315bea]">
                {students.length} students
              </span>
            </div>

            <div className="mt-5 space-y-3">
              {students.length === 0 ? (
                <div className="rounded-xl border border-dashed border-[#dfe4ee] p-8 text-center text-sm text-[#697386]">
                  No students yet.
                </div>
              ) : (
                students.map((student) => (
                  <div
                    key={student.id}
                    className="flex items-center justify-between rounded-xl border border-[#e7eaf0] p-4"
                  >
                    <div>
                      <p className="font-bold">
                        {student.name}
                      </p>

                      <p className="mt-1 text-sm text-[#697386]">
                        {student.email}
                      </p>
                    </div>

                    <button
                      onClick={() => void removeStudent(student)}
                      className="rounded-lg border border-red-200 bg-red-50 px-3 py-1.5 text-xs font-bold text-red-600"
                    >
                      Remove
                    </button>
                  </div>
                ))
              )}
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}