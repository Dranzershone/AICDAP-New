import React, { useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  TextField,
  InputAdornment,
  Chip,
  IconButton,
  Switch,
  FormControlLabel,
  Select,
  MenuItem,
  FormControl,
  Tabs,
  Tab,
  Checkbox,
  Pagination,
} from "@mui/material";
import {
  Search as SearchIcon,
  Refresh as RefreshIcon,
  Add as AddIcon,
  MoreVert as MoreVertIcon,
  KeyboardArrowDown as ArrowDownIcon,
  KeyboardArrowUp as ArrowUpIcon,
  Check as CheckIcon,
} from "@mui/icons-material";

const ModernDashboard = () => {
  const [currentTab, setCurrentTab] = useState(0);
  const [includeSystemTemplates, setIncludeSystemTemplates] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [rowsPerPage, setRowsPerPage] = useState(20);

  // Sample data inspired by the Elasticsearch interface
  const sampleData = [
    {
      name: "ilm-history",
      indexPatterns: "ilm-history-*",
      ilmPolicy: "ilm-history-ilm-policy",
      order: 2147483647,
      mappings: true,
      settings: true,
      aliases: false,
    },
    {
      name: "user-data-template",
      indexPatterns: "user-data-*",
      ilmPolicy: "user-data-policy",
      order: 100,
      mappings: true,
      settings: true,
      aliases: true,
    },
    {
      name: "logs-template",
      indexPatterns: "logs-*",
      ilmPolicy: "logs-retention-policy",
      order: 200,
      mappings: true,
      settings: true,
      aliases: true,
    },
  ];

  const handleTabChange = (event, newValue) => {
    setCurrentTab(newValue);
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        bgcolor: "#f8f9fa",
        p: 3,
      }}
    >
      {/* Header */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 3,
        }}
      >
        <Typography
          variant="h4"
          sx={{
            fontWeight: 500,
            color: "#1a1a1a",
            fontSize: "2rem",
          }}
        >
          Index Management
        </Typography>
        <Button
          variant="text"
          sx={{
            color: "#ff6b35",
            textTransform: "none",
            fontSize: "14px",
            fontWeight: 500,
          }}
        >
          Index Management docs
        </Button>
      </Box>

      {/* Main Content Card */}
      <Paper
        sx={{
          borderRadius: 2,
          boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
          overflow: "hidden",
        }}
      >
        {/* Tabs */}
        <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
          <Tabs
            value={currentTab}
            onChange={handleTabChange}
            sx={{
              "& .MuiTab-root": {
                textTransform: "none",
                fontSize: "14px",
                fontWeight: 500,
                minWidth: "auto",
                px: 3,
              },
              "& .Mui-selected": {
                color: "#ff6b35 !important",
              },
              "& .MuiTabs-indicator": {
                backgroundColor: "#ff6b35",
              },
            }}
          >
            <Tab label="Indices" />
            <Tab label="Index Templates" />
          </Tabs>
        </Box>

        {/* Content */}
        <Box sx={{ p: 3 }}>
          {/* Description */}
          <Typography
            variant="body2"
            sx={{
              color: "#6c757d",
              mb: 3,
              fontSize: "14px",
            }}
          >
            Use index templates to automatically apply settings, mappings, and
            aliases to indices.
          </Typography>

          {/* Controls Row */}
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              mb: 3,
            }}
          >
            <FormControlLabel
              control={
                <Switch
                  checked={includeSystemTemplates}
                  onChange={(e) => setIncludeSystemTemplates(e.target.checked)}
                  sx={{
                    "& .MuiSwitch-switchBase.Mui-checked": {
                      color: "#00e676",
                    },
                    "& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track": {
                      backgroundColor: "#00e676",
                    },
                  }}
                />
              }
              label="Include system templates"
              sx={{
                "& .MuiFormControlLabel-label": {
                  fontSize: "14px",
                  color: "#1a1a1a",
                },
              }}
            />

            <Box sx={{ display: "flex", gap: 2 }}>
              <Button
                variant="outlined"
                startIcon={<RefreshIcon />}
                sx={{
                  textTransform: "none",
                  borderColor: "#d1d5db",
                  color: "#374151",
                  "&:hover": {
                    borderColor: "#9ca3af",
                    bgcolor: "transparent",
                  },
                }}
              >
                Reload
              </Button>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                sx={{
                  textTransform: "none",
                  bgcolor: "#ff6b35",
                  "&:hover": {
                    bgcolor: "#e64a19",
                  },
                  boxShadow: "none",
                }}
              >
                Create a template
              </Button>
            </Box>
          </Box>

          {/* Search */}
          <TextField
            fullWidth
            placeholder="Search..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon sx={{ color: "#6c757d" }} />
                </InputAdornment>
              ),
            }}
            sx={{
              mb: 3,
              "& .MuiOutlinedInput-root": {
                bgcolor: "white",
                "& fieldset": {
                  borderColor: "#d1d5db",
                },
                "&:hover fieldset": {
                  borderColor: "#9ca3af",
                },
                "&.Mui-focused fieldset": {
                  borderColor: "#ff6b35",
                },
              },
            }}
          />

          {/* Table */}
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell padding="checkbox">
                    <Checkbox size="small" />
                  </TableCell>
                  <TableCell
                    sx={{
                      fontWeight: 600,
                      fontSize: "14px",
                      color: "#1a1a1a",
                      borderBottom: "2px solid #e5e7eb",
                    }}
                  >
                    <Box sx={{ display: "flex", alignItems: "center" }}>
                      Name
                      <ArrowUpIcon sx={{ ml: 0.5, fontSize: 16 }} />
                    </Box>
                  </TableCell>
                  <TableCell
                    sx={{
                      fontWeight: 600,
                      fontSize: "14px",
                      color: "#1a1a1a",
                      borderBottom: "2px solid #e5e7eb",
                    }}
                  >
                    Index patterns
                  </TableCell>
                  <TableCell
                    sx={{
                      fontWeight: 600,
                      fontSize: "14px",
                      color: "#1a1a1a",
                      borderBottom: "2px solid #e5e7eb",
                    }}
                  >
                    ILM policy
                  </TableCell>
                  <TableCell
                    sx={{
                      fontWeight: 600,
                      fontSize: "14px",
                      color: "#1a1a1a",
                      borderBottom: "2px solid #e5e7eb",
                    }}
                  >
                    Order
                  </TableCell>
                  <TableCell
                    sx={{
                      fontWeight: 600,
                      fontSize: "14px",
                      color: "#1a1a1a",
                      borderBottom: "2px solid #e5e7eb",
                    }}
                  >
                    Mappings
                  </TableCell>
                  <TableCell
                    sx={{
                      fontWeight: 600,
                      fontSize: "14px",
                      color: "#1a1a1a",
                      borderBottom: "2px solid #e5e7eb",
                    }}
                  >
                    Settings
                  </TableCell>
                  <TableCell
                    sx={{
                      fontWeight: 600,
                      fontSize: "14px",
                      color: "#1a1a1a",
                      borderBottom: "2px solid #e5e7eb",
                    }}
                  >
                    Aliases
                  </TableCell>
                  <TableCell
                    sx={{
                      fontWeight: 600,
                      fontSize: "14px",
                      color: "#1a1a1a",
                      borderBottom: "2px solid #e5e7eb",
                    }}
                  >
                    Actions
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {sampleData.map((row, index) => (
                  <TableRow
                    key={index}
                    sx={{
                      "&:hover": {
                        bgcolor: "#f8f9fa",
                      },
                      borderBottom: "1px solid #f1f3f4",
                    }}
                  >
                    <TableCell padding="checkbox">
                      <Checkbox size="small" />
                    </TableCell>
                    <TableCell
                      sx={{
                        color: "#ff6b35",
                        fontWeight: 500,
                        fontSize: "14px",
                      }}
                    >
                      {row.name}
                    </TableCell>
                    <TableCell sx={{ fontSize: "14px", color: "#1a1a1a" }}>
                      {row.indexPatterns}
                    </TableCell>
                    <TableCell sx={{ fontSize: "14px", color: "#1a1a1a" }}>
                      {row.ilmPolicy}
                    </TableCell>
                    <TableCell sx={{ fontSize: "14px", color: "#1a1a1a" }}>
                      {row.order}
                    </TableCell>
                    <TableCell>
                      {row.mappings && (
                        <CheckIcon sx={{ color: "#00e676", fontSize: 20 }} />
                      )}
                    </TableCell>
                    <TableCell>
                      {row.settings && (
                        <CheckIcon sx={{ color: "#00e676", fontSize: 20 }} />
                      )}
                    </TableCell>
                    <TableCell>
                      {row.aliases && (
                        <CheckIcon sx={{ color: "#00e676", fontSize: 20 }} />
                      )}
                    </TableCell>
                    <TableCell>
                      <IconButton size="small">
                        <MoreVertIcon sx={{ fontSize: 18, color: "#6c757d" }} />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>

          {/* Footer */}
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              mt: 3,
              pt: 2,
            }}
          >
            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              <Typography
                variant="body2"
                sx={{ fontSize: "14px", color: "#6c757d" }}
              >
                Rows per page:
              </Typography>
              <FormControl size="small">
                <Select
                  value={rowsPerPage}
                  onChange={(e) => setRowsPerPage(e.target.value)}
                  sx={{
                    fontSize: "14px",
                    minWidth: 60,
                    "& .MuiSelect-select": {
                      py: 0.5,
                    },
                  }}
                >
                  <MenuItem value={10}>10</MenuItem>
                  <MenuItem value={20}>20</MenuItem>
                  <MenuItem value={50}>50</MenuItem>
                  <MenuItem value={100}>100</MenuItem>
                </Select>
              </FormControl>
            </Box>

            <Pagination
              count={1}
              page={1}
              sx={{
                "& .MuiPaginationItem-root": {
                  fontSize: "14px",
                },
                "& .Mui-selected": {
                  bgcolor: "#ff6b35 !important",
                  color: "white",
                },
              }}
            />
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default ModernDashboard;
