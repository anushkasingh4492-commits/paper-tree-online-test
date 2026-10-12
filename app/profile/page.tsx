"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AcademyBranding from "@/components/AcademyBranding";
import StudentAccountMenu from "@/components/StudentAccountMenu";

type Student = {
  id?: string;
  name?: string;
  rollNumber?: string | null;
  email?: string | null;
};

type Payload = {
  success?: boolean;
  student?: Student;
  error?: string;
};

export default function ProfilePage() {
  const router = useRouter();
  const [data, setData] = useState<Payload | null>(null);
  const [name, setName] = useState("");
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  useEffect(() => {
    fetch("/api/dashboard", {
      cache: "no-store",
      credentials: "include",
    })
      .then(async (response) => {
        const value = await response.json();
        if (!response.ok || value.success === false) {
          throw new Error(value.error || "Unable to load your profile.");
        }
        setData(value);
        setName(value.student?.name || "");
      })
      .catch((e) =>
        setError(e instanceof Error ? e.message : "Unable to load your profile.")
      )
      .finally(() => setLoading(false));
  }, []);

  const student = data?.student;

  async function saveProfile() {
    setError("");
    setNotice("");

    const cleanName = name.trim();
    if (cleanName.length < 2 || cleanName.length > 100) {
      setError("Name must be between 2 and 100 characters.");
      return;
    }

    setSaving(true);
    try {
      const response = await fetch("/api/account/profile", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ name: cleanName }),
      });
      const result: Payload = await response.json();

      if (!response.ok || !result.success || !result.student) {
        throw new Error(result.error || "Could not update your profile.");
      }

      setData((previous) => ({
        ...previous,
        student: result.student,
      }));
      setName(result.student.name || cleanName);
      setEditing(false);
      setNotice("Profile updated successfully.");

      try {
        localStorage.setItem("studentName", result.student.name || cleanName);
      } catch {
        // The database update has succeeded even if browser storage is unavailable.
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not update your profile.");
    } finally {
      setSaving(false);
    }
  }

  function cancelEditing() {
    setName(student?.name || "");
    setEditing(false);
    setError("");
    setNotice("");
  }

  return (
    <main className="min-h-screen bg-[#f8f9fc] text-slate-900">
      <header className="flex h-[72px] items-center justify-between border-b border-slate-200 bg-white px-5 lg:px-8">
        <AcademyBranding variant="compact" />
        <StudentAccountMenu studentName={student?.name || "Student"} />
      </header>

      <div className="mx-auto max-w-3xl p-5 lg:p-8">
        <button
          onClick={() => router.push("/dashboard")}
          className="text-xs font-bold text-indigo-600"
        >
          ← Dashboard
        </button>

        <div className="mt-5 flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="text-3xl font-black">My Profile</h1>
            <p className="mt-1 text-sm text-slate-500">
              View and manage your student account details.
            </p>
          </div>

          {!loading && student && !editing && (
            <button
              onClick={() => {
                setName(student.name || "");
                setEditing(true);
                setError("");
                setNotice("");
              }}
              className="rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-bold text-white hover:bg-indigo-700"
            >
              Edit Profile
            </button>
          )}
        </div>

        {error && (
          <div role="alert" className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            {error}
          </div>
        )}

        {notice && (
          <div role="status" className="mt-6 rounded-xl border border-green-200 bg-green-50 p-4 text-sm text-green-700">
            {notice}
          </div>
        )}

        {loading ? (
          <div className="mt-7 rounded-2xl border border-slate-200 bg-white p-8 text-center text-sm text-slate-500">
            Loading your profile…
          </div>
        ) : student ? (
          <>
            <div className="mt-7 grid gap-4 sm:grid-cols-2">
              {editing ? (
                <div className="rounded-2xl border border-indigo-200 bg-white p-5 shadow-sm sm:col-span-2">
                  <label htmlFor="profile-name" className="text-[10px] font-black uppercase tracking-wider text-slate-400">
                    Full name
                  </label>
                  <input
                    id="profile-name"
                    value={name}
                    onChange={(event) => setName(event.target.value)}
                    maxLength={100}
                    autoComplete="name"
                    className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 text-base font-semibold outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
                  />
                  <p className="mt-2 text-xs text-slate-500">
                    Your student ID, roll number, and email cannot be changed here.
                  </p>
                </div>
              ) : (
                <Info label="Name" value={student.name || "—"} />
              )}
              <Info label="Student ID" value={student.id || "—"} />
              <Info label="Roll Number" value={student.rollNumber || "—"} />
              <Info label="Email" value={student.email || "—"} />
            </div>

            {editing && (
              <div className="mt-5 flex flex-wrap justify-end gap-3">
                <button
                  onClick={cancelEditing}
                  disabled={saving}
                  className="rounded-xl border border-slate-300 bg-white px-5 py-2.5 text-sm font-bold text-slate-700 disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  onClick={saveProfile}
                  disabled={saving}
                  className="rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-bold text-white hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {saving ? "Saving…" : "Save Changes"}
                </button>
              </div>
            )}
          </>
        ) : (
          <div className="mt-7 rounded-2xl border border-slate-200 bg-white p-8 text-center text-sm text-slate-500">
            Profile details are unavailable.
          </div>
        )}
      </div>
    </main>
  );
}

function Info({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="text-[10px] font-black uppercase tracking-wider text-slate-400">
        {label}
      </div>
      <div className="mt-2 break-words text-base font-black text-slate-800">
        {value}
      </div>
    </div>
  );
}
