"use client";

import * as Lucide from "lucide-react";
import type { SVGProps } from "react";

export type IconVariant = "line" | "solid";

export type IconName =
  /* Navigation */
  | "home"
  | "grid"
  | "chevron-right"
  | "chevron-down"
  | "chevron-up"
  | "chevron-left"
  | "menu"
  | "sun"
  | "moon"
  /* Action */
  | "play"
  | "analytics"
  | "plus"
  | "edit"
  | "trash"
  | "download"
  /* Learning & Tests */
  | "bookmark"
  | "book"
  | "graduation-cap"
  | "test-tube"
  | "clock"
  /* Status & Feedback */
  | "check"
  | "cross"
  | "alert"
  | "info"
  /* User & Roles */
  | "user"
  | "users"
  /* Communication */
  | "bell"
  | "lock"
  | "message"
  /* System & Settings */
  | "settings"
  | "search"
  /* Miscellaneous */
  | "star"
  | "trophy"
  | "sparkles";

/** Lucide line (outline) icons. Default style per the design system. */
const LINE_ICONS: Record<IconName, React.ComponentType<SVGProps<SVGSVGElement> & { size?: number | string }>> = {
  home: Lucide.Home,
  grid: Lucide.Grid,
  "chevron-right": Lucide.ChevronRight,
  "chevron-down": Lucide.ChevronDown,
  "chevron-up": Lucide.ChevronUp,
  "chevron-left": Lucide.ChevronLeft,
  menu: Lucide.Menu,
  sun: Lucide.Sun,
  moon: Lucide.Moon,
  play: Lucide.Play,
  analytics: Lucide.BarChart3,
  plus: Lucide.Plus,
  edit: Lucide.Edit2,
  trash: Lucide.Trash2,
  download: Lucide.Download,
  bookmark: Lucide.Bookmark,
  book: Lucide.Book,
  "graduation-cap": Lucide.GraduationCap,
  "test-tube": Lucide.TestTube,
  clock: Lucide.Clock,
  check: Lucide.Check,
  cross: Lucide.X,
  alert: Lucide.AlertTriangle,
  info: Lucide.Info,
  user: Lucide.User,
  users: Lucide.Users,
  bell: Lucide.Bell,
  lock: Lucide.Lock,
  message: Lucide.MessageCircle,
  settings: Lucide.Settings,
  search: Lucide.Search,
  star: Lucide.Star,
  trophy: Lucide.Trophy,
  sparkles: Lucide.Sparkles,
};

/**
 * Unified icon component for the Paper Tree design system.
 *
 * - All icons come from Lucide React (consistent line weight & stroke).
 * - `variant="line"` (default) = outline style for general UI.
 * - `variant="solid"` = reserved for high-emphasis / active / selected states.
 *   Lucide React ships outline icons; the solid slot keeps the API ready for
 *   filled variants and is rendered with the icon's default appearance.
 */
export function Icon({
  name,
  size = 20,
  color,
  variant = "line",
  className,
  ...props
}: {
  name: IconName;
  size?: number | string;
  color?: string;
  variant?: IconVariant;
  className?: string;
} & Omit<SVGProps<SVGSVGElement>, "size" | "color">) {
  const Icon = LINE_ICONS[name];

  // Solid variants are reserved for active/selected states. Lucide React is an
  // outline icon library, so the solid slot renders the same glyph; the
  // `variant` prop locks in the semantic intent (high-emphasis state).
  const _ = variant;

  return (
    <Icon
      size={size}
      color={color}
      className={className}
      {...props}
    />
  );
}
