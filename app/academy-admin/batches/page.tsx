"use client";

import { FormEvent, useEffect, useState } from "react";

type Academy = {
  id: string;
  name: string;
  code: string;
};

type Batch = {
  id: string;
  name: string;
  course_name: string | null;
  class_name?: string | null;
  created_at: string;
};

type Student = {
  id: string;
  name: string;
  email: string;
  roll_number: string | null;
  class_name: string | null;
};

const COURSE_OPTIONS = [
  {
    value: "MHT-CET PCM",
    label: "MHT-CET — PCM",
  },
  {
    value: "MHT-CET PCB",
    label: "MHT-CET — PCB",
  },
  {
    value: "NEET PCB",
    label: "NEET — PCB",
  },
  {
    value: "JEE PCM",
    label: "JEE — PCM",
  },
];

export default function AcademyBatchesPage() {
  const [academies, setAcademies] = useState<Academy[]>([]);
  const [selectedAcademyId, setSelectedAcademyId] =
    useState("");

  const [batches, setBatches] = useState<Batch[]>([]);
  const [students, setStudents] = useState<Student[]>([]);

  const [selectedBatch, setSelectedBatch] =
    useState<Batch | null>(null);

  const [assignedStudents, setAssignedStudents] =
    useState<string[]>([]);

  const [name, setName] = useState("");
  const [className, setClassName] = useState("");
  const [courseName, setCourseName] = useState("");

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [studentLoading, setStudentLoading] =
    useState(false);

  const [academyLoading, setAcademyLoading] =
    useState(true);

  /*
   * ==========================================
   * LOAD ACADEMIES
   * ==========================================
   *
   * Master Admin:
   *   Loads all academies and selects one.
   *
   * Academy Admin:
   *   /api/admin/academies returns 401.
   *   That is okay because their academy comes
   *   directly from their session.
   */
  async function loadAcademies() {
    setAcademyLoading(true);

    try {
      const res = await fetch(
        "/api/admin/academies",
        {
          cache: "no-store",
          credentials: "include",
        }
      );

      const data = await res.json();

      if (
        res.ok &&
        data.success &&
        Array.isArray(data.academies)
      ) {
        const academyList =
          data.academies.map(
            (academy: Academy) => ({
              id: String(academy.id),
              name: academy.name,
              code: academy.code,
            })
          );

        setAcademies(academyList);

        if (
          !selectedAcademyId &&
          academyList.length > 0
        ) {
          setSelectedAcademyId(
            academyList[0].id
          );
        }
      }
    } catch (error) {
      console.error(
        "ACADEMIES LOAD ERROR:",
        error
      );
    } finally {
      setAcademyLoading(false);
    }
  }

  /*
   * ==========================================
   * LOAD STUDENTS
   * ==========================================
   *
   * IMPORTANT:
   * Master Admin must send academyId.
   * Academy Admin does not need it because
   * the backend gets it from the session.
   */
  async function loadStudents() {
    try {
      const query = new URLSearchParams();

      if (selectedAcademyId) {
        query.set(
          "academyId",
          selectedAcademyId
        );
      }

      const url = query.toString()
        ? `/api/academy-admin/students?${query.toString()}`
        : "/api/academy-admin/students";

      const res = await fetch(url, {
        cache: "no-store",
        credentials: "include",
      });

      const data = await res.json();

      if (data.success) {
        setStudents(data.students || []);
      } else {
        console.error(
          "STUDENTS LOAD ERROR:",
          data.error
        );
        setStudents([]);
      }
    } catch (error) {
      console.error(
        "STUDENTS LOAD ERROR:",
        error
      );
      setStudents([]);
    }
  }

  /*
   * ==========================================
   * LOAD BATCHES
   * ==========================================
   */
  async function loadBatches() {
    try {
      const query = new URLSearchParams();

      if (selectedAcademyId) {
        query.set(
          "academyId",
          selectedAcademyId
        );
      }

      const url = query.toString()
        ? `/api/academy-admin/batches?${query.toString()}`
        : "/api/academy-admin/batches";

      const res = await fetch(url, {
        cache: "no-store",
        credentials: "include",
      });

      const data = await res.json();

      if (data.success) {
        setBatches(data.batches || []);
      } else {
        setMessage(
          data.error ||
            "Could not load batches."
        );
      }
    } catch (error) {
      console.error(
        "BATCHES LOAD ERROR:",
        error
      );

      setMessage(
        "Could not load batches."
      );
    }
  }

  /*
   * ==========================================
   * INITIAL LOAD
   * ==========================================
   */
  useEffect(() => {
    void loadAcademies();
  }, []);

  /*
   * ==========================================
   * LOAD DATA WHEN ACADEMY CHANGES
   * ==========================================
   */
  useEffect(() => {
    /*
     * Master Admin:
     * Wait until academy is selected.
     */
    if (
      academies.length > 0 &&
      !selectedAcademyId
    ) {
      return;
    }

    void loadBatches();
    void loadStudents();
  }, [
    selectedAcademyId,
    academies.length,
  ]);

  /*
   * ==========================================
   * ACADEMY CHANGE
   * ==========================================
   */
  function handleAcademyChange(
    academyId: string
  ) {
    setSelectedAcademyId(academyId);

    setSelectedBatch(null);
    setAssignedStudents([]);
    setBatches([]);
    setStudents([]);
    setMessage("");
  }

  /*
   * ==========================================
   * MANAGE STUDENTS
   * ==========================================
   */
  async function openManageStudents(
    batch: Batch
  ) {
    setSelectedBatch(batch);
    setStudentLoading(true);

    try {
      const query = new URLSearchParams();

      query.set(
        "batchId",
        String(batch.id)
      );

      if (selectedAcademyId) {
        query.set(
          "academyId",
          selectedAcademyId
        );
      }

      /*
       * IMPORTANT:
       * Use the new batch-students route.
       */
      const res = await fetch(
        `/api/academy-admin/batches/students?${query.toString()}`,
        {
          cache: "no-store",
          credentials: "include",
        }
      );

      const data = await res.json();

      if (data.success) {
        setAssignedStudents(
          (data.students || []).map(
            (student: Student) =>
              String(student.id)
          )
        );
      } else {
        setAssignedStudents([]);

        alert(
          data.error ||
            "Could not load assigned students."
        );
      }
    } catch (error) {
      console.error(
        "ASSIGNED STUDENTS LOAD ERROR:",
        error
      );

      setAssignedStudents([]);

      alert(
        "Could not load assigned students."
      );
    } finally {
      setStudentLoading(false);
    }
  }

  /*
   * ==========================================
   * ADD / REMOVE STUDENT
   * ==========================================
   */
  async function toggleStudent(
    studentId: string
  ) {
    if (!selectedBatch) {
      return;
    }

    const isAssigned =
      assignedStudents.includes(studentId);

    const action = isAssigned
      ? "remove"
      : "add";

    try {
      /*
       * IMPORTANT:
       * Use the new batch-students route.
       */
      const res = await fetch(
        "/api/academy-admin/batches/students",
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          credentials: "include",
          body: JSON.stringify({
            batchId:
              selectedBatch.id,

            studentId,

            action,

            ...(selectedAcademyId
              ? {
                  academyId:
                    selectedAcademyId,
                }
              : {}),
          }),
        }
      );

      const data = await res.json();

      if (!res.ok || !data.success) {
        alert(
          data.error ||
            "Failed to update student."
        );
        return;
      }

      setAssignedStudents(
        (current) =>
          isAssigned
            ? current.filter(
                (id) =>
                  id !== studentId
              )
            : [
                ...current,
                studentId,
              ]
      );
    } catch (error) {
      console.error(
        "TOGGLE STUDENT ERROR:",
        error
      );

      alert(
        "Something went wrong."
      );
    }
  }

  /*
   * ==========================================
   * CREATE BATCH
   * ==========================================
   */
  async function createBatch(
    e: FormEvent
  ) {
    e.preventDefault();
    setMessage("");

    if (
      !name.trim() ||
      !className.trim() ||
      !courseName.trim()
    ) {
      setMessage(
        "Please fill all details."
      );
      return;
    }

    /*
     * Master Admin must select an academy.
     *
     * Academy Admin uses the academy from
     * their session.
     */
    if (
      academies.length > 0 &&
      !selectedAcademyId
    ) {
      setMessage(
        "Please select an academy."
      );
      return;
    }

    setLoading(true);

    try {
      const body: Record<
        string,
        string
      > = {
        name: name.trim(),
        className:
          className.trim(),
        courseName:
          courseName.trim(),
      };

      if (selectedAcademyId) {
        body.academyId =
          selectedAcademyId;
      }

      const res = await fetch(
        "/api/academy-admin/batches",
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          credentials: "include",
          body: JSON.stringify(body),
        }
      );

      const data = await res.json();

      if (!res.ok || !data.success) {
        setMessage(
          data.error ||
            "Failed to create batch."
        );
        return;
      }

      setMessage(
        `${courseName} batch created successfully.`
      );

      setName("");
      setClassName("");
      setCourseName("");

      await loadBatches();
    } catch (error) {
      console.error(
        "CREATE BATCH ERROR:",
        error
      );

      setMessage(
        "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  }

  /*
   * ==========================================
   * REMOVE BATCH
   * ==========================================
   */
  async function removeBatch(
    batch: Batch
  ) {
    if (
      !window.confirm(
        `Remove ${batch.name}? Students are not deleted, but their membership in this batch will be removed.`
      )
    ) {
      return;
    }

    const params = new URLSearchParams();

    params.set(
      "id",
      String(batch.id)
    );

    /*
     * Master Admin needs academyId.
     * Academy Admin can omit it.
     */
    if (selectedAcademyId) {
      params.set(
        "academyId",
        selectedAcademyId
      );
    }

    try {
      const response = await fetch(
        `/api/academy-admin/batches?${params.toString()}`,
        {
          method: "DELETE",
          credentials: "include",
        }
      );

      const data =
        await response.json();

      if (
        !response.ok ||
        !data.success
      ) {
        setMessage(
          data.error ||
            "Could not remove batch."
        );
        return;
      }

      setBatches(
        (current) =>
          current.filter(
            (item) =>
              item.id !== batch.id
          )
      );

      if (
        selectedBatch?.id ===
        batch.id
      ) {
        setSelectedBatch(null);
        setAssignedStudents([]);
      }

      setMessage(
        "Batch removed."
      );
    } catch (error) {
      console.error(
        "REMOVE BATCH ERROR:",
        error
      );

      setMessage(
        "Could not remove batch."
      );
    }
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <header className="border-b border-[#e7eaf0] bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-xl font-extrabold">
              Batch Management
            </h1>

            <p className="mt-1 text-xs font-bold tracking-wider text-[#315bea]">
              ACADEMY ADMIN
            </p>
          </div>

          <button
            onClick={() =>
              history.back()
            }
            className="rounded-xl border border-[#e2e6ee] bg-white px-4 py-2.5 text-sm font-bold text-[#697386]"
          >
            ← Back
          </button>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-10">
        <div className="mb-10">
          <p className="text-xs font-bold uppercase tracking-[0.15em] text-[#315bea]">
            Academy Management
          </p>

          <h2 className="mt-2 text-3xl font-extrabold">
            Batches
          </h2>

          <p className="mt-2 text-sm text-[#697386]">
            Create and manage classes and
            batches for your academy.
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-[360px_1fr]">
          {/* CREATE BATCH */}
          <form
            onSubmit={createBatch}
            className="h-fit rounded-2xl border border-[#e3e8f5] bg-white p-6 shadow-sm"
          >
            <h3 className="text-lg font-extrabold">
              Create Batch
            </h3>

            {/* MASTER ADMIN ACADEMY SELECTOR */}
            {academies.length > 0 && (
              <select
                required
                value={
                  selectedAcademyId
                }
                onChange={(e) =>
                  handleAcademyChange(
                    e.target.value
                  )
                }
                className="mt-5 w-full rounded-xl border border-[#dfe4ee] bg-white px-4 py-3 text-sm outline-none focus:border-[#315bea]"
              >
                <option value="">
                  Select academy
                </option>

                {academies.map(
                  (academy) => (
                    <option
                      key={
                        academy.id
                      }
                      value={
                        academy.id
                      }
                    >
                      {academy.name}{" "}
                      ({academy.code})
                    </option>
                  )
                )}
              </select>
            )}

            <input
              required
              value={name}
              onChange={(e) =>
                setName(
                  e.target.value
                )
              }
              placeholder="Batch name"
              className="mt-5 w-full rounded-xl border border-[#dfe4ee] px-4 py-3 text-sm outline-none focus:border-[#315bea]"
            />

            <select
              required
              value={courseName}
              onChange={(e) =>
                setCourseName(
                  e.target.value
                )
              }
              className="mt-3 w-full rounded-xl border border-[#dfe4ee] bg-white px-4 py-3 text-sm outline-none focus:border-[#315bea]"
            >
              <option value="">
                Select course / stream
              </option>

              {COURSE_OPTIONS.map(
                (option) => (
                  <option
                    key={
                      option.value
                    }
                    value={
                      option.value
                    }
                  >
                    {option.label}
                  </option>
                )
              )}
            </select>

          
           

            <button
              disabled={
                loading ||
                academyLoading
              }
              type="submit"
              className="mt-5 w-full rounded-xl bg-[#315bea] px-4 py-3 text-sm font-bold text-white disabled:opacity-50"
            >
              {loading
                ? "Creating..."
                : "Create Batch"}
            </button>

            {message && (
              <p className="mt-4 text-sm font-medium text-[#697386]">
                {message}
              </p>
            )}
          </form>

          {/* BATCH LIST */}
          <section className="rounded-2xl border border-[#e3e8f5] bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-extrabold">
                Academy Batches
              </h3>

              <span className="rounded-full bg-[#f2f5ff] px-3 py-1 text-xs font-bold text-[#315bea]">
                {batches.length}{" "}
                batches
              </span>
            </div>

            <div className="mt-5 space-y-3">
              {batches.length ===
              0 ? (
                <div className="rounded-xl border border-dashed border-[#dfe4ee] p-8 text-center text-sm text-[#697386]">
                  No batches yet.
                </div>
              ) : (
                batches.map(
                  (batch) => (
                    <div
                      key={
                        batch.id
                      }
                      className="flex items-center justify-between rounded-xl border border-[#e7eaf0] p-4"
                    >
                      <div>
                        <p className="font-bold">
                          {
                            batch.name
                          }
                        </p>

                        {batch.course_name && (
                          <p className="mt-1 text-sm font-semibold text-[#315bea]">
                            {
                              batch.course_name
                            }
                          </p>
                        )}

                        {batch.class_name && (
                          <p className="mt-1 text-sm text-[#697386]">
                            Class:{" "}
                            {
                              batch.class_name
                            }
                          </p>
                        )}
                      </div>

                      <div className="flex items-center gap-3">
                        <button
                          onClick={() =>
                            openManageStudents(
                              batch
                            )
                          }
                          className="rounded-lg bg-[#eef2ff] px-3 py-1.5 text-xs font-bold text-[#315bea] hover:bg-[#e3e9ff]"
                        >
                          Manage
                          Students
                        </button>

                        <button
                          onClick={() =>
                            void removeBatch(
                              batch
                            )
                          }
                          className="rounded-lg border border-red-200 bg-red-50 px-3 py-1.5 text-xs font-bold text-red-600"
                        >
                          Remove
                        </button>

                        <span className="rounded-lg bg-[#f4f6fa] px-3 py-1.5 text-xs font-bold text-[#697386]">
                          Batch
                        </span>
                      </div>
                    </div>
                  )
                )
              )}
            </div>
          </section>
        </div>
      </div>

      {/* MANAGE STUDENTS MODAL */}
      {selectedBatch && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
          <div className="max-h-[80vh] w-full max-w-2xl overflow-hidden rounded-2xl bg-white shadow-2xl">
            <div className="flex items-center justify-between border-b border-[#e7eaf0] px-6 py-5">
              <div>
                <h3 className="text-lg font-extrabold">
                  Manage Students
                </h3>

                <p className="mt-1 text-sm text-[#697386]">
                  {
                    selectedBatch.name
                  }
                </p>

                {selectedBatch.course_name && (
                  <p className="mt-1 text-xs font-bold text-[#315bea]">
                    {
                      selectedBatch.course_name
                    }
                  </p>
                )}
              </div>

              <button
                onClick={() => {
                  setSelectedBatch(
                    null
                  );
                  setAssignedStudents(
                    []
                  );
                }}
                className="rounded-lg border border-[#e2e6ee] px-3 py-2 text-sm font-bold text-[#697386]"
              >
                ×
              </button>
            </div>

            <div className="max-h-[60vh] overflow-y-auto p-6">
              {studentLoading ? (
                <div className="py-10 text-center text-sm text-[#697386]">
                  Loading
                  students...
                </div>
              ) : students.length ===
                0 ? (
                <div className="rounded-xl border border-dashed border-[#dfe4ee] p-8 text-center text-sm text-[#697386]">
                  No students in
                  this academy
                  yet.
                </div>
              ) : (
                <div className="space-y-2">
                  {students.map(
                    (student) => {
                      const assigned =
                        assignedStudents.includes(
                          String(
                            student.id
                          )
                        );

                      return (
                        <button
                          key={
                            student.id
                          }
                          onClick={() =>
                            void toggleStudent(
                              String(
                                student.id
                              )
                            )
                          }
                          className={`flex w-full items-center justify-between rounded-xl border p-4 text-left transition ${
                            assigned
                              ? "border-[#315bea] bg-[#f2f5ff]"
                              : "border-[#e7eaf0] bg-white hover:bg-[#fafbfe]"
                          }`}
                        >
                          <div>
                            <p className="font-bold">
                              {
                                student.name
                              }
                            </p>

                            <p className="mt-1 text-xs text-[#697386]">
                              {
                                student.email
                              }

                              {student.roll_number
                                ? ` • Roll No. ${student.roll_number}`
                                : ""}
                            </p>
                          </div>

                          <div
                            className={`flex h-6 w-6 items-center justify-center rounded-md border text-xs font-extrabold ${
                              assigned
                                ? "border-[#315bea] bg-[#315bea] text-white"
                                : "border-[#d8deea] bg-white text-transparent"
                            }`}
                          >
                            {assigned
                              ? "✓"
                              : ""}
                          </div>
                        </button>
                      );
                    }
                  )}
                </div>
              )}
            </div>

            <div className="border-t border-[#e7eaf0] px-6 py-4">
              <div className="flex items-center justify-between">
                <p className="text-sm font-bold text-[#697386]">
                  {
                    assignedStudents.length
                  }{" "}
                  student
                  {assignedStudents.length ===
                  1
                    ? ""
                    : "s"}{" "}
                  assigned
                </p>

                <button
                  onClick={() => {
                    setSelectedBatch(
                      null
                    );
                    setAssignedStudents(
                      []
                    );
                  }}
                  className="rounded-xl bg-[#315bea] px-5 py-2.5 text-sm font-bold text-white"
                >
                  Done
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}