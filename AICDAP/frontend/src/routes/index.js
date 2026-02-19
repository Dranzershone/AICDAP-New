import React from "react";
import { Routes, Route } from "react-router-dom";
import {
  Home,
  About,
  Dashboard,
  Campaigns,
  CampaignBuilder,
  EmployeeManagement,
  Analytics,
  URLScanner,
  InsiderThreat,
} from "../pages";
import { Login, SignUp, ForgotPassword } from "../pages/auth";
import AdminLayout from "../layouts/AdminLayout";
import ProtectedRoute from "../components/ProtectedRoute";
import DemoPage from "../pages/demo/DemoPage";

// Placeholder components for routes that don't have pages yet
const UserGuide = () => (
  <div style={{ padding: "2rem", textAlign: "center", color: "#fff" }}>
    <h2>User Guide</h2>
    <p>User guide page coming soon...</p>
  </div>
);

const Pricing = () => (
  <div style={{ padding: "2rem", textAlign: "center", color: "#fff" }}>
    <h2>Pricing</h2>
    <p>Pricing page coming soon...</p>
  </div>
);

const NotFound = () => (
  <div style={{ padding: "2rem", textAlign: "center", color: "#fff" }}>
    <h2>404 - Page Not Found</h2>
    <p>The page you're looking for doesn't exist.</p>
  </div>
);

const AppRoutes = () => {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/guide" element={<UserGuide />} />
      <Route path="/pricing" element={<Pricing />} />
      <Route path="/demo" element={<DemoPage />} />
      <Route
        path="/login"
        element={
          <ProtectedRoute requireAuth={false}>
            <Login />
          </ProtectedRoute>
        }
      />
      <Route
        path="/signup"
        element={
          <ProtectedRoute requireAuth={false}>
            <SignUp />
          </ProtectedRoute>
        }
      />
      <Route
        path="/forgot-password"
        element={
          <ProtectedRoute requireAuth={false}>
            <ForgotPassword />
          </ProtectedRoute>
        }
      />

      {/* Admin Routes */}
      <Route
        path="/admin"
        element={
          <ProtectedRoute>
            <AdminLayout>
              <Dashboard />
            </AdminLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/dashboard"
        element={
          <ProtectedRoute>
            <AdminLayout>
              <Dashboard />
            </AdminLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/security"
        element={
          <ProtectedRoute>
            <AdminLayout>
              <div style={{ padding: "2rem", color: "#fff" }}>
                <h2>Security</h2>
                <p>Security page coming soon...</p>
              </div>
            </AdminLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/analytics"
        element={
          <ProtectedRoute>
            <AdminLayout>
              <Analytics />
            </AdminLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/users"
        element={
          <ProtectedRoute>
            <AdminLayout>
              <div style={{ padding: "2rem", color: "#fff" }}>
                <h2>Users</h2>
                <p>Users page coming soon...</p>
              </div>
            </AdminLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/employees"
        element={
          <ProtectedRoute>
            <AdminLayout>
              <EmployeeManagement />
            </AdminLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/reports"
        element={
          <ProtectedRoute>
            <AdminLayout>
              <div style={{ padding: "2rem", color: "#fff" }}>
                <h2>Reports</h2>
                <p>Reports page coming soon...</p>
              </div>
            </AdminLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/settings"
        element={
          <ProtectedRoute>
            <AdminLayout>
              <div style={{ padding: "2rem", color: "#fff" }}>
                <h2>Settings</h2>
                <p>Settings page coming soon...</p>
              </div>
            </AdminLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/url-scanner"
        element={
          <ProtectedRoute>
            <AdminLayout>
              <URLScanner />
            </AdminLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/insider"
        element={
          <ProtectedRoute>
            <AdminLayout>
              <InsiderThreat />
            </AdminLayout>
          </ProtectedRoute>
        }
      />
      <Route path="/url-scanner" element={<URLScanner />} />
      <Route
        path="/admin/campaigns"
        element={
          <ProtectedRoute>
            <AdminLayout>
              <Campaigns />
            </AdminLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/campaigns/create"
        element={
          <ProtectedRoute>
            <AdminLayout>
              <CampaignBuilder />
            </AdminLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/campaigns/:id"
        element={
          <ProtectedRoute>
            <AdminLayout>
              <div style={{ padding: "2rem", color: "#fff" }}>
                <h2>Campaign Details</h2>
                <p>Campaign details page coming soon...</p>
              </div>
            </AdminLayout>
          </ProtectedRoute>
        }
      />

      {/* 404 Route */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default AppRoutes;
