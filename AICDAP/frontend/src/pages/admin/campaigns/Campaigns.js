import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Chip,
  Avatar,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  LinearProgress,
  Menu,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  Alert,
  Skeleton,
  Snackbar,
  useTheme,
  alpha,
} from "@mui/material";
import {
  Add,
  Email,
  Visibility,
  MoreVert,
  PlayArrow,
  Pause,
  Stop,
  Delete,
  TrendingUp,
  Security,
  CheckCircle,
} from "@mui/icons-material";
import { useNavigate } from "react-router-dom";
import { CampaignService } from "../../../services/campaignService";

const Campaigns = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const isDark = theme.palette.mode === "dark";

  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedCampaign, setSelectedCampaign] = useState(null);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState({
    total: 0,
    active: 0,
    completed: 0,
    thisMonth: 0,
  });
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "success",
  });

  // Load campaigns on component mount
  useEffect(() => {
    loadCampaigns();
    loadStats();
  }, []);

  const loadCampaigns = async () => {
    try {
      setLoading(true);
      setError(null);
      const { data, error } = await CampaignService.getAllCampaigns();
      if (error) {
        setError(`Error loading campaigns: ${error}`);
      } else {
        setCampaigns(data || []);
      }
    } catch (error) {
      setError("Unexpected error loading campaigns");
      console.error("Error loading campaigns:", error);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const { data, error } = await CampaignService.getCampaignStats();
      if (!error && data) {
        setStats({
          total: data.total,
          active: data.active,
          completed: data.completed,
          thisMonth: data.thisMonth,
        });
      }
    } catch (error) {
      console.error("Error loading stats:", error);
    }
  };

  // Calculate overview stats from real data
  const totalCampaigns = stats.total;
  const activeCampaigns = stats.active;
  const totalTargets = campaigns.reduce(
    (sum, c) => sum + (c.total_targets || 0),
    0,
  );
  const averageClickRate =
    campaigns.length > 0 && totalTargets > 0
      ? Math.round(
          (campaigns.reduce((sum, c) => sum + (c.total_clicked || 0), 0) /
            totalTargets) *
            100,
        )
      : 0;

  const handleMenuOpen = (event, campaign) => {
    setAnchorEl(event.currentTarget);
    setSelectedCampaign(campaign);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedCampaign(null);
  };

  const handleDeleteCampaign = async () => {
    if (!selectedCampaign) return;

    try {
      const { error } = await CampaignService.deleteCampaign(
        selectedCampaign.id,
      );
      if (error) {
        setSnackbar({
          open: true,
          message: `Error deleting campaign: ${error}`,
          severity: "error",
        });
      } else {
        setCampaigns(campaigns.filter((c) => c.id !== selectedCampaign.id));
        setSnackbar({
          open: true,
          message: "Campaign deleted successfully",
          severity: "success",
        });
        loadStats(); // Refresh stats
      }
    } catch (error) {
      setSnackbar({
        open: true,
        message: "Unexpected error deleting campaign",
        severity: "error",
      });
    } finally {
      setShowDeleteDialog(false);
      handleMenuClose();
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "active":
        return "success";
      case "completed":
        return "primary";
      case "paused":
        return "warning";
      case "draft":
        return "default";
      default:
        return "default";
    }
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case "Low":
        return "success";
      case "Medium":
        return "warning";
      case "High":
        return "error";
      default:
        return "primary";
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case "active":
        return <PlayArrow />;
      case "completed":
        return <CheckCircle />;
      case "paused":
        return <Pause />;
      case "draft":
        return <Email />;
      default:
        return <Email />;
    }
  };

  return (
    <Box>
      {/* Header */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 4,
          flexWrap: "wrap",
          gap: 2,
        }}
      >
        <Box>
          <Typography 
            variant="h4" 
            component="h1" 
            gutterBottom
            sx={{ 
              fontWeight: 700,
              color: theme.palette.text.primary,
            }}
          >
            Campaign Management
          </Typography>
          <Typography 
            variant="body1" 
            sx={{ 
              color: theme.palette.text.secondary,
              maxWidth: 600,
            }}
          >
            Create, monitor, and analyze your phishing simulation campaigns
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => navigate("/admin/campaigns/create")}
          sx={{
            background: isDark
              ? "linear-gradient(135deg, #f38020 0%, #d4650b 100%)"
              : "linear-gradient(135deg, #f38020 0%, #d4650b 100%)",
            boxShadow: "0 4px 14px 0 rgba(243, 128, 32, 0.4)",
            px: 3,
            py: 1.5,
            fontWeight: 600,
            textTransform: "none",
            fontSize: "1rem",
            "&:hover": {
              background: "linear-gradient(135deg, #ff9d47 0%, #f38020 100%)",
              boxShadow: "0 6px 20px 0 rgba(243, 128, 32, 0.5)",
            },
          }}
        >
          Create Campaign
        </Button>
      </Box>

      {/* Overview Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card
            elevation={isDark ? 2 : 1}
            sx={{
              background: isDark 
                ? alpha(theme.palette.background.paper, 0.6)
                : theme.palette.background.paper,
              border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
              transition: "all 0.3s ease",
              "&:hover": {
                transform: "translateY(-4px)",
                boxShadow: isDark
                  ? `0 8px 24px ${alpha(theme.palette.primary.main, 0.3)}`
                  : `0 8px 24px ${alpha(theme.palette.primary.main, 0.2)}`,
              },
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                <Avatar 
                  sx={{ 
                    bgcolor: theme.palette.primary.main, 
                    width: 56, 
                    height: 56,
                  }}
                >
                  <Email />
                </Avatar>
                <Box>
                  <Typography 
                    variant="h4"
                    sx={{ 
                      fontWeight: 700,
                      color: theme.palette.text.primary,
                      mb: 0.5,
                    }}
                  >
                    {loading ? <Skeleton width={40} /> : totalCampaigns}
                  </Typography>
                  <Typography 
                    variant="body2" 
                    sx={{ 
                      color: theme.palette.text.secondary,
                      fontWeight: 500,
                    }}
                  >
                    Total Campaigns
                  </Typography>
                </Box>
              </Box>
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
              transition: "all 0.3s ease",
              "&:hover": {
                transform: "translateY(-4px)",
                boxShadow: isDark
                  ? `0 8px 24px ${alpha(theme.palette.success.main, 0.3)}`
                  : `0 8px 24px ${alpha(theme.palette.success.main, 0.2)}`,
              },
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                <Avatar 
                  sx={{ 
                    bgcolor: theme.palette.success.main, 
                    width: 56, 
                    height: 56,
                  }}
                >
                  <PlayArrow />
                </Avatar>
                <Box>
                  <Typography 
                    variant="h4"
                    sx={{ 
                      fontWeight: 700,
                      color: theme.palette.text.primary,
                      mb: 0.5,
                    }}
                  >
                    {loading ? <Skeleton width={40} /> : activeCampaigns}
                  </Typography>
                  <Typography 
                    variant="body2" 
                    sx={{ 
                      color: theme.palette.text.secondary,
                      fontWeight: 500,
                    }}
                  >
                    Active Campaigns
                  </Typography>
                </Box>
              </Box>
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
              transition: "all 0.3s ease",
              "&:hover": {
                transform: "translateY(-4px)",
                boxShadow: isDark
                  ? `0 8px 24px ${alpha(theme.palette.secondary.main, 0.3)}`
                  : `0 8px 24px ${alpha(theme.palette.secondary.main, 0.2)}`,
              },
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                <Avatar 
                  sx={{ 
                    bgcolor: theme.palette.secondary.main, 
                    width: 56, 
                    height: 56,
                  }}
                >
                  <Security />
                </Avatar>
                <Box>
                  <Typography 
                    variant="h4"
                    sx={{ 
                      fontWeight: 700,
                      color: theme.palette.text.primary,
                      mb: 0.5,
                    }}
                  >
                    {loading ? (
                      <Skeleton width={60} />
                    ) : (
                      totalTargets.toLocaleString()
                    )}
                  </Typography>
                  <Typography 
                    variant="body2" 
                    sx={{ 
                      color: theme.palette.text.secondary,
                      fontWeight: 500,
                    }}
                  >
                    Total Targets
                  </Typography>
                </Box>
              </Box>
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
              transition: "all 0.3s ease",
              "&:hover": {
                transform: "translateY(-4px)",
                boxShadow: isDark
                  ? `0 8px 24px ${alpha(theme.palette.warning.main, 0.3)}`
                  : `0 8px 24px ${alpha(theme.palette.warning.main, 0.2)}`,
              },
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                <Avatar 
                  sx={{ 
                    bgcolor: theme.palette.warning.main, 
                    width: 56, 
                    height: 56,
                  }}
                >
                  <TrendingUp />
                </Avatar>
                <Box>
                  <Typography 
                    variant="h4"
                    sx={{ 
                      fontWeight: 700,
                      color: theme.palette.text.primary,
                      mb: 0.5,
                    }}
                  >
                    {loading ? <Skeleton width={50} /> : `${averageClickRate}%`}
                  </Typography>
                  <Typography 
                    variant="body2" 
                    sx={{ 
                      color: theme.palette.text.secondary,
                      fontWeight: 500,
                    }}
                  >
                    Avg Click Rate
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Campaigns Table */}
      <Paper 
        elevation={isDark ? 2 : 1}
        sx={{ 
          background: isDark 
            ? alpha(theme.palette.background.paper, 0.6)
            : theme.palette.background.paper,
          backdropFilter: "blur(10px)",
          border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
        }}
      >
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell 
                  sx={{ 
                    fontWeight: 700, 
                    color: theme.palette.text.primary,
                    textTransform: "uppercase",
                    letterSpacing: 0.5,
                    fontSize: "0.75rem",
                  }}
                >
                  Campaign
                </TableCell>
                <TableCell 
                  sx={{ 
                    fontWeight: 700, 
                    color: theme.palette.text.primary,
                    textTransform: "uppercase",
                    letterSpacing: 0.5,
                    fontSize: "0.75rem",
                  }}
                >
                  Template
                </TableCell>
                <TableCell 
                  sx={{ 
                    fontWeight: 700, 
                    color: theme.palette.text.primary,
                    textTransform: "uppercase",
                    letterSpacing: 0.5,
                    fontSize: "0.75rem",
                  }}
                >
                  Status
                </TableCell>
                <TableCell 
                  sx={{ 
                    fontWeight: 700, 
                    color: theme.palette.text.primary,
                    textTransform: "uppercase",
                    letterSpacing: 0.5,
                    fontSize: "0.75rem",
                  }}
                >
                  Progress
                </TableCell>
                <TableCell 
                  sx={{ 
                    fontWeight: 700, 
                    color: theme.palette.text.primary,
                    textTransform: "uppercase",
                    letterSpacing: 0.5,
                    fontSize: "0.75rem",
                  }}
                >
                  Targets
                </TableCell>
                <TableCell 
                  sx={{ 
                    fontWeight: 700, 
                    color: theme.palette.text.primary,
                    textTransform: "uppercase",
                    letterSpacing: 0.5,
                    fontSize: "0.75rem",
                  }}
                >
                  Clicked
                </TableCell>
                <TableCell 
                  sx={{ 
                    fontWeight: 700, 
                    color: theme.palette.text.primary,
                    textTransform: "uppercase",
                    letterSpacing: 0.5,
                    fontSize: "0.75rem",
                  }}
                >
                  Reported
                </TableCell>
                <TableCell 
                  sx={{ 
                    fontWeight: 700, 
                    color: theme.palette.text.primary,
                    textTransform: "uppercase",
                    letterSpacing: 0.5,
                    fontSize: "0.75rem",
                  }}
                >
                  Created
                </TableCell>
                <TableCell 
                  align="right"
                  sx={{ 
                    fontWeight: 700, 
                    color: theme.palette.text.primary,
                    textTransform: "uppercase",
                    letterSpacing: 0.5,
                    fontSize: "0.75rem",
                  }}
                >
                  Actions
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading ? (
                Array.from({ length: 3 }).map((_, index) => (
                  <TableRow key={index}>
                    {Array.from({ length: 9 }).map((_, colIndex) => (
                      <TableCell key={colIndex}>
                        <Skeleton variant="text" />
                      </TableCell>
                    ))}
                  </TableRow>
                ))
              ) : campaigns.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={9} sx={{ textAlign: "center", py: 6 }}>
                    {error ? (
                      <Alert
                        severity="error"
                        sx={{ maxWidth: 500, mx: "auto" }}
                      >
                        {error}
                        <Button 
                          onClick={loadCampaigns} 
                          sx={{ 
                            ml: 2,
                            textTransform: "none",
                            fontWeight: 600,
                          }}
                        >
                          Retry
                        </Button>
                      </Alert>
                    ) : (
                      <Box>
                        <Email 
                          sx={{ 
                            fontSize: 64, 
                            color: theme.palette.text.secondary,
                            mb: 2,
                            opacity: 0.5,
                          }} 
                        />
                        <Typography
                          variant="h6"
                          sx={{ 
                            color: theme.palette.text.primary,
                            fontWeight: 600,
                            mb: 1,
                          }}
                        >
                          No campaigns found
                        </Typography>
                        <Typography
                          variant="body2"
                          sx={{ 
                            color: theme.palette.text.secondary,
                            mb: 3,
                          }}
                        >
                          Get started by creating your first phishing simulation campaign
                        </Typography>
                        <Button
                          variant="contained"
                          startIcon={<Add />}
                          onClick={() => navigate("/admin/campaigns/create")}
                          sx={{
                            textTransform: "none",
                            fontWeight: 600,
                            px: 3,
                          }}
                        >
                          Create Your First Campaign
                        </Button>
                      </Box>
                    )}
                  </TableCell>
                </TableRow>
              ) : (
                campaigns.map((campaign) => {
                  const progress =
                    campaign.total_targets > 0
                      ? Math.round(
                          (campaign.total_sent / campaign.total_targets) * 100,
                        )
                      : 0;

                  return (
                    <TableRow 
                      key={campaign.id} 
                      hover
                      sx={{
                        "&:hover": {
                          backgroundColor: isDark
                            ? alpha('#fff', 0.05)
                            : alpha('#000', 0.04),
                        },
                      }}
                    >
                      <TableCell>
                        <Box>
                          <Typography 
                            variant="subtitle2" 
                            gutterBottom
                            sx={{ 
                              fontWeight: 600,
                              color: theme.palette.text.primary,
                            }}
                          >
                            {campaign.name}
                          </Typography>
                          {campaign.template_name && (
                            <Chip
                              label={campaign.template_name}
                              size="small"
                              color="primary"
                              variant="outlined"
                              sx={{ fontWeight: 500 }}
                            />
                          )}
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Typography 
                          variant="body2"
                          sx={{ 
                            color: theme.palette.text.secondary,
                            fontWeight: 500,
                          }}
                        >
                          {campaign.template_name || "Custom Template"}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          icon={getStatusIcon(campaign.status)}
                          label={
                            campaign.status.charAt(0).toUpperCase() +
                            campaign.status.slice(1)
                          }
                          color={getStatusColor(campaign.status)}
                          variant="outlined"
                          size="small"
                          sx={{ fontWeight: 600 }}
                        />
                      </TableCell>
                      <TableCell>
                        <Box sx={{ width: 120 }}>
                          <LinearProgress
                            variant="determinate"
                            value={progress}
                            sx={{ 
                              mb: 0.5, 
                              height: 8, 
                              borderRadius: 1,
                            }}
                          />
                          <Typography 
                            variant="caption" 
                            sx={{ 
                              color: theme.palette.text.secondary,
                              fontWeight: 600,
                            }}
                          >
                            {progress}%
                          </Typography>
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Typography 
                          variant="body2"
                          sx={{ 
                            color: theme.palette.text.primary,
                            fontWeight: 600,
                          }}
                        >
                          {campaign.total_targets || 0}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Box>
                          <Typography
                            variant="body2"
                            sx={{
                              color: (campaign.total_clicked || 0) > 0
                                ? theme.palette.warning.main
                                : theme.palette.text.primary,
                              fontWeight: 600,
                            }}
                          >
                            {campaign.total_clicked || 0}
                          </Typography>
                          <Typography 
                            variant="caption" 
                            sx={{ 
                              color: theme.palette.text.secondary,
                              fontWeight: 500,
                            }}
                          >
                            {campaign.total_targets > 0
                              ? Math.round(
                                  ((campaign.total_clicked || 0) /
                                    campaign.total_targets) *
                                    100,
                                )
                              : 0}
                            %
                          </Typography>
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Box>
                          <Typography
                            variant="body2"
                            sx={{
                              color: (campaign.total_reported || 0) > 0
                                ? theme.palette.success.main
                                : theme.palette.text.primary,
                              fontWeight: 600,
                            }}
                          >
                            {campaign.total_reported || 0}
                          </Typography>
                          <Typography 
                            variant="caption" 
                            sx={{ 
                              color: theme.palette.text.secondary,
                              fontWeight: 500,
                            }}
                          >
                            {campaign.total_targets > 0
                              ? Math.round(
                                  ((campaign.total_reported || 0) /
                                    campaign.total_targets) *
                                    100,
                                )
                              : 0}
                            %
                          </Typography>
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Typography 
                          variant="body2" 
                          sx={{ 
                            color: theme.palette.text.secondary,
                            fontWeight: 500,
                          }}
                        >
                          {campaign.created_at
                            ? new Date(campaign.created_at).toLocaleDateString()
                            : "N/A"}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <IconButton
                          size="small"
                          onClick={(e) => handleMenuOpen(e, campaign)}
                          sx={{
                            color: theme.palette.text.secondary,
                            "&:hover": {
                              backgroundColor: isDark
                                ? alpha('#fff', 0.1)
                                : alpha('#000', 0.08),
                            },
                          }}
                        >
                          <MoreVert />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  );
                })
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Action Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
        PaperProps={{
          sx: {
            background: isDark 
              ? alpha(theme.palette.background.paper, 0.95)
              : theme.palette.background.paper,
            backdropFilter: "blur(10px)",
          }
        }}
      >
        <MenuItem
          onClick={() => navigate(`/admin/campaigns/${selectedCampaign?.id}`)}
          sx={{
            color: theme.palette.text.primary,
            fontWeight: 500,
            "&:hover": {
              backgroundColor: isDark
                ? alpha('#fff', 0.1)
                : alpha('#000', 0.08),
            },
          }}
        >
          <Visibility sx={{ mr: 1, fontSize: 20 }} /> View Details
        </MenuItem>
        {selectedCampaign?.status === "active" && (
          <MenuItem 
            onClick={handleMenuClose}
            sx={{
              color: theme.palette.text.primary,
              fontWeight: 500,
              "&:hover": {
                backgroundColor: isDark
                  ? alpha('#fff', 0.1)
                  : alpha('#000', 0.08),
              },
            }}
          >
            <Pause sx={{ mr: 1, fontSize: 20 }} /> Pause Campaign
          </MenuItem>
        )}
        {selectedCampaign?.status === "paused" && (
          <MenuItem 
            onClick={handleMenuClose}
            sx={{
              color: theme.palette.text.primary,
              fontWeight: 500,
              "&:hover": {
                backgroundColor: isDark
                  ? alpha('#fff', 0.1)
                  : alpha('#000', 0.08),
              },
            }}
          >
            <PlayArrow sx={{ mr: 1, fontSize: 20 }} /> Resume Campaign
          </MenuItem>
        )}
        {(selectedCampaign?.status === "active" ||
          selectedCampaign?.status === "paused") && (
          <MenuItem 
            onClick={handleMenuClose}
            sx={{
              color: theme.palette.text.primary,
              fontWeight: 500,
              "&:hover": {
                backgroundColor: isDark
                  ? alpha('#fff', 0.1)
                  : alpha('#000', 0.08),
              },
            }}
          >
            <Stop sx={{ mr: 1, fontSize: 20 }} /> Stop Campaign
          </MenuItem>
        )}
        <MenuItem
          onClick={() => {
            handleMenuClose();
            setShowDeleteDialog(true);
          }}
          sx={{ 
            color: theme.palette.error.main,
            fontWeight: 500,
            "&:hover": {
              backgroundColor: alpha(theme.palette.error.main, 0.1),
            },
          }}
        >
          <Delete sx={{ mr: 1, fontSize: 20 }} /> Delete Campaign
        </MenuItem>
      </Menu>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={showDeleteDialog}
        onClose={() => setShowDeleteDialog(false)}
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
          Delete Campaign
        </DialogTitle>
        <DialogContent>
          <Typography
            sx={{ 
              color: theme.palette.text.secondary,
              lineHeight: 1.7,
            }}
          >
            Are you sure you want to delete the campaign "<strong>{selectedCampaign?.name}</strong>"? 
            This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button 
            onClick={() => setShowDeleteDialog(false)}
            sx={{
              textTransform: "none",
              fontWeight: 600,
            }}
          >
            Cancel
          </Button>
          <Button
            color="error"
            variant="contained"
            onClick={handleDeleteCampaign}
            sx={{
              textTransform: "none",
              fontWeight: 600,
            }}
          >
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert
          severity={snackbar.severity}
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          sx={{
            backgroundColor: isDark 
              ? alpha(theme.palette.background.paper, 0.95)
              : theme.palette.background.paper,
          }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Campaigns;