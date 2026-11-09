"use client";

import { PerformanceTrendChart } from "./PerformanceTrendChart";
import { ScoreDistributionChart } from "./ScoreDistributionChart";
import { SubjectPerformanceBars } from "./SubjectPerformanceBars";
import { RecentTestsTable } from "./RecentTestsTable";
import { WeakAreasList } from "./WeakAreasList";
import type {
  RecentTest,
  ScoreDistribution,
  SubjectScore,
  TrendPoint,
  WeakArea,
} from "@/types/dashboard";

export function PerformanceTrendsSection({
  trend,
  distribution,
  subjects,
  recentTests,
  weakAreas,
  accuracy,
}: {
  trend: TrendPoint[];
  distribution: ScoreDistribution[];
  subjects: SubjectScore[];
  recentTests: RecentTest[];
  weakAreas: WeakArea[];
  accuracy: number;
}) {
  return (
    <section className="w-full space-y-5">
      <div className="flex justify-between items-start">
        <div>
          <h2 className="text-[18px] font-black text-text-primary">Performance Trends</h2>
          <p className="text-[11px] text-text-body">Track your progress over time.</p>
        </div>
        <div className="flex items-center gap-2 rounded-xl border border-border-default bg-surface-surface px-3 py-1.5">
          <span className="text-[10px] font-medium text-text-body">All completed tests</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <div className="lg:col-span-2">
          <PerformanceTrendChart data={trend} accuracy={accuracy} />
        </div>
        <div className="lg:col-span-1">
          <ScoreDistributionChart data={distribution} />
        </div>
      </div>

      <SubjectPerformanceBars data={subjects} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <RecentTestsTable tests={recentTests} />
        <WeakAreasList areas={weakAreas} />
      </div>
    </section>
  );
}
