"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

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

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(
          result?.error || "Invalid email or password."
        );
      }

      /*
       * Redirect according to the account role.
       */

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

        router.replace("/dashboard");
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
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <div className="flex min-h-screen">

        {/* BRAND PANEL */}

        <section className="hidden lg:flex lg:w-[52%] bg-[#315bea] relative overflow-hidden">
          <div className="absolute -right-32 -top-32 h-[500px] w-[500px] rounded-full border-[70px] border-white/[0.05]" />

          <div className="absolute -bottom-40 -left-20 h-[420px] w-[420px] rounded-full bg-white/[0.04]" />

          <div className="relative flex w-full flex-col justify-between p-14">

            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-[13px] bg-white text-lg font-extrabold text-[#315bea]">
                P
              </div>

              <div>
                <p className="text-[17px] font-extrabold text-white">
                  Paper Tree
                </p>

                <p className="text-[9px] font-bold tracking-[0.18em] text-blue-100">
                  ONLINE TEST
                </p>
              </div>
            </div>

            <div className="relative max-w-[560px]">
              <div className="mb-5 inline-flex items-center gap-2 rounded-full bg-white/10 px-3 py-1.5 text-[10px] font-bold uppercase tracking-[0.12em] text-blue-50">
                <span className="h-1.5 w-1.5 rounded-full bg-[#8dffb4]" />
                Paper Tree
              </div>

              <h1 className="text-[48px] font-extrabold leading-[1.08] tracking-[-0.045em] text-white">
                Practice smarter.
                <br />
                <span className="text-blue-100">
                  Perform better.
                </span>
              </h1>

              <p className="mt-6 max-w-[500px] text-[15px] leading-7 text-blue-100">
                Access your Paper Tree dashboard,
                tests and preparation tools from one
                secure login.
              </p>

              <div className="mt-8 flex flex-wrap gap-2">
                {[
                  "Physics",
                  "Chemistry",
                  "Mathematics",
                  "Biology",
                ].map((subject) => (
                  <span
                    key={subject}
                    className="rounded-lg border border-white/10 bg-white/10 px-3 py-2 text-xs font-semibold text-white"
                  >
                    {subject}
                  </span>
                ))}
              </div>
            </div>

            <p className="text-xs text-blue-200">
              © 2026 Paper Tree · Online Testing Platform
            </p>
          </div>
        </section>

        {/* LOGIN */}

        <section className="flex flex-1 items-center justify-center px-6 py-10 sm:px-10">
          <div className="w-full max-w-[430px]">

            <div className="mb-9 flex items-center gap-3 lg:hidden">
              <div className="flex h-11 w-11 items-center justify-center rounded-[13px] bg-[#315bea] text-lg font-extrabold text-white">
                P
              </div>

              <div>
                <p className="text-[17px] font-extrabold">
                  Paper Tree
                </p>

                <p className="text-[9px] font-bold tracking-[0.18em] text-[#98a1b2]">
                  ONLINE TEST
                </p>
              </div>
            </div>

            <div className="mb-8">
              <p className="text-xs font-semibold text-[#315bea]">
                PAPER TREE
              </p>

              <h2 className="mt-2 text-[30px] font-extrabold tracking-[-0.035em] text-[#172033]">
                Welcome back
              </h2>

              <p className="mt-2 text-sm leading-6 text-[#929aaa]">
                Sign in with your account to continue.
              </p>
            </div>

            <form
              onSubmit={handleSubmit}
              className="rounded-[22px] border border-[#e5e8ee] bg-white p-6 shadow-[0_12px_40px_rgba(20,30,55,0.05)] sm:p-8"
            >
              {error && (
                <div className="mb-5 rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-xs font-medium leading-5 text-red-600">
                  {error}
                </div>
              )}

              <div>
                <label
                  htmlFor="email"
                  className="mb-2 block text-xs font-bold text-[#4d5668]"
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
                  className="h-12 w-full rounded-xl border border-[#dfe3ea] bg-white px-4 text-sm text-[#172033] outline-none transition placeholder:text-[#b1b7c2] focus:border-[#315bea] focus:ring-4 focus:ring-[#315bea]/10 disabled:bg-[#f7f8fb]"
                />
              </div>

              <div className="mt-5">
                <div className="mb-2 flex items-center justify-between">
                  <label
                    htmlFor="password"
                    className="block text-xs font-bold text-[#4d5668]"
                  >
                    Password
                  </label>

                  <span className="text-[10px] font-medium text-[#a0a7b4]">
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
                  className="h-12 w-full rounded-xl border border-[#dfe3ea] bg-white px-4 text-sm text-[#172033] outline-none transition placeholder:text-[#b1b7c2] focus:border-[#315bea] focus:ring-4 focus:ring-[#315bea]/10 disabled:bg-[#f7f8fb]"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="mt-7 flex h-12 w-full items-center justify-center rounded-xl bg-[#315bea] text-sm font-bold text-white shadow-[0_8px_20px_rgba(49,91,234,0.18)] transition hover:bg-[#284ed2] active:scale-[0.99] disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? "Signing in..." : "Sign in"}
              </button>
            </form>

            <div className="mt-7 text-center">
              <p className="text-[11px] leading-5 text-[#a0a7b4]">
                One account. One login. Your dashboard
                depends on your account type.
              </p>
            </div>

          </div>
        </section>
      </div>
    </main>
  );
}