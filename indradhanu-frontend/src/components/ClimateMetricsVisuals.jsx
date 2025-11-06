import React from 'react';
import { Paper, Typography, Grid, Box, Chip, Divider } from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const ClimateMetricsVisuals = ({ metrics }) => {
  if (!metrics || !metrics.has_climate_data) {
    return null;
  }

  // KPI Cards Data
  const kpis = [
    { 
      label: '🌧️ Total Rainfall', 
      value: metrics.total_rainfall_mm, 
      unit: 'mm',
      color: '#2196F3'
    },
    { 
      label: '📉 Rainfall Anomaly', 
      value: metrics.rainfall_anomaly_pct, 
      unit: '%',
      color: metrics.rainfall_anomaly_pct > 0 ? '#4CAF50' : '#FF5722'
    },
    { 
      label: '🔥 Heatwave Days', 
      value: metrics.heatwave_days, 
      unit: 'days',
      color: '#FF9800'
    },
    { 
      label: '🌵 Drought Risk', 
      value: metrics.drought_risk_index, 
      unit: '/100',
      color: '#795548'
    },
    { 
      label: '💧 Flood Risk', 
      value: metrics.flood_risk_index, 
      unit: '/100',
      color: '#00BCD4'
    },
  ];

  // Risk level indicator
  const getRiskLevel = (value, type) => {
    if (value === null || value === undefined) return { level: 'Unknown', color: '#9E9E9E' };
    
    if (type === 'drought' || type === 'flood') {
      if (value > 70) return { level: 'High', color: '#F44336' };
      if (value > 40) return { level: 'Moderate', color: '#FF9800' };
      return { level: 'Low', color: '#4CAF50' };
    }
    
    if (type === 'anomaly') {
      if (Math.abs(value) > 20) return { level: 'Extreme', color: '#F44336' };
      if (Math.abs(value) > 10) return { level: 'Moderate', color: '#FF9800' };
      return { level: 'Normal', color: '#4CAF50' };
    }
    
    return { level: 'Normal', color: '#4CAF50' };
  };

  // Risk distribution data for pie chart
  const riskData = [
    { name: 'Drought Risk', value: metrics.drought_risk_index || 0, fill: '#795548' },
    { name: 'Flood Risk', value: metrics.flood_risk_index || 0, fill: '#00BCD4' },
    { name: 'Safe Zone', value: Math.max(0, 100 - (metrics.drought_risk_index || 0) - (metrics.flood_risk_index || 0)), fill: '#4CAF50' }
  ].filter(item => item.value > 0);

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
        🌦️ Climate Metrics & Regional Risk Analysis
      </Typography>

      {/* Data Period Info */}
      {metrics.data_period && (
        <Paper sx={{ p: 2, mb: 3, backgroundColor: 'info.light', color: 'info.contrastText' }}>
          <Typography variant="body1">
            📅 Analysis Period: {metrics.data_period.start_date} to {metrics.data_period.end_date} 
            ({metrics.data_period.total_days} days)
          </Typography>
        </Paper>
      )}

      {/* KPI Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {kpis.map((kpi, i) => {
          const riskLevel = getRiskLevel(kpi.value, 
            kpi.label.includes('Drought') ? 'drought' : 
            kpi.label.includes('Flood') ? 'flood' : 
            kpi.label.includes('Anomaly') ? 'anomaly' : 'normal'
          );
          
          return (
            <Grid item xs={12} sm={6} md={4} lg={2.4} key={i}>
              <Paper sx={{ 
                p: 2, 
                textAlign: 'center', 
                bgcolor: kpi.color, 
                color: 'white',
                height: '140px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center'
              }}>
                <Typography variant="body2" sx={{ mb: 1, opacity: 0.9 }}>
                  {kpi.label}
                </Typography>
                <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                  {kpi.value !== null && kpi.value !== undefined ? kpi.value : '–'}
                  {kpi.value !== null && kpi.value !== undefined && (
                    <Typography component="span" variant="body1" sx={{ ml: 0.5 }}>
                      {kpi.unit}
                    </Typography>
                  )}
                </Typography>
                {(kpi.label.includes('Risk') || kpi.label.includes('Anomaly')) && (
                  <Chip 
                    label={riskLevel.level} 
                    size="small" 
                    sx={{ 
                      mt: 1, 
                      bgcolor: riskLevel.color, 
                      color: 'white',
                      fontWeight: 'bold'
                    }} 
                  />
                )}
              </Paper>
            </Grid>
          );
        })}
      </Grid>

      <Grid container spacing={3}>
        {/* Regional Comparison */}
        {metrics.regional_stats && metrics.regional_stats.length > 0 && (
          <Grid item xs={12} lg={8}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                📊 Regional Comparison ({metrics.regions_count} regions)
              </Typography>
              <ResponsiveContainer width="100%" height={350}>
                <BarChart data={metrics.regional_stats}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="region" 
                    tick={{ fontSize: 12 }}
                    angle={-45}
                    textAnchor="end"
                    height={60}
                  />
                  <YAxis />
                  <Tooltip 
                    formatter={(value, name) => [
                      `${value} ${name.includes('rainfall') ? 'mm' : name.includes('temperature') ? '°C' : ''}`,
                      name.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
                    ]}
                  />
                  {metrics.regional_stats[0].total_rainfall !== undefined && (
                    <Bar dataKey="total_rainfall" fill="#2196F3" name="Total Rainfall" />
                  )}
                  {metrics.regional_stats[0].avg_rainfall !== undefined && (
                    <Bar dataKey="avg_rainfall" fill="#03A9F4" name="Avg Rainfall" />
                  )}
                  {metrics.regional_stats[0].rainfall !== undefined && (
                    <Bar dataKey="rainfall" fill="#2196F3" name="Rainfall" />
                  )}
                  {metrics.regional_stats[0].avg_temperature !== undefined && (
                    <Bar dataKey="avg_temperature" fill="#FF5722" name="Avg Temperature" />
                  )}
                </BarChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>
        )}

        {/* Risk Distribution Pie Chart */}
        {riskData.length > 1 && (
          <Grid item xs={12} lg={4}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                ⚠️ Risk Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={350}>
                <PieChart>
                  <Pie
                    data={riskData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value.toFixed(1)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {riskData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.fill} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => [`${value.toFixed(1)}%`, 'Risk Level']} />
                </PieChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>
        )}
      </Grid>

      {/* Additional Metrics */}
      {(metrics.avg_temperature_C || metrics.max_temperature_C || metrics.heatwave_threshold_C) && (
        <Paper sx={{ p: 3, mt: 3 }}>
          <Typography variant="h6" gutterBottom>
            🌡️ Temperature Analysis
          </Typography>
          <Grid container spacing={2}>
            {metrics.avg_temperature_C && (
              <Grid item xs={6} md={3}>
                <Typography variant="body2" color="text.secondary">Average Temperature</Typography>
                <Typography variant="h6">{metrics.avg_temperature_C}°C</Typography>
              </Grid>
            )}
            {metrics.max_temperature_C && (
              <Grid item xs={6} md={3}>
                <Typography variant="body2" color="text.secondary">Maximum Temperature</Typography>
                <Typography variant="h6">{metrics.max_temperature_C}°C</Typography>
              </Grid>
            )}
            {metrics.heatwave_threshold_C && (
              <Grid item xs={6} md={3}>
                <Typography variant="body2" color="text.secondary">Heatwave Threshold</Typography>
                <Typography variant="h6">{metrics.heatwave_threshold_C}°C</Typography>
              </Grid>
            )}
            {metrics.avg_rainfall_mm && (
              <Grid item xs={6} md={3}>
                <Typography variant="body2" color="text.secondary">Average Rainfall</Typography>
                <Typography variant="h6">{metrics.avg_rainfall_mm} mm</Typography>
              </Grid>
            )}
          </Grid>
        </Paper>
      )}

      {/* Insights */}
      {metrics.insights && metrics.insights.length > 0 && (
        <Paper sx={{ p: 3, mt: 3, backgroundColor: 'warning.light', color: 'warning.contrastText' }}>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            💡 Climate Insights & Recommendations
          </Typography>
          <Divider sx={{ mb: 2, borderColor: 'warning.dark' }} />
          {metrics.insights.map((insight, i) => (
            <Typography key={i} variant="body1" sx={{ mb: 1, display: 'flex', alignItems: 'flex-start' }}>
              • {insight}
            </Typography>
          ))}
        </Paper>
      )}
    </Box>
  );
};

export default ClimateMetricsVisuals;