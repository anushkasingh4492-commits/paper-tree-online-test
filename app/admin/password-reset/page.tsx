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
    <main className="min-h-screen bg-surface-app-bg text-text-primary">
      <header className="border-b border-border-default bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-xl font-extrabold">
              🔐 Password Management
            </h1>

            <p className="mt-1 text-xs text-text-body">
              Master Admin
            </p>
          </div>

          <button
            onClick={() =>
              router.push("/admin")
            }
            className="rounded-xl border border-border-default bg-white px-4 py-2.5 text-sm font-bold text-text-tertiary hover:bg-surface-app-bg"
          >
            ← Admin
          </button>
        </div>
      </header>

      <div className="mx-auto max-w-2xl px-6 py-10">
        <section className="rounded-3xl border border-border-default bg-surface-surface p-7 shadow-sm">
          <h2 className="text-xl font-extrabold">
            Reset Student / Teacher Password
          </h2>

          <p className="mt-2 text-sm text-text-tertiary">
            You can reset an account password without
            knowing the user's current password.
          </p>

          {error && (
            <div className="mt-5 rounded-xl border border-state-error/20 bg-state-error/10 px-4 py-3 text-sm font-medium text-state-error">
              {error}
            </div>
          )}

          {message && (
            <div className="mt-5 rounded-xl border border-state-success/20 bg-state-success/10 px-4 py-3 text-sm font-medium text-state-success">
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
                  ? "border-brand-primary bg-brand-primary/10 text-brand-primary"
                  : "border-border-default text-text-tertiary"
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
                  ? "border-brand-primary bg-brand-primary/10 text-brand-primary"
                  : "border-border-default text-text-tertiary"
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
            className="mt-2 h-12 w-full rounded-xl border border-border-default bg-white px-4 text-sm outline-none focus:border-brand-primary"
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
            className="mt-2 h-12 w-full rounded-xl border border-border-default px-4 text-sm outline-none focus:border-brand-primary"
          />

          <button
            onClick={resetPassword}
            disabled={resetting || loading}
            className="mt-7 w-full rounded-xl bg-brand-primary px-4 py-3 font-bold text-white hover:bg-brand-primary disabled:opacity-60"
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