"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AcademyBranding from "@/components/AcademyBranding";
import StudentAccountMenu from "@/components/StudentAccountMenu";
import StudentInsights from "@/components/StudentInsights";

export default function StatsPage() {
  const router = useRouter();
  const [studentName, setStudentName] = useState("Student");
  useEffect(() => { setStudentName(localStorage.getItem("studentName") || "Student"); }, []);
  return <main className="min-h-screen bg-[#f8f9fc] text-slate-900">
    <header className="h-[72px] bg-white border-b border-slate-200 px-5 lg:px-8 flex items-center justify-between"><AcademyBranding variant="compact" /><StudentAccountMenu studentName={studentName} /></header>
    <div className="mx-auto max-w-[1200px] p-5 lg:p-8"><button onClick={() => router.push("/dashboard")} className="text-xs font-bold text-indigo-600">← Dashboard</button><h1 className="mt-5 text-3xl font-black">My Stats</h1><p className="mt-1 mb-7 text-sm text-slate-500">Your performance, level, streak and achievements.</p><StudentInsights /></div>
  </main>;
}
