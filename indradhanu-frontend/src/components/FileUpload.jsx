import React, { useState, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  Button,
  LinearProgress,
  Alert,
  Chip,
  Snackbar,
} from '@mui/material';
import { CloudUpload, CheckCircle, Error, Analytics } from '@mui/icons-material';
import { useDropzone } from 'react-dropzone';
import { uploadFile, testConnection } from '../services/api';
import { toast } from 'react-toastify';

const FileUpload = ({ onUploadSuccess }) => {
  const navigate = useNavigate();
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [selectedFile, setSelectedFile] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [backendConnected, setBackendConnected] = useState(false);

  // Test Flask backend connection on component mount
  useEffect(() => {
    const checkBackend = async () => {
      const connected = await testConnection();
      setBackendConnected(connected);
      if (!connected) {
        setError('Cannot connect to Flask backend. Please ensure the server is running on port 5000.');
      }
    };
    checkBackend();
  }, []);

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    setError(null);
    setSuccess(false);
    
    if (rejectedFiles.length > 0) {
      const rejectedFile = rejectedFiles[0];
      if (rejectedFile.errors.some(e => e.code === 'file-too-large')) {
        setError('File is too large. Maximum size is 100MB.');
      } else {
        setError('Please select a valid CSV, XLSX, or JSON file.');
      }
      return;
    }

    if (acceptedFiles.length > 0) {
      setSelectedFile(acceptedFiles[0]);
      console.log('📁 File selected:', acceptedFiles[0].name);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/json': ['.json'],
    },
    multiple: false,
    maxSize: 100 * 1024 * 1024, // 100MB
  });

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first.');
      return;
    }

    if (!backendConnected) {
      setError('Backend connection failed. Please check if Flask server is running.');
      return;
    }

    console.log('🚀 Starting file upload process...');
    setUploading(true);
    setUploadProgress(0);
    setError(null);
    setSuccess(false);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      console.log('📤 Uploading to Flask /upload endpoint...');
      const response = await uploadFile(formData, (progressEvent) => {
        const progress = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        setUploadProgress(progress);
      });

      console.log('✅ Upload successful! Response:', response.data);
      
      // Extract upload_id from response (using filename as ID for now)
      const uploadId = response.data.filename || response.data.upload_id;
      const uploadData = {
        ...response.data,
        upload_id: uploadId,
        timestamp: new Date().toISOString(),
      };

      setUploadResult(uploadData);
      setSuccess(true);
      
      // Store upload data in localStorage for persistence
      localStorage.setItem('lastUpload', JSON.stringify(uploadData));
      
      toast.success('🎉 File uploaded and analyzed successfully!');
      
      // Call parent callback if provided
      if (onUploadSuccess) {
        onUploadSuccess(uploadData);
      }

      // Navigate to Analytics Dashboard after 2 seconds
      setTimeout(() => {
        console.log('🧭 Navigating to Analytics Dashboard...');
        navigate('/dashboard', { 
          state: { 
            uploadData: uploadData,
            fromUpload: true 
          } 
        });
      }, 2000);
      
    } catch (error) {
      console.error('❌ Upload error:', error);
      const errorMessage = error.response?.data?.error || 
                          error.response?.data?.message || 
                          error.message || 
                          'Upload failed. Please try again.';
      setError(errorMessage);
      toast.error(`Upload failed: ${errorMessage}`);
    } finally {
      setUploading(false);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const resetForm = () => {
    setSelectedFile(null);
    setUploadProgress(0);
    setError(null);
    setSuccess(false);
    setUploadResult(null);
  };

  return (
    <Box sx={{ maxWidth: 600, mx: 'auto', p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Upload Environmental Data
      </Typography>
      
      <Typography variant="body1" color="text.secondary" align="center" sx={{ mb: 3 }}>
        Upload your CSV, XLSX, or JSON file to get instant analytics and insights.
      </Typography>

      {/* Backend Connection Status */}
      <Alert 
        severity={backendConnected ? "success" : "warning"} 
        sx={{ mb: 2 }}
      >
        Flask Backend: {backendConnected ? "✅ Connected" : "⚠️ Disconnected"}
      </Alert>

      <Paper
        {...getRootProps()}
        elevation={isDragActive ? 8 : 2}
        sx={{
          p: 5,
          border: '3px dashed',
          borderColor: isDragActive ? 'primary.main' : 'grey.300',
          backgroundColor: isDragActive ? 'primary.light' : 'background.paper',
          cursor: 'pointer',
          textAlign: 'center',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          transform: isDragActive ? 'scale(1.02)' : 'scale(1)',
          '&:hover': {
            borderColor: 'primary.main',
            backgroundColor: 'action.hover',
            transform: 'scale(1.01)',
            boxShadow: 6,
          },
        }}
      >
        <input {...getInputProps()} />
        <Box
          sx={{
            animation: isDragActive ? 'pulse 1s infinite' : 'none',
            '@keyframes pulse': {
              '0%, 100%': { transform: 'scale(1)' },
              '50%': { transform: 'scale(1.1)' },
            },
          }}
        >
          <CloudUpload 
            sx={{ 
              fontSize: 64, 
              color: isDragActive ? 'primary.dark' : 'primary.main', 
              mb: 2,
              transition: 'all 0.3s ease',
            }} 
          />
        </Box>
        
        {isDragActive ? (
          <Typography variant="h5" color="primary.dark" fontWeight="bold">
            📂 Drop the file here...
          </Typography>
        ) : (
          <>
            <Typography variant="h5" gutterBottom fontWeight="600">
              Drag and drop your file here
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
              or click to browse files
            </Typography>
            <Typography variant="caption" color="text.secondary" display="block">
              Maximum file size: 100MB
            </Typography>
          </>
        )}
        
        <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center', gap: 1 }}>
          <Chip 
            label="CSV" 
            size="medium" 
            color="primary" 
            variant="outlined"
            sx={{ fontWeight: 600 }}
          />
          <Chip 
            label="XLSX" 
            size="medium" 
            color="primary" 
            variant="outlined"
            sx={{ fontWeight: 600 }}
          />
          <Chip 
            label="JSON" 
            size="medium" 
            color="primary" 
            variant="outlined"
            sx={{ fontWeight: 600 }}
          />
        </Box>
      </Paper>

      {selectedFile && (
        <Paper 
          elevation={3}
          sx={{ 
            p: 3, 
            mt: 3, 
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            borderRadius: 2,
            animation: 'slideIn 0.3s ease-out',
            '@keyframes slideIn': {
              from: { opacity: 0, transform: 'translateY(-10px)' },
              to: { opacity: 1, transform: 'translateY(0)' },
            },
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <CheckCircle sx={{ fontSize: 40 }} />
            <Box sx={{ flexGrow: 1 }}>
              <Typography variant="h6" fontWeight="600">
                {selectedFile.name}
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.9 }}>
                📦 {formatFileSize(selectedFile.size)}
              </Typography>
            </Box>
          </Box>
        </Paper>
      )}

      {error && (
        <Alert severity="error" sx={{ mt: 2 }} icon={<Error />}>
          {error}
        </Alert>
      )}

      {success && uploadResult && (
        <Alert severity="success" sx={{ mt: 2 }} icon={<Analytics />}>
          <Typography variant="subtitle2">Analysis Complete!</Typography>
          <Typography variant="body2">
            Processed {uploadResult.rows} rows, {uploadResult.columns} columns
          </Typography>
          <Typography variant="body2">
            Generated {uploadResult.charts?.length || 0} charts
          </Typography>
          <Typography variant="body2" sx={{ mt: 1, fontStyle: 'italic' }}>
            Redirecting to dashboard...
          </Typography>
        </Alert>
      )}

      {uploading && (
        <Box sx={{ mt: 2 }}>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Uploading and analyzing... {uploadProgress}%
          </Typography>
          <LinearProgress variant="determinate" value={uploadProgress} />
        </Box>
      )}

      <Box sx={{ display: 'flex', gap: 2, mt: 4 }}>
        <Button
          variant="contained"
          size="large"
          fullWidth
          onClick={handleUpload}
          disabled={!selectedFile || uploading || !backendConnected}
          startIcon={uploading ? null : <CloudUpload />}
          sx={{
            py: 1.5,
            fontSize: '1.1rem',
            fontWeight: 600,
            background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
            boxShadow: '0 3px 5px 2px rgba(33, 203, 243, .3)',
            transition: 'all 0.3s ease',
            '&:hover': {
              background: 'linear-gradient(45deg, #1976D2 30%, #1CB5E0 90%)',
              transform: 'translateY(-2px)',
              boxShadow: '0 6px 10px 2px rgba(33, 203, 243, .4)',
            },
            '&:disabled': {
              background: 'grey.300',
            },
          }}
        >
          {uploading ? '⚡ Analyzing...' : '🚀 Upload & Analyze'}
        </Button>
        
        {selectedFile && !uploading && (
          <Button
            variant="outlined"
            size="large"
            onClick={resetForm}
            sx={{
              py: 1.5,
              px: 3,
              fontSize: '1rem',
              fontWeight: 600,
              borderWidth: 2,
              '&:hover': {
                borderWidth: 2,
                transform: 'translateY(-2px)',
              },
            }}
          >
            Reset
          </Button>
        )}
      </Box>

      {/* Success Snackbar */}
      <Snackbar
        open={success}
        autoHideDuration={3000}
        onClose={() => setSuccess(false)}
        message="🎉 Upload successful! Redirecting to dashboard..."
      />
    </Box>
  );
};

export default FileUpload;