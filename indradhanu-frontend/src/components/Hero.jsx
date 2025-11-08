import React from 'react';
import { Box, Typography, Button, Container } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Hero = () => {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        color: 'white',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Background Video */}
      <Box
        component="video"
        autoPlay
        muted
        loop
        playsInline
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          zIndex: -2,
          opacity: 0,
          animation: 'fadeIn 2s ease-in-out forwards',
          '@keyframes fadeIn': {
            to: { opacity: 1 },
          },
        }}
      >
        <source src="/8947-215890483.mp4" type="video/mp4" />
      </Box>
      
      {/* Dark overlay for text readability */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          zIndex: -1,
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
        
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/upload')}
            sx={{
              backgroundColor: 'rgba(255, 255, 255, 0.2)',
              backdropFilter: 'blur(10px)',
              border: '2px solid rgba(255, 255, 255, 0.3)',
              color: 'white',
              px: 5,
              py: 2,
              fontSize: '1.2rem',
              fontWeight: 700,
              borderRadius: 3,
              transition: 'all 0.3s ease',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.3)',
                transform: 'translateY(-3px)',
                boxShadow: '0 10px 25px rgba(0,0,0,0.3)',
              },
            }}
          >
            🚀 Start Analyzing
          </Button>
          
          <Button
            variant="outlined"
            size="large"
            onClick={() => navigate('/weather')}
            sx={{
              border: '2px solid rgba(255, 255, 255, 0.5)',
              color: 'white',
              px: 5,
              py: 2,
              fontSize: '1.2rem',
              fontWeight: 700,
              borderRadius: 3,
              backdropFilter: 'blur(10px)',
              transition: 'all 0.3s ease',
              '&:hover': {
                border: '2px solid rgba(255, 255, 255, 0.8)',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                transform: 'translateY(-3px)',
                boxShadow: '0 10px 25px rgba(0,0,0,0.3)',
              },
            }}
          >
            🌤️ Weather Data
          </Button>
        </Box>
      </Container>
    </Box>
  );
};

export default Hero;