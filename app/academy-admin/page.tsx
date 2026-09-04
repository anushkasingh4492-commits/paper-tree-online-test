"use client";

import { useRouter } from "next/navigation";

export default function AcademyAdminPage() {
  const router = useRouter();

  function logout() {
    document.cookie =
      "master_session=; Max-Age=0; path=/";

    router.replace("/");
  }
const cards = [
  {
    title: "Teachers",
    description: "Manage teachers belonging to your academy.",
    icon: "",
    route: "/academy-admin/teachers",
  },
  {
    title: "Students",
    description: "Manage your academy students.",
    icon: "",
    route: "/academy-admin/students",
  },
  {
    title: "Batches",
    description: "Create and manage classes and batches.",
    icon: "",
    route: "/academy-admin/batches",
  },
  {
    title: "Scheduled Tests",
    description: "View tests assigned to your academy.",
    icon: "",
    route: "/academy-admin/tests",
  },
];

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <header className="border-b border-[#e7eaf0] bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-xl font-extrabold">
              Academy Administration
            </h1>

            <p className="mt-1 text-xs font-bold tracking-wider text-[#315bea]">
              ACADEMY ADMIN
            </p>
          </div>

          <button
            onClick={logout}
            className="rounded-xl border border-[#e2e6ee] bg-white px-4 py-2.5 text-sm font-bold text-[#697386]"
          >
            Logout
          </button>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-10">
        <div className="mb-10">
          <p className="text-xs font-bold uppercase tracking-[0.15em] text-[#315bea]">
            Academy Management
          </p>

          <h2 className="mt-2 text-3xl font-extrabold">
            Academy Control Center
          </h2>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-[#697386]">
            Manage your academy teachers, students, batches and
            scheduled tests.
          </p>
        </div>

        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
          {cards.map((card) => (
            <div
              key={card.title}
              className="rounded-2xl border border-[#e3e8f5] bg-white p-6 shadow-sm"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#f2f5ff] text-2xl">
                {card.icon}
              </div>

              <h3 className="mt-5 text-lg font-extrabold">
                {card.title}
              </h3>

              <p className="mt-2 text-sm leading-6 text-[#697386]">
                {card.description}
              </p>

            <button
  className="mt-5 text-sm font-bold text-[#315bea]"
  onClick={() => router.push(card.route)}
>
  Manage →
</button>

            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
