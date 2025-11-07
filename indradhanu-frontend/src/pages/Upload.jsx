import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Toolbar
} from '@mui/material';
import FileUpload from '../components/FileUpload';
import ResearchPaperUploader from '../components/ResearchPaperUploader';
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
      
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
          📊 Upload & Analyze Your Data
        </Typography>
        <Typography variant="body1" align="center" color="text.secondary" sx={{ mb: 4 }}>
          Upload environmental datasets or research documents for comprehensive analysis and insights
        </Typography>
        
        <Grid container spacing={4}>
          {/* Dataset Uploader */}
          <Grid item xs={12} lg={6}>
            <Paper sx={{ p: 4, height: 'fit-content' }}>
              <Typography variant="h5" component="h2" gutterBottom align="center">
                📈 Dataset Analysis
              </Typography>
              <Typography variant="body2" align="center" color="text.secondary" sx={{ mb: 3 }}>
                Upload CSV, Excel, or JSON files for data visualization and statistical analysis
              </Typography>
              <FileUpload onUploadSuccess={handleUploadSuccess} />
            </Paper>
          </Grid>
          
          {/* Research Paper Uploader */}
          <Grid item xs={12} lg={6}>
            <Paper sx={{ p: 4, height: 'fit-content' }}>
              <Typography variant="h5" component="h2" gutterBottom align="center">
                📚 Document Analysis
              </Typography>
              <Typography variant="body2" align="center" color="text.secondary" sx={{ mb: 3 }}>
                Upload research papers, reports, or documents for content analysis and summarization
              </Typography>
              <ResearchPaperUploader />
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Upload;