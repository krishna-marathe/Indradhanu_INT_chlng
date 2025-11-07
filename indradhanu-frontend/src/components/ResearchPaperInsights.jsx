import React from 'react';
import { 
  Paper, 
  Typography, 
  Chip, 
  Box, 
  Divider, 
  Grid, 
  Card, 
  CardContent,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import {
  Description,
  LocationOn,
  DateRange,
  TrendingUp,
  Science,
  Insights,
  Assessment
} from '@mui/icons-material';

const ResearchPaperInsights = ({ data }) => {
  console.log('🔍 ResearchPaperInsights received data:', data);
  console.log('🔍 Has analysis?', !!data?.analysis);
  console.log('🔍 Analysis content:', data?.analysis);
  
  if (!data || !data.analysis) {
    console.log('❌ No data or analysis found, returning null');
    return null;
  }

  const analysis = data.analysis;
  
  // Detailed logging of analysis fields
  console.log('📊 Analysis Details:');
  console.log('  - summary:', analysis.summary);
  console.log('  - word_count:', analysis.word_count);
  console.log('  - regions:', analysis.regions);
  console.log('  - years:', analysis.years);
  console.log('  - document_type:', analysis.document_type);
  console.log('  - analysis_confidence:', analysis.analysis_confidence);

  const getConfidenceColor = (confidence) => {
    switch (confidence) {
      case 'high': return 'success';
      case 'medium': return 'warning';
      case 'low': return 'error';
      default: return 'default';
    }
  };

  const getConfidenceIcon = (confidence) => {
    switch (confidence) {
      case 'high': return '🎯';
      case 'medium': return '⚠️';
      case 'low': return '❓';
      default: return '📊';
    }
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          📄 Research Paper Analysis
        </Typography>
        
        {/* Document Info */}
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} md={6}>
            <Typography variant="body2" color="text.secondary">Original Filename</Typography>
            <Typography variant="body1" sx={{ fontWeight: 'medium' }}>{data.original_filename}</Typography>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="body2" color="text.secondary">Document Type</Typography>
            <Chip 
              label={analysis.document_type || 'Research Paper'} 
              color="primary" 
              size="small" 
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="body2" color="text.secondary">Analysis Confidence</Typography>
            <Chip 
              label={`${getConfidenceIcon(analysis.analysis_confidence)} ${analysis.analysis_confidence?.toUpperCase() || 'MEDIUM'}`}
              color={getConfidenceColor(analysis.analysis_confidence)}
              size="small"
            />
          </Grid>
        </Grid>

        <Divider sx={{ mb: 3 }} />

        {/* Debug Info */}
        <Box sx={{ mb: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
          <Typography variant="caption" color="text.secondary">
            Debug: Analysis keys: {Object.keys(analysis).join(', ')}
          </Typography>
        </Box>

        {/* Summary */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Description /> Summary
          </Typography>
          <Typography variant="body1" sx={{ lineHeight: 1.6, mb: 2 }}>
            {String(analysis.summary || 'No summary available')}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            Word Count: {String(analysis.word_count || 'Unknown')} words
          </Typography>
          
          {/* Additional Debug Info */}
          <Box sx={{ mt: 2, p: 2, bgcolor: 'info.light', borderRadius: 1 }}>
            <Typography variant="caption">
              Raw Data Check: summary={typeof analysis.summary}, length={analysis.summary?.length || 0}
            </Typography>
          </Box>
        </Box>

        <Divider sx={{ mb: 3 }} />

        <Grid container spacing={3}>
          {/* Regions */}
          {analysis.regions && analysis.regions.length > 0 && (
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <LocationOn color="primary" /> Regions Mentioned
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {analysis.regions.map((region, i) => (
                      <Chip key={i} label={region} color="info" size="small" />
                    ))}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          )}

          {/* Years */}
          {analysis.years && analysis.years.length > 0 && (
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <DateRange color="secondary" /> Years Covered
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {analysis.years.map((year, i) => (
                      <Chip key={i} label={year} color="secondary" size="small" />
                    ))}
                  </Box>
                  {analysis.decades && analysis.decades.length > 0 && (
                    <Box sx={{ mt: 1 }}>
                      <Typography variant="caption" color="text.secondary">Decades: </Typography>
                      {analysis.decades.map((decade, i) => (
                        <Chip key={i} label={decade} variant="outlined" size="small" sx={{ ml: 0.5 }} />
                      ))}
                    </Box>
                  )}
                </CardContent>
              </Card>
            </Grid>
          )}

          {/* Key Trends */}
          {analysis.key_trends && analysis.key_trends.length > 0 && (
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <TrendingUp color="success" /> Key Trends & Measurements
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, maxHeight: 200, overflowY: 'auto' }}>
                    {analysis.key_trends.map((trend, i) => (
                      <Chip key={i} label={trend} color="success" variant="outlined" size="small" />
                    ))}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          )}

          {/* Research Methods */}
          {analysis.research_methods && analysis.research_methods.length > 0 && (
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Science color="warning" /> Research Methods
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {analysis.research_methods.map((method, i) => (
                      <Chip key={i} label={method} color="warning" variant="outlined" size="small" />
                    ))}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          )}

          {/* Climate Keywords */}
          {analysis.climate_keywords && analysis.climate_keywords.length > 0 && (
            <Grid item xs={12}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    🌍 Climate & Environmental Keywords
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {analysis.climate_keywords.map((keyword, i) => (
                      <Chip 
                        key={i} 
                        label={keyword} 
                        sx={{ 
                          bgcolor: 'primary.light', 
                          color: 'primary.contrastText' 
                        }} 
                        size="small" 
                      />
                    ))}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          )}

          {/* Key Findings */}
          {analysis.key_findings && analysis.key_findings.length > 0 && (
            <Grid item xs={12}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Insights color="error" /> Key Findings
                  </Typography>
                  <List dense>
                    {analysis.key_findings.map((finding, i) => (
                      <ListItem key={i}>
                        <ListItemIcon>
                          <Assessment color="error" />
                        </ListItemIcon>
                        <ListItemText 
                          primary={finding}
                          primaryTypographyProps={{ variant: 'body2' }}
                        />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>

        {/* Document Preview */}
        {analysis.preview && (
          <>
            <Divider sx={{ my: 3 }} />
            <Box>
              <Typography variant="h6" gutterBottom>
                📖 Document Preview
              </Typography>
              <Paper sx={{ p: 2, bgcolor: 'grey.50', maxHeight: 200, overflowY: 'auto' }}>
                <Typography variant="body2" sx={{ fontFamily: 'monospace', lineHeight: 1.4 }}>
                  {analysis.preview}
                </Typography>
              </Paper>
            </Box>
          </>
        )}

        {/* Metadata */}
        <Divider sx={{ my: 3 }} />
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="caption" color="text.secondary">
            Analyzed on: {new Date(data.timestamp).toLocaleString()}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            File size: {(data.file_size / 1024).toFixed(1)} KB
          </Typography>
        </Box>
      </Paper>
    </Box>
  );
};

export default ResearchPaperInsights;