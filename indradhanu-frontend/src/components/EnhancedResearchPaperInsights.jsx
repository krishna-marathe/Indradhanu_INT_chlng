import React from 'react';
import { 
  Paper, Typography, Chip, Box, Divider, Grid, Card, CardContent,
  List, ListItem, ListItemText, ListItemIcon, Accordion, AccordionSummary, AccordionDetails
} from '@mui/material';
import {
  Description, LocationOn, DateRange, TrendingUp, Science, Insights, Assessment,
  ExpandMore, BugReport, Recommend, Analytics, Functions
} from '@mui/icons-material';

const EnhancedResearchPaperInsights = ({ data }) => {
  if (!data || !data.analysis) return null;

  const analysis = data.analysis;

  const getConfidenceColor = (confidence) => {
    switch (confidence) {
      case 'high': return 'success';
      case 'medium': return 'warning';
      case 'low': return 'error';
      default: return 'default';
    }
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          📄 Comprehensive Research Paper Analysis
        </Typography>
        
        {/* Document Info */}
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} md={6}>
            <Typography variant="body2" color="text.secondary">Original Filename</Typography>
            <Typography variant="body1" sx={{ fontWeight: 'medium' }}>{data.original_filename}</Typography>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="body2" color="text.secondary">Document Type</Typography>
            <Chip label={analysis.document_type || 'Research Paper'} color="primary" size="small" />
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="body2" color="text.secondary">Analysis Confidence</Typography>
            <Chip 
              label={`${analysis.analysis_confidence?.toUpperCase() || 'MEDIUM'} (${analysis.confidence_score || 0}/12)`}
              color={getConfidenceColor(analysis.analysis_confidence)}
              size="small"
            />
          </Grid>
        </Grid>

        <Divider sx={{ mb: 3 }} />

        {/* Executive Summary */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Description /> Executive Summary
          </Typography>
          <Paper sx={{ p: 2, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
            <Typography variant="body1" sx={{ lineHeight: 1.8 }}>
              {analysis.executive_summary || analysis.summary || 'No summary available'}
            </Typography>
          </Paper>
          <Box sx={{ mt: 1, display: 'flex', gap: 2 }}>
            <Chip label={`${analysis.word_count?.toLocaleString() || 0} words`} size="small" />
            {analysis.sections_found && (
              <Chip label={`${analysis.sections_found.length} sections`} size="small" color="info" />
            )}
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
                    <LocationOn color="primary" /> Geographical Coverage ({analysis.regions.length})
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
                    <DateRange color="secondary" /> Temporal Coverage ({analysis.years.length} years)
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, maxHeight: 150, overflowY: 'auto' }}>
                    {analysis.years.map((year, i) => (
                      <Chip key={i} label={year} color="secondary" size="small" />
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
                    🌍 Climate & Environmental Keywords ({analysis.climate_keywords.length})
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {analysis.climate_keywords.map((keyword, i) => (
                      <Chip key={i} label={keyword} color="primary" variant="outlined" size="small" />
                    ))}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>

        {/* Methodology Section */}
        {analysis.methodology && (
          <>
            <Divider sx={{ my: 3 }} />
            <Accordion defaultExpanded>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Science color="warning" /> Research Methodology
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={2}>
                  {analysis.methodology.research_design && analysis.methodology.research_design.length > 0 && (
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" gutterBottom>Research Design:</Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {analysis.methodology.research_design.map((item, i) => (
                          <Chip key={i} label={item} size="small" variant="outlined" />
                        ))}
                      </Box>
                    </Grid>
                  )}
                  
                  {analysis.methodology.data_collection && analysis.methodology.data_collection.length > 0 && (
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" gutterBottom">Data Collection:</Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {analysis.methodology.data_collection.map((item, i) => (
                          <Chip key={i} label={item} size="small" variant="outlined" color="info" />
                        ))}
                      </Box>
                    </Grid>
                  )}
                  
                  {analysis.methodology.analysis_techniques && analysis.methodology.analysis_techniques.length > 0 && (
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" gutterBottom>Analysis Techniques:</Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {analysis.methodology.analysis_techniques.map((item, i) => (
                          <Chip key={i} label={item} size="small" variant="outlined" color="success" />
                        ))}
                      </Box>
                    </Grid>
                  )}
                  
                  {analysis.methodology.tools_used && analysis.methodology.tools_used.length > 0 && (
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" gutterBottom>Tools & Software:</Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {analysis.methodology.tools_used.map((item, i) => (
                          <Chip key={i} label={item} size="small" variant="outlined" color="secondary" />
                        ))}
                      </Box>
                    </Grid>
                  )}
                  
                  {analysis.methodology.sample_info && analysis.methodology.sample_info.length > 0 && (
                    <Grid item xs={12}>
                      <Typography variant="subtitle2" gutterBottom>Sample Information:</Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {analysis.methodology.sample_info.map((item, i) => (
                          <Chip key={i} label={`n=${item}`} size="small" color="warning" />
                        ))}
                      </Box>
                    </Grid>
                  )}
                </Grid>
              </AccordionDetails>
            </Accordion>
          </>
        )}

        {/* Key Findings */}
        {analysis.key_findings && analysis.key_findings.length > 0 && (
          <>
            <Divider sx={{ my: 3 }} />
            <Box>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Insights color="error" /> Key Findings ({analysis.key_findings.length})
              </Typography>
              <List dense>
                {analysis.key_findings.map((finding, i) => (
                  <ListItem key={i} sx={{ bgcolor: 'grey.50', mb: 1, borderRadius: 1 }}>
                    <ListItemIcon>
                      <Assessment color="error" />
                    </ListItemIcon>
                    <ListItemText 
                      primary={`${i + 1}. ${finding}`}
                      primaryTypographyProps={{ variant: 'body2' }}
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          </>
        )}

        {/* Statistical Data */}
        {analysis.statistical_data && (
          <>
            <Divider sx={{ my: 3 }} />
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Functions color="success" /> Statistical Data
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={2}>
                  {analysis.statistical_data.percentages && analysis.statistical_data.percentages.length > 0 && (
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" gutterBottom>Percentages:</Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {analysis.statistical_data.percentages.map((item, i) => (
                          <Chip key={i} label={item} size="small" color="success" />
                        ))}
                      </Box>
                    </Grid>
                  )}
                  
                  {analysis.statistical_data.p_values && analysis.statistical_data.p_values.length > 0 && (
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" gutterBottom>P-values:</Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {analysis.statistical_data.p_values.map((item, i) => (
                          <Chip key={i} label={item} size="small" color="error" />
                        ))}
                      </Box>
                    </Grid>
                  )}
                  
                  {analysis.statistical_data.correlations && analysis.statistical_data.correlations.length > 0 && (
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" gutterBottom>Correlations:</Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {analysis.statistical_data.correlations.map((item, i) => (
                          <Chip key={i} label={item} size="small" color="info" />
                        ))}
                      </Box>
                    </Grid>
                  )}
                  
                  {analysis.statistical_data.sample_sizes && analysis.statistical_data.sample_sizes.length > 0 && (
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" gutterBottom>Sample Sizes:</Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {analysis.statistical_data.sample_sizes.map((item, i) => (
                          <Chip key={i} label={item} size="small" color="warning" />
                        ))}
                      </Box>
                    </Grid>
                  )}
                </Grid>
              </AccordionDetails>
            </Accordion>
          </>
        )}

        {/* Research Gaps */}
        {analysis.research_gaps && analysis.research_gaps.length > 0 && (
          <>
            <Divider sx={{ my: 3 }} />
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <BugReport color="warning" /> Research Gaps & Limitations ({analysis.research_gaps.length})
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <List dense>
                  {analysis.research_gaps.map((gap, i) => (
                    <ListItem key={i}>
                      <ListItemIcon>
                        <BugReport color="warning" />
                      </ListItemIcon>
                      <ListItemText primary={gap} primaryTypographyProps={{ variant: 'body2' }} />
                    </ListItem>
                  ))}
                </List>
              </AccordionDetails>
            </Accordion>
          </>
        )}

        {/* Recommendations */}
        {analysis.recommendations && analysis.recommendations.length > 0 && (
          <>
            <Divider sx={{ my: 3 }} />
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Recommend color="success" /> Recommendations & Implications ({analysis.recommendations.length})
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <List dense>
                  {analysis.recommendations.map((rec, i) => (
                    <ListItem key={i}>
                      <ListItemIcon>
                        <Recommend color="success" />
                      </ListItemIcon>
                      <ListItemText primary={rec} primaryTypographyProps={{ variant: 'body2' }} />
                    </ListItem>
                  ))}
                </List>
              </AccordionDetails>
            </Accordion>
          </>
        )}

        {/* Document Preview */}
        {analysis.preview && (
          <>
            <Divider sx={{ my: 3 }} />
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Typography variant="h6">📖 Document Preview</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Paper sx={{ p: 2, bgcolor: 'grey.50', maxHeight: 300, overflowY: 'auto' }}>
                  <Typography variant="body2" sx={{ fontFamily: 'monospace', lineHeight: 1.6, whiteSpace: 'pre-wrap' }}>
                    {analysis.preview}
                  </Typography>
                </Paper>
              </AccordionDetails>
            </Accordion>
          </>
        )}

        {/* Metadata */}
        <Divider sx={{ my: 3 }} />
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 2 }}>
          <Typography variant="caption" color="text.secondary">
            Analyzed on: {new Date(data.timestamp).toLocaleString()}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            File size: {(data.file_size / 1024).toFixed(1)} KB
          </Typography>
          {analysis.sections_found && (
            <Typography variant="caption" color="text.secondary">
              Sections: {analysis.sections_found.join(', ')}
            </Typography>
          )}
        </Box>
      </Paper>
    </Box>
  );
};

export default EnhancedResearchPaperInsights;