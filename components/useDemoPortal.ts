"use client";

import { useSyncExternalStore } from "react";

export function isDemoPortalHostname(hostname: string) {
  const normalizedHost = hostname.toLowerCase();
  const configuredHost = process.env.NEXT_PUBLIC_DEMO_CBT_HOST?.toLowerCase();
  return (
    normalizedHost === "demo.cbt.papertreestudio.in" ||
    normalizedHost === configuredHost ||
    normalizedHost === "localhost" ||
    normalizedHost === "127.0.0.1"
  );
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
