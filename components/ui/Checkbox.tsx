"use client";

import * as React from "react";

interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "onChange"> {
  checked?: boolean;
  onChange?: (checked: boolean) => void;
  label?: React.ReactNode;
  disabled?: boolean;
  className?: string;
}

export function Checkbox({
  checked = false,
  onChange,
  label,
  disabled = false,
  className,
  ...props
}: CheckboxProps) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (disabled) return;
    onChange?.(e.target.checked);
  };

  const checkboxClasses = [
    "relative inline-flex items-center justify-center h-5 w-5 shrink-0 rounded-[4px] border transition-all duration-200",
    checked
      ? "bg-selection-checkbox-selected-fill border-selection-checkbox-selected-fill"
      : "bg-selection-checkbox-unselected-fill border-selection-checkbox-unselected-border",
    disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer",
  ].join(" ");

  const checkmarkClasses = [
    "w-3 h-3",
    checked
      ? "text-white"
      : "text-transparent",
  ].join(" ");

  return (
    <div className={`flex items-center gap-2.5 ${className ?? ""}`}>
      <input
        type="checkbox"
        checked={checked}
        onChange={handleChange}
        disabled={disabled}
        className="peer sr-only"
        {...props}
      />
      <div className={checkboxClasses}>
        <svg
          className={checkmarkClasses}
          fill="none"
          stroke="currentColor"
          strokeWidth="3"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path d="M20 6L9 17l-5-5" />
        </svg>
      </div>
      {label && (
        <label
          className="text-text-secondary text-sm font-medium select-none cursor-pointer"
          onClick={(e) => {
            if (disabled) return;
            onChange?.(!checked);
          }}
        >
          {label}
        </label>
      )}
    </div>
  );
}