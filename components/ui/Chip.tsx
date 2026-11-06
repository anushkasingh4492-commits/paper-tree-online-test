"use client";

import * as React from "react";

interface ChipProps extends Omit<React.HTMLAttributes<HTMLSpanElement>, "onSelect"> {
  selected?: boolean;
  onSelect?: (selected: boolean) => void;
  className?: string;
  children: React.ReactNode;
}

export function Chip({
  selected = false,
  onSelect,
  className,
  children,
  ...props
}: ChipProps) {
  const handleClick = () => {
    onSelect?.(!selected);
  };

  return (
    <span
      role="button"
      tabIndex={0}
      onClick={handleClick}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          handleClick();
        }
      }}
      className={[
        "inline-flex items-center justify-center gap-1.5 rounded-[4px] px-3 py-1.5 text-[10px] font-bold transition-all duration-200 cursor-pointer",
        selected
          ? "bg-selection-tab-chip-selected-bg text-selection-tab-chip-selected-text"
          : "bg-surface-surface text-text-tertiary border border-border-default",
        className,
      ].filter(Boolean).join(" ")}
      {...props}
    >
      {children}
    </span>
  );
}