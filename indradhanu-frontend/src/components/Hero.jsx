import React from 'react';
import { Box, Typography, Button, Container } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Hero = () => {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #2c5aa0 0%, #1e3f73 100%)',
        display: 'flex',
        alignItems: 'center',
        color: 'white',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Background pattern */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          opacity: 0.1,
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }}
      />
      
      <Container maxWidth="md" sx={{ textAlign: 'center', zIndex: 1 }}>
        <Typography
          variant="h2"
          component="h1"
          gutterBottom
          sx={{
            fontWeight: 700,
            fontSize: { xs: '2.5rem', md: '3.5rem' },
            mb: 3,
          }}
        >
          Environmental Data Analytics
        </Typography>
        
        <Typography
          variant="h5"
          component="p"
          sx={{
            mb: 4,
            opacity: 0.9,
            fontSize: { xs: '1.1rem', md: '1.3rem' },
            lineHeight: 1.6,
          }}
        >
          Transform your environmental data into actionable insights with our powerful 
          analytics engine. Upload, analyze, and visualize climate data effortlessly.
        </Typography>
        
        <Button
          variant="contained"
          size="large"
          onClick={() => navigate('/upload')}
          sx={{
            backgroundColor: 'rgba(255, 255, 255, 0.2)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.3)',
            color: 'white',
            px: 4,
            py: 1.5,
            fontSize: '1.1rem',
            fontWeight: 600,
            '&:hover': {
              backgroundColor: 'rgba(255, 255, 255, 0.3)',
            },
          }}
        >
          Start Analyzing
        </Button>
      </Container>
    </Box>
  );
};

export default Hero;