import React, { useState } from "react";
import {
  Box,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
  Divider,
  Collapse,
} from "@mui/material";
import {
  Dashboard as DashboardIcon,
  Storage as StorageIcon,
  Settings as SettingsIcon,
  Assignment as PolicyIcon,
  Transform as TransformIcon,
  CloudQueue as CloudIcon,
  PhotoCamera as SnapshotIcon,
  Security as SecurityIcon,
  SystemUpdate as UpgradeIcon,
  Analytics as AnalyticsIcon,
  GridView as PatternIcon,
  BookmarkBorder as SavedIcon,
  Dashboard as SpacesIcon,
  Assessment as ReportingIcon,
  Tune as TuneIcon,
  ExpandLess,
  ExpandMore,
} from "@mui/icons-material";

const ModernSidebar = ({ selectedSection = "Index Management" }) => {
  const [elasticsearchOpen, setElasticsearchOpen] = useState(true);
  const [kibanaOpen, setKibanaOpen] = useState(true);

  const elasticsearchItems = [
    { name: "Index Management", icon: <StorageIcon />, active: true },
    { name: "Index Lifecycle Policies", icon: <PolicyIcon /> },
    { name: "Rollup Jobs", icon: <TransformIcon /> },
    { name: "Transforms", icon: <TransformIcon /> },
    { name: "Remote Clusters", icon: <CloudIcon /> },
    { name: "Snapshot and Restore", icon: <SnapshotIcon /> },
    { name: "License Management", icon: <SecurityIcon /> },
    { name: "8.0 Upgrade Assistant", icon: <UpgradeIcon /> },
  ];

  const kibanaItems = [
    { name: "Index Patterns", icon: <PatternIcon /> },
    { name: "Saved Objects", icon: <SavedIcon /> },
    { name: "Spaces", icon: <SpacesIcon /> },
    { name: "Reporting", icon: <ReportingIcon /> },
    { name: "Advanced Settings", icon: <TuneIcon /> },
  ];

  return (
    <Box
      sx={{
        width: 280,
        height: "100vh",
        bgcolor: "grey.50",
        borderRight: "1px solid",
        borderColor: "divider",
        overflow: "auto",
      }}
    >
      {/* Header */}
      <Box
        sx={{
          p: 2,
          borderBottom: "1px solid",
          borderColor: "divider",
        }}
      >
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            mb: 1,
          }}
        >
          <Box
            sx={{
              width: 32,
              height: 32,
              bgcolor: "primary.main",
              borderRadius: 1,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              mr: 1,
            }}
          >
            <Typography
              sx={{
                color: "white",
                fontWeight: "bold",
                fontSize: "16px",
              }}
            >
              D
            </Typography>
          </Box>
        </Box>
        <Typography
          sx={{
            fontSize: "12px",
            color: "text.secondary",
            mb: 0.5,
          }}
        >
          Management / Index Management
        </Typography>
      </Box>

      {/* Navigation */}
      <List sx={{ p: 0 }}>
        {/* Elasticsearch Section */}
        <ListItem sx={{ px: 2, py: 1 }}>
          <ListItemButton
            onClick={() => setElasticsearchOpen(!elasticsearchOpen)}
            sx={{
              px: 0,
              py: 0.5,
              minHeight: "auto",
              "&:hover": { bgcolor: "transparent" },
            }}
          >
            <ListItemIcon sx={{ minWidth: 32 }}>
              <Box
                sx={{
                  width: 20,
                  height: 20,
                  bgcolor: "warning.main",
                  borderRadius: 0.5,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <Box
                  sx={{
                    width: 12,
                    height: 12,
                    bgcolor: "white",
                    borderRadius: "50%",
                  }}
                />
              </Box>
            </ListItemIcon>
            <ListItemText
              primary="Elasticsearch"
              primaryTypographyProps={{
                fontSize: "14px",
                fontWeight: 600,
                color: "text.primary",
              }}
            />
            {elasticsearchOpen ? <ExpandLess /> : <ExpandMore />}
          </ListItemButton>
        </ListItem>

        <Collapse in={elasticsearchOpen} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            {elasticsearchItems.map((item) => (
              <ListItem key={item.name} sx={{ px: 2, py: 0 }}>
                <ListItemButton
                  selected={item.name === selectedSection}
                  sx={{
                    px: 2,
                    py: 0.75,
                    borderRadius: 1,
                    mb: 0.25,
                    "&.Mui-selected": {
                      bgcolor: "rgba(243, 128, 32, 0.1)",
                      color: "primary.main",
                      "& .MuiListItemIcon-root": {
                        color: "primary.main",
                      },
                      "&:hover": {
                        bgcolor: "rgba(243, 128, 32, 0.1)",
                      },
                    },
                    "&:hover": {
                      bgcolor: "grey.100",
                    },
                  }}
                >
                  <ListItemIcon sx={{ minWidth: 32, color: "text.secondary" }}>
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText
                    primary={item.name}
                    primaryTypographyProps={{
                      fontSize: "14px",
                      fontWeight: item.active ? 500 : 400,
                    }}
                  />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Collapse>

        {/* Kibana Section */}
        <ListItem sx={{ px: 2, py: 1, mt: 1 }}>
          <ListItemButton
            onClick={() => setKibanaOpen(!kibanaOpen)}
            sx={{
              px: 0,
              py: 0.5,
              minHeight: "auto",
              "&:hover": { bgcolor: "transparent" },
            }}
          >
            <ListItemIcon sx={{ minWidth: 32 }}>
              <Box
                sx={{
                  width: 20,
                  height: 20,
                  bgcolor: "info.main",
                  borderRadius: 0.5,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <Typography
                  sx={{
                    color: "white",
                    fontSize: "10px",
                    fontWeight: "bold",
                  }}
                >
                  K
                </Typography>
              </Box>
            </ListItemIcon>
            <ListItemText
              primary="Kibana"
              primaryTypographyProps={{
                fontSize: "14px",
                fontWeight: 600,
                color: "text.primary",
              }}
            />
            {kibanaOpen ? <ExpandLess /> : <ExpandMore />}
          </ListItemButton>
        </ListItem>

        <Collapse in={kibanaOpen} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            {kibanaItems.map((item) => (
              <ListItem key={item.name} sx={{ px: 2, py: 0 }}>
                <ListItemButton
                  sx={{
                    px: 2,
                    py: 0.75,
                    borderRadius: 1,
                    mb: 0.25,
                    "&:hover": {
                      bgcolor: "grey.100",
                    },
                  }}
                >
                  <ListItemIcon sx={{ minWidth: 32, color: "text.secondary" }}>
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText
                    primary={item.name}
                    primaryTypographyProps={{
                      fontSize: "14px",
                      fontWeight: 400,
                    }}
                  />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Collapse>
      </List>
    </Box>
  );
};

export default ModernSidebar;
