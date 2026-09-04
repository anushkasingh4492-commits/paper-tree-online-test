"use client";

import { FormEvent, useEffect, useState } from "react";

type Student = {
  id: string;
  name: string;
  email: string;
};

export default function AcademyStudentsPage() {
  const [students, setStudents] = useState<Student[]>([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function loadStudents() {
    const res = await fetch("/api/academy-admin/students");
    const data = await res.json();

    if (data.success) {
      setStudents(data.students || []);
    }
  }

  useEffect(() => {
    loadStudents();
  }, []);

  async function createStudent(e: FormEvent) {
    e.preventDefault();
    setMessage("");
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
  rollNumber: "",
  className: "",
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
    

      await loadStudents();
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
            Create and manage students belonging to your academy.
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

            <input
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Student name"
              className="mt-5 w-full rounded-xl border border-[#dfe4ee] px-4 py-3 text-sm outline-none focus:border-[#315bea]"
            />

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
              disabled={loading}
              type="submit"
              className="mt-5 w-full rounded-xl bg-[#315bea] px-4 py-3 text-sm font-bold text-white disabled:opacity-50"
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

                    <span className="rounded-lg bg-[#f4f6fa] px-3 py-1.5 text-xs font-bold text-[#697386]">
                      Student
                    </span>
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
