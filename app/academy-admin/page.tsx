"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type Overview = {
  academy: { name: string; code?: string; logo_data?: string | null; status?: string; student_limit?: number; subscription_end?: string | null; subscription_tier?: string };
  counts: { teachers: number; students: number; batches: number; scheduled_tests: number };
  batches: Array<{ id: string; name: string; class_name?: string; student_count: number }>;
  tests: Array<{ id: string; title: string; batch_name?: string; start_time: string; status: string }>;
};

const actions = [
  { title: "Teachers", description: "Invite and manage teaching staff.", icon: "👩‍🏫", href: "/academy-admin/teachers" },
  { title: "Students", description: "Create student accounts and credentials.", icon: "🎓", href: "/academy-admin/students" },
  { title: "Batches", description: "Build classes and assign students.", icon: "👥", href: "/academy-admin/batches" },
  { title: "Scheduled tests", description: "Schedule academy papers for batches.", icon: "🗓️", href: "/academy-admin/tests" },
  { title: "Student performance", description: "Review student results, accuracy and attempted tests.", icon: "📊", href: "/academy-admin/performance" },
];

export default function AcademyAdminPage() {
  const router = useRouter();
  const [overview, setOverview] = useState<Overview | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    void fetch("/api/academy-admin/overview", { cache: "no-store", credentials: "include" })
      .then(async (response) => {
        const data = await response.json();
        if (!response.ok || !data.success) throw new Error(data.error || "Unable to load academy details.");
        setOverview(data);
      })
      .catch((reason) => setError(reason instanceof Error ? reason.message : "Unable to load academy details."));
  }, []);
  useEffect(() => {
    void fetch("/api/academy/branding", {
      cache: "no-store",
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        const academyName =
          data?.success && data?.academy?.name
            ? String(data.academy.name).trim()
            : "";

        document.title = academyName ? `${academyName} CBT` : "CBT";
      })
      .catch(() => {
        document.title = "CBT";
      });
  }, []);
  function logout() {
    document.cookie = "master_session=; Max-Age=0; path=/";
    router.replace("/login");
  }

  const countCards = [
    ["Teachers", overview?.counts.teachers ?? 0, "👩‍🏫"],
    ["Students", overview?.counts.students ?? 0, "🎓"],
    ["Batches", overview?.counts.batches ?? 0, "👥"],
    ["Open tests", overview?.counts.scheduled_tests ?? 0, "🗓️"],
  ];

  return (
    <main className="min-h-screen bg-surface-app-bg text-text-primary">
      <header className="border-b border-border-default bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div className="flex items-center gap-3">{overview?.academy.logo_data ? <img src={overview.academy.logo_data} alt="Institute logo" className="h-10 w-10 rounded-lg object-contain" /> : null}<div><p className="text-xs font-black tracking-[.16em] text-brand-primary">ACADEMY ADMIN</p><h1 className="mt-1 text-xl font-extrabold">{overview?.academy.name || "Academy control centre"}</h1></div></div>
          <button onClick={logout} className="rounded-xl border border-border-default px-4 py-2.5 text-sm font-bold text-text-tertiary">Logout</button>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-9">
        {error && <div className="mb-6 rounded-xl border border-state-error/20 bg-state-error/10 px-4 py-3 text-sm font-semibold text-state-error">{error}</div>}
        <section className="rounded-3xl bg-gradient-to-r from-[#315bea] to-[#6b47e8] px-7 py-8 text-white shadow-lg">
          <p className="text-xs font-black tracking-[.16em] text-white/90">ONE PLACE TO RUN YOUR ACADEMY</p>
          <h2 className="mt-2 text-3xl font-extrabold">Everything is in sync.</h2>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-white/90">Teachers, students, batches and tests use the same academy records that the master admin sees. Changes appear there automatically.</p>
          {overview?.academy.subscription_end && <p className="mt-5 text-xs font-bold text-white/90">Plan: {overview?.academy.subscription_tier || "GOLD"} · Subscription ends {new Date(overview.academy.subscription_end).toLocaleDateString("en-IN")}</p>}
        </section>

        <section className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {countCards.map(([label, value, icon]) => <div key={String(label)} className="rounded-2xl border border-border-default bg-white p-5 shadow-sm"><span className="text-2xl">{icon}</span><p className="mt-4 text-3xl font-extrabold">{value}</p><p className="mt-1 text-sm font-semibold text-text-tertiary">{label}</p></div>)}
        </section>

        <section className="mt-8 grid gap-5 md:grid-cols-2 xl:grid-cols-5">
          {actions.map((action) => <button key={action.title} onClick={() => router.push(action.href)} className="rounded-2xl border border-border-default bg-white p-5 text-left shadow-sm transition hover:-translate-y-0.5 hover:border-brand-primary"><span className="text-2xl">{action.icon}</span><h3 className="mt-4 font-extrabold">{action.title}</h3><p className="mt-1 text-sm leading-6 text-text-tertiary">{action.description}</p><span className="mt-4 block text-sm font-bold text-brand-primary">Manage →</span></button>)}
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-2">
          <div className="rounded-2xl border border-border-default bg-white p-6 shadow-sm"><div className="flex items-center justify-between"><h3 className="font-extrabold">Batch snapshot</h3><button onClick={() => router.push("/academy-admin/batches")} className="text-sm font-bold text-brand-primary">Manage</button></div><div className="mt-4 space-y-3">{overview?.batches.length ? overview.batches.map((batch) => <div key={batch.id} className="flex justify-between rounded-xl bg-surface-app-bg px-4 py-3"><span><b>{batch.name}</b><small className="ml-2 text-text-tertiary">{batch.class_name}</small></span><span className="text-sm font-bold text-brand-primary">{batch.student_count} students</span></div>) : <p className="text-sm text-text-tertiary">Create your first batch to organise students.</p>}</div></div>
          <div className="rounded-2xl border border-border-default bg-white p-6 shadow-sm"><div className="flex items-center justify-between"><h3 className="font-extrabold">Upcoming tests</h3><button onClick={() => router.push("/academy-admin/tests")} className="text-sm font-bold text-brand-primary">Schedule test</button></div><div className="mt-4 space-y-3">{overview?.tests.length ? overview.tests.map((test) => <div key={test.id} className="rounded-xl bg-surface-app-bg px-4 py-3"><b>{test.title}</b><p className="mt-1 text-xs text-text-tertiary">{test.batch_name || "Academy"} · {new Date(test.start_time).toLocaleString("en-IN")}</p></div>) : <p className="text-sm text-text-tertiary">No upcoming tests. Schedule one when a paper is ready.</p>}</div></div>
        </section>
      </div>
    </main>
  );
}
