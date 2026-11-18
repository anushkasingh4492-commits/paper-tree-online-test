"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { isDemoPortalHostname } from "@/components/useDemoPortal";

type Lead = {
  id: string;
  academy_id: string;
  academy_code: string;
  institute_name: string;
  contact_name: string;
  email: string | null;
  phone: string | null;
  status: "DEMO_SET_UP" | "REJECTED" | "FOLLOW_UP" | "INTERESTED" | "CONVERTED";
  follow_up_at: string | null;
  students_converted: number;
  sale_amount: string;
  commission: string;
  created_at: string;
};

const statuses: Lead["status"][] = ["DEMO_SET_UP", "REJECTED", "FOLLOW_UP", "INTERESTED", "CONVERTED"];
const courseOptions = ["MHT-CET PCM", "MHT-CET PCB", "NEET PCB", "CAT", "JEE PCM"];

export default function SalesDashboardPage() {
  const router = useRouter();
  const [leads, setLeads] = useState<Lead[]>([]);
  const [instituteName, setInstituteName] = useState("");
  const [academyCode, setAcademyCode] = useState("");
  const [contactName, setContactName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [notes, setNotes] = useState("");
  const [adminName, setAdminName] = useState("");
  const [adminEmail, setAdminEmail] = useState("");
  const [adminPassword, setAdminPassword] = useState("");
  const [studentLimit, setStudentLimit] = useState("50");
  const [subscriptionMonths, setSubscriptionMonths] = useState("12");
  const [subscriptionTier, setSubscriptionTier] = useState<"BRONZE" | "SILVER" | "GOLD">("GOLD");
  const [subscriptionStart, setSubscriptionStart] = useState(() => new Date().toISOString().slice(0, 10));
  const [assignedCourses, setAssignedCourses] = useState<string[]>([]);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const convertedLeads = leads.filter((lead) => lead.status === "CONVERTED");

  async function load() {
    try {
      const response = await fetch("/api/sales/leads", { cache: "no-store" });
      const data = await response.json();
      if (!response.ok || !data.success) throw new Error(data.error || "Unable to load sales dashboard.");
      setLeads(data.leads);
      setError("");
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Unable to load sales dashboard.");
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

  async function addInstitute(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setMessage("");
    try {
      const response = await fetch("/api/sales/leads", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          instituteName,
          academyCode,
          contactName,
          email,
          phone,
          notes,
          adminName,
          adminEmail,
          adminPassword,
          studentLimit,
          subscriptionMonths,
          subscriptionTier,
          subscriptionStart,
          assignedCourses,
        }),
      });
      const data = await response.json();
      if (!response.ok || !data.success) throw new Error(data.error || "Unable to save institute demo.");
      setInstituteName("");
      setAcademyCode("");
      setContactName("");
      setEmail("");
      setPhone("");
      setNotes("");
      setAdminName("");
      setAdminEmail("");
      setAdminPassword("");
      setMessage("Active academy and academy-admin login created.");
      await load();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Unable to save institute demo.");
    }
  }

  async function updateLead(lead: Lead, form: HTMLFormElement) {
    const formData = new FormData(form);
    const status = String(formData.get("status")) as Lead["status"];
    const followUpAt = String(formData.get("followUpAt") || "");
    const studentsConverted = Number(formData.get("studentsConverted") || 0);
    const saleAmount = Number(formData.get("saleAmount") || 0);
    const response = await fetch(`/api/sales/leads/${lead.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status, followUpAt, studentsConverted, saleAmount }),
    });
    const data = await response.json();
    if (!response.ok || !data.success) throw new Error(data.error || "Unable to update institute status.");
    await load();
  }

  async function logout() {
    await fetch("/api/logout", { method: "POST" });
    router.replace("/login");
  }

  return (
    <main className="min-h-screen bg-slate-50 px-5 py-8 text-slate-900 sm:px-8">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8 flex flex-wrap items-center justify-between gap-3">
          <div><h1 className="text-3xl font-black">Sales dashboard</h1><p className="mt-1 text-slate-600">Track your institute demos and follow-ups.</p></div>
          <div className="flex gap-2"><button onClick={() => router.push("/student-login")} className="rounded-xl bg-indigo-700 px-4 py-2.5 font-bold text-white">Switch to student mode</button><button onClick={logout} className="rounded-xl border bg-white px-4 py-2.5 font-bold">Log out</button></div>
        </header>
        {error && <p role="alert" className="mb-5 rounded-xl bg-red-50 p-4 text-sm font-semibold text-red-700">{error}</p>}
        {message && <p role="status" className="mb-5 rounded-xl bg-emerald-50 p-4 text-sm font-semibold text-emerald-700">{message}</p>}
        <section className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-7">
          {[
            ["Institutes set up", leads.length],
            ["Rejected", leads.filter((lead) => lead.status === "REJECTED").length],
            ["Follow-up", leads.filter((lead) => lead.status === "FOLLOW_UP").length],
            ["Interested", leads.filter((lead) => lead.status === "INTERESTED").length],
            ["Converted", leads.filter((lead) => lead.status === "CONVERTED").length],
            ["Students converted", convertedLeads.reduce((sum, lead) => sum + Number(lead.students_converted), 0)],
            ["Total sales", `₹${convertedLeads.reduce((sum, lead) => sum + Number(lead.sale_amount), 0).toLocaleString("en-IN", { maximumFractionDigits: 2 })}`],
            ["Commission (10%)", `₹${convertedLeads.reduce((sum, lead) => sum + Number(lead.commission), 0).toLocaleString("en-IN", { maximumFractionDigits: 2 })}`],
          ].map(([label, value]) => <article key={label} className="rounded-2xl border bg-white p-5"><p className="text-sm font-semibold text-slate-500">{label}</p><p className="mt-2 text-3xl font-black">{value}</p></article>)}
        </section>
        <section className="mt-7 grid gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(280px,1fr)]">
          <div className="space-y-4">
            {loading ? <p className="rounded-xl border bg-white p-5 text-slate-500">Loading your institutes…</p> : leads.length === 0 ? <p className="rounded-xl border bg-white p-5 text-slate-500">No institute demos yet. Add your first institute.</p> : leads.map((lead) => <article key={lead.id} className="rounded-2xl border bg-white p-5 shadow-sm">
              <div className="flex flex-wrap justify-between gap-2"><div><h2 className="font-extrabold">{lead.institute_name}</h2><p className="mt-1 text-sm text-slate-500">Academy code: {lead.academy_code} · {lead.contact_name}{lead.phone ? ` · ${lead.phone}` : ""}{lead.email ? ` · ${lead.email}` : ""}</p></div><p className="text-xs font-bold uppercase text-slate-500">Added {new Date(lead.created_at).toLocaleDateString("en-IN")}</p></div>
              <form className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-5" onSubmit={(event) => { event.preventDefault(); void updateLead(lead, event.currentTarget).catch((reason: unknown) => setError(reason instanceof Error ? reason.message : "Unable to update status.")); }}>
                <label className="text-xs font-bold">Status<select name="status" defaultValue={lead.status} className="mt-1 w-full rounded-lg border px-2 py-2 text-sm">{statuses.map((status) => <option key={status} value={status}>{status.replaceAll("_", " ")}</option>)}</select></label>
                <label className="text-xs font-bold">Follow-up date<input name="followUpAt" type="date" defaultValue={lead.follow_up_at?.slice(0, 10) || ""} className="mt-1 w-full rounded-lg border px-2 py-2 text-sm" /></label>
                <label className="text-xs font-bold">Students converted<input name="studentsConverted" type="number" min="0" defaultValue={lead.students_converted} className="mt-1 w-full rounded-lg border px-2 py-2 text-sm" /></label>
                <label className="text-xs font-bold">Sale amount (₹)<input name="saleAmount" type="number" min="0" step="0.01" defaultValue={lead.sale_amount} className="mt-1 w-full rounded-lg border px-2 py-2 text-sm" /></label>
                <button className="self-end rounded-lg bg-blue-700 px-3 py-2 text-sm font-bold text-white">Save</button>
              </form>
            </article>)}
          </div>
          <form onSubmit={addInstitute} className="h-fit rounded-2xl border bg-white p-5 shadow-sm">
            <h2 className="text-lg font-extrabold">Set up an active academy</h2>
            <p className="mt-1 text-xs text-slate-500">This creates the academy and its admin login immediately.</p>
            <label className="mt-4 block text-sm font-bold">Institute name<input required maxLength={255} value={instituteName} onChange={(event) => setInstituteName(event.target.value)} className="mt-1 w-full rounded-lg border px-3 py-2 font-normal" /></label>
            <label className="mt-3 block text-sm font-bold">Academy code<input required maxLength={100} pattern="[A-Za-z0-9][A-Za-z0-9_-]+" value={academyCode} onChange={(event) => setAcademyCode(event.target.value.toUpperCase())} placeholder="e.g. ACAD01" className="mt-1 w-full rounded-lg border px-3 py-2 font-normal" /></label>
            <label className="mt-3 block text-sm font-bold">Institute contact<input required maxLength={150} value={contactName} onChange={(event) => setContactName(event.target.value)} className="mt-1 w-full rounded-lg border px-3 py-2 font-normal" /></label>
            <label className="mt-3 block text-sm font-bold">Contact email (optional)<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} className="mt-1 w-full rounded-lg border px-3 py-2 font-normal" /></label>
            <label className="mt-3 block text-sm font-bold">Phone (optional)<input value={phone} onChange={(event) => setPhone(event.target.value)} className="mt-1 w-full rounded-lg border px-3 py-2 font-normal" /></label>
            <h3 className="mt-5 border-t pt-4 font-extrabold">Academy admin login</h3>
            <label className="mt-3 block text-sm font-bold">Admin name<input required maxLength={150} value={adminName} onChange={(event) => setAdminName(event.target.value)} className="mt-1 w-full rounded-lg border px-3 py-2 font-normal" /></label>
            <label className="mt-3 block text-sm font-bold">Admin email<input required type="email" value={adminEmail} onChange={(event) => setAdminEmail(event.target.value)} className="mt-1 w-full rounded-lg border px-3 py-2 font-normal" /></label>
            <label className="mt-3 block text-sm font-bold">Admin password (minimum 6 characters)<input required minLength={6} type="password" value={adminPassword} onChange={(event) => setAdminPassword(event.target.value)} className="mt-1 w-full rounded-lg border px-3 py-2 font-normal" /></label>
            <h3 className="mt-5 border-t pt-4 font-extrabold">Active subscription</h3>
            <div className="mt-3 grid grid-cols-2 gap-3">
              <label className="text-sm font-bold">Student seats<input required type="number" min="1" value={studentLimit} onChange={(event) => setStudentLimit(event.target.value)} className="mt-1 w-full rounded-lg border px-3 py-2 font-normal" /></label>
              <label className="text-sm font-bold">Plan tier<select value={subscriptionTier} onChange={(event) => setSubscriptionTier(event.target.value as "BRONZE" | "SILVER" | "GOLD")} className="mt-1 w-full rounded-lg border px-3 py-2 font-normal"><option value="BRONZE">Bronze</option><option value="SILVER">Silver</option><option value="GOLD">Gold</option></select></label>
              <label className="text-sm font-bold">Duration (months)<input required type="number" min="1" max="120" value={subscriptionMonths} onChange={(event) => setSubscriptionMonths(event.target.value)} className="mt-1 w-full rounded-lg border px-3 py-2 font-normal" /></label>
              <label className="text-sm font-bold">Starts on<input required type="date" value={subscriptionStart} onChange={(event) => setSubscriptionStart(event.target.value)} className="mt-1 w-full rounded-lg border px-3 py-2 font-normal" /></label>
            </div>
            <fieldset className="mt-4"><legend className="text-sm font-bold">Courses</legend><div className="mt-2 grid grid-cols-2 gap-2">{courseOptions.map((course) => <label key={course} className="flex items-center gap-2 text-xs"><input type="checkbox" checked={assignedCourses.includes(course)} onChange={() => setAssignedCourses((current) => current.includes(course) ? current.filter((value) => value !== course) : [...current, course])} />{course}</label>)}</div></fieldset>
            <label className="mt-3 block text-sm font-bold">Notes (optional)<textarea value={notes} onChange={(event) => setNotes(event.target.value)} rows={3} className="mt-1 w-full rounded-lg border px-3 py-2 font-normal" /></label>
            <button className="mt-5 w-full rounded-xl bg-blue-700 px-4 py-3 font-extrabold text-white">Create active academy</button>
          </form>
        </section>
      </div>
    </main>
  );
}
