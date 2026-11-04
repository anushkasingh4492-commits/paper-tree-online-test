"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type Student = {
  student_id: string;
  student_name: string;
  email: string;
  class_name?: string | null;
  tests_taken: number;
  average_score: number;
  average_accuracy: number;
  correct: number;
  wrong: number;
  unanswered: number;
};

export default function TeacherStudentsPage() {
  const router = useRouter();

  const [students, setStudents] =
    useState<Student[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  useEffect(() => {
    async function load() {
      try {
        const response = await fetch(
          "/api/teacher/student-performance",
          {
            credentials: "include",
            cache: "no-store",
          }
        );

        const result =
          await response.json();

        if (
          !response.ok ||
          !result.success
        ) {
          throw new Error(
            result.error ||
              "Failed to load student performance."
          );
        }

        setStudents(
          result.students || []
        );
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load student performance."
        );
      } finally {
        setLoading(false);
      }
    }

    void load();
  }, []);

  return (
    <main className="min-h-screen bg-surface-app-bg text-text-primary">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.15em] text-brand-primary">
              Teacher Portal
            </p>

            <h1 className="mt-2 text-3xl font-extrabold">
              Student Performance
            </h1>

            <p className="mt-2 text-sm text-text-tertiary">
              Performance from tests created by you.
            </p>
          </div>

          <button
            onClick={() =>
              router.push("/teacher")
            }
            className="rounded-xl border border-border-default bg-white px-4 py-2.5 text-sm font-bold text-text-tertiary hover:bg-surface-app-bg"
          >
            ← Teacher Portal
          </button>
        </div>

        {error && (
          <div className="rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm font-medium text-state-error">
            {error}
          </div>
        )}

        <section className="overflow-hidden rounded-2xl border border-border-default bg-white shadow-sm">
          {loading ? (
            <div className="p-8 text-sm text-text-tertiary">
              Loading student performance...
            </div>
          ) : students.length === 0 ? (
            <div className="p-10 text-center">
              <p className="font-bold">
                No completed student performance is available yet.
              </p>

              <p className="mt-2 text-sm text-text-body">
                Once students complete tests created by you,
                their performance will appear here.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full min-w-[900px] text-left">
                <thead className="border-b border-border-default bg-surface-app-bg">
                  <tr>
                    <th className="px-5 py-4 text-xs font-bold text-text-tertiary">
                      Student
                    </th>

                    <th className="px-5 py-4 text-xs font-bold text-text-tertiary">
                      Tests
                    </th>

                    <th className="px-5 py-4 text-xs font-bold text-text-tertiary">
                      Avg. Score
                    </th>

                    <th className="px-5 py-4 text-xs font-bold text-text-tertiary">
                      Avg. Accuracy
                    </th>

                    <th className="px-5 py-4 text-xs font-bold text-text-tertiary">
                      Correct
                    </th>

                    <th className="px-5 py-4 text-xs font-bold text-text-tertiary">
                      Wrong
                    </th>

                    <th className="px-5 py-4 text-xs font-bold text-text-tertiary">
                      Unanswered
                    </th>
                  </tr>
                </thead>

                <tbody className="divide-y divide-[#eef0f4]">
                  {students.map((student) => (
                    <tr
                      key={student.student_id}
                      className="hover:bg-surface-app-bg"
                    >
                      <td className="px-5 py-4">
                        <p className="font-bold text-text-primary">
                          {student.student_name}
                        </p>

                        <p className="mt-1 text-xs text-text-body">
                          {student.email}
                          {student.class_name
                            ? ` · ${student.class_name}`
                            : ""}
                        </p>
                      </td>

                      <td className="px-5 py-4 text-sm font-semibold">
                        {student.tests_taken}
                      </td>

                      <td className="px-5 py-4 text-sm font-bold text-brand-primary">
                        {Number(
                          student.average_score || 0
                        ).toFixed(1)}
                      </td>

                      <td className="px-5 py-4 text-sm font-bold">
                        {Number(
                          student.average_accuracy || 0
                        ).toFixed(1)}
                        %
                      </td>

                      <td className="px-5 py-4 text-sm font-semibold text-emerald-600">
                        {student.correct}
                      </td>

                      <td className="px-5 py-4 text-sm font-semibold text-rose-500">
                        {student.wrong}
                      </td>

                      <td className="px-5 py-4 text-sm font-semibold text-text-tertiary">
                        {student.unanswered}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}