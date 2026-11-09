"use client";

import { useEffect, useSyncExternalStore } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Award,
  Bell,
  BookOpenCheck,
  ChartNoAxesCombined,
  ClipboardList,
  Flame,
  LayoutDashboard,
  Moon,
  Sun,
  Target,
  UserRound,
  Trophy,
} from "lucide-react";
import AcademyBranding from "@/components/AcademyBranding";
import StudentAccountMenu from "@/components/StudentAccountMenu";
import StudentAvatar from "@/components/StudentAvatar";
import { fetchStudentData } from "./student-api";
import type { DashboardPayload } from "./student-types";

type Props = {
  children: React.ReactNode;
  active: "dashboard" | "tests" | "leaderboard";
  studentName?: string;
  courseName?: string;
  unreadCount?: number;
  forceDark?: boolean;
};

function subscribeToStudentTheme(callback: () => void) {
  window.addEventListener("paperTreeStudentThemeChange", callback);
  window.addEventListener("storage", callback);
  return () => {
    window.removeEventListener("paperTreeStudentThemeChange", callback);
    window.removeEventListener("storage", callback);
  };
}

function getStudentTheme() {
  try {
    return window.localStorage.getItem("paperTreeStudentDarkMode") === "true";
  } catch (error) {
    console.error("Could not read the saved student theme preference.", error);
    return false;
  }
}

function toggleStudentTheme() {
  try {
    const enabled = window.localStorage.getItem("paperTreeStudentDarkMode") === "true";
    window.localStorage.setItem("paperTreeStudentDarkMode", String(!enabled));
    window.dispatchEvent(new Event("paperTreeStudentThemeChange"));
  } catch (error) {
    console.error("Could not save the student theme preference.", error);
  }
}

const navigation: Array<{
  label: string;
  href: string;
  icon: typeof LayoutDashboard;
  active?: Props["active"];
}> = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard, active: "dashboard" },
  { label: "My Tests", href: "/tests", icon: ClipboardList, active: "tests" },
  { label: "Test Summary", href: "/test-summary", icon: ChartNoAxesCombined },
  { label: "Batch Leaderboard", href: "/student/batch-leaderboard", icon: Trophy, active: "leaderboard" },
  { label: "Mistake Notebook", href: "/student/mistakes", icon: BookOpenCheck },
  { label: "Edit Profile", href: "/edit-profile", icon: UserRound },
  { label: "My Achievements", href: "/achievements", icon: Award },
  { label: "Boss Fight Queue", href: "/boss-fight", icon: Flame },
  { label: "Weak Areas Test", href: "/tests/generate", icon: Target },
];

export default function StudentWorkspace({
  children,
  active,
  studentName: initialStudentName,
  courseName: initialCourseName,
  unreadCount: initialUnreadCount,
  forceDark = false,
}: Props) {
  const pathname = usePathname();
  const [studentName, setStudentName] = useState(initialStudentName ?? "");
  const [courseName, setCourseName] = useState(initialCourseName ?? "");
  const [unreadCount, setUnreadCount] = useState(initialUnreadCount ?? 0);
  const savedDarkMode = useSyncExternalStore(subscribeToStudentTheme, getStudentTheme, () => false);
  const [headerError, setHeaderError] = useState("");

  useEffect(() => {
    if (initialStudentName && initialCourseName !== undefined && initialUnreadCount !== undefined) return;
    let activeRequest = true;
    fetchStudentData<DashboardPayload>("/api/dashboard")
      .then((data) => {
        if (!activeRequest) return;
        if (!initialStudentName) setStudentName(data.student?.name ?? "");
        if (initialCourseName === undefined) setCourseName(data.assignment?.courseName ?? "");
        if (initialUnreadCount === undefined) {
          setUnreadCount(data.notifications?.filter((item) => !item.isRead).length ?? 0);
        }
      })
      .catch((error: unknown) => {
        if (activeRequest) {
          setHeaderError(error instanceof Error ? error.message : "Could not load your account details.");
        }
      });
    return () => {
      activeRequest = false;
    };
  }, [initialCourseName, initialStudentName, initialUnreadCount]);

  const firstName = studentName.trim().split(/\s+/)[0] || "";
  const isDark = forceDark || savedDarkMode;
  const shellTone = isDark ? "student-workspace student-workspace--dark" : "student-workspace";

  return (
    <div className={shellTone} data-current-path={pathname}>
      <aside className={`student-workspace__sidebar ${isDark ? "student-workspace__sidebar--dark" : ""}`}>
        <Link href="/dashboard" className="student-workspace__brand" aria-label="Go to dashboard">
          <AcademyBranding variant="compact" />
        </Link>
        <div className="student-workspace__nav-label">Workspace</div>
        <nav className="student-workspace__nav" aria-label="Workspace navigation">
          {navigation.map((item) => {
            const Icon = item.icon;
            const selected =
              (item.active && item.active === active) ||
              (!item.active && item.href === pathname);
            return (
              <Link
                href={item.href}
                key={item.href}
                aria-current={selected ? "page" : undefined}
                className={`student-workspace__nav-link ${selected ? "is-active" : ""}`}
              >
                <Icon size={17} strokeWidth={1.8} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>
        <div className="student-workspace__sidebar-footer">
          {studentName && <Link href="/profile" className="student-workspace__profile"><StudentAvatar name={studentName} size={36} /><span>{studentName}</span></Link>}
        </div>
      </aside>

      <div className="student-workspace__main">
        <header className="student-workspace__topbar">
          <div className="student-workspace__welcome">
            <p>Student workspace</p>
            <h1>Welcome back{firstName ? `, ${firstName}` : ""}</h1>
          </div>
          <div className="student-workspace__topbar-actions">
            <label className="student-workspace__course">
              <span>Course</span>
              <select aria-label="Assigned course" value={courseName} disabled>
                <option value={courseName}>{courseName || "No course assigned"}</option>
              </select>
            </label>
            <Link href="/notifications" className="student-workspace__icon-button" aria-label="Notifications">
              <Bell size={18} />
              {unreadCount > 0 && <span className="student-workspace__notification-count">{unreadCount}</span>}
            </Link>
            <button
              type="button"
              onClick={toggleStudentTheme}
              className="student-workspace__icon-button"
              aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
              aria-pressed={isDark}
            >
              {isDark ? <Sun size={18} /> : <Moon size={18} />}
            </button>
            {studentName && <StudentAccountMenu studentName={studentName} />}
          </div>
        </header>
        {headerError && <p className="student-workspace__error" role="alert">{headerError}</p>}
        <main className="student-workspace__content">{children}</main>
      </div>

      <nav className={`student-workspace__mobile-nav ${isDark ? "student-workspace__mobile-nav--dark" : ""}`} aria-label="Quick navigation">
        {navigation.slice(0, 5).map((item) => {
          const Icon = item.icon;
          const selected = item.active === active;
          return (
            <Link href={item.href} key={item.href} className={selected ? "is-active" : ""}>
              <Icon size={17} />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
