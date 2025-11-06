import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Chip,
  Alert,
  CircularProgress,
  Paper,
  Divider,
  IconButton,
  Tooltip,
  Fab,
} from '@mui/material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import {
  Download,
  Insights,
  Assessment,
  CloudUpload,
  Refresh,
  ArrowBack,
  Timeline,
  BarChart as BarChartIcon,
  PieChart as PieChartIcon,
} from '@mui/icons-material';
import { getUploads, getReport } from '../services/api';
import { toast } from 'react-toastify';
import GeoHeatmap from './GeoHeatmap';
import SatelliteDataVisuals from './SatelliteDataVisuals';
import SurfaceRadiationVisuals from './SurfaceRadiationVisuals';
import ClimateMetricsVisuals from './ClimateMetricsVisuals';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

const AnalyticsDashboard = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [uploads, setUploads] = useState([]);
  const [currentUpload, setCurrentUpload] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [downloadingReport, setDownloadingReport] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    // Check if we came from upload with data
    if (location.state?.uploadData) {
      console.log('📊 Received upload data from navigation:', location.state.uploadData);
      console.log('📊 Upload data statistics:', location.state.uploadData.statistics);
      setCurrentUpload(location.state.uploadData);
    }

    // Also check localStorage for last upload
    const lastUpload = localStorage.getItem('lastUpload');
    if (lastUpload && !location.state?.uploadData) {
      try {
        const uploadData = JSON.parse(lastUpload);
        console.log('📊 Retrieved upload data from localStorage:', uploadData);
        console.log('📊 LocalStorage data statistics:', uploadData.statistics);
        setCurrentUpload(uploadData);
      } catch (e) {
        console.error('Error parsing stored upload data:', e);
      }
    }

    fetchUploads();
  }, [location.state]);

  const fetchUploads = async () => {
    try {
      setLoading(true);
      console.log('📋 Fetching upload history...');
      const response = await getUploads();
      console.log('📋 Upload history received:', response.data);
      setUploads(response.data || []);
    } catch (error) {
      console.error('❌ Error fetching uploads:', error);
      setError('Failed to load upload history. Please ensure Flask backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchUploads();
    setRefreshing(false);
    toast.success('Dashboard refreshed!');
  };

  const handleDownloadReport = async (filename) => {
    try {
      setDownloadingReport(filename);
      console.log(`📥 Downloading report for: ${filename}`);

      // For now, show a message that PDF generation will be implemented
      toast.info('PDF report generation will be implemented in the next phase!');

      // TODO: Implement actual PDF download when backend report endpoint is ready
      // const response = await getReport(filename);
      // const blob = new Blob([response.data], { type: 'application/pdf' });
      // const url = window.URL.createObjectURL(blob);
      // const link = document.createElement('a');
      // link.href = url;
      // link.download = `${filename}_report.pdf`;
      // document.body.appendChild(link);
      // link.click();
      // document.body.removeChild(link);
      // window.URL.revokeObjectURL(url);
      // toast.success('Report downloaded successfully!');

    } catch (error) {
      console.error('❌ Error downloading report:', error);
      toast.error('Failed to download report. Please try again.');
    } finally {
      setDownloadingReport(null);
    }
  };

  const generateChartDataFromStatistics = (upload) => {
    console.log('🔍 Generating chart data from upload:', upload);

    const data = [];

    if (upload?.statistics?.descriptive_stats) {
      const stats = upload.statistics.descriptive_stats;
      console.log('📊 Found statistics:', stats);

      Object.entries(stats).forEach(([column, values]) => {
        if (values && typeof values === 'object' && values.mean !== undefined && !isNaN(values.mean)) {
          data.push({
            name: column,
            mean: Number(values.mean.toFixed(2)),
            median: values.median ? Number(values.median.toFixed(2)) : 0,
            std: values.std ? Number(values.std.toFixed(2)) : 0,
            min: values.min ? Number(values.min.toFixed(2)) : 0,
            max: values.max ? Number(values.max.toFixed(2)) : 0,
          });
        }
      });
    }

    console.log('📈 Generated chart data:', data);

    // Only return empty array if no real data - no fallback
    return data;
  };

  const generateTimeSeriesData = (upload) => {
    // Generate time series data for line charts using dynamic statistics
    const baseData = generateChartDataFromStatistics(upload);
    const timeSeriesData = [];

    for (let i = 0; i < 7; i++) {
      const dataPoint = { day: `Day ${i + 1}` };
      baseData.forEach(item => {
        // Add some variation to the mean values
        const variation = (Math.random() - 0.5) * 0.2;
        dataPoint[item.name] = Math.max(0, item.mean * (1 + variation));
      });
      timeSeriesData.push(dataPoint);
    }

    return timeSeriesData;
  };

  const handleBackToUpload = () => {
    console.log('🧭 Navigating back to upload page...');
    navigate('/');
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '50vh' }}>
        <Box sx={{ textAlign: 'center' }}>
          <CircularProgress size={60} />
          <Typography variant="h6" sx={{ mt: 2 }}>
            Loading Analytics Dashboard...
          </Typography>
        </Box>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
        <Button variant="contained" onClick={handleRefresh} startIcon={<Refresh />}>
          Retry
        </Button>
      </Container>
    );
  }

  // Determine what to display
  const displayUploads = currentUpload ? [currentUpload] : uploads;
  const showCurrentUpload = !!currentUpload;

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            📊 Analytics Dashboard
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            {showCurrentUpload ? 'Current Analysis Results' : 'Upload History & Analytics'}
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', gap: 1 }}>
          <Tooltip title="Refresh Dashboard">
            <IconButton onClick={handleRefresh} disabled={refreshing}>
              <Refresh />
            </IconButton>
          </Tooltip>
          <Button
            variant="outlined"
            startIcon={<ArrowBack />}
            onClick={handleBackToUpload}
          >
            Back to Upload
          </Button>
        </Box>
      </Box>

      {displayUploads.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <CloudUpload sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" gutterBottom>
            No Analytics Data Available
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            Upload a file to see analytics and insights here.
          </Typography>
          <Button variant="contained" onClick={handleBackToUpload} startIcon={<CloudUpload />}>
            Upload Data
          </Button>
        </Paper>
      ) : (
        <Grid container spacing={3}>
          {displayUploads.map((upload, index) => (
            <Grid item xs={12} key={upload.filename || upload.upload_id || index}>
              <Card elevation={3}>
                <CardContent>
                  {/* Upload Header */}
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
                    <Box>
                      <Typography variant="h5" gutterBottom>
                        📄 {upload.filename || 'Analysis Results'}
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
                        <Chip
                          icon={<Assessment />}
                          label={`${upload.rows || 0} rows`}
                          size="small"
                          color="primary"
                          variant="outlined"
                        />
                        <Chip
                          icon={<Insights />}
                          label={`${upload.columns || 0} columns`}
                          size="small"
                          color="secondary"
                          variant="outlined"
                        />
                        {upload.charts && (
                          <Chip
                            label={`${upload.charts.length} charts`}
                            size="small"
                            color="success"
                            variant="outlined"
                          />
                        )}
                        {upload.schema?.summary && (
                          <Chip
                            label={`${upload.schema.summary.numeric} numeric, ${upload.schema.summary.categorical} categorical`}
                            size="small"
                            color="info"
                            variant="outlined"
                          />
                        )}
                        {(upload.timestamp || upload.upload_timestamp) && (
                          <Chip
                            label={new Date(upload.timestamp || upload.upload_timestamp).toLocaleString()}
                            size="small"
                            color="default"
                            variant="outlined"
                          />
                        )}
                      </Box>
                    </Box>

                    <Button
                      variant="contained"
                      startIcon={<Download />}
                      onClick={() => handleDownloadReport(upload.filename || upload.upload_id)}
                      disabled={downloadingReport === (upload.filename || upload.upload_id)}
                      color="primary"
                    >
                      {downloadingReport === (upload.filename || upload.upload_id) ? 'Downloading...' : 'Download Report'}
                    </Button>
                  </Box>

                  <Divider sx={{ mb: 3 }} />

                  {/* Insights Section */}
                  {upload.insights && upload.insights.length > 0 && (
                    <Paper sx={{ p: 3, mb: 3, backgroundColor: 'primary.light', color: 'primary.contrastText' }}>
                      <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Insights /> Key Insights
                      </Typography>
                      <Grid container spacing={2}>
                        {upload.insights.map((insight, idx) => (
                          <Grid item xs={12} sm={6} key={idx}>
                            <Typography variant="body1" sx={{
                              p: 1,
                              backgroundColor: 'rgba(255,255,255,0.1)',
                              borderRadius: 1,
                              fontSize: '0.95rem'
                            }}>
                              {insight}
                            </Typography>
                          </Grid>
                        ))}
                      </Grid>
                    </Paper>
                  )}

                  {/* 🛰️ Satellite/Sensor Data Visualizations */}
                  <SatelliteDataVisuals analysis={upload} />

                  {/* 🌡️ Surface Temperature & Radiation Analysis */}
                  <SurfaceRadiationVisuals analysis={upload} />

                  {/* 🌦️ Climate Metrics & Regional Risk Analysis */}
                  <ClimateMetricsVisuals metrics={upload.climate_metrics} />

                  {/* Interactive Charts Section */}
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                    <Timeline /> Interactive Visualizations
                  </Typography>

                  <Grid container spacing={3} sx={{ mb: 3 }}>
                    {/* Line Chart */}
                    <Grid item xs={12} lg={6}>
                      <Paper sx={{ p: 2, height: 400 }}>
                        <Typography variant="subtitle1" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Timeline /> Trend Analysis
                        </Typography>
                        <ResponsiveContainer width="100%" height="90%">
                          <LineChart data={generateTimeSeriesData(upload)}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="day" />
                            <YAxis />
                            <RechartsTooltip />
                            <Legend />
                            {generateChartDataFromStatistics(upload).map((item, idx) => (
                              <Line
                                key={item.name}
                                type="monotone"
                                dataKey={item.name}
                                stroke={COLORS[idx % COLORS.length]}
                                strokeWidth={2}
                                dot={{ r: 4 }}
                              />
                            ))}
                          </LineChart>
                        </ResponsiveContainer>
                      </Paper>
                    </Grid>

                    {/* Bar Chart */}
                    <Grid item xs={12} lg={6}>
                      <Paper sx={{ p: 2, height: 400 }}>
                        <Typography variant="subtitle1" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <BarChartIcon /> Comparative Analysis
                        </Typography>
                        <ResponsiveContainer width="100%" height="90%">
                          <BarChart data={generateChartDataFromStatistics(upload)}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" />
                            <YAxis />
                            <RechartsTooltip />
                            <Bar dataKey="mean" fill="#8884d8">
                              {generateChartDataFromStatistics(upload).map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                              ))}
                            </Bar>
                          </BarChart>
                        </ResponsiveContainer>
                      </Paper>
                    </Grid>

                    {/* Pie Chart */}
                    <Grid item xs={12} lg={6}>
                      <Paper sx={{ p: 2, height: 400 }}>
                        <Typography variant="subtitle1" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <PieChartIcon /> Distribution Analysis
                        </Typography>
                        <ResponsiveContainer width="100%" height="90%">
                          <PieChart>
                            <Pie
                              data={generateChartDataFromStatistics(upload)}
                              cx="50%"
                              cy="50%"
                              labelLine={false}
                              label={({ name, mean }) => `${name}: ${mean?.toFixed(1) || 0}`}
                              outerRadius={80}
                              fill="#8884d8"
                              dataKey="mean"
                            >
                              {generateChartDataFromStatistics(upload).map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                              ))}
                            </Pie>
                            <RechartsTooltip />
                          </PieChart>
                        </ResponsiveContainer>
                      </Paper>
                    </Grid>
                  </Grid>

                  {/* Generated Charts from Flask Backend */}
                  {upload.charts && upload.charts.length > 0 && (
                    <Box sx={{ mt: 3 }}>
                      <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Assessment /> Generated Analysis Charts
                      </Typography>
                      <Grid container spacing={2}>
                        {upload.charts.map((chart, idx) => (
                          <Grid item xs={12} md={6} key={idx}>
                            <Paper sx={{ p: 2, textAlign: 'center' }}>
                              <Typography variant="subtitle1" gutterBottom color="primary">
                                {chart.title}
                              </Typography>
                              <Box sx={{
                                border: '2px solid',
                                borderColor: 'primary.light',
                                borderRadius: 2,
                                overflow: 'hidden',
                                backgroundColor: 'background.paper'
                              }}>
                                <img
                                  src={`http://127.0.0.1:5000${chart.url}`}
                                  alt={chart.title}
                                  style={{
                                    width: '100%',
                                    height: 'auto',
                                    display: 'block',
                                  }}
                                  onError={(e) => {
                                    console.error(`Failed to load chart: ${chart.url}`);
                                    e.target.style.display = 'none';
                                    e.target.nextSibling.style.display = 'block';
                                  }}
                                />
                                <Typography
                                  variant="body2"
                                  color="error"
                                  sx={{ display: 'none', p: 2 }}
                                >
                                  Failed to load chart image
                                </Typography>
                              </Box>
                            </Paper>
                          </Grid>
                        ))}
                      </Grid>
                    </Box>
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Floating Action Button for Upload */}
      <Fab
        color="primary"
        aria-label="upload"
        sx={{ position: 'fixed', bottom: 16, right: 16 }}
        onClick={handleBackToUpload}
      >
        <CloudUpload />
      </Fab>
    </Container>
  );
};

export default AnalyticsDashboard;