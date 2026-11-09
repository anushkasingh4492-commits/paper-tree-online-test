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
        <button
          onClick={() => setNotificationsOpen(!notificationsOpen)}
          className="relative p-2 rounded-lg text-text-secondary hover:text-brand-purple hover:bg-surface-subtle transition"
        >
          <Icon name="bell" size={20} />
          {unreadNotifications > 0 && (
            <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-state-error border-2 border-surface-surface" />
          )}
        </button>

        {/* Dark Mode Toggle */}
        <button
          onClick={() => onDarkModeChange(!darkMode)}
          className="p-2 rounded-lg text-text-secondary hover:text-brand-purple hover:bg-surface-subtle transition"
        >
          <Icon name={darkMode ? "sun" : "moon"} size={20} />
        </button>
      </div>
    </header>
  );
}