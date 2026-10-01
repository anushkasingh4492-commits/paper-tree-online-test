"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";

type Props = {
  studentName: string;
  activeTest?: boolean;
};

export default function StudentAccountMenu({ studentName, activeTest = false }: Props) {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [confirmLogout, setConfirmLogout] = useState(false);
  const [loggingOut, setLoggingOut] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  const initials = String(studentName || "Student")
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part.charAt(0).toUpperCase())
    .join("") || "S";

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
        <span className="w-8 h-8 rounded-full bg-gradient-to-br from-[#6944e8] to-[#4f2bd5] text-white flex items-center justify-center text-xs font-black">
          {initials}
        </span>
        <span className="hidden sm:block max-w-[130px] truncate text-[11px] font-bold text-[#33405a]">
          {studentName || "Student"}
        </span>
        <span className="text-[11px] text-[#8a91a0]">⌄</span>
      </button>

      {open && (
        <div className="absolute right-0 top-[calc(100%+8px)] z-[100] w-64 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl">
          <div className="border-b border-slate-100 bg-slate-50 px-4 py-3">
            <div className="text-sm font-black text-slate-900 truncate">{studentName || "Student"}</div>
            <div className="mt-0.5 text-[10px] font-bold uppercase tracking-wider text-slate-400">Student Account</div>
          </div>

          <div className="p-2">
            <MenuItem icon="👤" label="My Profile" onClick={() => router.push("/profile")} />
            <MenuItem icon="📊" label="My Stats" onClick={() => router.push("/stats")} />
            <MenuItem icon="📝" label="Test History" onClick={() => router.push("/history")} />
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
