"use client";

import { FormEvent, useEffect, useState } from "react";

type Teacher = {
  id: string;
  name: string;
  email: string;
};

export default function AcademyTeachersPage() {
  const [teachers, setTeachers] = useState<Teacher[]>([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  async function loadTeachers() {
    const res = await fetch("/api/academy-admin/teachers");
    const data = await res.json();

    if (data.success) {
      setTeachers(data.teachers);
    }
  }

  useEffect(() => {
    loadTeachers();
  }, []);

  async function createTeacher(e: FormEvent) {
    e.preventDefault();
    setMessage("");

    const res = await fetch("/api/academy-admin/teachers", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
        email,
        password,
      }),
    });

    const data = await res.json();

    if (!data.success) {
      setMessage(data.error || "Failed to create teacher");
      return;
    }

    setMessage("Teacher created successfully.");

    setName("");
    setEmail("");
    setPassword("");

    loadTeachers();
  }

  return (
    <main className="min-h-screen bg-slate-50 p-8">
      <div className="mx-auto max-w-5xl">
        <button
          onClick={() => history.back()}
          className="mb-6 text-sm text-slate-600 hover:text-black"
        >
          ← Back
        </button>

        <h1 className="text-3xl font-bold text-slate-900">
          Teachers
        </h1>

        <p className="mt-1 text-slate-500">
          Manage teachers belonging to your academy.
        </p>

        <div className="mt-8 grid gap-8 md:grid-cols-[350px_1fr]">
          <form
            onSubmit={createTeacher}
            className="rounded-2xl bg-white p-6 shadow-sm"
          >
            <h2 className="text-lg font-semibold">
              Add Teacher
            </h2>

            <input
              className="mt-4 w-full rounded-lg border p-3"
              placeholder="Teacher name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />

            <input
              className="mt-3 w-full rounded-lg border p-3"
              placeholder="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <input
              className="mt-3 w-full rounded-lg border p-3"
              placeholder="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <button
              type="submit"
              className="mt-4 w-full rounded-lg bg-black px-4 py-3 font-medium text-white"
            >
              Create Teacher
            </button>

            {message && (
              <p className="mt-4 text-sm text-slate-600">
                {message}
              </p>
            )}
          </form>

          <section className="rounded-2xl bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold">
              Academy Teachers
            </h2>

            <div className="mt-4 space-y-3">
              {teachers.length === 0 ? (
                <p className="text-slate-500">
                  No teachers yet.
                </p>
              ) : (
                teachers.map((teacher) => (
                  <div
                    key={teacher.id}
                    className="rounded-xl border p-4"
                  >
                    <div className="font-medium">
                      {teacher.name}
                    </div>

                    <div className="text-sm text-slate-500">
                      {teacher.email}
                    </div>
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
