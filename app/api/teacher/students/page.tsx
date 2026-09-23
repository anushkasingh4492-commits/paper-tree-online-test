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
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.15em] text-[#315bea]">
              Teacher Portal
            </p>

            <h1 className="mt-2 text-3xl font-extrabold">
              Student Performance
            </h1>

            <p className="mt-2 text-sm text-[#697386]">
              Performance from tests created by you.
            </p>
          </div>

          <button
            onClick={() =>
              router.push("/teacher")
            }
            className="rounded-xl border border-[#e2e6ee] bg-white px-4 py-2.5 text-sm font-bold text-[#697386] hover:bg-[#f8f9fb]"
          >
            ← Teacher Portal
          </button>
        </div>

        {error && (
          <div className="rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
            {error}
          </div>
        )}

        <section className="overflow-hidden rounded-2xl border border-[#e5e8ef] bg-white shadow-sm">
          {loading ? (
            <div className="p-8 text-sm text-[#697386]">
              Loading student performance...
            </div>
          ) : students.length === 0 ? (
            <div className="p-10 text-center">
              <p className="font-bold">
                No completed student performance is available yet.
              </p>

              <p className="mt-2 text-sm text-[#8a93a5]">
                Once students complete tests created by you,
                their performance will appear here.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full min-w-[900px] text-left">
                <thead className="border-b border-[#eef0f4] bg-[#fafbfc]">
                  <tr>
                    <th className="px-5 py-4 text-xs font-bold text-[#697386]">
                      Student
                    </th>

                    <th className="px-5 py-4 text-xs font-bold text-[#697386]">
                      Tests
                    </th>

                    <th className="px-5 py-4 text-xs font-bold text-[#697386]">
                      Avg. Score
                    </th>

                    <th className="px-5 py-4 text-xs font-bold text-[#697386]">
                      Avg. Accuracy
                    </th>

                    <th className="px-5 py-4 text-xs font-bold text-[#697386]">
                      Correct
                    </th>

                    <th className="px-5 py-4 text-xs font-bold text-[#697386]">
                      Wrong
                    </th>

                    <th className="px-5 py-4 text-xs font-bold text-[#697386]">
                      Unanswered
                    </th>
                  </tr>
                </thead>

                <tbody className="divide-y divide-[#eef0f4]">
                  {students.map((student) => (
                    <tr
                      key={student.student_id}
                      className="hover:bg-[#fafbff]"
                    >
                      <td className="px-5 py-4">
                        <p className="font-bold text-[#172033]">
                          {student.student_name}
                        </p>

                        <p className="mt-1 text-xs text-[#8a93a5]">
                          {student.email}
                          {student.class_name
                            ? ` · ${student.class_name}`
                            : ""}
                        </p>
                      </td>

                      <td className="px-5 py-4 text-sm font-semibold">
                        {student.tests_taken}
                      </td>

                      <td className="px-5 py-4 text-sm font-bold text-[#315bea]">
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

                      <td className="px-5 py-4 text-sm font-semibold text-[#697386]">
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