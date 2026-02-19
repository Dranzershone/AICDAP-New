import React, { useState, useEffect } from "react";
import {
  Box,
  Container,
  Typography,
  Paper,
  Button,
  Alert,
  CircularProgress,
  Grid,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Tab,
  Tabs,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  IconButton,
  Tooltip,
  useTheme,
  alpha,
} from "@mui/material";
import {
  Security,
  Warning,
  Person,
  Computer,
  Language,
  PlayArrow,
  Stop,
  Refresh,
  ExpandMore,
  Info,
  TrendingUp,
  NetworkCheck,
  Timeline,
  Visibility,
  VisibilityOff,
} from "@mui/icons-material";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip as ChartTooltip,
  Legend,
} from "chart.js";

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  ChartTooltip,
  Legend,
);

const InsiderThreat = () => {
  const theme = useTheme();
  const isDark = theme.palette.mode === "dark";

  const [loading, setLoading] = useState(false);
  const [analysisData, setAnalysisData] = useState(null);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("ready");
  const [selectedTab, setSelectedTab] = useState(0);
  const [showGraphDetails, setShowGraphDetails] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [usersPage, setUsersPage] = useState(0);
  const [usersPerPage] = useState(25);
  const [showOnlyMalicious, setShowOnlyMalicious] = useState(false);

  const handleScan = async () => {
    setLoading(true);
    setError("");
    setAnalysisData(null);
    setStatus("scanning");

    try {
      const response = await fetch(
        "http://localhost:8000/api/insider-threat/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        },
      );

      if (!response.ok) {
        throw new Error("Failed to run insider threat analysis");
      }

      const result = await response.json();

      if (result.success) {
        setAnalysisData(result.data);
        setStatus("completed");
      } else {
        throw new Error(result.message || "Analysis failed");
      }
    } catch (err) {
      setError(err.message || "An error occurred during analysis");
      setStatus("error");
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (score) => {
    if (score >= 0.8) return "error";
    if (score >= 0.6) return "warning";
    if (score >= 0.4) return "info";
    return "success";
  };

  const getRiskLevel = (score) => {
    if (score >= 0.8) return "HIGH";
    if (score >= 0.6) return "MEDIUM";
    if (score >= 0.4) return "LOW-MEDIUM";
    return "LOW";
  };

  const formatScore = (score) => (score * 100).toFixed(1);

  const getNodeTypeIcon = (type) => {
    switch (type) {
      case "user":
        return <Person />;
      case "pc":
        return <Computer />;
      case "domain":
        return <Language />;
      default:
        return <NetworkCheck />;
    }
  };

  const trainingLossChart = analysisData?.training_losses
    ? {
        labels: analysisData.training_losses.map((_, i) => `Epoch ${i + 1}`),
        datasets: [
          {
            label: "Training Loss",
            data: analysisData.training_losses,
            borderColor: theme.palette.primary.main,
            backgroundColor: alpha(theme.palette.primary.main, 0.1),
            borderWidth: 2,
            fill: true,
            tension: 0.4,
          },
        ],
      }
    : null;

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top",
        labels: {
          color: theme.palette.text.primary,
          font: {
            size: 12,
            weight: 600,
          },
        },
      },
      title: {
        display: true,
        text: "Model Training Progress",
        color: theme.palette.text.primary,
        font: {
          size: 16,
          weight: 600,
        },
      },
      tooltip: {
        backgroundColor: isDark ? alpha('#000', 0.9) : alpha('#fff', 0.9),
        titleColor: theme.palette.text.primary,
        bodyColor: theme.palette.text.primary,
        borderColor: theme.palette.divider,
        borderWidth: 1,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: "Loss",
          color: theme.palette.text.secondary,
          font: {
            size: 12,
            weight: 600,
          },
        },
        ticks: {
          color: theme.palette.text.secondary,
        },
        grid: {
          color: isDark ? alpha('#fff', 0.1) : alpha('#000', 0.1),
        },
      },
      x: {
        ticks: {
          color: theme.palette.text.secondary,
        },
        grid: {
          color: isDark ? alpha('#fff', 0.1) : alpha('#000', 0.1),
        },
      },
    },
  };

  const TabPanel = ({ children, value, index, ...other }) => (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
          <Security 
            sx={{ 
              mr: 2, 
              fontSize: 40,
              color: theme.palette.primary.main,
            }} 
          />
          <Typography 
            variant="h4" 
            component="h1"
            sx={{ 
              fontWeight: 700,
              color: theme.palette.text.primary,
            }}
          >
            Insider Threat Detection
          </Typography>
        </Box>
        <Typography 
          variant="subtitle1" 
          sx={{ 
            color: theme.palette.text.secondary,
            ml: 7,
          }}
        >
          AI-powered graph neural network analysis for detecting insider threats
        </Typography>
      </Box>

      {/* Control Panel */}
      <Paper 
        elevation={isDark ? 2 : 1}
        sx={{ 
          p: 4, 
          mb: 3,
          background: isDark 
            ? alpha(theme.palette.background.paper, 0.6)
            : theme.palette.background.paper,
          backdropFilter: "blur(10px)",
          border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
        }}
      >
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={4}>
            <Button
              fullWidth
              variant="contained"
              onClick={handleScan}
              disabled={loading}
              startIcon={
                loading ? <CircularProgress size={20} color="inherit" /> : <PlayArrow />
              }
              sx={{ 
                py: 1.8,
                fontWeight: 600,
                textTransform: "none",
                fontSize: "1rem",
              }}
            >
              {loading ? "Analyzing..." : "Start Analysis"}
            </Button>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: "center" }}>
              <Typography 
                variant="caption" 
                sx={{ 
                  color: theme.palette.text.secondary,
                  textTransform: "uppercase",
                  letterSpacing: 0.5,
                  fontWeight: 600,
                  display: "block",
                  mb: 1,
                }}
              >
                Status
              </Typography>
              <Chip
                label={status.charAt(0).toUpperCase() + status.slice(1)}
                color={
                  status === "completed"
                    ? "success"
                    : status === "error"
                      ? "error"
                      : "default"
                }
                icon={
                  status === "scanning" ? (
                    <CircularProgress size={16} color="inherit" />
                  ) : (
                    <Security />
                  )
                }
                sx={{ fontWeight: 600 }}
              />
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: "center" }}>
              <Typography 
                variant="caption" 
                sx={{ 
                  color: theme.palette.text.secondary,
                  textTransform: "uppercase",
                  letterSpacing: 0.5,
                  fontWeight: 600,
                  display: "block",
                  mb: 1,
                }}
              >
                Last Analysis
              </Typography>
              <Typography 
                variant="body1"
                sx={{ 
                  color: theme.palette.text.primary,
                  fontWeight: 600,
                }}
              >
                {analysisData?.analysis_date || "Never"}
              </Typography>
            </Box>
          </Grid>
        </Grid>

        {loading && (
          <Box sx={{ mt: 3 }}>
            <LinearProgress />
            <Typography 
              variant="body2" 
              sx={{ 
                mt: 1.5, 
                textAlign: "center",
                color: theme.palette.text.secondary,
              }}
            >
              Building graph, training model, and analyzing threats...
            </Typography>
          </Box>
        )}

        {error && (
          <Alert severity="error" sx={{ mt: 3 }}>
            {error}
          </Alert>
        )}
      </Paper>

      {/* Analysis Results */}
      {analysisData && (
        <Box>
          <Box 
            sx={{ 
              borderBottom: 1, 
              borderColor: isDark 
                ? alpha('#fff', 0.1)
                : 'divider', 
              mb: 3,
            }}
          >
            <Tabs
              value={selectedTab}
              onChange={(e, newValue) => setSelectedTab(newValue)}
              sx={{
                '& .MuiTab-root': {
                  textTransform: "none",
                  fontWeight: 600,
                  fontSize: "0.95rem",
                  minHeight: 64,
                  color: theme.palette.text.secondary,
                  '&.Mui-selected': {
                    color: theme.palette.primary.main,
                  },
                },
              }}
            >
              <Tab label="Threat Overview" icon={<Warning />} iconPosition="start" />
              <Tab label="Suspicious Users" icon={<Person />} iconPosition="start" />
              <Tab label="Graph Analysis" icon={<NetworkCheck />} iconPosition="start" />
              <Tab label="Training Metrics" icon={<Timeline />} iconPosition="start" />
            </Tabs>
          </Box>

          {/* Tab 0: Threat Overview */}
          <TabPanel value={selectedTab} index={0}>
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6} md={3}>
                <Card
                  elevation={isDark ? 2 : 1}
                  sx={{
                    background: isDark 
                      ? alpha(theme.palette.background.paper, 0.6)
                      : theme.palette.background.paper,
                    border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
                  }}
                >
                  <CardContent sx={{ textAlign: "center", p: 3 }}>
                    <Typography 
                      variant="h3" 
                      sx={{ 
                        color: theme.palette.primary.main,
                        fontWeight: 700,
                        mb: 1,
                      }}
                    >
                      {analysisData.summary?.users_analyzed || 0}
                    </Typography>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: theme.palette.text.secondary,
                        fontWeight: 500,
                      }}
                    >
                      Users Analyzed
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card
                  elevation={isDark ? 2 : 1}
                  sx={{
                    background: isDark 
                      ? alpha(theme.palette.background.paper, 0.6)
                      : theme.palette.background.paper,
                    border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
                  }}
                >
                  <CardContent sx={{ textAlign: "center", p: 3 }}>
                    <Typography 
                      variant="h3" 
                      sx={{ 
                        color: theme.palette.warning.main,
                        fontWeight: 700,
                        mb: 1,
                      }}
                    >
                      {analysisData.suspicious_users?.length || 0}
                    </Typography>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: theme.palette.text.secondary,
                        fontWeight: 500,
                      }}
                    >
                      Suspicious Users
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card
                  elevation={isDark ? 2 : 1}
                  sx={{
                    background: isDark 
                      ? alpha(theme.palette.background.paper, 0.6)
                      : theme.palette.background.paper,
                    border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
                  }}
                >
                  <CardContent sx={{ textAlign: "center", p: 3 }}>
                    <Typography 
                      variant="h3" 
                      sx={{ 
                        color: theme.palette.error.main,
                        fontWeight: 700,
                        mb: 1,
                      }}
                    >
                      {analysisData.summary?.known_malicious || 0}
                    </Typography>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: theme.palette.text.secondary,
                        fontWeight: 500,
                      }}
                    >
                      Known Threats
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card
                  elevation={isDark ? 2 : 1}
                  sx={{
                    background: isDark 
                      ? alpha(theme.palette.background.paper, 0.6)
                      : theme.palette.background.paper,
                    border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
                  }}
                >
                  <CardContent sx={{ textAlign: "center", p: 3 }}>
                    <Typography 
                      variant="h3" 
                      sx={{ 
                        color: theme.palette.info.main,
                        fontWeight: 700,
                        mb: 1,
                      }}
                    >
                      {analysisData.summary?.total_nodes || 0}
                    </Typography>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: theme.palette.text.secondary,
                        fontWeight: 500,
                      }}
                    >
                      Network Nodes
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12}>
                <Card
                  elevation={isDark ? 2 : 1}
                  sx={{
                    background: isDark 
                      ? alpha(theme.palette.background.paper, 0.6)
                      : theme.palette.background.paper,
                    border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
                  }}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Typography 
                      variant="h6" 
                      gutterBottom
                      sx={{ 
                        fontWeight: 600,
                        color: theme.palette.text.primary,
                        mb: 2,
                      }}
                    >
                      Analysis Summary
                    </Typography>
                    <Box sx={{ display: "flex", flexDirection: "column", gap: 1.5 }}>
                      <Box>
                        <Typography 
                          variant="caption" 
                          sx={{ 
                            color: theme.palette.text.secondary,
                            textTransform: "uppercase",
                            letterSpacing: 0.5,
                            fontWeight: 600,
                          }}
                        >
                          Analysis Date
                        </Typography>
                        <Typography 
                          variant="body1"
                          sx={{ 
                            color: theme.palette.text.primary,
                            fontWeight: 500,
                            mt: 0.5,
                          }}
                        >
                          {analysisData.analysis_date}
                        </Typography>
                      </Box>
                      <Divider />
                      <Box>
                        <Typography 
                          variant="caption" 
                          sx={{ 
                            color: theme.palette.text.secondary,
                            textTransform: "uppercase",
                            letterSpacing: 0.5,
                            fontWeight: 600,
                          }}
                        >
                          Network Size
                        </Typography>
                        <Typography 
                          variant="body1"
                          sx={{ 
                            color: theme.palette.text.primary,
                            fontWeight: 500,
                            mt: 0.5,
                          }}
                        >
                          {analysisData.summary?.total_nodes} nodes, {analysisData.summary?.total_edges} edges
                        </Typography>
                      </Box>
                      <Divider />
                      <Box>
                        <Typography 
                          variant="caption" 
                          sx={{ 
                            color: theme.palette.text.secondary,
                            textTransform: "uppercase",
                            letterSpacing: 0.5,
                            fontWeight: 600,
                          }}
                        >
                          Detection Method
                        </Typography>
                        <Typography 
                          variant="body1"
                          sx={{ 
                            color: theme.palette.text.primary,
                            fontWeight: 500,
                            mt: 0.5,
                          }}
                        >
                          Graph Neural Network (GraphSAGE)
                        </Typography>
                      </Box>
                      <Divider />
                      <Box>
                        <Typography 
                          variant="body2"
                          sx={{ 
                            color: theme.palette.text.secondary,
                            lineHeight: 1.7,
                            mt: 1,
                          }}
                        >
                          The system analyzed user behavior patterns, network connections, and identified 
                          potential insider threats based on anomalous activity patterns.
                        </Typography>
                      </Box>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </TabPanel>

          {/* Tab 1: Suspicious Users */}
          <TabPanel value={selectedTab} index={1}>
            <Card
              elevation={isDark ? 2 : 1}
              sx={{
                background: isDark 
                  ? alpha(theme.palette.background.paper, 0.6)
                  : theme.palette.background.paper,
                border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
              }}
            >
              <CardContent sx={{ p: 3 }}>
                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    mb: 3,
                    flexWrap: "wrap",
                    gap: 2,
                  }}
                >
                  <Typography 
                    variant="h6"
                    sx={{ 
                      fontWeight: 600,
                      color: theme.palette.text.primary,
                    }}
                  >
                    All Suspicious Users ({analysisData.suspicious_users?.length || 0})
                  </Typography>
                  <Box sx={{ display: "flex", gap: 2, alignItems: "center" }}>
                    <Button
                      variant={showOnlyMalicious ? "contained" : "outlined"}
                      color="error"
                      size="small"
                      onClick={() => setShowOnlyMalicious(!showOnlyMalicious)}
                      sx={{
                        textTransform: "none",
                        fontWeight: 600,
                      }}
                    >
                      {showOnlyMalicious ? "Show All" : "Show Only Malicious"}
                    </Button>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: theme.palette.text.secondary,
                      }}
                    >
                      Showing{" "}
                      {
                        (
                          (showOnlyMalicious
                            ? analysisData.suspicious_users?.filter(
                                (u) => u.is_known_malicious,
                              )
                            : analysisData.suspicious_users) || []
                        ).slice(
                          usersPage * usersPerPage,
                          (usersPage + 1) * usersPerPage,
                        ).length
                      }{" "}
                      of{" "}
                      {(showOnlyMalicious
                        ? analysisData.suspicious_users?.filter(
                            (u) => u.is_known_malicious,
                          )
                        : analysisData.suspicious_users
                      )?.length || 0}
                    </Typography>
                  </Box>
                </Box>
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell sx={{ fontWeight: 600, color: theme.palette.text.primary }}>#</TableCell>
                        <TableCell sx={{ fontWeight: 600, color: theme.palette.text.primary }}>User</TableCell>
                        <TableCell sx={{ fontWeight: 600, color: theme.palette.text.primary }}>Threat Score</TableCell>
                        <TableCell sx={{ fontWeight: 600, color: theme.palette.text.primary }}>Risk Level</TableCell>
                        <TableCell sx={{ fontWeight: 600, color: theme.palette.text.primary }}>Known Threat</TableCell>
                        <TableCell sx={{ fontWeight: 600, color: theme.palette.text.primary }}>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {(
                        (showOnlyMalicious
                          ? analysisData.suspicious_users?.filter(
                              (u) => u.is_known_malicious,
                            )
                          : analysisData.suspicious_users) || []
                      )
                        .slice(
                          usersPage * usersPerPage,
                          (usersPage + 1) * usersPerPage,
                        )
                        .map((user, index) => (
                          <TableRow
                            key={index}
                            hover
                            sx={{
                              backgroundColor: user.is_known_malicious
                                ? isDark 
                                  ? alpha(theme.palette.error.main, 0.15)
                                  : alpha(theme.palette.error.main, 0.08)
                                : "inherit",
                              "&:hover": {
                                backgroundColor: user.is_known_malicious
                                  ? isDark 
                                    ? alpha(theme.palette.error.main, 0.25)
                                    : alpha(theme.palette.error.main, 0.12)
                                  : isDark
                                    ? alpha('#fff', 0.05)
                                    : alpha('#000', 0.04),
                              },
                            }}
                          >
                            <TableCell>
                              <Typography
                                variant="body2"
                                sx={{
                                  fontWeight: user.is_known_malicious ? 700 : 500,
                                  color: theme.palette.text.primary,
                                }}
                              >
                                {usersPage * usersPerPage + index + 1}
                              </Typography>
                            </TableCell>
                            <TableCell>
                              <Box
                                sx={{ display: "flex", alignItems: "center" }}
                              >
                                <Person
                                  sx={{
                                    mr: 1,
                                    color: user.is_known_malicious
                                      ? theme.palette.error.main
                                      : theme.palette.text.secondary,
                                  }}
                                />
                                <Typography
                                  variant="body2"
                                  sx={{
                                    fontWeight: user.is_known_malicious ? 700 : 500,
                                    color: theme.palette.text.primary,
                                  }}
                                >
                                  {user.user}
                                </Typography>
                                {user.is_known_malicious && (
                                  <Warning
                                    sx={{
                                      ml: 1,
                                      color: theme.palette.error.main,
                                      fontSize: 18,
                                    }}
                                  />
                                )}
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Box
                                sx={{ display: "flex", alignItems: "center", gap: 1 }}
                              >
                                <Box sx={{ width: "100px" }}>
                                  <LinearProgress
                                    variant="determinate"
                                    value={user.score * 100}
                                    color={getRiskColor(user.score)}
                                    sx={{ height: 8, borderRadius: 1 }}
                                  />
                                </Box>
                                <Typography
                                  variant="body2"
                                  sx={{
                                    fontWeight: user.is_known_malicious ? 700 : 600,
                                    color: theme.palette.text.primary,
                                    minWidth: 50,
                                  }}
                                >
                                  {formatScore(user.score)}%
                                </Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Chip
                                label={getRiskLevel(user.score)}
                                color={getRiskColor(user.score)}
                                size="small"
                                variant={
                                  user.is_known_malicious
                                    ? "filled"
                                    : "outlined"
                                }
                                sx={{ fontWeight: 600 }}
                              />
                            </TableCell>
                            <TableCell>
                              <Chip
                                label={
                                  user.is_known_malicious
                                    ? "CONFIRMED THREAT"
                                    : "Benign"
                                }
                                color={
                                  user.is_known_malicious ? "error" : "success"
                                }
                                size="small"
                                variant={
                                  user.is_known_malicious
                                    ? "filled"
                                    : "outlined"
                                }
                                sx={{ fontWeight: 600 }}
                              />
                            </TableCell>
                            <TableCell>
                              <Tooltip title="View Details">
                                <IconButton
                                  size="small"
                                  onClick={() => setSelectedUser(user)}
                                  sx={{
                                    color: theme.palette.primary.main,
                                  }}
                                >
                                  <Info />
                                </IconButton>
                              </Tooltip>
                            </TableCell>
                          </TableRow>
                        ))}
                    </TableBody>
                  </Table>
                </TableContainer>

                {/* Pagination */}
                <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", mt: 3, gap: 2 }}>
                  <Button
                    disabled={usersPage === 0}
                    onClick={() => setUsersPage(usersPage - 1)}
                    variant="outlined"
                    size="small"
                    sx={{ textTransform: "none", fontWeight: 600 }}
                  >
                    Previous
                  </Button>
                  <Typography 
                    sx={{ 
                      color: theme.palette.text.primary,
                      fontWeight: 600,
                    }}
                  >
                    Page {usersPage + 1} of{" "}
                    {Math.ceil(
                      ((showOnlyMalicious
                        ? analysisData.suspicious_users?.filter(
                            (u) => u.is_known_malicious,
                          )
                        : analysisData.suspicious_users
                      )?.length || 0) / usersPerPage,
                    ) || 1}
                  </Typography>
                  <Button
                    disabled={
                      (usersPage + 1) * usersPerPage >=
                      ((showOnlyMalicious
                        ? analysisData.suspicious_users?.filter(
                            (u) => u.is_known_malicious,
                          )
                        : analysisData.suspicious_users
                      )?.length || 0)
                    }
                    onClick={() => setUsersPage(usersPage + 1)}
                    variant="outlined"
                    size="small"
                    sx={{ textTransform: "none", fontWeight: 600 }}
                  >
                    Next
                  </Button>
                </Box>

                {/* Summary Statistics */}
                <Box
                  sx={{
                    mt: 4,
                    p: 3,
                    bgcolor: isDark 
                      ? alpha('#fff', 0.05)
                      : alpha('#000', 0.02),
                    borderRadius: 2,
                    border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
                  }}
                >
                  <Typography 
                    variant="subtitle2" 
                    gutterBottom
                    sx={{ 
                      fontWeight: 600,
                      color: theme.palette.text.primary,
                      mb: 2,
                    }}
                  >
                    Detection Summary
                  </Typography>
                  <Grid container spacing={3}>
                    <Grid item xs={6} sm={3}>
                      <Typography 
                        variant="caption" 
                        sx={{ 
                          color: theme.palette.text.secondary,
                          textTransform: "uppercase",
                          letterSpacing: 0.5,
                          fontWeight: 600,
                        }}
                      >
                        Total Users Analyzed
                      </Typography>
                      <Typography 
                        variant="h5"
                        sx={{ 
                          color: theme.palette.text.primary,
                          fontWeight: 700,
                          mt: 0.5,
                        }}
                      >
                        {analysisData.suspicious_users?.length || 0}
                      </Typography>
                    </Grid>
                    <Grid item xs={6} sm={3}>
                      <Typography 
                        variant="caption" 
                        sx={{ 
                          color: theme.palette.text.secondary,
                          textTransform: "uppercase",
                          letterSpacing: 0.5,
                          fontWeight: 600,
                        }}
                      >
                        Known Malicious
                      </Typography>
                      <Typography 
                        variant="h5" 
                        sx={{ 
                          color: theme.palette.error.main,
                          fontWeight: 700,
                          mt: 0.5,
                        }}
                      >
                        {analysisData.suspicious_users?.filter(
                          (u) => u.is_known_malicious,
                        ).length || 0}
                      </Typography>
                    </Grid>
                    <Grid item xs={6} sm={3}>
                      <Typography 
                        variant="caption" 
                        sx={{ 
                          color: theme.palette.text.secondary,
                          textTransform: "uppercase",
                          letterSpacing: 0.5,
                          fontWeight: 600,
                        }}
                      >
                        High Risk (&gt;80%)
                      </Typography>
                      <Typography 
                        variant="h5" 
                        sx={{ 
                          color: theme.palette.warning.main,
                          fontWeight: 700,
                          mt: 0.5,
                        }}
                      >
                        {analysisData.suspicious_users?.filter(
                          (u) => u.score >= 0.8,
                        ).length || 0}
                      </Typography>
                    </Grid>
                    <Grid item xs={6} sm={3}>
                      <Typography 
                        variant="caption" 
                        sx={{ 
                          color: theme.palette.text.secondary,
                          textTransform: "uppercase",
                          letterSpacing: 0.5,
                          fontWeight: 600,
                        }}
                      >
                        Detection Accuracy
                      </Typography>
                      <Typography 
                        variant="h5" 
                        sx={{ 
                          color: theme.palette.success.main,
                          fontWeight: 700,
                          mt: 0.5,
                        }}
                      >
                        {analysisData.suspicious_users?.filter(
                          (u) => u.is_known_malicious,
                        ).length > 0
                          ? "✓"
                          : "N/A"}
                      </Typography>
                    </Grid>
                  </Grid>
                </Box>
              </CardContent>
            </Card>
          </TabPanel>

          {/* Tab 2: Graph Analysis */}
          <TabPanel value={selectedTab} index={2}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Card
                  elevation={isDark ? 2 : 1}
                  sx={{
                    background: isDark 
                      ? alpha(theme.palette.background.paper, 0.6)
                      : theme.palette.background.paper,
                    border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
                  }}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Typography 
                      variant="h6" 
                      gutterBottom
                      sx={{ 
                        fontWeight: 600,
                        color: theme.palette.text.primary,
                        mb: 2,
                      }}
                    >
                      Network Statistics
                    </Typography>
                    <List>
                      <ListItem sx={{ px: 0 }}>
                        <ListItemIcon sx={{ minWidth: 40 }}>
                          <NetworkCheck sx={{ color: theme.palette.primary.main }} />
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Typography 
                              variant="body2"
                              sx={{ 
                                fontWeight: 500,
                                color: theme.palette.text.primary,
                              }}
                            >
                              Total Nodes
                            </Typography>
                          }
                          secondary={
                            <Typography 
                              variant="h6"
                              sx={{ 
                                fontWeight: 700,
                                color: theme.palette.text.primary,
                              }}
                            >
                              {analysisData.graph_data?.stats?.total_nodes || 0}
                            </Typography>
                          }
                        />
                      </ListItem>
                      <Divider />
                      <ListItem sx={{ px: 0 }}>
                        <ListItemIcon sx={{ minWidth: 40 }}>
                          <Timeline sx={{ color: theme.palette.info.main }} />
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Typography 
                              variant="body2"
                              sx={{ 
                                fontWeight: 500,
                                color: theme.palette.text.primary,
                              }}
                            >
                              Total Edges
                            </Typography>
                          }
                          secondary={
                            <Typography 
                              variant="h6"
                              sx={{ 
                                fontWeight: 700,
                                color: theme.palette.text.primary,
                              }}
                            >
                              {analysisData.graph_data?.stats?.total_edges || 0}
                            </Typography>
                          }
                        />
                      </ListItem>
                      <Divider />
                      <ListItem sx={{ px: 0 }}>
                        <ListItemIcon sx={{ minWidth: 40 }}>
                          <Warning sx={{ color: theme.palette.error.main }} />
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Typography 
                              variant="body2"
                              sx={{ 
                                fontWeight: 500,
                                color: theme.palette.text.primary,
                              }}
                            >
                              Malicious Users
                            </Typography>
                          }
                          secondary={
                            <Typography 
                              variant="h6"
                              sx={{ 
                                fontWeight: 700,
                                color: theme.palette.text.primary,
                              }}
                            >
                              {analysisData.graph_data?.stats?.malicious_users || 0}
                            </Typography>
                          }
                        />
                      </ListItem>
                    </List>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={6}>
                <Card
                  elevation={isDark ? 2 : 1}
                  sx={{
                    background: isDark 
                      ? alpha(theme.palette.background.paper, 0.6)
                      : theme.palette.background.paper,
                    border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
                  }}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Typography 
                      variant="h6" 
                      gutterBottom
                      sx={{ 
                        fontWeight: 600,
                        color: theme.palette.text.primary,
                        mb: 2,
                      }}
                    >
                      Node Distribution
                    </Typography>
                    {analysisData.graph_data?.nodes && (
                      <Box>
                        {["user", "pc", "domain"].map((type) => {
                          const count = analysisData.graph_data.nodes.filter(
                            (n) => n.type === type,
                          ).length;
                          return (
                            <Box key={type} sx={{ mb: 2 }}>
                              <Box
                                sx={{
                                  display: "flex",
                                  alignItems: "center",
                                  justifyContent: "space-between",
                                  mb: 1,
                                }}
                              >
                                <Box sx={{ display: "flex", alignItems: "center" }}>
                                  {getNodeTypeIcon(type)}
                                  <Typography
                                    variant="body2"
                                    sx={{ 
                                      ml: 1, 
                                      textTransform: "capitalize",
                                      fontWeight: 500,
                                      color: theme.palette.text.primary,
                                    }}
                                  >
                                    {type}s
                                  </Typography>
                                </Box>
                                <Typography
                                  variant="h6"
                                  sx={{ 
                                    fontWeight: 700,
                                    color: theme.palette.text.primary,
                                  }}
                                >
                                  {count}
                                </Typography>
                              </Box>
                              <LinearProgress
                                variant="determinate"
                                value={(count / (analysisData.graph_data?.nodes?.length || 1)) * 100}
                                sx={{ 
                                  height: 6, 
                                  borderRadius: 1,
                                  backgroundColor: isDark 
                                    ? alpha('#fff', 0.1)
                                    : alpha('#000', 0.1),
                                }}
                              />
                            </Box>
                          );
                        })}
                      </Box>
                    )}
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12}>
                <Accordion
                  sx={{
                    background: isDark 
                      ? alpha(theme.palette.background.paper, 0.6)
                      : theme.palette.background.paper,
                    border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
                  }}
                >
                  <AccordionSummary 
                    expandIcon={<ExpandMore />}
                    sx={{
                      '& .MuiAccordionSummary-content': {
                        my: 1.5,
                      },
                    }}
                  >
                    <Typography 
                      variant="h6"
                      sx={{ 
                        fontWeight: 600,
                        color: theme.palette.text.primary,
                      }}
                    >
                      Graph Nodes Details
                    </Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    {analysisData.graph_data?.nodes && (
                      <TableContainer>
                        <Table size="small">
                          <TableHead>
                            <TableRow>
                              <TableCell sx={{ fontWeight: 600, color: theme.palette.text.primary }}>Node ID</TableCell>
                              <TableCell sx={{ fontWeight: 600, color: theme.palette.text.primary }}>Type</TableCell>
                              <TableCell sx={{ fontWeight: 600, color: theme.palette.text.primary }}>Degree</TableCell>
                              <TableCell sx={{ fontWeight: 600, color: theme.palette.text.primary }}>Malicious</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {analysisData.graph_data.nodes
                              .slice(0, 20)
                              .map((node, index) => (
                                <TableRow 
                                  key={index}
                                  hover
                                  sx={{
                                    '&:hover': {
                                      backgroundColor: isDark
                                        ? alpha('#fff', 0.05)
                                        : alpha('#000', 0.04),
                                    },
                                  }}
                                >
                                  <TableCell>
                                    <Typography 
                                      variant="body2"
                                      sx={{ 
                                        color: theme.palette.text.primary,
                                        fontFamily: "monospace",
                                      }}
                                    >
                                      {node.id}
                                    </Typography>
                                  </TableCell>
                                  <TableCell>
                                    <Chip
                                      icon={getNodeTypeIcon(node.type)}
                                      label={node.type}
                                      size="small"
                                      variant="outlined"
                                      sx={{ fontWeight: 500 }}
                                    />
                                  </TableCell>
                                  <TableCell>
                                    <Typography 
                                      variant="body2"
                                      sx={{ 
                                        color: theme.palette.text.primary,
                                        fontWeight: 600,
                                      }}
                                    >
                                      {node.degree}
                                    </Typography>
                                  </TableCell>
                                  <TableCell>
                                    <Chip
                                      label={node.is_malicious ? "Yes" : "No"}
                                      color={
                                        node.is_malicious ? "error" : "success"
                                      }
                                      size="small"
                                      sx={{ fontWeight: 600 }}
                                    />
                                  </TableCell>
                                </TableRow>
                              ))}
                          </TableBody>
                        </Table>
                      </TableContainer>
                    )}
                    {analysisData.graph_data?.nodes?.length > 20 && (
                      <Typography
                        variant="body2"
                        sx={{ 
                          mt: 2, 
                          textAlign: "center",
                          color: theme.palette.text.secondary,
                        }}
                      >
                        Showing first 20 nodes out of {analysisData.graph_data.nodes.length} total
                      </Typography>
                    )}
                  </AccordionDetails>
                </Accordion>
              </Grid>
            </Grid>
          </TabPanel>

          {/* Tab 3: Training Metrics */}
          <TabPanel value={selectedTab} index={3}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Card
                  elevation={isDark ? 2 : 1}
                  sx={{
                    background: isDark 
                      ? alpha(theme.palette.background.paper, 0.6)
                      : theme.palette.background.paper,
                    border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
                  }}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Typography 
                      variant="h6" 
                      gutterBottom
                      sx={{ 
                        fontWeight: 600,
                        color: theme.palette.text.primary,
                        mb: 3,
                      }}
                    >
                      Model Training Progress
                    </Typography>
                    {trainingLossChart && (
                      <Box sx={{ height: 400 }}>
                        <Line data={trainingLossChart} options={chartOptions} />
                      </Box>
                    )}
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={6}>
                <Card
                  elevation={isDark ? 2 : 1}
                  sx={{
                    background: isDark 
                      ? alpha(theme.palette.background.paper, 0.6)
                      : theme.palette.background.paper,
                    border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
                  }}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Typography 
                      variant="h6" 
                      gutterBottom
                      sx={{ 
                        fontWeight: 600,
                        color: theme.palette.text.primary,
                        mb: 2,
                      }}
                    >
                      Model Configuration
                    </Typography>
                    <List>
                      {[
                        { label: "Architecture", value: "GraphSAGE" },
                        { label: "Hidden Dimensions", value: "32 → 16 → 1" },
                        { label: "Activation", value: "ReLU" },
                        { label: "Loss Function", value: "Binary Cross Entropy" },
                        { label: "Optimizer", value: "Adam (lr=0.005)" },
                      ].map((item, index) => (
                        <React.Fragment key={index}>
                          <ListItem sx={{ px: 0, py: 1.5 }}>
                            <ListItemText
                              primary={
                                <Typography 
                                  variant="body2"
                                  sx={{ 
                                    fontWeight: 500,
                                    color: theme.palette.text.secondary,
                                  }}
                                >
                                  {item.label}
                                </Typography>
                              }
                              secondary={
                                <Typography 
                                  variant="body1"
                                  sx={{ 
                                    fontWeight: 600,
                                    color: theme.palette.text.primary,
                                  }}
                                >
                                  {item.value}
                                </Typography>
                              }
                            />
                          </ListItem>
                          {index < 4 && <Divider />}
                        </React.Fragment>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={6}>
                <Card
                  elevation={isDark ? 2 : 1}
                  sx={{
                    background: isDark 
                      ? alpha(theme.palette.background.paper, 0.6)
                      : theme.palette.background.paper,
                    border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
                  }}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Typography 
                      variant="h6" 
                      gutterBottom
                      sx={{ 
                        fontWeight: 600,
                        color: theme.palette.text.primary,
                        mb: 2,
                      }}
                    >
                      Training Statistics
                    </Typography>
                    <List>
                      {[
                        { 
                          label: "Training Epochs", 
                          value: analysisData.training_losses?.length || 0 
                        },
                        { 
                          label: "Final Loss", 
                          value: analysisData.training_losses?.length
                            ? analysisData.training_losses[
                                analysisData.training_losses.length - 1
                              ].toFixed(4)
                            : "N/A"
                        },
                        { 
                          label: "Initial Loss", 
                          value: analysisData.training_losses?.length
                            ? analysisData.training_losses[0].toFixed(4)
                            : "N/A"
                        },
                      ].map((item, index) => (
                        <React.Fragment key={index}>
                          <ListItem sx={{ px: 0, py: 1.5 }}>
                            <ListItemText
                              primary={
                                <Typography 
                                  variant="body2"
                                  sx={{ 
                                    fontWeight: 500,
                                    color: theme.palette.text.secondary,
                                  }}
                                >
                                  {item.label}
                                </Typography>
                              }
                              secondary={
                                <Typography 
                                  variant="body1"
                                  sx={{ 
                                    fontWeight: 600,
                                    color: theme.palette.text.primary,
                                  }}
                                >
                                  {item.value}
                                </Typography>
                              }
                            />
                          </ListItem>
                          {index < 2 && <Divider />}
                        </React.Fragment>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </TabPanel>
        </Box>
      )}

      {/* User Details Dialog */}
      <Dialog
        open={!!selectedUser}
        onClose={() => setSelectedUser(null)}
        maxWidth="sm"
        fullWidth
        PaperProps={{
          sx: {
            background: isDark 
              ? alpha(theme.palette.background.paper, 0.95)
              : theme.palette.background.paper,
            backdropFilter: "blur(10px)",
          }
        }}
      >
        <DialogTitle 
          sx={{ 
            fontWeight: 600,
            color: theme.palette.text.primary,
          }}
        >
          User Threat Details: {selectedUser?.user}
        </DialogTitle>
        <DialogContent>
          {selectedUser && (
            <Grid container spacing={3} sx={{ mt: 0.5 }}>
              <Grid item xs={12} sm={6}>
                <Typography 
                  variant="caption" 
                  sx={{ 
                    color: theme.palette.text.secondary,
                    textTransform: "uppercase",
                    letterSpacing: 0.5,
                    fontWeight: 600,
                  }}
                >
                  Threat Score
                </Typography>
                <Typography
                  variant="h3"
                  sx={{
                    color: theme.palette[getRiskColor(selectedUser.score)].main,
                    fontWeight: 700,
                    mt: 0.5,
                  }}
                >
                  {formatScore(selectedUser.score)}%
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography 
                  variant="caption" 
                  sx={{ 
                    color: theme.palette.text.secondary,
                    textTransform: "uppercase",
                    letterSpacing: 0.5,
                    fontWeight: 600,
                  }}
                >
                  Risk Level
                </Typography>
                <Box sx={{ mt: 1 }}>
                  <Chip
                    label={getRiskLevel(selectedUser.score)}
                    color={getRiskColor(selectedUser.score)}
                    sx={{ fontWeight: 600, fontSize: "0.875rem" }}
                  />
                </Box>
              </Grid>
              <Grid item xs={12}>
                <Typography 
                  variant="caption" 
                  sx={{ 
                    color: theme.palette.text.secondary,
                    textTransform: "uppercase",
                    letterSpacing: 0.5,
                    fontWeight: 600,
                  }}
                >
                  Known Threat Status
                </Typography>
                <Box sx={{ mt: 1 }}>
                  <Chip
                    label={
                      selectedUser.is_known_malicious
                        ? "Known Malicious User"
                        : "Unknown User"
                    }
                    color={selectedUser.is_known_malicious ? "error" : "success"}
                    sx={{ fontWeight: 600 }}
                  />
                </Box>
              </Grid>
            </Grid>
          )}
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button 
            onClick={() => setSelectedUser(null)}
            variant="contained"
            sx={{ 
              textTransform: "none",
              fontWeight: 600,
            }}
          >
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default InsiderThreat;