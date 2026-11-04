"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AcademyBranding from "@/components/AcademyBranding";
import StudentAccountMenu from "@/components/StudentAccountMenu";

type Test = { id: string; name?: string; exam?: string; score?: number | null; status?: string; date?: string; questionCount?: number };
type Payload = { success?: boolean; student?: { name?: string }; results?: Test[]; myTests?: Test[]; error?: string };

export default function HistoryPage() {
  const router = useRouter();
  const [data, setData] = useState<Payload | null>(null);
  const [studentName, setStudentName] = useState("Student");
  useEffect(() => { setStudentName(localStorage.getItem("studentName") || "Student"); fetch("/api/dashboard", { cache: "no-store", credentials: "include" }).then(r => r.json()).then(value => { setData(value); if (value?.student?.name) setStudentName(value.student.name); }).catch(() => undefined); }, []);
  const tests = (data?.myTests?.length ? data.myTests : data?.results || []);
  return <main className="min-h-screen bg-surface-app-bg text-text-primary"><header className="h-[72px] bg-white border-b border-border-default px-5 lg:px-8 flex items-center justify-between"><AcademyBranding variant="compact" /><StudentAccountMenu studentName={studentName} /></header><div className="mx-auto max-w-5xl p-5 lg:p-8"><button onClick={() => router.push("/dashboard")} className="text-xs font-bold text-brand-purple">← Dashboard</button><h1 className="mt-5 text-3xl font-black">Test History</h1><p className="mt-1 text-sm text-text-body">Your completed and recorded tests.</p><div className="mt-7 overflow-hidden rounded-2xl border border-border-default bg-white shadow-sm"><div className="grid grid-cols-[1fr_100px_120px] border-b border-border-default bg-surface-subtle px-5 py-3 text-[10px] font-black uppercase tracking-wider text-text-supporting-label"><span>Test</span><span>Score</span><span>Status</span></div>{tests.length ? tests.map((test, index) => <button key={`${test.id}-${index}`} type="button" onClick={() => router.push(`/test/result/${test.id}`)} className="grid w-full grid-cols-[1fr_100px_120px] items-center border-b border-border-default px-5 py-4 text-left hover:bg-surface-subtle last:border-0"><div><div className="text-sm font-black text-text-secondary">{test.name || test.exam || "Test"}</div><div className="mt-1 text-[10px] font-semibold text-text-supporting-label">{test.date || ""}</div></div><div className="text-sm font-black text-brand-purple">{test.score == null ? "—" : `${Number(test.score).toFixed(0)}%`}</div><div className="text-xs font-bold text-text-body">{test.status || "Completed"}</div></button>) : <div className="p-10 text-center text-sm font-semibold text-text-supporting-label">No test history yet.</div>}</div></div></main>;
}
