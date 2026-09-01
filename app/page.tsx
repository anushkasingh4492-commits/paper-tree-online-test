"use client";

import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <div className="flex min-h-screen items-center justify-center px-6 py-10">

        <div className="w-full max-w-5xl">

          {/* BRAND */}

          <div className="mb-12 text-center">

            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-[#315bea] text-2xl font-black text-white shadow-lg">
              P
            </div>

            <h1 className="mt-5 text-3xl font-extrabold tracking-tight">
              Paper Tree
            </h1>

            <p className="mt-2 text-sm text-[#8a93a5]">
              MHT-CET · NEET Online Testing Platform
            </p>

          </div>

          {/* TITLE */}

          <div className="mb-8 text-center">

            <p className="text-xs font-bold uppercase tracking-[0.15em] text-[#315bea]">
              Welcome
            </p>

            <h2 className="mt-2 text-2xl font-extrabold">
              Choose your portal
            </h2>

            <p className="mt-2 text-sm text-[#697386]">
              Select how you want to access Paper Tree.
            </p>

          </div>

          {/* PORTALS */}

          <div className="grid gap-5 md:grid-cols-3">

            {/* STUDENT */}

            <button
              type="button"
              onClick={() =>
                router.push("/student-login")
              }
              className="group rounded-2xl border border-[#e3e8f5] bg-white p-7 text-left shadow-sm transition hover:-translate-y-1 hover:border-[#cbd5f5] hover:shadow-lg"
            >

              <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-[#eef2ff] text-2xl">
                🎓
              </div>

              <h3 className="mt-6 text-xl font-extrabold">
                Student
              </h3>

              <p className="mt-2 text-sm leading-6 text-[#697386]">
                Take online tests, view scheduled tests,
                check results and track your preparation.
              </p>

              <div className="mt-6 text-sm font-bold text-[#315bea]">
                Student Login
                <span className="ml-2 transition group-hover:ml-3">
                  →
                </span>
              </div>

            </button>

            {/* TEACHER */}

            <button
              type="button"
              onClick={() =>
                router.push("/master-login?role=TEACHER")
              }
              className="group rounded-2xl border border-[#e3e8f5] bg-white p-7 text-left shadow-sm transition hover:-translate-y-1 hover:border-[#cbd5f5] hover:shadow-lg"
            >

              <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-[#eef8f2] text-2xl">
                👩‍🏫
              </div>

              <h3 className="mt-6 text-xl font-extrabold">
                Teacher
              </h3>

              <p className="mt-2 text-sm leading-6 text-[#697386]">
                Create papers, select questions,
                schedule tests and publish them to students.
              </p>

              <div className="mt-6 text-sm font-bold text-[#315bea]">
                Teacher Login
                <span className="ml-2 transition group-hover:ml-3">
                  →
                </span>
              </div>

            </button>

            {/* ADMIN */}

            <button
              type="button"
              onClick={() =>
                router.push("/master-login?role=ADMIN")
              }
              className="group rounded-2xl border border-[#e3e8f5] bg-white p-7 text-left shadow-sm transition hover:-translate-y-1 hover:border-[#cbd5f5] hover:shadow-lg"
            >

              <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-[#fff7ed] text-2xl">
                🛡️
              </div>

              <h3 className="mt-6 text-xl font-extrabold">
                Admin
              </h3>

              <p className="mt-2 text-sm leading-6 text-[#697386]">
                Manage the application, upload datasets,
                access the question bank and control portals.
              </p>

              <div className="mt-6 text-sm font-bold text-[#315bea]">
                Admin Login
                <span className="ml-2 transition group-hover:ml-3">
                  →
                </span>
              </div>

            </button>

          </div>

          <p className="mt-10 text-center text-[11px] text-[#a0a7b4]">
            © 2026 Paper Tree · Online Testing Platform
          </p>

        </div>
      </div>
    </main>
  );
}
