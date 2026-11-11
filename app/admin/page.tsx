"use client";

import { useRouter } from "next/navigation";
import { ArrowRight, BookOpen, Building2, KeyRound, LogOut, ShieldCheck, Upload, type LucideIcon } from "lucide-react";

type Accent = "blue" | "orange" | "green" | "purple";
type ManagementCardProps = { title: string; description: string; icon: LucideIcon; accent: Accent; onClick: () => void };

const accents: Record<Accent, { icon: string; top: string; bottom: string }> = {
  blue: { icon: "bg-blue-50 text-blue-600", top: "bg-blue-500/15", bottom: "bg-blue-400/10" },
  orange: { icon: "bg-orange-50 text-orange-500", top: "bg-orange-400/15", bottom: "bg-orange-300/10" },
  green: { icon: "bg-emerald-50 text-emerald-600", top: "bg-emerald-400/15", bottom: "bg-emerald-300/10" },
  purple: { icon: "bg-purple-50 text-purple-600", top: "bg-purple-400/15", bottom: "bg-purple-300/10" },
};

function ManagementCard({ title, description, icon: Icon, accent, onClick }: ManagementCardProps) {
  const style = accents[accent];

  return (
    <button type="button" onClick={onClick} className="group relative flex min-h-[180px] w-full items-center gap-5 overflow-hidden rounded-large border border-white/90 bg-white p-5 text-left shadow-[0_4px_12px_rgba(30,50,100,0.08)] transition duration-200 hover:-translate-y-1 hover:shadow-md focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-primary sm:gap-6 sm:p-7">
      <span className={`pointer-events-none absolute -right-16 -top-24 h-52 w-52 rounded-full ${style.top}`} />
      <span className={`pointer-events-none absolute -bottom-24 -right-16 h-52 w-52 rounded-full ${style.bottom}`} />
      <span className={`relative z-10 flex h-16 w-16 shrink-0 items-center justify-center rounded-large sm:h-24 sm:w-24 ${style.icon}`}>
        <Icon size={34} strokeWidth={2.2} className="sm:hidden" />
        <Icon size={42} strokeWidth={2.2} className="hidden sm:block" />
      </span>
      <span className="relative z-10 min-w-0 flex-1">
        <span className="block text-lg font-extrabold text-text-primary sm:text-xl">{title}</span>
        <span className="mt-2 block max-w-md text-sm leading-6 text-text-body sm:text-base">{description}</span>
      </span>
      <span className="relative z-10 flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-border-default bg-white/80 text-text-primary shadow-sm transition-transform duration-200 group-hover:translate-x-1 sm:h-12 sm:w-12">
        <ArrowRight size={22} aria-hidden="true" />
      </span>
    </button>
  );
}

export default function AdminPage() {
  const router = useRouter();
  const sections: ManagementCardProps[] = [
    { title: "Academy Management", description: "Manage academies, branding, and administrative settings for all institutions.", icon: Building2, accent: "blue", onClick: () => router.push("/admin/academies") },
    { title: "Batch Course Setup", description: "Create academy batches for MHT-CET, NEET, JEE, and CAT with question-bank imports.", icon: BookOpen, accent: "orange", onClick: () => router.push("/academy-admin/batches") },
    { title: "Upload Dataset", description: "Import question-bank datasets (JSON, CSV, Excel) by course or subject.", icon: Upload, accent: "green", onClick: () => router.push("/admin/upload-dataset") },
    { title: "Password Management", description: "Reset passwords for students and teachers whenever required.", icon: KeyRound, accent: "purple", onClick: () => router.push("/admin/password-reset") },
  ];

  function logout() {
    document.cookie = "master_session=; Max-Age=0; path=/";
    router.replace("/login");
  }

  return (
    <main className="admin-page flex min-h-screen text-text-primary">
      <aside className="hidden w-64 shrink-0 border-r border-border-default bg-white/80 lg:flex lg:flex-col">
        <div className="flex h-20 items-center gap-3 border-b border-border-default px-6">
          <div className="flex h-10 w-10 items-center justify-center rounded-card bg-brand-primary text-lg font-black text-white shadow-sm">P</div>
          <div><p className="font-extrabold leading-tight">Paper Tree</p><p className="text-[10px] font-bold tracking-[0.12em] text-text-body">ADMIN CONTROL</p></div>
        </div>
        <nav className="px-4 py-6" aria-label="Master admin navigation">
          <p className="mb-3 px-3 text-[11px] font-bold uppercase tracking-wide text-text-tertiary">Workspace</p>
          <div className="space-y-1">
            <a href="#dashboard" className="flex items-center gap-3 rounded-card bg-brand-primary/10 px-3 py-3 text-sm font-bold text-brand-primary"><Building2 size={20} aria-hidden="true" /> Dashboard</a>
            {sections.map(({ title, icon: Icon, onClick }) => <button key={title} type="button" onClick={onClick} className="flex w-full items-center gap-3 rounded-card px-3 py-3 text-left text-sm font-semibold text-text-secondary transition hover:bg-surface-subtle hover:text-brand-primary"><Icon size={20} aria-hidden="true" /> {title}</button>)}
          </div>
        </nav>
        <button type="button" onClick={logout} className="mt-auto flex items-center gap-3 border-t border-border-default px-7 py-6 text-sm font-bold text-text-secondary transition hover:bg-surface-subtle hover:text-state-error"><LogOut size={20} aria-hidden="true" /> Logout</button>
      </aside>

      <div className="min-w-0 flex-1">
        <header className="flex h-20 items-center justify-between border-b border-white/70 bg-white/70 px-5 backdrop-blur-sm sm:px-8 lg:justify-end">
          <div className="flex items-center gap-3 lg:hidden"><div className="flex h-10 w-10 items-center justify-center rounded-card bg-brand-primary text-lg font-black text-white">P</div><p className="font-extrabold">Paper Tree</p></div>
          <div className="flex items-center gap-3"><span className="rounded-card bg-white px-3 py-2 text-sm font-semibold text-text-secondary shadow-sm">Master Admin</span><button type="button" onClick={logout} className="rounded-card border border-border-default bg-white px-3 py-2 text-sm font-bold text-text-secondary transition hover:bg-surface-subtle">Logout</button></div>
        </header>
        <div id="dashboard" className="mx-auto w-full max-w-[1440px] px-5 py-10 sm:px-8 lg:px-12 lg:py-14">
          <header className="mb-10 lg:mb-12"><h1 className="text-3xl font-extrabold tracking-tight text-text-primary sm:text-4xl">Welcome back, <span className="text-brand-action-blue">Admin</span></h1><p className="mt-2 max-w-3xl text-base text-text-body">Manage Paper Tree academies and their complete administration from one central dashboard.</p></header>
          <section className="grid grid-cols-1 gap-card-gap xl:grid-cols-2" aria-label="Master admin tools">{sections.map((section) => <ManagementCard key={section.title} {...section} />)}</section>
          <section className="mt-4 flex items-center gap-4 rounded-large border border-brand-primary/15 bg-white/80 p-5 shadow-sm sm:gap-6 sm:p-6" aria-label="Admin access"><div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-card bg-brand-primary/10 text-brand-action-blue sm:h-16 sm:w-16"><ShieldCheck size={34} aria-hidden="true" /></div><div className="hidden h-12 w-0.5 bg-brand-action-blue sm:block" /><div><h2 className="text-lg font-extrabold">Admin Access</h2><p className="text-sm text-text-body">You have full administrative control over academy management.</p></div></section>
        </div>
      </div>
    </main>
  );
}
