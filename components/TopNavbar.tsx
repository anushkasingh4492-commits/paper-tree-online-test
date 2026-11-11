"use client";

import { useState } from "react";
import { Icon } from "./Icon";
import StudentAvatar from "./StudentAvatar";

type StudentSummary = {
  firstName: string;
  lastName: string;
  courseName: string;
  avatarKey?: string | null;
};

export function TopNavbar({
  className = "",
  student,
  darkMode,
  onDarkModeChange,
  unreadNotifications,
}: {
  className?: string;
  student: StudentSummary;
  darkMode: boolean;
  onDarkModeChange: (enabled: boolean) => void;
  unreadNotifications: number;
}) {
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const [courseOpen, setCourseOpen] = useState(false);
  return (
    <header
      className={`
      sticky top-0 z-40 flex items-center justify-between gap-2 px-3 py-3 sm:gap-4 sm:px-5 sm:py-4
      border-b border-border-default bg-surface-surface/95 shadow-sm backdrop-blur-md
        ${className}
      `}
    >
      {/* Left: Logo + Welcome */}
      <div className="flex min-w-0 items-center gap-2 sm:gap-4">
      <div className="flex shrink-0 items-center gap-2">
        <div className="flex h-8 w-8 items-center justify-center rounded-[10px] bg-brand-primary text-sm font-black text-white shadow-sm">
            IC
          </div>
        <div className="hidden text-[12px] font-extrabold text-text-primary md:block">Infinity Classes</div>
        </div>

      <div className="flex min-w-0 flex-col">
        <h1 className="truncate text-[12px] font-black leading-tight text-text-primary sm:text-[17px]">
            Welcome back, {student.firstName}
          </h1>
        <p className="hidden text-[11px] text-text-body sm:block">Here&apos;s your performance overview and next steps.</p>
        </div>
      </div>

      {/* Center: Course Selector */}
      <div className="hidden items-center gap-2 md:flex">
        <button
          onClick={() => setCourseOpen(!courseOpen)}
          className="flex items-center gap-2 rounded-xl border border-border-default bg-surface-subtle px-3 py-2 text-[12px] font-bold text-text-primary hover:bg-surface-elevated transition"
        >
          <span className="font-black">{student.courseName}</span>
          <Icon name="chevron-down" size={14} className="text-text-body" />
        </button>
      </div>

      {/* Right: Profile, Notifications, Dark Mode */}
      <div className="flex shrink-0 items-center gap-1 sm:gap-3">
        {/* Profile Dropdown */}
        <button
          onClick={() => setProfileOpen(!profileOpen)}
          className="flex items-center gap-2 rounded-full border border-border-default bg-surface-subtle px-2 py-1 sm:px-3 sm:py-1.5 text-[11px] font-medium text-text-secondary hover:bg-surface-elevated transition"
        >
          <StudentAvatar avatarKey={student.avatarKey} name={student.firstName} size={28} />
          <span className="hidden sm:inline">{student.firstName}{student.lastName ? ` ${student.lastName[0]}.` : ""}</span>
          <Icon name="chevron-down" size={14} className="text-text-body" />
        </button>

        {/* Notifications */}
        <div className="relative">
          <button
            onClick={() => setNotificationsOpen(!notificationsOpen)}
            className="relative p-2 rounded-lg text-text-secondary hover:text-brand-purple hover:bg-surface-subtle transition"
          >
            <Icon name="bell" size={20} />
            {unreadNotifications > 0 && (
              <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-state-error border-2 border-surface-surface" />
            )}
          </button>

          {notificationsOpen && (
            <div className="absolute right-0 mt-2 w-64 rounded-xl border border-border-default bg-surface-surface shadow-lg z-50">
              <div className="p-3 border-b border-border-default">
                <h3 className="text-[11px] font-black text-text-primary">Notifications</h3>
              </div>
              <div className="p-2 space-y-1">
                {unreadNotifications > 0 ? (
                  <div className="flex items-start gap-2 p-2 rounded-lg bg-amber-50 border border-amber-100">
                    <div className="w-6 h-6 rounded-full flex items-center justify-center bg-amber-100 text-amber-700 text-[9px] font-bold">
                      !
                    </div>
                    <div className="min-w-0">
                      <div className="text-[10px] font-bold text-text-primary">You have {unreadNotifications} unread notification</div>
                      <div className="text-[9px] text-text-body mt-0.5">Check your dashboard for updates.</div>
                    </div>
                  </div>
                ) : (
                  <div className="flex items-center justify-center py-4">
                    <span className="text-[10px] text-text-body">No new notifications</span>
                  </div>
                )}
              </div>
              <div className="border-t border-border-default p-2">
                <button
                  onClick={() => setNotificationsOpen(false)}
                  className="w-full flex items-center justify-center gap-1 px-2 py-1.5 rounded-lg text-[10px] font-bold text-brand-purple hover:bg-surface-subtle transition"
                >
                  Mark all as read
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Dark Mode Toggle */}
        <button
          type="button"
          onClick={() => onDarkModeChange(!darkMode)}
          aria-label={darkMode ? "Switch to light mode" : "Switch to dark mode"}
          title={darkMode ? "Switch to light mode" : "Switch to dark mode"}
          className="rounded-lg p-2 text-text-secondary transition hover:bg-surface-subtle hover:text-brand-purple focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-primary"
        >
          <Icon name={darkMode ? "sun" : "moon"} size={20} />
        </button>
      </div>
    </header>
  );
}