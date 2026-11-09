"use client";

import type { TrendPoint } from "@/types/dashboard";
import { Card } from "@/components/ui/Card";

export function PerformanceTrendChart({ data, accuracy }: { data: TrendPoint[]; accuracy: number }) {
  const maxScore = data.length ? Math.max(...data.map((d) => d.score)) : 0;
  const width = 400;
  const height = 200;
  const padding = 40;
  const improvement = data.length > 1 ? data[data.length - 1].score - data[0].score : 0;

  const points = data.map((d, i) => {
    const x = data.length === 1
      ? width / 2
      : padding + (i / (data.length - 1)) * (width - 2 * padding);
    const y = height - padding - (Math.max(0, Math.min(100, d.score)) / 100) * (height - 2 * padding);
    return { x, y, score: d.score, date: d.date };
  });

  const path = points
    .map((p, i) => (i === 0 ? `M${p.x},${p.y}` : `L${p.x},${p.y}`))
    .join(" ");

  return (
    <Card variant="default" padding="none" radius="large" className="border border-border-default p-3 sm:p-4">
      <div className="flex flex-col">
        {/* Chart Labels */}
        <div className="flex justify-between mb-4">
          <div className="text-[10px] font-bold text-text-body">100%</div>
          <div className="text-[10px] font-bold text-text-body">50%</div>
          <div className="text-[10px] font-bold text-text-body">0%</div>
        </div>

        <div className="relative h-[160px] w-full">
          {/* Grid lines */}
          <div className="absolute inset-0 flex flex-col justify-between pointer-events-none">
            {[0, 50, 100].map((pct, i) => (
              <div
                key={pct}
                className={`flex items-center justify-between border-b border-surface-subtle ${
                  i < 2 ? "pb-[33%]" : ""
                }`}
              >
                <span className="text-[10px] text-text-body">{pct}%</span>
              </div>
            ))}
          </div>

          {points.length ? (
          <svg className="absolute inset-0 w-full h-full" viewBox={`0 0 ${width} ${height}`}>
            <defs>
              <linearGradient id="lineGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#3478E8" stopOpacity="0.6" />
                <stop offset="100%" stopColor="#3478E8" stopOpacity="0" />
              </linearGradient>
            </defs>

            {/* Area fill */}
            {points.length > 1 && <path
              d={`M${points[0].x},${height - padding} ${path} L${points[points.length - 1].x},${height - padding} Z`}
              fill="url(#lineGradient)"
            />}

            {/* Line */}
            {points.length > 1 && <path d={path} fill="none" stroke="#3478E8" strokeWidth="2" className="drop-shadow-[0_2px_4px_rgba(52,120,232,0.3)]" />}

            {/* Points */}
            {points.map((p) => (
              <circle
                key={p.date}
                cx={p.x}
                cy={p.y}
                r={4}
                fill="#3478E8"
                className="drop-shadow-[0_2px_4px_rgba(52,120,232,0.4)]"
              />
            ))}
          </svg>
          ) : (
            <div className="absolute inset-0 flex items-center justify-center text-xs text-text-body">
              Complete a test to see your performance trend.
            </div>
          )}

          {/* X-axis labels */}
          <div className="absolute bottom-0 left-0 right-0 flex justify-between text-[10px] font-bold text-text-body px-2">
            {data.map((d) => (
              <span key={d.date} className="text-center w-full">
                {d.date}
              </span>
            ))}
          </div>
        </div>

        {/* Chart Summary Stats */}
        <div className="mt-3 grid grid-cols-3 gap-2 border-t border-border-default pt-3">
          <div className="text-center">
            <div className="text-[10px] text-text-body">Best Score</div>
            <div className="text-base font-black text-text-primary">{data.length ? `${maxScore.toFixed(1)}%` : "—"}</div>
          </div>
          <div className="text-center">
            <div className="text-[10px] text-text-body">Improvement</div>
            <div className={`text-base font-black ${improvement >= 0 ? "text-state-success" : "text-state-error"}`}>
              {data.length > 1 ? `${improvement > 0 ? "+" : ""}${improvement.toFixed(1)}%` : "—"}
            </div>
          </div>
          <div className="text-center">
            <div className="text-[10px] text-text-body">Accuracy</div>
            <div className="text-base font-black text-text-primary">{data.length ? `${accuracy.toFixed(1)}%` : "—"}</div>
          </div>
        </div>
      </div>
    </Card>
  );
}