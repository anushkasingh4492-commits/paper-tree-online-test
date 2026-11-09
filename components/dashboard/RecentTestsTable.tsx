"use client";

import type { RecentTest } from "@/types/dashboard";
import { Card } from "@/components/ui/Card";

export function RecentTestsTable({ tests }: { tests: RecentTest[] }) {
  return (
    <Card variant="default" padding="md" radius="large" className="border border-border-default">
      <div className="flex flex-col">
        <div className="flex justify-between items-baseline mb-4">
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-bold uppercase tracking-wider text-text-supporting-label">Recent Tests</span>
          </div>
          <a href="#" className="text-[10px] font-bold text-brand-purple hover:underline flex items-center gap-1">
            View All →
          </a>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-surface-subtle">
                <th className="py-3 text-[10px] font-bold uppercase tracking-wider text-text-supporting-label">TEST NAME</th>
                <th className="py-3 text-[10px] font-bold uppercase tracking-wider text-text-supporting-label">SCORE</th>
                <th className="py-3 text-[10px] font-bold uppercase tracking-wider text-text-supporting-label">ACCURACY</th>
                <th className="py-3 text-[10px] font-bold uppercase tracking-wider text-text-supporting-label">DATE</th>
              </tr>
            </thead>
            <tbody>
              {tests.length ? tests.map((test) => (
                <tr key={test.id} className="border-b border-surface-subtle hover:bg-surface-subtle/50 transition">
                  <td className="py-3 text-xs font-medium text-text-primary">{test.name}</td>
                  <td className="py-3 text-xs font-bold text-text-primary">{test.score.toFixed(1)}%</td>
                  <td className="py-3 text-xs font-bold text-state-error">{test.accuracy.toFixed(1)}%</td>
                  <td className="py-3 text-xs text-text-body">{test.date}</td>
                </tr>
              )) : (
                <tr>
                  <td colSpan={4} className="py-6 text-center text-xs text-text-body">Completed tests will appear here.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </Card>
  );
}