import React from "react";
import { BrowserRouter, useLocation } from "react-router-dom";
import { ThemeProvider, CssBaseline, Box } from "@mui/material";
import { ThemeContextProvider, useTheme } from "./contexts/ThemeContext";
import { Header } from "./components";
import AppRoutes from "./routes";
import { AuthProvider } from "./contexts/AuthContext";

const AppContent = () => {
  const location = useLocation();
  const isAuthPage = ["/login", "/signup", "/forgot-password"].includes(
    location.pathname,
  );

  return (
    <Box
      sx={{
        minHeight: "100vh",
        backgroundColor: "background.default",
      }}
    >
      {!isAuthPage && <Header />}
      <Box
        component="main"
        sx={{
          pt: !isAuthPage ? 10 : 0,
          minHeight: !isAuthPage ? "calc(100vh - 80px)" : "100vh",
        }}
      >
        <AppRoutes />
      </Box>
    </Box>
  );
};

function AppContentWithTheme() {
  const { theme } = useTheme();

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <AuthProvider>
          <AppContent />
        </AuthProvider>
      </BrowserRouter>
    </ThemeProvider>
  );
}

function App() {
  return (
    <ThemeContextProvider>
      <AppContentWithTheme />
    </ThemeContextProvider>
  );
}

export default App;
