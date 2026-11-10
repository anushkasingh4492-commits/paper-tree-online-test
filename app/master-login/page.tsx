"use client";

import { FormEvent, Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Icon } from "@/components/Icon";

function MasterLoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const requestedRole = searchParams.get("role");

  const role =
    requestedRole === "ADMIN" || requestedRole === "TEACHER"
      ? requestedRole
      : null;

  const isAdmin = role === "ADMIN";
  const isTeacher = role === "TEACHER";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function login(event: FormEvent) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          email,
          password,
          portalRole: role ?? "STAFF",
        }),
      });

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(
          result.error || "Invalid email or password."
        );
      }

      const validPortalRole = role === null
        ? ["ADMIN", "ACADEMY_ADMIN", "TEACHER"].includes(result.role)
        : role === "ADMIN"
          ? result.role === "ADMIN" || result.role === "ACADEMY_ADMIN"
          : result.role === "TEACHER";

      if (!validPortalRole) {
        throw new Error(
          `This account is not an ${isAdmin ? "Admin" : "Teacher"} account.`
        );
      }

      if (result.role === "ADMIN") {
        router.replace("/admin");
      } else if (result.role === "ACADEMY_ADMIN") {
        router.replace("/academy-admin");
      } else if (result.role === "TEACHER") {
        router.replace("/teacher");
      }
    } catch (err) {
      console.error("MASTER LOGIN ERROR:", err);

      setError(
        err instanceof Error
          ? err.message
          : "Login failed."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-surface-app-bg text-text-primary flex items-center justify-center px-6">

      <div className="w-full max-w-md bg-white/50 backdrop-blur-sm rounded-3xl border border-white/20 p-8 shadow-2xl relative overflow-hidden">

        {/* Decorative glow */}
        <div className="absolute -top-20 -right-20 h-[300px] w-[300px] rounded-full bg-brand-primary/20 blur-[100px]" />
        <div className="absolute -bottom-10 -left-10 h-[200px] w-[200px] rounded-full bg-purple-500/20 blur-[80px]" />

        {/* Illustration */}
        <div className="mb-6 relative z-10">
          <img
            src="/images/login/Glossy Purple Trophy with Stars.png"
            alt="Trophy"
            className="w-24 h-24 mx-auto drop-shadow-lg"
            loading="lazy"
          />
        </div>

        {/* BRAND */}
        <div className="mb-6 text-center relative z-10">

          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-primary text-2xl font-extrabold text-white shadow-lg">
            P
          </div>

          <h1 className="text-2xl font-extrabold text-text-primary">
            Paper Tree Educational Studio
          </h1>

          <p className="mt-1 text-sm text-text-tertiary">
            {isAdmin ? "Admin Portal" : isTeacher ? "Teacher Portal" : "Staff Portal"}
          </p>

        </div>

        {/* LOGIN CARD */}
        <div className="rounded-2xl border border-white/30 bg-white/80 backdrop-blur-md p-6 shadow-xl relative z-10">

          <div className="mb-6">

            <p className="text-xs font-bold uppercase tracking-[0.15em] text-brand-primary">
              {isAdmin ? "ADMIN LOGIN" : isTeacher ? "TEACHER LOGIN" : "STAFF LOGIN"}
            </p>

            <h2 className="mt-2 text-xl font-extrabold text-text-primary">
              Sign in to your portal
            </h2>

          </div>

          <form
            onSubmit={login}
            className="space-y-4"
          >

            <div className="space-y-2">

              <label className="mb-1 block text-xs font-semibold text-text-primary">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) =>
                  setEmail(e.target.value)
                }
                placeholder="Enter email"
                autoComplete="email"
                disabled={loading}
                required
                className="h-11 w-full rounded-xl border border-border-default bg-white px-4 text-sm outline-none transition focus:border-brand-primary focus:ring-4 focus:ring-brand-primary/10 disabled:bg-surface-app-bg"
              />

            </div>

            <div className="space-y-2">

              <label className="mb-1 block text-xs font-semibold text-text-primary">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) =>
                  setPassword(e.target.value)
                }
                placeholder="Enter password"
                autoComplete="current-password"
                disabled={loading}
                required
                className="h-11 w-full rounded-xl border border-border-default bg-white px-4 text-sm outline-none transition focus:border-brand-primary focus:ring-4 focus:ring-brand-primary/10 disabled:bg-surface-app-bg"
              />

            </div>

            {error && (
              <div className="rounded-xl border border-state-error/20 bg-state-error/10 px-4 py-3 text-sm font-medium text-state-error">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-xl bg-brand-primary px-4 py-3 font-bold text-white transition hover:bg-brand-action-blue disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading
                ? "Signing in..."
                : role ? `Sign in as ${isAdmin ? "Admin" : "Teacher"}` : "Sign in"}
            </button>
            <button
              type="button"
              onClick={() => router.push("/change-password")}
              className="mt-3 w-full rounded-xl border border-border-default bg-white px-4 py-3 text-sm font-bold text-brand-primary transition hover:bg-surface-subtle"
            >
              <Icon name="lock" size={14} className="text-brand-primary" /> Change Password
            </button>

          </form>

          {/* BACK */}
          <button
            type="button"
            onClick={() => router.push("/login")}
            className="mt-5 w-full text-center text-sm font-semibold text-text-tertiary hover:text-brand-primary"
          >
            ← Back to Login
          </button>

        </div>

      </div>

    </main>
  );
}

export default function MasterLoginPage() {
  return (
    <Suspense
      fallback={
        <main className="flex min-h-screen items-center justify-center bg-surface-app-bg">
          <p className="text-sm text-text-tertiary">
            Loading...
          </p>
        </main>
      }
    >
      <MasterLoginForm />
    </Suspense>
  );
}
