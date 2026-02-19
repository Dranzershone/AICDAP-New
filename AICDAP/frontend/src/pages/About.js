import React from "react";
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Avatar,
  Paper,
  Chip,
} from "@mui/material";
import { Security, Group, TrendingUp } from "@mui/icons-material";

const About = () => {
  const stats = [
    { label: "Enterprises Protected", value: "500+", color: "primary" },
    { label: "Insider Threats Detected", value: "25K+", color: "secondary" },
    { label: "Phishing Attempts Blocked", value: "2.5M+", color: "success" },
    { label: "Training Modules Completed", value: "100K+", color: "info" },
  ];

  const team = [
    {
      name: "Behavioral Analytics Engine",
      role: "AI-powered insider threat detection using advanced behavioral pattern analysis",
      icon: <Security />,
      color: "primary",
    },
    {
      name: "Phishing Intelligence Network",
      role: "Real-time threat intelligence and email security powered by global threat feeds",
      icon: <Group />,
      color: "secondary",
    },

    {
      name: "Interactive Security Education",
      role: "Gamified training platform with simulated phishing campaigns and assessments",
      icon: <TrendingUp />,
      color: "info",
    },
  ];

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header Section */}
      <Box sx={{ textAlign: "center", mb: 8 }}>
        <Typography variant="h2" component="h1" gutterBottom>
          About{" "}
          <Box component="span" sx={{ color: "primary.main" }}>
            AICDAP
          </Box>
        </Typography>
        <Typography
          variant="h5"
          color="text.secondary"
          sx={{ maxWidth: 800, mx: "auto" }}
        >
          We're on a mission to safeguard enterprises from within by detecting
          insider threats, preventing phishing attacks, and educating workforces
          to become the strongest line of cybersecurity defense.
        </Typography>
      </Box>

      {/* Mission Section */}
      <Paper
        sx={{
          p: { xs: 4, md: 6 },
          mb: 8,
          background:
            "linear-gradient(135deg, rgba(243, 128, 32, 0.1) 0%, rgba(0, 81, 195, 0.05) 100%)",
          border: "1px solid",
          borderColor: "primary.light",
        }}
      >
        <Grid container spacing={4} alignItems="center">
          <Grid item xs={12} md={6}>
            <Typography variant="h4" component="h2" gutterBottom>
              Our Mission
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              In today's threat landscape, the greatest risks often come from
              within. AICDAP was created to provide enterprises with
              comprehensive insider threat detection, phishing prevention, and
              cybersecurity education solutions that protect organizations from
              malicious actors while empowering employees with security
              awareness.
            </Typography>
            <Typography variant="body1" color="text.secondary">
              We believe that every organization deserves protection from
              insider threats and sophisticated phishing campaigns. Our
              integrated platform combines AI-powered detection with
              human-centered education to create a resilient security ecosystem.
            </Typography>
          </Grid>
          <Grid item xs={12} md={6}>
          </Grid>
        </Grid>
      </Paper>

      {/* Stats Section */}
      <Box sx={{ mb: 8 }}>
        <Typography
          variant="h4"
          component="h2"
          textAlign="center"
          gutterBottom
          sx={{ mb: 4 }}
        >
          Our Impact
        </Typography>
        <Grid container spacing={3}>
          {stats.map((stat, index) => (
            <Grid item xs={6} md={3} key={index}>
              <Card
                sx={{
                  textAlign: "center",
                  p: 3,
                  background: "background.paper",
                  border: "1px solid",
                  borderColor: "divider",
                }}
              >
                <Typography
                  variant="h3"
                  color={`${stat.color}.main`}
                  gutterBottom
                >
                  {stat.value}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {stat.label}
                </Typography>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Technology Section */}
      <Box sx={{ mb: 8 }}>
        <Typography
          variant="h4"
          component="h2"
          textAlign="center"
          gutterBottom
          sx={{ mb: 4 }}
        >
          What Makes Us Different
        </Typography>
        <Grid container spacing={6}>
          {team.map((item, index) => (
            <Grid item xs={12} md={6} key={index}>
              <Card
                sx={{
                  p: 3,
                  height: "100%",
                  background: "background.paper",
                  border: "1px solid",
                  borderColor: "divider",
                  transition: "transform 0.2s ease-in-out",
                  "&:hover": {
                    transform: "translateY(-2px)",
                  },
                }}
              >
                <CardContent sx={{ p: 0 }}>
                  <Box
                    sx={{ display: "flex", alignItems: "flex-start", mb: 2 }}
                  >
                    <Avatar
                      sx={{
                        bgcolor: `${item.color}.main`,
                        mr: 2,
                        width: 48,
                        height: 48,
                      }}
                    >
                      {item.icon}
                    </Avatar>
                    <Box>
                      <Typography variant="h6" component="h3" gutterBottom>
                        {item.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {item.role}
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

    </Container>
  );
};

export default About;
