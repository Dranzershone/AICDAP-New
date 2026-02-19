import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Avatar,
  useTheme,
} from "@mui/material";
import {
  PlayArrow,
  Email,
  School,
  CheckCircle,
  BugReport,
  TrendingUp,
  Security,
  Public,
  Hub,
} from "@mui/icons-material";
import { useNavigate } from "react-router-dom";

/* ---------- ANIMATIONS ---------- */

const fadeUp = {
  hidden: { opacity: 0, y: 40 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.8 } },
};

const stagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.18 } },
};

/* ---------- COMPONENT ---------- */

const Home = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const isDark = theme.palette.mode === "dark";

  /* ---------- COUNTERS ---------- */

  const [counts, setCounts] = useState({
    threats: 0,
    phishing: 0,
    training: 0,
    accuracy: 0,
  });

  const targets = {
    threats: 217000,
    phishing: 21700000,
    training: 868000,
    accuracy: 99.7,
  };

  const [startAnim, setStartAnim] = useState(false);

  useEffect(() => {
    if (!startAnim) return;

    const duration = 2000;
    const start = performance.now();

    const animate = (t) => {
      const progress = Math.min((t - start) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);

      const updated = {};
      Object.keys(targets).forEach((k) => {
        const val = targets[k] * ease;
        updated[k] =
          k === "accuracy" ? Number(val.toFixed(1)) : Math.floor(val);
      });

      setCounts(updated);
      if (progress < 1) requestAnimationFrame(animate);
    };

    requestAnimationFrame(animate);
  }, [startAnim]);

  const format = (v, k) => {
    if (k === "phishing") return (v / 1000000).toFixed(1) + "M";
    if (v >= 1000 && k !== "accuracy") return (v / 1000).toFixed(0) + "K";
    return v;
  };

  /* ---------- METRICS ---------- */

  const metrics = [
    { icon: <BugReport />, key: "threats", title: "Threats Detected", color: "#60A5FA" },
    { icon: <Email />, key: "phishing", title: "Phishing Blocked", color: "#A78BFA" },
    { icon: <School />, key: "training", title: "Trainings Completed", color: "#4ADE80" },
    { icon: <TrendingUp />, key: "accuracy", title: "Detection Accuracy", color: "#F59E0B" },
  ];

  return (
    <Box sx={{ position: "relative", overflow: "hidden" }}>

      {/* Background Glow - Adapts to theme */}
      <Box
        sx={{
          position: "absolute",
          width: 700,
          height: 700,
          background: isDark 
            ? "radial-gradient(circle, rgba(59, 130, 246, 0.4), transparent 70%)"
            : "radial-gradient(circle, rgba(59, 130, 246, 0.15), transparent 70%)",
          top: -250,
          left: -200,
          filter: "blur(140px)",
          zIndex: 0,
        }}
      />

      {/* HERO */}
      <Container maxWidth="lg" sx={{ py: 14, position: "relative", zIndex: 1 }}>
        <motion.div variants={stagger} initial="hidden" animate="visible">

          <motion.div variants={fadeUp}>
            <Typography
              variant="h1"
              sx={{
                fontWeight: 800,
                mb: 3,
                background: isDark
                  ? "linear-gradient(90deg, #E2E8F0, #60A5FA, #2563EB)"
                  : "linear-gradient(90deg, #1E293B, #2563EB, #1E40AF)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
                backgroundClip: "text",
                textShadow: isDark ? "0 0 35px rgba(96, 165, 250, 0.35)" : "none",
              }}
            >
              Secure Your Enterprise <Box component="span" sx={{ 
                background: isDark 
                  ? "linear-gradient(90deg, #F97316, #EF4444)"
                  : "linear-gradient(90deg, #EA580C, #DC2626)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
                backgroundClip: "text",
              }}>From Within</Box>
            </Typography>
          </motion.div>

          <motion.div variants={fadeUp}>
            <Typography 
              variant="h6" 
              sx={{ 
                mb: 4, 
                maxWidth: 650,
                color: isDark ? "rgba(226, 232, 240, 0.8)" : "rgba(51, 65, 85, 0.9)",
                fontWeight: 400,
                lineHeight: 1.6,
              }}
            >
              Detect insider threats before they become breaches using behavioral analytics,
              graph intelligence, and AI-driven anomaly detection.
            </Typography>
          </motion.div>

          <motion.div variants={fadeUp}>
            <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap" }}>
              <Button
                variant="contained"
                size="large"
                startIcon={<PlayArrow />}
                onClick={() => navigate("/admin/dashboard")}
                sx={{
                  px: 4,
                  py: 1.5,
                  fontSize: "1rem",
                  fontWeight: 600,
                  textTransform: "none",
                  boxShadow: isDark 
                    ? "0 4px 14px 0 rgba(59, 130, 246, 0.4)"
                    : "0 4px 14px 0 rgba(37, 99, 235, 0.3)",
                  "&:hover": {
                    boxShadow: isDark
                      ? "0 6px 20px 0 rgba(59, 130, 246, 0.5)"
                      : "0 6px 20px 0 rgba(37, 99, 235, 0.4)",
                  },
                }}
              >
                Detect Insider Threats
              </Button>

              <Button
                variant="outlined"
                size="large"
                onClick={() => navigate("/admin/insider")}
                sx={{
                  px: 4,
                  py: 1.5,
                  fontSize: "1rem",
                  fontWeight: 600,
                  textTransform: "none",
                  borderWidth: 2,
                  borderColor: isDark ? "rgba(96, 165, 250, 0.5)" : "primary.main",
                  color: isDark ? "#60A5FA" : "primary.main",
                  "&:hover": {
                    borderWidth: 2,
                    borderColor: isDark ? "#60A5FA" : "primary.dark",
                    backgroundColor: isDark 
                      ? "rgba(96, 165, 250, 0.1)"
                      : "rgba(37, 99, 235, 0.05)",
                  },
                }}
              >
                Insider Analysis
              </Button>
            </Box>
          </motion.div>

          <motion.div variants={fadeUp}>
            <Box sx={{ display: "flex", alignItems: "center", mt: 4, gap: 1 }}>
              <CheckCircle sx={{ color: "#22C55E", fontSize: 20 }} />
              <Typography 
                variant="body2" 
                sx={{ 
                  color: isDark ? "rgba(226, 232, 240, 0.7)" : "rgba(51, 65, 85, 0.8)",
                  fontWeight: 500,
                }}
              >
                Enterprise ready
              </Typography>
            </Box>
          </motion.div>

        </motion.div>
      </Container>

      {/* METRICS */}
      <Container maxWidth="lg" sx={{ py: 10 }}>
        <motion.div onViewportEnter={() => setStartAnim(true)} viewport={{ once: true }}>

          <Typography 
            variant="h3" 
            align="center" 
            sx={{ 
              mb: 2,
              fontWeight: 700,
              color: theme.palette.text.primary,
            }}
          >
            Real-Time Security Impact
          </Typography>
          
          <Typography 
            align="center" 
            sx={{ 
              mb: 7,
              color: theme.palette.text.secondary,
              fontSize: "1.1rem",
            }}
          >
            Live metrics showcasing our platform's effectiveness in protecting enterprises
          </Typography>

          <Grid container spacing={4}>
            {metrics.map((m, i) => (
              <Grid item xs={12} sm={6} md={3} key={i}>
                <motion.div whileHover={{ y: -10, transition: { duration: 0.3 } }}>
                  <Box
                    sx={{
                      p: 4,
                      textAlign: "center",
                      borderRadius: 4,
                      backdropFilter: "blur(12px)",
                      background: isDark 
                        ? "rgba(255, 255, 255, 0.05)"
                        : "rgba(255, 255, 255, 0.9)",
                      border: isDark 
                        ? "1px solid rgba(255, 255, 255, 0.1)"
                        : "1px solid rgba(0, 0, 0, 0.08)",
                      boxShadow: isDark
                        ? "0 4px 12px rgba(0, 0, 0, 0.2)"
                        : "0 4px 12px rgba(0, 0, 0, 0.05)",
                      transition: "all 0.3s ease",
                      "&:hover": {
                        boxShadow: isDark
                          ? `0 8px 24px ${m.color}40`
                          : `0 8px 24px ${m.color}30`,
                      },
                    }}
                  >
                    <Avatar 
                      sx={{ 
                        bgcolor: m.color, 
                        mx: "auto", 
                        mb: 2,
                        width: 56,
                        height: 56,
                      }}
                    >
                      {m.icon}
                    </Avatar>

                    <Typography
                      variant="h3"
                      sx={{
                        color: m.color,
                        fontWeight: 700,
                        textShadow: startAnim
                          ? `0 0 18px ${m.color}55`
                          : "none",
                        transform: startAnim ? "scale(1.04)" : "scale(1)",
                        transition: "0.5s",
                        mb: 1,
                      }}
                    >
                      {format(counts[m.key], m.key)}
                      {m.key === "accuracy" ? "%" : "+"}
                    </Typography>

                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: theme.palette.text.secondary,
                        fontWeight: 500,
                      }}
                    >
                      {m.title}
                    </Typography>
                  </Box>
                </motion.div>
              </Grid>
            ))}
          </Grid>
        </motion.div>
      </Container>

      {/* INSIDER THREAT INFO */}
      <Container maxWidth="md" sx={{ pb: 12 }}>
        <Box
          sx={{
            p: { xs: 4, md: 8 },
            textAlign: "center",
            borderRadius: 5,
            background: isDark
              ? "linear-gradient(135deg, rgba(59, 130, 246, 0.25), rgba(168, 85, 247, 0.25))"
              : "linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(168, 85, 247, 0.15))",
            backdropFilter: "blur(18px)",
            border: isDark
              ? "1px solid rgba(255, 255, 255, 0.18)"
              : "1px solid rgba(59, 130, 246, 0.3)",
            boxShadow: isDark
              ? "0 8px 32px rgba(59, 130, 246, 0.2)"
              : "0 8px 32px rgba(59, 130, 246, 0.15)",
          }}
        >
          <Typography 
            variant="h4" 
            sx={{ 
              mb: 2, 
              fontWeight: 700,
              color: isDark ? "#FFFFFF" : "#1E293B",
            }}
          >
            Insider Threats Cause Most Security Incidents
          </Typography>

          <Typography 
            sx={{ 
              mb: 5, 
              color: isDark ? "rgba(255, 255, 255, 0.85)" : "rgba(30, 41, 59, 0.8)",
              fontSize: "1.1rem",
              lineHeight: 1.7,
            }}
          >
            AICDAP continuously monitors behavioral signals across systems,
            detecting anomalies that traditional security tools miss.
          </Typography>

          <Button 
            variant="contained" 
            size="large"
            sx={{
              px: 5,
              py: 1.5,
              fontSize: "1rem",
              fontWeight: 600,
              textTransform: "none",
              backgroundColor: isDark ? "#3B82F6" : "#2563EB",
              boxShadow: "0 4px 14px 0 rgba(59, 130, 246, 0.4)",
              "&:hover": {
                backgroundColor: isDark ? "#2563EB" : "#1E40AF",
                boxShadow: "0 6px 20px 0 rgba(59, 130, 246, 0.5)",
              },
            }}
          >
            Analyze Insider Risk
          </Button>
        </Box>
      </Container>

      {/* ENTERPRISE SECTION */}
      <Container maxWidth="lg" sx={{ pb: 14 }}>
        <Typography 
          variant="h3" 
          align="center" 
          sx={{ 
            mb: 2,
            fontWeight: 700,
            color: theme.palette.text.primary,
          }}
        >
          Built for Enterprise-Scale Security
        </Typography>
        
        <Typography 
          align="center" 
          sx={{ 
            mb: 8,
            color: theme.palette.text.secondary,
            fontSize: "1.1rem",
          }}
        >
          Comprehensive protection across your entire infrastructure
        </Typography>

        <Grid container spacing={4}>
          {[
            {
              icon: <Security />,
              title: "Zero-Trust Architecture",
              desc: "Continuous verification of users, devices, and behaviors across your infrastructure.",
            },
            {
              icon: <Hub />,
              title: "Graph Intelligence Engine",
              desc: "Analyzes relationships between users, systems, and actions to detect hidden risks.",
            },
            {
              icon: <Public />,
              title: "Cross-Platform Visibility",
              desc: "Unified monitoring across endpoints, networks, applications, and cloud services.",
            },
          ].map((f, i) => (
            <Grid item xs={12} md={4} key={i}>
              <motion.div 
                whileHover={{ y: -10, transition: { duration: 0.3 } }}
                style={{ height: "100%" }}
              >
                <Box
                  sx={{
                    p: 4,
                    borderRadius: 4,
                    background: isDark 
                      ? "rgba(255, 255, 255, 0.05)"
                      : "rgba(255, 255, 255, 0.9)",
                    border: isDark 
                      ? "1px solid rgba(255, 255, 255, 0.1)"
                      : "1px solid rgba(0, 0, 0, 0.08)",
                    boxShadow: isDark
                      ? "0 4px 12px rgba(0, 0, 0, 0.2)"
                      : "0 4px 12px rgba(0, 0, 0, 0.05)",
                    height: "100%",
                    transition: "all 0.3s ease",
                    "&:hover": {
                      boxShadow: isDark
                        ? "0 8px 24px rgba(59, 130, 246, 0.3)"
                        : "0 8px 24px rgba(59, 130, 246, 0.2)",
                    },
                  }}
                >
                  <Avatar 
                    sx={{ 
                      bgcolor: "#3B82F6", 
                      mb: 2,
                      width: 56,
                      height: 56,
                    }}
                  >
                    {f.icon}
                  </Avatar>

                  <Typography 
                    variant="h6" 
                    sx={{ 
                      mb: 1.5,
                      fontWeight: 600,
                      color: theme.palette.text.primary,
                    }}
                  >
                    {f.title}
                  </Typography>

                  <Typography 
                    sx={{ 
                      color: theme.palette.text.secondary,
                      lineHeight: 1.7,
                    }}
                  >
                    {f.desc}
                  </Typography>
                </Box>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </Container>

    </Box>
  );
};

export default Home;