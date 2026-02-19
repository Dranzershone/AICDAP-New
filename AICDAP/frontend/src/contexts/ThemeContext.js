import React, { createContext, useContext, useMemo, useState } from "react";
import { createTheme } from "@mui/material/styles";

const ThemeContext = createContext();

export const ThemeContextProvider = ({ children }) => {
  const [mode, setMode] = useState("dark");

  const toggleTheme = () => {
    setMode((prev) => (prev === "dark" ? "light" : "dark"));
  };

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode,

          ...(mode === "dark"
            ? {
                background: {
                  default: "#070B14",
                  paper: "#0F172A",
                },
                primary: { main: "#4DA3FF" },
                secondary: { main: "#A78BFA" },
                text: {
                  primary: "#E5ECF5",
                  secondary: "#94A3B8",
                },
                divider: "rgba(255,255,255,0.08)",
              }
            : {
                background: {
                  default: "#F8FAFC",
                  paper: "#FFFFFF",
                },
                primary: { main: "#2563EB" },
                secondary: { main: "#7C3AED" },
                text: {
                  primary: "#0F172A",
                  secondary: "#475569",
                },
                divider: "rgba(0,0,0,0.08)",
              }),
        },

        typography: {
          fontFamily: `"Inter","Roboto","Helvetica","Arial",sans-serif`,

          h1: {
            fontWeight: 800,
            letterSpacing: "-0.02em",
          },
          h2: { fontWeight: 700 },
          h3: { fontWeight: 700 },
          h4: { fontWeight: 600 },

          button: {
            fontWeight: 600,
            textTransform: "none",
          },
        },

        shape: { borderRadius: 12 },

        components: {
          MuiCssBaseline: {
            styleOverrides: {
              body: {
                backgroundColor: mode === "dark" ? "#070B14" : "#F8FAFC",
                color: mode === "dark" ? "#E5ECF5" : "#0F172A",
              },

              /* ---------- GLOBAL GRADIENT HEADINGS ---------- */

              "h1, h2, h3": {
                background:
                  mode === "dark"
                    ? "linear-gradient(90deg,#E6F0FF,#60A5FA,#3B82F6)"
                    : "linear-gradient(90deg,#0F172A,#2563EB)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              },

              /* paragraph text */
              p: {
                color: mode === "dark" ? "#C7D2E0" : "#475569",
              },

              a: {
                textDecoration: "none",
                color: mode === "dark" ? "#60A5FA" : "#2563EB",
              },
            },
          },

          MuiButton: {
            styleOverrides: {
              root: {
                borderRadius: 10,
                padding: "10px 22px",
              },
            },
          },

          MuiCard: {
            styleOverrides: {
              root: {
                borderRadius: 16,
                border: "1px solid rgba(255,255,255,0.08)",
              },
            },
          },
        },
      }),
    [mode]
  );

  return (
    <ThemeContext.Provider value={{ theme, mode, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used inside ThemeContextProvider");
  }
  return context;
};