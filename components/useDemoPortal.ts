"use client";

import { useSyncExternalStore } from "react";

export function isDemoPortalHostname(hostname: string) {
  const configuredHost = (process.env.NEXT_PUBLIC_DEMO_CBT_HOST || "demo.cbt").toLowerCase();
  const normalizedHost = hostname.toLowerCase();
  return normalizedHost === configuredHost || normalizedHost === "localhost" || normalizedHost === "127.0.0.1";
}

function subscribe() {
  return () => {};
}

function getSnapshot() {
  return typeof window !== "undefined" && isDemoPortalHostname(window.location.hostname);
}

export function useDemoPortal() {
  return useSyncExternalStore(subscribe, getSnapshot, () => false);
}
