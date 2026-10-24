"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function EditProfilePage() {
  const router = useRouter();
  const [profile, setProfile] = useState({
    name: "",
    email: "",
    rollNumber: "",
    className: "",
    academy: "",
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch("/api/student/profile", { cache: "no-store" });
        const data = await res.json();
        if (data.success && data.profile) {
          setProfile(data.profile);
        }
      } catch {
        // silent
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <main className="min-h-screen bg-[#f6f8fc] text-[#172033]">
      <div className="mx-auto max-w-2xl px-6 py-10">
        <div className="mb-8">
          <button
            onClick={() => router.push("/dashboard")}
            className="text-sm font-semibold text-[#315bea] mb-2 inline-block transition hover:underline"
          >
            ← Back to Dashboard
          </button>
          <h1 className="text-2xl font-extrabold tracking-tight">
            Edit Profile
          </h1>
          <p className="text-sm text-[#697386]">
            Update your personal information.
          </p>
        </div>

        {loading ? (
          <div className="h-64 flex items-center justify-center">
            <div className="w-8 h-8 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin" />
          </div>
        ) : (
          <form
            onSubmit={(e) => {
              e.preventDefault();
              setSaving(true);
              setTimeout(() => {
                setSaving(false);
                router.push("/profile");
              }, 800);
            }}
            className="space-y-5"
          >
            <div className="rounded-xl border border-[#e5e8ef] bg-white p-5 shadow-sm">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-14 h-14 rounded-full bg-[#f0f5ff] flex items-center justify-center text-2xl overflow-hidden border border-[#dbe6f3]">
                  {profile.name?.charAt(0)?.toUpperCase() || "U"}
                </div>
                <div>
                  <p className="font-bold text-sm text-[#172033]">
                    {profile.name || "Student"}
                  </p>
                  <p className="text-[10px] text-[#8a93a5]">
                    {profile.rollNumber || "Roll number not set"}
                  </p>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-[10px] font-bold uppercase tracking-[0.15em] text-[#697386] mb-1">
                    Full Name
                  </label>
                  <input
                    type="text"
                    defaultValue={profile.name}
                    className="w-full rounded-xl border border-[#dfe4ee] bg-[#fafbfc] px-4 py-2.5 text-sm focus:border-[#315bea] focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-[10px] font-bold uppercase tracking-[0.15em] text-[#697386] mb-1">
                    Email Address
                  </label>
                  <input
                    type="email"
                    defaultValue={profile.email}
                    className="w-full rounded-xl border border-[#dfe4ee] bg-[#fafbfc] px-4 py-2.5 text-sm focus:border-[#315bea] focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-[10px] font-bold uppercase tracking-[0.15em] text-[#697386] mb-1">
                    Roll Number
                  </label>
                  <input
                    type="text"
                    defaultValue={profile.rollNumber}
                    className="w-full rounded-xl border border-[#dfe4ee] bg-[#fafbfc] px-4 py-2.5 text-sm focus:border-[#315bea] focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-[10px] font-bold uppercase tracking-[0.15em] text-[#697386] mb-1">
                    Class / Batch
                  </label>
                  <input
                    type="text"
                    defaultValue={profile.className}
                    className="w-full rounded-xl border border-[#dfe4ee] bg-[#fafbfc] px-4 py-2.5 text-sm focus:border-[#315bea] focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-[10px] font-bold uppercase tracking-[0.15em] text-[#697386] mb-1">
                    Academy / Institute
                  </label>
                  <input
                    type="text"
                    defaultValue={profile.academy}
                    className="w-full rounded-xl border border-[#dfe4ee] bg-[#fafbfc] px-4 py-2.5 text-sm focus:border-[#315bea] focus:outline-none"
                  />
                </div>
              </div>
            </div>

            <button
              type="submit"
              disabled={saving}
              className="w-full rounded-xl bg-[#315bea] px-5 py-3 font-bold text-white hover:bg-[#264ac7] disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              {saving ? "Saving…" : "Save Changes"}
            </button>

            <button
              type="button"
              onClick={() => router.push("/profile")}
              className="w-full rounded-xl border border-[#e5e8ef] bg-white px-5 py-3 font-bold text-[#172033] hover:bg-[#f8f9fb] transition"
            >
              Cancel
            </button>
          </form>
        )}
      </div>
    </main>
  );
}
