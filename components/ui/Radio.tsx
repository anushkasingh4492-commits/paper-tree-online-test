"use client";

import * as React from "react";

interface RadioProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "onChange"> {
  checked?: boolean;
  onChange?: (value: string | null) => void;
  value: string;
  label?: React.ReactNode;
  disabled?: boolean;
  className?: string;
}

export function Radio({
  checked = false,
  onChange,
  value,
  label,
  disabled = false,
  className,
  ...props
}: RadioProps) {
  const handleChange = () => {
    if (disabled) return;
    onChange?.(value);
  };

  return (
    <div className={`flex items-center gap-2 ${className ?? ""}`}>
      <input
        type="radio"
        checked={checked}
        onChange={handleChange}
        disabled={disabled}
        value={value}
        className="peer sr-only"
        {...props}
      />
      <div
        className={[
          "relative inline-flex items-center justify-center h-5 w-5 shrink-0 rounded-full border-2 transition-all duration-200",
          checked
            ? "border-selection-radio-selected-outer bg-selection-radio-selected-center"
            : "border-selection-checkbox-unselected-border bg-transparent",
          disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer",
        ].join(" ")}
      >
        {checked && (
          <div className="h-2.5 w-2.5 rounded-full bg-selection-radio-selected-center" />
        )}
      </div>
      {label && (
        <label
          className="text-text-secondary text-sm font-medium select-none cursor-pointer"
          onClick={handleChange}
        >
          {label}
        </label>
      )}
    </div>
  );
}