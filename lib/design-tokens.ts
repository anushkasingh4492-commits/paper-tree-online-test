/**
 * Paper Tree — Centralized Design System Tokens
 *
 * Single source of truth for every colour, radius, spacing, and interactive
 * state defined in the Wireframe-3 style guide. Use these constants in JS
 * (inline styles, canvas, charts) and the matching CSS custom properties in
 * `app/globals.css` for Tailwind classes.
 */

export const brand = {
  /** Primary Blue — main brand colour, primary CTAs, selected states */
  primary: "#2455C8",
  /** Deep Navy — pressed/active states, dark emphasis */
  deepNavy: "#081C49",
  /** Action Blue — hover / brighter primary state */
  actionBlue: "#3478E8",
  /** Purple — accent / secondary brand */
  purple: "#6846D9",
} as const;

export const state = {
  /** Error / destructive */
  error: "#D64545",
  /** Success / positive */
  success: "#20A568",
  /** Warning / attention */
  warning: "#E5B400",
  /** Info — same as Action Blue */
  info: "#3478E8",
  /** Yellow accent */
  yellow: "#FFC928",
  /** Subtle lavender surface for selected chips / tabs */
  subtleLavender: "#E5E9FF",
} as const;

/** Light-mode surface & background colours */
export const surfaceLight = {
  appBackground: "#F3F6FC",
  surface: "#FFFFFF",
  elevatedSurface: "#FFFFFF",
  subtleSurface: "#EEF2FF",
  mutedSurface: "#E5E9FF",
} as const;

/** Dark-mode surface & background colours */
export const surfaceDark = {
  appBackground: "#101828",
  surface: "#1B2942",
  elevatedSurface: "#263653",
  mutedSurface: "#303850",
} as const;

/** Text colour hierarchy (light mode) */
export const textLight = {
  primary: "#17233F",
  secondary: "#2A3868",
  tertiary: "#58688F",
  body: "#6F7E9E",
  supportingLabel: "#9AABCF",
  disabled: "#CFCEDC",
} as const;

/** Text colour hierarchy (dark mode) */
export const textDark = {
  primary: "#FFFFFF",
  secondary: "#E8EDF7",
  tertiary: "#A9B6CE",
  body: "#8FA0C4",
  supportingLabel: "#6A78A0",
  disabled: "#5A6484",
} as const;

/** Text-on-colour accessibility */
export const textOnColor = {
  onPrimary: "#FFFFFF",
  onSecondaryLight: "#2455CB",
  onSecondaryDark: "#FFFFFF",
  onDisabled: "#9AABCF",
} as const;

/** Corner radius scale */
export const radius = {
  micro: "4px", // tags, small chips
  standard: "8px", // inputs, buttons, standard cards
  card: "12px", // default card / medium containers
  large: "16px", // large cards / banners / feature containers
  hero: "24px", // extra large / hero containers
} as const;

/** Spacing */
export const spacing = {
  cardGap: "16px", // gap between all cards
  cardPadding: "16px", // internal card padding
  cardBorder: "1px solid", // card outline
} as const;

/** Interactive / CTA colours */
export const cta = {
  primary: {
    default: "#2455CB",
    hover: "#3478E8",
    pressed: "#081C49",
    disabled: "#D6DBE8",
  },
  secondaryLight: {
    default: "#E5E9FF",
  },
  secondaryDark: {
    default: "#30385C",
  },
  disabled: "#D6DBE8",
} as const;

/** Selection control colours */
export const selection = {
  radio: {
    selectedOuter: "#2455CB",
    selectedCenter: "#3455C8",
  },
  tabChip: {
    selectedBg: "#EEF2FF",
    selectedText: "#2455CB",
  },
  checkbox: {
    selectedFill: "#2455CB",
    selectedCheckmark: "#FFFFFF",
    selectedBorder: "#2455CB",
    unselectedFill: "#FFFFFF",
    unselectedBorder: "#D6DBE8",
  },
} as const;

/** Border colour (light) */
export const borderLight = {
  default: "#E5E9FF",
  muted: "#E5E9FF",
} as const;

/** Border colour (dark) */
export const borderDark = {
  default: "#303850",
  muted: "#303850",
} as const;

/** Gradient rule: gradients are strictly reserved for progress bars and graphs only. */
export const gradientRule =
  "Gradients are strictly reserved for progress bars and graphs only.";

/** Convenience: resolve surface / text / border by theme */
export function tokens(theme: "light" | "dark") {
  return {
    surface: theme === "dark" ? surfaceDark : surfaceLight,
    text: theme === "dark" ? textDark : textLight,
    border: theme === "dark" ? borderDark : borderLight,
  };
}
