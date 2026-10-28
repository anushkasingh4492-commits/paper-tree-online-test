"use client";

import Image from "next/image";

export function avatarPath(key?: string | null) {
  if (!key || !/^(girl|boy)-(0[1-9]|1[0-9]|20)$/.test(key)) return null;
  return `/avatars/${key}.webp`;
}

export default function StudentAvatar({ avatarKey, name, size = 40, className = "" }: { avatarKey?: string | null; name?: string; size?: number; className?: string }) {
  const src = avatarPath(avatarKey);
  const initials = String(name || "Student").trim().split(/\s+/).slice(0, 2).map((part) => part[0]?.toUpperCase() || "").join("") || "S";
  return src ? <Image src={src} alt={`${name || "Student"}'s avatar`} width={size} height={size} className={`shrink-0 rounded-full object-cover ring-2 ring-white/20 ${className}`} /> : <span aria-label={`${name || "Student"} avatar`} className={`inline-flex shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-violet-500 to-indigo-600 font-black text-white ${className}`} style={{ width: size, height: size, fontSize: Math.max(10, size * .32) }}>{initials}</span>;
}
