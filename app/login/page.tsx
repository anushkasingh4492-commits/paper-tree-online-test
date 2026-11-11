"use client";

import { FormEvent, Suspense, useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Poppins } from "next/font/google";
import {
  ArrowRight,
  Eye,
  EyeOff,
  Infinity as InfinityIcon,
  LockKeyhole,
  Mail,
  ShieldCheck,
} from "lucide-react";
import { Icon } from "@/components/Icon";

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
});

type Branding = {
  name: string;
  logo_data?: string;
};

type LoginResult = {
  success?: boolean;
  role?: "STUDENT" | "TEACHER" | "ACADEMY_ADMIN" | "ADMIN";
  user?: { id?: string; name?: string };
  error?: string;
};

const GOOGLE_ERRORS: Record<string, string> = {
  google_not_configured: "Google sign-in is not configured for this site yet. Use your email and password or ask your administrator.",
  google_no_account: "No account matches that Google email. Sign in with your registered account or contact your administrator.",
  google_account_ambiguous: "More than one account uses that email. Contact your administrator to resolve it.",
  google_account_inactive: "This account is currently inactive. Contact your academy administrator.",
  google_subscription_expired: "The academy subscription has expired. Contact your academy administrator.",
  google_email_unverified: "Google could not verify this email address. Try another account.",
  google_failed: "Google sign-in could not be completed. Please try again.",
};

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const googleError = searchParams.get("error");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(() =>
    googleError
      ? GOOGLE_ERRORS[googleError] ?? "Sign-in could not be completed. Please try again."
      : ""
  );
  const [recoveryNotice, setRecoveryNotice] = useState("");
  const [infoNotice, setInfoNotice] = useState("");
  const [branding, setBranding] = useState<Branding | null>(null);

  useEffect(() => {
    if (googleError) {
      window.history.replaceState({}, "", window.location.pathname);
    }

    let active = true;
    fetch("/api/academy/branding", { cache: "no-store" })
      .then(async (response) => {
        if (!response.ok) throw new Error("Could not load academy branding.");
        return response.json();
      })
      .then((data: { success?: boolean; academy?: Branding }) => {
        if (active && data.success && data.academy) setBranding(data.academy);
      })
      .catch((cause: unknown) => {
        console.error("BRANDING LOAD ERROR:", cause);
      });

    return () => {
      active = false;
    };
  }, [googleError]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setRecoveryNotice("");
    setLoading(true);

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          email: email.trim(),
          password,
          rememberMe,
        }),
      });
      const result = (await response.json()) as LoginResult;

      if (!response.ok || !result.success) {
        throw new Error(result.error || "Invalid email or password.");
      }

      if (result.role === "STUDENT") {
        if (result.user?.id) localStorage.setItem("studentId", String(result.user.id));
        if (result.user?.name) localStorage.setItem("studentName", result.user.name);
        window.location.replace("/dashboard");
        return;
      }

      const destinations: Record<Exclude<LoginResult["role"], "STUDENT" | undefined>, string> = {
        TEACHER: "/teacher",
        ACADEMY_ADMIN: "/academy-admin",
        ADMIN: "/admin",
      };
      if (!result.role) {
        throw new Error("The server returned an unknown account type.");
      }
      router.replace(destinations[result.role]);
      router.refresh();
    } catch (cause: unknown) {
      console.error("LOGIN ERROR:", cause);
      setError(cause instanceof Error ? cause.message : "Unable to connect to the server. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  const brandName = branding?.name || "Infinity Classes";

  return (
    <main className={`${poppins.className} flex min-h-screen items-center justify-center bg-[#f3f6fc] px-2 py-3 text-[#10234b] sm:px-4 sm:py-5`}>
      <div className="w-full max-w-[1120px] rounded-[23px] border border-[#d6deed] bg-white p-1.5 shadow-[0_8px_30px_rgba(12,35,82,0.12)] sm:p-2">
        <div className="overflow-hidden rounded-[19px] border border-[#1e64c8] bg-[#08439c] p-1.5 sm:p-2">
          <div className="relative">
            <Image
              src="/images/login/login-reference-hero.webp"
              alt={`${brandName}: online tests, performance insights, and achievement features`}
              width={937}
              height={410}
              priority
              className="hidden h-auto w-full md:block"
              sizes="(max-width: 1120px) 100vw, 1100px"
            />
            <section className="flex min-h-[150px] items-center justify-between gap-3 rounded-xl bg-gradient-to-br from-[#0757c4] via-[#0646a4] to-[#092d78] px-4 py-4 text-white md:hidden">
              <div className="min-w-0">
                <div className="mb-3 flex items-center gap-2">
                  <span className="grid h-8 w-8 place-items-center rounded-lg bg-white text-[#0757c4]">
                    <InfinityIcon size={22} strokeWidth={2.6} />
                  </span>
                  <span className="truncate text-[12px] font-bold">{brandName}</span>
                </div>
                <h1 className="text-[26px] font-extrabold leading-[1.03] tracking-tight">
                  Think. Test.
                  <span className="block text-[#ffd138]">Excel.</span>
                </h1>
                <p className="mt-2 max-w-[220px] text-[9px] leading-relaxed text-blue-100">
                  One platform. Every assessment.
                </p>
              </div>
              <Image
                src="/images/login/Stacked Books with Floating Question Tiles.png"
                alt=""
                width={160}
                height={120}
                className="h-auto w-[38%] max-w-[145px] object-contain"
                sizes="145px"
              />
            </section>
          </div>

          <form
            onSubmit={handleSubmit}
            className="relative z-10 mx-auto -mt-px grid w-[96%] gap-5 rounded-[18px] border border-[#dce5f4] bg-[#f5f8ff] px-4 py-5 shadow-[0_8px_22px_rgba(0,20,70,0.15)] sm:px-6 sm:py-6 md:grid-cols-2 md:gap-6 md:px-8 lg:w-[92%] lg:px-12"
          >
            <div className="min-w-0">
              <h2 className="text-[27px] font-extrabold leading-tight tracking-[-0.04em] text-[#102c67] sm:text-[30px]">
                Welcome back
              </h2>
              <p className="mb-4 text-[11px] text-[#60749a] sm:text-xs">
                Sign in to continue your assessment journey.
              </p>

              {error && (
                <div role="alert" className="mb-3 flex items-start gap-2 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-[10px] font-medium leading-relaxed text-red-700 sm:text-xs">
                  <Icon name="alert" size={15} className="mt-0.5 shrink-0 text-red-600" />
                  <span>{error}</span>
                </div>
              )}

              <label htmlFor="email" className="sr-only">Email address</label>
              <span className="mb-2 flex h-10 items-center gap-3 rounded-lg border border-[#cbd9ef] bg-[#e8effb] px-3 text-[#657da8] transition focus-within:border-[#3478e8] focus-within:ring-2 focus-within:ring-[#3478e8]/20">
                <Mail size={17} aria-hidden="true" />
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  placeholder="Enter your email address"
                  autoComplete="email"
                  required
                  disabled={loading}
                  className="h-full min-w-0 flex-1 bg-transparent text-[11px] text-[#142b58] outline-none placeholder:text-[#6f82a5] disabled:opacity-60"
                />
              </span>

              <label htmlFor="password" className="sr-only">Password</label>
              <span className="flex h-10 items-center gap-3 rounded-lg border border-[#cbd9ef] bg-[#e8effb] px-3 text-[#657da8] transition focus-within:border-[#3478e8] focus-within:ring-2 focus-within:ring-[#3478e8]/20">
                <LockKeyhole size={16} aria-hidden="true" />
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  required
                  disabled={loading}
                  className="h-full min-w-0 flex-1 bg-transparent text-[11px] text-[#142b58] outline-none placeholder:text-[#6f82a5] disabled:opacity-60"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((visible) => !visible)}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  aria-pressed={showPassword}
                  className="rounded p-1 text-[#657da8] hover:text-[#174fc3] focus-visible:outline-2 focus-visible:outline-[#3478e8]"
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </span>

              <div className="mt-2 flex flex-wrap items-center justify-between gap-x-3 gap-y-2 text-[10px]">
                <label className="flex cursor-pointer items-center gap-2 font-medium text-[#233a65]">
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(event) => setRememberMe(event.target.checked)}
                    disabled={loading}
                    className="h-4 w-4 rounded border-[#9fb3d3] accent-[#0b55db]"
                  />
                  Remember me
                </label>
                <button
                  type="button"
                  onClick={() => {
                    setRecoveryNotice("Forgotten passwords are reset by your academy administrator. Please contact them to restore access.");
                    setError("");
                  }}
                  className="font-semibold text-[#1454d1] hover:underline"
                >
                  Forgot password?
                </button>
              </div>
              {recoveryNotice && (
                <p role="status" className="mt-2 rounded-md bg-blue-50 px-2.5 py-2 text-[10px] leading-relaxed text-blue-800">
                  {recoveryNotice}
                </p>
              )}
            </div>

            <div className="flex min-w-0 flex-col justify-center gap-2.5 border-t border-[#d4deed] pt-4 md:border-l md:border-t-0 md:pl-6 md:pt-0 lg:pl-10">
              <button
                type="submit"
                disabled={loading}
                className="flex h-10 w-full items-center justify-center gap-2 rounded-full bg-[#0758e8] px-4 text-xs font-bold text-white shadow-[0_4px_12px_rgba(0,72,210,0.22)] transition hover:bg-[#064bc5] active:scale-[0.99] disabled:cursor-not-allowed disabled:opacity-60 sm:h-11 sm:text-sm"
              >
                {loading ? (
                  <>
                    <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" />
                    Signing in…
                  </>
                ) : (
                  <>Sign in to CBT <ArrowRight size={17} /></>
                )}
              </button>

              <a
                href="/api/auth/google/start"
                className="flex h-10 w-full items-center justify-center gap-2 rounded-full border border-[#c6d3e6] bg-white px-4 text-xs font-semibold text-[#1d3158] transition hover:bg-[#f4f7fc] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#3478e8] sm:h-11 sm:text-sm"
              >
                <svg aria-hidden="true" viewBox="0 0 24 24" className="h-[17px] w-[17px]">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.27-4.74 3.27-8.1Z" />
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.65l-3.57-2.77c-.99.66-2.25 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.15v2.84A11 11 0 0 0 12 23Z" />
                  <path fill="#FBBC05" d="M5.84 14.11a6.6 6.6 0 0 1 0-4.22V7.05H2.15a11 11 0 0 0 0 9.9l3.69-2.84Z" />
                  <path fill="#EA4335" d="M12 5.36c1.62 0 3.06.56 4.2 1.64l3.15-3.15C17.45 2.03 14.97 1 12 1a11 11 0 0 0-9.85 6.05l3.69 2.84C6.71 7.29 9.14 5.36 12 5.36Z" />
                </svg>
                Sign in with Google
              </a>

              <div className="mt-1 flex items-center justify-center gap-2 text-center text-[8px] leading-relaxed text-[#6b7c9b] sm:text-[9px]">
                <ShieldCheck size={16} className="shrink-0 text-[#5b77a4]" />
                A secure and trusted platform for students, teachers and administrators.
              </div>
              <div className="flex items-center justify-center gap-3 pt-1 text-[9px] font-semibold text-[#1454d1] sm:text-[10px]">
                <button type="button" onClick={() => setInfoNotice("Please contact your institute for its applicable privacy policy.")} className="hover:underline">
                  Privacy Policy
                </button>
                <span className="h-4 w-px bg-[#c4d1e4]" />
                <button type="button" onClick={() => setInfoNotice("Please contact your institute for its applicable terms of service.")} className="hover:underline">
                  Terms of Service
                </button>
              </div>
              {infoNotice && (
                <p role="status" className="text-center text-[9px] leading-relaxed text-[#536887]">
                  {infoNotice}
                </p>
              )}
            </div>
          </form>

          <div className="flex flex-wrap items-center justify-center gap-3 px-2 pb-2 pt-3 text-[9px] font-medium text-blue-100">
            <span>© {new Date().getFullYear()} {brandName}</span>
            <span aria-hidden="true">·</span>
            <Link href="/master-login" className="underline decoration-white/40 underline-offset-2 hover:text-white">
              Teacher / Admin login
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}

export default function Home() {
  return (
    <Suspense fallback={<main className="min-h-screen bg-[#f3f6fc]" />}>
      <LoginForm />
    </Suspense>
  );
}
