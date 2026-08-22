
"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();

    // Temporary navigation until real authentication is connected.
    router.push("/dashboard");
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc] flex items-center justify-center px-6">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-[#1d4ed8] text-white text-2xl font-bold shadow-lg mb-4">
            P
          </div>

          <h1 className="text-3xl font-bold tracking-tight text-[#111827]">
            Paper Tree
          </h1>

          <p className="mt-2 text-sm text-[#6b7280]">
            Online Test
          </p>
        </div>

        <div className="bg-white rounded-2xl border border-[#e5e7eb] shadow-sm p-8">
          <div className="mb-7">
            <h2 className="text-2xl font-semibold text-[#111827]">
              Welcome back
            </h2>
            <p className="mt-1 text-sm text-[#6b7280]">
              Sign in to continue your tests
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-[#374151] mb-2"
              >
                Email address
              </label>

              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                required
                className="w-full h-12 rounded-xl border border-[#d1d5db] px-4 text-sm outline-none transition focus:border-[#2563eb] focus:ring-4 focus:ring-blue-100"
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-[#374151] mb-2"
              >
                Password
              </label>

              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                required
                className="w-full h-12 rounded-xl border border-[#d1d5db] px-4 text-sm outline-none transition focus:border-[#2563eb] focus:ring-4 focus:ring-blue-100"
              />
            </div>

            <button
              type="submit"
              className="w-full h-12 rounded-xl bg-[#1d4ed8] text-white font-semibold text-sm transition hover:bg-[#1e40af] active:scale-[0.99]"
            >
              Sign In
            </button>
          </form>

          <div className="mt-6 pt-6 border-t border-[#f0f0f0] text-center">
            <p className="text-xs text-[#9ca3af]">
              MHT-CET Online Testing Platform
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
