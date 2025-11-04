import axios from "axios";

const API_BASE = "http://127.0.0.1:5000";

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE,
  timeout: 60000, // 60 seconds timeout for large files
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.data);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API functions
export const uploadFile = (formData, onUploadProgress) => {
  console.log('📤 Uploading file to Flask backend...');
  return api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: (progressEvent) => {
      const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
      console.log(`Upload progress: ${progress}%`);
      if (onUploadProgress) {
        onUploadProgress(progressEvent);
      }
    },
  });
};

export const getReport = (filename) => {
  console.log(`📥 Downloading report for: ${filename}`);
  return api.get(`/report/${filename}`, {
    responseType: 'blob',
  });
};

export const getUploads = () => {
  console.log('📋 Fetching upload history...');
  return api.get('/uploads');
};

export const getUploadById = (uploadId) => {
  console.log(`🔍 Fetching upload details for: ${uploadId}`);
  return api.get(`/uploads/${uploadId}`);
};

// Test connection to Flask backend
export const testConnection = async () => {
  try {
    const response = await api.get('/');
    console.log('✅ Flask backend connection successful:', response.data);
    return true;
  } catch (error) {
    console.error('❌ Flask backend connection failed:', error.message);
    return false;
  }
};

export default api;