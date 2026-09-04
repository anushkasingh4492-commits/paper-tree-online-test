"use client";

import { useRouter } from "next/navigation";

export default function AdminPage() {
  const router = useRouter();

  const cards = [
    {
      title: "Student Portal",
      description:
        "Open the student side to view the personalised dashboard, tests, results and scheduled tests.",
      icon: "",
      action: "Open Student Portal",
      route: "/dashboard",
    },
    {
      title: "Teacher Portal",
      description:
        "Create papers, cherry-pick questions, publish tests and manage teacher-created papers.",
      icon: "",
      action: "Open Teacher Portal",
      route: "/teacher",
    },
    {
      title: "Upload Dataset",
      description:
        "Upload new JSON question-bank datasets and add questions to the Paper Tree database.",
      icon: "⬆️",
      action: "Upload Dataset",
      route: "/admin/upload-dataset",
    },
    {
      title: "Question Bank",
      description:
        "Browse questions across MHT-CET and NEET by subject, chapter and difficulty.",
      icon: "",
      action: "View Question Bank",
      route: "/teacher/cherry-pick",
    },
    {
      title: "Create Paper",
      description:
        "Generate a paper automatically from the existing question bank.",
      icon: "",
      action: "Generate Paper",
      route: "/teacher/generate",
    },
    {
      title: "Test Summary",
      description:
        "View test activity, completed tests, upcoming tests and student performance.",
      icon: "",
      action: "View Test Summary",
      route: "/test-summary",
    },
    {
  title: "Academies",
  description:
    "Create and manage academy tenants and their administrator accounts.",
  icon: "",
  action: "Manage Academies",
  route: "/admin/academies",
},
  ];

  function logout() {
    document.cookie =
      "master_session=; Max-Age=0; path=/";

    router.replace("/master-login");
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      {/* HEADER */}

      <header className="border-b border-[#e7eaf0] bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#315bea] text-lg font-black text-white">
              P
            </div>

            <div>
              <h1 className="text-lg font-extrabold">
                Paper Tree
              </h1>

              <p className="text-[10px] font-bold tracking-[0.15em] text-[#929aaa]">
                MASTER ADMIN
              </p>
            </div>
          </div>

          <button
            onClick={logout}
            className="rounded-xl border border-[#e2e6ee] bg-white px-4 py-2.5 text-sm font-bold text-[#697386] transition hover:bg-[#f7f8fb]"
          >
            Logout
          </button>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-10">
        {/* INTRO */}

        <div className="mb-10">
          <p className="text-xs font-bold uppercase tracking-[0.15em] text-[#315bea]">
            Master Administration
          </p>

          <h2 className="mt-2 text-3xl font-extrabold tracking-tight">
            Admin Control Center
          </h2>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-[#697386]">
            Access the student portal, teacher tools,
            question bank and administrative dataset
            controls from one place.
          </p>
        </div>

        {/* QUICK STATS / ROLE ACCESS */}

        <section className="mb-8 grid gap-4 sm:grid-cols-3">
          <div className="rounded-2xl border border-[#e5e8ef] bg-white p-5">
            <p className="text-xs font-semibold text-[#929aaa]">
              Student System
            </p>

            <p className="mt-2 text-lg font-extrabold">
              Student Portal
            </p>

            <p className="mt-1 text-xs text-[#697386]">
              Dashboard · Tests · Results
            </p>
          </div>

          <div className="rounded-2xl border border-[#e5e8ef] bg-white p-5">
            <p className="text-xs font-semibold text-[#929aaa]">
              Teacher System
            </p>

            <p className="mt-2 text-lg font-extrabold">
              Teacher Portal
            </p>

            <p className="mt-1 text-xs text-[#697386]">
              Generate · Cherry Pick · Publish
            </p>
          </div>

          <div className="rounded-2xl border border-[#dfe5ff] bg-[#f7f9ff] p-5">
            <p className="text-xs font-semibold text-[#315bea]">
              Current Access
            </p>

            <p className="mt-2 text-lg font-extrabold text-[#315bea]">
              Master Admin
            </p>

            <p className="mt-1 text-xs text-[#697386]">
              Full application access
            </p>
          </div>
        </section>

        {/* ADMIN TOOLS */}

        <section>
          <div className="mb-4">
            <h3 className="text-lg font-extrabold">
              Application Access
            </h3>

            <p className="mt-1 text-xs text-[#8a93a5]">
              Choose what you want to manage.
            </p>
          </div>

          <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
            {cards.map((card) => (
              <button
                key={card.title}
                type="button"
                onClick={() =>
                  router.push(card.route)
                }
                className="group rounded-2xl border border-[#e3e8f5] bg-white p-6 text-left shadow-sm transition hover:-translate-y-1 hover:border-[#cfd8f8] hover:shadow-md"
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#f2f5ff] text-2xl">
                  {card.icon}
                </div>

                <h4 className="mt-5 text-lg font-extrabold">
                  {card.title}
                </h4>

                <p className="mt-2 min-h-[60px] text-sm leading-6 text-[#697386]">
                  {card.description}
                </p>

                <div className="mt-5 text-sm font-bold text-[#315bea]">
                  {card.action}
                  <span className="ml-2 transition group-hover:ml-3">
                    →
                  </span>
                </div>
              </button>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}