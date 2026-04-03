import React, { useState, useEffect, useRef } from "react";
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
  ArrowForward,
  Shield,
} from "@mui/icons-material";
import { useNavigate } from "react-router-dom";

/* ============================================================
   ANIMATED BACKGROUND CANVAS — static grid + floating particles + scan line
   No mouse interaction / hover bending
   ============================================================ */
const GridCanvas = ({ isDark }) => {
  const canvasRef = useRef(null);
  const animFrameRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener("resize", resize);

    const COLS = 20;
    const ROWS = 13;

    // Floating particles — autonomous, no mouse interaction
    const particles = Array.from({ length: 55 }, () => ({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      r: Math.random() * 1.8 + 0.4,
      alpha: Math.random() * 0.5 + 0.15,
      pulse: Math.random() * Math.PI * 2,
    }));

    // Connection lines between nearby particles
    const MAX_DIST = 110;

    let t = 0;
    const draw = () => {
      t += 0.007;
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const cellW = canvas.width / COLS;
      const cellH = canvas.height / ROWS;

      // Static grid lines
      ctx.strokeStyle = isDark ? "rgba(59,130,246,0.07)" : "rgba(37,99,235,0.06)";
      ctx.lineWidth = 1;
      for (let c = 0; c <= COLS; c++) {
        ctx.beginPath();
        ctx.moveTo(c * cellW, 0);
        ctx.lineTo(c * cellW, canvas.height);
        ctx.stroke();
      }
      for (let r = 0; r <= ROWS; r++) {
        ctx.beginPath();
        ctx.moveTo(0, r * cellH);
        ctx.lineTo(canvas.width, r * cellH);
        ctx.stroke();
      }

      // Subtle intersection dots
      for (let c = 0; c <= COLS; c++) {
        for (let r = 0; r <= ROWS; r++) {
          ctx.beginPath();
          ctx.arc(c * cellW, r * cellH, 1, 0, Math.PI * 2);
          ctx.fillStyle = isDark ? "rgba(59,130,246,0.18)" : "rgba(37,99,235,0.14)";
          ctx.fill();
        }
      }

      // Move + draw particles
      particles.forEach((p) => {
        p.x += p.vx;
        p.y += p.vy;
        p.pulse += 0.02;
        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;
        if (p.y < 0) p.y = canvas.height;
        if (p.y > canvas.height) p.y = 0;

        const pulsedAlpha = p.alpha * (0.7 + 0.3 * Math.sin(p.pulse));
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = isDark
          ? `rgba(147,197,253,${pulsedAlpha})`
          : `rgba(37,99,235,${pulsedAlpha * 0.55})`;
        ctx.fill();
      });

      // Connection lines between nearby particles
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.hypot(dx, dy);
          if (dist < MAX_DIST) {
            const lineAlpha = (1 - dist / MAX_DIST) * 0.18;
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = isDark
              ? `rgba(96,165,250,${lineAlpha})`
              : `rgba(37,99,235,${lineAlpha * 0.6})`;
            ctx.lineWidth = 0.6;
            ctx.stroke();
          }
        }
      }

      // Scanning line sweeping down
      const scanY = ((t * 70) % (canvas.height + 120)) - 60;
      const scanGrad = ctx.createLinearGradient(0, scanY - 80, 0, scanY + 80);
      scanGrad.addColorStop(0, "transparent");
      scanGrad.addColorStop(0.5, isDark ? "rgba(59,130,246,0.055)" : "rgba(37,99,235,0.035)");
      scanGrad.addColorStop(1, "transparent");
      ctx.fillStyle = scanGrad;
      ctx.fillRect(0, scanY - 80, canvas.width, 160);

      animFrameRef.current = requestAnimationFrame(draw);
    };

    draw();
    return () => {
      cancelAnimationFrame(animFrameRef.current);
      window.removeEventListener("resize", resize);
    };
  }, [isDark]);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: "fixed",
        top: 0, left: 0,
        width: "100%", height: "100%",
        zIndex: 0,
        pointerEvents: "none",
      }}
    />
  );
};

/* ============================================================
   GLITCH TEXT
   ============================================================ */
const GlitchText = ({ children, sx = {} }) => {
  const [glitch, setGlitch] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setGlitch(true);
      setTimeout(() => setGlitch(false), 120);
    }, 4000 + Math.random() * 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Box sx={{ position: "relative", display: "inline-block", ...sx }}>
      <Box component="span" sx={{
        position: "relative",
        display: "inline-block",
        "&::before": glitch ? {
          content: 'attr(data-text)',
          position: "absolute",
          top: 0, left: "2px",
          color: "#ef4444",
          clipPath: "polygon(0 30%, 100% 30%, 100% 50%, 0 50%)",
          animation: "none",
        } : {},
      }}>
        {children}
      </Box>
    </Box>
  );
};

/* ============================================================
   CYBER BADGE
   ============================================================ */
const CyberBadge = ({ children }) => (
  <Box sx={{
    display: "inline-flex", alignItems: "center", gap: 1,
    px: 2, py: 0.75,
    border: "1px solid rgba(59,130,246,0.4)",
    borderRadius: "2px",
    background: "rgba(59,130,246,0.08)",
    backdropFilter: "blur(8px)",
    position: "relative",
    "&::before": {
      content: '""',
      position: "absolute",
      top: -1, left: 8, width: 20, height: 2,
      background: "#3B82F6",
    },
    "&::after": {
      content: '""',
      position: "absolute",
      bottom: -1, right: 8, width: 20, height: 2,
      background: "#3B82F6",
    },
  }}>
    {children}
  </Box>
);

/* ============================================================
   STAT CARD
   ============================================================ */
const StatCard = ({ icon, value, suffix, title, color, isDark }) => {
  const [hovered, setHovered] = useState(false);

  return (
    <motion.div
      onHoverStart={() => setHovered(true)}
      onHoverEnd={() => setHovered(false)}
      whileHover={{ y: -8, scale: 1.02 }}
      transition={{ duration: 0.3 }}
    >
      <Box sx={{
        position: "relative",
        p: 4,
        borderRadius: "4px",
        background: isDark
          ? "rgba(5,10,25,0.85)"
          : "rgba(248,250,255,0.92)",
        border: `1px solid ${hovered ? color + "60" : (isDark ? "rgba(59,130,246,0.12)" : "rgba(37,99,235,0.12)")}`,
        backdropFilter: "blur(16px)",
        overflow: "hidden",
        transition: "border-color 0.3s",
        boxShadow: hovered
          ? `0 0 30px ${color}25, 0 8px 32px rgba(0,0,0,0.2)`
          : isDark ? "0 4px 16px rgba(0,0,0,0.3)" : "0 4px 16px rgba(0,0,0,0.06)",
        "&::before": {
          content: '""',
          position: "absolute",
          top: 0, left: 0, right: 0,
          height: "2px",
          background: `linear-gradient(90deg, transparent, ${color}, transparent)`,
          opacity: hovered ? 1 : 0,
          transition: "opacity 0.3s",
        },
        "&::after": {
          content: '""',
          position: "absolute",
          inset: 0,
          background: `radial-gradient(ellipse at 50% 0%, ${color}12, transparent 70%)`,
          opacity: hovered ? 1 : 0,
          transition: "opacity 0.3s",
        },
      }}>
        {/* Corner accents */}
        <Box sx={{ position: "absolute", top: 0, left: 0, width: 16, height: 16, borderTop: `2px solid ${color}`, borderLeft: `2px solid ${color}` }} />
        <Box sx={{ position: "absolute", bottom: 0, right: 0, width: 16, height: 16, borderBottom: `2px solid ${color}`, borderRight: `2px solid ${color}` }} />

        <Box sx={{ display: "flex", alignItems: "center", gap: 2, mb: 3 }}>
          <Box sx={{
            width: 44, height: 44,
            display: "flex", alignItems: "center", justifyContent: "center",
            background: `${color}18`,
            border: `1px solid ${color}40`,
            borderRadius: "4px",
            color: color,
          }}>
            {icon}
          </Box>
          <Typography sx={{ fontSize: "0.7rem", letterSpacing: "0.15em", color: isDark ? "rgba(148,163,184,0.8)" : "rgba(100,116,139,0.9)", textTransform: "uppercase", fontFamily: "'Courier New', monospace" }}>
            {title}
          </Typography>
        </Box>

        <Typography sx={{
          fontSize: "2.6rem",
          fontWeight: 800,
          fontFamily: "'Courier New', monospace",
          color: color,
          letterSpacing: "-0.02em",
          textShadow: hovered ? `0 0 20px ${color}60` : "none",
          transition: "text-shadow 0.3s",
          lineHeight: 1,
        }}>
          {value}{suffix}
        </Typography>
      </Box>
    </motion.div>
  );
};

/* ============================================================
   FEATURE CARD
   ============================================================ */
const FeatureCard = ({ icon, title, desc, index, isDark }) => {
  const [hovered, setHovered] = useState(false);
  const colors = ["#3B82F6", "#8B5CF6", "#06B6D4"];
  const color = colors[index % 3];

  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: index * 0.15 }}
      viewport={{ once: true }}
      onHoverStart={() => setHovered(true)}
      onHoverEnd={() => setHovered(false)}
      whileHover={{ y: -6 }}
      style={{ height: "100%" }}
    >
      <Box sx={{
        p: "32px",
        height: "100%",
        borderRadius: "4px",
        background: isDark ? "rgba(5,10,25,0.8)" : "rgba(248,250,255,0.9)",
        border: `1px solid ${hovered ? color + "50" : (isDark ? "rgba(255,255,255,0.07)" : "rgba(0,0,0,0.07)")}`,
        backdropFilter: "blur(16px)",
        position: "relative",
        overflow: "hidden",
        transition: "all 0.4s",
        boxShadow: hovered
          ? `0 0 40px ${color}20, 0 16px 48px rgba(0,0,0,0.15)`
          : isDark ? "0 2px 12px rgba(0,0,0,0.2)" : "0 2px 12px rgba(0,0,0,0.05)",
      }}>
        {/* Top border glow */}
        <Box sx={{
          position: "absolute", top: 0, left: 0, right: 0, height: 2,
          background: `linear-gradient(90deg, transparent 0%, ${color} 50%, transparent 100%)`,
          opacity: hovered ? 1 : 0.3,
          transition: "opacity 0.3s",
        }} />

        {/* Background shape */}
        <Box sx={{
          position: "absolute", bottom: -40, right: -40,
          width: 140, height: 140,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${color}15, transparent 70%)`,
          opacity: hovered ? 1 : 0.5,
          transition: "opacity 0.4s",
        }} />

        <Box sx={{
          width: 56, height: 56,
          display: "flex", alignItems: "center", justifyContent: "center",
          background: `${color}15`,
          border: `1px solid ${color}35`,
          borderRadius: "4px",
          color: color,
          mb: 3,
          fontSize: 24,
        }}>
          {icon}
        </Box>

        <Typography sx={{
          fontSize: "1.1rem",
          fontWeight: 700,
          mb: 1.5,
          color: isDark ? "#E2E8F0" : "#0F172A",
          fontFamily: "'Outfit', sans-serif",
          letterSpacing: "-0.01em",
        }}>
          {title}
        </Typography>

        <Typography sx={{
          color: isDark ? "rgba(148,163,184,0.85)" : "rgba(71,85,105,0.9)",
          lineHeight: 1.75,
          fontSize: "0.92rem",
        }}>
          {desc}
        </Typography>

        <Box sx={{
          mt: 3, display: "flex", alignItems: "center", gap: 1,
          color: color, opacity: hovered ? 1 : 0,
          transform: hovered ? "translateX(0)" : "translateX(-8px)",
          transition: "all 0.3s",
          fontSize: "0.85rem",
          fontWeight: 600,
          letterSpacing: "0.05em",
          textTransform: "uppercase",
        }}>
          Learn more <ArrowForward sx={{ fontSize: 16 }} />
        </Box>
      </Box>
    </motion.div>
  );
};

/* ============================================================
   MAIN HOME COMPONENT
   ============================================================ */
const Home = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const isDark = theme.palette.mode === "dark";

  /* ---------- COUNTERS ---------- */
  const [counts, setCounts] = useState({ threats: 0, phishing: 0, training: 0, accuracy: 0 });
  const targets = { threats: 217000, phishing: 21700000, training: 868000, accuracy: 99.7 };
  const [startAnim, setStartAnim] = useState(false);

  useEffect(() => {
    if (!startAnim) return;
    const duration = 2200;
    const start = performance.now();
    const animate = (t) => {
      const progress = Math.min((t - start) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      const updated = {};
      Object.keys(targets).forEach((k) => {
        const val = targets[k] * ease;
        updated[k] = k === "accuracy" ? Number(val.toFixed(1)) : Math.floor(val);
      });
      setCounts(updated);
      if (progress < 1) requestAnimationFrame(animate);
    };
    requestAnimationFrame(animate);
  }, [startAnim]);

  const format = (v, k) => {
    if (k === "phishing") return (v / 1000000).toFixed(1) + "M";
    if (v >= 1000 && k !== "accuracy") return (v / 1000).toFixed(0) + "K";
    return k === "accuracy" ? v.toFixed(1) : v;
  };

  const metrics = [
    { icon: <BugReport sx={{ fontSize: 22 }} />, key: "threats", title: "Threats Detected", color: "#3B82F6", suffix: "+" },
    { icon: <Email sx={{ fontSize: 22 }} />, key: "phishing", title: "Phishing Blocked", color: "#8B5CF6", suffix: "+" },
    { icon: <School sx={{ fontSize: 22 }} />, key: "training", title: "Trainings Done", color: "#10B981", suffix: "+" },
    { icon: <TrendingUp sx={{ fontSize: 22 }} />, key: "accuracy", title: "Detection Accuracy", color: "#F59E0B", suffix: "%" },
  ];

  const features = [
    {
      icon: <Security sx={{ fontSize: 26 }} />,
      title: "Zero-Trust Architecture",
      desc: "Continuous verification of users, devices, and behaviors across your entire infrastructure with no implicit trust.",
    },
    {
      icon: <Hub sx={{ fontSize: 26 }} />,
      title: "Graph Intelligence Engine",
      desc: "Analyzes relationships between users, systems, and actions to surface hidden threat pathways before exploitation.",
    },
    {
      icon: <Public sx={{ fontSize: 26 }} />,
      title: "Cross-Platform Visibility",
      desc: "Unified monitoring across endpoints, networks, applications, and cloud services with a single pane of glass.",
    },
  ];

  return (
    <Box sx={{
      position: "relative",
      minHeight: "100vh",
      background: isDark
        ? "linear-gradient(170deg, #020817 0%, #050f2a 50%, #020817 100%)"
        : "linear-gradient(170deg, #f0f7ff 0%, #e8f0fe 50%, #f0f7ff 100%)",
      fontFamily: "'Outfit', sans-serif",
    }}>
      <GridCanvas isDark={isDark} />

      {/* Ambient orbs */}
      <Box sx={{
        position: "fixed", top: "15%", left: "8%",
        width: 500, height: 500,
        background: isDark
          ? "radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%)"
          : "radial-gradient(circle, rgba(59,130,246,0.08) 0%, transparent 70%)",
        filter: "blur(60px)", zIndex: 0, pointerEvents: "none",
      }} />
      <Box sx={{
        position: "fixed", bottom: "20%", right: "5%",
        width: 400, height: 400,
        background: isDark
          ? "radial-gradient(circle, rgba(139,92,246,0.1) 0%, transparent 70%)"
          : "radial-gradient(circle, rgba(139,92,246,0.06) 0%, transparent 70%)",
        filter: "blur(60px)", zIndex: 0, pointerEvents: "none",
      }} />

      {/* ===== HERO ===== */}
      <Box sx={{ position: "relative", zIndex: 1 }}>
        <Container maxWidth="lg" sx={{ pt: { xs: 8, md: 10 }, pb: { xs: 4, md: 5 } }}>
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            <CyberBadge>
              <Box sx={{ width: 6, height: 6, borderRadius: "50%", bgcolor: "#22C55E", boxShadow: "0 0 6px #22C55E", animation: "pulse 2s infinite" }} />
              <Typography sx={{ fontSize: "0.7rem", letterSpacing: "0.2em", color: "#3B82F6", fontFamily: "'Courier New', monospace", textTransform: "uppercase" }}>
                AICDAP · Threat Detection Active
              </Typography>
            </CyberBadge>
          </motion.div>

          <Box sx={{ mt: 3, maxWidth: 820 }}>
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.25 }}
            >
              <Typography
                component="h1"
                sx={{
                  fontSize: { xs: "2.6rem", md: "4rem", lg: "4.8rem" },
                  fontWeight: 900,
                  lineHeight: 1.0,
                  letterSpacing: "-0.02em",
                  fontFamily: "'Outfit', sans-serif",
                  color: isDark ? "#E2E8F0" : "#0F172A",
                  mb: 0.5,
                }}
              >
                Secure Your
                <Box component="span" sx={{
                  display: "block",
                  background: "linear-gradient(135deg, #3B82F6 0%, #60A5FA 40%, #2563EB 100%)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                  backgroundClip: "text",
                  filter: "drop-shadow(0 0 28px rgba(59,130,246,0.45))",
                }}>
                  Enterprise
                </Box>
              </Typography>
              <Typography
                component="h1"
                sx={{
                  fontSize: { xs: "2.6rem", md: "4rem", lg: "4.8rem" },
                  fontWeight: 900,
                  lineHeight: 1.0,
                  letterSpacing: "-0.02em",
                  fontFamily: "'Outfit', sans-serif",
                  background: "linear-gradient(135deg, #F97316 0%, #EF4444 100%)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                  backgroundClip: "text",
                  filter: "drop-shadow(0 0 28px rgba(249,115,22,0.4))",
                  mb: 0,
                }}
              >
                From Within
              </Typography>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.45 }}
            >
              <Typography sx={{
                mt: 3, mb: 4,
                fontSize: { xs: "0.95rem", md: "1.05rem" },
                color: isDark ? "rgba(148,163,184,0.9)" : "rgba(71,85,105,0.9)",
                maxWidth: 520,
                lineHeight: 1.75,
                borderLeft: "2px solid rgba(59,130,246,0.5)",
                pl: 2,
              }}>
                Detect insider threats before they become breaches using behavioral analytics, graph intelligence, and AI-driven anomaly detection.
              </Typography>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.6 }}
            >
              <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap", alignItems: "center" }}>
                <Button
                  variant="contained"
                  size="large"
                  startIcon={<PlayArrow />}
                  onClick={() => navigate("/admin/dashboard")}
                  sx={{
                    px: 4, py: 1.4,
                    fontSize: "0.9rem",
                    fontWeight: 700,
                    textTransform: "none",
                    letterSpacing: "0.02em",
                    fontFamily: "'Outfit', sans-serif",
                    borderRadius: "3px",
                    background: "linear-gradient(135deg, #2563EB, #3B82F6)",
                    border: "1px solid rgba(59,130,246,0.5)",
                    boxShadow: "0 0 30px rgba(59,130,246,0.35), 0 4px 16px rgba(0,0,0,0.2)",
                    "&:hover": {
                      background: "linear-gradient(135deg, #1D4ED8, #2563EB)",
                      boxShadow: "0 0 50px rgba(59,130,246,0.5), 0 8px 24px rgba(0,0,0,0.25)",
                      transform: "translateY(-2px)",
                    },
                    transition: "all 0.3s",
                  }}
                >
                  Detect Insider Threats
                </Button>

                <Button
                  variant="outlined"
                  size="large"
                  endIcon={<ArrowForward />}
                  onClick={() => navigate("/admin/insider")}
                  sx={{
                    px: 4, py: 1.4,
                    fontSize: "0.9rem",
                    fontWeight: 600,
                    textTransform: "none",
                    letterSpacing: "0.02em",
                    fontFamily: "'Outfit', sans-serif",
                    borderRadius: "3px",
                    borderColor: isDark ? "rgba(59,130,246,0.4)" : "rgba(37,99,235,0.5)",
                    color: isDark ? "#93C5FD" : "#2563EB",
                    "&:hover": {
                      borderColor: "#3B82F6",
                      background: "rgba(59,130,246,0.1)",
                      transform: "translateY(-2px)",
                    },
                    transition: "all 0.3s",
                  }}
                >
                  Insider Analysis
                </Button>
              </Box>

              <Box sx={{ mt: 2.5, display: "flex", gap: 3, flexWrap: "wrap" }}>
                {["Enterprise Ready", "Real-time Detection", "99.7% Accuracy"].map((tag, i) => (
                  <Box key={i} sx={{ display: "flex", alignItems: "center", gap: 0.75 }}>
                    <CheckCircle sx={{ color: "#22C55E", fontSize: 16 }} />
                    <Typography sx={{ fontSize: "0.82rem", color: isDark ? "rgba(148,163,184,0.8)" : "rgba(71,85,105,0.8)", fontWeight: 500 }}>
                      {tag}
                    </Typography>
                  </Box>
                ))}
              </Box>
            </motion.div>
          </Box>
        </Container>
      </Box>

      {/* ===== DIVIDER ===== */}
      <Box sx={{ position: "relative", zIndex: 1, py: 2 }}>
        <Container maxWidth="lg">
          <Box sx={{
            height: "1px",
            background: isDark
              ? "linear-gradient(90deg, transparent, rgba(59,130,246,0.3) 30%, rgba(59,130,246,0.3) 70%, transparent)"
              : "linear-gradient(90deg, transparent, rgba(37,99,235,0.2) 30%, rgba(37,99,235,0.2) 70%, transparent)",
          }} />
        </Container>
      </Box>

      {/* ===== METRICS ===== */}
      <Box sx={{ position: "relative", zIndex: 1, py: { xs: 6, md: 8 } }}>
        <Container maxWidth="lg">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            onViewportEnter={() => setStartAnim(true)}
          >
            <Box sx={{ display: "flex", alignItems: "center", gap: 2, mb: 1 }}>
              <Box sx={{ height: 2, width: 32, bgcolor: "#3B82F6" }} />
              <Typography sx={{ fontSize: "0.7rem", letterSpacing: "0.2em", color: "#3B82F6", fontFamily: "'Courier New', monospace", textTransform: "uppercase" }}>
                Real-time Impact
              </Typography>
            </Box>
            <Typography variant="h3" sx={{
              fontWeight: 800,
              mb: 1,
              fontFamily: "'Outfit', sans-serif",
              color: isDark ? "#E2E8F0" : "#0F172A",
              letterSpacing: "-0.02em",
            }}>
              Security at Scale
            </Typography>
            <Typography sx={{
              mb: 5,
              color: isDark ? "rgba(148,163,184,0.75)" : "rgba(71,85,105,0.8)",
              maxWidth: 500,
              lineHeight: 1.7,
            }}>
              Live metrics from our platform protecting enterprises worldwide.
            </Typography>
          </motion.div>

          <Grid container spacing={3}>
            {metrics.map((m, i) => (
              <Grid item xs={12} sm={6} md={3} key={i}>
                <motion.div
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: i * 0.1 }}
                  viewport={{ once: true }}
                >
                  <StatCard
                    icon={m.icon}
                    value={format(counts[m.key], m.key)}
                    suffix={m.suffix}
                    title={m.title}
                    color={m.color}
                    isDark={isDark}
                  />
                </motion.div>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* ===== ALERT BANNER ===== */}
      <Box sx={{ position: "relative", zIndex: 1, py: { xs: 6, md: 10 } }}>
        <Container maxWidth="md">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            viewport={{ once: true }}
          >
            <Box sx={{
              position: "relative",
              p: { xs: 5, md: 8 },
              borderRadius: "4px",
              background: isDark
                ? "linear-gradient(135deg, rgba(37,99,235,0.12) 0%, rgba(139,92,246,0.1) 100%)"
                : "linear-gradient(135deg, rgba(37,99,235,0.08) 0%, rgba(139,92,246,0.06) 100%)",
              border: isDark
                ? "1px solid rgba(59,130,246,0.25)"
                : "1px solid rgba(37,99,235,0.2)",
              backdropFilter: "blur(20px)",
              overflow: "hidden",
              boxShadow: isDark
                ? "0 0 60px rgba(59,130,246,0.1), 0 16px 48px rgba(0,0,0,0.2)"
                : "0 0 40px rgba(37,99,235,0.08), 0 16px 48px rgba(0,0,0,0.06)",
            }}>
              {/* Corner accents */}
              {[{t:0,l:0},{t:0,r:0},{b:0,l:0},{b:0,r:0}].map((pos, i) => (
                <Box key={i} sx={{
                  position: "absolute",
                  ...pos,
                  width: 24, height: 24,
                  borderTop: pos.t === 0 ? "2px solid #3B82F6" : "none",
                  borderBottom: pos.b === 0 ? "2px solid #3B82F6" : "none",
                  borderLeft: pos.l === 0 ? "2px solid #3B82F6" : "none",
                  borderRight: pos.r === 0 ? "2px solid #3B82F6" : "none",
                }} />
              ))}

              {/* Background glow */}
              <Box sx={{
                position: "absolute", top: -80, right: -80,
                width: 300, height: 300,
                background: "radial-gradient(circle, rgba(139,92,246,0.12), transparent 70%)",
                filter: "blur(40px)",
              }} />

              <Box sx={{ position: "relative", textAlign: "center" }}>
                <Box sx={{
                  width: 64, height: 64,
                  display: "flex", alignItems: "center", justifyContent: "center",
                  background: "rgba(59,130,246,0.12)",
                  border: "1px solid rgba(59,130,246,0.3)",
                  borderRadius: "4px",
                  mx: "auto", mb: 3,
                  color: "#3B82F6",
                  fontSize: 32,
                }}>
                  <Shield sx={{ fontSize: 32 }} />
                </Box>

                <Typography variant="h4" sx={{
                  mb: 2, fontWeight: 800,
                  fontFamily: "'Outfit', sans-serif",
                  letterSpacing: "-0.02em",
                  color: isDark ? "#F1F5F9" : "#0F172A",
                }}>
                  Insider Threats Cause Most Security Incidents
                </Typography>

                <Typography sx={{
                  mb: 5,
                  color: isDark ? "rgba(148,163,184,0.85)" : "rgba(71,85,105,0.85)",
                  fontSize: "1.05rem",
                  lineHeight: 1.8,
                  maxWidth: 560,
                  mx: "auto",
                }}>
                  AICDAP continuously monitors behavioral signals across systems, detecting anomalies that traditional security tools miss.
                </Typography>

                <Button
                  variant="contained"
                  size="large"
                  endIcon={<ArrowForward />}
                  sx={{
                    px: 5, py: 1.6,
                    fontSize: "0.95rem",
                    fontWeight: 700,
                    textTransform: "none",
                    fontFamily: "'Outfit', sans-serif",
                    borderRadius: "3px",
                    background: "linear-gradient(135deg, #2563EB, #4F46E5)",
                    boxShadow: "0 0 30px rgba(59,130,246,0.4)",
                    "&:hover": {
                      background: "linear-gradient(135deg, #1D4ED8, #4338CA)",
                      boxShadow: "0 0 50px rgba(59,130,246,0.55)",
                      transform: "translateY(-2px)",
                    },
                    transition: "all 0.3s",
                  }}
                >
                  Analyze Insider Risk
                </Button>
              </Box>
            </Box>
          </motion.div>
        </Container>
      </Box>

      {/* ===== FEATURES ===== */}
      <Box sx={{ position: "relative", zIndex: 1, py: { xs: 6, md: 8 }, pb: { xs: 14, md: 18 } }}>
        <Container maxWidth="lg">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <Box sx={{ display: "flex", alignItems: "center", gap: 2, mb: 1 }}>
              <Box sx={{ height: 2, width: 32, bgcolor: "#8B5CF6" }} />
              <Typography sx={{ fontSize: "0.7rem", letterSpacing: "0.2em", color: "#8B5CF6", fontFamily: "'Courier New', monospace", textTransform: "uppercase" }}>
                Platform Capabilities
              </Typography>
            </Box>
            <Typography variant="h3" sx={{
              fontWeight: 800,
              mb: 1,
              fontFamily: "'Outfit', sans-serif",
              color: isDark ? "#E2E8F0" : "#0F172A",
              letterSpacing: "-0.02em",
            }}>
              Built for Enterprise Security
            </Typography>
            <Typography sx={{
              mb: 5,
              color: isDark ? "rgba(148,163,184,0.75)" : "rgba(71,85,105,0.8)",
              maxWidth: 460,
              lineHeight: 1.7,
            }}>
              Comprehensive protection across your entire digital infrastructure.
            </Typography>
          </motion.div>

          <Grid container spacing={3}>
            {features.map((f, i) => (
              <Grid item xs={12} md={4} key={i} sx={{ display: "flex" }}>
                <FeatureCard {...f} index={i} isDark={isDark} />
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* CSS for pulse animation */}
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&display=swap');
        @keyframes pulse {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.6; transform: scale(0.85); }
        }
      `}</style>
    </Box>
  );
};

export default Home;