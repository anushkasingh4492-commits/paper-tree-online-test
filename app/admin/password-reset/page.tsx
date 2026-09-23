"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type Account = {
  id: string;
  name: string;
  email: string;
  academy_name?: string | null;
  class_name?: string | null;
};

export default function AdminPasswordResetPage() {
  const router = useRouter();

  const [teachers, setTeachers] =
    useState<Account[]>([]);

  const [students, setStudents] =
    useState<Account[]>([]);

  const [type, setType] =
    useState<"TEACHER" | "STUDENT">(
      "STUDENT"
    );

  const [userId, setUserId] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [loading, setLoading] =
    useState(true);

  const [resetting, setResetting] =
    useState(false);

  const [error, setError] =
    useState("");

  const [message, setMessage] =
    useState("");

  useEffect(() => {
    async function load() {
      try {
        const response = await fetch(
          "/api/admin/password-reset",
          {
            credentials: "include",
            cache: "no-store",
          }
        );

        const result =
          await response.json();

        if (
          !response.ok ||
          !result.success
        ) {
          throw new Error(
            result.error ||
              "Failed to load accounts."
          );
        }

        setTeachers(
          result.teachers || []
        );

        setStudents(
          result.students || []
        );
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load accounts."
        );
      } finally {
        setLoading(false);
      }
    }

    void load();
  }, []);

  const accounts =
    type === "TEACHER"
      ? teachers
      : students;

  async function resetPassword() {
    setError("");
    setMessage("");

    if (!userId) {
      setError("Select an account.");
      return;
    }

    if (password.length < 8) {
      setError(
        "Password must be at least 8 characters long."
      );
      return;
    }

    if (
      !window.confirm(
        "Are you sure you want to reset this password?"
      )
    ) {
      return;
    }

    setResetting(true);

    try {
      const response = await fetch(
        "/api/admin/password-reset",
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          credentials: "include",
          body: JSON.stringify({
            userType: type,
            userId,
            newPassword: password,
          }),
        }
      );

      const result =
        await response.json();

      if (
        !response.ok ||
        !result.success
      ) {
        throw new Error(
          result.error ||
            "Failed to reset password."
        );
      }

      setMessage(result.message);
      setPassword("");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to reset password."
      );
    } finally {
      setResetting(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <header className="border-b border-[#e7eaf0] bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-xl font-extrabold">
              🔐 Password Management
            </h1>

            <p className="mt-1 text-xs text-[#8a93a5]">
              Master Admin
            </p>
          </div>

          <button
            onClick={() =>
              router.push("/admin")
            }
            className="rounded-xl border border-[#e2e6ee] bg-white px-4 py-2.5 text-sm font-bold text-[#697386] hover:bg-[#f8f9fb]"
          >
            ← Admin
          </button>
        </div>
      </header>

      <div className="mx-auto max-w-2xl px-6 py-10">
        <section className="rounded-3xl border border-[#e1e6f2] bg-white p-7 shadow-sm">
          <h2 className="text-xl font-extrabold">
            Reset Student / Teacher Password
          </h2>

          <p className="mt-2 text-sm text-[#697386]">
            You can reset an account password without
            knowing the user's current password.
          </p>

          {error && (
            <div className="mt-5 rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
              {error}
            </div>
          )}

          {message && (
            <div className="mt-5 rounded-xl border border-emerald-100 bg-emerald-50 px-4 py-3 text-sm font-medium text-emerald-600">
              {message}
            </div>
          )}

          <div className="mt-7 grid grid-cols-2 gap-3">
            <button
              onClick={() => {
                setType("STUDENT");
                setUserId("");
              }}
              className={`rounded-xl border-2 px-4 py-3 text-sm font-bold ${
                type === "STUDENT"
                  ? "border-[#315bea] bg-blue-50 text-[#315bea]"
                  : "border-[#e2e6ee] text-[#697386]"
              }`}
            >
              🎓 Student
            </button>

            <button
              onClick={() => {
                setType("TEACHER");
                setUserId("");
              }}
              className={`rounded-xl border-2 px-4 py-3 text-sm font-bold ${
                type === "TEACHER"
                  ? "border-[#315bea] bg-blue-50 text-[#315bea]"
                  : "border-[#e2e6ee] text-[#697386]"
              }`}
            >
              👨‍🏫 Teacher
            </button>
          </div>

          <label className="mt-6 block text-sm font-bold">
            Select account
          </label>

          <select
            value={userId}
            onChange={(e) =>
              setUserId(e.target.value)
            }
            disabled={loading}
            className="mt-2 h-12 w-full rounded-xl border border-[#dfe3eb] bg-white px-4 text-sm outline-none focus:border-[#315bea]"
          >
            <option value="">
              {loading
                ? "Loading accounts..."
                : "Select an account"}
            </option>

            {accounts.map((account) => (
              <option
                key={account.id}
                value={account.id}
              >
                {account.name} — {account.email}
                {account.academy_name
                  ? ` — ${account.academy_name}`
                  : ""}
              </option>
            ))}
          </select>

          <label className="mt-6 block text-sm font-bold">
            New password
          </label>

          <input
            type="password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            placeholder="Minimum 8 characters"
            minLength={8}
            className="mt-2 h-12 w-full rounded-xl border border-[#dfe3eb] px-4 text-sm outline-none focus:border-[#315bea]"
          />

          <button
            onClick={resetPassword}
            disabled={resetting || loading}
            className="mt-7 w-full rounded-xl bg-[#315bea] px-4 py-3 font-bold text-white hover:bg-[#264ac7] disabled:opacity-60"
          >
            {resetting
              ? "Resetting..."
              : "Reset Password"}
          </button>
        </section>
      </div>
    </main>
  );
}