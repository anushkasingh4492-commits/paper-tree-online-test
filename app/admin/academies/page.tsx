"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";

type Academy = {
  id: string;
  name: string;
  code: string;
  teacher_count: number;
  student_count: number;
  batch_count?: number;
  subscription_plan?: string;
  student_limit?: number;
  subscription_start?: string;
  subscription_end?: string;
  status?: string;
};

type AcademyDetailsData = {
  students: Array<Record<string, unknown>>;
  teachers: Array<Record<string, unknown>>;
  batches: Array<Record<string, unknown>>;
  papers: Array<Record<string, unknown>>;
  scheduledTests: Array<Record<string, unknown>>;
  questions: Array<Record<string, unknown>>;
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

  const [studentLimit, setStudentLimit] = useState("10");
  const [subscriptionMonths, setSubscriptionMonths] = useState("12");
  const [startDate, setStartDate] = useState(
    new Date().toISOString().split("T")[0]
  );

  const [selectedAcademy, setSelectedAcademy] =
    useState<Academy | null>(null);
  const [detailsVersion, setDetailsVersion] = useState(0);

  const [studentName, setStudentName] = useState("");
  const [studentEmail, setStudentEmail] = useState("");
  const [studentPassword, setStudentPassword] = useState("");
  const [studentRoll, setStudentRoll] = useState("");
  const [studentExam, setStudentExam] = useState("JEE-MAINS");

  const [teacherName, setTeacherName] = useState("");
  const [teacherEmail, setTeacherEmail] = useState("");
  const [teacherPassword, setTeacherPassword] = useState("");

  const [batchName, setBatchName] = useState("");
  const [batchClass, setBatchClass] = useState("");
async function loadAcademies() {
  try {
    setLoading(true);

    const res = await fetch("/api/admin/academies", {
      cache: "no-store",
      credentials: "include",
    });

    const data = await res.json();

    console.log("ACADEMIES API:", res.status, data);

    if (!res.ok || !data.success) {
      setMessage(data.error || "Failed to load academies.");
      return;
    }

    setAcademies(data.academies || []);
  } catch (error) {
    console.error("LOAD ACADEMIES ERROR:", error);
    setMessage("Failed to load academies.");
  } finally {
    setLoading(false);
  }
}

  useEffect(() => {
    loadAcademies();
  }, []);

  const totals = useMemo(() => {
    return {
      academies: academies.length,
      students: academies.reduce(
        (sum, academy) => sum + Number(academy.student_count || 0),
        0
      ),
      teachers: academies.reduce(
        (sum, academy) => sum + Number(academy.teacher_count || 0),
        0
      ),
    };
  }, [academies]);

  function getExpiryDate() {
    const date = new Date(startDate);
    date.setMonth(date.getMonth() + Number(subscriptionMonths || 0));
    return date.toISOString().split("T")[0];
  }

  async function updateAcademy(academy: Academy, changes: Record<string, unknown>) {
    const res = await fetch(`/api/admin/academies/${academy.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(changes),
    });
    const data = await res.json();
    if (!res.ok || !data.success) {
      setMessage(data.error || "Failed to update academy.");
      return;
    }
    setMessage("Academy updated successfully.");
    setAcademies((current) => current.map((item) => item.id === academy.id ? { ...item, ...data.academy } : item));
    setSelectedAcademy((current) => current?.id === academy.id ? { ...current, ...data.academy } : current);
  }

  async function resetAcademyAdmin(academy: Academy) {
    const password = window.prompt("Enter a new academy admin password (minimum 6 characters):");
    if (!password) return;

    const res = await fetch(`/api/admin/academies/${academy.id}/reset-admin`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    });
    const data = await res.json();

    if (!res.ok || !data.success) {
      setMessage(data.error || "Failed to reset academy admin password.");
      return;
    }

    setMessage(`Credentials reset: ${data.credentials.email} / ${data.credentials.password}`);
  }

  function getStatus(academy: Academy) {
    if (academy.status === "SUSPENDED") {
      return {
        label: "Suspended",
        className: "bg-red-50 text-red-600",
      };
    }

    if (academy.status === "RESTRICTED") {
      return {
        label: "Restricted",
        className: "bg-orange-50 text-orange-600",
      };
    }

    if (academy.subscription_end) {
      const expiry = new Date(academy.subscription_end);
      const now = new Date();

      if (expiry < now) {
        return {
          label: "Expired",
          className: "bg-red-50 text-red-600",
        };
      }

      const days =
        (expiry.getTime() - now.getTime()) /
        (1000 * 60 * 60 * 24);

      if (days <= 30) {
        return {
          label: "Expiring Soon",
          className: "bg-orange-50 text-orange-600",
        };
      }
    }

    return {
      label: "Active",
      className: "bg-green-50 text-green-600",
    };
  }

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

          // Subscription information
          subscriptionPlan: `${studentLimit} Students · ${subscriptionMonths} Months`,
          studentLimit: Number(studentLimit),
          subscriptionStart: startDate,
          subscriptionEnd: getExpiryDate(),
        }),
      });

      const data = await res.json();

      if (!res.ok || !data.success) {
        setMessage(data.error || "Failed to create academy.");
        return;
      }

      setMessage(
        `✅ Academy created successfully · Admin: ${data.admin.email}`
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

  async function addStudent(e: FormEvent) {
    e.preventDefault();

    if (!selectedAcademy) return;

    try {
      const res = await fetch("/api/academy-admin/students", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          academyId: selectedAcademy.id,
          name: studentName,
          email: studentEmail,
          password: studentPassword,
          rollNumber: studentRoll,
          exam: studentExam,
        }),
      });

      const data = await res.json();

      if (!res.ok || !data.success) {
        setMessage(data.error || "Failed to add student.");
        return;
      }

      setMessage(
        `✅ Student created. Username: ${studentEmail} · Password: ${studentPassword}`
      );

      setDetailsVersion((version) => version + 1);
      await loadAcademies();

      setStudentName("");
      setStudentEmail("");
      setStudentPassword("");
      setStudentRoll("");
      setStudentExam("JEE-MAINS");
    } catch {
      setMessage("Failed to add student.");
    }
  }

  async function addTeacher(e: FormEvent) {
    e.preventDefault();

    if (!selectedAcademy) return;

    try {
      const res = await fetch("/api/academy-admin/teachers", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          academyId: selectedAcademy.id,
          name: teacherName,
          email: teacherEmail,
          password: teacherPassword,
        }),
      });

      const data = await res.json();

      if (!res.ok || !data.success) {
        setMessage(data.error || "Failed to add teacher.");
        return;
      }

      setMessage(
        `✅ Teacher created. Username: ${teacherEmail} · Password: ${teacherPassword}`
      );

      setDetailsVersion((version) => version + 1);
      await loadAcademies();

      setTeacherName("");
      setTeacherEmail("");
      setTeacherPassword("");
    } catch {
      setMessage("Failed to add teacher.");
    }
  }

  async function createBatch(e: FormEvent) {
    e.preventDefault();

    if (!selectedAcademy) return;

    try {
      const res = await fetch("/api/academy-admin/batches", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          academyId: selectedAcademy.id,
          name: batchName,
          className: batchClass,
        }),
      });

      const data = await res.json();

      if (!res.ok || !data.success) {
        setMessage(data.error || "Failed to create batch.");
        return;
      }

      setMessage("✅ Batch created successfully.");

      setDetailsVersion((version) => version + 1);
      await loadAcademies();

      setBatchName("");
      setBatchClass("");
    } catch {
      setMessage("Failed to create batch.");
    }
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      {/* HEADER */}

      <header className="border-b border-[#e7eaf0] bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#315bea] text-lg font-black text-white">
              P
            </div>

            <div>
              <h1 className="text-lg font-extrabold">
                Paper Tree
              </h1>

              <p className="text-[10px] font-bold tracking-[0.15em] text-[#929aaa]">
                MASTER ADMIN
              </p>
            </div>
          </div>

          <a
            href="/admin"
            className="rounded-xl border border-[#e2e6ee] bg-white px-4 py-2.5 text-sm font-bold"
          >
            ← Dashboard
          </a>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-8">
        {/* TITLE */}

        <div className="mb-8">
          <p className="text-xs font-bold uppercase tracking-[0.15em] text-[#315bea]">
            🏢 Master Administration
          </p>

          <h2 className="mt-2 text-3xl font-extrabold tracking-tight">
            Academy Control Center
          </h2>

          <p className="mt-2 max-w-3xl text-sm leading-6 text-[#697386]">
            Manage academies, subscriptions, students, teachers,
            batches and access from one place.
          </p>
        </div>

        {/* STATS */}

        <section className="mb-8 grid gap-4 md:grid-cols-4">
          <Stat
            title="Academies"
            value={totals.academies}
            icon="🏫"
          />

          <Stat
            title="Students"
            value={totals.students}
            icon="👨‍🎓"
          />

          <Stat
            title="Teachers"
            value={totals.teachers}
            icon="👨‍🏫"
          />

          <Stat
            title="System Access"
            value="FULL"
            icon="🔐"
          />
        </section>

        {/* CREATE ACADEMY */}

        <section className="mb-8 rounded-2xl border border-[#e3e8f5] bg-white p-6 shadow-sm">
          <div className="mb-6">
            <h3 className="text-xl font-extrabold">
              🏫 Create New Academy
            </h3>

            <p className="mt-1 text-xs text-[#697386]">
              Create the academy, administrator and subscription
              together.
            </p>
          </div>

          <form
            onSubmit={createAcademy}
            className="grid gap-4 md:grid-cols-2 lg:grid-cols-3"
          >
            <Input
              value={academyName}
              onChange={setAcademyName}
              placeholder="Academy name"
            />

            <Input
              value={academyCode}
              onChange={(value) =>
                setAcademyCode(value.toUpperCase())
              }
              placeholder="Academy code e.g. VIGYAN"
            />

            <Input
              value={adminName}
              onChange={setAdminName}
              placeholder="Academy admin name"
            />

            <Input
              type="email"
              value={adminEmail}
              onChange={setAdminEmail}
              placeholder="Admin email"
            />

            <Input
              type="password"
              value={adminPassword}
              onChange={setAdminPassword}
              placeholder="Admin password"
            />

            <div>
              <label className="mb-2 block text-xs font-bold text-[#697386]">
                🎟️ Subscription
              </label>

              <div className="grid grid-cols-2 gap-2">
                <input
                  type="number"
                  min="1"
                  value={studentLimit}
                  onChange={(e) => setStudentLimit(e.target.value)}
                  placeholder="Student seats"
                  className="w-full rounded-xl border border-[#dfe4ed] px-4 py-3 text-sm outline-none focus:border-[#315bea]"
                />
                <input
                  type="number"
                  min="1"
                  value={subscriptionMonths}
                  onChange={(e) => setSubscriptionMonths(e.target.value)}
                  placeholder="Months"
                  className="w-full rounded-xl border border-[#dfe4ed] px-4 py-3 text-sm outline-none focus:border-[#315bea]"
                />
              </div>
            </div>

            <div>
              <label className="mb-2 block text-xs font-bold text-[#697386]">
                📅 Subscription Start
              </label>

              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="w-full rounded-xl border border-[#dfe4ed] px-4 py-3 text-sm outline-none focus:border-[#315bea]"
              />
            </div>

            <div className="rounded-xl bg-[#f7f9ff] p-4">
              <p className="text-[11px] font-bold text-[#929aaa]">
                SUBSCRIPTION SUMMARY
              </p>

              <p className="mt-1 text-sm font-extrabold text-[#315bea]">
                {studentLimit} student seats · {subscriptionMonths} months
              </p>

              <p className="mt-1 text-xs text-[#697386]">
                Expires: {getExpiryDate()}
              </p>
            </div>

            {message && (
              <div className="md:col-span-2 lg:col-span-3 rounded-xl bg-[#f2f5ff] px-4 py-3 text-xs font-semibold text-[#315bea]">
                {message}
              </div>
            )}

            <button
              type="submit"
              disabled={saving}
              className="rounded-xl bg-[#315bea] px-5 py-3 text-sm font-bold text-white transition hover:bg-[#264bc9] disabled:opacity-50"
            >
              {saving
                ? "Creating..."
                : "➕ Create Academy"}
            </button>
          </form>
        </section>

        {/* ACADEMIES */}

        <section>
          <div className="mb-4 flex items-end justify-between">
            <div>
              <h3 className="text-xl font-extrabold">
                🏢 Academy Management
              </h3>

              <p className="mt-1 text-xs text-[#697386]">
                Select an academy to manage everything related
                to it.
              </p>
            </div>

            <span className="text-xs font-bold text-[#929aaa]">
              {academies.length} academies
            </span>
          </div>

          {loading ? (
            <div className="rounded-2xl bg-white p-8 text-sm text-[#697386]">
              Loading academies...
            </div>
          ) : academies.length === 0 ? (
            <div className="rounded-2xl border border-dashed border-[#dfe4ed] bg-white p-10 text-center text-sm text-[#697386]">
              No academies created yet.
            </div>
          ) : (
            <div className="space-y-4">
              {academies.map((academy) => {
                const status = getStatus(academy);

                return (
                  <div
                    key={academy.id}
                    className={`rounded-2xl border bg-white p-6 shadow-sm transition ${
                      selectedAcademy?.id === academy.id
                        ? "border-[#315bea] ring-2 ring-[#315bea]/10"
                        : "border-[#e3e8f5]"
                    }`}
                  >
                    <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
                      <div>
                        <div className="flex items-center gap-3">
                          <h4 className="text-lg font-extrabold">
                            {academy.name}
                          </h4>

                          <span
                            className={`rounded-lg px-3 py-1 text-[11px] font-bold ${status.className}`}
                          >
                            {status.label}
                          </span>
                        </div>

                        <p className="mt-1 text-xs font-bold text-[#315bea]">
                          CODE: {academy.code}
                        </p>
                      </div>

                      <button
                        onClick={() =>
                          setSelectedAcademy(
                            selectedAcademy?.id === academy.id
                              ? null
                              : academy
                          )
                        }
                        className="rounded-xl bg-[#315bea] px-4 py-2.5 text-xs font-bold text-white"
                      >
                        {selectedAcademy?.id === academy.id
                          ? "Close Management"
                          : "Manage Academy →"}
                      </button>
                    </div>

                    <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
                      <MiniStat
                        label="Students"
                        value={academy.student_count}
                        icon="👨‍🎓"
                      />

                      <MiniStat
                        label="Teachers"
                        value={academy.teacher_count}
                        icon="👨‍🏫"
                      />

                      <MiniStat
                        label="Batches"
                        value={academy.batch_count ?? "—"}
                        icon="📚"
                      />

                      <MiniStat
                        label="Student limit"
                        value={
                          academy.student_limit ?? "—"
                        }
                        icon="🎟️"
                      />

                      <MiniStat
                        label="Expiry"
                        value={
                          academy.subscription_end
                            ? new Date(
                                academy.subscription_end
                              ).toLocaleDateString()
                            : "Not set"
                        }
                        icon="📅"
                      />
                    </div>

                    {selectedAcademy?.id === academy.id && (
                      <div className="mt-6 border-t border-[#eef0f4] pt-6">
                        <div className="mb-5">
                          <h5 className="font-extrabold">
                            ⚙️ Manage {academy.name}
                          </h5>

                          <p className="mt-1 text-xs text-[#697386]">
                            Students, teachers and batches can be
                            managed from here.
                          </p>
                        </div>

                        {message && (
                          <div className="mb-5 rounded-xl border border-[#cfe0ff] bg-[#f2f6ff] px-4 py-3 text-sm font-semibold text-[#315bea]">
                            {message}
                          </div>
                        )}

                        <div className="grid gap-5 lg:grid-cols-3">
                          {/* STUDENT */}

                          <ManagementCard
                            title="👨‍🎓 Add Student"
                            description="Create a student account for this academy."
                          >
                            <form
                              onSubmit={addStudent}
                              className="space-y-3"
                            >
                              <Input
                                value={studentName}
                                onChange={setStudentName}
                                placeholder="Student name"
                              />

                              <Input
                                type="email"
                                value={studentEmail}
                                onChange={setStudentEmail}
                                placeholder="Student email"
                              />

                              <Input
                                type="password"
                                value={studentPassword}
                                onChange={setStudentPassword}
                                placeholder="Student password"
                              />

                              <Input
                                value={studentRoll}
                                onChange={setStudentRoll}
                                placeholder="Roll number"
                              />

                              <select
                                value={studentExam}
                                onChange={(e) => setStudentExam(e.target.value)}
                                className="w-full rounded-xl border border-[#dfe4ed] bg-white px-4 py-3 text-sm outline-none focus:border-[#315bea]"
                              >
                                <option value="JEE-MAINS">JEE Mains</option>
                                <option value="NEET">NEET</option>
                                <option value="MHT-CET">MHT-CET</option>
                              </select>

                              <button className="w-full rounded-xl bg-[#315bea] px-4 py-3 text-xs font-bold text-white">
                                ➕ Add Student
                              </button>
                            </form>
                          </ManagementCard>

                          {/* TEACHER */}

                          <ManagementCard
                            title="👨‍🏫 Add Teacher"
                            description="Create a teacher account for this academy."
                          >
                            <form
                              onSubmit={addTeacher}
                              className="space-y-3"
                            >
                              <Input
                                value={teacherName}
                                onChange={setTeacherName}
                                placeholder="Teacher name"
                              />

                              <Input
                                type="email"
                                value={teacherEmail}
                                onChange={setTeacherEmail}
                                placeholder="Teacher email"
                              />

                              <Input
                                type="password"
                                value={teacherPassword}
                                onChange={setTeacherPassword}
                                placeholder="Teacher password"
                              />

                              <button className="w-full rounded-xl bg-[#315bea] px-4 py-3 text-xs font-bold text-white">
                                ➕ Add Teacher
                              </button>
                            </form>
                          </ManagementCard>

                          {/* BATCH */}

                          <ManagementCard
                            title="📚 Create Batch"
                            description="Create a batch for this academy."
                          >
                            <form
                              onSubmit={createBatch}
                              className="space-y-3"
                            >
                              <Input
                                value={batchName}
                                onChange={setBatchName}
                                placeholder="Batch name"
                              />

                              <Input
                                value={batchClass}
                                onChange={setBatchClass}
                                placeholder="Class"
                              />

                              <button className="w-full rounded-xl bg-[#315bea] px-4 py-3 text-xs font-bold text-white">
                                ➕ Create Batch
                              </button>
                            </form>
                          </ManagementCard>
                        </div>

                        <div className="mt-5 grid gap-3 md:grid-cols-4">
                          <ActionButton
                            icon="👥"
                            title="Manage Students"
                          />

                          <ActionButton
                            icon="👨‍🏫"
                            title="Manage Teachers"
                          />

                          <ActionButton
                            icon="📚"
                            title="Manage Batches"
                          />

                          <ActionButton
                            icon="📝"
                            title="Tests & Papers"
                          />
                        </div>

                        <div className="mt-5 flex flex-wrap gap-3">
                          <button
                            onClick={() => updateAcademy(academy, { status: academy.status === "SUSPENDED" ? "ACTIVE" : "SUSPENDED" })}
                            className="rounded-xl border border-orange-200 bg-orange-50 px-4 py-2.5 text-xs font-bold text-orange-600"
                          >
                            {academy.status === "SUSPENDED" ? "▶️ Resume Academy" : "⏸️ Suspend Academy"}
                          </button>

                          <button
                            onClick={() => updateAcademy(academy, { status: academy.status === "RESTRICTED" ? "ACTIVE" : "RESTRICTED" })}
                            className="rounded-xl border border-red-200 bg-red-50 px-4 py-2.5 text-xs font-bold text-red-600"
                          >
                            {academy.status === "RESTRICTED" ? "🔓 Restore Access" : "🔒 Restrict Access"}
                          </button>

                          <button
                            onClick={() => {
                              const limit = window.prompt("Student limit", String(academy.student_limit ?? 10));
                              const end = window.prompt("Subscription end date (YYYY-MM-DD)", academy.subscription_end?.slice(0, 10) || "");
                              if (limit && end) updateAcademy(academy, { studentLimit: Number(limit), subscriptionEnd: end });
                            }}
                            className="rounded-xl border border-[#dfe4ed] bg-white px-4 py-2.5 text-xs font-bold text-[#697386]"
                          >
                            🎟️ Manage Subscription
                          </button>

                          <button
                            onClick={() => resetAcademyAdmin(academy)}
                            className="rounded-xl border border-blue-200 bg-blue-50 px-4 py-2.5 text-xs font-bold text-[#315bea]"
                          >
                            🔑 Reset Admin Password
                          </button>
                        </div>

                        <AcademyDetails
                          key={`${academy.id}-${detailsVersion}`}
                          academyId={academy.id}
                        />
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}

function AcademyDetails({ academyId }: { academyId: string }) {
  const [details, setDetails] =
    useState<AcademyDetailsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function downloadPaper(paperId: string, paperCode: string) {
    const response = await fetch(
      `/api/admin/academies/${academyId}/papers/${paperId}/download`
    );

    if (!response.ok) {
      setError("Unable to download this paper.");
      return;
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${paperCode || "paper"}.json`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }

  useEffect(() => {
    let active = true;

    async function loadDetails() {
      setLoading(true);
      setError("");

      try {
        const response = await fetch(
          `/api/admin/academies/${academyId}/details`,
          { cache: "no-store" }
        );
        const data = await response.json();

        if (!response.ok || !data.success) {
          throw new Error(
            data.error || "Failed to load academy details."
          );
        }

        if (active) setDetails(data);
      } catch (loadError) {
        if (active) {
          setError(
            loadError instanceof Error
              ? loadError.message
              : "Failed to load academy details."
          );
        }
      } finally {
        if (active) setLoading(false);
      }
    }

    loadDetails();

    return () => {
      active = false;
    };
  }, [academyId]);

  if (loading) {
    return (
      <div className="mt-6 rounded-2xl border border-[#e3e8f5] bg-[#fafbfe] p-5 text-sm text-[#697386]">
        Loading full academy details...
      </div>
    );
  }

  if (error || !details) {
    return (
      <div className="mt-6 rounded-2xl border border-red-100 bg-red-50 p-5 text-sm font-semibold text-red-600">
        {error || "No academy details found."}
      </div>
    );
  }

  return (
    <section className="mt-6 rounded-2xl border border-[#dfe4ed] bg-[#f8faff] p-5">
      <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
        <div>
          <h5 className="text-lg font-extrabold">
            Full Academy Details
          </h5>
          <p className="mt-1 text-xs text-[#697386]">
            Students, teachers, batches, papers, schedules and every linked question.
          </p>
        </div>
        <div className="text-right text-xs font-bold text-[#697386]">
          <div>{details.students.length} students</div>
          <div>{details.teachers.length} teachers</div>
          <div>{details.papers.length} papers</div>
        </div>
      </div>

      <div className="grid gap-4 xl:grid-cols-2">
        <DetailGroup title="Students">
          {details.students.length === 0 ? (
            <EmptyDetail />
          ) : (
            details.students.map((student) => (
              <DetailRow
                key={String(student.id)}
                title={String(student.name ?? "Unnamed student")}
                lines={[
                  `Username: ${String(student.email ?? "-")}`,
                  `Roll: ${String(student.roll_number ?? "-")} · Class: ${String(student.class_name ?? "-")}`,
                  `Password: ${student.has_password ? "Set securely (cannot be displayed)" : "Not set"}`,
                  `Created: ${formatDetailDate(student.created_at)}`,
                ]}
              />
            ))
          )}
        </DetailGroup>

        <DetailGroup title="Teachers">
          {details.teachers.length === 0 ? (
            <EmptyDetail />
          ) : (
            details.teachers.map((teacher) => (
              <DetailRow
                key={String(teacher.id)}
                title={String(teacher.name ?? "Unnamed teacher")}
                lines={[
                  `Username: ${String(teacher.email ?? "-")}`,
                  `Password: ${teacher.has_password ? "Set securely (cannot be displayed)" : "Not set"}`,
                  `Created: ${formatDetailDate(teacher.created_at)}`,
                ]}
              />
            ))
          )}
        </DetailGroup>

        <DetailGroup title="Batches">
          {details.batches.length === 0 ? (
            <EmptyDetail />
          ) : (
            details.batches.map((batch) => (
              <DetailRow
                key={String(batch.id)}
                title={String(batch.name ?? "Unnamed batch")}
                lines={[
                  `Class: ${String(batch.class_name ?? "-")}`,
                  `Students: ${String(batch.student_count ?? 0)}`,
                  `Created: ${formatDetailDate(batch.created_at)}`,
                ]}
              />
            ))
          )}
        </DetailGroup>

        <DetailGroup title="Scheduled Tests">
          {details.scheduledTests.length === 0 ? (
            <EmptyDetail />
          ) : (
            details.scheduledTests.map((test) => (
              <DetailRow
                key={String(test.id)}
                title={String(test.title ?? "Untitled test")}
                lines={[
                  `Status: ${String(test.status ?? "-")}`,
                  `Paper: ${String(test.paper_code ?? "-")} · Batch: ${String(test.batch_name ?? "Individual")}`,
                  `Start: ${formatDetailDate(test.start_time)} · End: ${formatDetailDate(test.end_time)}`,
                  `Duration: ${String(test.duration_minutes ?? 0)} minutes`,
                ]}
              />
            ))
          )}
        </DetailGroup>
      </div>

      <div className="mt-4">
        <DetailGroup title="Papers and Questions">
          {details.papers.length === 0 ? (
            <EmptyDetail />
          ) : (
            details.papers.map((paper) => {
              const paperQuestions = details.questions.filter(
                (question) => question.paper_id === paper.id
              );

              return (
                <details
                  key={String(paper.id)}
                  className="border-b border-[#e8ecf4] py-3 last:border-b-0"
                >
                  <summary className="cursor-pointer list-none text-sm font-extrabold text-[#172033]">
                    {String(paper.code ?? "Paper")} · {String(paper.description ?? "Untitled")}
                    <span className="ml-2 text-xs font-semibold text-[#697386]">
                      {paperQuestions.length} questions · {String(paper.exam ?? "-")} · {String(paper.status ?? "-")}
                    </span>
                  </summary>

                  <div className="mt-2 flex flex-wrap items-center justify-between gap-2">
                    <p className="text-xs text-[#697386]">
                      Created by: {String(paper.creator_name ?? paper.creator_email ?? "Unknown teacher")}
                    </p>
                    <button
                      type="button"
                      onClick={() =>
                        downloadPaper(
                          String(paper.id),
                          String(paper.code ?? "paper")
                        )
                      }
                      className="rounded-lg border border-[#315bea] px-3 py-1.5 text-xs font-bold text-[#315bea] hover:bg-[#f1f4ff]"
                    >
                      Download JSON
                    </button>
                  </div>

                  <div className="mt-3 space-y-3">
                    {paperQuestions.length === 0 ? (
                      <EmptyDetail />
                    ) : (
                      paperQuestions.map((question, index) => (
                        <div
                          key={`${String(question.id)}-${index}`}
                          className="rounded-xl border border-[#e3e8f5] bg-white p-4"
                        >
                          <div className="flex flex-wrap justify-between gap-2 text-[11px] font-bold text-[#315bea]">
                            <span>Question {String(question.question_order ?? index + 1)}</span>
                            <span>{String(question.subject ?? "-")} · {String(question.chapter_name ?? "-")} · {String(question.difficulty ?? "-")}</span>
                          </div>
                          <p className="mt-2 whitespace-pre-wrap text-sm font-semibold text-[#172033]">
                            {String(question.stem ?? "Question text unavailable")}
                          </p>
                          <p className="mt-2 text-xs text-[#697386]">
                            Options: {formatQuestionOptions(question.options)}
                          </p>
                          <p className="mt-1 text-xs font-bold text-green-700">
                            Correct answer: {String(question.correct_option ?? "-")}
                          </p>
                          {question.solution ? (
                            <p className="mt-2 whitespace-pre-wrap text-xs leading-5 text-[#697386]">
                              Solution: {String(question.solution)}
                            </p>
                          ) : null}
                        </div>
                      ))
                    )}
                  </div>
                </details>
              );
            })
          )}
        </DetailGroup>
      </div>
    </section>
  );
}

function DetailGroup({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded-xl border border-[#e3e8f5] bg-white p-4">
      <h6 className="mb-2 text-sm font-extrabold">{title}</h6>
      {children}
    </div>
  );
}

function DetailRow({
  title,
  lines,
}: {
  title: string;
  lines: string[];
}) {
  return (
    <div className="border-b border-[#eef0f4] py-3 last:border-b-0">
      <p className="text-sm font-bold">{title}</p>
      {lines.map((line) => (
        <p key={line} className="mt-1 text-xs text-[#697386]">
          {line}
        </p>
      ))}
    </div>
  );
}

function EmptyDetail() {
  return <p className="py-3 text-xs text-[#929aaa]">No records found.</p>;
}

function formatDetailDate(value: unknown) {
  if (!value) return "-";
  const date = new Date(String(value));
  return Number.isNaN(date.getTime())
    ? String(value)
    : date.toLocaleString();
}

function formatQuestionOptions(value: unknown) {
  if (!value) return "-";
  if (typeof value === "string") return value;

  try {
    return JSON.stringify(value);
  } catch {
    return "Unavailable";
  }
}

function Input({
  value,
  onChange,
  placeholder,
  type = "text",
}: {
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
  type?: string;
}) {
  return (
    <input
      type={type}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      required
      className="w-full rounded-xl border border-[#dfe4ed] bg-white px-4 py-3 text-sm outline-none transition focus:border-[#315bea]"
    />
  );
}

function Stat({
  title,
  value,
  icon,
}: {
  title: string;
  value: string | number;
  icon: string;
}) {
  return (
    <div className="rounded-2xl border border-[#e3e8f5] bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <p className="text-xs font-bold text-[#929aaa]">
          {title}
        </p>

        <span className="text-lg">{icon}</span>
      </div>

      <p className="mt-2 text-2xl font-extrabold">
        {value}
      </p>
    </div>
  );
}

function MiniStat({
  label,
  value,
  icon,
}: {
  label: string;
  value: string | number;
  icon: string;
}) {
  return (
    <div className="rounded-xl bg-[#f7f9fc] p-3">
      <p className="text-[10px] font-bold text-[#929aaa]">
        {icon} {label}
      </p>

      <p className="mt-1 text-sm font-extrabold">
        {value}
      </p>
    </div>
  );
}

function ManagementCard({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded-2xl border border-[#e3e8f5] bg-[#fafbfe] p-5">
      <h6 className="font-extrabold">{title}</h6>

      <p className="mb-4 mt-1 text-[11px] leading-5 text-[#697386]">
        {description}
      </p>

      {children}
    </div>
  );
}

function ActionButton({
  icon,
  title,
}: {
  icon: string;
  title: string;
}) {
  return (
    <button className="rounded-xl border border-[#e3e8f5] bg-white px-4 py-3 text-left text-xs font-bold transition hover:border-[#315bea]">
      <span className="mr-2">{icon}</span>
      {title}
    </button>
  );
}