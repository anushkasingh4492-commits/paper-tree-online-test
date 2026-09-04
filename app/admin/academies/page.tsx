"use client";

import { FormEvent, useEffect, useState } from "react";

type Academy = {
  id: string;
  name: string;
  code: string;
  teacher_count: number;
  student_count: number;
};

export default function AcademiesPage() {
  const [academies, setAcademies] = useState<Academy[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  const [academyName, setAcademyName] = useState("");
  const [academyCode, setAcademyCode] = useState("");
  const [adminName, setAdminName] = useState("");
  const [adminEmail, setAdminEmail] = useState("");
  const [adminPassword, setAdminPassword] = useState("");

  async function loadAcademies() {
    try {
      const res = await fetch("/api/admin/academies");
      const data = await res.json();

      if (data.success) {
        setAcademies(data.academies || []);
      }
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadAcademies();
  }, []);

  async function createAcademy(e: FormEvent) {
    e.preventDefault();

    setSaving(true);
    setMessage("");

    try {
      const res = await fetch("/api/admin/academies", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          academyName,
          academyCode,
          adminName,
          adminEmail,
          adminPassword,
        }),
      });

      const data = await res.json();

      if (!res.ok || !data.success) {
        setMessage(data.error || "Failed to create academy.");
        return;
      }

      setMessage(
        `Academy created successfully. Admin login: ${data.admin.email}`
      );

      setAcademyName("");
      setAcademyCode("");
      setAdminName("");
      setAdminEmail("");
      setAdminPassword("");

      await loadAcademies();
    } catch {
      setMessage("Network error. Please try again.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <header className="border-b border-[#e7eaf0] bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-xl font-extrabold">
              Academy Management
            </h1>
            <p className="mt-1 text-xs text-[#697386]">
              Create and manage Paper Tree academy tenants.
            </p>
          </div>

          <a
            href="/admin"
            className="rounded-xl border border-[#e2e6ee] bg-white px-4 py-2.5 text-sm font-bold"
          >
            ← Admin
          </a>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-10">
        <div className="grid gap-8 lg:grid-cols-[420px_1fr]">
          {/* CREATE */}

          <section className="rounded-2xl border border-[#e3e8f5] bg-white p-6 shadow-sm">
            <h2 className="text-lg font-extrabold">
              Create Academy
            </h2>

            <p className="mt-1 text-xs text-[#697386]">
              Create the academy and its administrator account together.
            </p>

            <form
              onSubmit={createAcademy}
              className="mt-6 space-y-4"
            >
              <input
                value={academyName}
                onChange={(e) => setAcademyName(e.target.value)}
                placeholder="Academy name"
                className="w-full rounded-xl border border-[#dfe4ed] px-4 py-3 text-sm outline-none focus:border-[#315bea]"
                required
              />

              <input
                value={academyCode}
                onChange={(e) =>
                  setAcademyCode(e.target.value.toUpperCase())
                }
                placeholder="Academy code e.g. VIGYAN"
                className="w-full rounded-xl border border-[#dfe4ed] px-4 py-3 text-sm uppercase outline-none focus:border-[#315bea]"
                required
              />

              <div className="border-t border-[#eef0f4] pt-4">
                <p className="mb-3 text-xs font-bold uppercase tracking-wider text-[#929aaa]">
                  Academy Admin
                </p>

                <div className="space-y-3">
                  <input
                    value={adminName}
                    onChange={(e) => setAdminName(e.target.value)}
                    placeholder="Admin name"
                    className="w-full rounded-xl border border-[#dfe4ed] px-4 py-3 text-sm outline-none focus:border-[#315bea]"
                    required
                  />

                  <input
                    type="email"
                    value={adminEmail}
                    onChange={(e) => setAdminEmail(e.target.value)}
                    placeholder="Admin email"
                    className="w-full rounded-xl border border-[#dfe4ed] px-4 py-3 text-sm outline-none focus:border-[#315bea]"
                    required
                  />

                  <input
                    type="password"
                    value={adminPassword}
                    onChange={(e) =>
                      setAdminPassword(e.target.value)
                    }
                    placeholder="Admin password"
                    minLength={6}
                    className="w-full rounded-xl border border-[#dfe4ed] px-4 py-3 text-sm outline-none focus:border-[#315bea]"
                    required
                  />
                </div>
              </div>

              {message && (
                <div className="rounded-xl bg-[#f2f5ff] px-4 py-3 text-xs font-semibold text-[#315bea]">
                  {message}
                </div>
              )}

              <button
                type="submit"
                disabled={saving}
                className="w-full rounded-xl bg-[#315bea] px-4 py-3 text-sm font-bold text-white disabled:opacity-50"
              >
                {saving ? "Creating..." : "Create Academy"}
              </button>
            </form>
          </section>

          {/* LIST */}

          <section>
            <h2 className="mb-4 text-lg font-extrabold">
              Academies
            </h2>

            {loading ? (
              <div className="rounded-2xl bg-white p-6 text-sm text-[#697386]">
                Loading...
              </div>
            ) : academies.length === 0 ? (
              <div className="rounded-2xl border border-dashed border-[#dfe4ed] bg-white p-10 text-center text-sm text-[#697386]">
                No academies created yet.
              </div>
            ) : (
              <div className="space-y-4">
                {academies.map((academy) => (
                  <div
                    key={academy.id}
                    className="rounded-2xl border border-[#e3e8f5] bg-white p-5 shadow-sm"
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 className="font-extrabold">
                          {academy.name}
                        </h3>

                        <p className="mt-1 text-xs font-bold text-[#315bea]">
                          {academy.code}
                        </p>
                      </div>

                      <span className="rounded-lg bg-[#f2f5ff] px-3 py-1 text-xs font-bold text-[#315bea]">
                        Active
                      </span>
                    </div>

                    <div className="mt-5 flex gap-6 text-xs text-[#697386]">
                      <span>
                        Teachers:{" "}
                        <strong className="text-[#172033]">
                          {academy.teacher_count}
                        </strong>
                      </span>

                      <span>
                        Students:{" "}
                        <strong className="text-[#172033]">
                          {academy.student_count}
                        </strong>
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
        </div>
      </div>
    </main>
  );
}
