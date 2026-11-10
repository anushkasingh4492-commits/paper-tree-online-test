"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import AcademyBranding from "@/components/AcademyBranding";
import { Icon } from "@/components/Icon";

export default function Home() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();

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
        }),
      });

      const contentType =
        response.headers.get("content-type") || "";

      const text = await response.text();

      let result: any;

      if (contentType.includes("application/json")) {
        try {
          result = JSON.parse(text);
        } catch {
          throw new Error(
            "Login API returned invalid JSON."
          );
        }
      } else {
        console.error(
          "Login API returned non-JSON:",
          text.slice(0, 500)
        );

        throw new Error(
          `Login failed: ${response.status} ${response.statusText}`
        );
      }

      if (!response.ok || !result.success) {
        setError(
          result?.error ||
            "Invalid email or password."
        );
        return;
      }

      const loggedInStudent =
        result.user ||
        result.student;

      if (loggedInStudent?.id) {
        localStorage.setItem(
          "studentId",
          String(loggedInStudent.id)
        );
      }

      if (loggedInStudent?.name) {
        localStorage.setItem(
          "studentName",
          loggedInStudent.name
        );
      }

      window.location.replace("/dashboard");
      return;
    } catch (error) {
      console.error("LOGIN ERROR:", error);

      setError(
        error instanceof Error
          ? error.message
          : "Unable to connect to the server. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-surface-app-bg text-text-primary">
      <div className="flex min-h-screen w-full">

        {/* LEFT BRAND PANEL */}
        <section className="hidden lg:flex lg:w-[52%] bg-brand-primary relative overflow-hidden">

          <div className="absolute -right-32 -top-32 h-[500px] w-[500px] rounded-full border-[70px] border-white/[0.06]" />
          <div className="absolute -bottom-40 -left-20 h-[420px] w-[420px] rounded-full bg-white/[0.05]" />
          <div className="absolute top-1/3 left-1/4 h-[300px] w-[300px] bg-indigo-500/20 blur-[100px] rounded-full" />

          <div className="relative flex w-full flex-col justify-between p-14">

            <AcademyBranding
              variant="login"
              className="text-white"
            />

            <div className="relative max-w-[560px]">

              <div className="mb-8">
                <img
                  src="/images/login/Glossy Neon Checklist Scroll.png"
                  alt="Student dashboard"
                  className="w-full h-auto block mx-auto drop-shadow-2xl"
                  loading="lazy"
                />
              </div>

              <div className="space-y-3">
                <h2 className="text-3xl font-extrabold text-white tracking-tight">
                  Welcome back
                </h2>
                <p className="text-indigo-100 text-lg">
                  Sign in to access your performance dashboard,<br />
                  badges, streak, and upcoming tests.
                </p>
              </div>

            </div>

          </div>

        </section>

        {/* RIGHT FORM PANEL */}
        <main className="flex-1 w-full min-w-0 bg-surface-app-bg">

          <div className="flex items-center justify-center px-6 py-12 lg:py-20">

            <form
              onSubmit={handleSubmit}
              className="w-full max-w-md space-y-6"
            >

              <div className="text-center">
                <h1 className="text-2xl font-extrabold text-text-primary">
                  Sign in to CBT
                </h1>
                <p className="mt-1 text-text-body">
                  Enter your student credentials below
                </p>
              </div>

              {error && (
                <div className="rounded-xl border border-state-error/20 bg-state-error/10 px-4 py-3 text-sm font-medium text-state-error">
                  {error}
                </div>
              )}

              <div className="space-y-2">
                <label
                  htmlFor="email"
                  className="block text-xs font-bold text-text-tertiary uppercase tracking-wider"
                >
                  Email address
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  autoComplete="email"
                  required
                  disabled={loading}
                  className="h-12 w-full rounded-xl border border-border-default bg-surface-surface px-4 text-sm text-text-primary outline-none transition placeholder:text-text-supporting-label focus:border-brand-primary focus:ring-4 focus:ring-brand-primary/10 disabled:bg-surface-app-bg"
                />
              </div>

              <div className="space-y-2">
                <div className="mb-2 flex items-center justify-between">
                  <label
                    htmlFor="password"
                    className="block text-xs font-bold text-text-tertiary uppercase tracking-wider"
                  >
                    Password
                  </label>
                  <span className="text-[10px] font-medium text-text-body">
                    Secure login
                  </span>
                </div>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  required
                  disabled={loading}
                  className="h-12 w-full rounded-xl border border-border-default bg-surface-surface px-4 text-sm text-text-primary outline-none transition placeholder:text-text-supporting-label focus:border-brand-primary focus:ring-4 focus:ring-brand-primary/10 disabled:bg-surface-app-bg"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="mt-2 flex h-12 w-full items-center justify-center rounded-xl bg-brand-primary text-sm font-bold text-white shadow-[0_8px_20px_rgba(36,85,200,0.18)] transition-all duration-200 hover:bg-brand-action-blue active:bg-brand-deep-navy disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? "Signing in..." : "Sign in"}
              </button>

              <button
                type="button"
                onClick={() => router.push("/change-password")}
                className="w-full rounded-xl border border-border-default bg-brand-subtle-lavender px-4 py-3 text-sm font-bold text-brand-primary transition-all duration-200 hover:bg-brand-action-blue hover:text-white active:bg-brand-deep-navy active:text-white"
              >
                <Icon name="lock" size={14} className="text-brand-primary" /> Change Password
              </button>

            </form>

            <div className="mt-6">
              <button
                type="button"
                onClick={() => router.push("/master-login")}
                className="w-full rounded-xl border border-border-default bg-brand-subtle-lavender px-4 py-3 text-sm font-bold text-brand-primary transition-all duration-200 hover:bg-brand-action-blue hover:text-white active:bg-brand-deep-navy active:text-white"
              >
                Teacher / Admin Login
              </button>
            </div>

            <div className="mt-8 text-center">
              <p className="text-[11px] leading-5 text-text-body">
                Competitive Exam Preparation Platform
              </p>
              <p className="mt-1 text-[10px] text-text-disabled">
                Your account is secured with encrypted authentication.
              </p>
            </div>

          </div>

        </main>
      </div>
    </main>
  );
}
