"use client";

import { useRouter } from "next/navigation";
import { Building2, BookOpen, Upload, Key, Shield } from "lucide-react";

export default function AdminPage() {
  const router = useRouter();

  function logout() {
    document.cookie = "master_session=; Max-Age=0; path=/";
    router.replace("/login");
  }

  return (
    <main className="min-h-screen bg-surface-app-bg text-text-primary">
      {/* HEADER */}
      <header className="border-b border-border-default bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-brand-primary text-lg font-black text-white shadow-sm">
              P
            </div>
            <div>
              <h1 className="text-lg font-extrabold">Paper Tree</h1>
              <p className="text-[10px] font-bold tracking-[0.15em] text-text-body">MASTER ADMIN</p>
            </div>
          </div>
          <button
            onClick={logout}
            className="rounded-xl border border-border-default bg-surface-surface px-4 py-2.5 text-sm font-bold text-text-tertiary transition hover:border-border-default hover:bg-surface-subtle"
          >
            🚪 Logout
          </button>
        </div>
      </header>

      {/* CONTENT */}
      <div className="mx-auto max-w-7xl px-6 py-12">
        {/* HERO - Center aligned per spec */}
        <section className="text-center flex flex-col items-center justify-center py-12 px-4 relative overflow-hidden">
          {/* Abstract Geometry Details */}
          <div className="absolute top-8 left-12 w-8 h-8 rounded-full bg-blue-300 opacity-40 blur-xs" />
          <div className="absolute top-12 right-16 w-10 h-10 rounded-full bg-orange-300 opacity-40 blur-xs" />

          <div className="relative z-10">
            <h2 className="text-3xl md:text-4xl font-extrabold text-blue-600 tracking-tight mb-2">
              Admin Control Center
            </h2>
            <p className="text-slate-500 max-w-xl text-sm md:text-base mb-4">
              Manage Paper Tree academies and their complete administration from one central dashboard.
            </p>
            {/* Small decorative centered horizontal split element */}
            <div className="w-16 h-0.5 bg-slate-200 mx-auto" />
          </div>
        </section>

        {/* ACTION GRID - 2x2 layout */}
        <section className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-6xl mx-auto px-4 mt-6">

          {/* Card 1: Academies */}
          <button
            type="button"
            onClick={() => router.push("/admin/academies")}
            className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex items-start space-x-5 hover:shadow-md transition-shadow duration-200"
          >
            <div className="w-16 h-16 rounded-xl flex items-center justify-center shrink-0 bg-blue-50 text-blue-600">
              <Building2 size={24} />
            </div>
            <div className="flex flex-col text-left">
              <h4 className="text-lg font-bold text-slate-800 mb-1">Academy Management</h4>
              <p className="text-xs md:text-sm text-slate-400 leading-relaxed">
                Manage academies, branding, and administrative settings for all institutions.
              </p>
            </div>
          </button>

          {/* Card 2: Batch Course Setup */}
          <button
            type="button"
            onClick={() => router.push("/academy-admin/batches")}
            className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex items-start space-x-5 hover:shadow-md transition-shadow duration-200"
          >
            <div className="w-16 h-16 rounded-xl flex items-center justify-center shrink-0 bg-orange-50 text-orange-600">
              <BookOpen size={24} />
            </div>
            <div className="flex flex-col text-left">
              <h4 className="text-lg font-bold text-slate-800 mb-1">Batch Course Setup</h4>
              <p className="text-xs md:text-sm text-slate-400 leading-relaxed">
                Create academy batches for MHT-CET, NEET, JEE, and CAT with question-bank imports.
              </p>
            </div>
          </button>

          {/* Card 3: Upload Dataset */}
          <button
            type="button"
            onClick={() => router.push("/admin/upload-dataset")}
            className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex items-start space-x-5 hover:shadow-md transition-shadow duration-200"
          >
            <div className="w-16 h-16 rounded-xl flex items-center justify-center shrink-0 bg-emerald-50 text-emerald-600">
              <Upload size={24} />
            </div>
            <div className="flex flex-col text-left">
              <h4 className="text-lg font-bold text-slate-800 mb-1">Upload Dataset</h4>
              <p className="text-xs md:text-sm text-slate-400 leading-relaxed">
                Import question-bank datasets (JSON, CSV, Excel) by course/subject.
              </p>
            </div>
          </button>

          {/* Card 4: Password Management */}
          <button
            type="button"
            onClick={() => router.push("/admin/password-reset")}
            className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex items-start space-x-5 hover:shadow-md transition-shadow duration-200"
          >
            <div className="w-16 h-16 rounded-xl flex items-center justify-center shrink-0 bg-purple-50 text-purple-600">
              <Key size={24} />
            </div>
            <div className="flex flex-col text-left">
              <h4 className="text-lg font-bold text-slate-800 mb-1">Password Management</h4>
              <p className="text-xs md:text-sm text-slate-400 leading-relaxed">
                Reset passwords for students and teachers whenever required.
              </p>
            </div>
          </button>

        </section>

        {/* ACCESS VERIFICATION BANNER */}
        <div className="w-full bg-blue-50/60 rounded-xl p-4 border border-blue-100/50 flex items-center space-x-3 mt-8">
          <Shield className="text-blue-500 w-5 h-5" />
          <div>
            <p className="text-xs md:text-sm text-slate-500 font-medium">Master Admin Access</p>
            <p className="text-xs md:text-sm text-slate-500">
              You have full administrative control over academy management.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
