import React from 'react';
import { Box, Container, Typography, Grid, Card, CardContent, Paper } from '@mui/material';
import Hero from '../components/Hero';
import { Assessment, CloudUpload, Insights, TrendingUp } from '@mui/icons-material';

const Home = () => {
  const features = [
    {
      icon: <CloudUpload sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Easy Data Upload',
      description: 'Support for CSV, XLSX, and JSON files with drag-and-drop functionality.',
    },
    {
      icon: <Assessment sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Advanced Analytics',
      description: 'Automated data cleaning, statistical analysis, and correlation detection.',
    },
    {
      icon: <TrendingUp sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Interactive Visualizations',
      description: 'Dynamic charts and graphs to visualize your environmental data trends.',
    },
    {
      icon: <Insights sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'AI-Powered Insights',
      description: 'Get meaningful insights and recommendations from your data automatically.',
    },
  ];

  return (
    <Box>
      <Hero />
      
      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Typography variant="h3" component="h2" align="center" gutterBottom>
          Powerful Analytics Features
        </Typography>
        <Typography variant="h6" align="center" color="text.secondary" sx={{ mb: 6 }}>
          Everything you need to analyze environmental data effectively
        </Typography>
        
        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card
                elevation={3}
                sx={{
                  height: '100%',
                  textAlign: 'center',
                  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                  borderRadius: 3,
                  '&:hover': {
                    transform: 'translateY(-12px)',
                    boxShadow: '0 12px 24px rgba(0,0,0,0.15)',
                  },
                }}
              >
                <CardContent sx={{ p: 4 }}>
                  <Box 
                    sx={{ 
                      mb: 2,
                      animation: 'float 3s ease-in-out infinite',
                      animationDelay: `${index * 0.2}s`,
                      '@keyframes float': {
                        '0%, 100%': { transform: 'translateY(0)' },
                        '50%': { transform: 'translateY(-10px)' },
                      },
                    }}
                  >
                    {feature.icon}
                  </Box>
                  <Typography variant="h6" component="h3" gutterBottom fontWeight={600}>
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" lineHeight={1.7}>
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* About Section */}
      <Box 
        sx={{ 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          py: 10,
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            opacity: 0.1,
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          }}
        />
        <Container maxWidth="md" sx={{ position: 'relative', zIndex: 1 }}>
          <Paper 
            elevation={8}
            sx={{ 
              p: 6, 
              textAlign: 'center',
              borderRadius: 4,
              background: 'rgba(255, 255, 255, 0.95)',
              backdropFilter: 'blur(10px)',
            }}
          >
            <Typography 
              variant="h3" 
              component="h2" 
              gutterBottom
              sx={{
                fontWeight: 700,
                background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                mb: 3,
              }}
            >
              About Climate Sphere
            </Typography>
            <Typography 
              variant="h6" 
              color="text.secondary" 
              sx={{ 
                lineHeight: 1.8,
                fontWeight: 400,
              }}
            >
              Climate Sphere is a comprehensive environmental data analysis platform 
              designed to bridge the gap between raw climate data and actionable insights. 
              Whether you're monitoring air quality, tracking temperature patterns, or 
              analyzing humidity trends, our platform provides the tools you need to make 
              informed decisions for a sustainable future.
            </Typography>
          </Paper>
        </Container>
      </Box>
    </Box>
  );
};

export default Home;