"use client";

import { useRouter } from "next/navigation";

export default function AdminPage() {
  const router = useRouter();

  function logout() {
    document.cookie = "master_session=; Max-Age=0; path=/";
    router.replace("/master-login");
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      {/* HEADER */}
      <header className="border-b border-[#e7eaf0] bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#315bea] text-lg font-black text-white shadow-sm">
              P
            </div>

            <div>
              <h1 className="text-lg font-extrabold">
                Paper Tree
              </h1>

              <p className="text-[10px] font-bold tracking-[0.15em] text-[#929aaa]">
                MASTER ADMIN
              </p>
            </div>
          </div>

          <button
            onClick={logout}
            className="rounded-xl border border-[#e2e6ee] bg-white px-4 py-2.5 text-sm font-bold text-[#697386] transition hover:border-[#cfd5df] hover:bg-[#f8f9fb]"
          >
            Logout
          </button>
        </div>
      </header>

      {/* CONTENT */}
      <div className="mx-auto max-w-7xl px-6 py-12">
        {/* HERO */}
        <section className="relative overflow-hidden rounded-3xl border border-[#e1e6f2] bg-white px-8 py-9 shadow-sm">
          <div className="relative z-10 max-w-2xl">
            <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-[#f1f4ff] px-3 py-1.5 text-[11px] font-bold uppercase tracking-[0.12em] text-[#315bea]">
              <span className="h-1.5 w-1.5 rounded-full bg-[#315bea]" />
              Master Administration
            </div>

            <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl">
              Admin Control Center
            </h2>

            <p className="mt-3 max-w-xl text-sm leading-6 text-[#697386]">
              Manage Paper Tree academies and their complete
              administration from one central dashboard.
            </p>
          </div>

          {/* Decorative element */}
          <div className="pointer-events-none absolute -right-16 -top-20 h-64 w-64 rounded-full bg-[#315bea]/5" />
          <div className="pointer-events-none absolute -bottom-28 right-24 h-48 w-48 rounded-full bg-[#315bea]/5" />
        </section>

        {/* SECTION HEADER */}
        <section className="mt-10">
          <div className="mb-5">
            <h3 className="text-xl font-extrabold">
              Academy Management
            </h3>

            <p className="mt-1 text-sm text-[#8a93a5]">
              Full control over all academy tenants and their
              administration.
            </p>
          </div>

          {/* ACADEMY CARD */}
          <button
            type="button"
            onClick={() => router.push("/admin/academies")}
            className="group w-full rounded-3xl border border-[#e0e5f0] bg-white p-7 text-left shadow-sm transition duration-200 hover:-translate-y-0.5 hover:border-[#cbd5f5] hover:shadow-lg sm:p-8"
          >
            <div className="flex flex-col gap-7 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex items-start gap-5">
                <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-[#f1f4ff] text-3xl">
                  🏫
                </div>

                <div>
                  <h4 className="text-xl font-extrabold">
                    Academies
                  </h4>

                  <p className="mt-2 max-w-2xl text-sm leading-6 text-[#697386]">
                    Create and manage academy tenants, academy
                    administrators, teachers, students, batches and
                    academy-level data.
                  </p>

                  <div className="mt-4 flex flex-wrap gap-2">
                    <span className="rounded-lg bg-[#f7f8fb] px-3 py-1.5 text-xs font-semibold text-[#697386]">
                      Create
                    </span>

                    <span className="rounded-lg bg-[#f7f8fb] px-3 py-1.5 text-xs font-semibold text-[#697386]">
                      Update
                    </span>

                    <span className="rounded-lg bg-[#f7f8fb] px-3 py-1.5 text-xs font-semibold text-[#697386]">
                      Manage
                    </span>

                    <span className="rounded-lg bg-[#f7f8fb] px-3 py-1.5 text-xs font-semibold text-[#697386]">
                      Full Access
                    </span>
                  </div>
                </div>
              </div>

              <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-[#e2e6ee] text-lg text-[#315bea] transition group-hover:border-[#315bea] group-hover:bg-[#315bea] group-hover:text-white">
                →
              </div>
            </div>
          </button>
        </section>

        {/* ACCESS NOTE */}
        <div className="mt-6 flex items-center gap-3 rounded-2xl border border-[#e3e8f5] bg-[#fafbff] px-5 py-4">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#f1f4ff] text-sm">
            ✓
          </div>

          <div>
            <p className="text-xs font-bold text-[#315bea]">
              Master Admin Access
            </p>

            <p className="mt-0.5 text-xs text-[#697386]">
              You have full administrative control over academy
              management.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}