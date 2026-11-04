"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function NotificationsPage() {
  const router = useRouter();
  const [notifications, setNotifications] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch("/api/notifications", { cache: "no-store" });
        const data = await res.json();
        if (data.success) setNotifications(data.notifications || []);
      } catch {
        // silent
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <main className="min-h-screen bg-surface-app-bg text-text-primary">
      <div className="mx-auto max-w-3xl px-6 py-10">
        <div className="flex items-center justify-between mb-8">
          <div>
            <button
              onClick={() => router.push("/dashboard")}
              className="text-sm font-semibold text-brand-primary mb-2 inline-block transition hover:underline"
            >
              ← Back to Dashboard
            </button>
            <h1 className="text-2xl font-extrabold tracking-tight">
              Notifications
            </h1>
            <p className="text-sm text-text-tertiary">
              Stay updated with your test schedules and announcements.
            </p>
          </div>
        </div>

        {loading ? (
          <div className="h-64 flex items-center justify-center">
            <div className="w-8 h-8 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin" />
          </div>
        ) : notifications.length === 0 ? (
          <div className="rounded-2xl border border-border-default bg-white p-16 text-center shadow-sm">
            <div className="text-4xl mb-4">𔔩</div>
            <h2 className="text-xl font-bold text-text-primary">No notifications</h2>
            <p className="mt-2 text-text-tertiary">
              You're all caught up. New test schedules and announcements will appear here.
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {notifications.map((n) => (
              <div
                key={n.id}
                className={`rounded-xl border p-4 flex items-start gap-3 ${!n.isRead ? "border-brand-primary bg-surface-subtle" : "border-border-default bg-white"}`}
              >
                <div className="w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5">
                  {!n.isRead ? (
                    <span className="text-[10px]">𔔩</span>
                  ) : (
                    <span className="text-[10px] text-text-body">✓</span>
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-text-primary leading-tight">
                    {n.title}
                  </p>
                  <p className="mt-1 text-sm text-text-tertiary leading-relaxed">
                    {n.message}
                  </p>
                  <p className="mt-2 text-[10px] text-text-body">
                    {n.createdAt}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
