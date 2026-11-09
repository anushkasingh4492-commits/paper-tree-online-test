"use client";

import { useMemo, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { ArrowRight, LockKeyhole, Trophy } from "lucide-react";
import type { DashboardInsights } from "@/types/dashboard";

type Badge = DashboardInsights["badges"][number];
type BadgeGroup = { category: string; badges: Badge[] };

function BadgeArtwork({ badge, size = 36 }: { badge: Badge; size?: number }) {
  return badge.asset ? (
    <Image
      src={badge.asset}
      alt=""
      width={size}
      height={size}
      className="h-full w-full object-contain"
      unoptimized
    />
  ) : (
    <Trophy size={Math.round(size * 0.58)} className="text-amber-500" aria-hidden="true" />
  );
}

function BadgeDeck({
  group,
  expanded,
  onClick,
}: {
  group: BadgeGroup;
  expanded: boolean;
  onClick: () => void;
}) {
  const earned = group.badges.filter((badge) => badge.earned).length;
  const preview = group.badges.slice(0, 3);

  return (
    <button
      type="button"
      onClick={onClick}
      aria-expanded={expanded}
      className={`group relative flex h-[112px] w-[108px] shrink-0 flex-col items-center justify-between overflow-hidden rounded-xl border p-2.5 text-center transition hover:-translate-y-0.5 hover:shadow-md focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-primary ${
        expanded
          ? "border-brand-primary bg-brand-primary/5 shadow-sm"
          : "border-border-default bg-surface-surface"
      }`}
    >
      <span className="relative block h-[58px] w-full">
        {preview.map((badge, index) => (
          <span
            key={badge.id}
            className={`absolute top-1/2 flex h-10 w-10 -translate-y-1/2 items-center justify-center overflow-hidden rounded-lg border border-border-default bg-surface-surface p-1 shadow-sm ${
              badge.earned ? "" : "grayscale opacity-60"
            }`}
            style={{
              left: `calc(50% + ${(index - (preview.length - 1) / 2) * 22}px)`,
              transform: `translate(-50%, -50%) rotate(${(index - (preview.length - 1) / 2) * 9}deg)`,
              zIndex: preview.length - index,
            }}
          >
            <BadgeArtwork badge={badge} size={34} />
          </span>
        ))}
        {group.badges.length > preview.length && (
          <span className="absolute right-1 top-0 rounded-full bg-surface-subtle px-1.5 py-0.5 text-[8px] font-bold text-text-body">
            +{group.badges.length - preview.length}
          </span>
        )}
      </span>
      <span className="w-full truncate text-[10px] font-extrabold text-text-primary">
        {group.category}
      </span>
      <span className="text-[8px] font-semibold text-text-body">
        {earned} of {group.badges.length} earned
      </span>
    </button>
  );
}

function BadgeCard({ badge }: { badge: Badge }) {
  const progress = badge.target > 0
    ? Math.min(100, (badge.progress / badge.target) * 100)
    : 0;

  return (
    <article className="flex min-w-0 items-center gap-2.5 rounded-xl border border-border-default bg-surface-surface p-2.5">
      <span className={`relative flex h-10 w-10 shrink-0 items-center justify-center overflow-hidden rounded-lg bg-surface-subtle p-1 ${
        badge.earned ? "" : "grayscale opacity-60"
      }`}>
        <BadgeArtwork badge={badge} size={36} />
        {!badge.earned && (
          <span className="absolute inset-0 flex items-center justify-center bg-surface-surface/40 text-text-body">
            <LockKeyhole size={13} aria-label="Locked" />
          </span>
        )}
      </span>
      <span className="min-w-0 flex-1">
        <span className="block truncate text-[10px] font-bold text-text-primary">{badge.name}</span>
        <span className="mt-0.5 block text-[8px] text-text-body">
          {badge.progress} / {badge.target}
          {badge.tier > 0 ? ` · Tier ${badge.tier}` : ""}
        </span>
        <span className="mt-1 block h-1 overflow-hidden rounded-full bg-surface-subtle">
          <span
            className="block h-full rounded-full bg-gradient-to-r from-amber-400 to-orange-500"
            style={{ width: `${progress}%` }}
          />
        </span>
      </span>
    </article>
  );
}

export function TrophyWall({ badges }: { badges: DashboardInsights["badges"] }) {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const groups = useMemo(() => {
    const byCategory = new Map<string, Badge[]>();
    badges.forEach((badge) => {
      const current = byCategory.get(badge.category) ?? [];
      current.push(badge);
      byCategory.set(badge.category, current);
    });
    return Array.from(byCategory, ([category, categoryBadges]) => ({
      category,
      badges: categoryBadges,
    }));
  }, [badges]);
  const selectedGroup = groups.find((group) => group.category === selectedCategory);
  const earnedCount = badges.filter((badge) => badge.earned).length;

  return (
    <section className="w-full rounded-2xl border border-border-default bg-surface-surface p-3 shadow-sm sm:p-4">
      <div className="mb-3 flex items-center justify-between gap-3">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-1.5">
            <Trophy size={15} className="text-amber-500" />
            <h2 className="text-[15px] font-black text-text-primary">Trophy Wall</h2>
            <span className="text-[9px] font-bold text-text-body">
              {earnedCount} of {badges.length} earned
            </span>
          </div>
          <p className="mt-0.5 text-[9px] text-text-body">
            Each badge variety has its own deck. Select a deck to see every milestone.
          </p>
        </div>
        <Link
          href="/achievements"
          className="shrink-0 inline-flex items-center gap-1 text-[9px] font-bold text-brand-purple hover:underline"
        >
          View all <ArrowRight size={11} />
        </Link>
      </div>

      {groups.length ? (
        <>
          <div className="flex gap-2 overflow-x-auto pb-1">
            {groups.map((group) => (
              <BadgeDeck
                key={group.category}
                group={group}
                expanded={selectedCategory === group.category}
                onClick={() => setSelectedCategory(
                  selectedCategory === group.category ? null : group.category
                )}
              />
            ))}
          </div>
          {selectedGroup && (
            <div className="mt-3 border-t border-border-default pt-3">
              <div className="mb-2 flex items-center justify-between gap-2">
                <h3 className="text-[10px] font-extrabold text-text-primary">
                  {selectedGroup.category} badges
                </h3>
                <button
                  type="button"
                  onClick={() => setSelectedCategory(null)}
                  className="text-[9px] font-semibold text-text-body hover:text-brand-purple"
                >
                  Close deck
                </button>
              </div>
              <div className="grid max-h-56 grid-cols-1 gap-2 overflow-y-auto sm:grid-cols-2 xl:grid-cols-3">
                {selectedGroup.badges.map((badge) => (
                  <BadgeCard key={badge.id} badge={badge} />
                ))}
              </div>
            </div>
          )}
        </>
      ) : (
        <p className="py-4 text-center text-xs text-text-body">
          Your badge decks will appear as you start completing tests.
        </p>
      )}
    </section>
  );
}
