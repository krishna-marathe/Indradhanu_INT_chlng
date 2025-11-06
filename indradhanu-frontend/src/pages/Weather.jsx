import React from 'react';
import { Container } from '@mui/material';
import WeatherDashboard from '../components/WeatherDashboard';

const Weather = () => {
  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <WeatherDashboard />
    </Container>
  );
};

export default Weather;