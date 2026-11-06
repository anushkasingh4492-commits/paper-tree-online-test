"use client";

import * as React from "react";

export type ButtonVariant = "primary" | "secondary";
export type ButtonSize = "sm" | "md" | "lg";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  isDisabled?: boolean;
  isLoading?: boolean;
  children: React.ReactNode;
}

const SIZE_CLASSES: Record<ButtonSize, string> = {
  sm: "h-9 px-3 text-xs",
  md: "h-12 px-4 text-sm",
  lg: "h-14 px-6 text-base",
};

export function Button({
  variant = "primary",
  size = "md",
  isDisabled = false,
  isLoading = false,
  children,
  className,
  ...props
}: ButtonProps) {
  const base = "flex items-center justify-center gap-2 rounded-xl font-bold outline-none transition-all duration-200 disabled:pointer-events-none disabled:opacity-50 disabled:cursor-not-allowed";

  const variantClasses = {
    primary: {
      default: "bg-brand-primary text-white shadow-[0_8px_20px_rgba(36,85,200,0.18)]",
      hover: "hover:bg-brand-action-blue",
      pressed: "active:bg-brand-deep-navy",
      disabled: "bg-cta-disabled text-text-disabled shadow-none",
    },
    secondary: {
      default: "bg-brand-subtle-lavender text-brand-primary border border-border-default",
      hover: "hover:bg-brand-action-blue hover:text-white",
      pressed: "active:bg-brand-deep-navy active:text-white",
      disabled: "bg-cta-disabled text-text-disabled border-border-default",
    },
  };

  const v = variantClasses[variant];
  const disabled = isDisabled || isLoading;

  return (
    <button
      disabled={disabled}
      className={[
        base,
        v.default,
        disabled ? v.disabled : `${v.hover} ${v.pressed}`,
        SIZE_CLASSES[size],
        className,
      ].filter(Boolean).join("")}
      {...props}
    >
      {isLoading && (
        <span className="flex items-center gap-1">
          <svg
            className="animate-spin h-4 w-4 text-current"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
        </span>
      )}
      {children}
    </button>
  );
}