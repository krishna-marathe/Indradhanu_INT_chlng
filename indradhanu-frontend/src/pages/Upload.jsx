import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  Toolbar
} from '@mui/material';
import FileUpload from '../components/FileUpload';
import { toast } from 'react-toastify';

const Upload = () => {
  const navigate = useNavigate();

  const handleUploadSuccess = (result) => {
    console.log('📊 Upload successful:', result);
    toast.success('✅ File uploaded and analyzed successfully!');
    
    // Store the result and navigate to dashboard
    localStorage.setItem('lastUpload', JSON.stringify(result));
    navigate('/dashboard', { state: { uploadData: result } });
  };

  return (
    <Box>
      {/* Add toolbar spacing for fixed navbar */}
      <Toolbar />
      
      <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
        <Box
          sx={{
            textAlign: 'center',
            mb: 5,
            animation: 'fadeIn 0.6s ease-out',
            '@keyframes fadeIn': {
              from: { opacity: 0, transform: 'translateY(-20px)' },
              to: { opacity: 1, transform: 'translateY(0)' },
            },
          }}
        >
          <Typography 
            variant="h3" 
            component="h1" 
            gutterBottom 
            sx={{ 
              fontWeight: 700,
              background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              mb: 2,
            }}
          >
            📊 Upload & Analyze Your Data
          </Typography>
          <Typography 
            variant="h6" 
            align="center" 
            color="text.secondary" 
            sx={{ 
              maxWidth: 600, 
              mx: 'auto',
              lineHeight: 1.6,
            }}
          >
            Upload CSV, Excel, or JSON files for comprehensive data visualization and statistical analysis
          </Typography>
        </Box>
        
        <Paper 
          elevation={4}
          sx={{ 
            p: 5,
            borderRadius: 3,
            background: 'linear-gradient(to bottom, #ffffff 0%, #f5f7fa 100%)',
          }}
        >
          <FileUpload onUploadSuccess={handleUploadSuccess} />
        </Paper>
      </Container>
    </Box>
  );
};

export default Upload;