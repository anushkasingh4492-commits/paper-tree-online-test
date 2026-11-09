"use client";

import { useState } from "react";
import { Trophy, Lock } from "lucide-react";
import Image from "next/image";
import { Card } from "@/components/ui/Card";
import type { DashboardInsights } from "@/types/dashboard";

export function TrophyCard({ trophy }: { trophy: DashboardInsights["badges"][number] }) {
  const tierNames = ["", "I", "II", "III", "IV", "V"];
  const tierLabel = tierNames[trophy.tier] || "";
  const progressPct = Math.min((trophy.progress / Math.max(1, trophy.target)) * 100, 100);

  return (
    <Card
      variant={trophy.earned ? "default" : "subtle"}
      padding="md"
      radius="large"
      className={`
        relative overflow-hidden group border border-border-default transition-all duration-300
        ${trophy.earned
          ? "bg-gradient-to-br from-amber-100 via-yellow-100 to-orange-100"
          : "bg-white/30 border-white/20 backdrop-blur-sm"
        }
      `}
    >
      {/* Stacked card effect - 2 cards behind rotated 5deg */}
      <div className="absolute inset-0 -z-10 bg-current/10 rounded-[16px] transform rotate-[5deg] scale-[1.02] opacity-50 pointer-events-none" />
      <div className="absolute inset-0 -z-20 bg-current/10 rounded-[16px] transform rotate-[-5deg] scale-[1.04] opacity-30 pointer-events-none" />

      <div className="relative z-10 flex flex-col items-center gap-3">
        <div className="relative flex h-16 w-16 items-center justify-center rounded-full">
          {trophy.asset ? (
            <Image
              src={trophy.asset}
              alt={`${trophy.name}${tierLabel ? ` ${tierLabel}` : ""} badge`}
              width={56}
              height={56}
              className={`h-14 w-14 object-contain drop-shadow-md ${trophy.earned ? "" : "grayscale opacity-65"}`}
            />
          ) : (
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white/40 backdrop-blur-sm">
              <Trophy size={28} className={trophy.earned ? "text-yellow-500" : "text-slate-400"} />
            </div>
          )}
          {!trophy.earned && (
            <span className="absolute -right-1 -top-1 flex h-6 w-6 items-center justify-center rounded-full border-2 border-white bg-slate-700 text-white shadow">
              <Lock size={12} />
            </span>
          )}
        </div>

        <div className="text-center">
          <div className="text-xs font-black text-text-primary">{trophy.name}</div>
          <div className="text-[10px] font-semibold text-text-body">{tierLabel}</div>
          {!trophy.earned && <div className="text-[9px] font-bold uppercase tracking-wider text-text-supporting-label">Locked</div>}
        </div>

        {/* Progress Indicator */}
        <div className="w-full mt-2">
          <div className="flex justify-between text-[9px] font-bold text-text-body mb-1">
            <span>{trophy.progress}</span>
            <span>/{trophy.target}</span>
          </div>
          <div className="h-1.5 rounded-full bg-white/30 overflow-hidden">
            <div
              className="h-full rounded-full bg-gradient-to-r from-yellow-400 to-orange-500 transition-all duration-700"
              style={{ width: `${progressPct}%` }}
            />
          </div>
        </div>
      </div>
    </Card>
  );
}

export function TrophyWall({ badges }: { badges: DashboardInsights["badges"] }) {
  const [category, setCategory] = useState("All");

  const categories = ["All", ...new Set(badges.map((badge) => badge.category))];
  const filteredTrophies = category === "All" ? badges : badges.filter((badge) => badge.category === category);

  return (
    <section className="w-full">
      <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-4 mb-5">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Trophy size={18} className="text-yellow-500" />
            <h2 className="text-[18px] font-black text-text-primary">Trophy Wall</h2>
          </div>
          <p className="text-[11px] text-text-body">Earn trophies, upgrade titles, and unlock more!</p>
        </div>
        <a href="#" className="text-[11px] font-bold text-brand-purple hover:underline flex items-center gap-1">
          VIEW ALL TROPHIES →
        </a>
      </div>

      {/* Category Tabs */}
      <div className="flex gap-2 overflow-x-auto pb-2 mb-4 scrollbar-hide">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setCategory(cat)}
            className={`px-4 py-2 rounded-full text-[10px] font-bold uppercase tracking-wider transition-all ${
              category === cat
                ? "bg-brand-primary text-white shadow-md"
                : "bg-surface-subtle text-text-body hover:bg-surface-elevated"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Trophy Grid - 3 columns */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {filteredTrophies.length
          ? filteredTrophies.map((trophy) => <TrophyCard key={trophy.id} trophy={trophy} />)
          : <p className="text-sm text-text-body">Your badges will appear here as you complete tests.</p>}
      </div>
    </section>
  );
}