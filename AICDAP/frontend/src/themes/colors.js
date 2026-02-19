/**
 * Color Constants for AICDAP Theme
 *
 * This file provides consistent color values that match our Cloudflare-inspired theme.
 * Use these constants instead of hardcoded hex values to maintain consistency
 * and make theme changes easier to manage.
 */

// Primary Brand Colors
export const CLOUDFLARE_COLORS = {
  // Primary Orange
  primary: {
    main: "#f38020",
    light: "#ff9d47",
    dark: "#d4650b",
    contrast: "#ffffff",
  },

  // Secondary Blue
  secondary: {
    main: "#0051c3",
    light: "#3b82f6",
    dark: "#003d99",
    contrast: "#ffffff",
  },

  // Status Colors
  success: {
    main: "#059669",
    light: "#10b981",
    dark: "#047857",
    contrast: "#ffffff",
  },

  warning: {
    main: "#f59e0b",
    light: "#fbbf24",
    dark: "#d97706",
    contrast: "#ffffff",
  },

  error: {
    main: "#dc2626",
    light: "#ef4444",
    dark: "#b91c1c",
    contrast: "#ffffff",
  },

  info: {
    main: "#0ea5e9",
    light: "#38bdf8",
    dark: "#0284c7",
    contrast: "#ffffff",
  },

  // Neutral Grays
  grey: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
  },

  // Text Colors
  text: {
    primary: "#1f2937",
    secondary: "#6b7280",
    disabled: "#9ca3af",
  },

  // Background Colors
  background: {
    default: "#ffffff",
    paper: "#ffffff",
    grey: "#f9fafb",
  },

  // Utility Colors
  divider: "#e5e7eb",
  border: "#d1d5db",
};

// CSS Custom Properties (CSS Variables)
export const CSS_VARIABLES = {
  "--color-primary": CLOUDFLARE_COLORS.primary.main,
  "--color-primary-light": CLOUDFLARE_COLORS.primary.light,
  "--color-primary-dark": CLOUDFLARE_COLORS.primary.dark,
  "--color-secondary": CLOUDFLARE_COLORS.secondary.main,
  "--color-secondary-light": CLOUDFLARE_COLORS.secondary.light,
  "--color-secondary-dark": CLOUDFLARE_COLORS.secondary.dark,
  "--color-text-primary": CLOUDFLARE_COLORS.text.primary,
  "--color-text-secondary": CLOUDFLARE_COLORS.text.secondary,
  "--color-background": CLOUDFLARE_COLORS.background.default,
  "--color-border": CLOUDFLARE_COLORS.border,
  "--color-divider": CLOUDFLARE_COLORS.divider,
};

// Alpha (Transparency) Utilities
export const withAlpha = (color, alpha) => {
  // Convert hex to rgba
  const hex = color.replace('#', '');
  const r = parseInt(hex.substr(0, 2), 16);
  const g = parseInt(hex.substr(2, 2), 16);
  const b = parseInt(hex.substr(4, 2), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
};

// Pre-defined alpha variants for common use cases
export const ALPHA_VARIANTS = {
  primary: {
    5: withAlpha(CLOUDFLARE_COLORS.primary.main, 0.05),
    10: withAlpha(CLOUDFLARE_COLORS.primary.main, 0.1),
    15: withAlpha(CLOUDFLARE_COLORS.primary.main, 0.15),
    20: withAlpha(CLOUDFLARE_COLORS.primary.main, 0.2),
    30: withAlpha(CLOUDFLARE_COLORS.primary.main, 0.3),
    50: withAlpha(CLOUDFLARE_COLORS.primary.main, 0.5),
  },
  secondary: {
    5: withAlpha(CLOUDFLARE_COLORS.secondary.main, 0.05),
    10: withAlpha(CLOUDFLARE_COLORS.secondary.main, 0.1),
    15: withAlpha(CLOUDFLARE_COLORS.secondary.main, 0.15),
    20: withAlpha(CLOUDFLARE_COLORS.secondary.main, 0.2),
    30: withAlpha(CLOUDFLARE_COLORS.secondary.main, 0.3),
    50: withAlpha(CLOUDFLARE_COLORS.secondary.main, 0.5),
  },
  black: {
    5: "rgba(0, 0, 0, 0.05)",
    10: "rgba(0, 0, 0, 0.1)",
    15: "rgba(0, 0, 0, 0.15)",
    20: "rgba(0, 0, 0, 0.2)",
    30: "rgba(0, 0, 0, 0.3)",
    50: "rgba(0, 0, 0, 0.5)",
  },
  white: {
    5: "rgba(255, 255, 255, 0.05)",
    10: "rgba(255, 255, 255, 0.1)",
    15: "rgba(255, 255, 255, 0.15)",
    20: "rgba(255, 255, 255, 0.2)",
    30: "rgba(255, 255, 255, 0.3)",
    50: "rgba(255, 255, 255, 0.5)",
    90: "rgba(255, 255, 255, 0.9)",
    95: "rgba(255, 255, 255, 0.95)",
  },
};

// Gradient Utilities
export const GRADIENTS = {
  primary: `linear-gradient(135deg, ${CLOUDFLARE_COLORS.primary.main} 0%, ${CLOUDFLARE_COLORS.primary.dark} 100%)`,
  primaryLight: `linear-gradient(135deg, ${CLOUDFLARE_COLORS.primary.light} 0%, ${CLOUDFLARE_COLORS.primary.main} 100%)`,
  secondary: `linear-gradient(135deg, ${CLOUDFLARE_COLORS.secondary.main} 0%, ${CLOUDFLARE_COLORS.secondary.dark} 100%)`,
  combined: `linear-gradient(135deg, ${CLOUDFLARE_COLORS.primary.main} 0%, ${CLOUDFLARE_COLORS.secondary.main} 100%)`,
  subtle: `linear-gradient(135deg, ${CLOUDFLARE_COLORS.grey[50]} 0%, ${CLOUDFLARE_COLORS.grey[100]} 100%)`,
  subtleReverse: `linear-gradient(135deg, ${CLOUDFLARE_COLORS.grey[100]} 0%, ${CLOUDFLARE_COLORS.grey[50]} 100%)`,
  // For overlays and hero sections
  primaryOverlay: `linear-gradient(135deg, ${ALPHA_VARIANTS.primary[10]} 0%, ${ALPHA_VARIANTS.secondary[5]} 100%)`,
  secondaryOverlay: `linear-gradient(135deg, ${ALPHA_VARIANTS.secondary[10]} 0%, ${ALPHA_VARIANTS.primary[5]} 100%)`,
};

// Shadow Utilities
export const SHADOWS = {
  sm: "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
  md: "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
  lg: "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
  xl: "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
  xxl: "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
  primary: `0 4px 12px ${ALPHA_VARIANTS.primary[30]}`,
  primaryHover: `0 6px 16px ${ALPHA_VARIANTS.primary[40]}`,
  secondary: `0 4px 12px ${ALPHA_VARIANTS.secondary[30]}`,
};

// Border Radius
export const BORDER_RADIUS = {
  sm: "4px",
  md: "8px",
  lg: "12px",
  xl: "16px",
  full: "50%",
};

// Usage Examples:
//
// Instead of: backgroundColor: "#f38020"
// Use: backgroundColor: CLOUDFLARE_COLORS.primary.main
//
// Instead of: backgroundColor: "rgba(243, 128, 32, 0.1)"
// Use: backgroundColor: ALPHA_VARIANTS.primary[10]
//
// Instead of: background: "linear-gradient(135deg, #f38020 0%, #d4650b 100%)"
// Use: background: GRADIENTS.primary
//
// Instead of: boxShadow: "0 4px 12px rgba(243, 128, 32, 0.3)"
// Use: boxShadow: SHADOWS.primary

export default CLOUDFLARE_COLORS;
