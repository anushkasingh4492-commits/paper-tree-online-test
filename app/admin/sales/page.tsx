"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { isDemoPortalHostname } from "@/components/useDemoPortal";

type SalesUser = {
  id: string;
  name: string;
  email: string;
  active: boolean;
  institutes_set_up: number;
  rejected: number;
  follow_up: number;
  interested: number;
  converted: number;
  students_converted: number;
  sales_amount: string;
  commission: string;
};

type Lead = {
  id: string;
  institute_name: string;
  contact_name: string;
  status: string;
  sales_person: string;
  students_converted: number;
  sale_amount: string;
  commission: string;
  created_at: string;
};

export default function SalesManagementPage() {
  const router = useRouter();
  const [salesUsers, setSalesUsers] = useState<SalesUser[]>([]);
  const [leads, setLeads] = useState<Lead[]>([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    setError("");
    try {
      const [teamResponse, leadsResponse] = await Promise.all([
        fetch("/api/sales/team", { cache: "no-store" }),
        fetch("/api/sales/leads", { cache: "no-store" }),
      ]);
      const [teamData, leadsData] = await Promise.all([teamResponse.json(), leadsResponse.json()]);
      if (!teamResponse.ok || !teamData.success) throw new Error(teamData.error || "Could not load sales team.");
      if (!leadsResponse.ok || !leadsData.success) throw new Error(leadsData.error || "Could not load institute demos.");
      setSalesUsers(teamData.salesUsers);
      setLeads(leadsData.leads);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Could not load sales data.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (!isDemoPortalHostname(window.location.hostname)) {
      router.replace("/admin");
      return;
    }
    void Promise.resolve().then(load);
  }, [router]);

  const totals = useMemo(() => salesUsers.reduce((total, person) => ({
    demos: total.demos + Number(person.institutes_set_up),
    rejected: total.rejected + Number(person.rejected),
    followUp: total.followUp + Number(person.follow_up),
    interested: total.interested + Number(person.interested),
    converted: total.converted + Number(person.converted),
    students: total.students + Number(person.students_converted),
    salesAmount: total.salesAmount + Number(person.sales_amount),
    commission: total.commission + Number(person.commission),
  }), { demos: 0, rejected: 0, followUp: 0, interested: 0, converted: 0, students: 0, salesAmount: 0, commission: 0 }), [salesUsers]);

  async function createSalesUser(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setMessage("");
    try {
      const response = await fetch("/api/sales/team", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });
      const data = await response.json();
      if (!response.ok || !data.success) throw new Error(data.error || "Could not create sales login.");
      setName("");
      setEmail("");
      setPassword("");
      setMessage("Sales login created.");
      await load();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Could not create sales login.");
    }
  }

  const cards = [
    ["Institutes set up", totals.demos],
    ["Rejected", totals.rejected],
    ["Follow-up", totals.followUp],
    ["Interested", totals.interested],
    ["Converted", totals.converted],
    ["Students converted", totals.students],
    ["Total sales", `₹${totals.salesAmount.toLocaleString("en-IN", { maximumFractionDigits: 2 })}`],
    ["Commission (10%)", `₹${totals.commission.toLocaleString("en-IN", { maximumFractionDigits: 2 })}`],
  ] as const;

  return (
    <main className="min-h-screen bg-slate-50 px-5 py-8 text-slate-900 sm:px-8">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
          <div><button onClick={() => router.push("/admin")} className="mb-2 text-sm font-bold text-blue-700">← Admin portal</button><h1 className="text-3xl font-black">Sales performance</h1><p className="mt-1 text-slate-600">Manage sales logins and track institute demos, conversions, and commissions.</p></div>
          <button onClick={load} className="rounded-xl border bg-white px-4 py-2 font-bold">Refresh</button>
        </header>
        {error && <p role="alert" className="mb-5 rounded-xl bg-red-50 p-4 text-sm font-semibold text-red-700">{error}</p>}
        {message && <p role="status" className="mb-5 rounded-xl bg-emerald-50 p-4 text-sm font-semibold text-emerald-700">{message}</p>}

        <section className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4" aria-label="Sales totals">
          {cards.map(([label, value]) => <article key={label} className="rounded-2xl border bg-white p-5 shadow-sm"><p className="text-sm font-semibold text-slate-500">{label}</p><p className="mt-2 text-3xl font-black">{value}</p></article>)}
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(280px,1fr)]">
          <div className="overflow-hidden rounded-2xl border bg-white shadow-sm">
            <h2 className="border-b px-5 py-4 text-lg font-extrabold">Sales team</h2>
            {loading ? <p className="p-5 text-slate-500">Loading sales team…</p> : salesUsers.length === 0 ? <p className="p-5 text-slate-500">No sales logins yet.</p> : <div className="overflow-x-auto"><table className="w-full min-w-[800px] text-left text-sm"><thead className="bg-slate-50 text-slate-500"><tr>{["Name", "Email", "Institutes", "Converted", "Students", "Commission", "Access"].map((item) => <th key={item} className="px-4 py-3 font-bold">{item}</th>)}</tr></thead><tbody>{salesUsers.map((person) => <tr key={person.id} className="border-t"><td className="px-4 py-3 font-bold">{person.name}</td><td className="px-4 py-3">{person.email}</td><td className="px-4 py-3">{person.institutes_set_up}</td><td className="px-4 py-3">{person.converted}</td><td className="px-4 py-3">{person.students_converted}</td><td className="px-4 py-3">₹{Number(person.commission).toLocaleString("en-IN", { maximumFractionDigits: 2 })}</td><td className="px-4 py-3"><button onClick={async () => { const response = await fetch("/api/sales/team", { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ id: person.id, active: !person.active }) }); const result = await response.json(); if (!response.ok || !result.success) { setError(result.error || "Could not update account."); return; } await load(); }} className={`font-bold ${person.active ? "text-red-700" : "text-emerald-700"}`}>{person.active ? "Disable" : "Enable"}</button></td></tr>)}</tbody></table></div>}
          </div>
          <form onSubmit={createSalesUser} className="h-fit rounded-2xl border bg-white p-5 shadow-sm">
            <h2 className="text-lg font-extrabold">Create sales login</h2>
            <label className="mt-4 block text-sm font-bold">Name<input required value={name} onChange={(event) => setName(event.target.value)} className="mt-1 w-full rounded-lg border px-3 py-2 font-normal" /></label>
            <label className="mt-3 block text-sm font-bold">Email<input required type="email" value={email} onChange={(event) => setEmail(event.target.value)} className="mt-1 w-full rounded-lg border px-3 py-2 font-normal" /></label>
            <label className="mt-3 block text-sm font-bold">Temporary password<input required minLength={8} type="password" value={password} onChange={(event) => setPassword(event.target.value)} className="mt-1 w-full rounded-lg border px-3 py-2 font-normal" /></label>
            <button className="mt-5 w-full rounded-xl bg-blue-700 px-4 py-3 font-extrabold text-white">Create login</button>
          </form>
        </section>

        <section className="mt-8 overflow-hidden rounded-2xl border bg-white shadow-sm">
          <h2 className="border-b px-5 py-4 text-lg font-extrabold">Institute demos in Academy Management</h2>
          {loading ? <p className="p-5 text-slate-500">Loading institute demos…</p> : leads.length === 0 ? <p className="p-5 text-slate-500">Institute demos added by sales staff will appear here.</p> : <div className="overflow-x-auto"><table className="w-full min-w-[800px] text-left text-sm"><thead className="bg-slate-50 text-slate-500"><tr>{["Institute", "Salesperson", "Status", "Students", "Sale amount", "Commission"].map((item) => <th key={item} className="px-4 py-3 font-bold">{item}</th>)}</tr></thead><tbody>{leads.map((lead) => <tr key={lead.id} className="border-t"><td className="px-4 py-3 font-bold">{lead.institute_name}</td><td className="px-4 py-3">{lead.sales_person}</td><td className="px-4 py-3">{lead.status.replaceAll("_", " ")}</td><td className="px-4 py-3">{lead.students_converted}</td><td className="px-4 py-3">₹{Number(lead.sale_amount).toLocaleString("en-IN")}</td><td className="px-4 py-3">₹{Number(lead.commission).toLocaleString("en-IN", { maximumFractionDigits: 2 })}</td></tr>)}</tbody></table></div>}
        </section>
      </div>
    </main>
  );
}
