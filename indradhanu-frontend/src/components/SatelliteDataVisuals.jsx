import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ScatterChart, Scatter, ResponsiveContainer } from 'recharts';
import { MapContainer, TileLayer } from 'react-leaflet';
import { HeatmapLayer } from 'react-leaflet-heatmap-layer-v3';
import { Typography, Paper, Grid, Box } from '@mui/material';

const SatelliteDataVisuals = ({ analysis }) => {
  if (!analysis) return null;

  return (
    <Box sx={{ mt: 3 }}>
      {/* 🌍 Geospatial Heatmap */}
      {analysis.hasGeoData && analysis.geo_points && analysis.geo_points.length > 0 && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            🌍 Geospatial Heatmap - {analysis.geoVariable || 'Values'}
          </Typography>
          <Box sx={{ height: '400px', width: '100%' }}>
            <MapContainer 
              center={[20.59, 78.96]} 
              zoom={5} 
              style={{ height: '100%', width: '100%' }}
            >
              <TileLayer 
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; OpenStreetMap contributors'
              />
              <HeatmapLayer
                fitBoundsOnLoad
                fitBoundsOnUpdate
                points={analysis.geo_points.map(point => [
                  point.latitude,
                  point.longitude,
                  point.value || 1
                ])}
                longitudeExtractor={m => m[1]}
                latitudeExtractor={m => m[0]}
                intensityExtractor={m => m[2]}
              />
            </MapContainer>
          </Box>
        </Paper>
      )}

      {/* 📈 Time-Series Charts */}
      {analysis.hasTimeData && analysis.time_series && Object.keys(analysis.time_series).length > 0 && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            📈 Time Series Analysis
          </Typography>
          <Grid container spacing={3}>
            {Object.entries(analysis.time_series).map(([col, data]) => (
              <Grid item xs={12} md={6} key={col}>
                <Typography variant="subtitle1" gutterBottom>
                  {col.toUpperCase()} vs Time
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="timestamp" 
                      tick={{ fontSize: 12 }}
                      angle={-45}
                      textAnchor="end"
                      height={60}
                    />
                    <YAxis />
                    <Tooltip 
                      labelFormatter={(value) => `Time: ${value}`}
                      formatter={(value, name) => [value, name.toUpperCase()]}
                    />
                    <Line 
                      type="monotone" 
                      dataKey={col} 
                      stroke="#8884d8" 
                      strokeWidth={2}
                      dot={{ r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Grid>
            ))}
          </Grid>
        </Paper>
      )}

      {/* ☀️ Solar Irradiance vs Albedo Scatter Plot */}
      {analysis.hasScatterData && analysis.scatter_data && analysis.scatter_data.length > 0 && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            ☀️ Solar Irradiance vs Albedo
          </Typography>
          <ResponsiveContainer width="100%" height={400}>
            <ScatterChart data={analysis.scatter_data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="solar_irradiance_wm2" 
                name="Solar Irradiance (W/m²)"
                type="number"
              />
              <YAxis 
                dataKey="albedo" 
                name="Albedo"
                type="number"
              />
              <Tooltip 
                cursor={{ strokeDasharray: '3 3' }}
                formatter={(value, name) => [
                  value, 
                  name === 'solar_irradiance_wm2' ? 'Solar Irradiance (W/m²)' : 'Albedo'
                ]}
              />
              <Scatter 
                data={analysis.scatter_data} 
                fill="#82ca9d"
              />
            </ScatterChart>
          </ResponsiveContainer>
        </Paper>
      )}

      {/* 📊 Additional Scatter Plots */}
      {analysis.additional_scatters && analysis.additional_scatters.length > 0 && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            📊 Variable Relationships
          </Typography>
          <Grid container spacing={3}>
            {analysis.additional_scatters.map((scatter, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Typography variant="subtitle1" gutterBottom>
                  {scatter.x_column.toUpperCase()} vs {scatter.y_column.toUpperCase()}
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <ScatterChart data={scatter.data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey={scatter.x_column}
                      name={scatter.x_column.toUpperCase()}
                      type="number"
                    />
                    <YAxis 
                      dataKey={scatter.y_column}
                      name={scatter.y_column.toUpperCase()}
                      type="number"
                    />
                    <Tooltip 
                      cursor={{ strokeDasharray: '3 3' }}
                      formatter={(value, name) => [value, name.toUpperCase()]}
                    />
                    <Scatter 
                      data={scatter.data} 
                      fill="#ff7300"
                    />
                  </ScatterChart>
                </ResponsiveContainer>
              </Grid>
            ))}
          </Grid>
        </Paper>
      )}

      {/* 📋 Dataset Summary */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          📋 Dataset Summary
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={6} md={3}>
            <Typography variant="body2" color="text.secondary">Total Rows</Typography>
            <Typography variant="h6">{analysis.total_rows?.toLocaleString()}</Typography>
          </Grid>
          <Grid item xs={6} md={3}>
            <Typography variant="body2" color="text.secondary">Total Columns</Typography>
            <Typography variant="h6">{analysis.total_columns}</Typography>
          </Grid>
          <Grid item xs={6} md={3}>
            <Typography variant="body2" color="text.secondary">Numeric Variables</Typography>
            <Typography variant="h6">{analysis.numeric_columns?.length || 0}</Typography>
          </Grid>
          <Grid item xs={6} md={3}>
            <Typography variant="body2" color="text.secondary">Dataset Type</Typography>
            <Typography variant="h6">
              {analysis.dataset_type === 'satellite_sensor' ? '🛰️ Satellite/Sensor' : '📊 General'}
            </Typography>
          </Grid>
        </Grid>
        
        {analysis.numeric_columns && analysis.numeric_columns.length > 0 && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Numeric Variables:
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {analysis.numeric_columns.map((col, index) => (
                <Typography 
                  key={index}
                  variant="caption" 
                  sx={{ 
                    backgroundColor: 'primary.light', 
                    color: 'primary.contrastText',
                    px: 1, 
                    py: 0.5, 
                    borderRadius: 1 
                  }}
                >
                  {col}
                </Typography>
              ))}
            </Box>
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default SatelliteDataVisuals;