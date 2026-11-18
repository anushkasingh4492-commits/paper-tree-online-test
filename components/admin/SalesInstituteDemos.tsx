"use client";

import { useEffect, useState } from "react";
import { useDemoPortal } from "@/components/useDemoPortal";

type Demo = {
  id: string;
  institute_name: string;
  contact_name: string;
  status: string;
  sales_person: string;
  created_at: string;
};

export default function SalesInstituteDemos() {
  const [demos, setDemos] = useState<Demo[]>([]);
  const [error, setError] = useState("");
  const enabled = useDemoPortal();

  useEffect(() => {
    if (!enabled) return;
    void fetch("/api/sales/leads", { cache: "no-store" })
      .then(async (response) => {
        const data = await response.json();
        if (!response.ok || !data.success) throw new Error(data.error || "Could not load sales demos.");
        setDemos(data.leads);
      })
      .catch((reason: unknown) => setError(reason instanceof Error ? reason.message : "Could not load sales demos."));
  }, [enabled]);

  if (!enabled) return null;

  return (
    <section className="rounded-3xl border border-border-default bg-white p-6 shadow-sm">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-lg font-black">Sales institute demos</h2>
          <p className="text-xs text-text-tertiary">Institutes entered by sales staff appear here.</p>
        </div>
        <a href="/admin/sales" className="rounded-lg bg-brand-primary px-4 py-2 text-sm font-bold text-white">Sales performance</a>
      </div>
      {error ? <p role="alert" className="text-sm font-semibold text-state-error">{error}</p> : demos.length === 0 ? <p className="text-sm text-text-tertiary">No sales demos have been set up yet.</p> : (
        <div className="overflow-x-auto">
          <table className="w-full min-w-[600px] text-left text-sm">
            <thead className="text-xs text-text-tertiary"><tr>{["Institute", "Contact", "Salesperson", "Status", "Created"].map((heading) => <th key={heading} className="border-b px-3 py-2">{heading}</th>)}</tr></thead>
            <tbody>{demos.map((demo) => <tr key={demo.id} className="border-b last:border-0"><td className="px-3 py-3 font-bold">{demo.institute_name}</td><td className="px-3 py-3">{demo.contact_name}</td><td className="px-3 py-3">{demo.sales_person}</td><td className="px-3 py-3">{demo.status.replaceAll("_", " ")}</td><td className="px-3 py-3">{new Date(demo.created_at).toLocaleDateString("en-IN")}</td></tr>)}</tbody>
          </table>
        </div>
      )}
    </section>
  );
}
