import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  CircularProgress,
  Alert,
  LinearProgress,
  Divider,
  Tooltip
} from '@mui/material';
import {
  Air as AirIcon,
  Warning as WarningIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import axios from 'axios';

const AQIDisplay = ({ latitude, longitude }) => {
  const [aqiData, setAqiData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';

  useEffect(() => {
    if (latitude && longitude) {
      fetchAQIData();
    }
  }, [latitude, longitude]);

  const fetchAQIData = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.get(`${API_BASE_URL}/aqi/current`, {
        params: {
          lat: latitude,
          lon: longitude
        }
      });

      setAqiData(response.data.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch AQI data');
      console.error('AQI fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getAQIIcon = (category) => {
    switch (category) {
      case 'Good':
        return <CheckIcon sx={{ fontSize: 40, color: '#00e400' }} />;
      case 'Moderate':
        return <InfoIcon sx={{ fontSize: 40, color: '#ffff00' }} />;
      case 'Unhealthy for Sensitive Groups':
        return <WarningIcon sx={{ fontSize: 40, color: '#ff7e00' }} />;
      case 'Unhealthy':
        return <ErrorIcon sx={{ fontSize: 40, color: '#ff0000' }} />;
      case 'Very Unhealthy':
        return <ErrorIcon sx={{ fontSize: 40, color: '#8f3f97' }} />;
      case 'Hazardous':
        return <ErrorIcon sx={{ fontSize: 40, color: '#7e0023' }} />;
      default:
        return <AirIcon sx={{ fontSize: 40 }} />;
    }
  };

  const getAQIProgress = (aqi) => {
    return Math.min((aqi / 500) * 100, 100);
  };

  if (loading) {
    return (
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box display="flex" alignItems="center" justifyContent="center" py={4}>
            <CircularProgress size={40} />
            <Typography variant="h6" sx={{ ml: 2 }}>
              Fetching Air Quality data...
            </Typography>
          </Box>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Alert severity="warning">
            {error}
          </Alert>
        </CardContent>
      </Card>
    );
  }

  if (!aqiData) {
    return null;
  }

  return (
    <Card
      sx={{
        mb: 3,
        background: `linear-gradient(135deg, ${aqiData.color}15 0%, ${aqiData.color}05 100%)`,
        border: `2px solid ${aqiData.color}`,
        boxShadow: `0 4px 12px ${aqiData.color}40`
      }}
    >
      <CardContent>
        {/* Header */}
        <Box display="flex" alignItems="center" mb={3}>
          <AirIcon sx={{ fontSize: 32, mr: 1, color: 'primary.main' }} />
          <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
            Air Quality Index (AQI)
          </Typography>
        </Box>

        <Grid container spacing={3}>
          {/* Main AQI Display */}
          <Grid item xs={12} md={4}>
            <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                p: 3,
                backgroundColor: 'white',
                borderRadius: 2,
                boxShadow: 2
              }}
            >
              {getAQIIcon(aqiData.category)}
              <Typography
                variant="h2"
                sx={{
                  fontWeight: 'bold',
                  color: aqiData.color,
                  my: 2
                }}
              >
                {aqiData.aqi}
              </Typography>
              <Chip
                label={aqiData.category}
                sx={{
                  backgroundColor: aqiData.color,
                  color: 'white',
                  fontWeight: 'bold',
                  fontSize: '1rem',
                  px: 2,
                  py: 1
                }}
              />
              <Typography variant="caption" sx={{ mt: 2, color: 'text.secondary', fontWeight: 'bold' }}>
                📍 {aqiData.location.city}
              </Typography>
              {aqiData.location.station_name && aqiData.location.station_name !== aqiData.location.city && (
                <Typography 
                  variant="caption" 
                  sx={{ 
                    color: aqiData.location.station_distance_km > 100 ? 'warning.main' : 'text.secondary', 
                    fontSize: '0.7rem',
                    fontWeight: aqiData.location.station_distance_km > 100 ? 'bold' : 'normal'
                  }}
                >
                  Monitoring Station: {aqiData.location.station_name}
                  {aqiData.location.station_distance_km > 0 && (
                    <> ({aqiData.location.station_distance_km} km away)</>
                  )}
                </Typography>
              )}
              <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                Updated: {new Date(aqiData.last_update).toLocaleString()}
              </Typography>
            </Box>
          </Grid>

          {/* Health Information */}
          <Grid item xs={12} md={8}>
            <Box sx={{ height: '100%' }}>
              {/* Distance Warning */}
              {aqiData.location.station_distance_km > 100 && (
                <Alert severity="warning" sx={{ mb: 2 }}>
                  <Typography variant="caption">
                    ⚠️ Note: AQI data is from a monitoring station {aqiData.location.station_distance_km} km away. 
                    Actual air quality at your location may differ. Consider getting a dedicated WAQI API token for more accurate local data.
                  </Typography>
                </Alert>
              )}
              
              {/* AQI Progress Bar */}
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle2" gutterBottom>
                  AQI Level
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={getAQIProgress(aqiData.aqi)}
                  sx={{
                    height: 10,
                    borderRadius: 5,
                    backgroundColor: '#e0e0e0',
                    '& .MuiLinearProgress-bar': {
                      backgroundColor: aqiData.color
                    }
                  }}
                />
                <Box display="flex" justifyContent="space-between" mt={0.5}>
                  <Typography variant="caption">0 (Good)</Typography>
                  <Typography variant="caption">500 (Hazardous)</Typography>
                </Box>
              </Box>

              {/* Health Implications */}
              <Alert
                severity={
                  aqiData.category === 'Good' ? 'success' :
                  aqiData.category === 'Moderate' ? 'info' :
                  aqiData.category === 'Unhealthy for Sensitive Groups' ? 'warning' :
                  'error'
                }
                sx={{ mb: 2 }}
              >
                <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>
                  Health Implications
                </Typography>
                <Typography variant="body2">
                  {aqiData.health_implications}
                </Typography>
              </Alert>

              {/* Cautionary Statement */}
              {aqiData.cautionary_statement !== 'None' && (
                <Alert severity="warning" sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>
                    ⚠️ Cautionary Statement
                  </Typography>
                  <Typography variant="body2">
                    {aqiData.cautionary_statement}
                  </Typography>
                </Alert>
              )}

              {/* Dominant Pollutant */}
              <Box
                sx={{
                  p: 2,
                  backgroundColor: 'white',
                  borderRadius: 1,
                  border: '1px solid #e0e0e0'
                }}
              >
                <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>
                  🔬 Dominant Pollutant
                </Typography>
                <Chip
                  label={aqiData.dominant_pollutant}
                  color="primary"
                  variant="outlined"
                />
              </Box>
            </Box>
          </Grid>

          {/* Pollutant Details */}
          {Object.keys(aqiData.pollutants).length > 0 && (
            <Grid item xs={12}>
              <Divider sx={{ my: 2 }} />
              <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2 }}>
                📊 Pollutant Breakdown
              </Typography>
              <Grid container spacing={2}>
                {Object.entries(aqiData.pollutants).map(([key, pollutant]) => (
                  <Grid item xs={6} sm={4} md={2} key={key}>
                    <Tooltip title={pollutant.name} arrow>
                      <Card
                        sx={{
                          textAlign: 'center',
                          p: 2,
                          backgroundColor: 'white',
                          '&:hover': {
                            boxShadow: 3,
                            transform: 'translateY(-2px)',
                            transition: 'all 0.3s'
                          }
                        }}
                      >
                        <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 'bold' }}>
                          {pollutant.name}
                        </Typography>
                        <Typography variant="h6" sx={{ fontWeight: 'bold', color: 'primary.main', my: 1 }}>
                          {pollutant.value}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {pollutant.unit}
                        </Typography>
                      </Card>
                    </Tooltip>
                  </Grid>
                ))}
              </Grid>
            </Grid>
          )}

          {/* AQI Scale Reference */}
          <Grid item xs={12}>
            <Divider sx={{ my: 2 }} />
            <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 2 }}>
              📋 AQI Scale Reference
            </Typography>
            <Grid container spacing={1}>
              {[
                { range: '0-50', category: 'Good', color: '#00e400' },
                { range: '51-100', category: 'Moderate', color: '#ffff00' },
                { range: '101-150', category: 'Unhealthy for Sensitive', color: '#ff7e00' },
                { range: '151-200', category: 'Unhealthy', color: '#ff0000' },
                { range: '201-300', category: 'Very Unhealthy', color: '#8f3f97' },
                { range: '301+', category: 'Hazardous', color: '#7e0023' }
              ].map((scale, index) => (
                <Grid item xs={6} sm={4} md={2} key={index}>
                  <Box
                    sx={{
                      p: 1,
                      backgroundColor: scale.color,
                      color: index < 2 ? '#000' : '#fff',
                      borderRadius: 1,
                      textAlign: 'center'
                    }}
                  >
                    <Typography variant="caption" sx={{ fontWeight: 'bold', display: 'block' }}>
                      {scale.range}
                    </Typography>
                    <Typography variant="caption" sx={{ fontSize: '0.7rem' }}>
                      {scale.category}
                    </Typography>
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default AQIDisplay;
