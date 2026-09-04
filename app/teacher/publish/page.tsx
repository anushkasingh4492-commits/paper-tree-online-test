"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type Batch = {
  id: string;
  name: string;
  class_name?: string | null;
};

type Student = {
  id: string;
  name: string;
  email: string;
  roll_number?: string | null;
  class_name?: string | null;
};

export default function TeacherPublishPage() {
  const router = useRouter();

  const [test, setTest] = useState<any>(null);
  const [title, setTitle] = useState("Scheduled Test");
  const [startTime, setStartTime] = useState("");
  const [duration, setDuration] = useState(60);

  const [loading, setLoading] = useState(false);
  const [loadingTargets, setLoadingTargets] = useState(true);
  const [message, setMessage] = useState("");

  const [targetType, setTargetType] =
    useState<"batch" | "student">("batch");

  const [batches, setBatches] = useState<Batch[]>([]);
  const [students, setStudents] = useState<Student[]>([]);

  const [batchId, setBatchId] = useState("");
  const [studentId, setStudentId] = useState("");

  /*
   * =======================================================
   * LOAD GENERATED TEST
   * =======================================================
   */

  useEffect(() => {
    const saved = localStorage.getItem(
      "teacherGeneratedTest"
    );

    if (!saved) {
      router.push("/teacher/generate");
      return;
    }

    try {
      const data = JSON.parse(saved);

      setTest(data);

      if (data.questionCount) {
        setTitle(
          `Test - ${data.questionCount} Questions`
        );
      }

      if (data.duration) {
        setDuration(Number(data.duration));
      }
    } catch {
      router.push("/teacher/generate");
    }
  }, [router]);

  /*
   * =======================================================
   * LOAD TEACHER TARGETS
   * =======================================================
   */

  useEffect(() => {
    async function loadTargets() {
      setLoadingTargets(true);

      try {
        const response = await fetch(
          "/api/teacher/targets",
          {
            credentials: "include",
          }
        );

        const data = await response.json();

        if (!response.ok || !data.success) {
          throw new Error(
            data.error ||
              "Could not load batches and students."
          );
        }

        setBatches(
          Array.isArray(data.batches)
            ? data.batches
            : []
        );

        setStudents(
          Array.isArray(data.students)
            ? data.students
            : []
        );
      } catch (error) {
        console.error(
          "LOAD TEACHER TARGETS ERROR:",
          error
        );

        setMessage(
          error instanceof Error
            ? error.message
            : "Could not load batches and students."
        );
      } finally {
        setLoadingTargets(false);
      }
    }

    loadTargets();
  }, []);

  /*
   * =======================================================
   * PUBLISH TEST
   * =======================================================
   */

  async function publishTest() {
    if (!startTime) {
      setMessage(
        "Please select the test start time."
      );
      return;
    }

    if (duration < 1) {
      setMessage(
        "Duration must be at least 1 minute."
      );
      return;
    }

    if (
      targetType === "batch" &&
      !batchId
    ) {
      setMessage(
        "Please select a batch."
      );
      return;
    }

    if (
      targetType === "student" &&
      !studentId
    ) {
      setMessage(
        "Please select a student."
      );
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const start = new Date(startTime);

      if (Number.isNaN(start.getTime())) {
        throw new Error(
          "Invalid start date and time."
        );
      }

      const end = new Date(
        start.getTime() +
          duration * 60 * 1000
      );

      const response = await fetch(
        "/api/teacher/publish-test",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          credentials: "include",

          body: JSON.stringify({
            title: title.trim() || "Scheduled Test",

            startTime:
              start.toISOString(),

            endTime:
              end.toISOString(),

            duration,

            test,

            batchId:
              targetType === "batch"
                ? batchId
                : null,

            studentId:
              targetType === "student"
                ? studentId
                : null,
          }),
        }
      );

      const data =
        await response.json();

      if (
        !response.ok ||
        !data.success
      ) {
        throw new Error(
          data.error ||
            "Could not publish test."
        );
      }

      localStorage.removeItem(
        "teacherGeneratedTest"
      );

      setMessage(
        targetType === "batch"
          ? "Test published successfully to the selected batch."
          : "Test published successfully to the selected student."
      );

      setTimeout(() => {
        router.push("/teacher");
      }, 1500);
    } catch (error) {
      console.error(
        "PUBLISH TEST ERROR:",
        error
      );

      setMessage(
        error instanceof Error
          ? error.message
          : "Could not publish test."
      );
    } finally {
      setLoading(false);
    }
  }

  /*
   * =======================================================
   * LOADING
   * =======================================================
   */

  if (!test) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#f6f8fc]">
        <p className="text-gray-500">
          Loading...
        </p>
      </main>
    );
  }

  /*
   * =======================================================
   * PAGE
   * =======================================================
   */

  return (
    <main className="min-h-screen bg-[#f6f8fc]">
      <div className="mx-auto max-w-4xl px-6 py-10">

        <button
          type="button"
          onClick={() =>
            router.push(
              "/teacher/generate"
            )
          }
          className="mb-6 text-sm font-semibold text-[#315bea]"
        >
          ← Back
        </button>

        <div className="rounded-2xl bg-white p-8 shadow-sm">

          <p className="text-sm font-bold uppercase tracking-wider text-[#315bea]">
            Teacher Portal
          </p>

          <h1 className="mt-2 text-3xl font-bold">
            Publish Test
          </h1>

          <p className="mt-2 text-gray-500">
            Schedule this test for your students.
          </p>

          {/* =================================================
              TEST DETAILS
              ================================================= */}

          <div className="mt-8 space-y-6">

            <div>
              <label className="mb-2 block text-sm font-semibold">
                Test Title
              </label>

              <input
                value={title}
                onChange={(e) =>
                  setTitle(
                    e.target.value
                  )
                }
                className="w-full rounded-xl border px-4 py-3 outline-none focus:border-[#315bea]"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm font-semibold">
                Start Date & Time
              </label>

              <input
                type="datetime-local"
                value={startTime}
                onChange={(e) =>
                  setStartTime(
                    e.target.value
                  )
                }
                className="w-full rounded-xl border px-4 py-3 outline-none focus:border-[#315bea]"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm font-semibold">
                Duration (minutes)
              </label>

              <input
                type="number"
                min={1}
                value={duration}
                onChange={(e) =>
                  setDuration(
                    Math.max(
                      1,
                      Number(
                        e.target.value
                      ) || 1
                    )
                  )
                }
                className="w-full rounded-xl border px-4 py-3 outline-none focus:border-[#315bea]"
              />
            </div>

          </div>

          {/* =================================================
              TARGETING
              ================================================= */}

          <div className="mt-8 border-t pt-8">

            <h2 className="text-lg font-bold">
              Who should receive this test?
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              Choose an entire batch or assign the
              test to one student.
            </p>

            {/* Target type */}

            <div className="mt-5 grid gap-3 md:grid-cols-2">

              <button
                type="button"
                onClick={() => {
                  setTargetType("batch");
                  setStudentId("");
                }}
                className={`rounded-xl border-2 p-4 text-left transition ${
                  targetType === "batch"
                    ? "border-[#315bea] bg-blue-50"
                    : "border-gray-200 bg-white"
                }`}
              >
                <p className="font-bold">
                  Assign to Batch
                </p>

                <p className="mt-1 text-sm text-gray-500">
                  All students in the selected
                  batch will receive the test.
                </p>
              </button>

              <button
                type="button"
                onClick={() => {
                  setTargetType("student");
                  setBatchId("");
                }}
                className={`rounded-xl border-2 p-4 text-left transition ${
                  targetType === "student"
                    ? "border-[#315bea] bg-blue-50"
                    : "border-gray-200 bg-white"
                }`}
              >
                <p className="font-bold">
                  Assign to One Student
                </p>

                <p className="mt-1 text-sm text-gray-500">
                  Only the selected student
                  will receive the test.
                </p>
              </button>

            </div>

            {/* =================================================
                BATCH
                ================================================= */}

            {targetType === "batch" && (
              <div className="mt-5">

                <label className="mb-2 block text-sm font-semibold">
                  Select Batch
                </label>

                <select
                  value={batchId}
                  onChange={(e) =>
                    setBatchId(
                      e.target.value
                    )
                  }
                  disabled={loadingTargets}
                  className="w-full rounded-xl border px-4 py-3 outline-none focus:border-[#315bea]"
                >
                  <option value="">
                    {loadingTargets
                      ? "Loading batches..."
                      : "Select a batch"}
                  </option>

                  {batches.map(
                    (batch) => (
                      <option
                        key={batch.id}
                        value={batch.id}
                      >
                        {batch.name}
                        {batch.class_name
                          ? ` — ${batch.class_name}`
                          : ""}
                      </option>
                    )
                  )}
                </select>

                {!loadingTargets &&
                  batches.length === 0 && (
                    <p className="mt-2 text-sm text-amber-600">
                      No batches are available
                      in your academy.
                    </p>
                  )}

              </div>
            )}

            {/* =================================================
                STUDENT
                ================================================= */}

            {targetType === "student" && (
              <div className="mt-5">

                <label className="mb-2 block text-sm font-semibold">
                  Select Student
                </label>

                <select
                  value={studentId}
                  onChange={(e) =>
                    setStudentId(
                      e.target.value
                    )
                  }
                  disabled={loadingTargets}
                  className="w-full rounded-xl border px-4 py-3 outline-none focus:border-[#315bea]"
                >
                  <option value="">
                    {loadingTargets
                      ? "Loading students..."
                      : "Select a student"}
                  </option>

                  {students.map(
                    (student) => (
                      <option
                        key={student.id}
                        value={student.id}
                      >
                        {student.name}
                        {student.email
                          ? ` — ${student.email}`
                          : ""}
                      </option>
                    )
                  )}
                </select>

                {!loadingTargets &&
                  students.length === 0 && (
                    <p className="mt-2 text-sm text-amber-600">
                      No students are available
                      in your academy.
                    </p>
                  )}

              </div>
            )}

            {/* =================================================
                TARGET SUMMARY
                ================================================= */}

            {targetType === "batch" &&
              batchId && (
                <div className="mt-4 rounded-xl bg-blue-50 p-4 text-sm text-blue-700">
                  This test will be assigned to
                  the selected batch.
                </div>
              )}

            {targetType === "student" &&
              studentId && (
                <div className="mt-4 rounded-xl bg-blue-50 p-4 text-sm text-blue-700">
                  This test will be assigned only
                  to the selected student.
                </div>
              )}

          </div>

          {/* =================================================
              QUESTION SUMMARY
              ================================================= */}

          <div className="mt-8 rounded-xl bg-gray-50 p-5">

            <p className="font-semibold">
              Questions
            </p>

            <p className="mt-1 text-gray-600">
              {test.questionCount ||
                "Generated"}{" "}
              questions
            </p>

          </div>

          {/* =================================================
              MESSAGE
              ================================================= */}

          {message && (
            <div className="mt-6 rounded-xl bg-blue-50 p-4 text-sm text-blue-700">
              {message}
            </div>
          )}

          {/* =================================================
              PUBLISH
              ================================================= */}

          <button
            type="button"
            onClick={publishTest}
            disabled={
              loading ||
              loadingTargets ||
              (targetType === "batch" &&
                !batchId) ||
              (targetType === "student" &&
                !studentId)
            }
            className="mt-8 w-full rounded-xl bg-[#315bea] px-5 py-4 font-bold text-white hover:bg-[#264ac7] disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading
              ? "Publishing..."
              : "Publish & Notify Students"}
          </button>

        </div>
      </div>
    </main>
  );
}