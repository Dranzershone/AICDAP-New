import React, { useState } from "react";
import { 
  Box, 
  Typography, 
  Grid, 
  Paper, 
  useTheme, 
  alpha,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import CampaignLineChart from "../../components/CampaignLineChart";
import { 
  Dashboard as DashboardIcon,
  Campaign,
  Newspaper,
  TrendingUp,
  Add,
} from "@mui/icons-material";

const Dashboard = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const isDark = theme.palette.mode === "dark";
  const [selectedCampaign, setSelectedCampaign] = useState("");

  // Sample campaigns - replace with your actual data
  const campaigns = [
    { id: 1, name: "Campaign 17/02/2026 - Canva Team Invitation Phishing" },
    { id: 2, name: "Campaign 17/02/2026 - Instagram Copyright Violation Notice" },
    { id: 3, name: "Campaign 17/02/2026 - Google Login Phishing" },
    { id: 4, name: "Campaign 17/02/2026 - AWS Billing Suspension Phishing" },
    { id: 5, name: "Campaign 17/02/2026 - Twitter/X Account Lock Alert" },
    { id: 6, name: "Campaign 17/02/2026 - GitHub Security Alert" },
  ];

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
          <DashboardIcon 
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
            Dashboard
          </Typography>
        </Box>
        <Typography 
          variant="body1" 
          sx={{ 
            color: theme.palette.text.secondary,
            ml: 7,
          }}
        >
          Welcome to the AICDAP admin panel. Manage your security awareness campaigns from here.
        </Typography>
      </Box>

      {/* Main Dashboard Content */}
      <Grid container spacing={3}>
        {/* Last Campaign Card */}
        <Grid item xs={12} md={6}>
          <Paper
            elevation={isDark ? 2 : 1}
            sx={{
              p: 4,
              minHeight: 300,
              textAlign: "center",
              background: isDark
                ? `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.2)} 0%, ${alpha(theme.palette.primary.main, 0.05)} 100%)`
                : `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.1)} 0%, ${alpha(theme.palette.primary.main, 0.03)} 100%)`,
              border: `2px solid ${isDark ? alpha(theme.palette.primary.main, 0.3) : alpha(theme.palette.primary.main, 0.2)}`,
              borderRadius: 2,
              cursor: "pointer",
              transition: "all 0.3s ease",
              backdropFilter: "blur(10px)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              "&:hover": {
                transform: "translateY(-8px)",
                boxShadow: isDark
                  ? `0 12px 32px ${alpha(theme.palette.primary.main, 0.4)}`
                  : `0 12px 32px ${alpha(theme.palette.primary.main, 0.3)}`,
                borderColor: theme.palette.primary.main,
                background: isDark
                  ? `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.25)} 0%, ${alpha(theme.palette.primary.main, 0.1)} 100%)`
                  : `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.15)} 0%, ${alpha(theme.palette.primary.main, 0.05)} 100%)`,
              },
            }}
            onClick={() => navigate("/admin/campaigns/create")}
          >
            <Box
              sx={{
                width: 80,
                height: 80,
                borderRadius: "50%",
                backgroundColor: isDark
                  ? alpha(theme.palette.primary.main, 0.2)
                  : alpha(theme.palette.primary.main, 0.1),
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                mb: 3,
                transition: "all 0.3s ease",
              }}
            >
              <Add 
                sx={{ 
                  fontSize: 48, 
                  color: theme.palette.primary.main,
                }} 
              />
            </Box>
            <Typography 
              variant="h5" 
              gutterBottom
              sx={{ 
                fontWeight: 600,
                color: theme.palette.text.primary,
                mb: 1,
              }}
            >
              Create New Campaign
            </Typography>
            <Typography 
              variant="body1" 
              sx={{ 
                color: theme.palette.text.secondary,
                maxWidth: 300,
              }}
            >
              Launch a new phishing simulation campaign to test your team's security awareness
            </Typography>
          </Paper>
        </Grid>

        {/* Cybersecurity News Card */}
        <Grid item xs={12} md={6}>
          <Paper
            elevation={isDark ? 2 : 1}
            sx={{
              p: 4,
              minHeight: 300,
              textAlign: "center",
              background: isDark
                ? `linear-gradient(135deg, ${alpha(theme.palette.warning.main, 0.2)} 0%, ${alpha(theme.palette.warning.main, 0.05)} 100%)`
                : `linear-gradient(135deg, ${alpha(theme.palette.warning.main, 0.1)} 0%, ${alpha(theme.palette.warning.main, 0.03)} 100%)`,
              border: `2px solid ${isDark ? alpha(theme.palette.warning.main, 0.3) : alpha(theme.palette.warning.main, 0.2)}`,
              borderRadius: 2,
              backdropFilter: "blur(10px)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <Box
              sx={{
                width: 80,
                height: 80,
                borderRadius: "50%",
                backgroundColor: isDark
                  ? alpha(theme.palette.warning.main, 0.2)
                  : alpha(theme.palette.warning.main, 0.1),
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                mb: 3,
              }}
            >
              <Newspaper 
                sx={{ 
                  fontSize: 48, 
                  color: theme.palette.warning.main,
                }} 
              />
            </Box>
            <Typography 
              variant="h5" 
              gutterBottom
              sx={{ 
                fontWeight: 600,
                color: theme.palette.text.primary,
                mb: 1,
              }}
            >
              Latest Cybersecurity News
            </Typography>
            <Typography 
              variant="body1" 
              sx={{ 
                color: theme.palette.text.secondary,
                maxWidth: 300,
              }}
            >
              Stay updated with the latest phishing threats and security trends
            </Typography>
          </Paper>
        </Grid>

        {/* Campaign Selector */}
        <Grid item xs={12}>
          <Paper 
            elevation={isDark ? 2 : 1}
            sx={{ 
              p: 3,
              background: isDark 
                ? alpha(theme.palette.background.paper, 0.6)
                : theme.palette.background.paper,
              backdropFilter: "blur(10px)",
              border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
            }}
          >
            <FormControl fullWidth>
              <InputLabel 
                id="dashboard-campaign-select-label"
                sx={{
                  color: theme.palette.text.secondary,
                  '&.Mui-focused': {
                    color: theme.palette.primary.main,
                  },
                }}
              >
                Select Campaign
              </InputLabel>
              <Select
                labelId="dashboard-campaign-select-label"
                id="dashboard-campaign-select"
                value={selectedCampaign}
                label="Select Campaign"
                onChange={(e) => setSelectedCampaign(e.target.value)}
                sx={{
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderColor: isDark ? alpha('#fff', 0.2) : alpha('#000', 0.2),
                  },
                  '&:hover .MuiOutlinedInput-notchedOutline': {
                    borderColor: isDark ? alpha('#fff', 0.3) : alpha('#000', 0.3),
                  },
                  '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                    borderColor: theme.palette.primary.main,
                  },
                  '& .MuiSelect-select': {
                    color: theme.palette.text.primary,
                  },
                  '& .MuiSvgIcon-root': {
                    color: theme.palette.text.secondary,
                  },
                }}
                MenuProps={{
                  PaperProps: {
                    sx: {
                      bgcolor: isDark 
                        ? theme.palette.background.paper 
                        : theme.palette.background.paper,
                      backgroundImage: 'none',
                      mt: 1,
                      boxShadow: isDark
                        ? `0 8px 24px ${alpha('#000', 0.5)}`
                        : `0 8px 24px ${alpha('#000', 0.15)}`,
                      border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
                      '& .MuiMenuItem-root': {
                        color: theme.palette.text.primary,
                        fontSize: '0.95rem',
                        py: 1.5,
                        '&:hover': {
                          backgroundColor: isDark 
                            ? alpha(theme.palette.primary.main, 0.15)
                            : alpha(theme.palette.primary.main, 0.08),
                        },
                        '&.Mui-selected': {
                          backgroundColor: isDark 
                            ? alpha(theme.palette.primary.main, 0.25)
                            : alpha(theme.palette.primary.main, 0.12),
                          '&:hover': {
                            backgroundColor: isDark 
                              ? alpha(theme.palette.primary.main, 0.3)
                              : alpha(theme.palette.primary.main, 0.15),
                          },
                        },
                      },
                    },
                  },
                }}
              >
                <MenuItem value="">
                  <em style={{ color: theme.palette.text.secondary }}>Select a campaign</em>
                </MenuItem>
                {campaigns.map((campaign) => (
                  <MenuItem key={campaign.id} value={campaign.id}>
                    {campaign.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Paper>
        </Grid>

        {/* Analytics Chart */}
        <Grid item xs={12}>
          <Paper
            elevation={isDark ? 2 : 1}
            sx={{
              p: 4,
              minHeight: 400,
              background: isDark 
                ? alpha(theme.palette.background.paper, 0.6)
                : theme.palette.background.paper,
              backdropFilter: "blur(10px)",
              border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
            }}
          >
            <Box sx={{ display: "flex", alignItems: "center", mb: 3 }}>
              <TrendingUp 
                sx={{ 
                  mr: 1.5, 
                  fontSize: 28,
                  color: theme.palette.primary.main,
                }} 
              />
              <Typography 
                variant="h6"
                sx={{ 
                  fontWeight: 600,
                  color: theme.palette.text.primary,
                }}
              >
                Campaign Performance Overview
              </Typography>
            </Box>
            <CampaignLineChart />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;