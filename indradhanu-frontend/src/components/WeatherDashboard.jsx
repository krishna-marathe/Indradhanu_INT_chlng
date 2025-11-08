import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  TextField,
  CircularProgress,
  Alert,
  Chip,
  Paper,
  Autocomplete,
  InputAdornment,
  Divider
} from '@mui/material';
import {
  CloudQueue as WeatherIcon,
  CloudQueue,
  Thermostat as TempIcon,
  Speed as PressureIcon,
  Air as WindIcon,
  Air,
  WaterDrop as RainIcon,
  WaterDrop,
  LocationOn as LocationIcon,
  Refresh as RefreshIcon,
  Search as SearchIcon,
  Public as GlobalIcon
} from '@mui/icons-material';
import axios from 'axios';
import AQIDisplay from './AQIDisplay';

const WeatherDashboard = () => {
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [coordinates, setCoordinates] = useState({
    latitude: 52.52,
    longitude: 13.41
  });
  const [locationSearch, setLocationSearch] = useState('');
  const [locationOptions, setLocationOptions] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [popularLocations, setPopularLocations] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [locationLoading, setLocationLoading] = useState(true);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';

  const fetchWeatherData = async (analyze = false) => {
    setLoading(true);
    setError(null);

    try {
      let response;
      
      if (analyze) {
        // Fetch with analysis and charts
        response = await axios.post(`${API_BASE_URL}/weather/analyze`, {
          latitude: coordinates.latitude,
          longitude: coordinates.longitude,
          hours: 6
        });
        setWeatherData(response.data.data);
      } else {
        // Fetch basic weather data
        response = await axios.get(`${API_BASE_URL}/weather/current`, {
          params: {
            lat: coordinates.latitude,
            lon: coordinates.longitude,
            hours: 6
          }
        });
        setWeatherData(response.data.data);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch weather data');
      console.error('Weather fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCoordinateChange = (field) => (event) => {
    setCoordinates(prev => ({
      ...prev,
      [field]: parseFloat(event.target.value) || 0
    }));
  };

  const getCurrentLocation = () => {
    if (navigator.geolocation) {
      setLocationLoading(true);
      setError(null);
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const newCoords = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          };
          setCoordinates(newCoords);
          setSelectedLocation({
            name: 'Current Location',
            clean_name: 'Your Current Location',
            latitude: newCoords.latitude,
            longitude: newCoords.longitude
          });
          setLocationSearch('Your Current Location');
          setLocationLoading(false);
          console.log('📍 Location updated:', newCoords);
        },
        (error) => {
          console.error('Geolocation error:', error);
          setError('Unable to get current location. Please check your browser permissions.');
          setLocationLoading(false);
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 0
        }
      );
    } else {
      setError('Geolocation is not supported by this browser');
    }
  };

  const searchLocations = async (query) => {
    if (!query || query.length < 2) {
      setLocationOptions([]);
      return;
    }

    setSearchLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/geocoding/search`, {
        params: { q: query, limit: 8 }
      });
      setLocationOptions(response.data.results || []);
    } catch (err) {
      console.error('Location search error:', err);
      setLocationOptions([]);
    } finally {
      setSearchLoading(false);
    }
  };

  const loadPopularLocations = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/geocoding/popular`);
      setPopularLocations(response.data.locations || []);
    } catch (err) {
      console.error('Popular locations error:', err);
    }
  };

  const handleLocationSelect = (location) => {
    if (location) {
      setCoordinates({
        latitude: location.latitude,
        longitude: location.longitude
      });
      setSelectedLocation(location);
      setLocationSearch(location.clean_name || location.name);
    }
  };

  const handlePopularLocationClick = (location) => {
    handleLocationSelect(location);
  };

  // Load popular locations and auto-fetch current location on component mount
  useEffect(() => {
    loadPopularLocations();
    
    // Automatically get current location on page load
    setLocationLoading(true);
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const newCoords = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          };
          setCoordinates(newCoords);
          setSelectedLocation({
            name: 'Current Location',
            clean_name: 'Your Current Location',
            latitude: newCoords.latitude,
            longitude: newCoords.longitude
          });
          setLocationLoading(false);
          console.log('📍 Auto-detected location:', newCoords);
        },
        (error) => {
          console.log('Geolocation not available, using default location');
          setLocationLoading(false);
          // Keep default Berlin coordinates if geolocation fails
        },
        {
          enableHighAccuracy: false,
          timeout: 5000,
          maximumAge: 0
        }
      );
    } else {
      setLocationLoading(false);
    }
  }, []);

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  const StatCard = ({ icon, title, value, unit, trend }) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box display="flex" alignItems="center" mb={1}>
          {icon}
          <Typography variant="h6" sx={{ ml: 1, fontWeight: 'bold' }}>
            {title}
          </Typography>
        </Box>
        <Typography variant="h4" color="primary" sx={{ fontWeight: 'bold' }}>
          {value !== null && value !== undefined ? `${value}${unit}` : 'N/A'}
        </Typography>
        {trend && (
          <Chip 
            label={trend} 
            size="small" 
            color={trend === 'increasing' ? 'success' : trend === 'decreasing' ? 'error' : 'default'}
            sx={{ mt: 1 }}
          />
        )}
      </CardContent>
    </Card>
  );

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold', mb: 3 }}>
        🌤️ Real-Time Weather Analytics
      </Typography>

      {/* Location Input */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <LocationIcon />
            Location Settings
          </Typography>
          {locationLoading && (
            <Chip 
              icon={<CircularProgress size={16} />} 
              label="Detecting location..." 
              size="small" 
              color="primary"
              variant="outlined"
            />
          )}
        </Box>
        
        {/* Location Search */}
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={12} md={6}>
            <Autocomplete
              freeSolo
              options={locationOptions}
              getOptionLabel={(option) => option.clean_name || option.name || option}
              loading={searchLoading}
              onInputChange={(event, newInputValue) => {
                setLocationSearch(newInputValue);
                searchLocations(newInputValue);
              }}
              onChange={(event, newValue) => {
                if (newValue && typeof newValue === 'object') {
                  handleLocationSelect(newValue);
                }
              }}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Search Location"
                  placeholder="Enter city name (e.g., New York, London, Tokyo)"
                  InputProps={{
                    ...params.InputProps,
                    startAdornment: (
                      <InputAdornment position="start">
                        <SearchIcon />
                      </InputAdornment>
                    ),
                    endAdornment: (
                      <>
                        {searchLoading ? <CircularProgress color="inherit" size={20} /> : null}
                        {params.InputProps.endAdornment}
                      </>
                    ),
                  }}
                />
              )}
              renderOption={(props, option) => (
                <Box component="li" {...props}>
                  <LocationIcon sx={{ mr: 1, color: 'text.secondary' }} />
                  <Box>
                    <Typography variant="body1">
                      {option.clean_name || option.name}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {option.latitude?.toFixed(2)}°, {option.longitude?.toFixed(2)}°
                    </Typography>
                  </Box>
                </Box>
              )}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <Button
              variant="outlined"
              onClick={getCurrentLocation}
              fullWidth
              startIcon={<LocationIcon />}
              sx={{ height: '56px' }}
            >
              Use Current Location
            </Button>
          </Grid>
        </Grid>

        {/* Popular Locations */}
        {popularLocations.length > 0 && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <GlobalIcon sx={{ mr: 1, fontSize: 16 }} />
              Popular Locations:
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {popularLocations.slice(0, 8).map((location, index) => (
                <Chip
                  key={index}
                  label={location.clean_name}
                  onClick={() => handlePopularLocationClick(location)}
                  variant="outlined"
                  size="small"
                  sx={{ cursor: 'pointer' }}
                />
              ))}
            </Box>
          </Box>
        )}

        <Divider sx={{ my: 2 }} />
        
        {/* Coordinate Input */}
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={3}>
            <TextField
              label="Latitude"
              type="number"
              value={coordinates.latitude}
              onChange={handleCoordinateChange('latitude')}
              fullWidth
              size="small"
              inputProps={{ step: 0.01, min: -90, max: 90 }}
            />
          </Grid>
          <Grid item xs={12} sm={3}>
            <TextField
              label="Longitude"
              type="number"
              value={coordinates.longitude}
              onChange={handleCoordinateChange('longitude')}
              fullWidth
              size="small"
              inputProps={{ step: 0.01, min: -180, max: 180 }}
            />
          </Grid>
          <Grid item xs={12} sm={3}>
            <Button
              variant="contained"
              onClick={() => fetchWeatherData(false)}
              disabled={loading}
              fullWidth
              startIcon={loading ? <CircularProgress size={20} /> : <RefreshIcon />}
            >
              Fetch Data
            </Button>
          </Grid>
          <Grid item xs={12} sm={3}>
            <Button
              variant="contained"
              color="secondary"
              onClick={() => fetchWeatherData(true)}
              disabled={loading}
              fullWidth
              startIcon={<WeatherIcon />}
            >
              Analyze
            </Button>
          </Grid>
        </Grid>

        {/* Selected Location Display */}
        {selectedLocation && (
          <Alert 
            severity={selectedLocation.name === 'Current Location' ? 'success' : 'info'} 
            sx={{ mt: 2 }}
            icon={selectedLocation.name === 'Current Location' ? <LocationIcon /> : undefined}
          >
            <Typography variant="body2">
              <strong>{selectedLocation.name === 'Current Location' ? '📍 Auto-detected:' : 'Selected:'}</strong> {selectedLocation.clean_name} 
              ({selectedLocation.latitude?.toFixed(4)}°, {selectedLocation.longitude?.toFixed(4)}°)
            </Typography>
          </Alert>
        )}
      </Paper>

      {/* Error Display */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Loading State */}
      {loading && (
        <Box display="flex" justifyContent="center" alignItems="center" py={4}>
          <CircularProgress size={40} />
          <Typography variant="h6" sx={{ ml: 2 }}>
            Fetching weather data...
          </Typography>
        </Box>
      )}

      {/* Weather Data Display */}
      {weatherData && !loading && (
        <>
          {/* Location Info */}
          <Paper sx={{ p: 2, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              📍 Location: {weatherData.location?.latitude?.toFixed(2)}°, {weatherData.location?.longitude?.toFixed(2)}°
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Timezone: {weatherData.location?.timezone} | 
              Elevation: {weatherData.location?.elevation}m | 
              Data Points: {weatherData.data_points} | 
              Updated: {formatTimestamp(weatherData.timestamp)}
            </Typography>
          </Paper>

          {/* AQI Display */}
          <AQIDisplay 
            latitude={weatherData.location?.latitude} 
            longitude={weatherData.location?.longitude} 
          />

          {/* Statistics by Category */}
          {weatherData.statistics && (
            <Box sx={{ mb: 3 }}>
              {/* Atmospheric Statistics */}
              {weatherData.statistics.atmospheric && Object.keys(weatherData.statistics.atmospheric).length > 0 && (
                <Paper sx={{ p: 3, mb: 2 }}>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                    🌤️ Atmospheric Conditions
                  </Typography>
                  <Grid container spacing={2}>
                    {weatherData.statistics.atmospheric.temperature && (
                      <Grid item xs={12} sm={6} md={3}>
                        <StatCard
                          icon={<TempIcon color="primary" />}
                          title="Temperature"
                          value={weatherData.statistics.atmospheric.temperature.current?.toFixed(1)}
                          unit="°C"
                          trend={weatherData.statistics.atmospheric.temperature.trend}
                        />
                      </Grid>
                    )}
                    {weatherData.statistics.atmospheric.humidity && (
                      <Grid item xs={12} sm={6} md={3}>
                        <StatCard
                          icon={<RainIcon color="primary" />}
                          title="Humidity"
                          value={weatherData.statistics.atmospheric.humidity.current?.toFixed(0)}
                          unit="%"
                          trend={weatherData.statistics.atmospheric.humidity.trend}
                        />
                      </Grid>
                    )}
                    {weatherData.statistics.atmospheric.wind_speed_10m && (
                      <Grid item xs={12} sm={6} md={3}>
                        <StatCard
                          icon={<WindIcon color="primary" />}
                          title="Wind Speed"
                          value={weatherData.statistics.atmospheric.wind_speed_10m.current?.toFixed(1)}
                          unit=" km/h"
                        />
                      </Grid>
                    )}
                    {weatherData.statistics.atmospheric.cloud_cover && (
                      <Grid item xs={12} sm={6} md={3}>
                        <StatCard
                          icon={<CloudQueue color="primary" />}
                          title="Cloud Cover"
                          value={weatherData.statistics.atmospheric.cloud_cover.current?.toFixed(0)}
                          unit="%"
                        />
                      </Grid>
                    )}
                  </Grid>
                </Paper>
              )}

              {/* Hydrological Statistics */}
              {weatherData.statistics.hydrological && Object.keys(weatherData.statistics.hydrological).length > 0 && (
                <Paper sx={{ p: 3, mb: 2 }}>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                    💧 Hydrological Conditions
                  </Typography>
                  <Grid container spacing={2}>
                    {weatherData.statistics.hydrological.sea_level_pressure && (
                      <Grid item xs={12} sm={6} md={4}>
                        <StatCard
                          icon={<PressureIcon color="primary" />}
                          title="Sea Level Pressure"
                          value={weatherData.statistics.hydrological.sea_level_pressure.current_hpa?.toFixed(0)}
                          unit=" hPa"
                          trend={weatherData.statistics.hydrological.sea_level_pressure.trend}
                        />
                      </Grid>
                    )}
                    {weatherData.statistics.hydrological.rainfall && (
                      <Grid item xs={12} sm={6} md={4}>
                        <StatCard
                          icon={<RainIcon color="primary" />}
                          title="Total Rainfall"
                          value={weatherData.statistics.hydrological.rainfall.total_mm?.toFixed(1)}
                          unit=" mm"
                        />
                      </Grid>
                    )}
                    {weatherData.statistics.hydrological.cyclone_activity && (
                      <Grid item xs={12} sm={6} md={4}>
                        <Card sx={{ height: '100%' }}>
                          <CardContent>
                            <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
                              🌀 Cyclone Risk
                            </Typography>
                            <Typography variant="h4" sx={{ 
                              fontWeight: 'bold',
                              color: weatherData.statistics.hydrological.cyclone_activity.risk_level === 'low' ? 'success.main' :
                                     weatherData.statistics.hydrological.cyclone_activity.risk_level === 'moderate' ? 'warning.main' : 'error.main'
                            }}>
                              {weatherData.statistics.hydrological.cyclone_activity.risk_level?.toUpperCase()}
                            </Typography>
                          </CardContent>
                        </Card>
                      </Grid>
                    )}
                  </Grid>
                </Paper>
              )}

              {/* Environmental Statistics */}
              {weatherData.statistics.environmental && Object.keys(weatherData.statistics.environmental).length > 0 && (
                <Paper sx={{ p: 3, mb: 2 }}>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                    🌿 Environmental Quality
                  </Typography>
                  <Grid container spacing={2}>
                    {weatherData.statistics.environmental.air_quality_index && (
                      <Grid item xs={12} sm={6} md={4}>
                        <Card sx={{ height: '100%' }}>
                          <CardContent>
                            <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
                              🌬️ Air Quality Index
                            </Typography>
                            <Typography variant="h4" sx={{ 
                              fontWeight: 'bold',
                              color: weatherData.statistics.environmental.air_quality_index.category === 'good' ? 'success.main' :
                                     weatherData.statistics.environmental.air_quality_index.category === 'moderate' ? 'warning.main' : 'error.main'
                            }}>
                              {weatherData.statistics.environmental.air_quality_index.aqi}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {weatherData.statistics.environmental.air_quality_index.category?.replace('_', ' ').toUpperCase()}
                            </Typography>
                          </CardContent>
                        </Card>
                      </Grid>
                    )}
                    {weatherData.statistics.environmental.pm2_5 && (
                      <Grid item xs={12} sm={6} md={4}>
                        <StatCard
                          icon={<Air color="primary" />}
                          title="PM2.5"
                          value={weatherData.statistics.environmental.pm2_5.current?.toFixed(1)}
                          unit=" μg/m³"
                        />
                      </Grid>
                    )}
                    {weatherData.statistics.environmental.pm10 && (
                      <Grid item xs={12} sm={6} md={4}>
                        <StatCard
                          icon={<Air color="primary" />}
                          title="PM10"
                          value={weatherData.statistics.environmental.pm10.current?.toFixed(1)}
                          unit=" μg/m³"
                        />
                      </Grid>
                    )}
                  </Grid>
                </Paper>
              )}

              {/* Oceanic Statistics */}
              {weatherData.statistics.oceanic && Object.keys(weatherData.statistics.oceanic).length > 0 && (
                <Paper sx={{ p: 3, mb: 2 }}>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                    🌊 Oceanic & Coastal Conditions
                  </Typography>
                  <Grid container spacing={2}>
                    {weatherData.statistics.oceanic.sea_surface_temperature && (
                      <Grid item xs={12} sm={6} md={4}>
                        <StatCard
                          icon={<TempIcon color="primary" />}
                          title="Sea Surface Temp"
                          value={weatherData.statistics.oceanic.sea_surface_temperature.current?.toFixed(1)}
                          unit="°C"
                          trend={weatherData.statistics.oceanic.sea_surface_temperature.trend}
                        />
                      </Grid>
                    )}
                    {weatherData.statistics.oceanic.wave_height && (
                      <Grid item xs={12} sm={6} md={4}>
                        <StatCard
                          icon={<WaterDrop color="primary" />}
                          title="Wave Height"
                          value={weatherData.statistics.oceanic.wave_height.current?.toFixed(1)}
                          unit=" m"
                        />
                      </Grid>
                    )}
                    {weatherData.statistics.oceanic.ocean_wind && (
                      <Grid item xs={12} sm={6} md={4}>
                        <StatCard
                          icon={<WindIcon color="primary" />}
                          title="Ocean Wind"
                          value={weatherData.statistics.oceanic.ocean_wind.current?.toFixed(1)}
                          unit=" m/s"
                        />
                      </Grid>
                    )}
                  </Grid>
                </Paper>
              )}
            </Box>
          )}

          {/* Charts Display */}
          {weatherData.charts && weatherData.charts.length > 0 && (
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                📊 Weather Visualizations ({weatherData.charts.length} charts)
              </Typography>
              <Grid container spacing={3}>
                {weatherData.charts.map((chart, index) => (
                  <Grid item xs={12} lg={6} key={index}>
                    <Card sx={{ height: '100%' }}>
                      <CardContent>
                        <Typography variant="h6" gutterBottom sx={{ 
                          fontWeight: 'bold',
                          color: 'primary.main',
                          display: 'flex',
                          alignItems: 'center',
                          gap: 1
                        }}>
                          📈 {chart.title}
                          {chart.category && (
                            <Chip 
                              label={chart.category} 
                              size="small" 
                              variant="outlined"
                              sx={{ ml: 'auto' }}
                            />
                          )}
                        </Typography>
                        {chart.url ? (
                          // Display image chart if URL exists
                          <Box
                            sx={{
                              position: 'relative',
                              width: '100%',
                              minHeight: '300px',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              backgroundColor: '#f5f5f5',
                              borderRadius: 1,
                              overflow: 'hidden'
                            }}
                          >
                            <Box
                              component="img"
                              src={`${API_BASE_URL}${chart.url}`}
                              alt={chart.title}
                              sx={{
                                maxWidth: '100%',
                                maxHeight: '400px',
                                width: 'auto',
                                height: 'auto',
                                borderRadius: 1,
                                boxShadow: 1
                              }}
                              onError={(e) => {
                                e.target.style.display = 'none';
                              }}
                            />
                          </Box>
                        ) : (
                          // Display enhanced data summary if no URL
                          <Box
                            sx={{
                              position: 'relative',
                              width: '100%',
                              minHeight: '250px',
                              display: 'flex',
                              flexDirection: 'column',
                              alignItems: 'center',
                              justifyContent: 'center',
                              background: 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
                              borderRadius: 2,
                              p: 3,
                              border: '1px solid #dee2e6',
                              boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                            }}
                          >
                            <Box sx={{ fontSize: '4rem', mb: 2, opacity: 0.8 }}>
                              {chart.type === 'line' ? '📈' : 
                               chart.type === 'bar' ? '📊' : 
                               chart.category === 'atmospheric' ? '🌤️' :
                               chart.category === 'hydrological' ? '💧' :
                               chart.category === 'oceanic' ? '🌊' :
                               chart.category === 'environmental' ? '🌿' : '📊'}
                            </Box>
                            
                            <Typography variant="h6" sx={{ 
                              fontWeight: 'bold', 
                              textAlign: 'center', 
                              mb: 2,
                              color: 'primary.main'
                            }}>
                              Real-Time Data Analysis
                            </Typography>
                            
                            <Box sx={{ 
                              backgroundColor: 'white', 
                              borderRadius: 1, 
                              p: 2, 
                              width: '100%',
                              boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
                            }}>
                              <Typography variant="body1" sx={{ 
                                textAlign: 'center', 
                                color: 'text.primary',
                                fontWeight: 500,
                                lineHeight: 1.6
                              }}>
                                {chart.description || 'Real-time weather data analysis'}
                              </Typography>
                            </Box>
                            
                            <Chip 
                              label={`${chart.category} data`} 
                              size="small" 
                              sx={{ 
                                mt: 2,
                                backgroundColor: 'primary.main',
                                color: 'white',
                                fontWeight: 'bold'
                              }}
                            />
                          </Box>
                        )}
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Paper>
          )}

          {/* Insights */}
          {weatherData.insights && weatherData.insights.length > 0 && (
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                💡 Weather Insights ({weatherData.insights.length})
              </Typography>
              <Grid container spacing={2}>
                {weatherData.insights.map((insight, index) => {
                  // Determine alert severity based on insight content
                  let severity = 'info';
                  if (insight.includes('hazardous') || insight.includes('very high') || insight.includes('emergency')) {
                    severity = 'error';
                  } else if (insight.includes('high') || insight.includes('strong') || insight.includes('heavy') || insight.includes('poor')) {
                    severity = 'warning';
                  } else if (insight.includes('good') || insight.includes('clear') || insight.includes('calm') || insight.includes('stable')) {
                    severity = 'success';
                  }

                  return (
                    <Grid item xs={12} md={6} key={index}>
                      <Alert severity={severity} sx={{ height: '100%' }}>
                        <Typography variant="body2">
                          {insight}
                        </Typography>
                      </Alert>
                    </Grid>
                  );
                })}
              </Grid>
            </Paper>
          )}
        </>
      )}
    </Box>
  );
};

export default WeatherDashboard;