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

  const brandName = branding?.name || "Paper Tree";

  return (
    <main className="min-h-screen bg-surface-app-bg text-text-primary">
      <div className="flex min-h-screen w-full">

        {/* LEFT BRAND PANEL */}
        <section className="hidden lg:flex lg:w-[52%] bg-brand-primary relative overflow-hidden">

          <div className="absolute -right-32 -top-32 h-[500px] w-[500px] rounded-full border-[70px] border-white/[0.06]" />
          <div className="absolute -bottom-40 -left-20 h-[420px] w-[420px] rounded-full bg-white/[0.05]" />
          <div className="absolute top-1/4 left-1/5 h-[320px] w-[320px] bg-purple-500/20 blur-[100px] rounded-full" />

          <div className="relative flex w-full flex-col justify-between p-14">

            <div className="flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-white text-2xl font-black text-brand-primary shadow-lg">
                P
              </div>
              <div className="text-white">
                <div className="font-extrabold text-[20px] tracking-tight">
                  {brandName}
                </div>
                <div className="text-indigo-100 text-[11px] font-semibold uppercase tracking-wider mt-0.5">
                  Educational Studio
                </div>
              </div>
            </div>

            <div className="relative max-w-[560px] mt-6">

              <div className="mb-8">
                <img
                  src="/images/login/Stacked Books with Floating Question Tiles.png"
                  alt="Study materials"
                  className="w-full h-auto block mx-auto drop-shadow-2xl"
                  loading="lazy"
                />
              </div>

              <div className="space-y-3">
                <h2 className="text-3xl font-extrabold text-white tracking-tight">
                  Welcome back
                </h2>
                <p className="text-indigo-100 text-lg">
                  Sign in to access your dashboard,<br />
                  performance insights, and learning tools.
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
                  Enter your credentials below
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

              <button
                type="submit"
                disabled={loading}
                className="mt-2 flex h-12 w-full items-center justify-center rounded-xl bg-brand-primary text-sm font-bold text-white shadow-[0_8px_20px_rgba(36,85,200,0.18)] transition-all duration-200 hover:bg-brand-action-blue active:bg-brand-deep-navy disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading
                  ? "Signing in..."
                  : "Sign in to CBT"}
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
                Secure access for students, teachers and
                administrators.
              </p>
              <p className="mt-2 text-[10px] font-medium text-text-disabled">
                © {new Date().getFullYear()} Paper Tree Educational Studio
              </p>
            </div>

          </div>

        </main>
      </div>
    </main>
  );
}
