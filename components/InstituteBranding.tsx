"use client";

import { useEffect, useState } from "react";

type Branding = {
  academyName: string;
  logoUrl: string | null;
  tagline: string;
  copyright: string;
};

export default function InstituteBranding() {
  const [branding, setBranding] = useState<Branding | null>(null);

  useEffect(() => {
    async function loadBranding() {
      try {
        const response = await fetch("/api/branding", {
          cache: "no-store",
        });

        const data = await response.json();

        if (data.success && data.branding) {
          setBranding(data.branding);
        }
      } catch (error) {
        console.error("Could not load institute branding:", error);
      }
    }

    loadBranding();
  }, []);

  if (!branding) {
    return null;
  }

  return (
    <>
      <header className="w-full border-b bg-white">
        <div className="mx-auto flex max-w-7xl items-center gap-4 px-6 py-4">
          {branding.logoUrl ? (
            <img
              src={branding.logoUrl}
              alt={`${branding.academyName} logo`}
              className="h-14 w-14 object-contain"
            />
          ) : (
            <div className="flex h-14 w-14 items-center justify-center rounded-lg bg-gray-100 text-xs font-semibold text-gray-500">
              LOGO
            </div>
          )}

          <div>
            <h1 className="text-xl font-bold text-gray-900">
              {branding.academyName}
            </h1>

            <p className="text-sm text-gray-500">
              {branding.tagline}
            </p>
          </div>
        </div>
      </header>
    </>
  );
}