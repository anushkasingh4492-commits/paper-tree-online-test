"use client";

import {
  FormEvent,
  ReactNode,
  useEffect,
  useMemo,
  useState,
} from "react";
import { useRouter } from "next/navigation";

type Academy = {
  id: string;
  name: string;
  code: string;
  domain?: string;
  logo_data?: string;
  teacher_count: number;
  student_count: number;
  batch_count?: number;
  subscription_plan?: string;
  student_limit?: number;
  subscription_start?: string;
  subscription_end?: string;
  status?: string;
};

type Details = {
  academy: Record<string, unknown>;
  students: Record<string, unknown>[];
  teachers: Record<string, unknown>[];
  batches: Record<string, unknown>[];
  papers: Record<string, unknown>[];
  scheduledTests: Record<string, unknown>[];
  questions: Record<string, unknown>[];
};

type Section =
  | "overview"
  | "students"
  | "teachers"
  | "batches"
  | "tests"
  | "subscription";

type Toast = {
  id: number;
  kind: "success" | "error" | "info";
  text: string;
};

const CLASS_OPTIONS = [
  "Class 11",
  "Class 12",
  "Class 11 + 12",
];

const BATCH_COURSE_OPTIONS = [
  "MHT-CET PCM",
  "MHT-CET PCB",
  "NEET PCB",
  "JEE PCM",
];

export default function AcademiesPage() {
  const router = useRouter();

  const [academies, setAcademies] = useState<Academy[]>([]);
  const [loading, setLoading] = useState(true);

  const [selectedAcademy, setSelectedAcademy] =
    useState<Academy | null>(null);

  const [section, setSection] =
    useState<Section>("overview");

  const [details, setDetails] = useState<Details | null>(null);
  const [detailsLoading, setDetailsLoading] = useState(false);
  const [saving, setSaving] = useState(false);

  const [toasts, setToasts] = useState<Toast[]>([]);

  const [academySearch, setAcademySearch] = useState("");
  const [studentSearch, setStudentSearch] = useState("");
  const [teacherSearch, setTeacherSearch] = useState("");
  const [batchSearch, setBatchSearch] = useState("");

  const [openBatch, setOpenBatch] =
    useState<string | null>(null);

  const [batchStudents, setBatchStudents] =
    useState<Record<string, Record<string, unknown>[]>>({});

  const [batchLoading, setBatchLoading] =
    useState<string | null>(null);

  const [modal, setModal] = useState<
    null | {
      type:
        | "student"
        | "teacher"
        | "batch"
        | "subscription"
        | "delete";
      entityType?: "student" | "teacher" | "batch";
      id?: string;
      title?: string;
    }
  >(null);

  const [modalValue, setModalValue] = useState("");
  const [modalValue2, setModalValue2] = useState("");
  const [modalValue3, setModalValue3] = useState("");

  const [academyName, setAcademyName] = useState("");
  const [academyCode, setAcademyCode] = useState("");

  const [adminName, setAdminName] = useState("");
  const [adminEmail, setAdminEmail] = useState("");
  const [adminPassword, setAdminPassword] = useState("");

  const [studentName, setStudentName] = useState("");
  const [studentEmail, setStudentEmail] = useState("");
  const [studentPassword, setStudentPassword] = useState("");
  const [studentClass, setStudentClass] = useState("");

  const [teacherName, setTeacherName] = useState("");
  const [teacherEmail, setTeacherEmail] = useState("");
  const [teacherPassword, setTeacherPassword] = useState("");

  const [batchName, setBatchName] = useState("");
  const [batchClass, setBatchClass] = useState("");
  const [batchCourse, setBatchCourse] = useState("");

  const [subscriptionSeats, setSubscriptionSeats] =
    useState("50");

  const [subscriptionMonths, setSubscriptionMonths] =
    useState("12");

  const [startDate, setStartDate] = useState(
    new Date().toISOString().slice(0, 10)
  );

  const [academyBrandName, setAcademyBrandName] =
    useState("");

  const [academyLogoData, setAcademyLogoData] =
    useState("");

  const [academyDomain, setAcademyDomain] =
    useState("");

  const [brandSaving, setBrandSaving] =
    useState(false);

  const notify = (
    text: string,
    kind: Toast["kind"] = "success"
  ) => {
    const id = Date.now() + Math.random();

    setToasts((t) => [
      ...t,
      {
        id,
        text,
        kind,
      },
    ]);

    window.setTimeout(() => {
      setToasts((t) =>
        t.filter((x) => x.id !== id)
      );
    }, 3500);
  };

  async function loadAcademies() {
    try {
      setLoading(true);

      const res = await fetch(
        "/api/admin/academies",
        {
          cache: "no-store",
          credentials: "include",
        }
      );

      const data = await res.json();

      if (!res.ok || !data.success) {
        throw new Error(
          data.error || "Failed to load academies"
        );
      }

      setAcademies(data.academies || []);

      if (selectedAcademy) {
        const fresh = (
          data.academies || []
        ).find(
          (a: Academy) =>
            a.id === selectedAcademy.id
        );

        if (fresh) {
          setSelectedAcademy(fresh);
        }
      }
    } catch (e) {
      notify(
        e instanceof Error
          ? e.message
          : "Failed to load academies",
        "error"
      );
    } finally {
      setLoading(false);
    }
  }

  async function loadDetails(academyId: string) {
    try {
      setDetailsLoading(true);

      const res = await fetch(
        `/api/admin/academies/${academyId}/details`,
        {
          cache: "no-store",
          credentials: "include",
        }
      );

      const data = await res.json();

      if (!res.ok || !data.success) {
        throw new Error(
          data.error ||
            "Failed to load academy details"
        );
      }

      setDetails(data);
    } catch (e) {
      notify(
        e instanceof Error
          ? e.message
          : "Failed to load academy details",
        "error"
      );

      setDetails(null);
    } finally {
      setDetailsLoading(false);
    }
  }

  useEffect(() => {
    loadAcademies();
  }, []);

  useEffect(() => {
    if (selectedAcademy) {
      loadDetails(selectedAcademy.id);
    } else {
      setDetails(null);
    }
  }, [selectedAcademy?.id]);

  const totals = useMemo(
    () => ({
      academies: academies.length,

      students: academies.reduce(
        (n, a) =>
          n + Number(a.student_count || 0),
        0
      ),

      teachers: academies.reduce(
        (n, a) =>
          n + Number(a.teacher_count || 0),
        0
      ),

      batches: academies.reduce(
        (n, a) =>
          n + Number(a.batch_count || 0),
        0
      ),
    }),
    [academies]
  );

  const filteredAcademies =
    academies.filter((a) =>
      `${a.name} ${a.code}`
        .toLowerCase()
        .includes(
          academySearch.toLowerCase()
        )
    );

  async function refreshEverything() {
    await loadAcademies();

    if (selectedAcademy) {
      await loadDetails(selectedAcademy.id);
    }
  }

  function selectAcademy(
    academy: Academy,
    nextSection: Section = "overview"
  ) {
    setSelectedAcademy(academy);

    setAcademyBrandName(academy.name);
    setAcademyLogoData(
      academy.logo_data || ""
    );
    setAcademyDomain(
      academy.domain || ""
    );

    setSection(nextSection);

    setOpenBatch(null);
    setBatchStudents({});

    window.setTimeout(
      () =>
        document
          .getElementById(
            "academy-manager"
          )
          ?.scrollIntoView({
            behavior: "smooth",
            block: "start",
          }),
      20
    );
  }

  async function saveBranding(
    e: FormEvent
  ) {
    e.preventDefault();

    setBrandSaving(true);

    await patchAcademy(
      {
        academyName: academyBrandName,
        logoData: academyLogoData,
        domain: academyDomain,
      },
      "Academy branding updated"
    );

    setBrandSaving(false);
  }

  function readLogo(file: File | undefined) {
    if (!file) return;

    if (
      !file.type.startsWith("image/") ||
      file.size > 1_500_000
    ) {
      notify(
        "Choose an image smaller than 1.5 MB",
        "error"
      );
      return;
    }

    const reader = new FileReader();

    reader.onload = () =>
      setAcademyLogoData(
        String(reader.result || "")
      );

    reader.readAsDataURL(file);
  }

  async function createAcademy(
    e: FormEvent
  ) {
    e.preventDefault();

    setSaving(true);

    try {
      const end = addMonths(
        startDate,
        Number(subscriptionMonths)
      );

      const res = await fetch(
        "/api/admin/academies",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            academyName,
            academyCode,
            adminName,
            adminEmail,
            adminPassword,

            subscriptionPlan:
              `${subscriptionSeats} Students · ${subscriptionMonths} Months`,

            studentLimit:
              Number(subscriptionSeats),

            subscriptionStart:
              startDate,

            subscriptionEnd:
              end,
          }),
        }
      );

      const data = await res.json();

      if (!res.ok || !data.success) {
        throw new Error(
          data.error ||
            "Failed to create academy"
        );
      }

      notify(
        `🏫 ${academyName} created successfully`
      );

      setAcademyName("");
      setAcademyCode("");
      setAdminName("");
      setAdminEmail("");
      setAdminPassword("");

      await loadAcademies();
    } catch (e) {
      notify(
        e instanceof Error
          ? e.message
          : "Failed to create academy",
        "error"
      );
    } finally {
      setSaving(false);
    }
  }

  async function addStudent(
    e: FormEvent
  ) {
    e.preventDefault();

    if (!selectedAcademy) return;

    try {
      const res = await fetch(
        "/api/academy-admin/students",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            academyId:
              selectedAcademy.id,
            name: studentName,
            email: studentEmail,
            password: studentPassword,
            className: studentClass,
          }),
        }
      );

      const data = await res.json();

      if (!res.ok || !data.success) {
        throw new Error(
          data.error ||
            "Failed to create student"
        );
      }

      notify(
        `🎓 ${studentName} created successfully`
      );

      setStudentName("");
      setStudentEmail("");
      setStudentPassword("");
      setStudentClass("");

      await refreshEverything();
    } catch (e) {
      notify(
        e instanceof Error
          ? e.message
          : "Failed to create student",
        "error"
      );
    }
  }

  async function addTeacher(
    e: FormEvent
  ) {
    e.preventDefault();

    if (!selectedAcademy) return;

    try {
      const res = await fetch(
        "/api/academy-admin/teachers",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            academyId:
              selectedAcademy.id,
            name: teacherName,
            email: teacherEmail,
            password: teacherPassword,
          }),
        }
      );

      const data = await res.json();

      if (!res.ok || !data.success) {
        throw new Error(
          data.error ||
            "Failed to create teacher"
        );
      }

      notify(
        `👨‍🏫 ${teacherName} created successfully`
      );

      setTeacherName("");
      setTeacherEmail("");
      setTeacherPassword("");

      await refreshEverything();
    } catch (e) {
      notify(
        e instanceof Error
          ? e.message
          : "Failed to create teacher",
        "error"
      );
    }
  }

  async function addBatch(
    e: FormEvent
  ) {
    e.preventDefault();

    if (!selectedAcademy) {
      notify(
        "Please select an academy first.",
        "error"
      );
      return;
    }

    if (
      !batchName.trim() ||
      !batchClass.trim() ||
      !batchCourse.trim()
    ) {
      notify(
        "Please fill batch name, class and course.",
        "error"
      );
      return;
    }

    try {
      const res = await fetch(
        "/api/academy-admin/batches",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          credentials: "include",

          body: JSON.stringify({
            academyId:
              selectedAcademy.id,

            name: batchName.trim(),

            className:
              batchClass.trim(),

            courseName:
              batchCourse.trim(),
          }),
        }
      );

      const data = await res.json();

      if (!res.ok || !data.success) {
        throw new Error(
          data.error ||
            "Failed to create batch"
        );
      }

      notify(
        `📚 ${batchName} created successfully`
      );

      setBatchName("");
      setBatchClass("");
      setBatchCourse("");

      await refreshEverything();
    } catch (e) {
      notify(
        e instanceof Error
          ? e.message
          : "Failed to create batch",
        "error"
      );
    }
  }

  async function patchAcademy(
    changes: Record<string, unknown>,
    text: string
  ) {
    if (!selectedAcademy) return;

    try {
      const res = await fetch(
        `/api/admin/academies/${selectedAcademy.id}`,
        {
          method: "PATCH",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify(
            changes
          ),
        }
      );

      const data = await res.json();

      if (!res.ok || !data.success) {
        throw new Error(
          data.error ||
            "Failed to update academy"
        );
      }

      notify(text);

      await refreshEverything();
    } catch (e) {
      notify(
        e instanceof Error
          ? e.message
          : "Failed to update academy",
        "error"
      );
    }
  }

  async function deleteAcademy() {
    if (!selectedAcademy) return;

    const academy = selectedAcademy;

    if (
      !window.confirm(
        `Delete ${academy.name}? This permanently removes its admin, students, teachers, batches, papers and tests.`
      )
    ) {
      return;
    }

    try {
      const res = await fetch(
        `/api/admin/academies/${academy.id}`,
        {
          method: "DELETE",
        }
      );

      const data = await res.json();

      if (!res.ok || !data.success) {
        throw new Error(
          data.error ||
            "Academy could not be deleted"
        );
      }

      setSelectedAcademy(null);
      setDetails(null);

      notify(
        `${academy.name} deleted successfully`
      );

      await loadAcademies();
    } catch (e) {
      notify(
        e instanceof Error
          ? e.message
          : "Academy could not be deleted",
        "error"
      );
    }
  }

  function openSubscription() {
    if (!selectedAcademy) return;

    setModal({
      type: "subscription",
      title: "Manage subscription",
    });

    setModalValue(
      String(
        selectedAcademy.student_limit || 0
      )
    );

    setModalValue2(
      selectedAcademy.subscription_end
        ? toDateInput(
            selectedAcademy.subscription_end
          )
        : ""
    );
  }

  async function saveSubscription() {
    const seats = Number(modalValue);

    if (
      !Number.isInteger(seats) ||
      seats < 1 ||
      !modalValue2
    ) {
      notify(
        "Enter a valid seat limit and expiry date",
        "error"
      );

      return;
    }

    setModal(null);

    await patchAcademy(
      {
        studentLimit: seats,
        subscriptionEnd: modalValue2,
      },
      "🎟️ Subscription updated successfully"
    );
  }

  async function extendSubscription(
    months: number
  ) {
    if (!selectedAcademy) return;

    const base =
      selectedAcademy.subscription_end &&
      new Date(
        selectedAcademy.subscription_end
      ) > new Date()
        ? toDateInput(
            selectedAcademy.subscription_end
          )
        : new Date()
            .toISOString()
            .slice(0, 10);

    await patchAcademy(
      {
        subscriptionEnd: addMonths(
          base,
          months
        ),
      },
      `🔄 Subscription extended by ${months} month${
        months === 1 ? "" : "s"
      }`
    );
  }

  async function performDelete() {
    if (
      !selectedAcademy ||
      !modal?.id ||
      !modal.type
    ) {
      return;
    }

    const id = modal.id;
    const type = modal.entityType;

    if (!type) return;

    setModal(null);

    const endpoint =
      type === "student"
        ? `/api/admin/academies/${selectedAcademy.id}/students/${id}`
        : type === "teacher"
        ? `/api/admin/academies/${selectedAcademy.id}/teachers/${id}`
        : `/api/admin/academies/${selectedAcademy.id}/batches/${id}`;

    try {
      const res = await fetch(
        endpoint,
        {
          method: "DELETE",
        }
      );

      const data = await res.json();

      if (!res.ok || !data.success) {
        throw new Error(
          data.error || "Delete failed"
        );
      }

      notify(
        type === "student"
          ? "🗑️ Student removed"
          : type === "teacher"
          ? "🗑️ Teacher removed"
          : "🗑️ Batch removed"
      );

      await refreshEverything();
    } catch (e) {
      notify(
        e instanceof Error
          ? e.message
          : "Delete failed",
        "error"
      );
    }
  }

  async function updateRecord(
    type:
      | "student"
      | "teacher"
      | "batch",
    id: string
  ) {
    if (!selectedAcademy) return;

    const endpoint =
      type === "student"
        ? `/api/admin/academies/${selectedAcademy.id}/students/${id}`
        : type === "teacher"
        ? `/api/admin/academies/${selectedAcademy.id}/teachers/${id}`
        : `/api/admin/academies/${selectedAcademy.id}/batches/${id}`;

    const body =
      type === "student"
        ? {
            name: modalValue,
            email: modalValue2,
            className: modalValue3,
          }
        : type === "teacher"
        ? {
            name: modalValue,
            email: modalValue2,
          }
        : {
            name: modalValue,
            className: modalValue2,
            courseName: modalValue3,
          };

    try {
      const res = await fetch(
        endpoint,
        {
          method: "PATCH",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify(body),
        }
      );

      const data = await res.json();

      if (!res.ok || !data.success) {
        throw new Error(
          data.error || "Update failed"
        );
      }

      setModal(null);

      notify(
        `✏️ ${
          type[0].toUpperCase() +
          type.slice(1)
        } updated`
      );

      await refreshEverything();
    } catch (e) {
      notify(
        e instanceof Error
          ? e.message
          : "Update failed",
        "error"
      );
    }
  }

  async function loadBatchStudents(
    batchId: string,
    toggle = true
  ) {
    if (!selectedAcademy) return;

    if (
      toggle &&
      openBatch === batchId
    ) {
      setOpenBatch(null);
      return;
    }

    setOpenBatch(batchId);
    setBatchLoading(batchId);

    try {
      const res = await fetch(
        `/api/academy-admin/batches/students?batchId=${encodeURIComponent(
          batchId
        )}&academyId=${encodeURIComponent(
          selectedAcademy.id
        )}`,
        {
          cache: "no-store",
        }
      );

      const data = await res.json();

      if (!res.ok || !data.success) {
        throw new Error(
          data.error ||
            "Failed to load batch students"
        );
      }

      setBatchStudents((m) => ({
        ...m,
        [batchId]: data.students || [],
      }));
    } catch (e) {
      notify(
        e instanceof Error
          ? e.message
          : "Failed to load batch students",
        "error"
      );
    } finally {
      setBatchLoading(null);
    }
  }

  async function changeBatchStudent(
    batchId: string,
    studentId: string,
    action: "add" | "remove"
  ) {
    if (!selectedAcademy) return;

    try {
      const res = await fetch(
        "/api/academy-admin/batches/students",
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            batchId,
            studentId,
            action,
            academyId:
              selectedAcademy.id,
          }),
        }
      );

      const data = await res.json();

      if (!res.ok || !data.success) {
        throw new Error(
          data.error ||
            "Failed to update batch"
        );
      }

      notify(
        action === "add"
          ? "➕ Student added to batch"
          : "➖ Student removed from batch"
      );

      await loadBatchStudents(
        batchId,
        false
      );

      await loadDetails(
        selectedAcademy.id
      );
    } catch (e) {
      notify(
        e instanceof Error
          ? e.message
          : "Failed to update batch",
        "error"
      );
    }
  }

  function openEdit(
    type:
      | "student"
      | "teacher"
      | "batch",
    record: Record<string, unknown>
  ) {
    setModal({
      type,
      id: String(record.id),
      title: `Edit ${type}`,
    });

    setModalValue(
      String(record.name ?? "")
    );

    if (
      type === "student" ||
      type === "teacher"
    ) {
      setModalValue2(
        String(record.email ?? "")
      );
    } else {
      setModalValue2(
        String(
          record.class_name ?? ""
        )
      );

      setModalValue3(
        String(
          record.course_name ?? ""
        )
      );
    }

    setModalValue3(
      type === "student"
        ? String(
            record.class_name ?? ""
          )
        : type === "batch"
        ? String(
            record.course_name ?? ""
          )
        : ""
    );
  }

  const students = (
    details?.students || []
  ).filter((s) =>
    `${s.name ?? ""} ${
      s.email ?? ""
    } ${
      s.class_name ?? ""
    }`
      .toLowerCase()
      .includes(
        studentSearch.toLowerCase()
      )
  );

  const teachers = (
    details?.teachers || []
  ).filter((t) =>
    `${t.name ?? ""} ${
      t.email ?? ""
    }`
      .toLowerCase()
      .includes(
        teacherSearch.toLowerCase()
      )
  );

  const batches = (
    details?.batches || []
  ).filter((b) =>
    `${b.name ?? ""} ${
      b.class_name ?? ""
    } ${
      b.course_name ?? ""
    }`
      .toLowerCase()
      .includes(
        batchSearch.toLowerCase()
      )
  );

  return (
    <main className="min-h-screen bg-[#f5f7fb] text-[#172033]">
      <Toasts toasts={toasts} />

      <header className="sticky top-0 z-30 border-b border-[#e3e8f5] bg-white/95 backdrop-blur">
        <div className="mx-auto flex max-w-[1500px] items-center justify-between px-6 py-4">
          <div>
            <p className="text-[10px] font-black uppercase tracking-[0.2em] text-[#315bea]">
              Paper Tree
            </p>

            <h1 className="text-xl font-black">
              MASTER ADMIN · Academy Management
            </h1>
          </div>

          <button
            onClick={() =>
              router.push("/admin")
            }
            className="rounded-xl border border-[#dfe4ed] px-4 py-2 text-sm font-bold hover:bg-[#f7f9fc]"
          >
            ← Dashboard
          </button>
        </div>
      </header>

      <div className="mx-auto max-w-[1500px] space-y-6 px-6 py-7">
        <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <Stat
            title="Academies"
            value={totals.academies}
            icon="🏫"
          />

          <Stat
            title="Students"
            value={totals.students}
            icon="🎓"
          />

          <Stat
            title="Teachers"
            value={totals.teachers}
            icon="👨‍🏫"
          />

          <Stat
            title="Batches"
            value={totals.batches}
            icon="📚"
          />
        </section>

        <section className="rounded-3xl border border-[#e3e8f5] bg-white p-6 shadow-sm">
          <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
            <div>
              <h2 className="text-lg font-black">
                🏫 Create Academy
              </h2>

              <p className="text-xs text-[#697386]">
                Create an academy and its first admin account.
              </p>
            </div>
          </div>

          <form
            onSubmit={createAcademy}
            className="grid gap-3 md:grid-cols-2 xl:grid-cols-4"
          >
            <Field
              label="Academy name"
              value={academyName}
              onChange={setAcademyName}
              placeholder="Academy name"
            />

            <Field
              label="Academy code"
              value={academyCode}
              onChange={setAcademyCode}
              placeholder="ACADEMY01"
            />

            <Field
              label="Admin name"
              value={adminName}
              onChange={setAdminName}
              placeholder="Admin name"
            />

            <Field
              label="Admin email"
              value={adminEmail}
              onChange={setAdminEmail}
              placeholder="admin@example.com"
              type="email"
            />

            <Field
              label="Admin password"
              value={adminPassword}
              onChange={setAdminPassword}
              placeholder="Minimum 6 characters"
              type="password"
            />

            <Field
              label="Student seats"
              value={subscriptionSeats}
              onChange={setSubscriptionSeats}
              placeholder="50"
              type="number"
            />

            <Field
              label="Subscription months"
              value={subscriptionMonths}
              onChange={setSubscriptionMonths}
              placeholder="12"
              type="number"
            />

            <label className="text-xs font-bold">
              Start date

              <input
                type="date"
                value={startDate}
                onChange={(e) =>
                  setStartDate(
                    e.target.value
                  )
                }
                className="mt-1 w-full rounded-xl border border-[#dfe4ed] px-3 py-3 text-sm"
                required
              />
            </label>

            <div className="md:col-span-2 xl:col-span-4">
              <button
                disabled={saving}
                className="rounded-xl bg-[#315bea] px-5 py-3 text-sm font-black text-white disabled:opacity-50"
              >
                {saving
                  ? "Creating…"
                  : "✨ Create Academy"}
              </button>
            </div>
          </form>
        </section>

        <section className="space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h2 className="text-lg font-black">
                Your Academies
              </h2>

              <p className="text-xs text-[#697386]">
                Only live database academies appear here.
              </p>
            </div>

            <input
              value={academySearch}
              onChange={(e) =>
                setAcademySearch(
                  e.target.value
                )
              }
              placeholder="🔍 Search academies"
              className="rounded-xl border border-[#dfe4ed] bg-white px-4 py-3 text-sm outline-none focus:border-[#315bea]"
            />
          </div>

          {loading ? (
            <Empty text="Loading academies…" />
          ) : filteredAcademies.length ===
            0 ? (
            <Empty text="No academies found." />
          ) : (
            <div className="grid gap-4 lg:grid-cols-2 xl:grid-cols-3">
              {filteredAcademies.map(
                (academy) => (
                  <AcademyCard
                    key={academy.id}
                    academy={academy}
                    selected={
                      selectedAcademy?.id ===
                      academy.id
                    }
                    onManage={() =>
                      selectAcademy(academy)
                    }
                  />
                )
              )}
            </div>
          )}
        </section>

        {selectedAcademy && (
          <section
            id="academy-manager"
            className="scroll-mt-24 rounded-3xl border border-[#dce3f3] bg-white shadow-sm"
          >
            <form
              onSubmit={saveBranding}
              className="flex flex-wrap items-end gap-3 border-b border-[#e8ecf4] bg-[#fafbfe] p-5"
            >
              <label className="min-w-[220px] flex-1 text-xs font-bold">
                Institute name

                <input
                  value={academyBrandName}
                  onChange={(e) =>
                    setAcademyBrandName(
                      e.target.value
                    )
                  }
                  className="mt-1 w-full rounded-xl border border-[#dfe4ed] bg-white px-3 py-2.5 text-sm"
                  required
                />
              </label>

              <label className="min-w-[260px] flex-1 text-xs font-bold">
                Custom domain

                <input
                  value={academyDomain}
                  onChange={(e) =>
                    setAcademyDomain(
                      e.target.value
                    )
                  }
                  placeholder="web.infinityclasses.net"
                  className="mt-1 w-full rounded-xl border border-[#dfe4ed] bg-white px-3 py-2.5 text-sm"
                />
              </label>

              <label className="text-xs font-bold">
                Logo

                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) =>
                    readLogo(
                      e.target.files?.[0]
                    )
                  }
                  className="mt-1 block w-full text-xs"
                />
              </label>

              {academyLogoData && (
                <img
                  src={academyLogoData}
                  alt="Logo preview"
                  className="h-11 w-11 rounded-lg border bg-white object-contain"
                />
              )}

              <button
                disabled={brandSaving}
                className="rounded-xl bg-[#315bea] px-4 py-2.5 text-xs font-black text-white disabled:opacity-50"
              >
                {brandSaving
                  ? "Saving..."
                  : "Save Branding"}
              </button>
            </form>

            <div className="border-b border-[#e8ecf4] p-6">
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                  <p className="text-[10px] font-black uppercase tracking-[0.18em] text-[#315bea]">
                    Selected academy
                  </p>

                  <h2 className="mt-1 text-2xl font-black">
                    {selectedAcademy.name}
                  </h2>

                  <p className="mt-1 text-xs text-[#697386]">
                    Code:{" "}
                    {selectedAcademy.code} ·{" "}
                    {statusLabel(
                      selectedAcademy
                    )}
                  </p>
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={deleteAcademy}
                    className="rounded-xl border border-red-200 px-4 py-2 text-xs font-bold text-red-600"
                  >
                    Delete Academy
                  </button>

                  <button
                    onClick={() => {
                      setSelectedAcademy(
                        null
                      );
                      setDetails(null);
                    }}
                    className="rounded-xl border px-4 py-2 text-xs font-bold"
                  >
                    Close
                  </button>
                </div>
              </div>

              <div className="mt-5 grid grid-cols-2 gap-2 md:grid-cols-6">
                {(
                  [
                    [
                      "overview",
                      "🏠 Overview",
                    ],
                    [
                      "students",
                      "🎓 Students",
                    ],
                    [
                      "teachers",
                      "👨‍🏫 Teachers",
                    ],
                    [
                      "batches",
                      "📚 Batches",
                    ],
                    [
                      "tests",
                      "📝 Tests & Papers",
                    ],
                    [
                      "subscription",
                      "🎟️ Subscription",
                    ],
                  ] as [
                    Section,
                    string
                  ][]
                ).map(
                  ([id, label]) => (
                    <button
                      key={id}
                      onClick={() =>
                        setSection(id)
                      }
                      className={`rounded-xl px-3 py-3 text-xs font-black transition ${
                        section === id
                          ? "bg-[#315bea] text-white"
                          : "bg-[#f6f8fc] hover:bg-[#edf1fb]"
                      }`}
                    >
                      {label}
                    </button>
                  )
                )}
              </div>
            </div>

            {detailsLoading ? (
              <div className="p-10 text-center text-sm font-bold text-[#697386]">
                Loading live academy data…
              </div>
            ) : details ? (
              <div className="p-6">
                {section ===
                  "overview" && (
                  <Overview
                    academy={
                      selectedAcademy
                    }
                    details={details}
                    onSection={
                      setSection
                    }
                  />
                )}

                {section ===
                  "students" && (
                  <StudentsPanel
                    students={students}
                    search={
                      studentSearch
                    }
                    setSearch={
                      setStudentSearch
                    }
                    onEdit={openEdit}
                    onDelete={(
                      id: string,
                      name: string
                    ) =>
                      setModal({
                        type: "delete",
                        entityType:
                          "student",
                        id,
                        title: `Remove ${name}?`,
                      })
                    }
                  />
                )}

                {section ===
                  "teachers" && (
                  <TeachersPanel
                    teachers={teachers}
                    search={
                      teacherSearch
                    }
                    setSearch={
                      setTeacherSearch
                    }
                    onEdit={openEdit}
                    onDelete={(
                      id: string,
                      name: string
                    ) =>
                      setModal({
                        type: "delete",
                        entityType:
                          "teacher",
                        id,
                        title: `Remove ${name}?`,
                      })
                    }
                  />
                )}

                {section ===
                  "batches" && (
                  <BatchesPanel
                    batches={batches}
                    students={
                      details.students
                    }
                    search={
                      batchSearch
                    }
                    setSearch={
                      setBatchSearch
                    }
                    openBatch={
                      openBatch
                    }
                    batchStudents={
                      batchStudents
                    }
                    batchLoading={
                      batchLoading
                    }
                    onOpen={
                      loadBatchStudents
                    }
                    onAdd={
                      changeBatchStudent
                    }
                    onEdit={openEdit}
                    onDelete={(
                      id: string,
                      name: string
                    ) =>
                      setModal({
                        type: "delete",
                        entityType:
                          "batch",
                        id,
                        title: `Delete ${name}?`,
                      })
                    }
                  />
                )}

                {section ===
                  "tests" && (
                  <TestsPanel
                    papers={
                      details.papers
                    }
                    scheduledTests={
                      details.scheduledTests
                    }
                    questions={
                      details.questions
                    }
                  />
                )}

                {section ===
                  "subscription" && (
                  <SubscriptionPanel
                    academy={
                      selectedAcademy
                    }
                    onManage={
                      openSubscription
                    }
                    onExtend={
                      extendSubscription
                    }
                  />
                )}

                {section ===
                  "overview" && (
                  <div className="mt-6 grid gap-4 xl:grid-cols-3">
                    <ManagementCard
                      title="🎓 Add Student"
                      description="Create the student first. Then create a batch and assign this student from Manage Batches."
                    >
                      <form
                        onSubmit={
                          addStudent
                        }
                        className="space-y-2"
                      >
                        <Field
                          value={
                            studentName
                          }
                          onChange={
                            setStudentName
                          }
                          placeholder="Student name"
                          label=""
                        />

                        <Field
                          value={
                            studentEmail
                          }
                          onChange={
                            setStudentEmail
                          }
                          placeholder="Student email"
                          type="email"
                          label=""
                        />

                        <Field
                          value={
                            studentPassword
                          }
                          onChange={
                            setStudentPassword
                          }
                          placeholder="Password"
                          type="password"
                          label=""
                        />

                        <Select
                          label="Class"
                          value={
                            studentClass
                          }
                          onChange={
                            setStudentClass
                          }
                          options={
                            CLASS_OPTIONS
                          }
                        />

                        <button className="w-full rounded-xl bg-[#315bea] px-4 py-3 text-xs font-black text-white">
                          ➕ Add Student
                        </button>
                      </form>
                    </ManagementCard>

                    <ManagementCard
                      title="👨‍🏫 Add Teacher"
                      description="Create an academy-specific teacher account."
                    >
                      <form
                        onSubmit={
                          addTeacher
                        }
                        className="space-y-2"
                      >
                        <Field
                          value={
                            teacherName
                          }
                          onChange={
                            setTeacherName
                          }
                          placeholder="Teacher name"
                          label=""
                        />

                        <Field
                          value={
                            teacherEmail
                          }
                          onChange={
                            setTeacherEmail
                          }
                          placeholder="Teacher email"
                          type="email"
                          label=""
                        />

                        <Field
                          value={
                            teacherPassword
                          }
                          onChange={
                            setTeacherPassword
                          }
                          placeholder="Password"
                          type="password"
                          label=""
                        />

                        <button className="mt-2 w-full rounded-xl bg-[#172033] px-4 py-3 text-xs font-black text-white">
                          ➕ Add Teacher
                        </button>
                      </form>
                    </ManagementCard>

                    <ManagementCard
                      title="📚 Create Batch"
                      description="Create a batch with its exam/course assignment, then add existing academy students to it."
                    >
                      <form
                        onSubmit={
                          addBatch
                        }
                        className="space-y-2"
                      >
                        <Field
                          value={
                            batchName
                          }
                          onChange={
                            setBatchName
                          }
                          placeholder="Batch name"
                          label=""
                        />

                        <Select
                          label="Class"
                          value={
                            batchClass
                          }
                          onChange={
                            setBatchClass
                          }
                          options={
                            CLASS_OPTIONS
                          }
                        />

                        <Select
                          label="Course / Exam"
                          value={
                            batchCourse
                          }
                          onChange={
                            setBatchCourse
                          }
                          options={
                            BATCH_COURSE_OPTIONS
                          }
                        />

                        <button className="w-full rounded-xl bg-[#315bea] px-4 py-3 text-xs font-black text-white">
                          ✨ Create Batch
                        </button>
                      </form>
                    </ManagementCard>
                  </div>
                )}
              </div>
            ) : (
              <Empty text="No details available." />
            )}
          </section>
        )}
      </div>

      {modal && (
        <Modal
          modal={modal}
          value={modalValue}
          value2={modalValue2}
          value3={modalValue3}
          setValue={setModalValue}
          setValue2={setModalValue2}
          setValue3={setModalValue3}
          onClose={() =>
            setModal(null)
          }
          onConfirm={
            modal.type === "delete"
              ? performDelete
              : modal.type ===
                "subscription"
              ? saveSubscription
              : () =>
                  updateRecord(
                    modal.type as
                      | "student"
                      | "teacher"
                      | "batch",
                    modal.id!
                  )
          }
        />
      )}
    </main>
  );
}

function Overview({
  academy,
  details,
  onSection,
}: {
  academy: Academy;
  details: Details;
  onSection: (
    s: Section
  ) => void;
}) {
  const seats = Number(
    academy.student_limit || 0
  );

  const used =
    details.students.length;

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <BigStat
          icon="🎓"
          label="Students"
          value={used}
          sub={`${Math.max(
            seats - used,
            0
          )} seats remaining`}
        />

        <BigStat
          icon="👨‍🏫"
          label="Teachers"
          value={
            details.teachers.length
          }
          sub="Academy-specific accounts"
        />

        <BigStat
          icon="📚"
          label="Batches"
          value={
            details.batches.length
          }
          sub="Active academy batches"
        />

        <BigStat
          icon="📝"
          label="Papers"
          value={
            details.papers.length
          }
          sub={`${details.questions.length} linked questions`}
        />
      </div>

      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        {[
          [
            "🎓",
            "Manage Students",
            "students",
          ],
          [
            "👨‍🏫",
            "Manage Teachers",
            "teachers",
          ],
          [
            "📚",
            "Manage Batches",
            "batches",
          ],
          [
            "📝",
            "Tests & Papers",
            "tests",
          ],
        ].map(
          ([icon, label, id]) => (
            <button
              key={id}
              onClick={() =>
                onSection(
                  id as Section
                )
              }
              className="rounded-2xl border border-[#e3e8f5] p-5 text-left transition hover:-translate-y-0.5 hover:border-[#315bea]"
            >
              <span className="text-2xl">
                {icon}
              </span>

              <p className="mt-3 text-sm font-black">
                {label}
              </p>

              <p className="mt-1 text-xs text-[#697386]">
                Open live academy data →
              </p>
            </button>
          )
        )}
      </div>
    </div>
  );
}

function StudentsPanel({
  students,
  search,
  setSearch,
  onEdit,
  onDelete,
}: any) {
  return (
    <Panel
      title="🎓 Manage Students"
      count={students.length}
      search={search}
      setSearch={setSearch}
      placeholder="Search name, email or class"
    >
      <div className="grid gap-3">
        {students.length ? (
          students.map(
            (s: any) => (
              <RecordCard
                key={s.id}
                icon="🎓"
                title={String(
                  s.name || "-"
                )}
                meta={String(
                  s.email || "-"
                )}
                lines={[
                  `Class: ${
                    s.class_name || "-"
                  }`,
                  `Password: ${
                    s.has_password
                      ? "Set securely"
                      : "Not set"
                  }`,
                  `Created: ${formatDate(
                    s.created_at
                  )}`,
                ]}
                actions={
                  <>
                    <button
                      onClick={() =>
                        onEdit(
                          "student",
                          s
                        )
                      }
                      className="rounded-lg border px-3 py-2 text-xs font-bold"
                    >
                      ✏️ Edit
                    </button>

                    <button
                      onClick={() =>
                        onDelete(
                          String(s.id),
                          String(
                            s.name ||
                              "student"
                          )
                        )
                      }
                      className="rounded-lg border border-red-200 px-3 py-2 text-xs font-bold text-red-600"
                    >
                      🗑️ Remove
                    </button>
                  </>
                }
              />
            )
          )
        ) : (
          <Empty text="No students in this academy." />
        )}
      </div>
    </Panel>
  );
}

function TeachersPanel({
  teachers,
  search,
  setSearch,
  onEdit,
  onDelete,
}: any) {
  return (
    <Panel
      title="👨‍🏫 Manage Teachers"
      count={teachers.length}
      search={search}
      setSearch={setSearch}
      placeholder="Search teacher or email"
    >
      <div className="grid gap-3">
        {teachers.length ? (
          teachers.map(
            (t: any) => (
              <RecordCard
                key={t.id}
                icon="👨‍🏫"
                title={String(
                  t.name || "-"
                )}
                meta={String(
                  t.email || "-"
                )}
                lines={[
                  `Password: ${
                    t.has_password
                      ? "Set securely"
                      : "Not set"
                  }`,
                  `Created: ${formatDate(
                    t.created_at
                  )}`,
                ]}
                actions={
                  <>
                    <button
                      onClick={() =>
                        onEdit(
                          "teacher",
                          t
                        )
                      }
                      className="rounded-lg border px-3 py-2 text-xs font-bold"
                    >
                      ✏️ Edit
                    </button>

                    <button
                      onClick={() =>
                        onDelete(
                          String(t.id),
                          String(
                            t.name ||
                              "teacher"
                          )
                        )
                      }
                      className="rounded-lg border border-red-200 px-3 py-2 text-xs font-bold text-red-600"
                    >
                      🗑️ Remove
                    </button>
                  </>
                }
              />
            )
          )
        ) : (
          <Empty text="No teachers in this academy." />
        )}
      </div>
    </Panel>
  );
}

function BatchesPanel({
  batches,
  students,
  search,
  setSearch,
  openBatch,
  batchStudents,
  batchLoading,
  onOpen,
  onAdd,
  onEdit,
  onDelete,
}: any) {
  return (
    <Panel
      title="📚 Manage Batches"
      count={batches.length}
      search={search}
      setSearch={setSearch}
      placeholder="Search batch, class or course"
    >
      <div className="space-y-3">
        {batches.length ? (
          batches.map((b: any) => {
            const members =
              batchStudents[b.id] ||
              [];

            const memberIds =
              new Set(
                members.map(
                  (s: any) => s.id
                )
              );

            return (
              <div
                key={b.id}
                className="rounded-2xl border border-[#e3e8f5] p-4"
              >
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <p className="font-black">
                      📚{" "}
                      {b.name || "-"}
                    </p>

                    <p className="mt-1 text-xs text-[#697386]">
                      Class:{" "}
                      {b.class_name ||
                        "-"}{" "}
                      · Course:{" "}
                      {b.course_name ||
                        "Not assigned"}{" "}
                      ·{" "}
                      {b.student_count ||
                        0}{" "}
                      students
                    </p>
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={() =>
                        onOpen(
                          String(b.id)
                        )
                      }
                      className="rounded-lg border px-3 py-2 text-xs font-bold"
                    >
                      {openBatch ===
                      b.id
                        ? "▲ Hide"
                        : "👥 Students"}
                    </button>

                    <button
                      onClick={() =>
                        onEdit(
                          "batch",
                          b
                        )
                      }
                      className="rounded-lg border px-3 py-2 text-xs font-bold"
                    >
                      ✏️ Edit
                    </button>

                    <button
                      onClick={() =>
                        onDelete(
                          String(b.id),
                          String(
                            b.name ||
                              "batch"
                          )
                        )
                      }
                      className="rounded-lg border border-red-200 px-3 py-2 text-xs font-bold text-red-600"
                    >
                      🗑️ Delete
                    </button>
                  </div>
                </div>

                {openBatch ===
                  b.id && (
                  <div className="mt-4 border-t pt-4">
                    {batchLoading ===
                    b.id ? (
                      <p className="text-xs text-[#697386]">
                        Loading students…
                      </p>
                    ) : (
                      <>
                        <p className="mb-2 text-xs font-black">
                          Students in this batch
                        </p>

                        {members.length ? (
                          <div className="mb-4 flex flex-wrap gap-2">
                            {members.map(
                              (
                                s: any
                              ) => (
                                <span
                                  key={
                                    s.id
                                  }
                                  className="rounded-full bg-[#eef2ff] px-3 py-1.5 text-xs font-bold"
                                >
                                  🎓{" "}
                                  {
                                    s.name
                                  }

                                  <button
                                    onClick={() =>
                                      onAdd(
                                        b.id,
                                        s.id,
                                        "remove"
                                      )
                                    }
                                    className="ml-1 text-red-600"
                                  >
                                    ×
                                  </button>
                                </span>
                              )
                            )}
                          </div>
                        ) : (
                          <p className="mb-4 text-xs text-[#929aaa]">
                            No students assigned yet.
                          </p>
                        )}

                        <p className="mb-2 text-xs font-black">
                          Add an academy student
                        </p>

                        <div className="flex flex-wrap gap-2">
                          {students
                            .filter(
                              (s: any) =>
                                !memberIds.has(
                                  s.id
                                )
                            )
                            .slice(
                              0,
                              20
                            )
                            .map(
                              (
                                s: any
                              ) => (
                                <button
                                  key={
                                    s.id
                                  }
                                  onClick={() =>
                                    onAdd(
                                      b.id,
                                      s.id,
                                      "add"
                                    )
                                  }
                                  className="rounded-lg border px-3 py-2 text-xs font-bold hover:border-[#315bea]"
                                >
                                  ➕{" "}
                                  {
                                    s.name
                                  }{" "}
                                  ·{" "}
                                  {s.class_name ||
                                    "-"}
                                </button>
                              )
                            )}

                          {students.filter(
                            (s: any) =>
                              !memberIds.has(
                                s.id
                              )
                          ).length ===
                            0 && (
                            <span className="text-xs text-[#929aaa]">
                              All academy students are already assigned.
                            </span>
                          )}
                        </div>
                      </>
                    )}
                  </div>
                )}
              </div>
            );
          })
        ) : (
          <Empty text="No batches in this academy." />
        )}
      </div>
    </Panel>
  );
}

function TestsPanel({
  papers,
  scheduledTests,
  questions,
}: any) {
  return (
    <div className="space-y-6">
      <Panel
        title="📝 Tests & Papers"
        count={papers.length}
        search=""
        setSearch={() => {}}
        placeholder=""
      >
        <div className="grid gap-3">
          {papers.length ? (
            papers.map((p: any) => {
              const paperQuestions =
                questions.filter(
                  (q: any) =>
                    q.paper_id ===
                    p.id
                );

              return (
                <details
                  key={p.id}
                  className="rounded-2xl border border-[#e3e8f5] bg-[#fcfdff] p-4"
                >
                  <summary className="cursor-pointer list-none">
                    <p className="font-black">
                      📝{" "}
                      {p.code ||
                        "Paper"}{" "}
                      ·{" "}
                      {p.description ||
                        "Untitled"}
                    </p>

                    <p className="mt-1 text-xs font-semibold text-[#315bea]">
                      {p.exam || "-"}{" "}
                      ·{" "}
                      {p.status ||
                        "-"}{" "}
                      ·{" "}
                      {
                        paperQuestions.length
                      }{" "}
                      questions
                    </p>

                    <p className="mt-1 text-xs text-[#697386]">
                      Creator:{" "}
                      {p.creator_name ||
                        p.creator_email ||
                        "-"}{" "}
                      · Created:{" "}
                      {formatDate(
                        p.created_at
                      )}
                    </p>
                  </summary>

                  <div className="mt-4 space-y-3 border-t pt-4">
                    {paperQuestions.length ? (
                      paperQuestions.map(
                        (
                          q: any,
                          i: number
                        ) => (
                          <div
                            key={`${q.id}-${i}`}
                            className="rounded-xl border bg-white p-3"
                          >
                            <p className="text-[11px] font-black text-[#315bea]">
                              Question{" "}
                              {q.question_order ||
                                i + 1}{" "}
                              ·{" "}
                              {q.subject ||
                                "-"}{" "}
                              ·{" "}
                              {q.chapter_name ||
                                "-"}
                            </p>

                            <p className="mt-2 whitespace-pre-wrap text-sm font-semibold">
                              {q.stem ||
                                "Question text unavailable"}
                            </p>

                            <p className="mt-2 text-xs text-[#697386]">
                              Difficulty:{" "}
                              {q.difficulty ||
                                "-"}{" "}
                              · Type:{" "}
                              {q.question_type ||
                                "-"}{" "}
                              · Correct:{" "}
                              {q.correct_option ||
                                "-"}
                            </p>

                            {q.solution ? (
                              <p className="mt-2 whitespace-pre-wrap text-xs text-[#697386]">
                                Solution:{" "}
                                {q.solution}
                              </p>
                            ) : null}
                          </div>
                        )
                      )
                    ) : (
                      <Empty text="No questions linked to this paper." />
                    )}
                  </div>
                </details>
              );
            })
          ) : (
            <Empty text="No papers created for this academy." />
          )}
        </div>
      </Panel>

      <Panel
        title="📅 Scheduled Tests"
        count={
          scheduledTests.length
        }
        search=""
        setSearch={() => {}}
        placeholder=""
      >
        <div className="grid gap-3">
          {scheduledTests.length ? (
            scheduledTests.map(
              (t: any) => (
                <RecordCard
                  key={t.id}
                  icon="📅"
                  title={String(
                    t.title ||
                      "Untitled test"
                  )}
                  meta={String(
                    t.status || "-"
                  )}
                  lines={[
                    `Paper: ${
                      t.paper_code ||
                      "-"
                    }`,
                    `Batch: ${
                      t.batch_name ||
                      "Individual"
                    }`,
                    `Start: ${formatDate(
                      t.start_time
                    )}`,
                    `End: ${formatDate(
                      t.end_time
                    )}`,
                    `Duration: ${
                      t.duration_minutes ||
                      0
                    } minutes`,
                  ]}
                />
              )
            )
          ) : (
            <Empty text="No scheduled tests for this academy." />
          )}
        </div>
      </Panel>
    </div>
  );
}

function SubscriptionPanel({
  academy,
  onManage,
  onExtend,
}: {
  academy: Academy;
  onManage: () => void;
  onExtend: (m: number) => void;
}) {
  const used = Number(
    academy.student_count || 0
  );

  const limit = Number(
    academy.student_limit || 0
  );

  const percent = limit
    ? Math.min(
        100,
        Math.round(
          (used / limit) * 100
        )
      )
    : 0;

  return (
    <div className="space-y-5">
      <div className="grid gap-4 md:grid-cols-3">
        <BigStat
          icon="🎟️"
          label="Plan"
          value={
            academy.subscription_plan ||
            "Custom"
          }
          sub="Current plan"
        />

        <BigStat
          icon="👥"
          label="Seats"
          value={`${used} / ${limit}`}
          sub={`${Math.max(
            limit - used,
            0
          )} remaining`}
        />

        <BigStat
          icon="⏳"
          label="Expiry"
          value={
            academy.subscription_end
              ? toDateInput(
                  academy.subscription_end
                )
              : "-"
          }
          sub={statusLabel(
            academy
          )}
        />
      </div>

      <div className="rounded-2xl border p-5">
        <div className="flex justify-between text-xs font-black">
          <span>
            Seat usage
          </span>

          <span>
            {percent}%
          </span>
        </div>

        <div className="mt-2 h-3 overflow-hidden rounded-full bg-[#edf0f5]">
          <div
            className="h-full rounded-full bg-[#315bea]"
            style={{
              width: `${percent}%`,
            }}
          />
        </div>

        <div className="mt-5 flex flex-wrap gap-2">
          <button
            onClick={onManage}
            className="rounded-xl bg-[#172033] px-4 py-3 text-xs font-black text-white"
          >
            ⚙️ Manage subscription
          </button>

          <button
            onClick={() =>
              onExtend(1)
            }
            className="rounded-xl border px-4 py-3 text-xs font-black"
          >
            ➕ 1 Month
          </button>

          <button
            onClick={() =>
              onExtend(3)
            }
            className="rounded-xl border px-4 py-3 text-xs font-black"
          >
            ➕ 3 Months
          </button>

          <button
            onClick={() =>
              onExtend(12)
            }
            className="rounded-xl border px-4 py-3 text-xs font-black"
          >
            🚀 1 Year
          </button>
        </div>
      </div>
    </div>
  );
}

function Panel({
  title,
  count,
  search,
  setSearch,
  placeholder,
  children,
}: any) {
  return (
    <div>
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <h3 className="text-lg font-black">
          {title}{" "}
          <span className="ml-1 rounded-full bg-[#eef2ff] px-2 py-1 text-xs text-[#315bea]">
            {count}
          </span>
        </h3>

        {placeholder && (
          <input
            value={search}
            onChange={(e) =>
              setSearch(
                e.target.value
              )
            }
            placeholder={
              placeholder
            }
            className="rounded-xl border border-[#dfe4ed] px-4 py-2.5 text-sm outline-none focus:border-[#315bea]"
          />
        )}
      </div>

      {children}
    </div>
  );
}

function RecordCard({
  icon,
  title,
  meta,
  lines,
  actions,
}: any) {
  return (
    <div className="rounded-2xl border border-[#e3e8f5] bg-[#fcfdff] p-4">
      <div className="flex flex-wrap justify-between gap-4">
        <div className="min-w-0">
          <p className="font-black">
            {icon} {title}
          </p>

          <p className="mt-1 text-xs font-semibold text-[#315bea]">
            {meta}
          </p>

          {lines.map(
            (x: string) => (
              <p
                key={x}
                className="mt-1 text-xs text-[#697386]"
              >
                {x}
              </p>
            )
          )}
        </div>

        {actions && (
          <div className="flex shrink-0 items-start gap-2">
            {actions}
          </div>
        )}
      </div>
    </div>
  );
}

function AcademyCard({
  academy,
  selected,
  onManage,
}: {
  academy: Academy;
  selected: boolean;
  onManage: () => void;
}) {
  return (
    <div
      className={`rounded-2xl border bg-white p-5 shadow-sm ${
        selected
          ? "border-[#315bea] ring-2 ring-[#315bea]/10"
          : "border-[#e3e8f5]"
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-lg font-black">
            🏫 {academy.name}
          </p>

          <p className="mt-1 text-xs text-[#697386]">
            Code: {academy.code}
          </p>
        </div>

        <span className="rounded-full bg-[#eef2ff] px-3 py-1 text-[10px] font-black text-[#315bea]">
          {statusLabel(
            academy
          )}
        </span>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-2">
        <Mini
          label="Students"
          value={
            academy.student_count ||
            0
          }
          icon="🎓"
        />

        <Mini
          label="Teachers"
          value={
            academy.teacher_count ||
            0
          }
          icon="👨‍🏫"
        />

        <Mini
          label="Batches"
          value={
            academy.batch_count ||
            0
          }
          icon="📚"
        />
      </div>

      <button
        onClick={onManage}
        className="mt-4 w-full rounded-xl bg-[#172033] px-4 py-3 text-xs font-black text-white"
      >
        ⚡ Manage Academy
      </button>
    </div>
  );
}

function Modal({
  modal,
  value,
  value2,
  value3,
  setValue,
  setValue2,
  setValue3,
  onClose,
  onConfirm,
}: any) {
  const edit = [
    "student",
    "teacher",
    "batch",
  ].includes(modal.type);

  const sub =
    modal.type ===
    "subscription";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#101828]/50 p-4">
      <div className="w-full max-w-lg rounded-3xl bg-white p-6 shadow-2xl">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-black">
            {modal.title ||
              "Confirm"}
          </h3>

          <button
            onClick={onClose}
            className="rounded-full bg-[#f1f3f7] px-3 py-1"
          >
            ×
          </button>
        </div>

        {edit && (
          <div className="mt-5 space-y-3">
            <Field
              label="Name"
              value={value}
              onChange={setValue}
              placeholder="Name"
            />

            {modal.type ===
            "student" ? (
              <>
                <Field
                  label="Email"
                  value={value2}
                  onChange={setValue2}
                  placeholder="Email"
                  type="email"
                />

                <Select
                  label="Class"
                  value={value3}
                  onChange={
                    setValue3
                  }
                  options={
                    CLASS_OPTIONS
                  }
                />
              </>
            ) : modal.type ===
              "teacher" ? (
              <Field
                label="Email"
                value={value2}
                onChange={setValue2}
                placeholder="Email"
                type="email"
              />
            ) : (
              <>
                <Select
                  label="Class"
                  value={value2}
                  onChange={
                    setValue2
                  }
                  options={
                    CLASS_OPTIONS
                  }
                />

                <Select
                  label="Course / Exam"
                  value={value3}
                  onChange={
                    setValue3
                  }
                  options={
                    BATCH_COURSE_OPTIONS
                  }
                />
              </>
            )}
          </div>
        )}

        {sub && (
          <div className="mt-5 space-y-3">
            <Field
              label="Student seats"
              value={value}
              onChange={setValue}
              placeholder="50"
              type="number"
            />

            <label className="text-xs font-bold">
              Subscription end

              <input
                type="date"
                value={value2}
                onChange={(e) =>
                  setValue2(
                    e.target.value
                  )
                }
                className="mt-1 w-full rounded-xl border px-3 py-3"
              />
            </label>
          </div>
        )}

        {modal.type ===
          "delete" && (
          <p className="mt-5 text-sm text-[#697386]">
            This removes the record
            from the academy. This
            action cannot be undone.
          </p>
        )}

        <div className="mt-6 flex justify-end gap-2">
          <button
            onClick={onClose}
            className="rounded-xl border px-4 py-3 text-xs font-black"
          >
            Cancel
          </button>

          <button
            onClick={onConfirm}
            className={`rounded-xl px-4 py-3 text-xs font-black text-white ${
              modal.type ===
              "delete"
                ? "bg-red-600"
                : "bg-[#315bea]"
            }`}
          >
            {modal.type ===
            "delete"
              ? "🗑️ Confirm remove"
              : sub
              ? "💾 Save"
              : "Save changes"}
          </button>
        </div>
      </div>
    </div>
  );
}

function ManagementCard({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: ReactNode;
}) {
  return (
    <div className="rounded-2xl border border-[#e3e8f5] bg-[#fafbfe] p-5">
      <h3 className="font-black">
        {title}
      </h3>

      <p className="mb-4 mt-1 text-xs leading-5 text-[#697386]">
        {description}
      </p>

      {children}
    </div>
  );
}

function Field({
  label,
  value,
  onChange,
  placeholder,
  type = "text",
}: any) {
  return (
    <label className="block text-xs font-bold">
      {label}

      <input
        required
        value={value}
        onChange={(e) =>
          onChange(e.target.value)
        }
        placeholder={
          placeholder
        }
        type={type}
        className="mt-1 w-full rounded-xl border border-[#dfe4ed] bg-white px-3 py-3 text-sm outline-none focus:border-[#315bea]"
      />
    </label>
  );
}

function Select({
  label,
  value,
  onChange,
  options,
}: any) {
  return (
    <label className="block text-xs font-bold">
      {label}

      <select
        required
        value={value}
        onChange={(e) =>
          onChange(e.target.value)
        }
        className="mt-1 w-full rounded-xl border border-[#dfe4ed] bg-white px-3 py-3 text-sm outline-none focus:border-[#315bea]"
      >
        <option value="">
          Select…
        </option>

        {options.map(
          (o: string) => (
            <option
              key={o}
              value={o}
            >
              {o}
            </option>
          )
        )}
      </select>
    </label>
  );
}

function Stat({
  title,
  value,
  icon,
}: any) {
  return (
    <div className="rounded-2xl border border-[#e3e8f5] bg-white p-5 shadow-sm">
      <div className="flex justify-between">
        <p className="text-xs font-bold text-[#929aaa]">
          {title}
        </p>

        <span>{icon}</span>
      </div>

      <p className="mt-2 text-2xl font-black">
        {value}
      </p>
    </div>
  );
}

function BigStat({
  icon,
  label,
  value,
  sub,
}: any) {
  return (
    <div className="rounded-2xl border border-[#e3e8f5] bg-[#fafbfe] p-5">
      <span className="text-xl">
        {icon}
      </span>

      <p className="mt-3 text-[10px] font-black uppercase tracking-wide text-[#929aaa]">
        {label}
      </p>

      <p className="mt-1 break-words text-xl font-black">
        {value}
      </p>

      <p className="mt-1 text-xs text-[#697386]">
        {sub}
      </p>
    </div>
  );
}

function Mini({
  icon,
  label,
  value,
}: any) {
  return (
    <div className="rounded-xl bg-[#f7f9fc] p-3">
      <p className="text-[10px] font-bold text-[#929aaa]">
        {icon} {label}
      </p>

      <p className="mt-1 text-sm font-black">
        {value}
      </p>
    </div>
  );
}

function Empty({
  text,
}: {
  text: string;
}) {
  return (
    <div className="rounded-2xl border border-dashed border-[#dfe4ed] bg-white p-8 text-center text-sm font-bold text-[#929aaa]">
      {text}
    </div>
  );
}

function Toasts({
  toasts,
}: {
  toasts: Toast[];
}) {
  return (
    <div className="fixed right-5 top-5 z-[60] flex w-[min(380px,calc(100vw-40px))] flex-col gap-2">
      {toasts.map((t) => (
        <div
          key={t.id}
          className={`rounded-2xl border bg-white px-4 py-3 text-sm font-bold shadow-xl ${
            t.kind === "error"
              ? "border-red-200 text-red-700"
              : t.kind === "info"
              ? "border-blue-200 text-blue-700"
              : "border-green-200 text-green-700"
          }`}
        >
          {t.text}
        </div>
      ))}
    </div>
  );
}

function formatDate(v: unknown) {
  if (!v) return "-";

  const d = new Date(
    String(v)
  );

  return Number.isNaN(
    d.getTime()
  )
    ? String(v)
    : d.toLocaleString();
}

function toDateInput(v: string) {
  const d = new Date(v);

  return Number.isNaN(
    d.getTime()
  )
    ? v.slice(0, 10)
    : d.toISOString().slice(0, 10);
}

function addMonths(
  dateString: string,
  months: number
) {
  const d = new Date(
    `${dateString}T12:00:00`
  );

  d.setMonth(
    d.getMonth() + months
  );

  return d.toISOString().slice(0, 10);
}

function statusLabel(a: Academy) {
  if (a.status === "SUSPENDED")
    return "Suspended";

  if (a.status === "RESTRICTED")
    return "Restricted";

  if (
    a.subscription_end &&
    new Date(
      a.subscription_end
    ) < new Date()
  ) {
    return "Expired";
  }

  return "Active";
}