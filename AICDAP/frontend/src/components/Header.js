import React from "react";
import { useNavigate } from "react-router-dom";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Container,
  useMediaQuery,
  useTheme,
  IconButton,
  Menu,
  MenuItem,
  Avatar,
  Divider,
} from "@mui/material";
import {
  Menu as MenuIcon,
  LogoutOutlined,
  PersonOutline,
  Brightness4,
  BrightnessHigh,
} from "@mui/icons-material";
import { useAuth } from "../contexts/AuthContext";
import { useTheme as useThemeContext } from "../contexts/ThemeContext";

const Header = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [userMenuAnchor, setUserMenuAnchor] = React.useState(null);
  const { user, signOut, isAuthenticated } = useAuth();
  const { toggleTheme, isDarkMode } = useThemeContext();

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleUserMenuOpen = (event) => {
    setUserMenuAnchor(event.currentTarget);
  };

  const handleUserMenuClose = () => {
    setUserMenuAnchor(null);
  };

  const handleSignOut = async () => {
    handleUserMenuClose();
    await signOut();
    navigate("/");
  };

  const navigationItems = [
    { label: "Home", path: "/" },
    { label: "About us", path: "/about" },
    { label: "Phishing Detection", path: "/url-scanner" },
    { label: "Insider Detection", path: "/admin/insider" },
    { label: "Enterprise Solutions", path: "/pricing" },
  ];

  const renderDesktopNav = () => (
    <Box sx={{ display: "flex", alignItems: "center", gap: 4 }}>
      {navigationItems.map((item) => (
        <Button
          key={item.label}
          color="inherit"
          onClick={() => navigate(item.path)}
          sx={{
            color: "text.secondary",
            fontWeight: 400,
            fontSize: "0.95rem",
            "&:hover": {
              color: "text.primary",
              backgroundColor: "transparent",
            },
          }}
        >
          {item.label}
        </Button>
      ))}
    </Box>
  );

  const renderUserMenu = () => (
    <>
      <IconButton onClick={handleUserMenuOpen} sx={{ ml: 2 }}>
        <Avatar
          sx={{
            width: 32,
            height: 32,
            bgcolor: "primary.main",
            fontSize: "0.875rem",
          }}
        >
          {user?.user_metadata?.firstName?.charAt(0)?.toUpperCase() ||
            user?.email?.charAt(0)?.toUpperCase() ||
            "U"}
        </Avatar>
      </IconButton>
      <Menu
        anchorEl={userMenuAnchor}
        open={Boolean(userMenuAnchor)}
        onClose={handleUserMenuClose}
        PaperProps={{
          sx: {
            backgroundColor: "background.paper",
            mt: 1.5,
            minWidth: 200,
          },
        }}
      >
        <MenuItem disabled sx={{ opacity: 1 }}>
          <Box>
            <Typography variant="subtitle2" sx={{ color: "text.primary" }}>
              {user?.user_metadata?.firstName && user?.user_metadata?.lastName
                ? `${user.user_metadata.firstName} ${user.user_metadata.lastName}`
                : user?.email || "User"}
            </Typography>
            <Typography variant="caption" sx={{ color: "text.secondary" }}>
              {user?.email}
            </Typography>
          </Box>
        </MenuItem>
        <Divider />
        <MenuItem
          onClick={() => {
            handleUserMenuClose();
            navigate("/admin/dashboard");
          }}
        >
          <PersonOutline sx={{ mr: 1, fontSize: "1rem" }} />
          Dashboard
        </MenuItem>
        <MenuItem onClick={handleSignOut}>
          <LogoutOutlined sx={{ mr: 1, fontSize: "1rem" }} />
          Sign Out
        </MenuItem>
      </Menu>
    </>
  );

  const renderMobileNav = () => (
    <>
      <IconButton
        color="inherit"
        aria-label="menu"
        onClick={handleMenuOpen}
        sx={{ color: "text.primary" }}
      >
        <MenuIcon />
      </IconButton>
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
        PaperProps={{
          sx: {
            backgroundColor: "background.paper",
            mt: 1.5,
          },
        }}
      >
        {navigationItems.map((item) => (
          <MenuItem
            key={item.label}
            onClick={() => {
              handleMenuClose();
              navigate(item.path);
            }}
            sx={{
              color: "text.secondary",
              "&:hover": {
                color: "text.primary",
                backgroundColor: "action.hover",
              },
            }}
          >
            {item.label}
          </MenuItem>
        ))}
        {!isAuthenticated && (
          <>
            <MenuItem onClick={handleMenuClose}>
              <Button
                variant="outlined"
                size="small"
                sx={{ mr: 1 }}
                onClick={() => navigate("/signup")}
              >
                Sign up
              </Button>
            </MenuItem>
            <MenuItem onClick={handleMenuClose}>
              <Button
                variant="contained"
                size="small"
                onClick={() => navigate("/login")}
              >
                Login
              </Button>
            </MenuItem>
          </>
        )}
        {isAuthenticated && (
          <>
            <Divider />
            <MenuItem
              onClick={() => {
                handleMenuClose();
                navigate("/admin/dashboard");
              }}
            >
              Dashboard
            </MenuItem>
            <MenuItem
              onClick={() => {
                handleMenuClose();
                handleSignOut();
              }}
            >
              Sign Out
            </MenuItem>
          </>
        )}
      </Menu>
    </>
  );

  return (
    <>
      <AppBar position="fixed" elevation={0}>
        <Container maxWidth="lg">
          <Toolbar sx={{ justifyContent: "space-between", py: 1 }}>
            {/* Logo */}
            <Typography
              variant="h5"
              component="div"
              onClick={() => navigate("/")}
              sx={{
                fontWeight: 700,
                color: "primary.main",
                fontSize: "1.5rem",
                letterSpacing: "0.5px",
                cursor: "pointer",
                "&:hover": {
                  opacity: 0.8,
                },
              }}
            >
              AICDAP
            </Typography>

            {/* Desktop Navigation */}
            {!isMobile && (
              <Box sx={{ display: "flex", alignItems: "center", gap: 4 }}>
                {renderDesktopNav()}
                {/* Theme Toggle Button */}
                <IconButton
                  onClick={toggleTheme}
                  sx={{
                    color: "text.primary",
                    transition: "transform 0.3s ease-in-out",
                    "&:hover": {
                      transform: "rotate(20deg)",
                    },
                  }}
                  title={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
                >
                  {isDarkMode ? <BrightnessHigh /> : <Brightness4 />}
                </IconButton>
                {!isAuthenticated ? (
                  <Box sx={{ display: "flex", gap: 2, ml: 2 }}>
                    <Button
                      variant="outlined"
                      size="medium"
                      onClick={() => navigate("/signup")}
                    >
                      Sign up
                    </Button>
                    <Button
                      variant="contained"
                      size="medium"
                      onClick={() => navigate("/login")}
                    >
                      Login
                    </Button>
                  </Box>
                ) : (
                  renderUserMenu()
                )}
              </Box>
            )}

            {/* Mobile Navigation */}
            {isMobile && renderMobileNav()}
          </Toolbar>
        </Container>
      </AppBar>
    </>
  );
};

export default Header;
