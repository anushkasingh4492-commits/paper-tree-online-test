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

export function isInfinityPortalHostname(hostname: string) {
  const normalizedHost = hostname.toLowerCase();
  return (
    normalizedHost === "web.infinityclasses.net" ||
    normalizedHost === "web.infinity.classes.net"
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

export function useInfinityPortal() {
  return useSyncExternalStore(
    subscribe,
    () => typeof window !== "undefined" && isInfinityPortalHostname(window.location.hostname),
    () => false,
  );
}
