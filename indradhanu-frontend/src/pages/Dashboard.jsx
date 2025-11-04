import React from 'react';
import { Box, Toolbar } from '@mui/material';
import AnalyticsDashboard from '../components/AnalyticsDashboard';

const Dashboard = () => {
  return (
    <Box>
      {/* Add toolbar spacing for fixed navbar */}
      <Toolbar />
      <AnalyticsDashboard />
    </Box>
  );
};

export default Dashboard;