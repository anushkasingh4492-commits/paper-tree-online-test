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
    <main
      className="min-h-screen w-full text-text-primary relative"
      style={{
        backgroundImage: "url('/images/login/Glossy Neon Checklist Scroll.png')",
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
        backgroundAttachment: "fixed",
      }}
    >
      {/* Full-screen overlay to soften the image and ensure text readability */}
      <div className="absolute inset-0 bg-black/30 backdrop-blur-sm z-0" />

      <div className="relative z-10 flex min-h-screen w-full">

        {/* LEFT BRAND PANEL */}
        <section className="hidden lg:flex lg:w-[52%] relative overflow-hidden">

          {/* Decorative glows on top of image */}
          <div className="absolute -right-32 -top-32 h-[500px] w-[500px] rounded-full border-[70px] border-white/[0.06]" />
          <div className="absolute -bottom-40 -left-20 h-[420px] w-[420px] rounded-full bg-white/[0.05]" />
          <div className="absolute top-1/3 left-1/4 h-[300px] w-[300px] bg-indigo-500/20 blur-[100px] rounded-full" />
          <div className="absolute bottom-1/4 right-1/6 h-[260px] w-[260px] bg-purple-500/20 blur-[90px] rounded-full" />

          <div className="relative flex w-full flex-col justify-between p-14">

            <AcademyBranding
              variant="login"
              className="text-white"
            />

            <div className="relative max-w-[560px]">

              {/* Hero illustration */}
              <div className="mb-8 relative">
                <img
                  src="/images/login/Glossy Neon Checklist Scroll.png"
                  alt="Student dashboard"
                  className="w-full h-auto block mx-auto drop-shadow-2xl relative z-10"
                  loading="lazy"
                  decoding="async"
                />
                <div className="absolute -inset-4 bg-white/20 rounded-[30px] blur-[40px]" />
              </div>

              <div className="space-y-3">
                <h2 className="text-3xl font-extrabold text-white tracking-tight leading-[1.15]">
                  Welcome back
                </h2>
                <p className="text-indigo-100 text-lg leading-relaxed">
                  Sign in to access your performance dashboard,<br className="hidden lg:block" />
                  badges, streak, and upcoming tests.
                </p>
              </div>

            </div>

          </div>

        </section>

        {/* RIGHT FORM PANEL */}
        <main className="flex-1 w-full min-w-0 bg-black/40 backdrop-blur-md">

          <div className="flex items-center justify-center px-6 py-12 lg:py-20">

            <form
              onSubmit={handleSubmit}
              className="w-full max-w-md space-y-6 bg-white/10 backdrop-blur-md rounded-3xl p-8 border border-white/20 shadow-2xl"
            >

              <div className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-white/20 text-white mb-4 shadow-lg shadow-black/30">
                  <span className="text-lg font-black">P</span>
                </div>
                <h1 className="text-2xl font-extrabold text-white tracking-tight">
                  Sign in to CBT
                </h1>
                <p className="mt-1 text-indigo-100">
                  Enter your student credentials below
                </p>
              </div>

              {error && (
                <div className="rounded-xl border border-red-500/50 bg-red-500/10 px-4 py-3 text-sm font-medium text-red-100 flex items-center gap-2">
                  <Icon name="alert" size={16} className="text-red-400" />
                  {error}
                </div>
              )}

              {/* EMAIL */}
              <div className="space-y-2">
                <label
                  htmlFor="email"
                  className="block text-xs font-bold text-indigo-200 uppercase tracking-wider"
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
                  className="h-12 w-full rounded-xl border border-white/30 bg-white/10 px-4 text-sm text-white outline-none transition placeholder:text-indigo-300 focus:border-indigo-400 focus:ring-4 focus:ring-indigo-500/20 disabled:bg-white/5"
                />
              </div>

              {/* PASSWORD */}
              <div className="space-y-2">
                <div className="mb-2 flex items-center justify-between">
                  <label
                    htmlFor="password"
                    className="block text-xs font-bold text-indigo-200 uppercase tracking-wider"
                  >
                    Password
                  </label>
                  <span className="text-[10px] font-medium text-indigo-300">
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
                  className="h-12 w-full rounded-xl border border-white/30 bg-white/10 px-4 text-sm text-white outline-none transition placeholder:text-indigo-300 focus:border-indigo-400 focus:ring-4 focus:ring-indigo-500/20 disabled:bg-white/5"
                />
              </div>

              {/* LOGIN BUTTON */}
              <button
                type="submit"
                disabled={loading}
                className="mt-2 flex h-12 w-full items-center justify-center rounded-xl bg-indigo-600 text-sm font-bold text-white shadow-[0_8px_20px_rgba(79,70,229,0.35)] transition-all duration-200 hover:bg-indigo-500 active:bg-indigo-700 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? (
                  <span className="flex items-center gap-2">
                    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Signing in...
                  </span>
                ) : "Sign in"}
              </button>

              <button
                type="button"
                onClick={() => router.push("/change-password")}
                className="w-full rounded-xl border border-white/30 bg-white/10 px-4 py-3 text-sm font-bold text-indigo-100 transition-all duration-200 hover:bg-white/20 hover:text-white active:bg-white/30 flex items-center justify-center gap-2"
              >
                <Icon name="lock" size={14} className="text-indigo-300" /> Change Password
              </button>

            </form>

            {/* STAFF LOGIN */}
            <div className="mt-6">
              <button
                type="button"
                onClick={() => router.push("/master-login")}
                className="w-full rounded-xl border border-white/30 bg-white/10 px-4 py-3 text-sm font-bold text-indigo-100 transition-all duration-200 hover:bg-white/20 hover:text-white active:bg-white/30"
              >
                Teacher / Admin Login
              </button>
            </div>

            <div className="mt-8 text-center">
              <p className="text-[11px] leading-5 text-indigo-200">
                Competitive Exam Preparation Platform
              </p>
              <p className="mt-1 text-[10px] text-indigo-300/70">
                Your account is secured with encrypted authentication.
              </p>
            </div>

          </div>

        </main>
      </div>
    </main>
  );
}
