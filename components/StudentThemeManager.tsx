"use client";

import { useEffect } from "react";
import { usePathname } from "next/navigation";

const THEME_KEY = "paperTreeStudentDarkMode";
const THEME_EVENT = "paperTreeStudentThemeChange";

function isStudentRoute(pathname: string): boolean {
  return (
    pathname === "/dashboard" ||
    pathname === "/profile" ||
    pathname === "/edit-profile" ||
    pathname === "/achievements" ||
    pathname === "/tests" ||
    pathname.startsWith("/tests/") ||
    pathname.startsWith("/test/") ||
    pathname === "/test-summary" ||
    pathname === "/history" ||
    pathname === "/stats" ||
    pathname.startsWith("/student/") ||
    pathname.startsWith("/scheduled-test/")
  );
}

/** Keeps the student's saved theme active while navigating between student routes. */
export default function StudentThemeManager() {
  const pathname = usePathname();

  useEffect(() => {
    const applyTheme = () => {
      let enabled = false;
      try {
        enabled = window.localStorage.getItem(THEME_KEY) === "true";
      } catch {
        enabled = false;
      }
      const shouldUseDark = isStudentRoute(pathname || "") && enabled;
      document.body.classList.toggle("student-theme-dark", shouldUseDark);
      document.documentElement.style.colorScheme = shouldUseDark ? "dark" : "light";
    };

    applyTheme();
    window.addEventListener(THEME_EVENT, applyTheme);
    window.addEventListener("storage", applyTheme);
    return () => {
      window.removeEventListener(THEME_EVENT, applyTheme);
      window.removeEventListener("storage", applyTheme);
    };
  }, [pathname]);

  return null;
}
