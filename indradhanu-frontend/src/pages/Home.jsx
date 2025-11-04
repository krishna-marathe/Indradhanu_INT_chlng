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
                sx={{
                  height: '100%',
                  textAlign: 'center',
                  transition: 'transform 0.3s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                  },
                }}
              >
                <CardContent sx={{ p: 3 }}>
                  <Box sx={{ mb: 2 }}>
                    {feature.icon}
                  </Box>
                  <Typography variant="h6" component="h3" gutterBottom>
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* About Section */}
      <Box sx={{ backgroundColor: 'grey.50', py: 8 }}>
        <Container maxWidth="md">
          <Paper sx={{ p: 4, textAlign: 'center' }}>
            <Typography variant="h4" component="h2" gutterBottom>
              About Indradhanu Analytics
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ lineHeight: 1.8 }}>
              Indradhanu Analytics is a comprehensive environmental data analysis platform 
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