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
  { key: "create-test", label: "Create a Test", icon: "test-tube", href: "/tests/generate" },
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
  onCollapsedChange,
}: {
  className?: string;
  student: StudentSummary;
  onCollapsedChange?: (collapsed: boolean) => void;
}) {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);
  const setSidebarCollapsed = (nextCollapsed: boolean) => {
    setCollapsed(nextCollapsed);
    onCollapsedChange?.(nextCollapsed);
  };

  return (
    <aside
      aria-label="Student navigation"
      className={`
        fixed left-0 top-0 z-50 flex h-dvh flex-col overflow-hidden border-r border-border-default
        bg-surface-surface/95 backdrop-blur-sm transition-[width] duration-200
        ${collapsed ? "w-20" : "w-[220px]"}
        ${className}
      `}
    >
      {/* Sidebar Brand */}
      <div className={`flex h-[82px] shrink-0 items-center gap-3 border-b border-border-default bg-surface-surface ${collapsed ? "justify-center px-2" : "px-5"}`}>
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
            onClick={() => setSidebarCollapsed(false)}
            className="absolute right-1 top-1 rounded-lg bg-surface-subtle p-1.5 text-text-secondary transition hover:bg-border-default hover:text-text-primary"
            aria-label="Expand sidebar"
          >
            <Icon name="chevron-right" size={16} />
          </button>
        )}
      </div>

      {/* Scrollable Nav Area */}
      <div className="min-h-0 flex-1 overflow-y-auto overscroll-contain">
        <p className={`px-4 pb-2 pt-5 text-[9px] font-bold uppercase tracking-[.16em] text-text-supporting-label ${collapsed ? "sr-only" : ""}`}>
          Workspace
        </p>

        <nav aria-label="Workspace" className={`space-y-1 ${collapsed ? "px-2" : "px-3"}`}>
          {NAV_ITEMS.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.key}
                href={item.href}
                title={collapsed ? item.label : undefined}
                aria-current={isActive ? "page" : undefined}
                className={`flex h-10 w-full items-center rounded-xl py-2 text-xs font-medium transition-all ${collapsed ? "justify-center px-2" : "gap-3 px-3"} ${isActive
                  ? "bg-surface-subtle text-brand-purple"
                  : "text-text-secondary hover:bg-surface-app-bg hover:text-text-primary"
                }`}
              >
                <span className="w-7 h-7 rounded-lg flex items-center justify-center shrink-0">
                  <Icon name={item.icon} size={16} className={isActive ? "text-brand-purple" : "text-text-secondary"} />
                </span>
                <span className={`min-w-0 truncate ${collapsed ? "hidden" : ""}`}>{item.label}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Bottom: collapsed toggle + profile (always visible, not scrolled away) */}
      <div className={`shrink-0 border-t border-border-default bg-surface-surface pb-4 ${collapsed ? "px-2" : "px-4"}`}>
        {!collapsed && (
          <button
            onClick={() => setSidebarCollapsed(true)}
            className="w-full h-10 flex items-center justify-between gap-3 px-3 rounded-xl text-xs font-medium text-text-secondary hover:bg-surface-app-bg transition"
          >
            <span className="flex items-center gap-3 min-w-0">
              <span className="w-7 h-7 rounded-lg flex items-center justify-center shrink-0">
                <Icon name="chevron-left" size={16} className="text-text-secondary" />
              </span>
              <span className="truncate">Collapse</span>
            </span>
          </button>
        )}
        <div className={`flex items-center ${collapsed ? "justify-center pt-3" : "mt-3 gap-3 px-3"}`}>
            <StudentAvatar avatarKey={student.avatarKey} name={student.firstName} size={32} />
            {!collapsed && <div className="min-w-0 flex-1">
              <div className="text-xs font-bold text-text-primary truncate">
                {student.firstName} {student.lastName}
              </div>
              <div className="text-[10px] text-text-body truncate">{student.courseName}</div>
            </div>}
        </div>
      </div>
    </aside>
  );
}
