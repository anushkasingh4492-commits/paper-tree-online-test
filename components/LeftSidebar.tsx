"use client";

import { usePathname } from "next/navigation";
import { useState } from "react";
import Link from "next/link";
import { Icon, type IconName } from "./Icon";
import StudentAvatar from "./StudentAvatar";

const NAV_ITEMS: Array<{
  key: string;
  label: string;
  icon: IconName;
  href: string;
}> = [
  { key: "dashboard", label: "Dashboard", icon: "home", href: "/dashboard" },
  { key: "my-tests", label: "My Tests", icon: "test-tube", href: "/tests" },
  { key: "test-summary", label: "Test Summary", icon: "analytics", href: "/test-summary" },
  { key: "batch-leaderboard", label: "Batch Leaderboard", icon: "trophy", href: "/student/batch-leaderboard" },
  { key: "mistake-notebook", label: "Mistake Notebook", icon: "book", href: "/student/mistakes" },
  { key: "edit-profile", label: "Edit Profile", icon: "user", href: "/profile" },
  { key: "my-achievements", label: "My Achievements", icon: "star", href: "/achievements" },
  { key: "boss-fight-queue", label: "Boss Fight Queue", icon: "alert", href: "/boss-fight" },
  { key: "weak-areas-test", label: "Weak Areas Test", icon: "grid", href: "/tests/weak-areas" },
];

type StudentSummary = {
  firstName: string;
  lastName: string;
  courseName: string;
  avatarKey?: string | null;
};

export function LeftSidebar({
  className = "",
  student,
}: {
  className?: string;
  student: StudentSummary;
}) {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={`
        fixed xl:relative xl:inset-0 xl:top-0 xl:left-0 xl:h-screen xl:w-[220px] xl:border-r xl:border-border-default
        xl:flex xl:flex-col z-50
        ${className}
      `}
    >
      {/* Sidebar Brand */}
      <div className="h-[82px] px-5 flex items-center gap-3 border-b border-border-default bg-surface-surface">
        <div className="w-9 h-9 rounded-[11px] bg-brand-primary text-white flex items-center justify-center font-black text-lg shadow-sm">
          IC
        </div>
        <div className={`flex flex-col ${collapsed ? "hidden" : ""}`}>
          <div className="font-extrabold text-[15px] leading-4 text-text-primary">
            Infinity Classes
          </div>
          <div className="text-[9px] font-semibold tracking-[.17em] text-text-supporting-label mt-1">
            EDUCATIONAL STUDIO
          </div>
        </div>
        {collapsed && (
          <button
            onClick={() => setCollapsed(false)}
            className="ml-auto p-1.5 rounded-lg bg-surface-subtle text-text-secondary hover:bg-border-default hover:text-text-primary transition"
            aria-label="Expand sidebar"
          >
            <Icon name="chevron-right" size={16} />
          </button>
        )}
      </div>

      <div className={`px-4 pt-5 flex-1 overflow-y-auto ${collapsed ? "hidden" : ""}`}>
        <p className="px-2 mb-2 text-[9px] uppercase tracking-[.16em] font-bold text-text-supporting-label">
          Workspace
        </p>

        <nav className="space-y-1">
          {NAV_ITEMS.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.key}
                href={item.href}
                className={`w-full h-10 flex items-center gap-3 px-2.5 rounded-xl text-xs font-medium transition-all ${
                  isActive
                    ? "bg-surface-subtle text-brand-purple"
                    : "text-text-secondary hover:bg-surface-app-bg"
                }`}
              >
                <span className="w-7 h-7 rounded-lg flex items-center justify-center">
                  <Icon name={item.icon} size={16} className={isActive ? "text-brand-purple" : "text-text-secondary"} />
                </span>
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Bottom: collapsed toggle + profile */}
      {!collapsed && (
        <div className="px-4 pb-4 border-t border-border-default bg-surface-surface">
          <button
            onClick={() => setCollapsed(true)}
            className="w-full h-10 flex items-center justify-between gap-3 px-2.5 rounded-xl text-xs font-medium text-text-secondary hover:bg-surface-app-bg transition"
          >
            <span className="flex items-center gap-3">
              <span className="w-7 h-7 rounded-lg flex items-center justify-center">
                <Icon name="chevron-left" size={16} className="text-text-secondary" />
              </span>
              Collapse
            </span>
          </button>
          <div className="mt-3 flex items-center gap-3 px-2">
            <StudentAvatar avatarKey={student.avatarKey} name={student.firstName} size={32} />
            <div className="min-w-0 flex-1">
              <div className="text-xs font-bold text-text-primary truncate">
                {student.firstName} {student.lastName}
              </div>
              <div className="text-[10px] text-text-body truncate">{student.courseName}</div>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
}