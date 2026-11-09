"use client";

import type { RecentTest } from "@/types/dashboard";
import { Card } from "@/components/ui/Card";

export function RecentTestsTable({ tests }: { tests: RecentTest[] }) {
  return (
    <Card variant="default" padding="none" radius="large" className="border border-border-default p-3 sm:p-4">
      <div className="flex flex-col">
        <div className="mb-2 flex items-baseline justify-between">
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-bold uppercase tracking-wider text-text-supporting-label">Recent Tests</span>
          </div>
          <a href="/tests" className="text-[10px] font-bold text-brand-purple hover:underline flex items-center gap-1">
            View All →
          </a>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-surface-subtle">
                <th className="py-2 text-[8px] font-bold uppercase tracking-wider text-text-supporting-label">Test name</th>
                <th className="py-2 text-[8px] font-bold uppercase tracking-wider text-text-supporting-label">Score</th>
                <th className="py-2 text-[8px] font-bold uppercase tracking-wider text-text-supporting-label">Accuracy</th>
                <th className="py-2 text-[8px] font-bold uppercase tracking-wider text-text-supporting-label">Date</th>
              </tr>
            </thead>
            <tbody>
              {tests.length ? tests.map((test) => (
                <tr key={test.id} className="border-b border-surface-subtle hover:bg-surface-subtle/50 transition">
                  <td className="max-w-[200px] truncate py-2 text-[9px] font-medium text-text-primary">{test.name}</td>
                  <td className="py-2 text-[9px] font-bold text-text-primary">{test.score.toFixed(1)}%</td>
                  <td className="py-2 text-[9px] font-bold text-state-error">{test.accuracy.toFixed(1)}%</td>
                  <td className="py-2 text-[9px] text-text-body">{test.date}</td>
                </tr>
              )) : (
                <tr>
                  <td colSpan={4} className="py-5 text-center text-[10px] text-text-body">Completed tests will appear here.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </Card>
  );
}