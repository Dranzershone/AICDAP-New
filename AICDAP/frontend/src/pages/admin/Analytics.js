import React, { useState } from "react";
import { 
  Box, 
  Typography, 
  Paper, 
  useTheme, 
  alpha,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";
import CampaignLineChart from "../../components/CampaignLineChart";
import { TrendingUp } from "@mui/icons-material";

const Analytics = () => {
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
          <TrendingUp 
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
            Campaign Analytics
          </Typography>
        </Box>
        <Typography 
          variant="body1" 
          sx={{ 
            color: theme.palette.text.secondary,
            ml: 7,
          }}
        >
          Detailed analytics of campaign performance and insights
        </Typography>
      </Box>

      {/* Campaign Selector */}
      <Paper 
        elevation={isDark ? 2 : 1}
        sx={{ 
          p: 3,
          mb: 3,
          background: isDark 
            ? alpha(theme.palette.background.paper, 0.6)
            : theme.palette.background.paper,
          backdropFilter: "blur(10px)",
          border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
        }}
      >
        <FormControl fullWidth>
          <InputLabel 
            id="campaign-select-label"
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
            labelId="campaign-select-label"
            id="campaign-select"
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

      {/* Chart Container */}
      <Paper 
        elevation={isDark ? 2 : 1}
        sx={{ 
          p: 4,
          background: isDark 
            ? alpha(theme.palette.background.paper, 0.6)
            : theme.palette.background.paper,
          backdropFilter: "blur(10px)",
          border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
        }}
      >
        <Typography 
          variant="h6" 
          gutterBottom
          sx={{ 
            fontWeight: 600,
            color: theme.palette.text.primary,
            mb: 3,
          }}
        >
          Performance Overview
        </Typography>
        <CampaignLineChart />
      </Paper>
    </Box>
  );
};

export default Analytics;