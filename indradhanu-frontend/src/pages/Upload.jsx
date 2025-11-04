import React, { useState } from 'react';
import { Box, Container, Toolbar } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import FileUpload from '../components/FileUpload';
import AnalyticsDashboard from '../components/AnalyticsDashboard';

const Upload = () => {
  const [uploadResult, setUploadResult] = useState(null);
  const navigate = useNavigate();

  const handleUploadSuccess = (result) => {
    setUploadResult(result);
    // Optionally navigate to dashboard after a delay
    // setTimeout(() => navigate('/dashboard'), 3000);
  };

  return (
    <Box>
      {/* Add toolbar spacing for fixed navbar */}
      <Toolbar />
      
      <Container maxWidth="lg" sx={{ py: 4 }}>
        {!uploadResult ? (
          <FileUpload onUploadSuccess={handleUploadSuccess} />
        ) : (
          <AnalyticsDashboard currentUpload={uploadResult} />
        )}
      </Container>
    </Box>
  );
};

export default Upload;