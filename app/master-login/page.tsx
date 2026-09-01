"use client";

import { FormEvent, Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
function MasterLoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const requestedRole = searchParams.get("role");

  const role =
    requestedRole === "ADMIN" ? "ADMIN" : "TEACHER";

  const isAdmin = role === "ADMIN";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function login(event: FormEvent) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const response = await fetch("/api/auth/master-login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(
          result.error || "Invalid email or password."
        );
      }

      // Make sure the account matches the portal
      if (result.role !== role) {
        throw new Error(
          `This account is not an ${isAdmin ? "Admin" : "Teacher"} account.`
        );
      }

      if (result.role === "ADMIN") {
        router.replace("/admin");
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
    <main className="flex min-h-screen items-center justify-center bg-[#f6f8fc] px-6">

      <div className="w-full max-w-md">

        {/* BRAND */}

        <div className="mb-8 text-center">

          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-[#315bea] text-2xl font-extrabold text-white">
            P
          </div>

          <h1 className="text-2xl font-extrabold text-[#172033]">
            Paper Tree
          </h1>

          <p className="mt-1 text-sm text-[#697386]">
            {isAdmin
              ? "Admin Portal"
              : "Teacher Portal"}
          </p>

        </div>

        {/* LOGIN CARD */}

        <div className="rounded-3xl border border-[#e8ebf1] bg-white p-8 shadow-sm">

          <div className="mb-7">

            <p className="text-xs font-bold uppercase tracking-[0.15em] text-[#315bea]">
              {isAdmin ? "ADMIN LOGIN" : "TEACHER LOGIN"}
            </p>

            <h2 className="mt-2 text-2xl font-extrabold text-[#172033]">
              {isAdmin
                ? "Welcome, Admin"
                : "Welcome, Teacher"}
            </h2>

            <p className="mt-2 text-sm text-[#697386]">
              Sign in to access your{" "}
              {isAdmin ? "admin" : "teacher"} dashboard.
            </p>

          </div>

          <form
            onSubmit={login}
            className="space-y-5"
          >

            {/* EMAIL */}

            <div>

              <label className="mb-2 block text-sm font-semibold text-[#263044]">
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
                className="h-12 w-full rounded-xl border border-[#dfe3eb] px-4 text-sm outline-none transition focus:border-[#315bea] focus:ring-4 focus:ring-[#315bea]/10 disabled:bg-[#f7f8fb]"
              />

            </div>

            {/* PASSWORD */}

            <div>

              <label className="mb-2 block text-sm font-semibold text-[#263044]">
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
                className="h-12 w-full rounded-xl border border-[#dfe3eb] px-4 text-sm outline-none transition focus:border-[#315bea] focus:ring-4 focus:ring-[#315bea]/10 disabled:bg-[#f7f8fb]"
              />

            </div>

            {/* ERROR */}

            {error && (
              <div className="rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
                {error}
              </div>
            )}

            {/* BUTTON */}

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-xl bg-[#315bea] px-4 py-3 font-bold text-white transition hover:bg-[#264ac7] disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading
                ? "Signing in..."
                : `Sign in as ${isAdmin ? "Admin" : "Teacher"}`}
            </button>

          </form>

          {/* BACK */}

          <button
            type="button"
            onClick={() => router.push("/")}
            className="mt-5 w-full text-center text-sm font-semibold text-[#697386] hover:text-[#315bea]"
          >
            ← Back to portal selection
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
        <main className="flex min-h-screen items-center justify-center bg-[#f6f8fc]">
          <p className="text-sm text-[#697386]">
            Loading...
          </p>
        </main>
      }
    >
      <MasterLoginForm />
    </Suspense>
  );
}