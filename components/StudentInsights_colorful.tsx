"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Lock, Share2, Sparkles, Trophy, Zap, Target, MessageCircle,Swords } from "lucide-react";

type Badge = {
  id: string;
  name: string;
  icon: string;
  asset?: string | null;
  category: string;
  tier: number;
  earned: boolean;
  progress: number;
  target: number;
  detail: string;
  subject?: string | null;
  earnedAt?: string | null;
};

type Insights = {
  rank: number | null;
  batchSize: number;
  batchName: string;
  testsCompleted: number;
  qualifyingTests: number;
  averagePercentage: number;
  streak: number;
  maxStreak: number;
  lastActiveDate: string | null;
  points: number;
  level: number;
  levelName: string;
  nextLevelName: string | null;
  nextLevelAt: number | null;
  levelProgress: number;
  badges: Badge[];
  weakAreas: Array<{ chapter: string; subject: string; rate: number }>;
};

type Branding = { name?: string | null; logo_data?: string | null };

const LEVELS = [
  [1, "Rookie"], [2, "Rising Player"], [3, "Grinder"], [4, "Challenger"], [5, "Pro"],
  [6, "Elite"], [7, "Master"], [8, "Grandmaster"], [9, "Legend"], [10, "Mythic"], [11, "GOAT"],
] as const;

const CATEGORIES = ["All", "Score", "Streak", "Improvement", "Volume", "Mastery", "Rank", "Comeback", "Ultimate", "Hidden"];
const TIER_NAMES = ["", "I", "II", "III", "IV"];
const TIER_TARGETS = [0, 1, 10, 25, 50];
const COLORS: Record<string, string> = {
  Score: "from-amber-300 via-yellow-400 to-orange-500",
  Streak: "from-orange-400 via-red-500 to-pink-500",
  Improvement: "from-cyan-300 via-sky-500 to-indigo-600",
  Volume: "from-violet-300 via-purple-500 to-fuchsia-600",
  Mastery: "from-emerald-300 via-green-500 to-teal-600",
  Rank: "from-yellow-200 via-amber-400 to-orange-600",
  Comeback: "from-pink-300 via-rose-500 to-red-600",
  Ultimate: "from-fuchsia-300 via-violet-500 to-indigo-700",
};

function clamp(n: number, min = 0, max = 100) { return Math.min(max, Math.max(min, n)); }

export default function StudentInsights() {
  const router = useRouter();
  const [data, setData] = useState<Insights | null>(null);
  const [branding, setBranding] = useState<Branding | null>(null);
  const [loading, setLoading] = useState(true);
  const [revisionLoading, setRevisionLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [selectedBadge, setSelectedBadge] = useState<Badge | null>(null);
  const [sharing, setSharing] = useState(false);
  const [category, setCategory] = useState("All");

  useEffect(() => {
    Promise.all([
      fetch("/api/student/insights", { cache: "no-store", credentials: "include" }).then((r) => r.json()),
      fetch("/api/academy/branding", { cache: "no-store", credentials: "include" }).then((r) => r.json()).catch(() => null),
    ]).then(([insights, brand]) => {
      if (insights?.success) setData(insights);
      if (brand?.success) setBranding(brand);
    }).catch(() => undefined).finally(() => setLoading(false));
  }, []);

  async function createRevisionTest() {
    setRevisionLoading(true); setMessage("");
    try {
      const response = await fetch("/api/student/revision-test", { method: "POST", credentials: "include" });
      const value = await response.json();
      if (!response.ok || !value.success) throw new Error(value.error || "Could not create revision test.");
      router.push(`/test/${value.testId}`);
    } catch (error) { setMessage(error instanceof Error ? error.message : "Could not create revision test."); }
    finally { setRevisionLoading(false); }
  }

  async function shareBadge() {
    if (!selectedBadge || !data) return;
    setSharing(true);
    try {
      const canvas = document.createElement("canvas");
      canvas.width = 1200; canvas.height = 630;
      const ctx = canvas.getContext("2d");
      if (!ctx) return;
      const bg = ctx.createLinearGradient(0, 0, 1200, 630);
      bg.addColorStop(0, "#050816"); bg.addColorStop(.52, "#111a3c"); bg.addColorStop(1, "#3b176d");
      ctx.fillStyle = bg; ctx.fillRect(0, 0, 1200, 630);
      for (let i = 0; i < 70; i++) {
        ctx.fillStyle = `rgba(255,255,255,${0.025 + (i % 5) * .01})`;
        ctx.beginPath(); ctx.arc((i * 173) % 1200, (i * 83) % 630, 1 + (i % 4), 0, Math.PI * 2); ctx.fill();
      }
      ctx.fillStyle = "#a5b4fc"; ctx.font = "700 24px Arial"; ctx.fillText((branding?.name || "PAPER TREE").toUpperCase(), 70, 70);
      if (branding?.logo_data) {
        try {
          const img = new Image(); img.crossOrigin = "anonymous"; img.src = branding.logo_data;
          await new Promise<void>((resolve) => { img.onload = () => resolve(); img.onerror = () => resolve(); });
          if (img.complete && img.naturalWidth) ctx.drawImage(img, 1010, 32, 120, 80);
        } catch {}
      }
      if (selectedBadge.asset) {
        try {
          const badgeImg = new Image();
          badgeImg.crossOrigin = "anonymous";
          badgeImg.src = selectedBadge.asset;
          await new Promise<void>((resolve) => { badgeImg.onload = () => resolve(); badgeImg.onerror = () => resolve(); });
          if (badgeImg.complete && badgeImg.naturalWidth) ctx.drawImage(badgeImg, 58, 110, 112, 112);
        } catch {}
      } else {
        ctx.fillStyle = "#fff"; ctx.font = "900 86px Arial"; ctx.fillText(selectedBadge.icon || "🏆", 72, 200);
      }
      ctx.font = "900 58px Arial"; ctx.fillText(`${selectedBadge.name.toUpperCase()}${selectedBadge.tier ? ` ${TIER_NAMES[selectedBadge.tier]}` : ""}`, 190, 190);
      ctx.fillStyle = "#cbd5e1"; ctx.font = "600 28px Arial"; ctx.fillText(selectedBadge.detail.slice(0, 58), 76, 252);
      ctx.fillStyle = "#fff"; ctx.font = "900 42px Arial"; ctx.fillText(`LEVEL ${data.level} • ${data.levelName}`, 76, 365);
      ctx.fillStyle = "#fbbf24"; ctx.font = "900 36px Arial"; ctx.fillText(`🔥 ${data.streak} DAY STREAK`, 76, 425);
      ctx.fillStyle = "#94a3b8"; ctx.font = "600 22px Arial"; ctx.fillText("Keep learning. Keep leveling up.", 76, 535);
      const blob = await new Promise<Blob | null>((resolve) => canvas.toBlob(resolve, "image/png"));
      if (!blob) return;
      const file = new File([blob], `${selectedBadge.id}-achievement.png`, { type: "image/png" });
      if (navigator.share && navigator.canShare?.({ files: [file] })) {
        await navigator.share({ title: `${selectedBadge.name} unlocked!`, text: `I unlocked ${selectedBadge.name} on ${branding?.name || "Paper Tree"}!`, files: [file] });
      } else {
        const url = URL.createObjectURL(blob); const a = document.createElement("a"); a.href = url; a.download = file.name; a.click(); URL.revokeObjectURL(url);
      }
    } finally { setSharing(false); }
  }

  function shareWhatsApp() {
    if (!selectedBadge || !data) return;
    const tier = selectedBadge.tier ? ` ${TIER_NAMES[selectedBadge.tier]}` : "";
    const text = `🏆 I unlocked ${selectedBadge.name}${tier}! 🔥 ${data.streak} day streak • Level ${data.level} ${data.levelName}.`;
    window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, "_blank", "noopener,noreferrer");
  }

  if (loading || !data) return null;
  const filtered = data.badges.filter((b) => category === "All" || b.category === category);
  const earned = data.badges.filter((b) => b.earned);
  const levelIndex = Math.max(0, data.level - 1);
  const nextName = data.nextLevelName;
  const safeSelectedBadge = selectedBadge
  ? {
      ...selectedBadge,
      name:
        typeof selectedBadge.name === "string"
          ? selectedBadge.name
          : "Achievement",
      icon:
        typeof selectedBadge.icon === "string"
          ? selectedBadge.icon
          : "🏆",
      asset:
        typeof selectedBadge.asset === "string" && selectedBadge.asset
          ? selectedBadge.asset
          : null,
      category:
        typeof selectedBadge.category === "string"
          ? selectedBadge.category
          : "Score",
      detail:
        typeof selectedBadge.detail === "string"
          ? selectedBadge.detail
          : "Keep completing tests to unlock this achievement.",
      tier:
        Number.isFinite(Number(selectedBadge.tier))
          ? Number(selectedBadge.tier)
          : 0,
      progress:
        Number.isFinite(Number(selectedBadge.progress))
          ? Number(selectedBadge.progress)
          : 0,
      target:
        Number.isFinite(Number(selectedBadge.target))
          ? Number(selectedBadge.target)
          : 1,
      earned: Boolean(selectedBadge.earned),
    }
  : null;

  return (
    <section className="mt-8 space-y-6">
      <style jsx>{`\n        @keyframes ptFloat {0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}\n        @keyframes ptPulse {0%,100%{box-shadow:0 0 0 0 rgba(129,140,248,0)}50%{box-shadow:0 0 42px 7px rgba(129,140,248,.22)}}\n        @keyframes ptFire {0%,100%{transform:scale(1) rotate(-3deg)}50%{transform:scale(1.14) rotate(3deg)}}\n        @keyframes ptShine {0%{transform:translateX(-140%) rotate(18deg)}100%{transform:translateX(240%) rotate(18deg)}}\n        @keyframes ptPop {0%{transform:scale(.84);opacity:0}100%{transform:scale(1);opacity:1}}\n        @keyframes ptSpark {0%,100%{opacity:.25;transform:scale(.8)}50%{opacity:1;transform:scale(1.2)}}\n        .pt-float{animation:ptFloat 4s ease-in-out infinite}.pt-pulse{animation:ptPulse 3s ease-in-out infinite}.pt-fire{animation:ptFire 1.1s ease-in-out infinite}.pt-pop{animation:ptPop .35s ease-out both}.pt-spark{animation:ptSpark 1.8s ease-in-out infinite}\n      `}</style>

      <div className="relative overflow-hidden rounded-[32px] border border-indigo-400/20 bg-[radial-gradient(circle_at_85%_5%,rgba(99,102,241,.4),transparent_28%),radial-gradient(circle_at_15%_100%,rgba(236,72,153,.2),transparent_30%),linear-gradient(135deg,#060917,#111a39_52%,#2a1452)] p-6 text-white shadow-2xl md:p-8 pt-pulse">
        <div className="absolute -right-16 -top-20 h-56 w-56 rounded-full bg-indigo-500/20 blur-3xl" />
        <div className="absolute -bottom-20 left-1/3 h-56 w-56 rounded-full bg-fuchsia-500/10 blur-3xl" />
        <div className="pointer-events-none absolute right-[28%] top-8 text-2xl pt-spark">✦</div><div className="pointer-events-none absolute right-[18%] top-28 text-xl pt-spark">✦</div>
        <div className="relative grid gap-8 lg:grid-cols-[1fr_auto] lg:items-center">
          <div>
            <div className="flex items-center gap-2 text-[11px] font-black uppercase tracking-[.25em] text-indigo-200"><Sparkles size={15}/> Player Progress</div>
            <div className="mt-3 flex items-end gap-4"><div className="text-7xl font-black leading-none tracking-[-.08em] text-transparent bg-clip-text bg-gradient-to-b from-white to-indigo-200">{data.level}</div><div className="pb-1"><div className="text-2xl font-black uppercase">{data.levelName}</div><div className="mt-1 text-xs font-bold text-slate-400">{data.qualifyingTests} qualifying tests</div></div></div>
            <div className="mt-6 max-w-2xl"><div className="flex items-center justify-between text-[11px] font-black uppercase tracking-wider text-slate-400"><span>Level progress</span><span>{nextName ? `${Math.max(0, (data.nextLevelAt || 0) - data.qualifyingTests)} more tests to ${nextName}` : "MAX LEVEL • GOAT"}</span></div><div className="mt-2 h-4 overflow-hidden rounded-full bg-white/10 p-1"><div className="relative h-full overflow-hidden rounded-full bg-gradient-to-r from-cyan-300 via-indigo-400 to-fuchsia-400 transition-all duration-1000" style={{width:`${clamp(data.levelProgress)}%`}}><span className="absolute inset-0 w-1/3 bg-white/30 blur-sm" style={{animation:"ptShine 2.5s linear infinite"}}/></div></div></div>
            <div className="mt-5 flex flex-wrap gap-2 text-xs font-black"><span className="rounded-full border border-white/10 bg-white/10 px-3 py-2">⚡ {data.points.toLocaleString()} XP</span><span className="rounded-full border border-white/10 bg-white/10 px-3 py-2">🏆 {earned.length} badges</span><span className="rounded-full border border-white/10 bg-white/10 px-3 py-2">🎯 {data.averagePercentage}% avg</span></div>
          </div>
          <div className="pt-float flex min-w-[210px] flex-col items-center rounded-[30px] border border-orange-300/20 bg-orange-400/10 px-9 py-7 backdrop-blur"><div className="pt-fire text-7xl">🔥</div><div className="mt-1 text-6xl font-black tracking-tight">{data.streak}</div><div className="text-[11px] font-black uppercase tracking-[.25em] text-orange-200">Day Streak</div><div className="mt-2 text-center text-[10px] font-semibold text-slate-400">Best: {data.maxStreak} days</div></div>
        </div>
      </div>

      <div className="grid gap-3 sm:grid-cols-3">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><div className="flex items-center gap-2 text-xs font-black uppercase tracking-wider text-slate-400"><Trophy size={15}/> Batch Rank</div><div className="mt-2 text-3xl font-black text-indigo-600">{data.rank ? `#${data.rank}` : "—"}</div><div className="mt-1 text-xs font-semibold text-slate-500">{data.batchName || "No batch assigned"}{data.batchSize ? ` • ${data.batchSize} students` : ""}</div></div>
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><div className="flex items-center gap-2 text-xs font-black uppercase tracking-wider text-slate-400"><Target size={15}/> Qualifying Tests</div><div className="mt-2 text-3xl font-black text-emerald-600">{data.qualifyingTests}</div><div className="mt-1 text-xs font-semibold text-slate-500">Max 3 per IST day count toward levels</div></div>
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><div className="flex items-center gap-2 text-xs font-black uppercase tracking-wider text-slate-400"><Zap size={15}/> XP Power</div><div className="mt-2 text-3xl font-black text-fuchsia-600">{data.points.toLocaleString()}</div><div className="mt-1 text-xs font-semibold text-slate-500">Keep completing challenges</div></div>
      </div>

      <div className="relative overflow-hidden rounded-[26px] border border-cyan-200 bg-gradient-to-r from-cyan-50 via-white to-indigo-50 p-5 shadow-sm"><div className="absolute right-2 top-0 text-8xl opacity-[.05]">⚔️</div><div className="relative flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"><div><div className="text-[10px] font-black uppercase tracking-[.2em] text-cyan-700">Test</div><h3 className="mt-1 text-2xl font-black text-slate-900">🎯 Target your weak areas</h3><p className="mt-1 text-xs font-semibold text-slate-500">A personalised challenge built from your performance.</p></div><button type="button" onClick={() => void createRevisionTest()} disabled={revisionLoading} className="rounded-xl bg-slate-950 px-5 py-3 text-xs font-black text-white shadow-lg transition hover:-translate-y-1 hover:shadow-xl disabled:opacity-60"><Swords className="mr-2 inline" size={15}/>{revisionLoading ? "BUILDING TEST..." : "START TEST"}</button></div>{message && <p className="mt-2 text-xs font-bold text-red-600">{message}</p>}</div>

      <div className="rounded-[30px] border border-slate-200 bg-white p-5 shadow-sm md:p-7">
        <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between"><div><div className="text-[10px] font-black uppercase tracking-[.2em] text-slate-400">Achievement Vault</div><h2 className="mt-1 text-2xl font-black tracking-tight text-slate-950">🏆 Trophy Wall</h2><p className="mt-1 text-xs font-semibold text-slate-500">Earn them. Upgrade them. Show them off.</p></div><div className="text-xs font-black text-slate-400">{earned.length}/{data.badges.length} unlocked</div></div>
        <div className="mt-5 flex gap-2 overflow-x-auto pb-1">{CATEGORIES.map((c)=><button key={c} onClick={()=>setCategory(c)} className={`whitespace-nowrap rounded-full px-3 py-2 text-[10px] font-black transition ${category===c?"bg-slate-950 text-white shadow":"bg-slate-100 text-slate-500 hover:bg-slate-200"}`}>{c}</button>)}</div>
        <div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
          {filtered.map((badge) => { const pct = badge.target ? clamp((badge.progress / badge.target) * 100) : badge.earned ? 100 : 0; const colors = COLORS[badge.category] || COLORS.Score; return <button key={badge.id} type="button" onClick={() => {
  setSelectedBadge({
    ...badge,
    name: String(badge.name ?? "Achievement"),
    icon: String(badge.icon ?? "🏆"),
    category: String(badge.category ?? "Score"),
    detail: String(
      badge.detail ??
        "Keep completing tests to unlock this achievement."
    ),
    tier: Number(badge.tier) || 0,
    progress: Number(badge.progress) || 0,
    target: Number(badge.target) || 1,
    earned: Boolean(badge.earned),
  });
}} className={`group relative overflow-hidden rounded-2xl border p-4 text-left transition duration-300 hover:-translate-y-1 hover:shadow-xl ${badge.earned?"border-slate-200 bg-white":"border-slate-200 bg-gradient-to-br from-white to-slate-50"}`}><div className={`relative mx-auto flex h-20 w-20 items-center justify-center rounded-[22px] ${badge.earned ? `bg-gradient-to-br ${colors} shadow-lg pt-float ${badge.tier===4?"ring-4 ring-yellow-300/70 scale-105":badge.tier===3?"ring-2 ring-violet-300/70":badge.tier===2?"ring-2 ring-cyan-300/60":""}` : "bg-gradient-to-br from-slate-100 to-slate-200 shadow-inner"}`}>
  {badge.asset ? (
    <img
      src={badge.asset}
      alt={badge.name}
      className={`h-[68px] w-[68px] object-contain drop-shadow-md transition duration-300 group-hover:scale-110 ${badge.earned ? "" : "opacity-65"}`}
    />
  ) : (
    <span className={`text-4xl ${badge.earned ? "" : "opacity-60 grayscale"}`}>{badge.icon || "🏆"}</span>
  )}
  {!badge.earned && (
    <span className="absolute -right-1 -top-1 flex h-7 w-7 items-center justify-center rounded-full border-2 border-white bg-slate-800 text-white shadow-md">
      <Lock size={13} />
    </span>
  )}
</div><div className={`mt-3 text-center text-xs font-black ${badge.earned?"text-slate-900":"text-slate-400"}`}>{badge.name}{badge.tier?` ${TIER_NAMES[badge.tier]}`:""}</div><div className="mt-1 text-center text-[9px] font-bold uppercase tracking-wider text-slate-400">{badge.earned ? (badge.tier > 0 && badge.tier < 4 ? `${badge.progress.toLocaleString()} / ${TIER_TARGETS[badge.tier + 1].toLocaleString()} to Tier ${TIER_NAMES[badge.tier + 1]}` : badge.detail) : `${badge.progress.toLocaleString()} / ${badge.target.toLocaleString()}`}</div>{!badge.earned&&<div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-200"><div className="h-full rounded-full bg-slate-400 transition-all" style={{width:`${pct}%`}}/></div>}</button>})}
        </div>
      </div>

      {data.weakAreas.length>0&&<div className="rounded-[26px] border border-rose-100 bg-white p-5 shadow-sm"><div className="text-[10px] font-black uppercase tracking-[.2em] text-rose-500">Boss Fight Queue</div><div className="mt-1 text-xl font-black text-slate-900">Chapters to conquer</div><div className="mt-4 grid gap-2 md:grid-cols-2">{data.weakAreas.map((area)=><div key={`${area.subject}-${area.chapter}`} className="rounded-xl border border-slate-100 bg-slate-50 p-3"><div className="flex items-center justify-between gap-3"><span className="truncate text-sm font-black text-slate-700">{area.chapter}</span><span className="text-xs font-black text-rose-500">{area.rate}% misses</span></div><div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-200"><div className="h-full rounded-full bg-gradient-to-r from-amber-400 to-rose-500" style={{width:`${clamp(area.rate)}%`}}/></div></div>)}</div></div>}

     {safeSelectedBadge && (
  <div
    className="fixed inset-0 z-[100] flex items-center justify-center bg-slate-950/75 p-4 backdrop-blur-md"
    onClick={() => setSelectedBadge(null)}
  >
    <div
      className="pt-pop w-full max-w-md overflow-hidden rounded-[32px] bg-white shadow-2xl"
      onClick={(e) => e.stopPropagation()}
    >
      {/* HEADER */}
      <div className="relative overflow-hidden bg-gradient-to-br from-slate-950 via-indigo-950 to-purple-950 p-8 text-center text-white">

        <div className="absolute -left-10 -top-10 h-40 w-40 rounded-full bg-fuchsia-500/20 blur-3xl" />
        <div className="absolute -right-10 bottom-0 h-40 w-40 rounded-full bg-cyan-500/20 blur-3xl" />

        <div className="relative">

          <div className="text-[10px] font-black uppercase tracking-[0.25em] text-indigo-200">
            {safeSelectedBadge.earned
              ? "✨ Achievement Unlocked"
              : "🔒 Locked Achievement"}
          </div>

          {/* BADGE */}
          <div
            className={`mx-auto mt-6 flex h-32 w-32 items-center justify-center rounded-[30px] bg-gradient-to-br ${
              COLORS[safeSelectedBadge.category] || COLORS.Score
            } text-7xl shadow-2xl ${
              safeSelectedBadge.earned
                ? "pt-float"
                : "grayscale"
            }`}
          >
            {safeSelectedBadge.earned
              ? safeSelectedBadge.icon
              : "🔒"}
          </div>

          {/* NAME */}
          <h3 className="mt-6 text-3xl font-black">
            {safeSelectedBadge.name}
            {safeSelectedBadge.tier > 0
              ? ` ${TIER_NAMES[safeSelectedBadge.tier] || ""}`
              : ""}
          </h3>

          {/* DETAIL */}
          <p className="mx-auto mt-3 max-w-sm text-sm font-semibold leading-6 text-slate-300">
            {safeSelectedBadge.detail}
          </p>

          {/* PROGRESS */}
          {!safeSelectedBadge.earned &&
            safeSelectedBadge.target > 0 && (
              <div className="mx-auto mt-6 max-w-xs">
                <div className="mb-2 flex justify-between text-[10px] font-black text-slate-400">
                  <span>PROGRESS</span>

                  <span>
                    {safeSelectedBadge.progress.toLocaleString()}
                    {" / "}
                    {safeSelectedBadge.target.toLocaleString()}
                  </span>
                </div>

                <div className="h-2 overflow-hidden rounded-full bg-white/10">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-cyan-400 to-indigo-500 transition-all"
                    style={{
                      width: `${clamp(
                        (safeSelectedBadge.progress /
                          Math.max(
                            1,
                            safeSelectedBadge.target
                          )) *
                          100
                      )}%`,
                    }}
                  />
                </div>
              </div>
            )}
        </div>
      </div>

      {/* ACTIONS */}
      <div className="space-y-3 p-5">

        {safeSelectedBadge.earned && (
          <div className="grid grid-cols-3 gap-2">

            <button
              type="button"
              disabled={sharing}
              onClick={() => void shareBadge()}
              className="flex items-center justify-center gap-1 rounded-xl bg-slate-950 px-3 py-3 text-[10px] font-black text-white transition hover:-translate-y-0.5 disabled:opacity-40"
            >
              <Share2 size={14} />
              SHARE
            </button>

            <button
              type="button"
              onClick={shareWhatsApp}
              className="flex items-center justify-center gap-1 rounded-xl bg-[#25D366] px-3 py-3 text-[10px] font-black text-white transition hover:-translate-y-0.5"
            >
              <MessageCircle size={14} />
              WHATSAPP
            </button>

            <button
              type="button"
              disabled={sharing}
              onClick={() => void shareBadge()}
              className="flex items-center justify-center gap-1 rounded-xl bg-gradient-to-r from-fuchsia-500 to-orange-400 px-3 py-3 text-[10px] font-black text-white transition hover:-translate-y-0.5 disabled:opacity-40"
            >
              
            </button>

          </div>
        )}

        {!safeSelectedBadge.earned && (
          <div className="rounded-2xl bg-slate-50 p-4 text-center">
            <div className="text-2xl">🔐</div>

            <p className="mt-2 text-xs font-bold text-slate-600">
              Keep completing tests to unlock this achievement.
            </p>
          </div>
        )}

        {safeSelectedBadge.earned && (
          <p className="text-center text-[10px] font-semibold text-slate-400">
            Share your achievement and show your progress.
          </p>
        )}

        <button
          type="button"
          onClick={() => setSelectedBadge(null)}
          className="w-full rounded-xl bg-slate-100 px-4 py-3 text-xs font-black text-slate-600 transition hover:bg-slate-200"
        >
          CLOSE
        </button>

      </div>
    </div>
  </div>
)}
    </section>
  );
}
