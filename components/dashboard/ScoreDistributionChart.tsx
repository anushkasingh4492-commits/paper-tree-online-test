"use client";

import type { ScoreDistribution } from "@/types/dashboard";
import { Card } from "@/components/ui/Card";

const COLOR_MAP: Record<string, string> = {
  red: "text-red-500",
  orange: "text-orange-500",
  yellow: "text-yellow-500",
  green: "text-green-500",
};

export function ScoreDistributionChart({ data }: { data: ScoreDistribution[] }) {
  const totalCount = data.reduce((sum, d) => sum + d.count, 0);

  return (
    <Card variant="default" padding="md" radius="large" className="border border-border-default">
      <div className="flex flex-col">
        <div className="flex justify-between items-baseline mb-6">
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-text-supporting-label">Score Distribution</h3>
            <p className="text-[10px] text-text-body">All tests ({totalCount} attempts)</p>
          </div>
          <div className="w-20 h-20 rounded-full border-8 border-surface-subtle flex items-center justify-center relative">
            <svg className="w-full h-full transform -rotate-90">
              <circle cx="40" cy="40" r="30" stroke="currentColor" strokeWidth="8" fill="none" className="text-border-muted" />
              {data.map((d, index) => {
                const sweepAngle = (d.percentage / 100) * 360;
                const offset = (data.slice(0, index).reduce((sum, item) => sum + item.percentage, 0) / 100) * 188.5;
                return (
                  <circle
                    key={d.range}
                    cx="40"
                    cy="40"
                    r="30"
                    stroke="currentColor"
                    strokeWidth="8"
                    fill="none"
                    className={COLOR_MAP[d.color]}
                    strokeDasharray={`${(sweepAngle / 360) * 188.5} 188.5`}
                    strokeDashoffset={-offset}
                  />
                );
              })}
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-2xl font-black text-text-primary">{totalCount}</span>
              <span className="text-[10px] text-text-body">Tests</span>
            </div>
          </div>
        </div>

        <div className="space-y-3">
          {data.length ? data.map((d) => (
            <div key={d.range} className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${COLOR_MAP[d.color] ?? "text-gray-400"}`}>
                  <svg className="w-full h-full" fill="currentColor" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="2" />
                  </svg>
                </div>
                <span className="text-[10px] font-medium text-text-body">{d.range}</span>
              </div>
              <span className="text-xs font-bold text-text-primary">{d.count} ({d.percentage}%)</span>
            </div>
          )) : <p className="text-xs text-text-body">Complete a test to see your score distribution.</p>}
        </div>
      </div>
    </Card>
  );
}