import React, { useState, useRef } from "react";
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Chip,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  Divider,
} from "@mui/material";
import {
  CloudUpload,
  Delete,
  Download,
  CheckCircle,
  Error,
  Warning,
  Visibility,
} from "@mui/icons-material";
import Papa from "papaparse";
import { EmployeeService } from "../../services/employeeService";

const CSVImport = ({ onEmployeesImported, maxFileSize = 5 * 1024 * 1024 }) => {
  const [file, setFile] = useState(null);
  const [csvData, setCsvData] = useState([]);
  const [validData, setValidData] = useState([]);
  const [errors, setErrors] = useState([]);
  const [warnings, setWarnings] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [showErrors, setShowErrors] = useState(false);
  const [isImporting, setIsImporting] = useState(false);
  const [existingEmails, setExistingEmails] = useState([]);
  const fileInputRef = useRef(null);

  const requiredColumns = ["name", "email", "department"];

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const checkDuplicateEmails = async (employees) => {
    try {
      const { data: allEmployees } = await EmployeeService.getAllEmployees();
      const existingEmailSet = new Set(
        allEmployees?.map((emp) => emp.email.toLowerCase()) || [],
      );
      setExistingEmails(existingEmailSet);
      return existingEmailSet;
    } catch (error) {
      console.error("Error checking existing emails:", error);
      return new Set();
    }
  };

  const validateRow = (row, index, existingEmailSet) => {
    const errors = [];
    const warnings = [];

    // Check required fields
    if (!row.name || row.name.trim() === "") {
      errors.push(`Row ${index + 2}: Name is required`);
    }

    if (!row.email || row.email.trim() === "") {
      errors.push(`Row ${index + 2}: Email is required`);
    } else if (!validateEmail(row.email.trim())) {
      errors.push(`Row ${index + 2}: Invalid email format`);
    }

    if (!row.department || row.department.trim() === "") {
      warnings.push(`Row ${index + 2}: Department is empty`);
    }

    // Check for duplicate emails in the current dataset
    const duplicateIndex = csvData.findIndex(
      (item, i) =>
        i !== index &&
        item.email &&
        item.email.toLowerCase() === row.email?.toLowerCase(),
    );

    if (duplicateIndex !== -1) {
      warnings.push(
        `Row ${index + 2}: Duplicate email found (also in row ${duplicateIndex + 2})`,
      );
    }

    // Check for existing emails in database
    if (row.email && existingEmailSet.has(row.email.toLowerCase().trim())) {
      errors.push(`Row ${index + 2}: Email already exists in database`);
    }

    return { errors, warnings };
  };

  const processCSV = async (file) => {
    setIsProcessing(true);
    setErrors([]);
    setWarnings([]);
    setValidData([]);

    // First, check existing emails in database
    const existingEmailSet = await checkDuplicateEmails();

    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      transformHeader: (header) => {
        // Normalize headers to lowercase and remove extra spaces
        return header.toLowerCase().trim();
      },
      transform: (value) => {
        // Clean up values
        return value.trim();
      },
      complete: (results) => {
        const data = results.data;
        const parseErrors = results.errors;

        // Check for parsing errors
        if (parseErrors.length > 0) {
          setErrors(
            parseErrors.map((error) => `Parse error: ${error.message}`),
          );
          setIsProcessing(false);
          return;
        }

        // Check if required columns exist
        const headers = results.meta.fields || [];
        const missingColumns = requiredColumns.filter(
          (col) =>
            !headers.some(
              (header) => header.toLowerCase() === col.toLowerCase(),
            ),
        );

        if (missingColumns.length > 0) {
          setErrors([`Missing required columns: ${missingColumns.join(", ")}`]);
          setIsProcessing(false);
          return;
        }

        setCsvData(data);

        // Validate data
        const allErrors = [];
        const allWarnings = [];
        const valid = [];

        data.forEach((row, index) => {
          const validation = validateRow(row, index, existingEmailSet);
          allErrors.push(...validation.errors);
          allWarnings.push(...validation.warnings);

          // If no critical errors, add to valid data
          if (validation.errors.length === 0) {
            valid.push({
              name: row.name.trim(),
              email: row.email.toLowerCase().trim(),
              department: row.department?.trim() || "Unassigned",
              rowNumber: index + 2,
            });
          }
        });

        setErrors(allErrors);
        setWarnings(allWarnings);
        setValidData(valid);
        setIsProcessing(false);
      },
      error: (error) => {
        setErrors([`Failed to parse CSV: ${error.message}`]);
        setIsProcessing(false);
      },
    });
  };

  const handleFileSelect = (event) => {
    const selectedFile = event.target.files[0];

    if (!selectedFile) return;

    // Validate file type
    if (!selectedFile.name.toLowerCase().endsWith(".csv")) {
      setErrors(["Please select a CSV file"]);
      return;
    }

    // Validate file size
    if (selectedFile.size > maxFileSize) {
      setErrors([
        `File size must be less than ${Math.round(maxFileSize / (1024 * 1024))}MB`,
      ]);
      return;
    }

    setFile(selectedFile);
    processCSV(selectedFile);
  };

  const handleImport = async () => {
    if (validData.length === 0) return;

    setIsImporting(true);

    try {
      // Insert employees into Supabase
      const { data, error } =
        await EmployeeService.bulkCreateEmployees(validData);

      if (error) {
        setErrors([`Failed to import employees: ${error}`]);
        setIsImporting(false);
        return;
      }

      // Notify parent component of successful import
      onEmployeesImported(data);
      handleReset();
    } catch (error) {
      setErrors([`Unexpected error during import: ${error.message}`]);
    } finally {
      setIsImporting(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setCsvData([]);
    setValidData([]);
    setErrors([]);
    setWarnings([]);
    setShowPreview(false);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const downloadTemplate = () => {
    const template =
      "name,email,department\nJohn Doe,john.doe@company.com,Engineering\nJane Smith,jane.smith@company.com,Marketing\nBob Johnson,bob.johnson@company.com,Sales";
    const blob = new Blob([template], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "employee_template.csv";
    link.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <Box>
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Import Employees from CSV
          </Typography>

          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Upload a CSV file containing employee information. Required columns:
            Name, Email, Department
          </Typography>

          <Box sx={{ display: "flex", gap: 2, mb: 2 }}>
            <input
              type="file"
              accept=".csv"
              onChange={handleFileSelect}
              ref={fileInputRef}
              style={{ display: "none" }}
            />

            <Button
              variant="outlined"
              startIcon={<CloudUpload />}
              onClick={() => fileInputRef.current?.click()}
              disabled={isProcessing || isImporting}
            >
              Choose CSV File
            </Button>

            <Button
              variant="text"
              startIcon={<Download />}
              onClick={downloadTemplate}
            >
              Download Template
            </Button>
          </Box>

          {file && (
            <Box sx={{ mb: 2 }}>
              <Chip
                label={`${file.name} (${Math.round(file.size / 1024)}KB)`}
                onDelete={handleReset}
                deleteIcon={<Delete />}
                variant="outlined"
              />
            </Box>
          )}

          {isProcessing && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" gutterBottom>
                Processing CSV file...
              </Typography>
              <LinearProgress />
            </Box>
          )}

          {errors.length > 0 && (
            <Alert
              severity="error"
              sx={{ mb: 2 }}
              action={
                errors.length > 3 && (
                  <Button
                    size="small"
                    onClick={() => setShowErrors(true)}
                    startIcon={<Visibility />}
                  >
                    View All
                  </Button>
                )
              }
            >
              <Typography variant="subtitle2" gutterBottom>
                {errors.length} Error{errors.length > 1 ? "s" : ""} Found
              </Typography>
              {errors.slice(0, 3).map((error, index) => (
                <Typography key={index} variant="body2">
                  {error}
                </Typography>
              ))}
              {errors.length > 3 && (
                <Typography variant="body2">
                  ...and {errors.length - 3} more
                </Typography>
              )}
            </Alert>
          )}

          {warnings.length > 0 && (
            <Alert severity="warning" sx={{ mb: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                {warnings.length} Warning{warnings.length > 1 ? "s" : ""}
              </Typography>
              {warnings.slice(0, 2).map((warning, index) => (
                <Typography key={index} variant="body2">
                  {warning}
                </Typography>
              ))}
              {warnings.length > 2 && (
                <Typography variant="body2">
                  ...and {warnings.length - 2} more
                </Typography>
              )}
            </Alert>
          )}

          {validData.length > 0 && (
            <Box>
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  mb: 2,
                }}
              >
                <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                  <CheckCircle color="success" />
                  <Typography variant="subtitle1">
                    {validData.length} valid employee
                    {validData.length > 1 ? "s" : ""} ready to import
                  </Typography>
                </Box>

                <Box sx={{ display: "flex", gap: 1 }}>
                  <Button
                    variant="outlined"
                    size="small"
                    onClick={() => setShowPreview(true)}
                    startIcon={<Visibility />}
                  >
                    Preview
                  </Button>
                  <Button
                    variant="contained"
                    onClick={handleImport}
                    startIcon={<CloudUpload />}
                    disabled={isImporting}
                  >
                    {isImporting
                      ? "Importing..."
                      : `Import ${validData.length} Employee${validData.length > 1 ? "s" : ""}`}
                  </Button>
                </Box>
              </Box>
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Preview Dialog */}
      <Dialog
        open={showPreview}
        onClose={() => setShowPreview(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Preview Import Data</DialogTitle>
        <DialogContent>
          <TableContainer component={Paper} sx={{ maxHeight: 400 }}>
            <Table stickyHeader size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Email</TableCell>
                  <TableCell>Department</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {validData.map((employee, index) => (
                  <TableRow key={index}>
                    <TableCell>{employee.name}</TableCell>
                    <TableCell>{employee.email}</TableCell>
                    <TableCell>{employee.department}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowPreview(false)}>Close</Button>
          <Button
            variant="contained"
            onClick={() => {
              setShowPreview(false);
              handleImport();
            }}
          >
            Import All
          </Button>
        </DialogActions>
      </Dialog>

      {/* Errors Dialog */}
      <Dialog
        open={showErrors}
        onClose={() => setShowErrors(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            <Error color="error" />
            All Errors ({errors.length})
          </Box>
        </DialogTitle>
        <DialogContent>
          <List>
            {errors.map((error, index) => (
              <React.Fragment key={index}>
                <ListItem>
                  <ListItemText primary={error} />
                </ListItem>
                {index < errors.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowErrors(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default CSVImport;
