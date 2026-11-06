"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Icon } from "@/components/Icon";

type Branding = {
  name: string;
  logo_data?: string;
};

export default function Home() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [branding, setBranding] = useState<Branding | null>(null);

  useEffect(() => {
    async function loadBranding() {
      try {
        const response = await fetch("/api/academy/branding", {
          cache: "no-store",
        });

        if (!response.ok) {
          throw new Error("Could not load branding.");
        }

        const data = await response.json();

        if (data.success && data.academy) {
          setBranding(data.academy);
        }
      } catch (error) {
        console.error("BRANDING LOAD ERROR:", error);
      }
    }

    loadBranding();
  }, []);

  async function handleSubmit(
    e: FormEvent<HTMLFormElement>
  ) {
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

      const text = await response.text();

      console.log("LOGIN STATUS:", response.status);
      console.log("LOGIN RESPONSE:", text);

      let result: any = null;

      if (text) {
        try {
          result = JSON.parse(text);
        } catch {
          throw new Error(
            `Login server returned invalid data (${response.status}).`
          );
        }
      }

      if (!response.ok) {
        throw new Error(
          result?.error ||
            `Login failed with status ${response.status}.`
        );
      }

      if (!result?.success) {
        throw new Error(
          result?.error || "Login failed."
        );
      }

      if (result.role === "STUDENT") {
        if (result.user?.id) {
          localStorage.setItem(
            "studentId",
            String(result.user.id)
          );
        }

        if (result.user?.name) {
          localStorage.setItem(
            "studentName",
            result.user.name
          );
        }

        window.location.replace("/dashboard");
        return;
      } else if (result.role === "TEACHER") {
        router.replace("/teacher");
      } else if (result.role === "ACADEMY_ADMIN") {
        router.replace("/academy-admin");
      } else if (result.role === "ADMIN") {
        router.replace("/admin");
      } else {
        throw new Error("Unknown account role.");
      }

      router.refresh();
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

  const instituteName = branding?.name || "Paper Tree Educational Studio";

  return (
    <main className="min-h-screen bg-surface-app-bg text-text-primary">
      <div className="flex min-h-screen">

        {/* ========================================================= */}
        {/* LEFT BRAND / CBT PANEL                                   */}
        {/* ========================================================= */}

        <section className="relative hidden min-h-screen overflow-hidden bg-brand-deep-navy lg:flex lg:w-[52%]">

          {/* Background decoration */}

          <div className="absolute -right-40 -top-40 h-[620px] w-[620px] rounded-full border-[90px] border-white/[0.045]" />

          <div className="absolute right-20 top-40 h-[300px] w-[300px] rounded-full border-[45px] border-white/[0.035]" />

          <div className="absolute -bottom-48 -left-32 h-[560px] w-[560px] rounded-full bg-white/[0.035]" />

          <div className="relative z-10 flex w-full flex-col justify-between p-14">

            {/* ===================================================== */}
            {/* INSTITUTE BRAND                                      */}
            {/* ===================================================== */}

            <div className="flex items-center gap-3">

              {branding?.logo_data ? (
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-[14px] bg-white p-1.5 shadow-lg">
                  <img
                    src={branding.logo_data}
                    alt={`${instituteName} logo`}
                    className="h-full w-full rounded-lg object-contain"
                  />
                </div>
              ) : (
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-[14px] bg-brand-primary text-xl font-extrabold text-white shadow-lg">
                  {instituteName
                    .charAt(0)
                    .toUpperCase()}
                </div>
              )}

              <div>
                <p className="text-[18px] font-extrabold tracking-tight text-white">
                  {instituteName}
                </p>

                <p className="text-[9px] font-bold tracking-[0.22em] text-white/90">
                  COMPUTER BASED TESTING
                </p>
              </div>

            </div>

            {/* ===================================================== */}
            {/* MAIN CONTENT                                         */}
            {/* ===================================================== */}

            <div className="relative max-w-[590px]">

              <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/10 px-4 py-2 text-[10px] font-bold uppercase tracking-[0.14em] text-white/80 backdrop-blur">
                <span className="h-1.5 w-1.5 rounded-full bg-brand-yellow" />
                Computer Based Testing
              </div>

              <h1 className="text-[50px] font-extrabold leading-[1.07] tracking-[-0.045em] text-white xl:text-[58px]">
                Test smarter.
                <br />
                <span className="text-white/90">
                  Perform better.
                </span>
              </h1>

              <p className="mt-7 max-w-[510px] text-[15px] leading-7 text-white/90">
                A secure and modern computer-based testing
                platform for online examinations, practice
                tests and assessments.
              </p>

              {/* CBT FEATURES */}

              <div className="mt-9 grid max-w-[470px] grid-cols-2 gap-3">

                <div className="rounded-xl border border-white/10 bg-white/[0.12] px-4 py-3.5 backdrop-blur">
                  <div className="mb-2 flex h-7 w-7 items-center justify-center rounded-lg bg-white/[0.12] text-sm text-white">
                    <Icon name="check" size={16} color="text-white" variant="solid" />
                  </div>

                  <p className="text-xs font-bold text-white">
                    Secure Exams
                  </p>

                  <p className="mt-1 text-[10px] text-white/70">
                    Reliable online testing
                  </p>
                </div>

                <div className="rounded-xl border border-white/10 bg-white/[0.12] px-4 py-3.5 backdrop-blur">
                  <div className="mb-2 flex h-7 w-7 items-center justify-center rounded-lg bg-white/[0.12] text-sm text-white">
                    <Icon name="clock" size={16} color="text-white" />
                  </div>

                  <p className="text-xs font-bold text-white">
                    Live Testing
                  </p>

                  <p className="mt-1 text-[10px] text-white/70">
                    Timed examinations
                  </p>
                </div>

                <div className="rounded-xl border border-white/10 bg-white/[0.12] px-4 py-3.5 backdrop-blur">
                  <div className="mb-2 flex h-7 w-7 items-center justify-center rounded-lg bg-white/[0.12] text-sm text-white">
                    <Icon name="analytics" size={16} color="text-white" />
                  </div>

                  <p className="text-xs font-bold text-white">
                    Instant Results
                  </p>

                  <p className="mt-1 text-[10px] text-white/70">
                    Fast performance insights
                  </p>
                </div>

                <div className="rounded-xl border border-white/10 bg-white/[0.12] px-4 py-3.5 backdrop-blur">
                  <div className="mb-2 flex h-7 w-7 items-center justify-center rounded-lg bg-white/[0.12] text-sm text-white">
                    <Icon name="graduation-cap" size={16} color="text-white" />
                  </div>

                  <p className="text-xs font-bold text-white">
                    Smart Assessment
                  </p>

                  <p className="mt-1 text-[10px] text-white/70">
                    Structured test experience
                  </p>
                </div>

              </div>
            </div>

            {/* ===================================================== */}
            {/* LEFT FOOTER                                          */}
            {/* ===================================================== */}

            <div className="flex items-center justify-between text-xs text-text-supporting-label/70">

              <span>
                © {new Date().getFullYear()} Paper Tree Educational Studio
              </span>

              <span>
                Computer Based Testing Platform
              </span>

            </div>

          </div>
        </section>

        {/* ========================================================= */}
        {/* RIGHT LOGIN PANEL                                        */}
        {/* ========================================================= */}

        <section className="flex flex-1 items-center justify-center px-6 py-10 sm:px-10">

          <div className="w-full max-w-md">

            {/* ===================================================== */}
            {/* MOBILE BRAND                                         */}
            {/* ===================================================== */}

            <div className="mb-10 flex items-center gap-3 lg:hidden">

              {branding?.logo_data ? (
                <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-[13px] bg-white p-1.5 shadow-md">
                  <img
                    src={branding.logo_data}
                    alt={`${instituteName} logo`}
                    className="h-full w-full rounded-lg object-contain"
                  />
                </div>
              ) : (
                <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-[13px] bg-brand-primary text-lg font-extrabold text-white shadow-md">
                  {instituteName
                    .charAt(0)
                    .toUpperCase()}
                </div>
              )}

              <div>

                <p className="text-[17px] font-extrabold text-text-primary">
                  {instituteName}
                </p>

                <p className="text-[9px] font-bold tracking-[0.2em] text-text-supporting-label">
                  COMPUTER BASED TESTING
                </p>

              </div>

            </div>

            {/* ===================================================== */}
            {/* LOGIN HEADING                                        */}
            {/* ===================================================== */}

            <div className="mb-8">

              <div className="mb-3 inline-flex items-center gap-2 rounded-full bg-brand-subtle-lavender px-3 py-1.5">

                <span className="h-1.5 w-1.5 rounded-full bg-brand-primary" />

                <span className="text-[10px] font-bold uppercase tracking-[0.12em] text-brand-primary">
                  Computer Based Testing
                </span>

              </div>

              <h2 className="mt-2 text-[31px] font-extrabold tracking-[-0.04em] text-text-primary">
                Welcome back
              </h2>

              <p className="mt-2 text-sm leading-6 text-text-body">
                Sign in to access your testing dashboard.
              </p>

            </div>

            {/* ===================================================== */}
            {/* LOGIN FORM                                           */}
            {/* ===================================================== */}

            <form
              onSubmit={handleSubmit}
              className="rounded-[22px] border border-border-default bg-surface-surface p-6 shadow-[0_15px_45px_rgba(20,30,55,0.06)] sm:p-8"
            >

              {/* ERROR */}

              {error && (
                <div className="mb-5 rounded-xl border border-state-error/20 bg-state-error/10 px-4 py-3 text-xs font-medium leading-5 text-state-error">
                  {error}
                </div>
              )}

              {/* EMAIL */}

              <div>

                <label
                  htmlFor="email"
                  className="mb-2 block text-xs font-bold text-text-tertiary"
                >
                  Email address
                </label>

                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) =>
                    setEmail(e.target.value)
                  }
                  placeholder="you@example.com"
                  autoComplete="email"
                  required
                  disabled={loading}
                  className="h-12 w-full rounded-xl border border-border-default bg-surface-surface px-4 text-sm text-text-primary outline-none transition placeholder:text-text-supporting-label focus:border-brand-primary focus:ring-4 focus:ring-brand-primary/10 disabled:bg-surface-app-bg"
                />

              </div>

              {/* PASSWORD */}

              <div className="mt-5">

                <div className="mb-2 flex items-center justify-between">

                  <label
                    htmlFor="password"
                    className="block text-xs font-bold text-text-tertiary"
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
                  onChange={(e) =>
                    setPassword(e.target.value)
                  }
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  required
                  disabled={loading}
                  className="h-12 w-full rounded-xl border border-border-default bg-surface-surface px-4 text-sm text-text-primary outline-none transition placeholder:text-text-supporting-label focus:border-brand-primary focus:ring-4 focus:ring-brand-primary/10 disabled:bg-surface-app-bg"
                />

              </div>

              {/* LOGIN BUTTON */}

              <button
                type="submit"
                disabled={loading}
                className="mt-7 flex h-12 w-full items-center justify-center rounded-xl bg-brand-primary text-sm font-bold text-white shadow-[0_8px_20px_rgba(36,85,200,0.18)] transition-all duration-200 hover:bg-brand-action-blue active:bg-brand-deep-navy disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading
                  ? "Signing in..."
                  : "Sign in to CBT"}
              </button>

            </form>

            {/* ===================================================== */}
            {/* RIGHT FOOTER                                          */}
            {/* ===================================================== */}

            <div className="mt-7 text-center">

              <p className="text-[11px] leading-5 text-text-body">
                Secure access for students, teachers and
                administrators.
              </p>

              <p className="mt-2 text-[10px] font-medium text-text-disabled">
                © {new Date().getFullYear()} Paper Tree Educational Studio
              </p>

            </div>

          </div>

        </section>

      </div>
    </main>
  );
}