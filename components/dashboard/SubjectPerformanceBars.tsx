"use client";

import type { SubjectScore } from "@/types/dashboard";
import { Card } from "@/components/ui/Card";

export function SubjectPerformanceBars({ data }: { data: SubjectScore[] }) {
  return (
    <Card variant="default" padding="md" radius="large" className="border border-border-default">
      <div className="flex flex-col">
        <div className="flex justify-between items-baseline mb-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-text-supporting-label">Subject Performance</h3>
        </div>

        <div className="space-y-3">
          {data.map((subject) => (
            <div key={subject.subject} className="flex flex-col gap-2">
              <div className="flex justify-between items-baseline">
                <span className="text-xs font-medium text-text-primary">{subject.subject}</span>
                <span className="text-xs font-bold text-text-primary">{subject.score}%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-surface-subtle overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-1000 ${
                    subject.score >= 80 ? "bg-brand-primary" : subject.score >= 70 ? "bg-blue-400" : "bg-green-400"
                  }`}
                  style={{ width: `${subject.score}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}