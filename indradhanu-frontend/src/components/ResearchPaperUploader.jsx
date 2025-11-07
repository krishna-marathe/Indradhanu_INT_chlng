import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Button,
  Box,
  Typography,
  Paper,
  LinearProgress,
  Alert,
  Chip,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  CloudUpload,
  Description,
  PictureAsPdf,
  Article,
  Clear
} from '@mui/icons-material';
import { toast } from 'react-toastify';

const ResearchPaperUploader = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file type
      const allowedTypes = ['.pdf', '.docx', '.txt'];
      const fileExt = '.' + file.name.split('.').pop().toLowerCase();
      
      if (!allowedTypes.includes(fileExt)) {
        setError('Please select a PDF, DOCX, or TXT file.');
        return;
      }
      
      // Validate file size (50MB limit)
      if (file.size > 50 * 1024 * 1024) {
        setError('File size must be less than 50MB.');
        return;
      }
      
      setSelectedFile(file);
      setError(null);
    }
  };

  const handlePaperUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('http://127.0.0.1:5000/upload_research_paper', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      
      console.log('🔍 Upload response received:', data);
      console.log('🔍 Has analysis?', !!data.analysis);
      console.log('🔍 Analysis content:', data.analysis);

      if (response.ok) {
        toast.success('✅ Research paper analyzed successfully!');
        
        console.log('📤 Storing in localStorage and navigating...');
        console.log('📤 Data to store:', JSON.stringify(data, null, 2));
        
        // Store the result and navigate to dashboard
        localStorage.setItem('lastUpload', JSON.stringify(data));
        
        console.log('📤 Navigating to dashboard with state:', { paperAnalysis: data });
        navigate('/dashboard', { state: { paperAnalysis: data } });
      } else {
        throw new Error(data.error || 'Analysis failed');
      }
    } catch (err) {
      console.error('Upload error:', err);
      setError(err.message || 'Failed to analyze research paper. Please try again.');
      toast.error('❌ Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
    setError(null);
  };

  const getFileIcon = (filename) => {
    const ext = filename.split('.').pop().toLowerCase();
    switch (ext) {
      case 'pdf':
        return <PictureAsPdf color="error" />;
      case 'docx':
        return <Article color="primary" />;
      case 'txt':
        return <Description color="action" />;
      default:
        return <Description />;
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Paper sx={{ p: 3, textAlign: 'center', border: '2px dashed', borderColor: 'primary.light' }}>
        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1 }}>
          📚 Research Paper Analyzer
        </Typography>
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Upload research documents (PDF, DOCX, TXT) for automatic analysis and summarization
        </Typography>

        {/* File Input */}
        <Box sx={{ mb: 3 }}>
          <input
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={handleFileChange}
            style={{ display: 'none' }}
            id="research-paper-upload"
          />
          <label htmlFor="research-paper-upload">
            <Button
              variant="outlined"
              component="span"
              startIcon={<CloudUpload />}
              sx={{ mb: 2 }}
              disabled={loading}
            >
              Choose Research Paper
            </Button>
          </label>
        </Box>

        {/* Selected File Display */}
        {selectedFile && (
          <Box sx={{ mb: 3 }}>
            <Paper sx={{ p: 2, bgcolor: 'grey.50', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                {getFileIcon(selectedFile.name)}
                <Box sx={{ textAlign: 'left' }}>
                  <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
                    {selectedFile.name}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {formatFileSize(selectedFile.size)}
                  </Typography>
                </Box>
              </Box>
              <Tooltip title="Remove file">
                <IconButton onClick={clearFile} size="small">
                  <Clear />
                </IconButton>
              </Tooltip>
            </Paper>
          </Box>
        )}

        {/* Supported Formats */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
            Supported formats:
          </Typography>
          <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1 }}>
            <Chip label="PDF" size="small" color="error" variant="outlined" />
            <Chip label="DOCX" size="small" color="primary" variant="outlined" />
            <Chip label="TXT" size="small" color="default" variant="outlined" />
          </Box>
        </Box>

        {/* Error Display */}
        {error && (
          <Alert severity="error" sx={{ mb: 2, textAlign: 'left' }}>
            {error}
          </Alert>
        )}

        {/* Upload Button */}
        <Button
          variant="contained"
          onClick={handlePaperUpload}
          disabled={!selectedFile || loading}
          startIcon={<Description />}
          sx={{ minWidth: 200 }}
        >
          {loading ? 'Analyzing...' : 'Analyze Paper'}
        </Button>

        {/* Loading Progress */}
        {loading && (
          <Box sx={{ mt: 2 }}>
            <LinearProgress />
            <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
              Extracting and analyzing document content...
            </Typography>
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default ResearchPaperUploader;