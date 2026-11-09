"use client";

import type { WeakArea } from "@/types/dashboard";
import { Card } from "@/components/ui/Card";

export function WeakAreasList({ areas }: { areas: WeakArea[] }) {
  return (
    <Card variant="default" padding="md" radius="large" className="border border-border-default">
      <div className="flex flex-col">
        <div className="flex justify-between items-baseline mb-4">
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-bold uppercase tracking-wider text-text-supporting-label">Weak Areas</span>
          </div>
          <a href="#" className="text-[10px] font-bold text-brand-purple hover:underline flex items-center gap-1">
            View All →
          </a>
        </div>

        <div className="space-y-2">
          {areas.length ? areas.map((area) => (
            <div
              key={area.topic}
              className="flex items-center justify-between p-3 rounded-xl border border-surface-subtle bg-white/30"
            >
              <div className="flex items-center gap-2">
                <span
                  className={`w-2 h-2 rounded-full ${
                    area.flagged ? "bg-state-error" : "bg-state-warning"
                  }`}
                />
                <span className="text-sm font-medium text-text-primary">{area.topic}</span>
              </div>
              <span className="text-[10px] font-bold text-state-error">{area.accuracy?.toFixed(0) ?? "—"}% accuracy</span>
            </div>
          )) : <p className="py-4 text-xs text-text-body">Complete more tests to identify focus topics.</p>}
        </div>

        <p className="mt-4 text-[10px] text-text-body italic">
          Topics that need more attention.
        </p>
      </div>
    </Card>
  );
}