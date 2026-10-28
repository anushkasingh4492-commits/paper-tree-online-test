"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import StudentAvatar from "@/components/StudentAvatar";

type Props = {
  studentName: string;
  activeTest?: boolean;
};

export default function StudentAccountMenu({ studentName, activeTest = false }: Props) {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [confirmLogout, setConfirmLogout] = useState(false);
  const [loggingOut, setLoggingOut] = useState(false);
  const [avatarKey, setAvatarKey] = useState<string | null>(null);
  const [avatarPickerOpen, setAvatarPickerOpen] = useState(false);
  const [avatarSaving, setAvatarSaving] = useState(false);
  const [avatarError, setAvatarError] = useState("");
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let active = true;
    fetch("/api/student/avatar", { cache: "no-store", credentials: "include" })
      .then((response) => response.ok ? response.json() : null)
      .then((payload) => {
        if (!active) return;
        const key = typeof payload?.avatarKey === "string" ? payload.avatarKey : null;
        setAvatarKey(key);
        if (!key) setAvatarPickerOpen(true);
      })
      .catch(() => { /* Avatar prompt can be retried from the account menu. */ });
    return () => { active = false; };
  }, []);

  async function saveAvatar(key: string) {
    setAvatarSaving(true);
    setAvatarError("");
    try {
      const response = await fetch("/api/student/avatar", {
        method: "PATCH", credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ avatarKey: key }),
      });
      const payload = await response.json();
      if (!response.ok || !payload.success) throw new Error(payload.error || "Could not save avatar.");
      setAvatarKey(key);
      setAvatarPickerOpen(false);
    } catch (error) {
      setAvatarError(error instanceof Error ? error.message : "Could not save avatar.");
    } finally { setAvatarSaving(false); }
  }

  useEffect(() => {
    const onPointerDown = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", onPointerDown);
    return () => document.removeEventListener("mousedown", onPointerDown);
  }, []);

  async function logout() {
    if (loggingOut) return;
    setLoggingOut(true);
    localStorage.removeItem("studentName");
    localStorage.removeItem("username");
    localStorage.removeItem("studentId");
    try {
      await fetch("/api/logout", { method: "POST", credentials: "include" });
    } finally {
      router.replace("/student-login");
    }
  }

  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        aria-expanded={open}
        className="flex items-center gap-2 rounded-xl border border-[#e8eaf1] bg-white px-2 py-1.5 shadow-[0_2px_8px_rgba(30,35,60,.03)] hover:bg-[#f8f9fc] transition"
      >
        <StudentAvatar avatarKey={avatarKey} name={studentName} size={32} />
        <span className="hidden sm:block max-w-[130px] truncate text-[11px] font-bold text-[#33405a]">
          {studentName || "Student"}
        </span>
        <span className="text-[11px] text-[#8a91a0]">⌄</span>
      </button>

      {open && (
        <div className="absolute right-0 top-[calc(100%+8px)] z-[100] w-64 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl">
          <div className="border-b border-slate-100 bg-slate-50 px-4 py-3">
            <div className="flex items-center gap-3">
              <StudentAvatar avatarKey={avatarKey} name={studentName} size={42} />
              <div className="min-w-0"><div className="text-sm font-black text-slate-900 truncate">{studentName || "Student"}</div>
              <button type="button" onClick={() => { setOpen(false); setAvatarPickerOpen(true); }} className="mt-1 text-[10px] font-black text-indigo-600 hover:underline">Change avatar</button></div>
            </div>
            <div className="mt-0.5 text-[10px] font-bold uppercase tracking-wider text-slate-400">Student Account</div>
          </div>

          <div className="p-2">
            <MenuItem icon="👤" label="My Profile" onClick={() => router.push("/profile")} />
            <MenuItem icon="📊" label="My Stats" onClick={() => router.push("/stats")} />
            <MenuItem icon="📝" label="My Tests" onClick={() => router.push("/tests/test-summary")} />
            <MenuItem icon="🏆" label="My Achievements" onClick={() => router.push("/dashboard#trophy-wall")} />
            <MenuItem icon="🔐" label="Change Password" onClick={() => router.push("/change-password")} />

            <div className="my-1 border-t border-slate-100" />

            <button
              type="button"
              onClick={() => {
                setOpen(false);
                setConfirmLogout(true);
              }}
              className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-xs font-bold text-rose-600 hover:bg-rose-50 transition"
            >
              <span>🚪</span>
              Logout
            </button>
          </div>
        </div>
      )}

      {avatarPickerOpen && (
        <div className="fixed inset-0 z-[250] flex items-center justify-center bg-slate-950/70 p-3 sm:p-5 backdrop-blur-sm" role="dialog" aria-modal="true" aria-labelledby="avatar-picker-title">
          <div className="w-full max-w-2xl max-h-[92dvh] overflow-y-auto rounded-3xl bg-white p-4 sm:p-6 shadow-2xl">
            <div className="flex items-start justify-between gap-3">
              <div><div className="text-xs font-black uppercase tracking-[.18em] text-indigo-600">Make it yours</div><h2 id="avatar-picker-title" className="mt-1 text-xl sm:text-2xl font-black text-slate-900">Choose your student avatar</h2><p className="mt-1 text-xs sm:text-sm text-slate-500">Your avatar will appear beside your name around Paper Tree CBT.</p></div>
              {avatarKey && <button type="button" onClick={() => setAvatarPickerOpen(false)} className="rounded-xl px-3 py-2 text-sm font-bold text-slate-500 hover:bg-slate-100">Later</button>}
            </div>
            {avatarError && <p className="mt-3 rounded-lg bg-rose-50 p-2 text-xs text-rose-700">{avatarError}</p>}
            <div className="mt-4 grid grid-cols-4 sm:grid-cols-5 md:grid-cols-8 gap-2 sm:gap-3">
              {Array.from({ length: 40 }, (_, i) => {
                const key = `${i < 20 ? "girl" : "boy"}-${String((i % 20) + 1).padStart(2, "0")}`;
                return <button key={key} type="button" disabled={avatarSaving} onClick={() => void saveAvatar(key)} aria-label={`Choose avatar ${i + 1}`} className={`relative rounded-full p-0.5 transition hover:scale-105 focus:outline-none focus:ring-2 focus:ring-indigo-500 ${avatarKey === key ? "ring-2 ring-indigo-600 ring-offset-2" : ""}`}><img src={`/avatars/${key}.webp`} alt="" className="aspect-square w-full rounded-full object-cover" loading="lazy" />{avatarKey === key && <span className="absolute -right-1 -top-1 rounded-full bg-indigo-600 px-1.5 py-0.5 text-[9px] font-black text-white">✓</span>}</button>;
              })}
            </div>
            <p className="mt-4 text-center text-[11px] text-slate-400">{avatarSaving ? "Saving your choice…" : "Tap any avatar to select it. You can change it later."}</p>
          </div>
        </div>
      )}

      {confirmLogout && (
        <div className="fixed inset-0 z-[200] flex items-center justify-center bg-slate-950/60 p-4 backdrop-blur-sm" onClick={() => !loggingOut && setConfirmLogout(false)}>
          <div className="w-full max-w-sm rounded-3xl bg-white p-6 shadow-2xl" onClick={(event) => event.stopPropagation()}>
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-rose-50 text-xl">🚪</div>
            <h2 className="mt-4 text-center text-xl font-black text-slate-900">Log out?</h2>
            <p className="mt-2 text-center text-sm leading-6 text-slate-500">
              {activeTest
                ? "You are currently taking a test. Leaving now may submit or interrupt your test."
                : "You can sign in again whenever you want."}
            </p>
            <div className="mt-5 grid grid-cols-2 gap-3">
              <button type="button" disabled={loggingOut} onClick={() => setConfirmLogout(false)} className="rounded-xl border border-slate-200 px-4 py-3 text-xs font-black text-slate-700 hover:bg-slate-50 disabled:opacity-50">Cancel</button>
              <button type="button" disabled={loggingOut} onClick={() => void logout()} className="rounded-xl bg-rose-600 px-4 py-3 text-xs font-black text-white hover:bg-rose-700 disabled:opacity-50">{loggingOut ? "Logging out…" : "Logout"}</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function MenuItem({ icon, label, onClick }: { icon: string; label: string; onClick: () => void }) {
  return (
    <button type="button" onClick={onClick} className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-xs font-bold text-slate-700 hover:bg-slate-50 transition">
      <span className="w-6 text-center">{icon}</span>
      {label}
    </button>
  );
}
