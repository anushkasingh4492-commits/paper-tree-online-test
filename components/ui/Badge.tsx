"use client";

import * as React from "react";

export type BadgeVariant =
  | "default"
  | "primary"
  | "success"
  | "warning"
  | "error"
  | "info"
  | "subtle";

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant;
  className?: string;
  children: React.ReactNode;
}

const VARIANT_CLASSES: Record<BadgeVariant, string> = {
  default: "bg-surface-subtle text-text-secondary border border-border-default",
  primary: "bg-brand-primary text-white",
  success: "bg-state-success text-white",
  warning: "bg-state-warning text-white",
  error: "bg-state-error text-white",
  info: "bg-state-info text-white",
  subtle: "bg-brand-subtle-lavender text-brand-primary",
};

export function Badge({
  variant = "default",
  className,
  children,
  ...props
}: BadgeProps) {
  return (
    <span
      className={[
        "inline-flex items-center rounded-[4px] px-2.5 py-0.5 text-[10px] font-medium",
        VARIANT_CLASSES[variant],
        className,
      ].filter(Boolean).join(" ")}
      {...props}
    >
      {children}
    </span>
  );
}