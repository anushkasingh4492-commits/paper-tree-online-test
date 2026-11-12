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

  const brandName = branding?.name || "Paper Tree";

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

      let result: {
        success?: boolean;
        error?: string;
        role?: string;
        user?: { id?: string | number; name?: string };
      } | null = null;

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

  return (
    <main className="min-h-screen w-full bg-surface-app-bg text-text-primary flex flex-col">
      <div className="flex-1 flex flex-col lg:flex-row">
        {/* LEFT: Academy branding + CBT + feature cards */}
        <section className="flex-1 bg-brand-primary flex flex-col p-8 lg:px-12 lg:py-16 text-white overflow-hidden relative">
          <div className="absolute inset-0 bg-brand-deep-navy/40" />
          <div className="relative z-10">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-10 h-10 rounded-xl bg-white flex items-center justify-center">
                <Icon name="graduation-cap" size={20} className="text-brand-primary" />
              </div>
              <div>
                <h2 className="text-xl font-extrabold tracking-tight">{brandName}</h2>
                <p className="text-[10px] font-bold uppercase tracking-wider text-brand-primary/90">COMPUTER BASED TESTING</p>
              </div>
            </div>
            <span className="px-3 py-1 rounded-full bg-brand-action-blue text-[10px] font-bold uppercase tracking-wider text-brand-deep-navy mb-8 inline-block">
              CBT
            </span>
            <h1 className="text-4xl md:text-5xl font-black tracking-tight leading-tight mb-6">
              Test smarter.<br />
              Perform better.
            </h1>
            <p className="text-brand-primary/90 text-sm max-w-md leading-relaxed mb-10">
              A secure and modern computer-based testing platform for online examinations, practice tests and assessments.
            </p>

            <div className="grid grid-cols-2 gap-4 mb-10">
              <div className="rounded-xl border border-brand-primary/20 bg-brand-action-blue/10 p-5 flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center">
                  <Icon name="check" size={16} className="text-white" />
                </div>
                <div>
                  <div className="font-bold text-sm text-white">Secure Exams</div>
                  <div className="text-[10px] text-brand-primary/80">Reliable online testing</div>
                </div>
              </div>
              <div className="rounded-xl border border-brand-primary/20 bg-brand-action-blue/10 p-5 flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center">
                  <Icon name="clock" size={16} className="text-white" />
                </div>
                <div>
                  <div className="font-bold text-sm text-white">Live Testing</div>
                  <div className="text-[10px] text-brand-primary/80">Timed examinations</div>
                </div>
              </div>
              <div className="rounded-xl border border-brand-primary/20 bg-brand-action-blue/10 p-5 flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center">
                  <Icon name="users" size={16} className="text-white" />
                </div>
                <div>
                  <div className="font-bold text-sm text-white">Instant Results</div>
                  <div className="text-[10px] text-brand-primary/80">Fast performance insights</div>
                </div>
              </div>
              <div className="rounded-xl border border-brand-primary/20 bg-brand-action-blue/10 p-5 flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center">
                  <Icon name="analytics" size={16} className="text-white" />
                </div>
                <div>
                  <div className="font-bold text-sm text-white">Smart Assessment</div>
                  <div className="text-[10px] text-brand-primary/80">Structured test experience</div>
                </div>
              </div>
            </div>

            <p className="text-brand-primary/60 text-[10px] font-medium">
              © {new Date().getFullYear()} {brandName}
            </p>
          </div>
        </section>

        {/* RIGHT: Simple login form */}
        <section className="flex-1 flex items-center justify-center p-8 lg:p-12 bg-white/5 backdrop-blur-sm">
          <div className="w-full max-w-md space-y-6">
            <div>
              <h2 className="text-2xl font-extrabold text-text-primary">Welcome back</h2>
              <p className="mt-1 text-text-tertiary">Sign in to continue to your tests.</p>
            </div>

            {error && (
              <div className="rounded-xl border border-state-error/20 bg-state-error/10 px-4 py-3 text-sm font-medium text-state-error">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-xs font-bold uppercase tracking-wider text-text-tertiary mb-1">
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
                  className="h-12 w-full rounded-xl border border-border-default bg-white px-4 text-sm text-text-primary outline-none transition focus:border-brand-primary focus:ring-4 focus:ring-brand-primary/10 disabled:bg-surface-subtle"
                />
              </div>

              <div>
                <div className="mb-1 flex items-center justify-between">
                  <label htmlFor="password" className="block text-xs font-bold uppercase tracking-wider text-text-tertiary">
                    Password
                  </label>
                  <span className="text-[10px] font-medium text-text-body">Secure login</span>
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
                  className="h-12 w-full rounded-xl border border-border-default bg-white px-4 text-sm text-text-primary outline-none transition focus:border-brand-primary focus:ring-4 focus:ring-brand-primary/10 disabled:bg-surface-subtle"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="mt-2 flex h-12 w-full items-center justify-center rounded-xl bg-brand-primary text-sm font-bold text-white shadow-[0_8px_20px_rgba(36,85,200,0.25)] transition-all duration-200 hover:bg-brand-action-blue active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? "Signing in..." : "Sign in to CBT"}
              </button>
            </form>

            <div className="mt-6 w-full">
              <button
                type="button"
                onClick={() => router.push("/master-login")}
                className="w-full rounded-xl border border-border-default bg-white px-4 py-3 text-sm font-bold text-text-tertiary transition-all duration-200 hover:bg-surface-subtle active:bg-surface-muted"
              >
                Teacher / Admin Login
              </button>
            </div>

            <div className="mt-8 text-center">
              <p className="text-[11px] leading-5 text-text-tertiary">
                Secure access for students, teachers and administrators.
              </p>
              <p className="mt-2 text-[10px] font-medium text-text-body">
                © {new Date().getFullYear()} {brandName}
              </p>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
