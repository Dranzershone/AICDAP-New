import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Chip,
  TextField,
  InputAdornment,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  Tabs,
  Tab,
  Snackbar,
  Skeleton,
} from "@mui/material";
import {
  Add,
  Search,
  Edit,
  Delete,
  PersonAdd,
  CloudUpload,
  Download,
  FilterList,
  Group,
  Email,
  Business,
} from "@mui/icons-material";
import { CSVImport } from "../../../components/CSVImport";
import { EmployeeService } from "../../../services/employeeService";

const TabPanel = ({ children, value, index, ...other }) => (
  <div
    role="tabpanel"
    hidden={value !== index}
    id={`employee-tabpanel-${index}`}
    aria-labelledby={`employee-tab-${index}`}
    {...other}
  >
    {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
  </div>
);

const EmployeeManagement = () => {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    total: 0,
    active: 0,
    departments: 0,
    thisMonth: 0,
  });

  const [tabValue, setTabValue] = useState(0);
  const [searchTerm, setSearchTerm] = useState("");
  const [departmentFilter, setDepartmentFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [addEmployeeOpen, setAddEmployeeOpen] = useState(false);
  const [editEmployeeOpen, setEditEmployeeOpen] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "success",
  });
  const [actionLoading, setActionLoading] = useState(false);

  const [newEmployee, setNewEmployee] = useState({
    name: "",
    email: "",
    department: "",
  });

  const departments = [
    ...new Set(employees.map((emp) => emp.department).filter(Boolean)),
  ];

  // Load employees on component mount
  useEffect(() => {
    loadEmployees();
    loadStats();
  }, []);

  const loadEmployees = async () => {
    try {
      setLoading(true);
      const { data, error } = await EmployeeService.getAllEmployees();
      if (error) {
        setSnackbar({
          open: true,
          message: `Error loading employees: ${error}`,
          severity: "error",
        });
      } else {
        setEmployees(data || []);
      }
    } catch (error) {
      setSnackbar({
        open: true,
        message: "Unexpected error loading employees",
        severity: "error",
      });
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const { data, error } = await EmployeeService.getEmployeeStats();
      if (!error && data) {
        setStats(data);
      }
    } catch (error) {
      console.error("Error loading stats:", error);
    }
  };

  const filteredEmployees = employees.filter((employee) => {
    const matchesSearch =
      employee.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      employee.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesDepartment =
      !departmentFilter || employee.department === departmentFilter;
    const matchesStatus = !statusFilter || employee.status === statusFilter;

    return matchesSearch && matchesDepartment && matchesStatus;
  });

  const getStatusColor = (status) => {
    switch (status) {
      case "active":
        return "success";
      case "inactive":
        return "default";
      default:
        return "default";
    }
  };

  const handleAddEmployee = async () => {
    try {
      setActionLoading(true);
      const { data, error } = await EmployeeService.createEmployee({
        ...newEmployee,
        status: "active",
      });

      if (error) {
        setSnackbar({
          open: true,
          message: `Error adding employee: ${error}`,
          severity: "error",
        });
      } else {
        setEmployees([data, ...employees]);
        setNewEmployee({ name: "", email: "", department: "" });
        setAddEmployeeOpen(false);
        setSnackbar({
          open: true,
          message: "Employee added successfully",
          severity: "success",
        });
        loadStats(); // Refresh stats
      }
    } catch (error) {
      setSnackbar({
        open: true,
        message: "Unexpected error adding employee",
        severity: "error",
      });
    } finally {
      setActionLoading(false);
    }
  };

  const handleEditEmployee = async () => {
    try {
      setActionLoading(true);
      const { data, error } = await EmployeeService.updateEmployee(
        selectedEmployee.id,
        selectedEmployee,
      );

      if (error) {
        setSnackbar({
          open: true,
          message: `Error updating employee: ${error}`,
          severity: "error",
        });
      } else {
        setEmployees(
          employees.map((emp) => (emp.id === selectedEmployee.id ? data : emp)),
        );
        setEditEmployeeOpen(false);
        setSelectedEmployee(null);
        setSnackbar({
          open: true,
          message: "Employee updated successfully",
          severity: "success",
        });
        loadStats(); // Refresh stats
      }
    } catch (error) {
      setSnackbar({
        open: true,
        message: "Unexpected error updating employee",
        severity: "error",
      });
    } finally {
      setActionLoading(false);
    }
  };

  const handleDeleteEmployee = async (id) => {
    if (!window.confirm("Are you sure you want to delete this employee?")) {
      return;
    }

    try {
      const { error } = await EmployeeService.deleteEmployee(id);

      if (error) {
        setSnackbar({
          open: true,
          message: `Error deleting employee: ${error}`,
          severity: "error",
        });
      } else {
        setEmployees(employees.filter((emp) => emp.id !== id));
        setSnackbar({
          open: true,
          message: "Employee deleted successfully",
          severity: "success",
        });
        loadStats(); // Refresh stats
      }
    } catch (error) {
      setSnackbar({
        open: true,
        message: "Unexpected error deleting employee",
        severity: "error",
      });
    }
  };

  const handleEmployeesImported = (importedEmployees) => {
    if (importedEmployees && importedEmployees.length > 0) {
      setEmployees([...importedEmployees, ...employees]);
      setSnackbar({
        open: true,
        message: `${importedEmployees.length} employees imported successfully`,
        severity: "success",
      });
      loadStats(); // Refresh stats
    }
  };

  const exportEmployees = () => {
    const csv = [
      "name,email,department,status,created_at",
      ...employees.map(
        (emp) =>
          `"${emp.name}","${emp.email}","${emp.department}","${emp.status}","${emp.created_at}"`,
      ),
    ].join("\n");

    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "employees.csv";
    link.click();
    window.URL.revokeObjectURL(url);
  };

  const statsCards = [
    {
      title: "Total Employees",
      value: stats.total,
      icon: <Group />,
      color: "#1976d2",
    },
    {
      title: "Active Employees",
      value: stats.active,
      icon: <PersonAdd />,
      color: "#2e7d32",
    },
    {
      title: "Departments",
      value: stats.departments,
      icon: <Business />,
      color: "#ed6c02",
    },
    {
      title: "This Month",
      value: stats.thisMonth,
      icon: <Add />,
      color: "#9c27b0",
    },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography
        variant="h4"
        gutterBottom
        sx={{ color: "text.primary", fontWeight: "bold" }}
      >
        Employee Management
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {statsCards.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card
              sx={{
                bgcolor: "background.paper",
                border: "1px solid",
                borderColor: "divider",
              }}
            >
              <CardContent>
                <Box
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                  }}
                >
                  <Box>
                    <Typography
                      variant="h4"
                      sx={{ color: "text.primary", fontWeight: "bold" }}
                    >
                      {stat.value}
                    </Typography>
                    <Typography
                      variant="body2"
                      sx={{ color: "text.secondary" }}
                    >
                      {stat.title}
                    </Typography>
                  </Box>
                  <Box
                    sx={{
                      bgcolor: stat.color,
                      borderRadius: 2,
                      p: 1,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    {stat.icon}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Main Content */}
      <Card
        sx={{
          bgcolor: "background.paper",
          border: "1px solid",
          borderColor: "divider",
        }}
      >
        <CardContent>
          <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
            <Tabs
              value={tabValue}
              onChange={(e, newValue) => setTabValue(newValue)}
              sx={{
                "& .MuiTab-root": {
                  color: "text.secondary",
                  "&.Mui-selected": {
                    color: "primary.main",
                  },
                },
                "& .MuiTabs-indicator": {
                  backgroundColor: "primary.main",
                },
              }}
            >
              <Tab label="Employee List" />
              <Tab label="Import CSV" />
            </Tabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            {/* Filters and Actions */}
            <Box
              sx={{
                display: "flex",
                gap: 2,
                mb: 3,
                flexWrap: "wrap",
                alignItems: "center",
              }}
            >
              <TextField
                placeholder="Search employees..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                size="small"
                sx={{
                  minWidth: 200,
                  "& .MuiOutlinedInput-root": {
                    color: "text.primary",
                    "& fieldset": { borderColor: "divider" },
                  },
                }}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Search sx={{ color: "text.secondary" }} />
                    </InputAdornment>
                  ),
                }}
              />

              <FormControl size="small" sx={{ minWidth: 150 }}>
                <InputLabel sx={{ color: "text.secondary" }}>
                  Department
                </InputLabel>
                <Select
                  value={departmentFilter}
                  onChange={(e) => setDepartmentFilter(e.target.value)}
                  sx={{
                    color: "text.primary",
                    "& .MuiOutlinedInput-notchedOutline": {
                      borderColor: "divider",
                    },
                  }}
                >
                  <MenuItem value="">All Departments</MenuItem>
                  {departments.map((dept) => (
                    <MenuItem key={dept} value={dept}>
                      {dept}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel sx={{ color: "text.secondary" }}>Status</InputLabel>
                <Select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  sx={{
                    color: "text.primary",
                    "& .MuiOutlinedInput-notchedOutline": {
                      borderColor: "divider",
                    },
                  }}
                >
                  <MenuItem value="">All Status</MenuItem>
                  <MenuItem value="active">Active</MenuItem>
                  <MenuItem value="inactive">Inactive</MenuItem>
                </Select>
              </FormControl>

              <Box sx={{ flexGrow: 1 }} />

              <Button
                variant="outlined"
                startIcon={<Download />}
                onClick={exportEmployees}
                sx={{ color: "text.primary", borderColor: "divider" }}
              >
                Export
              </Button>

              <Button
                variant="contained"
                startIcon={<Add />}
                onClick={() => setAddEmployeeOpen(true)}
                sx={{ bgcolor: "#1976d2" }}
              >
                Add Employee
              </Button>
            </Box>

            {/* Employee Table */}
            <TableContainer
              component={Paper}
              sx={{ bgcolor: "background.paper" }}
            >
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell
                      sx={{ color: "text.primary", fontWeight: "bold" }}
                    >
                      Name
                    </TableCell>
                    <TableCell
                      sx={{ color: "text.primary", fontWeight: "bold" }}
                    >
                      Email
                    </TableCell>
                    <TableCell
                      sx={{ color: "text.primary", fontWeight: "bold" }}
                    >
                      Department
                    </TableCell>
                    <TableCell
                      sx={{ color: "text.primary", fontWeight: "bold" }}
                    >
                      Status
                    </TableCell>
                    <TableCell
                      sx={{ color: "text.primary", fontWeight: "bold" }}
                    >
                      Date Added
                    </TableCell>
                    <TableCell
                      sx={{ color: "text.primary", fontWeight: "bold" }}
                    >
                      Actions
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {loading ? (
                    // Loading skeleton rows
                    Array.from({ length: 5 }).map((_, index) => (
                      <TableRow key={index}>
                        <TableCell>
                          <Skeleton
                            variant="text"
                            sx={{ bgcolor: "grey.200" }}
                          />
                        </TableCell>
                        <TableCell>
                          <Skeleton
                            variant="text"
                            sx={{ bgcolor: "grey.200" }}
                          />
                        </TableCell>
                        <TableCell>
                          <Skeleton
                            variant="text"
                            sx={{ bgcolor: "grey.200" }}
                          />
                        </TableCell>
                        <TableCell>
                          <Skeleton
                            variant="rounded"
                            width={60}
                            height={24}
                            sx={{ bgcolor: "grey.200" }}
                          />
                        </TableCell>
                        <TableCell>
                          <Skeleton
                            variant="text"
                            sx={{ bgcolor: "grey.200" }}
                          />
                        </TableCell>
                        <TableCell>
                          <Skeleton
                            variant="circular"
                            width={32}
                            height={32}
                            sx={{
                              bgcolor: "grey.200",
                              mr: 1,
                              display: "inline-block",
                            }}
                          />
                          <Skeleton
                            variant="circular"
                            width={32}
                            height={32}
                            sx={{
                              bgcolor: "grey.200",
                              display: "inline-block",
                            }}
                          />
                        </TableCell>
                      </TableRow>
                    ))
                  ) : filteredEmployees.length === 0 ? (
                    <TableRow>
                      <TableCell
                        colSpan={6}
                        sx={{
                          textAlign: "center",
                          color: "text.secondary",
                          py: 4,
                        }}
                      >
                        {searchTerm || departmentFilter || statusFilter
                          ? "No employees found matching your criteria"
                          : "No employees found. Add some employees or import from CSV."}
                      </TableCell>
                    </TableRow>
                  ) : (
                    filteredEmployees.map((employee) => (
                      <TableRow key={employee.id} hover>
                        <TableCell sx={{ color: "text.primary" }}>
                          {employee.name}
                        </TableCell>
                        <TableCell sx={{ color: "text.secondary" }}>
                          {employee.email}
                        </TableCell>
                        <TableCell sx={{ color: "text.secondary" }}>
                          {employee.department}
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={employee.status}
                            color={getStatusColor(employee.status)}
                            size="small"
                          />
                        </TableCell>
                        <TableCell sx={{ color: "text.secondary" }}>
                          {employee.created_at
                            ? new Date(employee.created_at).toLocaleDateString()
                            : "N/A"}
                        </TableCell>
                        <TableCell>
                          <IconButton
                            size="small"
                            onClick={() => {
                              setSelectedEmployee(employee);
                              setEditEmployeeOpen(true);
                            }}
                            sx={{ color: "#90caf9" }}
                          >
                            <Edit />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => handleDeleteEmployee(employee.id)}
                            sx={{ color: "#f44336" }}
                          >
                            <Delete />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <CSVImport onEmployeesImported={handleEmployeesImported} />
          </TabPanel>
        </CardContent>
      </Card>

      {/* Add Employee Dialog */}
      <Dialog
        open={addEmployeeOpen}
        onClose={() => setAddEmployeeOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle
          sx={{ bgcolor: "background.paper", color: "text.primary" }}
        >
          Add New Employee
        </DialogTitle>
        <DialogContent sx={{ bgcolor: "background.paper", pt: 2 }}>
          <TextField
            fullWidth
            label="Name"
            value={newEmployee.name}
            onChange={(e) =>
              setNewEmployee({ ...newEmployee, name: e.target.value })
            }
            sx={{
              mb: 2,
              "& .MuiOutlinedInput-root": { color: "text.primary" },
              "& .MuiInputLabel-root": { color: "text.secondary" },
            }}
          />
          <TextField
            fullWidth
            label="Email"
            type="email"
            value={newEmployee.email}
            onChange={(e) =>
              setNewEmployee({ ...newEmployee, email: e.target.value })
            }
            sx={{
              mb: 2,
              "& .MuiOutlinedInput-root": { color: "text.primary" },
              "& .MuiInputLabel-root": { color: "text.secondary" },
            }}
          />
          <TextField
            fullWidth
            label="Department"
            value={newEmployee.department}
            onChange={(e) =>
              setNewEmployee({ ...newEmployee, department: e.target.value })
            }
            sx={{
              "& .MuiOutlinedInput-root": { color: "text.primary" },
              "& .MuiInputLabel-root": { color: "text.secondary" },
            }}
          />
        </DialogContent>
        <DialogActions sx={{ bgcolor: "background.paper" }}>
          <Button
            onClick={() => setAddEmployeeOpen(false)}
            sx={{ color: "text.primary" }}
          >
            Cancel
          </Button>
          <Button
            onClick={handleAddEmployee}
            variant="contained"
            disabled={
              !newEmployee.name ||
              !newEmployee.email ||
              !newEmployee.department ||
              actionLoading
            }
          >
            {actionLoading ? "Adding..." : "Add"}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit Employee Dialog */}
      <Dialog
        open={editEmployeeOpen}
        onClose={() => setEditEmployeeOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle
          sx={{ bgcolor: "background.paper", color: "text.primary" }}
        >
          Edit Employee
        </DialogTitle>
        <DialogContent sx={{ bgcolor: "background.paper", pt: 2 }}>
          {selectedEmployee && (
            <>
              <TextField
                fullWidth
                label="Name"
                value={selectedEmployee.name}
                onChange={(e) =>
                  setSelectedEmployee({
                    ...selectedEmployee,
                    name: e.target.value,
                  })
                }
                sx={{
                  mb: 2,
                  "& .MuiOutlinedInput-root": { color: "text.primary" },
                  "& .MuiInputLabel-root": {
                    color: "text.secondary",
                  },
                }}
              />
              <TextField
                fullWidth
                label="Email"
                type="email"
                value={selectedEmployee.email}
                onChange={(e) =>
                  setSelectedEmployee({
                    ...selectedEmployee,
                    email: e.target.value,
                  })
                }
                sx={{
                  mb: 2,
                  "& .MuiOutlinedInput-root": { color: "text.primary" },
                  "& .MuiInputLabel-root": {
                    color: "text.secondary",
                  },
                }}
              />
              <TextField
                fullWidth
                label="Department"
                value={selectedEmployee.department}
                onChange={(e) =>
                  setSelectedEmployee({
                    ...selectedEmployee,
                    department: e.target.value,
                  })
                }
                sx={{
                  mb: 2,
                  "& .MuiOutlinedInput-root": { color: "text.primary" },
                  "& .MuiInputLabel-root": {
                    color: "text.secondary",
                  },
                }}
              />
              <FormControl fullWidth>
                <InputLabel sx={{ color: "rgba(255, 255, 255, 0.7)" }}>
                  Status
                </InputLabel>
                <Select
                  value={selectedEmployee.status}
                  onChange={(e) =>
                    setSelectedEmployee({
                      ...selectedEmployee,
                      status: e.target.value,
                    })
                  }
                  sx={{
                    color: "text.primary",
                    "& .MuiOutlinedInput-notchedOutline": {
                      borderColor: "divider",
                    },
                  }}
                >
                  <MenuItem value="active">Active</MenuItem>
                  <MenuItem value="inactive">Inactive</MenuItem>
                </Select>
              </FormControl>
            </>
          )}
        </DialogContent>
        <DialogActions sx={{ bgcolor: "background.paper" }}>
          <Button
            onClick={() => setEditEmployeeOpen(false)}
            sx={{ color: "text.primary" }}
          >
            Cancel
          </Button>
          <Button
            onClick={handleEditEmployee}
            variant="contained"
            disabled={actionLoading}
          >
            {actionLoading ? "Updating..." : "Update"}
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
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default EmployeeManagement;
