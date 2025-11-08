"""
LLM-Powered Chart Advisor - Uses AI to recommend and configure charts intelligently
"""
import os
import requests
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class LLMChartAdvisor:
    """Uses LLM to intelligently recommend charts based on data analysis"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY', os.getenv('REACT_APP_GEMINI_API_KEY'))
        self.api_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent'
    
    def analyze_and_recommend_charts(self, data_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze data and get LLM recommendations for chart types
        
        Args:
            data_summary: Dictionary with data statistics and column info
            
        Returns:
            Dictionary with chart recommendations and configurations
        """
        try:
            prompt = self._build_analysis_prompt(data_summary)
            
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                headers={'Content-Type': 'application/json'},
                json={
                    'contents': [{
                        'parts': [{
                            'text': prompt
                        }]
                    }]
                },
                timeout=20
            )
            
            if response.status_code == 200:
                data = response.json()
                recommendations = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                return self._parse_recommendations(recommendations)
            else:
                print(f"⚠️ LLM API error: {response.status_code}")
                return self._generate_fallback_recommendations(data_summary)
                
        except Exception as e:
            print(f"⚠️ Error getting LLM recommendations: {str(e)}")
            return self._generate_fallback_recommendations(data_summary)
    
    def _build_analysis_prompt(self, data_summary: Dict[str, Any]) -> str:
        """Build prompt for LLM to analyze data and recommend charts"""
        
        # Extract column information
        columns_info = []
        numeric_cols = []
        categorical_cols = []
        temporal_cols = []
        
        if 'columns' in data_summary:
            for col, info in data_summary['columns'].items():
                col_type = info.get('type', 'unknown')
                
                if col_type == 'numeric':
                    numeric_cols.append(col)
                    columns_info.append(
                        f"- {col} (numeric): min={info.get('min', 'N/A')}, "
                        f"max={info.get('max', 'N/A')}, mean={info.get('mean', 'N/A')}"
                    )
                elif col_type == 'categorical':
                    categorical_cols.append(col)
                    columns_info.append(
                        f"- {col} (categorical): {info.get('unique_count', 'N/A')} unique values"
                    )
                elif col_type == 'datetime':
                    temporal_cols.append(col)
                    columns_info.append(f"- {col} (datetime/temporal)")
        
        prompt = f"""You are a data visualization expert analyzing climate/environmental data.

Dataset Overview:
- Total rows: {data_summary.get('row_count', 'N/A')}
- Total columns: {len(data_summary.get('columns', {}))}
- Numeric columns: {len(numeric_cols)}
- Categorical columns: {len(categorical_cols)}
- Temporal columns: {len(temporal_cols)}

Column Details:
{chr(10).join(columns_info[:15])}

Task: Recommend the TOP 5 most insightful visualizations for this dataset. For each recommendation, provide:

1. CHART_TYPE: (histogram, scatter, line, bar, heatmap, boxplot, etc.)
2. X_AXIS: column name
3. Y_AXIS: column name (if applicable)
4. TITLE: descriptive chart title
5. INSIGHT: what this chart will reveal (1 sentence)
6. PRIORITY: HIGH, MEDIUM, or LOW

Format your response EXACTLY like this:

CHART 1:
TYPE: scatter
X: temperature
Y: humidity
TITLE: Temperature vs Humidity Relationship
INSIGHT: Shows correlation between temperature and humidity levels
PRIORITY: HIGH

CHART 2:
[continue pattern...]

Provide exactly 5 chart recommendations. Focus on charts that reveal patterns, trends, correlations, and anomalies in climate data."""
        
        return prompt
    
    def _parse_recommendations(self, llm_response: str) -> Dict[str, Any]:
        """Parse LLM response into structured chart recommendations"""
        
        recommendations = []
        
        try:
            # Split by CHART markers
            chart_blocks = llm_response.split('CHART ')[1:]  # Skip first empty split
            
            for block in chart_blocks[:5]:  # Limit to 5 charts
                chart_config = {}
                lines = block.strip().split('\n')
                
                for line in lines:
                    line = line.strip()
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().upper()
                        value = value.strip()
                        
                        if key == 'TYPE':
                            chart_config['type'] = value.lower()
                        elif key == 'X' or key == 'X_AXIS':
                            chart_config['x_column'] = value
                        elif key == 'Y' or key == 'Y_AXIS':
                            chart_config['y_column'] = value
                        elif key == 'TITLE':
                            chart_config['title'] = value
                        elif key == 'INSIGHT':
                            chart_config['insight'] = value
                        elif key == 'PRIORITY':
                            chart_config['priority'] = value.upper()
                
                if 'type' in chart_config and 'title' in chart_config:
                    recommendations.append(chart_config)
            
        except Exception as e:
            print(f"⚠️ Error parsing LLM recommendations: {str(e)}")
        
        return {
            'recommendations': recommendations,
            'total_recommended': len(recommendations)
        }
    
    def _generate_fallback_recommendations(self, data_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Generate basic recommendations if LLM fails"""
        
        recommendations = []
        numeric_cols = []
        categorical_cols = []
        
        if 'columns' in data_summary:
            for col, info in data_summary['columns'].items():
                if info.get('type') == 'numeric':
                    numeric_cols.append(col)
                elif info.get('type') == 'categorical':
                    categorical_cols.append(col)
        
        # Histogram for first numeric column
        if numeric_cols:
            recommendations.append({
                'type': 'histogram',
                'x_column': numeric_cols[0],
                'title': f'Distribution of {numeric_cols[0]}',
                'insight': f'Shows the frequency distribution of {numeric_cols[0]} values',
                'priority': 'HIGH'
            })
        
        # Scatter plot for first two numeric columns
        if len(numeric_cols) >= 2:
            recommendations.append({
                'type': 'scatter',
                'x_column': numeric_cols[0],
                'y_column': numeric_cols[1],
                'title': f'{numeric_cols[0]} vs {numeric_cols[1]}',
                'insight': f'Reveals correlation between {numeric_cols[0]} and {numeric_cols[1]}',
                'priority': 'HIGH'
            })
        
        # Bar chart for first categorical column
        if categorical_cols:
            recommendations.append({
                'type': 'bar',
                'x_column': categorical_cols[0],
                'title': f'Distribution of {categorical_cols[0]}',
                'insight': f'Compares frequency across {categorical_cols[0]} categories',
                'priority': 'MEDIUM'
            })
        
        # Correlation heatmap if multiple numeric columns
        if len(numeric_cols) > 2:
            recommendations.append({
                'type': 'heatmap',
                'title': 'Correlation Matrix',
                'insight': 'Shows relationships between all numeric variables',
                'priority': 'HIGH'
            })
        
        return {
            'recommendations': recommendations,
            'total_recommended': len(recommendations)
        }
    
    def generate_chart_insights(self, chart_config: Dict[str, Any], data_stats: Dict[str, Any]) -> str:
        """
        Generate AI-powered insights for a specific chart
        
        Args:
            chart_config: Chart configuration (type, columns, etc.)
            data_stats: Relevant statistics for the chart
            
        Returns:
            AI-generated insight about what the chart shows
        """
        try:
            prompt = f"""You are analyzing a climate data visualization.

Chart Type: {chart_config.get('type', 'unknown')}
Chart Title: {chart_config.get('title', 'Chart')}
Variables: {', '.join([chart_config.get('x_column', ''), chart_config.get('y_column', '')])}

Data Statistics:
{self._format_stats(data_stats)}

Task: Provide a concise insight (2-3 sentences) about what this chart reveals. Focus on:
- Key patterns or trends
- Notable values or anomalies
- Climate/environmental implications

Insight:"""
            
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                headers={'Content-Type': 'application/json'},
                json={
                    'contents': [{
                        'parts': [{
                            'text': prompt
                        }]
                    }]
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                insight = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                return insight.strip()
            else:
                return chart_config.get('insight', 'Chart shows data patterns and trends.')
                
        except Exception as e:
            print(f"⚠️ Error generating chart insight: {str(e)}")
            return chart_config.get('insight', 'Chart shows data patterns and trends.')
    
    def _format_stats(self, data_stats: Dict[str, Any]) -> str:
        """Format statistics for prompt"""
        stats_lines = []
        for key, value in data_stats.items():
            if isinstance(value, (int, float)):
                stats_lines.append(f"- {key}: {value:.2f}")
            else:
                stats_lines.append(f"- {key}: {value}")
        return '\n'.join(stats_lines[:10])
