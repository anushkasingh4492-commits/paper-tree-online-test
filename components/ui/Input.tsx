"use client";

import * as React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: React.ReactNode;
  error?: string;
  helperText?: React.ReactNode;
  className?: string;
}

export function Input({
  label,
  error,
  helperText,
  className,
  ...props
}: InputProps) {
  const inputClasses = [
    "h-12 w-full rounded-xl border px-4 text-sm outline-none transition-all duration-200",
    "bg-surface-surface text-text-primary placeholder:text-text-supporting-label",
    "border-border-default focus:border-brand-primary focus:ring-4 focus:ring-brand-primary/10",
    error ? "border-state-error focus:border-state-error focus:ring-state-error/10" : "",
    "disabled:bg-surface-app-bg disabled:text-text-disabled disabled:cursor-not-allowed",
    className,
  ].filter(Boolean).join(" ");

  return (
    <div className="w-full space-y-1">
      {label && (
        <label className="mb-1 block text-[10px] font-bold uppercase tracking-[0.15em] text-text-tertiary">
          {label}
        </label>
      )}
      <input className={inputClasses} {...props} />
      {error && (
        <p className="mt-1 text-[10px] font-medium text-state-error">{error}</p>
      )}
      {helperText && !error && (
        <p className="mt-1 text-[10px] text-text-body">{helperText}</p>
      )}
    </div>
  );
}