"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

export default function MasterLoginPage() {
  const router = useRouter();

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
        body: JSON.stringify({ email, password }),
      });

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(result.error || "Login failed.");
      }

      if (result.role === "ADMIN") {
        router.push("/admin");
      } else if (result.role === "TEACHER") {
        router.push("/teacher");
      } else {
        throw new Error("Unknown account role.");
      }
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Login failed."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-[#f6f8fc] px-6">
      <div className="w-full max-w-md rounded-3xl border border-[#e8ebf1] bg-white p-8 shadow-sm">
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-[#315bea] text-2xl font-extrabold text-white">
            P
          </div>

          <h1 className="text-2xl font-extrabold text-[#172033]">
            Paper Tree
          </h1>

          <p className="mt-1 text-sm text-[#697386]">
            Admin / Teacher Login
          </p>
        </div>

        <form onSubmit={login} className="space-y-5">
          <div>
            <label className="mb-2 block text-sm font-semibold text-[#263044]">
              Email
            </label>

            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter email"
              className="w-full rounded-xl border border-[#dfe3eb] px-4 py-3 outline-none transition focus:border-[#315bea]"
              required
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-semibold text-[#263044]">
              Password
            </label>

            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              className="w-full rounded-xl border border-[#dfe3eb] px-4 py-3 outline-none transition focus:border-[#315bea]"
              required
            />
          </div>

          {error && (
            <div className="rounded-xl bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl bg-[#315bea] px-4 py-3 font-bold text-white transition hover:bg-[#264ac7] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>
      </div>
    </main>
  );
}
