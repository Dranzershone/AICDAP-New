import React from "react";

import {
  Box,
  Container,
  Typography,
  Button,
  Card,
  CardContent,
  TextField,
  Grid,
  Paper,
  Chip,
  Avatar,
  IconButton,
  Divider,
} from "@mui/material";
import {
  PlayArrow,
  Security,
  Speed,
  Timeline,
  Favorite,
  Share,
  MoreVert,
} from "@mui/icons-material";

const ThemeDemo = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Typography Examples */}
      <Box sx={{ mb: 6 }}>
        <Typography variant="h2" gutterBottom>
          Theme Typography Examples
        </Typography>
        <Typography variant="h4" color="primary" gutterBottom>
          Protect Your App Against Non-Humans
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
          Enter the future of bot-free mobile apps. Simplify bot detection,
          enhance user experiences, and fortify your app's ecosystem.
        </Typography>

        <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap" }}>
          <Button
            variant="contained"
            size="large"
            startIcon={<PlayArrow />}
            onClick={() => {
              console.log("click");
              //navigate("/admin/dashboard");
            }}
          >
            Try Demoaa
          </Button>
          <Button variant="outlined" size="large">
            Verify you're human
          </Button>
        </Box>
      </Box>

      {/* Cards and Components */}
      <Grid container spacing={4} sx={{ mb: 6 }}>
        <Grid item xs={12} md={4}>
          <Card
            sx={{
              height: "100%",
              background:
                "linear-gradient(135deg, rgba(243, 128, 32, 0.1) 0%, rgba(0, 81, 195, 0.05) 100%)",
              border: "1px solid",
              borderColor: "primary.light",
            }}
          >
            <CardContent>
              <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
                <Avatar sx={{ bgcolor: "primary.main", mr: 2 }}>
                  <Security />
                </Avatar>
                <Typography variant="h6">Real-Time Monitoring</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Advanced bot detection algorithms that work in real-time to
                protect your application.
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Chip
                  label="Security"
                  size="small"
                  color="primary"
                  variant="outlined"
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card
            sx={{
              height: "100%",
              background:
                "linear-gradient(135deg, rgba(0, 81, 195, 0.1) 0%, rgba(243, 128, 32, 0.05) 100%)",
              border: "1px solid",
              borderColor: "secondary.light",
            }}
          >
            <CardContent>
              <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
                <Avatar sx={{ bgcolor: "secondary.main", mr: 2 }}>
                  <Speed />
                </Avatar>
                <Typography variant="h6">Create a campaign</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Comprehensive analytics dashboard with detailed reports and
                insights.
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Chip
                  label="Analytics"
                  size="small"
                  color="secondary"
                  variant="outlined"
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ height: "100%" }}>
            <CardContent>
              <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
                <Avatar sx={{ bgcolor: "success.main", mr: 2 }}>
                  <Timeline />
                </Avatar>
                <Typography variant="h6">Insider-Threat Monitoring</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Monitor your app's security status with real-time notifications
                and alerts.
              </Typography>
              <Box
                sx={{
                  mt: 2,
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <Chip
                  label="Monitoring"
                  size="small"
                  color="success"
                  variant="outlined"
                />
                <Box>
                  <IconButton size="small" color="primary">
                    <Favorite />
                  </IconButton>
                  <IconButton size="small" color="primary">
                    <Share />
                  </IconButton>
                  <IconButton size="small" color="primary">
                    <MoreVert />
                  </IconButton>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Form Components */}
      <Paper
        sx={{
          p: 4,
          mb: 4,
          background:
            "linear-gradient(135deg, rgba(249, 250, 251, 0.8) 0%, rgba(243, 244, 246, 0.9) 100%)",
          border: "1px solid",
          borderColor: "divider",
        }}
      >
        <Typography variant="h5" gutterBottom>
          Theme Form Components
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Email Address"
              variant="outlined"
              placeholder="Enter your email"
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Password"
              type="password"
              variant="outlined"
              placeholder="Enter your password"
              sx={{ mb: 2 }}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Company Name"
              variant="outlined"
              placeholder="Your company"
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Message"
              multiline
              rows={3}
              variant="outlined"
              placeholder="Tell us about your needs"
              sx={{ mb: 2 }}
            />
          </Grid>
        </Grid>
        <Divider sx={{ my: 3 }} />
        <Box sx={{ display: "flex", gap: 2, justifyContent: "flex-end" }}>
          <Button variant="outlined" size="large">
            Cancel
          </Button>
          <Button variant="contained" size="large">
            Get Started
          </Button>
        </Box>
      </Paper>

      {/* Color Palette Display */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          Theme Color Palette
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={6} sm={3}>
            <Paper
              sx={{
                p: 2,
                textAlign: "center",
                bgcolor: "primary.main",
                color: "primary.contrastText",
              }}
            >
              <Typography variant="subtitle2">Primary</Typography>
              <Typography variant="caption">#7367f0</Typography>
            </Paper>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Paper
              sx={{
                p: 2,
                textAlign: "center",
                bgcolor: "secondary.main",
                color: "secondary.contrastText",
              }}
            >
              <Typography variant="subtitle2">Secondary</Typography>
              <Typography variant="caption">#29c8e7</Typography>
            </Paper>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Paper
              sx={{
                p: 2,
                textAlign: "center",
                bgcolor: "success.main",
                color: "success.contrastText",
              }}
            >
              <Typography variant="subtitle2">Success</Typography>
              <Typography variant="caption">#66bb6a</Typography>
            </Paper>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Paper
              sx={{
                p: 2,
                textAlign: "center",
                bgcolor: "error.main",
                color: "error.contrastText",
              }}
            >
              <Typography variant="subtitle2">Error</Typography>
              <Typography variant="caption">#ff4757</Typography>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default ThemeDemo;
