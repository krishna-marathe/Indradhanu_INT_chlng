import React from 'react';
import { Container, Box, Typography, Toolbar } from '@mui/material';
import WeatherDashboard from '../components/WeatherDashboard';

const Weather = () => {
  return (
    <Box>
      <Toolbar />
      <Box
        sx={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          py: 6,
          mb: 4,
          position: 'relative',
          overflow: 'hidden',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'url("data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'0.05\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")',
            opacity: 0.1,
          },
        }}
      >
        <Container maxWidth="lg">
          <Box
            sx={{
              textAlign: 'center',
              color: 'white',
              position: 'relative',
              zIndex: 1,
              animation: 'fadeInUp 0.6s ease-out',
              '@keyframes fadeInUp': {
                from: { opacity: 0, transform: 'translateY(20px)' },
                to: { opacity: 1, transform: 'translateY(0)' },
              },
            }}
          >
            <Typography
              variant="h2"
              component="h1"
              gutterBottom
              sx={{
                fontWeight: 800,
                fontSize: { xs: '2.5rem', md: '3.5rem' },
                textShadow: '2px 2px 4px rgba(0,0,0,0.2)',
              }}
            >
              🌤️ Real-Time Weather Analytics
            </Typography>
            <Typography
              variant="h5"
              sx={{
                opacity: 0.95,
                maxWidth: 700,
                mx: 'auto',
                fontWeight: 400,
                lineHeight: 1.6,
              }}
            >
              Get live weather data and comprehensive analysis for any location worldwide
            </Typography>
          </Box>
        </Container>
      </Box>
      
      <Container maxWidth="xl" sx={{ pb: 6 }}>
        <WeatherDashboard />
      </Container>
    </Box>
  );
};

export default Weather;