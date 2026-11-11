"use client";

import * as React from "react";

export type CardVariant = "default" | "elevated" | "subtle" | "bordered";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: CardVariant;
  padding?: "none" | "sm" | "md" | "lg";
  radius?: "micro" | "standard" | "card" | "large" | "hero";
  children: React.ReactNode;
  className?: string;
}

const PADDING_CLASSES: Record<string, string> = {
  none: "p-0",
  sm: "p-4",
  md: "p-6",
  lg: "p-8",
};

const RADIUS_CLASSES: Record<string, string> = {
  micro: "rounded-[4px]",
  standard: "rounded-[8px]",
  card: "rounded-[12px]",
  large: "rounded-[16px]",
  hero: "rounded-[24px]",
};

export function Card({
  variant = "default",
  padding = "sm",
  radius = "card",
  children,
  className,
  ...props
}: CardProps) {
  const base =
    "relative overflow-hidden transition-all duration-200 border border-border-default";

  const variantClasses = {
    default: "bg-surface-surface shadow-sm",
    elevated: "bg-surface-elevated shadow-md",
    subtle: "bg-surface-subtle border border-border-muted",
    bordered: "bg-surface-surface border-2 border-border-default",
  };

  return (
    <div
      className={[base, variantClasses[variant], PADDING_CLASSES[padding], RADIUS_CLASSES[radius], className].filter(Boolean).join(" ")}
      {...props}
    >
      {children}
    </div>
  );
}

export interface CardGridProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
  cols?: "1" | "2" | "3" | "4" | "auto";
}

/** A grid of cards with exactly 16px gap between all cards. */
export function CardGrid({
  children,
  className,
  cols = "auto",
  ...props
}: CardGridProps) {
  const colClasses: Record<string, string> = {
    "1": "grid-cols-1",
    "2": "grid-cols-2",
    "3": "grid-cols-3",
    "4": "grid-cols-4",
    auto: "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4",
  };

  return (
    <div
      className={[
        "grid gap-4",
        colClasses[cols],
        "w-full",
        className,
      ].filter(Boolean).join(" ")}
      {...props}
    >
      {children}
    </div>
  );
}
