import React from 'react';
import { Box } from '@mui/material';
import ModernSidebar from '../../components/ModernSidebar';
import ModernDashboard from './ModernDashboard';

const DemoPage = () => {
  return (
    <Box sx={{
      display: 'flex',
      minHeight: '100vh',
      bgcolor: '#ffffff'
    }}>
      {/* Sidebar */}
      <ModernSidebar selectedSection="Index Management" />

      {/* Main Content */}
      <Box sx={{
        flex: 1,
        overflow: 'auto'
      }}>
        <ModernDashboard />
      </Box>
    </Box>
  );
};

export default DemoPage;
