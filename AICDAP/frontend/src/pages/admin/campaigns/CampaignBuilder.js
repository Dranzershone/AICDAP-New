import React, { useState, useEffect } from "react";
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Button,
  Grid,
  Paper,
  Stepper,
  Step,
  StepLabel,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  Chip,
  Avatar,
  IconButton,
  LinearProgress,
  CircularProgress,
  Alert,
  Skeleton,
  TextField,
  useTheme,
  alpha,
} from "@mui/material";
import {
  Groups,
  Email,
  Launch,
  ArrowForward,
  CheckCircle,
  Close,
  Send,
  Visibility,
  Edit,
} from "@mui/icons-material";
import { useNavigate } from "react-router-dom";
import { EmployeeService } from "../../../services/employeeService";
import { CampaignService } from "../../../services/campaignService";

const CampaignBuilder = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const isDark = theme.palette.mode === "dark";

  const [activeStep, setActiveStep] = useState(0);
  const [selectedTargets, setSelectedTargets] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [campaignLaunched, setCampaignLaunched] = useState(false);
  const [showTargetDialog, setShowTargetDialog] = useState(false);
  const [showTemplateDialog, setShowTemplateDialog] = useState(false);
  const [showLaunchDialog, setShowLaunchDialog] = useState(false);
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [employees, setEmployees] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [campaignData, setCampaignData] = useState({
    name: "",
    description: "",
  });

  const steps = ["Select Targets", "Select Template", "Launch Campaign"];

  // Load departments and employees on component mount
  useEffect(() => {
    loadDepartmentsAndEmployees();
  }, []);

  const loadDepartmentsAndEmployees = async () => {
    try {
      setLoading(true);
      setError(null);

      // Get all employees
      const { data: employeeData, error: employeeError } =
        await EmployeeService.getAllEmployees();

      if (employeeError) {
        setError(`Error loading employees: ${employeeError}`);
        return;
      }

      setEmployees(employeeData || []);

      // Group employees by department and create department objects
      const departmentMap = {};
      (employeeData || []).forEach((employee) => {
        const dept = employee.department || "Unassigned";
        if (!departmentMap[dept]) {
          departmentMap[dept] = {
            id: dept.toLowerCase().replace(/\s+/g, "_"),
            name: dept,
            employees: [],
            employeeCount: 0,
            description: `${dept} department`,
          };
        }
        departmentMap[dept].employees.push(employee);
        departmentMap[dept].employeeCount++;
      });

      // Convert to array and sort by employee count
      const departmentList = Object.values(departmentMap).sort(
        (a, b) => b.employeeCount - a.employeeCount,
      );
      setDepartments(departmentList);
    } catch (error) {
      setError("Unexpected error loading department data");
      console.error("Error loading departments:", error);
    } finally {
      setLoading(false);
    }
  };

  // Load templates
  useEffect(() => {
    const fetchTemplates = async () => {
      const { data, error } = await CampaignService.getTemplates();
      if (error) {
        setError("Error loading templates");
      } else {
        setTemplates(data || []);
      }
    };
    fetchTemplates();
  }, []);

  const handleTargetSelect = (department) => {
    const isSelected = selectedTargets.find((t) => t.id === department.id);
    if (isSelected) {
      setSelectedTargets(selectedTargets.filter((t) => t.id !== department.id));
    } else {
      setSelectedTargets([...selectedTargets, department]);
    }
  };

  const handleNext = () => {
    if (activeStep === 0 && selectedTargets.length > 0) {
      setActiveStep(1);
    } else if (activeStep === 1 && selectedTemplate) {
      setActiveStep(2);
    }
  };

  const handleLaunchCampaign = async () => {
    try {
      // 1. Create the campaign in the database first
      const campaignName =
        campaignData.name ||
        `Campaign ${new Date().toLocaleDateString()} - ${selectedTemplate?.name}`;
      const newCampaignData = {
        name: campaignName,
        description:
          campaignData.description ||
          `Phishing simulation using ${selectedTemplate?.name} template`,
        template_id: selectedTemplate?.template_id,
        template_name: selectedTemplate?.name,
        status: "draft", // Start as draft
        total_targets: selectedTargets.reduce(
          (acc, dept) => acc + dept.employeeCount,
          0,
        ),
        targets: selectedTargets,
      };

      const { data: createdCampaign, error: createError } =
        await CampaignService.createCampaign(newCampaignData);

      if (createError) {
        console.error("Error creating campaign:", createError);
        alert("Failed to create campaign. Please try again.");
        return;
      }

      // 2. Launch the campaign using the backend API
      const { error: launchError } = await CampaignService.launchCampaign({
        campaign_id: createdCampaign.id,
        name: createdCampaign.name,
        template_id: createdCampaign.template_id,
      });

      if (launchError) {
        console.error("Error launching campaign:", launchError);
        alert(`Failed to launch campaign: ${launchError}`);
        return;
      }

      setCampaignLaunched(true);
      setShowLaunchDialog(false);

      setTimeout(() => {
        navigate("/admin/campaigns");
      }, 3000);
    } catch (error) {
      console.error("Unexpected error:", error);
      alert("An unexpected error occurred. Please try again.");
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

  if (campaignLaunched) {
    return (
      <Container maxWidth="md" sx={{ py: 8, textAlign: "center" }}>
        <CheckCircle 
          sx={{ 
            fontSize: 96, 
            color: theme.palette.success.main, 
            mb: 3,
            animation: "pulse 2s ease-in-out infinite",
            "@keyframes pulse": {
              "0%, 100%": { transform: "scale(1)" },
              "50%": { transform: "scale(1.1)" },
            },
          }} 
        />
        <Typography 
          variant="h4" 
          gutterBottom
          sx={{ 
            fontWeight: 700,
            color: theme.palette.text.primary,
          }}
        >
          Campaign Launched Successfully!
        </Typography>
        <Typography 
          variant="body1" 
          sx={{ 
            mb: 4,
            color: theme.palette.text.secondary,
            lineHeight: 1.7,
          }}
        >
          Emails are being sent to{" "}
          <strong>
            {selectedTargets.reduce((acc, dept) => acc + dept.employeeCount, 0)}{" "}
            employees
          </strong>{" "}
          across <strong>{selectedTargets.length} departments</strong> using the "
          <strong>{selectedTemplate?.name}</strong>" template.
        </Typography>
        <LinearProgress 
          sx={{ 
            mb: 2,
            height: 8,
            borderRadius: 1,
          }} 
        />
        <Typography 
          variant="body2" 
          sx={{ color: theme.palette.text.secondary }}
        >
          Redirecting to campaigns dashboard...
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography 
          variant="h4" 
          component="h1" 
          gutterBottom
          sx={{ 
            fontWeight: 700,
            color: theme.palette.text.primary,
          }}
        >
          Create Campaign
        </Typography>
        <Typography 
          variant="body1" 
          sx={{ color: theme.palette.text.secondary }}
        >
          Set up a new phishing simulation campaign in three simple steps
        </Typography>
      </Box>

      {/* Progress Stepper */}
      <Paper 
        elevation={isDark ? 2 : 1}
        sx={{ 
          p: 3, 
          mb: 4,
          background: isDark 
            ? alpha(theme.palette.background.paper, 0.6)
            : theme.palette.background.paper,
          border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
        }}
      >
        <Stepper 
          activeStep={activeStep} 
          alternativeLabel
          sx={{
            '& .MuiStepLabel-label': {
              color: theme.palette.text.secondary,
              fontWeight: 500,
              '&.Mui-active': {
                color: theme.palette.primary.main,
                fontWeight: 600,
              },
              '&.Mui-completed': {
                color: theme.palette.success.main,
                fontWeight: 600,
              },
            },
          }}
        >
          {steps.map((label, index) => (
            <Step key={label} completed={index < activeStep}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
      </Paper>

      {/* Main Campaign Builder UI */}
      <Paper
        elevation={isDark ? 2 : 1}
        sx={{
          p: 4,
          background: isDark
            ? `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.15)} 0%, ${alpha(theme.palette.background.paper, 0.6)} 100%)`
            : `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.08)} 0%, ${alpha('#fff', 0.95)} 100%)`,
          border: `2px solid ${isDark ? alpha(theme.palette.primary.main, 0.3) : alpha(theme.palette.primary.main, 0.2)}`,
          borderRadius: 3,
          backdropFilter: "blur(10px)",
        }}
      >
        <Typography
          variant="h5"
          sx={{
            color: theme.palette.primary.main,
            textAlign: "center",
            mb: 4,
            fontWeight: 700,
          }}
        >
          Campaign Builder Workflow
        </Typography>

        <Grid container spacing={3} justifyContent="center">
          {/* Step 1: Select Targets */}
          <Grid item xs={12} md={4}>
            <Card
              elevation={isDark ? 3 : 2}
              sx={{
                height: 220,
                cursor: loading ? "not-allowed" : "pointer",
                border: "2px solid",
                borderColor: selectedTargets.length > 0 
                  ? theme.palette.success.main 
                  : isDark 
                    ? alpha('#fff', 0.2)
                    : alpha(theme.palette.primary.main, 0.3),
                background: isDark 
                  ? alpha(theme.palette.background.paper, 0.6)
                  : theme.palette.background.paper,
                transition: "all 0.3s ease",
                "&:hover": {
                  borderColor: theme.palette.primary.main,
                  transform: "translateY(-4px)",
                  boxShadow: isDark
                    ? `0 8px 24px ${alpha(theme.palette.primary.main, 0.3)}`
                    : `0 8px 24px ${alpha(theme.palette.primary.main, 0.2)}`,
                },
              }}
              onClick={() => !loading && setShowTargetDialog(true)}
            >
              <CardContent 
                sx={{ 
                  textAlign: "center", 
                  p: 3,
                  height: "100%",
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "center",
                }}
              >
                <Groups 
                  sx={{ 
                    fontSize: 56, 
                    color: theme.palette.primary.main, 
                    mb: 2 
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
                  Select Targets
                </Typography>
                <Typography
                  variant="body2"
                  sx={{ 
                    color: theme.palette.text.secondary,
                    mb: 2,
                  }}
                >
                  {loading
                    ? "Loading departments..."
                    : "Select departments to target"}
                </Typography>
                {loading ? (
                  <CircularProgress size={24} sx={{ mx: "auto" }} />
                ) : selectedTargets.length > 0 ? (
                  <Chip
                    label={`${selectedTargets.length} departments selected`}
                    color="success"
                    size="small"
                    sx={{ fontWeight: 600 }}
                  />
                ) : departments.length > 0 ? (
                  <Chip
                    label={`${departments.length} departments available`}
                    color="primary"
                    size="small"
                    variant="outlined"
                    sx={{ fontWeight: 600 }}
                  />
                ) : (
                  <Chip
                    label="No departments found"
                    color="default"
                    size="small"
                    sx={{ fontWeight: 600 }}
                  />
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* Arrow */}
          <Grid
            item
            xs={12}
            md={1}
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <ArrowForward 
              sx={{ 
                color: theme.palette.primary.main, 
                fontSize: 40,
                opacity: activeStep >= 1 ? 1 : 0.3,
                transition: "opacity 0.3s ease",
              }} 
            />
          </Grid>

          {/* Step 2: Select Template */}
          <Grid item xs={12} md={4}>
            <Card
              elevation={isDark ? 3 : 2}
              sx={{
                height: 220,
                cursor: activeStep >= 1 ? "pointer" : "not-allowed",
                border: "2px solid",
                borderColor: selectedTemplate
                  ? theme.palette.success.main
                  : isDark 
                    ? alpha('#fff', 0.2)
                    : alpha(theme.palette.primary.main, 0.3),
                background: isDark 
                  ? alpha(theme.palette.background.paper, activeStep >= 1 ? 0.6 : 0.3)
                  : activeStep >= 1 
                    ? theme.palette.background.paper 
                    : alpha(theme.palette.background.paper, 0.5),
                opacity: activeStep >= 1 ? 1 : 0.5,
                transition: "all 0.3s ease",
                "&:hover": {
                  borderColor: activeStep >= 1 ? theme.palette.primary.main : undefined,
                  transform: activeStep >= 1 ? "translateY(-4px)" : undefined,
                  boxShadow: activeStep >= 1 
                    ? isDark
                      ? `0 8px 24px ${alpha(theme.palette.primary.main, 0.3)}`
                      : `0 8px 24px ${alpha(theme.palette.primary.main, 0.2)}`
                    : undefined,
                },
              }}
              onClick={() => activeStep >= 1 && setShowTemplateDialog(true)}
            >
              <CardContent 
                sx={{ 
                  textAlign: "center", 
                  p: 3,
                  height: "100%",
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "center",
                }}
              >
                <Email 
                  sx={{ 
                    fontSize: 56, 
                    color: theme.palette.primary.main, 
                    mb: 2 
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
                  Select Template
                </Typography>
                <Typography
                  variant="body2"
                  sx={{ 
                    color: theme.palette.text.secondary,
                    mb: 2,
                  }}
                >
                  Choose phishing email template
                </Typography>
                {selectedTemplate ? (
                  <Chip
                    label={selectedTemplate.name}
                    color="success"
                    size="small"
                    sx={{ fontWeight: 600 }}
                  />
                ) : (
                  <Chip
                    label="Not selected"
                    color="default"
                    size="small"
                    variant="outlined"
                    sx={{ fontWeight: 600 }}
                  />
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* Arrow */}
          <Grid
            item
            xs={12}
            md={1}
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <ArrowForward 
              sx={{ 
                color: theme.palette.primary.main, 
                fontSize: 40,
                opacity: activeStep >= 2 ? 1 : 0.3,
                transition: "opacity 0.3s ease",
              }} 
            />
          </Grid>

          {/* Step 3: Launch Now */}
          <Grid item xs={12} md={2}>
            <Card
              elevation={isDark ? 3 : 2}
              sx={{
                height: 220,
                cursor: activeStep >= 2 ? "pointer" : "not-allowed",
                border: "2px solid",
                borderColor: isDark 
                  ? alpha('#fff', 0.2)
                  : alpha(theme.palette.primary.main, 0.3),
                background: isDark 
                  ? alpha(theme.palette.background.paper, activeStep >= 2 ? 0.6 : 0.3)
                  : activeStep >= 2 
                    ? theme.palette.background.paper 
                    : alpha(theme.palette.background.paper, 0.5),
                opacity: activeStep >= 2 ? 1 : 0.5,
                transition: "all 0.3s ease",
                "&:hover": {
                  borderColor: activeStep >= 2 ? theme.palette.primary.main : undefined,
                  transform: activeStep >= 2 ? "translateY(-4px)" : undefined,
                  boxShadow: activeStep >= 2 
                    ? isDark
                      ? `0 8px 24px ${alpha(theme.palette.primary.main, 0.3)}`
                      : `0 8px 24px ${alpha(theme.palette.primary.main, 0.2)}`
                    : undefined,
                },
              }}
              onClick={() => activeStep >= 2 && setShowLaunchDialog(true)}
            >
              <CardContent
                sx={{
                  textAlign: "center",
                  p: 3,
                  height: "100%",
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "center",
                }}
              >
                <Launch 
                  sx={{ 
                    fontSize: 56, 
                    color: theme.palette.primary.main, 
                    mb: 2 
                  }} 
                />
                <Typography 
                  variant="h6" 
                  sx={{ 
                    color: theme.palette.text.primary,
                    fontWeight: 600,
                  }}
                >
                  Launch Now
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Final Arrow */}
        <Box sx={{ display: "flex", justifyContent: "flex-end", mt: 4, mr: { xs: 0, md: 8 } }}>
          <Box 
            sx={{ 
              textAlign: "right",
              p: 2,
              borderRadius: 2,
              backgroundColor: isDark 
                ? alpha(theme.palette.primary.main, 0.1)
                : alpha(theme.palette.primary.main, 0.05),
            }}
          >
            <Send 
              sx={{ 
                color: theme.palette.primary.main, 
                fontSize: 36, 
                mb: 1 
              }} 
            />
            <Typography 
              variant="body2" 
              sx={{ 
                color: theme.palette.text.primary,
                fontWeight: 500,
              }}
            >
              Send emails to selected employees
            </Typography>
            <Typography 
              variant="caption" 
              sx={{ 
                color: theme.palette.text.secondary,
              }}
            >
              Track opens, clicks, and reports
            </Typography>
          </Box>
        </Box>
      </Paper>

      {/* Target Selection Dialog */}
      <Dialog
        open={showTargetDialog}
        onClose={() => setShowTargetDialog(false)}
        maxWidth="md"
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
          Select Target Departments
          <IconButton
            onClick={() => setShowTargetDialog(false)}
            sx={{ 
              position: "absolute", 
              right: 8, 
              top: 8,
              color: theme.palette.text.secondary,
            }}
          >
            <Close />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          {loading ? (
            <Box
              sx={{ display: "flex", flexDirection: "column", gap: 2, p: 2 }}
            >
              {Array.from({ length: 3 }).map((_, index) => (
                <Box
                  key={index}
                  sx={{ display: "flex", alignItems: "center", gap: 2 }}
                >
                  <Skeleton variant="circular" width={48} height={48} />
                  <Box sx={{ flex: 1 }}>
                    <Skeleton variant="text" width="60%" height={24} />
                    <Skeleton variant="text" width="80%" height={20} />
                  </Box>
                </Box>
              ))}
            </Box>
          ) : error ? (
            <Alert severity="error" sx={{ m: 2 }}>
              {error}
              <Button 
                onClick={loadDepartmentsAndEmployees} 
                sx={{ 
                  ml: 2,
                  textTransform: "none",
                  fontWeight: 600,
                }}
              >
                Retry
              </Button>
            </Alert>
          ) : departments.length === 0 ? (
            <Alert severity="info" sx={{ m: 2 }}>
              No departments found. Please add some employees first.
            </Alert>
          ) : (
            <List>
              {departments.map((dept) => (
                <ListItem key={dept.id} disablePadding>
                  <ListItemButton
                    selected={!!selectedTargets.find((t) => t.id === dept.id)}
                    onClick={() => handleTargetSelect(dept)}
                    sx={{
                      borderRadius: 1,
                      mb: 1,
                      border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
                      "&.Mui-selected": {
                        backgroundColor: isDark 
                          ? alpha(theme.palette.primary.main, 0.2)
                          : alpha(theme.palette.primary.main, 0.1),
                        borderColor: theme.palette.primary.main,
                      },
                      "&:hover": {
                        backgroundColor: isDark 
                          ? alpha('#fff', 0.05)
                          : alpha('#000', 0.04),
                      },
                    }}
                  >
                    <Avatar 
                      sx={{ 
                        bgcolor: theme.palette.primary.main, 
                        mr: 2,
                        width: 48,
                        height: 48,
                      }}
                    >
                      <Groups />
                    </Avatar>
                    <ListItemText
                      primary={
                        <Typography 
                          variant="subtitle1"
                          sx={{ 
                            fontWeight: 600,
                            color: theme.palette.text.primary,
                          }}
                        >
                          {dept.name}
                        </Typography>
                      }
                      secondary={
                        <Typography 
                          variant="body2"
                          sx={{ color: theme.palette.text.secondary }}
                        >
                          {dept.employeeCount} employees • {dept.description}
                        </Typography>
                      }
                    />
                    {selectedTargets.find((t) => t.id === dept.id) && (
                      <CheckCircle 
                        sx={{ 
                          color: theme.palette.success.main,
                          fontSize: 28,
                        }} 
                      />
                    )}
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          )}
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button 
            onClick={() => setShowTargetDialog(false)}
            sx={{
              textTransform: "none",
              fontWeight: 600,
            }}
          >
            Cancel
          </Button>
          <Button
            variant="contained"
            onClick={() => {
              setShowTargetDialog(false);
              if (selectedTargets.length > 0) {
                handleNext();
              }
            }}
            disabled={selectedTargets.length === 0}
            sx={{
              textTransform: "none",
              fontWeight: 600,
            }}
          >
            Continue ({selectedTargets.length} selected)
          </Button>
        </DialogActions>
      </Dialog>

      {/* Template Selection Dialog */}
      <Dialog
        open={showTemplateDialog}
        onClose={() => setShowTemplateDialog(false)}
        maxWidth="lg"
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
          Select Email Template
          <IconButton
            onClick={() => setShowTemplateDialog(false)}
            sx={{ 
              position: "absolute", 
              right: 8, 
              top: 8,
              color: theme.palette.text.secondary,
            }}
          >
            <Close />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={3}>
            {templates.map((template) => (
              <Grid item xs={12} md={6} key={template.id}>
                <Card
                  elevation={isDark ? 2 : 1}
                  sx={{
                    cursor: "pointer",
                    border: "2px solid",
                    borderColor: selectedTemplate?.id === template.id
                      ? theme.palette.primary.main
                      : isDark 
                        ? alpha('#fff', 0.1)
                        : alpha('#000', 0.08),
                    background: isDark 
                      ? alpha(theme.palette.background.paper, 0.6)
                      : theme.palette.background.paper,
                    transition: "all 0.3s ease",
                    "&:hover": {
                      borderColor: theme.palette.primary.main,
                      transform: "translateY(-4px)",
                      boxShadow: isDark
                        ? `0 8px 24px ${alpha(theme.palette.primary.main, 0.3)}`
                        : `0 8px 24px ${alpha(theme.palette.primary.main, 0.2)}`,
                    },
                  }}
                  onClick={() => setSelectedTemplate(template)}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Box
                      sx={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "flex-start",
                        mb: 2,
                      }}
                    >
                      <Typography 
                        variant="h6"
                        sx={{ 
                          fontWeight: 600,
                          color: theme.palette.text.primary,
                        }}
                      >
                        {template.name}
                      </Typography>
                      <Chip
                        label={template.difficulty}
                        color={getDifficultyColor(template.difficulty)}
                        size="small"
                        sx={{ fontWeight: 600 }}
                      />
                    </Box>
                    <Typography
                      variant="body2"
                      sx={{ 
                        mb: 2,
                        color: theme.palette.text.secondary,
                        lineHeight: 1.6,
                      }}
                    >
                      {template.description}
                    </Typography>
                    <Paper
                      sx={{
                        p: 2,
                        backgroundColor: isDark 
                          ? alpha('#fff', 0.05)
                          : alpha('#000', 0.02),
                        mb: 2,
                        border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
                      }}
                    >
                      <Typography 
                        variant="caption" 
                        sx={{ 
                          color: theme.palette.text.secondary,
                          textTransform: "uppercase",
                          letterSpacing: 0.5,
                          fontWeight: 600,
                        }}
                      >
                        Preview:
                      </Typography>
                      <Typography 
                        variant="body2"
                        sx={{ 
                          color: theme.palette.text.primary,
                          mt: 1,
                        }}
                      >
                        {template.preview}
                      </Typography>
                    </Paper>
                    <Box sx={{ display: "flex", gap: 1 }}>
                      <Button 
                        size="small" 
                        startIcon={<Visibility />}
                        sx={{
                          textTransform: "none",
                          fontWeight: 600,
                        }}
                      >
                        Preview
                      </Button>
                      <Button 
                        size="small" 
                        startIcon={<Edit />}
                        sx={{
                          textTransform: "none",
                          fontWeight: 600,
                        }}
                      >
                        Customize
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button 
            onClick={() => setShowTemplateDialog(false)}
            sx={{
              textTransform: "none",
              fontWeight: 600,
            }}
          >
            Cancel
          </Button>
          <Button
            variant="contained"
            onClick={() => {
              setShowTemplateDialog(false);
              if (selectedTemplate) {
                handleNext();
              }
            }}
            disabled={!selectedTemplate}
            sx={{
              textTransform: "none",
              fontWeight: 600,
            }}
          >
            Continue with {selectedTemplate?.name || "Template"}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Launch Confirmation Dialog */}
      <Dialog
        open={showLaunchDialog}
        onClose={() => setShowLaunchDialog(false)}
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
          Launch Campaign
        </DialogTitle>
        <DialogContent>
          <Typography 
            variant="body1" 
            sx={{ 
              mb: 3,
              color: theme.palette.text.secondary,
            }}
          >
            Provide campaign details and launch your phishing simulation.
          </Typography>

          <TextField
            fullWidth
            label="Campaign Name"
            value={campaignData.name}
            onChange={(e) =>
              setCampaignData({ ...campaignData, name: e.target.value })
            }
            placeholder={`Campaign ${new Date().toLocaleDateString()} - ${selectedTemplate?.name}`}
            sx={{ 
              mb: 2,
              '& .MuiOutlinedInput-root': {
                backgroundColor: isDark 
                  ? alpha('#fff', 0.05)
                  : alpha('#000', 0.02),
              },
            }}
          />

          <TextField
            fullWidth
            multiline
            rows={3}
            label="Campaign Description"
            value={campaignData.description}
            onChange={(e) =>
              setCampaignData({ ...campaignData, description: e.target.value })
            }
            placeholder={`Phishing simulation using ${selectedTemplate?.name} template targeting ${selectedTargets.length} departments`}
            sx={{ 
              mb: 3,
              '& .MuiOutlinedInput-root': {
                backgroundColor: isDark 
                  ? alpha('#fff', 0.05)
                  : alpha('#000', 0.02),
              },
            }}
          />

          <Box 
            sx={{ 
              p: 2,
              borderRadius: 2,
              backgroundColor: isDark 
                ? alpha('#fff', 0.05)
                : alpha('#000', 0.02),
              border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
            }}
          >
            <Typography 
              variant="subtitle2" 
              gutterBottom
              sx={{ 
                fontWeight: 600,
                color: theme.palette.text.primary,
                mb: 1.5,
              }}
            >
              Campaign Summary:
            </Typography>
            <Box sx={{ display: "flex", flexDirection: "column", gap: 0.5 }}>
              <Typography 
                variant="body2" 
                sx={{ color: theme.palette.text.secondary }}
              >
                • <strong>Targets:</strong> {selectedTargets.map((t) => t.name).join(", ")}
              </Typography>
              <Typography 
                variant="body2" 
                sx={{ color: theme.palette.text.secondary }}
              >
                • <strong>Total Recipients:</strong>{" "}
                {selectedTargets.reduce(
                  (acc, dept) => acc + dept.employeeCount,
                  0,
                )}{" "}
                employees
              </Typography>
              <Typography 
                variant="body2" 
                sx={{ color: theme.palette.text.secondary }}
              >
                • <strong>Template:</strong> {selectedTemplate?.name}
              </Typography>
              <Typography 
                variant="body2" 
                sx={{ color: theme.palette.text.secondary }}
              >
                • <strong>Difficulty:</strong> {selectedTemplate?.difficulty}
              </Typography>
            </Box>
          </Box>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button 
            onClick={() => setShowLaunchDialog(false)}
            sx={{
              textTransform: "none",
              fontWeight: 600,
            }}
          >
            Cancel
          </Button>
          <Button
            variant="contained"
            color="error"
            startIcon={<Send />}
            onClick={handleLaunchCampaign}
            sx={{
              textTransform: "none",
              fontWeight: 600,
            }}
          >
            Launch Campaign
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default CampaignBuilder;