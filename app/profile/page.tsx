"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AcademyBranding from "@/components/AcademyBranding";
import StudentAccountMenu from "@/components/StudentAccountMenu";

type Payload = { success?: boolean; student?: { id?: string; name?: string; rollNumber?: string | null; email?: string | null }; error?: string };

export default function ProfilePage() {
  const router = useRouter();
  const [data, setData] = useState<Payload | null>(null);
  const [error, setError] = useState("");
  useEffect(() => { fetch("/api/dashboard", { cache: "no-store", credentials: "include" }).then(r => r.json()).then(setData).catch(() => setError("Unable to load your profile.")); }, []);
  const student = data?.student;
  return <main className="min-h-screen bg-[#f8f9fc] text-slate-900">
    <header className="h-[72px] bg-white border-b border-slate-200 px-5 lg:px-8 flex items-center justify-between"><AcademyBranding variant="compact" /><StudentAccountMenu studentName={student?.name || localStorageSafe("studentName", "Student")} /></header>
    <div className="mx-auto max-w-3xl p-5 lg:p-8">
      <button onClick={() => router.push("/dashboard")} className="text-xs font-bold text-indigo-600">← Dashboard</button>
      <h1 className="mt-5 text-3xl font-black">My Profile</h1>
      <p className="mt-1 text-sm text-slate-500">Your student account details.</p>
      {error ? <div className="mt-6 rounded-2xl bg-red-50 p-5 text-sm text-red-600">{error}</div> : <div className="mt-7 grid gap-4 sm:grid-cols-2">
        <Info label="Name" value={student?.name || "—"} /><Info label="Student ID" value={student?.id || "—"} /><Info label="Roll Number" value={student?.rollNumber || "—"} /><Info label="Email" value={student?.email || "—"} />
      </div>}
    </div>
  </main>;
}
function localStorageSafe(key: string, fallback: string) { if (typeof window === "undefined") return fallback; return localStorage.getItem(key) || fallback; }
function Info({ label, value }: { label: string; value: string }) { return <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><div className="text-[10px] font-black uppercase tracking-wider text-slate-400">{label}</div><div className="mt-2 text-base font-black text-slate-800 break-words">{value}</div></div>; }
