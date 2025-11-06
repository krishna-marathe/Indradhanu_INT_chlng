import React from 'react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ScatterChart, 
  Scatter, 
  ResponsiveContainer, 
  Legend,
  ReferenceLine
} from 'recharts';
import { Paper, Typography, Box, Grid, Chip } from '@mui/material';

const SurfaceRadiationVisuals = ({ analysis }) => {
  if (!analysis || !analysis.surface_radiation_analysis || !analysis.surface_radiation_analysis.has_surface_radiation_data) {
    return null;
  }

  const { 
    trend_data, 
    scatter_data, 
    albedo_temp_scatter,
    solar_temp_regression, 
    albedo_temp_regression,
    insights,
    data_points,
    column_names
  } = analysis.surface_radiation_analysis;

  // Custom regression line component
  const RegressionLine = ({ regression, xKey, yKey }) => {
    if (!regression) return null;
    
    return (
      <ReferenceLine
        segment={[
          { x: Math.min(...scatter_data.map(d => d[xKey])), y: regression.intercept + regression.slope * Math.min(...scatter_data.map(d => d[xKey])) },
          { x: Math.max(...scatter_data.map(d => d[xKey])), y: regression.intercept + regression.slope * Math.max(...scatter_data.map(d => d[xKey])) }
        ]}
        stroke="red"
        strokeWidth={2}
        strokeDasharray="5 5"
      />
    );
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
        🌡️ Surface Temperature & Radiation Analysis
      </Typography>

      {/* Data Summary */}
      <Paper sx={{ p: 2, mb: 3, backgroundColor: 'info.light', color: 'info.contrastText' }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={6}>
            <Typography variant="body1">
              📊 Analyzing {data_points} data points with surface temperature and solar radiation measurements
            </Typography>
          </Grid>
          <Grid item xs={12} md={6}>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              {column_names && (
                <>
                  <Chip label={`Temp: ${column_names.temperature}`} size="small" />
                  <Chip label={`Solar: ${column_names.solar_irradiance}`} size="small" />
                  <Chip label={`Albedo: ${column_names.albedo}`} size="small" />
                </>
              )}
            </Box>
          </Grid>
        </Grid>
      </Paper>

      {/* Trend Chart */}
      {trend_data && trend_data.length > 0 && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            🌡️ Surface Temperature Trend Over Time
          </Typography>
          <ResponsiveContainer width="100%" height={350}>
            <LineChart data={trend_data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="timestamp" 
                tick={{ fontSize: 12 }}
                angle={-45}
                textAnchor="end"
                height={60}
              />
              <YAxis 
                label={{ value: "Surface Temp (°C)", angle: -90, position: 'insideLeft' }}
              />
              <Tooltip 
                labelFormatter={(value) => `Time: ${value}`}
                formatter={(value) => [`${value}°C`, 'Surface Temperature']}
              />
              <Line 
                type="monotone" 
                dataKey="surface_temp_c" 
                stroke="#ff7300" 
                strokeWidth={3}
                dot={{ r: 5, fill: '#ff7300' }}
                activeDot={{ r: 7 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </Paper>
      )}

      <Grid container spacing={3}>
        {/* Solar Irradiance vs Surface Temperature Scatter Plot */}
        {scatter_data && scatter_data.length > 0 && (
          <Grid item xs={12} lg={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                ☀️ Solar Irradiance vs Surface Temperature
              </Typography>
              <ResponsiveContainer width="100%" height={350}>
                <ScatterChart data={scatter_data}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="solar_irradiance_wm2" 
                    name="Solar Irradiance (W/m²)"
                    type="number"
                    domain={['dataMin - 10', 'dataMax + 10']}
                  />
                  <YAxis 
                    dataKey="surface_temp_c" 
                    name="Surface Temp (°C)"
                    type="number"
                    domain={['dataMin - 1', 'dataMax + 1']}
                  />
                  <Tooltip 
                    cursor={{ strokeDasharray: '3 3' }}
                    formatter={(value, name) => [
                      name === 'solar_irradiance_wm2' ? `${value} W/m²` : `${value}°C`,
                      name === 'solar_irradiance_wm2' ? 'Solar Irradiance' : 'Surface Temperature'
                    ]}
                  />
                  <Legend />
                  <Scatter 
                    data={scatter_data} 
                    fill="#8884d8"
                    name="Data Points"
                  />
                </ScatterChart>
              </ResponsiveContainer>
              
              {solar_temp_regression && (
                <Box sx={{ mt: 2, p: 2, backgroundColor: 'grey.100', borderRadius: 1 }}>
                  <Typography variant="body2" gutterBottom>
                    📈 Regression Analysis:
                  </Typography>
                  <Typography variant="body2">
                    • R² = {solar_temp_regression.r_squared} ({solar_temp_regression.r_squared > 0.7 ? 'Strong' : solar_temp_regression.r_squared > 0.4 ? 'Moderate' : 'Weak'} correlation)
                  </Typography>
                  <Typography variant="body2">
                    • Slope = {solar_temp_regression.slope}°C per W/m²
                  </Typography>
                  <Typography variant="body2">
                    • p-value = {solar_temp_regression.p_value} {solar_temp_regression.p_value < 0.05 ? '(Significant)' : '(Not significant)'}
                  </Typography>
                </Box>
              )}
            </Paper>
          </Grid>
        )}

        {/* Albedo vs Surface Temperature Scatter Plot */}
        {albedo_temp_scatter && albedo_temp_scatter.length > 0 && (
          <Grid item xs={12} lg={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                🌍 Albedo vs Surface Temperature
              </Typography>
              <ResponsiveContainer width="100%" height={350}>
                <ScatterChart data={albedo_temp_scatter}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="albedo" 
                    name="Albedo"
                    type="number"
                    domain={['dataMin - 0.01', 'dataMax + 0.01']}
                  />
                  <YAxis 
                    dataKey="surface_temp_c" 
                    name="Surface Temp (°C)"
                    type="number"
                    domain={['dataMin - 1', 'dataMax + 1']}
                  />
                  <Tooltip 
                    cursor={{ strokeDasharray: '3 3' }}
                    formatter={(value, name) => [
                      name === 'albedo' ? value.toFixed(3) : `${value}°C`,
                      name === 'albedo' ? 'Albedo' : 'Surface Temperature'
                    ]}
                  />
                  <Legend />
                  <Scatter 
                    data={albedo_temp_scatter} 
                    fill="#82ca9d"
                    name="Data Points"
                  />
                </ScatterChart>
              </ResponsiveContainer>
              
              {albedo_temp_regression && (
                <Box sx={{ mt: 2, p: 2, backgroundColor: 'grey.100', borderRadius: 1 }}>
                  <Typography variant="body2" gutterBottom>
                    📈 Regression Analysis:
                  </Typography>
                  <Typography variant="body2">
                    • R² = {albedo_temp_regression.r_squared} ({albedo_temp_regression.r_squared > 0.7 ? 'Strong' : albedo_temp_regression.r_squared > 0.4 ? 'Moderate' : 'Weak'} correlation)
                  </Typography>
                  <Typography variant="body2">
                    • Slope = {albedo_temp_regression.slope}°C per albedo unit
                  </Typography>
                  <Typography variant="body2">
                    • p-value = {albedo_temp_regression.p_value} {albedo_temp_regression.p_value < 0.05 ? '(Significant)' : '(Not significant)'}
                  </Typography>
                </Box>
              )}
            </Paper>
          </Grid>
        )}
      </Grid>

      {/* Insights Summary */}
      {insights && insights.length > 0 && (
        <Paper sx={{ p: 3, mt: 3, backgroundColor: 'success.light', color: 'success.contrastText' }}>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            💡 Analysis Insights
          </Typography>
          {insights.map((insight, index) => (
            <Typography key={index} variant="body1" sx={{ mb: 1 }}>
              • {insight}
            </Typography>
          ))}
        </Paper>
      )}
    </Box>
  );
};

export default SurfaceRadiationVisuals;