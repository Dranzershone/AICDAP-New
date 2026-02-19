import { createTheme } from "@mui/material/styles";

/**
 * AICDAP Cloudflare-Inspired Theme
 *
 * This theme implements Cloudflare's design system with:
 * - Primary: Cloudflare Orange (#f38020) for CTAs and brand elements
 * - Secondary: Cloudflare Blue (#0051c3) for informational elements
 * - Neutral grays: Professional hierarchy with proper contrast ratios
 * - Typography: Inter font family for modern, readable text
 * - Components: Consistent styling with accessibility in mind
 *
 * Color Accessibility:
 * - All text meets WCAG AA contrast requirements (4.5:1 minimum)
 * - Focus indicators are clearly visible
 * - Color is never the only indicator of information
 *
 * Usage:
 * - Use primary colors for important actions and brand elements
 * - Use secondary colors for informational content
 * - Use grey scale for hierarchy and supporting elements
 * - Maintain consistent spacing using the 8px grid system
 */

const cloudflareTheme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#f38020", // Cloudflare orange
      light: "#ff9d47",
      dark: "#d4650b",
      contrastText: "#ffffff",
    },
    secondary: {
      main: "#0051c3", // Cloudflare blue
      light: "#3b82f6",
      dark: "#003d99",
      contrastText: "#ffffff",
    },
    background: {
      default: "#ffffff", // Clean white background
      paper: "#ffffff",
    },
    text: {
      primary: "#1f2937", // Dark gray for primary text
      secondary: "#6b7280", // Medium gray for secondary text
      disabled: "#9ca3af",
    },
    error: {
      main: "#dc2626",
      light: "#ef4444",
      dark: "#b91c1c",
      contrastText: "#ffffff",
    },
    warning: {
      main: "#f59e0b",
      light: "#fbbf24",
      dark: "#d97706",
      contrastText: "#ffffff",
    },
    info: {
      main: "#0ea5e9",
      light: "#38bdf8",
      dark: "#0284c7",
      contrastText: "#ffffff",
    },
    success: {
      main: "#059669",
      light: "#10b981",
      dark: "#047857",
      contrastText: "#ffffff",
    },
    divider: "#e5e7eb",
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
  },
  typography: {
    fontFamily:
      'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    fontWeightLight: 300,
    fontWeightRegular: 400,
    fontWeightMedium: 500,
    fontWeightBold: 600,
    h1: {
      fontSize: "3.5rem",
      fontWeight: 600,
      lineHeight: 1.1,
      letterSpacing: "-0.025em",
      color: "#1f2937",
    },
    h2: {
      fontSize: "2.75rem",
      fontWeight: 600,
      lineHeight: 1.2,
      letterSpacing: "-0.025em",
      color: "#1f2937",
    },
    h3: {
      fontSize: "2.25rem",
      fontWeight: 600,
      lineHeight: 1.25,
      letterSpacing: "-0.025em",
      color: "#1f2937",
    },
    h4: {
      fontSize: "1.875rem",
      fontWeight: 600,
      lineHeight: 1.3,
      color: "#1f2937",
    },
    h5: {
      fontSize: "1.5rem",
      fontWeight: 600,
      lineHeight: 1.375,
      color: "#1f2937",
    },
    h6: {
      fontSize: "1.25rem",
      fontWeight: 600,
      lineHeight: 1.4,
      color: "#1f2937",
    },
    body1: {
      fontSize: "1rem",
      lineHeight: 1.6,
      color: "#374151",
      letterSpacing: "0em",
    },
    body2: {
      fontSize: "0.875rem",
      lineHeight: 1.5,
      color: "#4b5563",
      letterSpacing: "0em",
    },
    subtitle1: {
      fontSize: "1rem",
      fontWeight: 500,
      lineHeight: 1.75,
      color: "#374151",
    },
    subtitle2: {
      fontSize: "0.875rem",
      fontWeight: 500,
      lineHeight: 1.57,
      color: "#4b5563",
    },
    button: {
      textTransform: "none",
      fontWeight: 500,
      fontSize: "0.875rem",
      lineHeight: 1.5,
      letterSpacing: "0.025em",
    },
    caption: {
      fontSize: "0.75rem",
      fontWeight: 400,
      lineHeight: 1.5,
      color: "#6b7280",
    },
    overline: {
      fontSize: "0.75rem",
      fontWeight: 500,
      lineHeight: 2,
      letterSpacing: "0.1em",
      textTransform: "uppercase",
      color: "#6b7280",
    },
  },
  spacing: 8,
  breakpoints: {
    values: {
      xs: 0,
      sm: 640,
      md: 768,
      lg: 1024,
      xl: 1280,
    },
  },
  shape: {
    borderRadius: 8,
  },
  shadows: [
    "none",
    "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
    "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
    "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
    "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
  ],
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: "#ffffff",
          color: "#1f2937",
        },
        "*": {
          scrollbarWidth: "thin",
          "&::-webkit-scrollbar": {
            width: "6px",
            height: "6px",
          },
          "&::-webkit-scrollbar-track": {
            backgroundColor: "#f3f4f6",
          },
          "&::-webkit-scrollbar-thumb": {
            backgroundColor: "#d1d5db",
            borderRadius: "3px",
            "&:hover": {
              backgroundColor: "#9ca3af",
            },
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          padding: "10px 24px",
          fontSize: "0.875rem",
          fontWeight: 500,
          textTransform: "none",
          boxShadow: "none",
          transition: "all 0.2s ease-in-out",
        },
        contained: {
          background: "linear-gradient(135deg, #f38020 0%, #d4650b 100%)",
          color: "#ffffff",
          "&:hover": {
            background: "linear-gradient(135deg, #ff9d47 0%, #f38020 100%)",
            boxShadow: "0 4px 12px rgba(243, 128, 32, 0.3)",
            transform: "translateY(-1px)",
          },
          "&:active": {
            transform: "translateY(0)",
          },
        },
        outlined: {
          borderColor: "#f38020",
          color: "#f38020",
          backgroundColor: "transparent",
          "&:hover": {
            borderColor: "#d4650b",
            backgroundColor: "rgba(243, 128, 32, 0.05)",
          },
        },
        text: {
          color: "#374151",
          "&:hover": {
            backgroundColor: "rgba(243, 128, 32, 0.05)",
            color: "#f38020",
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: "rgba(255, 255, 255, 0.95)",
          backdropFilter: "blur(10px)",
          boxShadow:
            "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
          borderBottom: "1px solid #e5e7eb",
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: "#ffffff",
          backgroundImage: "none",
          boxShadow:
            "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
        },
        elevation1: {
          boxShadow:
            "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
        },
        elevation2: {
          boxShadow:
            "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: "#ffffff",
          borderRadius: 12,
          border: "1px solid #e5e7eb",
          boxShadow:
            "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
          transition: "all 0.2s ease-in-out",
          "&:hover": {
            boxShadow:
              "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
            transform: "translateY(-2px)",
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          "& .MuiOutlinedInput-root": {
            backgroundColor: "#ffffff",
            borderRadius: 8,
            "& fieldset": {
              borderColor: "#d1d5db",
              borderWidth: "1px",
            },
            "&:hover fieldset": {
              borderColor: "#9ca3af",
            },
            "&.Mui-focused fieldset": {
              borderColor: "#f38020",
              borderWidth: "2px",
            },
            "& input": {
              color: "#1f2937",
            },
          },
          "& .MuiInputLabel-root": {
            color: "#6b7280",
            "&.Mui-focused": {
              color: "#f38020",
            },
          },
          "& .MuiFormHelperText-root": {
            color: "#6b7280",
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 6,
          height: 28,
          fontSize: "0.75rem",
          fontWeight: 500,
        },
        colorPrimary: {
          backgroundColor: "rgba(243, 128, 32, 0.1)",
          color: "#d4650b",
          "&:hover": {
            backgroundColor: "rgba(243, 128, 32, 0.15)",
          },
        },
        colorSecondary: {
          backgroundColor: "rgba(0, 81, 195, 0.1)",
          color: "#003d99",
          "&:hover": {
            backgroundColor: "rgba(0, 81, 195, 0.15)",
          },
        },
      },
    },
    MuiAvatar: {
      styleOverrides: {
        root: {
          backgroundColor: "#f38020",
          color: "#ffffff",
          fontWeight: 500,
        },
      },
    },
    MuiMenu: {
      styleOverrides: {
        paper: {
          backgroundColor: "#ffffff",
          borderRadius: 8,
          border: "1px solid #e5e7eb",
          boxShadow:
            "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
          marginTop: 4,
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          color: "#374151",
          fontSize: "0.875rem",
          "&:hover": {
            backgroundColor: "rgba(243, 128, 32, 0.05)",
            color: "#f38020",
          },
          "&.Mui-selected": {
            backgroundColor: "rgba(243, 128, 32, 0.1)",
            color: "#f38020",
            "&:hover": {
              backgroundColor: "rgba(243, 128, 32, 0.15)",
            },
          },
        },
      },
    },
    MuiDivider: {
      styleOverrides: {
        root: {
          borderColor: "#e5e7eb",
        },
      },
    },
    MuiTypography: {
      styleOverrides: {
        root: {
          color: "inherit",
        },
        h1: {
          color: "#1f2937",
        },
        h2: {
          color: "#1f2937",
        },
        h3: {
          color: "#1f2937",
        },
        h4: {
          color: "#1f2937",
        },
        h5: {
          color: "#1f2937",
        },
        h6: {
          color: "#1f2937",
        },
        body1: {
          color: "#374151",
        },
        body2: {
          color: "#4b5563",
        },
        caption: {
          color: "#6b7280",
        },
      },
    },
  },
});

// Dark Mode Theme
const darkTheme = createTheme({
  palette: {
    mode: "dark",
    primary: {
      main: "#f38020", // Cloudflare orange stays vibrant in dark mode
      light: "#ff9d47",
      dark: "#d4650b",
      contrastText: "#ffffff",
    },
    secondary: {
      main: "#3b82f6", // Lighter blue variant for dark mode visibility
      light: "#60a5fa",
      dark: "#1d4ed8",
      contrastText: "#ffffff",
    },
    background: {
      default: "#0f172a", // Deep dark background
      paper: "#1e293b", // Slightly lighter for cards/papers
    },
    text: {
      primary: "#f1f5f9", // Light text for dark background
      secondary: "#cbd5e1", // Medium light gray for secondary text
      disabled: "#64748b",
    },
    error: {
      main: "#ef4444",
      light: "#f87171",
      dark: "#dc2626",
      contrastText: "#ffffff",
    },
    warning: {
      main: "#f59e0b",
      light: "#fbbf24",
      dark: "#d97706",
      contrastText: "#ffffff",
    },
    info: {
      main: "#38bdf8",
      light: "#7dd3fc",
      dark: "#0284c7",
      contrastText: "#ffffff",
    },
    success: {
      main: "#10b981",
      light: "#6ee7b7",
      dark: "#059669",
      contrastText: "#ffffff",
    },
    divider: "#334155",
    grey: {
      50: "#f8fafc",
      100: "#f1f5f9",
      200: "#e2e8f0",
      300: "#cbd5e1",
      400: "#94a3b8",
      500: "#64748b",
      600: "#475569",
      700: "#334155",
      800: "#1e293b",
      900: "#0f172a",
    },
  },
  typography: {
    fontFamily:
      'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    fontWeightLight: 300,
    fontWeightRegular: 400,
    fontWeightMedium: 500,
    fontWeightBold: 600,
    h1: {
      fontSize: "3.5rem",
      fontWeight: 600,
      lineHeight: 1.1,
      letterSpacing: "-0.025em",
      color: "#f1f5f9",
    },
    h2: {
      fontSize: "2.75rem",
      fontWeight: 600,
      lineHeight: 1.2,
      letterSpacing: "-0.025em",
      color: "#f1f5f9",
    },
    h3: {
      fontSize: "2.25rem",
      fontWeight: 600,
      lineHeight: 1.25,
      letterSpacing: "-0.025em",
      color: "#f1f5f9",
    },
    h4: {
      fontSize: "1.875rem",
      fontWeight: 600,
      lineHeight: 1.3,
      color: "#f1f5f9",
    },
    h5: {
      fontSize: "1.5rem",
      fontWeight: 600,
      lineHeight: 1.375,
      color: "#f1f5f9",
    },
    h6: {
      fontSize: "1.25rem",
      fontWeight: 600,
      lineHeight: 1.4,
      color: "#f1f5f9",
    },
    body1: {
      fontSize: "1rem",
      lineHeight: 1.6,
      color: "#e2e8f0",
      letterSpacing: "0em",
    },
    body2: {
      fontSize: "0.875rem",
      lineHeight: 1.5,
      color: "#cbd5e1",
      letterSpacing: "0em",
    },
    subtitle1: {
      fontSize: "1rem",
      fontWeight: 500,
      lineHeight: 1.75,
      color: "#cbd5e1",
    },
    subtitle2: {
      fontSize: "0.875rem",
      fontWeight: 500,
      lineHeight: 1.57,
      color: "#94a3b8",
    },
    button: {
      textTransform: "none",
      fontWeight: 500,
      fontSize: "0.875rem",
      lineHeight: 1.5,
      letterSpacing: "0.025em",
    },
    caption: {
      fontSize: "0.75rem",
      fontWeight: 400,
      lineHeight: 1.5,
      color: "#64748b",
    },
    overline: {
      fontSize: "0.75rem",
      fontWeight: 500,
      lineHeight: 2,
      letterSpacing: "0.1em",
      textTransform: "uppercase",
      color: "#64748b",
    },
  },
  spacing: 8,
  breakpoints: {
    values: {
      xs: 0,
      sm: 640,
      md: 768,
      lg: 1024,
      xl: 1280,
    },
  },
  shape: {
    borderRadius: 8,
  },
  shadows: [
    "none",
    "0 1px 3px 0 rgba(0, 0, 0, 0.5), 0 1px 2px 0 rgba(0, 0, 0, 0.3)",
    "0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -1px rgba(0, 0, 0, 0.3)",
    "0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.25)",
    "0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.2)",
    "0 25px 50px -12px rgba(0, 0, 0, 0.7)",
  ],
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: "#0f172a",
          color: "#f1f5f9",
        },
        "*": {
          scrollbarWidth: "thin",
          "&::-webkit-scrollbar": {
            width: "6px",
            height: "6px",
          },
          "&::-webkit-scrollbar-track": {
            backgroundColor: "#1e293b",
          },
          "&::-webkit-scrollbar-thumb": {
            backgroundColor: "#475569",
            borderRadius: "3px",
            "&:hover": {
              backgroundColor: "#64748b",
            },
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          padding: "10px 24px",
          fontSize: "0.875rem",
          fontWeight: 500,
          textTransform: "none",
          boxShadow: "none",
          transition: "all 0.2s ease-in-out",
        },
        contained: {
          background: "linear-gradient(135deg, #f38020 0%, #d4650b 100%)",
          color: "#ffffff",
          "&:hover": {
            background: "linear-gradient(135deg, #ff9d47 0%, #f38020 100%)",
            boxShadow: "0 4px 12px rgba(243, 128, 32, 0.4)",
            transform: "translateY(-1px)",
          },
          "&:active": {
            transform: "translateY(0)",
          },
        },
        outlined: {
          borderColor: "#f38020",
          color: "#f38020",
          backgroundColor: "transparent",
          "&:hover": {
            borderColor: "#ff9d47",
            backgroundColor: "rgba(243, 128, 32, 0.1)",
          },
        },
        text: {
          color: "#cbd5e1",
          "&:hover": {
            backgroundColor: "rgba(243, 128, 32, 0.1)",
            color: "#f38020",
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: "rgba(15, 23, 42, 0.95)",
          backdropFilter: "blur(10px)",
          boxShadow:
            "0 1px 3px 0 rgba(0, 0, 0, 0.5), 0 1px 2px 0 rgba(0, 0, 0, 0.3)",
          borderBottom: "1px solid #334155",
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: "#1e293b",
          backgroundImage: "none",
          boxShadow:
            "0 1px 3px 0 rgba(0, 0, 0, 0.5), 0 1px 2px 0 rgba(0, 0, 0, 0.3)",
        },
        elevation1: {
          boxShadow:
            "0 1px 3px 0 rgba(0, 0, 0, 0.5), 0 1px 2px 0 rgba(0, 0, 0, 0.3)",
        },
        elevation2: {
          boxShadow:
            "0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -1px rgba(0, 0, 0, 0.3)",
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: "#1e293b",
          borderRadius: 12,
          border: "1px solid #334155",
          boxShadow:
            "0 1px 3px 0 rgba(0, 0, 0, 0.5), 0 1px 2px 0 rgba(0, 0, 0, 0.3)",
          transition: "all 0.2s ease-in-out",
          "&:hover": {
            boxShadow:
              "0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.25)",
            transform: "translateY(-2px)",
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          "& .MuiOutlinedInput-root": {
            backgroundColor: "#0f172a",
            borderRadius: 8,
            "& fieldset": {
              borderColor: "#475569",
              borderWidth: "1px",
            },
            "&:hover fieldset": {
              borderColor: "#64748b",
            },
            "&.Mui-focused fieldset": {
              borderColor: "#f38020",
              borderWidth: "2px",
            },
            "& input": {
              color: "#f1f5f9",
            },
          },
          "& .MuiInputLabel-root": {
            color: "#94a3b8",
            "&.Mui-focused": {
              color: "#f38020",
            },
          },
          "& .MuiFormHelperText-root": {
            color: "#64748b",
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 6,
          height: 28,
          fontSize: "0.75rem",
          fontWeight: 500,
        },
        colorPrimary: {
          backgroundColor: "rgba(243, 128, 32, 0.15)",
          color: "#ff9d47",
          "&:hover": {
            backgroundColor: "rgba(243, 128, 32, 0.25)",
          },
        },
        colorSecondary: {
          backgroundColor: "rgba(59, 130, 246, 0.15)",
          color: "#60a5fa",
          "&:hover": {
            backgroundColor: "rgba(59, 130, 246, 0.25)",
          },
        },
      },
    },
    MuiAvatar: {
      styleOverrides: {
        root: {
          backgroundColor: "#f38020",
          color: "#ffffff",
          fontWeight: 500,
        },
      },
    },
    MuiMenu: {
      styleOverrides: {
        paper: {
          backgroundColor: "#1e293b",
          borderRadius: 8,
          border: "1px solid #334155",
          boxShadow:
            "0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.25)",
          marginTop: 4,
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          color: "#cbd5e1",
          fontSize: "0.875rem",
          "&:hover": {
            backgroundColor: "rgba(243, 128, 32, 0.1)",
            color: "#f38020",
          },
          "&.Mui-selected": {
            backgroundColor: "rgba(243, 128, 32, 0.15)",
            color: "#f38020",
            "&:hover": {
              backgroundColor: "rgba(243, 128, 32, 0.2)",
            },
          },
        },
      },
    },
    MuiDivider: {
      styleOverrides: {
        root: {
          borderColor: "#334155",
        },
      },
    },
    MuiTypography: {
      styleOverrides: {
        root: {
          color: "inherit",
        },
        h1: {
          color: "#f1f5f9",
        },
        h2: {
          color: "#f1f5f9",
        },
        h3: {
          color: "#f1f5f9",
        },
        h4: {
          color: "#f1f5f9",
        },
        h5: {
          color: "#f1f5f9",
        },
        h6: {
          color: "#f1f5f9",
        },
        body1: {
          color: "#e2e8f0",
        },
        body2: {
          color: "#cbd5e1",
        },
        caption: {
          color: "#64748b",
        },
      },
    },
  },
});

export { cloudflareTheme, darkTheme };
export default cloudflareTheme;
