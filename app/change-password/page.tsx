"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

export default function ChangePasswordPage() {
  const router = useRouter();

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();

    setError("");
    setMessage("");

    if (newPassword.length < 8) {
      setError("New password must be at least 8 characters long.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setError("New passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        "/api/account/change-password",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify({
            currentPassword,
            newPassword,
            confirmPassword,
          }),
        }
      );

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(
          result.error || "Failed to change password."
        );
      }

      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
      setMessage("Password changed successfully.");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to change password."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#f6f8fc] flex items-center justify-center px-6">
      <div className="w-full max-w-md">
        <div className="mb-7 text-center">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-[#315bea] text-2xl font-extrabold text-white">
            P
          </div>

          <h1 className="mt-4 text-2xl font-extrabold text-[#172033]">
            Change Password
          </h1>

          <p className="mt-2 text-sm text-[#697386]">
            Update your Paper Tree account password.
          </p>
        </div>

        <form
          onSubmit={submit}
          className="rounded-3xl border border-[#e5e8ee] bg-white p-7 shadow-sm"
        >
          {error && (
            <div className="mb-5 rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
              {error}
            </div>
          )}

          {message && (
            <div className="mb-5 rounded-xl border border-emerald-100 bg-emerald-50 px-4 py-3 text-sm font-medium text-emerald-600">
              {message}
            </div>
          )}

          <label className="mb-2 block text-sm font-semibold text-[#263044]">
            Current password
          </label>

          <input
            type="password"
            value={currentPassword}
            onChange={(e) =>
              setCurrentPassword(e.target.value)
            }
            autoComplete="current-password"
            required
            className="mb-5 h-12 w-full rounded-xl border border-[#dfe3eb] px-4 text-sm outline-none focus:border-[#315bea] focus:ring-4 focus:ring-[#315bea]/10"
          />

          <label className="mb-2 block text-sm font-semibold text-[#263044]">
            New password
          </label>

          <input
            type="password"
            value={newPassword}
            onChange={(e) =>
              setNewPassword(e.target.value)
            }
            autoComplete="new-password"
            required
            minLength={8}
            className="h-12 w-full rounded-xl border border-[#dfe3eb] px-4 text-sm outline-none focus:border-[#315bea] focus:ring-4 focus:ring-[#315bea]/10"
          />

          <p className="mt-2 text-xs text-[#8a93a5]">
            Minimum 8 characters.
          </p>

          <label className="mb-2 mt-5 block text-sm font-semibold text-[#263044]">
            Confirm new password
          </label>

          <input
            type="password"
            value={confirmPassword}
            onChange={(e) =>
              setConfirmPassword(e.target.value)
            }
            autoComplete="new-password"
            required
            minLength={8}
            className="h-12 w-full rounded-xl border border-[#dfe3eb] px-4 text-sm outline-none focus:border-[#315bea] focus:ring-4 focus:ring-[#315bea]/10"
          />

          <button
            type="submit"
            disabled={loading}
            className="mt-7 w-full rounded-xl bg-[#315bea] px-4 py-3 font-bold text-white transition hover:bg-[#264ac7] disabled:opacity-60"
          >
            {loading
              ? "Changing password..."
              : "Change Password"}
          </button>

          <button
            type="button"
            onClick={() => router.back()}
            className="mt-4 w-full text-sm font-semibold text-[#697386] hover:text-[#315bea]"
          >
            ← Back
          </button>
        </form>
      </div>
    </main>
  );
}