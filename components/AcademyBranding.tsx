"use client";

import { useEffect, useState } from "react";

type AcademyBrand = {
  name?: string | null;
  logo_data?: string | null;
  subtitle?: string | null;
};

type Props = {
  variant?: "header" | "login" | "compact";
  className?: string;
};

export default function AcademyBranding({
  variant = "header",
  className = "",
}: Props) {
  const [academy, setAcademy] =
    useState<AcademyBrand | null>(null);

  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    let active = true;

    fetch("/api/academy/branding", {
      cache: "no-store",
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        if (!active) return;

        if (data?.success && data?.academy) {
          setAcademy(data.academy);
        }

        setLoaded(true);
      })
      .catch(() => {
        if (active) {
          setLoaded(true);
        }
      });

    return () => {
      active = false;
    };
  }, []);

  // Prevent Paper Tree from flashing before academy data loads
  if (!loaded) {
    return (
      <div
        className={`flex items-center gap-3 ${className}`}
      >
        <div className="h-10 w-10 animate-pulse rounded-xl bg-slate-200" />

        <div className="h-4 w-32 animate-pulse rounded bg-slate-200" />
      </div>
    );
  }

  const name =
    academy?.name?.trim() || "Paper Tree";

  const logo =
    academy?.logo_data || null;

  const subtitle =
    academy?.subtitle?.trim() ||
    "COMPUTER BASED TESTING";

  if (variant === "compact") {
    return (
      <div
        className={`flex items-center gap-3 min-w-0 ${className}`}
      >
        {logo ? (
          <img
            src={logo}
            alt={`${name} logo`}
            className="h-10 w-10 shrink-0 rounded-xl object-contain bg-white"
          />
        ) : (
          <div className="h-10 w-10 shrink-0 rounded-xl bg-blue-600 text-white flex items-center justify-center font-black text-lg">
            {name.charAt(0).toUpperCase()}
          </div>
        )}

        <div className="min-w-0">
          <div className="font-extrabold text-sm truncate">
            {name}
          </div>

          <div className="text-[9px] font-bold tracking-[0.16em] text-slate-400 truncate">
            {subtitle}
          </div>
        </div>
      </div>
    );
  }

  if (variant === "login") {
    return (
      <div
        className={`flex items-center gap-3 ${className}`}
      >
        {logo ? (
          <img
            src={logo}
            alt={`${name} logo`}
            className="h-11 w-11 rounded-[13px] object-contain bg-white"
          />
        ) : (
          <div className="h-11 w-11 rounded-[13px] bg-white text-[#315bea] flex items-center justify-center text-lg font-extrabold">
            {name.charAt(0).toUpperCase()}
          </div>
        )}

        <div className="min-w-0">
          <p className="text-[17px] font-extrabold truncate">
            {name}
          </p>

          <p className="text-[9px] font-bold tracking-[0.18em] text-blue-100">
            {subtitle}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`flex items-center gap-3 min-w-0 ${className}`}
    >
      {logo ? (
        <img
          src={logo}
          alt={`${name} logo`}
          className="h-10 w-10 shrink-0 rounded-xl object-contain bg-white"
        />
      ) : (
        <div className="h-10 w-10 shrink-0 rounded-xl bg-blue-600 text-white flex items-center justify-center font-black text-lg">
          {name.charAt(0).toUpperCase()}
        </div>
      )}

      <div className="min-w-0">
        <div className="font-extrabold text-[15px] leading-4 truncate">
          {name}
        </div>

        <div className="text-[9px] font-semibold tracking-[.17em] text-slate-400 mt-1 truncate">
          {subtitle}
        </div>
      </div>
    </div>
  );
}