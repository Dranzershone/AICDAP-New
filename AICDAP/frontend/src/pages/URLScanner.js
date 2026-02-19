import React, { useState, useRef } from "react";
import {
  Box,
  Container,
  Typography,
  Paper,
  TextField,
  Button,
  Alert,
  CircularProgress,
  Chip,
  Grid,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Tabs,
  Tab,
  IconButton,
  Tooltip,
  FormControlLabel,
  Switch,
  useTheme,
  alpha,
} from "@mui/material";
import {
  Security,
  Warning,
  CheckCircle,
  Error,
  Info,
  Link as LinkIcon,
  Search,
  Shield,
  Email,
  Image as ImageIcon,
  Upload,
  Clear,
  ContentPaste,
} from "@mui/icons-material";

const URLScanner = () => {
  const theme = useTheme();
  const isDark = theme.palette.mode === "dark";
  
  const [activeTab, setActiveTab] = useState(0);

  // URL Scanner states
  const [url, setUrl] = useState("");
  const [urlLoading, setUrlLoading] = useState(false);
  const [urlResult, setUrlResult] = useState(null);
  const [urlError, setUrlError] = useState("");

  // Email Scanner states
  const [emailText, setEmailText] = useState("");
  const [emailLoading, setEmailLoading] = useState(false);
  const [emailResult, setEmailResult] = useState(null);
  const [emailError, setEmailError] = useState("");
  const [senderHistory, setSenderHistory] = useState(0);

  // Image Scanner states
  const [selectedImage, setSelectedImage] = useState(null);
  const [imageLoading, setImageLoading] = useState(false);
  const [imageResult, setImageResult] = useState(null);
  const [imageError, setImageError] = useState("");
  const fileInputRef = useRef(null);

  const getRiskColor = (risk) => {
    switch (risk) {
      case "low":
        return "success";
      case "low-medium":
        return "info";
      case "medium":
        return "warning";
      case "high":
        return "error";
      default:
        return "default";
    }
  };

  const getRiskIcon = (risk) => {
    switch (risk) {
      case "low":
        return <CheckCircle />;
      case "low-medium":
        return <Info />;
      case "medium":
        return <Warning />;
      case "high":
        return <Error />;
      default:
        return <Security />;
    }
  };

  const handleUrlScan = async () => {
    if (!url.trim()) {
      setUrlError("Please enter a URL to scan");
      return;
    }

    setUrlLoading(true);
    setUrlError("");
    setUrlResult(null);

    try {
      const response = await fetch("http://localhost:8000/api/analyze-url", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: url.trim() }),
      });

      if (!response.ok) {
        throw new Error("Failed to analyze URL");
      }

      const data = await response.json();
      setUrlResult(data);
    } catch (err) {
      setUrlError(err.message || "An error occurred while scanning the URL");
    } finally {
      setUrlLoading(false);
    }
  };

  const handleEmailScan = async () => {
    if (!emailText.trim()) {
      setEmailError("Please enter email content to analyze");
      return;
    }

    setEmailLoading(true);
    setEmailError("");
    setEmailResult(null);

    try {
      const response = await fetch(
        "http://localhost:8000/api/email-phishing/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email_text: emailText,
            sender_history: senderHistory,
          }),
        },
      );

      if (!response.ok) {
        throw new Error("Failed to analyze email");
      }

      const result = await response.json();
      if (result.success) {
        setEmailResult(result.data);
      } else {
        throw new Error(result.error || "Email analysis failed");
      }
    } catch (err) {
      setEmailError(
        err.message || "An error occurred while analyzing the email",
      );
    } finally {
      setEmailLoading(false);
    }
  };

  const handleImageUpload = async (file) => {
    if (!file) return;

    setImageLoading(true);
    setImageError("");
    setImageResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        "http://localhost:8000/api/email-phishing/analyze-image",
        {
          method: "POST",
          body: formData,
        },
      );

      if (!response.ok) {
        throw new Error("Failed to analyze image");
      }

      const result = await response.json();
      if (result.success) {
        setImageResult(result);
      } else {
        throw new Error(result.error || "Image analysis failed");
      }
    } catch (err) {
      setImageError(
        err.message || "An error occurred while analyzing the image",
      );
    } finally {
      setImageLoading(false);
    }
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(file);
      handleImageUpload(file);
    }
  };

  const handlePasteFromClipboard = async () => {
    try {
      const text = await navigator.clipboard.readText();
      setEmailText(text);
    } catch (err) {
      setEmailError("Failed to paste from clipboard. Please paste manually.");
    }
  };

  const handleKeyPress = (event, scanFunction) => {
    if (event.key === "Enter") {
      scanFunction();
    }
  };

  const TabPanel = ({ children, value, index, ...other }) => (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`scanner-tabpanel-${index}`}
      aria-labelledby={`scanner-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ mt: 3 }}>{children}</Box>}
    </div>
  );

  const renderUrlScanner = () => (
    <>
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
        <Box sx={{ mb: 3 }}>
          <Typography 
            variant="h6" 
            sx={{ 
              mb: 1,
              fontWeight: 600,
              color: theme.palette.text.primary,
            }}
          >
            URL Security Scanner
          </Typography>
          <Typography 
            variant="body2" 
            sx={{ color: theme.palette.text.secondary }}
          >
            Enter a URL to check for phishing attempts, malicious content, and security risks
          </Typography>
        </Box>

        <Grid container spacing={2} alignItems="flex-end">
          <Grid item xs={12} md={9}>
            <TextField
              fullWidth
              label="Enter URL to scan"
              placeholder="https://example.com"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              onKeyPress={(e) => handleKeyPress(e, handleUrlScan)}
              disabled={urlLoading}
              InputProps={{
                startAdornment: (
                  <LinkIcon sx={{ mr: 1, color: theme.palette.text.secondary }} />
                ),
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  backgroundColor: isDark 
                    ? alpha('#fff', 0.05)
                    : alpha('#000', 0.02),
                },
              }}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <Button
              fullWidth
              variant="contained"
              onClick={handleUrlScan}
              disabled={urlLoading || !url.trim()}
              startIcon={
                urlLoading ? <CircularProgress size={20} color="inherit" /> : <Search />
              }
              sx={{ 
                py: 1.8,
                fontWeight: 600,
                textTransform: "none",
                fontSize: "1rem",
              }}
            >
              {urlLoading ? "Scanning..." : "Scan URL"}
            </Button>
          </Grid>
        </Grid>

        {urlError && (
          <Alert severity="error" sx={{ mt: 3 }}>
            {urlError}
          </Alert>
        )}
      </Paper>

      {urlResult && (
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
                  Scan Results
                </Typography>
                <Box sx={{ mb: 3 }}>
                  <Chip
                    icon={getRiskIcon(urlResult.risk_level)}
                    label={`Risk Level: ${urlResult.risk_level?.toUpperCase()}`}
                    color={getRiskColor(urlResult.risk_level)}
                    size="medium"
                    sx={{ 
                      px: 1,
                      fontWeight: 600,
                      fontSize: "0.875rem",
                    }}
                  />
                </Box>
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
                      URL
                    </Typography>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: theme.palette.text.primary,
                        wordBreak: "break-all",
                        mt: 0.5,
                      }}
                    >
                      {urlResult.url}
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
                      Is Phishing
                    </Typography>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: urlResult.is_phishing 
                          ? theme.palette.error.main 
                          : theme.palette.success.main,
                        fontWeight: 600,
                        mt: 0.5,
                      }}
                    >
                      {urlResult.is_phishing ? "Yes" : "No"}
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
                      Confidence
                    </Typography>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: theme.palette.text.primary,
                        fontWeight: 600,
                        mt: 0.5,
                      }}
                    >
                      {(urlResult.confidence * 100).toFixed(1)}%
                    </Typography>
                  </Box>
                </Box>
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
                  Detected Features
                </Typography>
                <List dense>
                  {Object.entries(urlResult.features || {}).map(
                    ([feature, detected]) => (
                      <ListItem 
                        key={feature} 
                        divider
                        sx={{
                          px: 0,
                          py: 1,
                        }}
                      >
                        <ListItemIcon sx={{ minWidth: 40 }}>
                          {detected ? (
                            <Warning color="warning" />
                          ) : (
                            <CheckCircle color="success" />
                          )}
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
                              {feature
                                .replace(/_/g, " ")
                                .replace(/\b\w/g, (l) => l.toUpperCase())}
                            </Typography>
                          }
                          secondary={
                            <Typography 
                              variant="caption"
                              sx={{ color: theme.palette.text.secondary }}
                            >
                              {detected ? "Detected" : "Not detected"}
                            </Typography>
                          }
                        />
                      </ListItem>
                    ),
                  )}
                </List>
              </CardContent>
            </Card>
          </Grid>

          {urlResult.domain_info && (
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
                    Domain Information
                  </Typography>
                  <Grid container spacing={3}>
                    {Object.entries(urlResult.domain_info).map(
                      ([key, value]) => (
                        <Grid item xs={12} sm={6} md={4} key={key}>
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
                              {key
                                .replace(/_/g, " ")
                                .replace(/\b\w/g, (l) => l.toUpperCase())}
                            </Typography>
                            <Typography 
                              variant="body1"
                              sx={{ 
                                color: theme.palette.text.primary,
                                fontWeight: 500,
                                mt: 0.5,
                              }}
                            >
                              {typeof value === "boolean"
                                ? value
                                  ? "Yes"
                                  : "No"
                                : value || "N/A"}
                            </Typography>
                          </Box>
                        </Grid>
                      ),
                    )}
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      )}
    </>
  );

  const renderEmailScanner = () => (
    <>
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
        <Box
          sx={{
            mb: 3,
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
          }}
        >
          <Box>
            <Typography 
              variant="h6"
              sx={{ 
                mb: 1,
                fontWeight: 600,
                color: theme.palette.text.primary,
              }}
            >
              Email Content Analysis
            </Typography>
            <Typography 
              variant="body2" 
              sx={{ color: theme.palette.text.secondary }}
            >
              Paste suspicious email content for comprehensive phishing detection
            </Typography>
          </Box>
          <Box sx={{ display: "flex", gap: 1 }}>
            <Tooltip title="Paste from clipboard">
              <IconButton 
                onClick={handlePasteFromClipboard} 
                size="small"
                sx={{
                  backgroundColor: isDark 
                    ? alpha('#fff', 0.05)
                    : alpha('#000', 0.04),
                  '&:hover': {
                    backgroundColor: isDark 
                      ? alpha('#fff', 0.1)
                      : alpha('#000', 0.08),
                  },
                }}
              >
                <ContentPaste fontSize="small" />
              </IconButton>
            </Tooltip>
            <Tooltip title="Clear text">
              <IconButton 
                onClick={() => setEmailText("")} 
                size="small"
                sx={{
                  backgroundColor: isDark 
                    ? alpha('#fff', 0.05)
                    : alpha('#000', 0.04),
                  '&:hover': {
                    backgroundColor: isDark 
                      ? alpha('#fff', 0.1)
                      : alpha('#000', 0.08),
                  },
                }}
              >
                <Clear fontSize="small" />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>

        <TextField
          fullWidth
          multiline
          rows={8}
          label="Email Content"
          placeholder="Paste the suspicious email content here for analysis..."
          value={emailText}
          onChange={(e) => setEmailText(e.target.value)}
          disabled={emailLoading}
          sx={{
            mb: 3,
            '& .MuiOutlinedInput-root': {
              backgroundColor: isDark 
                ? alpha('#fff', 0.05)
                : alpha('#000', 0.02),
            },
          }}
        />

        <Grid container spacing={2} alignItems="flex-end">
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              label="Sender History Count"
              type="number"
              value={senderHistory}
              onChange={(e) =>
                setSenderHistory(Math.max(0, parseInt(e.target.value) || 0))
              }
              disabled={emailLoading}
              helperText="Previous emails from sender"
              size="small"
              sx={{
                '& .MuiOutlinedInput-root': {
                  backgroundColor: isDark 
                    ? alpha('#fff', 0.05)
                    : alpha('#000', 0.02),
                },
              }}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Button
              fullWidth
              variant="contained"
              onClick={handleEmailScan}
              disabled={emailLoading || !emailText.trim()}
              startIcon={
                emailLoading ? <CircularProgress size={20} color="inherit" /> : <Email />
              }
              sx={{ 
                py: 1.8,
                fontWeight: 600,
                textTransform: "none",
                fontSize: "1rem",
              }}
            >
              {emailLoading ? "Analyzing..." : "Analyze Email"}
            </Button>
          </Grid>
        </Grid>

        {emailError && (
          <Alert severity="error" sx={{ mt: 3 }}>
            {emailError}
          </Alert>
        )}
      </Paper>

      {emailResult && (
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
                  Phishing Analysis Results
                </Typography>
                <Box sx={{ mb: 3 }}>
                  <Chip
                    icon={getRiskIcon(emailResult.risk_level)}
                    label={`${emailResult.classification}`}
                    color={getRiskColor(emailResult.risk_level)}
                    size="medium"
                    sx={{ 
                      px: 1,
                      fontWeight: 600,
                      fontSize: "0.875rem",
                    }}
                  />
                </Box>
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
                      Risk Score
                    </Typography>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: theme.palette.text.primary,
                        fontWeight: 600,
                        mt: 0.5,
                      }}
                    >
                      {(emailResult.risk_score * 100).toFixed(1)}%
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
                      Classification
                    </Typography>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: theme.palette.text.primary,
                        fontWeight: 600,
                        mt: 0.5,
                      }}
                    >
                      {emailResult.classification}
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
                      Word Count
                    </Typography>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: theme.palette.text.primary,
                        fontWeight: 600,
                        mt: 0.5,
                      }}
                    >
                      {emailResult.details?.word_count || 0}
                    </Typography>
                  </Box>
                </Box>
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
                  Risk Components
                </Typography>
                <List dense>
                  {Object.entries(emailResult.components || {}).map(
                    ([component, score]) => (
                      <ListItem 
                        key={component} 
                        divider
                        sx={{
                          px: 0,
                          py: 1.5,
                        }}
                      >
                        <ListItemText
                          primary={
                            <Typography 
                              variant="body2"
                              sx={{ 
                                fontWeight: 500,
                                color: theme.palette.text.primary,
                              }}
                            >
                              {component
                                .replace(/_/g, " ")
                                .replace(/\b\w/g, (l) => l.toUpperCase())}
                            </Typography>
                          }
                          secondary={
                            <Typography 
                              variant="body2"
                              sx={{ 
                                color: theme.palette.text.secondary,
                                fontWeight: 600,
                              }}
                            >
                              {(score * 100).toFixed(1)}%
                            </Typography>
                          }
                        />
                      </ListItem>
                    ),
                  )}
                </List>
              </CardContent>
            </Card>
          </Grid>

          {emailResult.indicators && (
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
                    Detected Indicators
                  </Typography>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Typography 
                        variant="subtitle2" 
                        gutterBottom
                        sx={{ 
                          fontWeight: 600,
                          color: theme.palette.text.primary,
                          mb: 2,
                        }}
                      >
                        Psychological Triggers
                      </Typography>
                      {emailResult.indicators.psychological_triggers?.length >
                      0 ? (
                        <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
                          {emailResult.indicators.psychological_triggers.map(
                            (trigger, index) => (
                              <Chip
                                key={index}
                                label={trigger}
                                size="small"
                                color="warning"
                                sx={{ fontWeight: 500 }}
                              />
                            ),
                          )}
                        </Box>
                      ) : (
                        <Typography 
                          variant="body2" 
                          sx={{ color: theme.palette.text.secondary }}
                        >
                          None detected
                        </Typography>
                      )}
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Typography 
                        variant="subtitle2" 
                        gutterBottom
                        sx={{ 
                          fontWeight: 600,
                          color: theme.palette.text.primary,
                          mb: 2,
                        }}
                      >
                        URLs Found ({emailResult.indicators.url_count || 0})
                      </Typography>
                      {emailResult.indicators.urls_found?.length > 0 ? (
                        <Box 
                          sx={{ 
                            maxHeight: 200, 
                            overflow: "auto",
                            backgroundColor: isDark 
                              ? alpha('#fff', 0.05)
                              : alpha('#000', 0.02),
                            p: 2,
                            borderRadius: 1,
                          }}
                        >
                          {emailResult.indicators.urls_found.map((url, index) => (
                            <Typography
                              key={index}
                              variant="body2"
                              sx={{ 
                                wordBreak: "break-all", 
                                mb: 1,
                                color: theme.palette.text.primary,
                                fontFamily: "monospace",
                                fontSize: "0.75rem",
                              }}
                            >
                              {url}
                            </Typography>
                          ))}
                        </Box>
                      ) : (
                        <Typography 
                          variant="body2" 
                          sx={{ color: theme.palette.text.secondary }}
                        >
                          No URLs found
                        </Typography>
                      )}
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      )}
    </>
  );

  const renderImageScanner = () => (
    <>
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
        <Box sx={{ mb: 3 }}>
          <Typography 
            variant="h6" 
            gutterBottom
            sx={{ 
              mb: 1,
              fontWeight: 600,
              color: theme.palette.text.primary,
            }}
          >
            Email Image Analysis
          </Typography>
          <Typography 
            variant="body2" 
            sx={{ color: theme.palette.text.secondary }}
          >
            Upload an image of an email to extract text and analyze for phishing indicators
          </Typography>
        </Box>

        <Paper
          sx={{
            textAlign: "center",
            border: "2px dashed",
            borderColor: isDark 
              ? alpha('#fff', 0.2)
              : alpha('#000', 0.2),
            borderRadius: 2,
            p: 5,
            mb: 2,
            backgroundColor: isDark 
              ? alpha('#fff', 0.02)
              : alpha('#000', 0.01),
            transition: "all 0.3s ease",
            cursor: "pointer",
            '&:hover': {
              borderColor: theme.palette.primary.main,
              backgroundColor: isDark 
                ? alpha(theme.palette.primary.main, 0.05)
                : alpha(theme.palette.primary.main, 0.03),
            },
          }}
          onClick={() => !imageLoading && fileInputRef.current?.click()}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileSelect}
            accept="image/*"
            style={{ display: "none" }}
          />

          {selectedImage ? (
            <Box>
              <ImageIcon
                sx={{ 
                  fontSize: 64, 
                  color: theme.palette.primary.main, 
                  mb: 2 
                }}
              />
              <Typography 
                variant="body1" 
                gutterBottom
                sx={{ 
                  fontWeight: 500,
                  color: theme.palette.text.primary,
                }}
              >
                {selectedImage.name}
              </Typography>
              <Typography 
                variant="body2" 
                sx={{ 
                  color: theme.palette.text.secondary,
                  mb: 2,
                }}
              >
                {(selectedImage.size / 1024 / 1024).toFixed(2)} MB
              </Typography>
              <Button
                variant="outlined"
                onClick={(e) => {
                  e.stopPropagation();
                  fileInputRef.current?.click();
                }}
                startIcon={<Upload />}
                disabled={imageLoading}
                sx={{
                  textTransform: "none",
                  fontWeight: 600,
                }}
              >
                Choose Different Image
              </Button>
            </Box>
          ) : (
            <Box>
              <Upload 
                sx={{ 
                  fontSize: 64, 
                  color: theme.palette.text.secondary, 
                  mb: 2 
                }} 
              />
              <Typography 
                variant="h6" 
                gutterBottom
                sx={{ 
                  fontWeight: 600,
                  color: theme.palette.text.primary,
                }}
              >
                Drop an image here or click to browse
              </Typography>
              <Typography 
                variant="body2" 
                sx={{ 
                  color: theme.palette.text.secondary,
                  mb: 3,
                }}
              >
                Supports PNG, JPG, JPEG, GIF, BMP, TIFF
              </Typography>
              <Button
                variant="contained"
                startIcon={<Upload />}
                disabled={imageLoading}
                sx={{
                  textTransform: "none",
                  fontWeight: 600,
                  px: 4,
                }}
              >
                Choose Image
              </Button>
            </Box>
          )}
        </Paper>

        {imageLoading && (
          <Box 
            sx={{ 
              display: "flex", 
              justifyContent: "center", 
              alignItems: "center",
              mt: 3,
              gap: 2,
            }}
          >
            <CircularProgress size={24} />
            <Typography sx={{ color: theme.palette.text.secondary }}>
              Extracting text and analyzing...
            </Typography>
          </Box>
        )}

        {imageError && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {imageError}
          </Alert>
        )}
      </Paper>

      {imageResult && (
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
                  OCR Results
                </Typography>
                <Box sx={{ display: "flex", flexDirection: "column", gap: 1.5, mb: 2 }}>
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
                      Confidence
                    </Typography>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: theme.palette.text.primary,
                        fontWeight: 600,
                        mt: 0.5,
                      }}
                    >
                      {imageResult.ocr_result?.confidence || 0}%
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
                      Characters
                    </Typography>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: theme.palette.text.primary,
                        fontWeight: 600,
                        mt: 0.5,
                      }}
                    >
                      {imageResult.ocr_result?.character_count || 0}
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
                      Words
                    </Typography>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: theme.palette.text.primary,
                        fontWeight: 600,
                        mt: 0.5,
                      }}
                    >
                      {imageResult.ocr_result?.word_count || 0}
                    </Typography>
                  </Box>
                </Box>
                <Box
                  sx={{
                    mt: 2,
                    p: 2,
                    bgcolor: isDark 
                      ? alpha('#fff', 0.05)
                      : alpha('#000', 0.02),
                    borderRadius: 1,
                    maxHeight: 200,
                    overflow: "auto",
                    border: `1px solid ${isDark ? alpha('#fff', 0.1) : alpha('#000', 0.08)}`,
                  }}
                >
                  <Typography 
                    variant="body2"
                    sx={{ 
                      color: theme.palette.text.primary,
                      fontFamily: "monospace",
                      fontSize: "0.75rem",
                      whiteSpace: "pre-wrap",
                    }}
                  >
                    {imageResult.extracted_text || "No text extracted"}
                  </Typography>
                </Box>
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
                  Phishing Analysis
                </Typography>
                <Box sx={{ mb: 3 }}>
                  <Chip
                    icon={getRiskIcon(imageResult.data?.risk_level)}
                    label={`${imageResult.data?.classification || "UNKNOWN"}`}
                    color={getRiskColor(imageResult.data?.risk_level)}
                    size="medium"
                    sx={{ 
                      px: 1,
                      fontWeight: 600,
                      fontSize: "0.875rem",
                    }}
                  />
                </Box>
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
                      Risk Score
                    </Typography>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: theme.palette.text.primary,
                        fontWeight: 600,
                        mt: 0.5,
                      }}
                    >
                      {((imageResult.data?.risk_score || 0) * 100).toFixed(1)}%
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
                      Classification
                    </Typography>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: theme.palette.text.primary,
                        fontWeight: 600,
                        mt: 0.5,
                      }}
                    >
                      {imageResult.data?.classification || "Unknown"}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {imageResult.data?.indicators && (
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
                    Analysis Details
                  </Typography>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Typography 
                        variant="subtitle2" 
                        gutterBottom
                        sx={{ 
                          fontWeight: 600,
                          color: theme.palette.text.primary,
                          mb: 2,
                        }}
                      >
                        Risk Components
                      </Typography>
                      <Box sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
                        {Object.entries(imageResult.data.components || {}).map(
                          ([component, score]) => (
                            <Box key={component}>
                              <Typography
                                variant="body2"
                                sx={{ 
                                  color: theme.palette.text.primary,
                                  fontWeight: 500,
                                }}
                              >
                                {component
                                  .replace(/_/g, " ")
                                  .replace(/\b\w/g, (l) => l.toUpperCase())}
                              </Typography>
                              <Typography
                                variant="body2"
                                sx={{ 
                                  color: theme.palette.text.secondary,
                                  fontWeight: 600,
                                }}
                              >
                                {(score * 100).toFixed(1)}%
                              </Typography>
                            </Box>
                          ),
                        )}
                      </Box>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Typography 
                        variant="subtitle2" 
                        gutterBottom
                        sx={{ 
                          fontWeight: 600,
                          color: theme.palette.text.primary,
                          mb: 2,
                        }}
                      >
                        Psychological Triggers
                      </Typography>
                      {imageResult.data.indicators.psychological_triggers
                        ?.length > 0 ? (
                        <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
                          {imageResult.data.indicators.psychological_triggers.map(
                            (trigger, index) => (
                              <Chip
                                key={index}
                                label={trigger}
                                size="small"
                                color="warning"
                                sx={{ fontWeight: 500 }}
                              />
                            ),
                          )}
                        </Box>
                      ) : (
                        <Typography 
                          variant="body2" 
                          sx={{ color: theme.palette.text.secondary }}
                        >
                          None detected
                        </Typography>
                      )}
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      )}
    </>
  );

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
          <Shield 
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
            Security Scanner
          </Typography>
        </Box>
        <Typography 
          variant="subtitle1" 
          sx={{ 
            color: theme.palette.text.secondary,
            ml: 7,
          }}
        >
          Comprehensive analysis for URLs, email content, and image-based threats
        </Typography>
      </Box>

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
          value={activeTab}
          onChange={(e, newValue) => setActiveTab(newValue)}
          sx={{
            '& .MuiTab-root': {
              textTransform: "none",
              fontWeight: 600,
              fontSize: "1rem",
              minHeight: 64,
              color: theme.palette.text.secondary,
              '&.Mui-selected': {
                color: theme.palette.primary.main,
              },
            },
          }}
        >
          <Tab icon={<LinkIcon />} label="URL Scanner" iconPosition="start" />
          <Tab icon={<Email />} label="Email Analysis" iconPosition="start" />
          <Tab icon={<ImageIcon />} label="Image Analysis" iconPosition="start" />
        </Tabs>
      </Box>

      <TabPanel value={activeTab} index={0}>
        {renderUrlScanner()}
      </TabPanel>

      <TabPanel value={activeTab} index={1}>
        {renderEmailScanner()}
      </TabPanel>

      <TabPanel value={activeTab} index={2}>
        {renderImageScanner()}
      </TabPanel>
    </Container>
  );
};

export default URLScanner;