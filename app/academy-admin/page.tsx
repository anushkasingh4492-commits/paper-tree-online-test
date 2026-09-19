"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type Overview = {
  academy: { name: string; code?: string; logo_data?: string | null; status?: string; student_limit?: number; subscription_end?: string | null };
  counts: { teachers: number; students: number; batches: number; scheduled_tests: number };
  batches: Array<{ id: string; name: string; class_name?: string; student_count: number }>;
  tests: Array<{ id: string; title: string; batch_name?: string; start_time: string; status: string }>;
};

const actions = [
  { title: "Teachers", description: "Invite and manage teaching staff.", icon: "👩‍🏫", href: "/academy-admin/teachers" },
  { title: "Students", description: "Create student accounts and credentials.", icon: "🎓", href: "/academy-admin/students" },
  { title: "Batches", description: "Build classes and assign students.", icon: "👥", href: "/academy-admin/batches" },
  { title: "Scheduled tests", description: "Schedule academy papers for batches.", icon: "🗓️", href: "/academy-admin/tests" },
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

  function logout() {
    document.cookie = "master_session=; Max-Age=0; path=/";
    router.replace("/");
  }

  const countCards = [
    ["Teachers", overview?.counts.teachers ?? 0, "👩‍🏫"],
    ["Students", overview?.counts.students ?? 0, "🎓"],
    ["Batches", overview?.counts.batches ?? 0, "👥"],
    ["Open tests", overview?.counts.scheduled_tests ?? 0, "🗓️"],
  ];

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <header className="border-b border-[#e7eaf0] bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div className="flex items-center gap-3">{overview?.academy.logo_data ? <img src={overview.academy.logo_data} alt="Institute logo" className="h-10 w-10 rounded-lg object-contain" /> : null}<div><p className="text-xs font-black tracking-[.16em] text-[#315bea]">ACADEMY ADMIN</p><h1 className="mt-1 text-xl font-extrabold">{overview?.academy.name || "Academy control centre"}</h1></div></div>
          <button onClick={logout} className="rounded-xl border border-[#e2e6ee] px-4 py-2.5 text-sm font-bold text-[#697386]">Logout</button>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-9">
        {error && <div className="mb-6 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">{error}</div>}
        <section className="rounded-3xl bg-gradient-to-r from-[#315bea] to-[#6b47e8] px-7 py-8 text-white shadow-lg">
          <p className="text-xs font-black tracking-[.16em] text-blue-100">ONE PLACE TO RUN YOUR ACADEMY</p>
          <h2 className="mt-2 text-3xl font-extrabold">Everything is in sync.</h2>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-blue-100">Teachers, students, batches and tests use the same academy records that the master admin sees. Changes appear there automatically.</p>
          {overview?.academy.subscription_end && <p className="mt-5 text-xs font-bold text-blue-100">Subscription ends {new Date(overview.academy.subscription_end).toLocaleDateString("en-IN")}</p>}
        </section>

        <section className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {countCards.map(([label, value, icon]) => <div key={String(label)} className="rounded-2xl border border-[#e3e8f5] bg-white p-5 shadow-sm"><span className="text-2xl">{icon}</span><p className="mt-4 text-3xl font-extrabold">{value}</p><p className="mt-1 text-sm font-semibold text-[#697386]">{label}</p></div>)}
        </section>

        <section className="mt-8 grid gap-5 md:grid-cols-2 xl:grid-cols-4">
          {actions.map((action) => <button key={action.title} onClick={() => router.push(action.href)} className="rounded-2xl border border-[#e3e8f5] bg-white p-5 text-left shadow-sm transition hover:-translate-y-0.5 hover:border-[#315bea]"><span className="text-2xl">{action.icon}</span><h3 className="mt-4 font-extrabold">{action.title}</h3><p className="mt-1 text-sm leading-6 text-[#697386]">{action.description}</p><span className="mt-4 block text-sm font-bold text-[#315bea]">Manage →</span></button>)}
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-2">
          <div className="rounded-2xl border border-[#e3e8f5] bg-white p-6 shadow-sm"><div className="flex items-center justify-between"><h3 className="font-extrabold">Batch snapshot</h3><button onClick={() => router.push("/academy-admin/batches")} className="text-sm font-bold text-[#315bea]">Manage</button></div><div className="mt-4 space-y-3">{overview?.batches.length ? overview.batches.map((batch) => <div key={batch.id} className="flex justify-between rounded-xl bg-[#f7f8fc] px-4 py-3"><span><b>{batch.name}</b><small className="ml-2 text-[#697386]">{batch.class_name}</small></span><span className="text-sm font-bold text-[#315bea]">{batch.student_count} students</span></div>) : <p className="text-sm text-[#697386]">Create your first batch to organise students.</p>}</div></div>
          <div className="rounded-2xl border border-[#e3e8f5] bg-white p-6 shadow-sm"><div className="flex items-center justify-between"><h3 className="font-extrabold">Upcoming tests</h3><button onClick={() => router.push("/academy-admin/tests")} className="text-sm font-bold text-[#315bea]">Schedule test</button></div><div className="mt-4 space-y-3">{overview?.tests.length ? overview.tests.map((test) => <div key={test.id} className="rounded-xl bg-[#f7f8fc] px-4 py-3"><b>{test.title}</b><p className="mt-1 text-xs text-[#697386]">{test.batch_name || "Academy"} · {new Date(test.start_time).toLocaleString("en-IN")}</p></div>) : <p className="text-sm text-[#697386]">No upcoming tests. Schedule one when a paper is ready.</p>}</div></div>
        </section>
      </div>
    </main>
  );
}
