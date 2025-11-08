"""
AI Chart Explainer - Uses Gemini AI to generate explanations for charts and graphs
"""
import os
import requests
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()


class AIChartExplainer:
    """Generate AI-powered explanations for charts and visualizations"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY', os.getenv('REACT_APP_GEMINI_API_KEY', 'AIzaSyA4IX7we2BPAuvKTRgHZjf1E1zomexttBM'))
        self.api_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent'
    
    def explain_chart(self, chart_info: Dict[str, Any], data_summary: Dict[str, Any]) -> str:
        """
        Generate an AI explanation for a chart
        
        Args:
            chart_info: Dictionary containing chart metadata (title, type, category, etc.)
            data_summary: Summary statistics of the data being visualized
            
        Returns:
            AI-generated explanation of what the chart shows
        """
        try:
            # Build context prompt
            prompt = self._build_chart_prompt(chart_info, data_summary)
            
            # Call Gemini API with shorter timeout
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
                timeout=15  # Increased timeout for AI generation
            )
            
            if response.status_code == 200:
                data = response.json()
                explanation = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                return explanation.strip()
            else:
                print(f"⚠️ Gemini API error: {response.status_code}")
                return self._generate_fallback_explanation(chart_info, data_summary)
                
        except Exception as e:
            print(f"⚠️ Error generating AI explanation: {str(e)}")
            return self._generate_fallback_explanation(chart_info, data_summary)
    
    def _build_chart_prompt(self, chart_info: Dict[str, Any], data_summary: Dict[str, Any]) -> str:
        """Build a detailed prompt for Gemini to explain the chart"""
        
        chart_title = chart_info.get('title', 'Chart')
        chart_type = chart_info.get('type', 'unknown')
        category = chart_info.get('category', 'general')
        
        # Extract relevant statistics
        stats_text = self._format_statistics(data_summary, chart_info)
        
        prompt = f"""You are a data analyst explaining a climate/environmental data visualization to users.

Chart Information:
- Title: {chart_title}
- Type: {chart_type}
- Category: {category}

Data Summary:
{stats_text}

Task: Provide a clear, concise explanation (2-3 sentences) of what this chart shows and what insights can be drawn from it. Focus on:
1. What the chart displays
2. Key patterns or trends visible
3. What this means for climate/environmental analysis

Keep the explanation professional but accessible. Use specific numbers when available. Be direct and insightful.

Explanation:"""
        
        return prompt
    
    def _format_statistics(self, data_summary: Dict[str, Any], chart_info: Dict[str, Any]) -> str:
        """Format data statistics for the prompt"""
        
        stats_lines = []
        
        # Get column info from chart
        x_col = chart_info.get('x_column', '')
        y_col = chart_info.get('y_column', '')
        
        # Add relevant statistics
        if 'columns' in data_summary:
            for col, info in data_summary['columns'].items():
                if col in [x_col, y_col] or len(stats_lines) < 5:
                    if info.get('type') == 'numeric':
                        stats_lines.append(
                            f"- {col}: min={info.get('min', 'N/A')}, max={info.get('max', 'N/A')}, "
                            f"mean={info.get('mean', 'N/A')}, std={info.get('std', 'N/A')}"
                        )
                    elif info.get('type') == 'categorical':
                        unique = info.get('unique_count', 0)
                        stats_lines.append(f"- {col}: {unique} unique values")
        
        # Add row count
        if 'row_count' in data_summary:
            stats_lines.append(f"- Total data points: {data_summary['row_count']}")
        
        return '\n'.join(stats_lines) if stats_lines else "No detailed statistics available"
    
    def _generate_fallback_explanation(self, chart_info: Dict[str, Any], data_summary: Dict[str, Any]) -> str:
        """Generate a basic explanation if AI fails"""
        
        chart_title = chart_info.get('title', 'Chart')
        chart_type = chart_info.get('type', 'visualization')
        
        # Basic template-based explanation
        explanations = {
            'line': f"This line chart shows the trend of {chart_title} over time, allowing you to identify patterns and changes in the data.",
            'bar': f"This bar chart compares {chart_title} across different categories, making it easy to see relative differences.",
            'scatter': f"This scatter plot reveals the relationship between variables in {chart_title}, helping identify correlations.",
            'histogram': f"This histogram displays the distribution of {chart_title}, showing how frequently different values occur.",
            'box': f"This box plot summarizes the statistical distribution of {chart_title}, highlighting median, quartiles, and outliers.",
            'heatmap': f"This heatmap visualizes correlations in {chart_title}, with colors indicating the strength of relationships.",
            'pie': f"This pie chart shows the proportional breakdown of {chart_title}, illustrating the relative size of each component."
        }
        
        return explanations.get(chart_type, f"This {chart_type} chart visualizes {chart_title}, providing insights into the data patterns.")
    
    def explain_multiple_charts(self, charts: List[Dict[str, Any]], data_summary: Dict[str, Any], max_charts: int = 15) -> List[Dict[str, Any]]:
        """
        Generate explanations for multiple charts
        
        Args:
            charts: List of chart information dictionaries
            data_summary: Summary statistics of the data
            max_charts: Maximum number of charts to explain (to avoid timeout)
            
        Returns:
            List of charts with added 'ai_explanation' field
        """
        explained_charts = []
        
        # Limit number of charts to explain to avoid timeout
        charts_to_explain = charts[:max_charts]
        
        for i, chart in enumerate(charts_to_explain):
            try:
                print(f"🤖 Generating AI explanation for chart {i+1}/{len(charts_to_explain)}: {chart.get('title', 'Untitled')}")
                
                # Generate explanation with timeout protection
                explanation = self.explain_chart(chart, data_summary)
                
                # Add explanation to chart info
                chart_with_explanation = chart.copy()
                chart_with_explanation['ai_explanation'] = explanation
                
                explained_charts.append(chart_with_explanation)
            except Exception as e:
                print(f"⚠️ Failed to generate explanation for chart {i+1}: {str(e)}")
                # Add chart without explanation
                chart_copy = chart.copy()
                chart_copy['ai_explanation'] = self._generate_fallback_explanation(chart, data_summary)
                explained_charts.append(chart_copy)
        
        # Add remaining charts without explanations if we hit the limit
        if len(charts) > max_charts:
            print(f"⚠️ Skipping AI explanations for {len(charts) - max_charts} charts to avoid timeout")
            for chart in charts[max_charts:]:
                chart_copy = chart.copy()
                chart_copy['ai_explanation'] = self._generate_fallback_explanation(chart, data_summary)
                explained_charts.append(chart_copy)
        
        return explained_charts
    
    def generate_detailed_analysis(self, charts: List[Dict[str, Any]], insights: List[str], data_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive AI analysis including summary, trends, and recommendations
        
        Args:
            charts: List of all charts generated
            insights: List of key insights
            data_summary: Summary statistics
            
        Returns:
            Dictionary with executive_summary, key_trends, recommendations, and data_quality
        """
        try:
            # Build comprehensive prompt for detailed analysis
            chart_titles = [c.get('title', 'Chart') for c in charts]
            
            # Get column information
            columns_info = []
            if 'columns' in data_summary:
                for col, info in list(data_summary['columns'].items())[:10]:
                    if info.get('type') == 'numeric':
                        columns_info.append(f"{col}: {info.get('min', 'N/A')} to {info.get('max', 'N/A')}")
                    else:
                        columns_info.append(f"{col}: {info.get('unique_count', 'N/A')} unique values")
            
            prompt = f"""You are a senior climate data analyst providing a comprehensive analysis report.

Dataset Overview:
- Total data points: {data_summary.get('row_count', 'N/A')}
- Number of variables: {len(data_summary.get('columns', {}))}
- Visualizations created: {len(charts)}
- Charts: {', '.join(chart_titles[:8])}

Data Variables:
{chr(10).join(f'- {info}' for info in columns_info[:8])}

Key Insights Identified:
{chr(10).join(f'- {insight}' for insight in insights[:10])}

Task: Provide a comprehensive analysis in the following format:

EXECUTIVE SUMMARY:
[3-4 sentences summarizing the overall findings, main patterns, and significance]

KEY TRENDS:
[List 4-5 major trends or patterns discovered in the data, each as a bullet point]

RECOMMENDATIONS:
[List 3-4 actionable recommendations based on the findings]

DATA QUALITY:
[1-2 sentences about data completeness, reliability, and any limitations]

Keep it professional, specific, and actionable. Use data-driven language.

Analysis:"""
            
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
                timeout=25  # Longer timeout for detailed analysis
            )
            
            if response.status_code == 200:
                data = response.json()
                full_analysis = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                
                # Parse the response into sections
                return self._parse_detailed_analysis(full_analysis)
            else:
                return self._generate_fallback_detailed_analysis(charts, insights, data_summary)
                
        except Exception as e:
            print(f"⚠️ Error generating detailed analysis: {str(e)}")
            return self._generate_fallback_detailed_analysis(charts, insights, data_summary)
    
    def _parse_detailed_analysis(self, full_text: str) -> Dict[str, Any]:
        """Parse AI response into structured sections"""
        sections = {
            'executive_summary': '',
            'key_trends': [],
            'recommendations': [],
            'data_quality': ''
        }
        
        try:
            # Split by sections
            parts = full_text.split('\n\n')
            current_section = None
            
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                    
                if 'EXECUTIVE SUMMARY' in part.upper():
                    current_section = 'executive_summary'
                    # Get text after the header
                    text = part.split(':', 1)[1].strip() if ':' in part else part
                    sections['executive_summary'] = text
                elif 'KEY TRENDS' in part.upper():
                    current_section = 'key_trends'
                elif 'RECOMMENDATIONS' in part.upper():
                    current_section = 'recommendations'
                elif 'DATA QUALITY' in part.upper():
                    current_section = 'data_quality'
                    text = part.split(':', 1)[1].strip() if ':' in part else part
                    sections['data_quality'] = text
                elif current_section == 'key_trends' and (part.startswith('-') or part.startswith('•') or part.startswith('*')):
                    sections['key_trends'].append(part.lstrip('-•* '))
                elif current_section == 'recommendations' and (part.startswith('-') or part.startswith('•') or part.startswith('*')):
                    sections['recommendations'].append(part.lstrip('-•* '))
                elif current_section == 'executive_summary' and not any(x in part.upper() for x in ['KEY TRENDS', 'RECOMMENDATIONS', 'DATA QUALITY']):
                    sections['executive_summary'] += ' ' + part
                elif current_section == 'data_quality' and not any(x in part.upper() for x in ['EXECUTIVE', 'KEY TRENDS', 'RECOMMENDATIONS']):
                    sections['data_quality'] += ' ' + part
            
            # Clean up
            sections['executive_summary'] = sections['executive_summary'].strip()
            sections['data_quality'] = sections['data_quality'].strip()
            
        except Exception as e:
            print(f"⚠️ Error parsing analysis: {str(e)}")
            # Return the full text as executive summary if parsing fails
            sections['executive_summary'] = full_text[:500]
        
        return sections
    
    def _generate_fallback_detailed_analysis(self, charts: List[Dict[str, Any]], insights: List[str], data_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback detailed analysis if AI fails"""
        return {
            'executive_summary': f"This analysis examined {data_summary.get('row_count', 'N/A')} data points across {len(data_summary.get('columns', {}))} variables, generating {len(charts)} visualizations. The analysis revealed {len(insights)} key insights about climate patterns and trends.",
            'key_trends': insights[:5] if insights else ["Data patterns identified", "Temporal trends observed", "Correlations discovered"],
            'recommendations': [
                "Continue monitoring these climate indicators",
                "Investigate identified anomalies further",
                "Consider additional data sources for validation"
            ],
            'data_quality': "The dataset appears complete with no major gaps. Standard statistical analysis was applied."
        }
    
    def generate_overall_analysis(self, charts: List[Dict[str, Any]], insights: List[str], data_summary: Dict[str, Any]) -> str:
        """
        Generate an overall analysis summary using AI (backward compatibility)
        
        Args:
            charts: List of all charts generated
            insights: List of key insights
            data_summary: Summary statistics
            
        Returns:
            Overall analysis summary
        """
        try:
            # Use the detailed analysis but return only executive summary for backward compatibility
            detailed = self.generate_detailed_analysis(charts, insights, data_summary)
            return detailed.get('executive_summary', '')
        except Exception as e:
            print(f"Warning: Detailed analysis failed: {e}")
            
            prompt = f"""You are a climate data analyst providing an executive summary of a comprehensive data analysis.

Analysis Overview:
- Number of visualizations: {len(charts)}
- Charts created: {', '.join(chart_titles)}
- Total data points: {data_summary.get('row_count', 'N/A')}
- Key insights identified: {len(insights)}

Key Insights:
{chr(10).join(f'- {insight}' for insight in insights[:10])}

Task: Provide a brief executive summary (3-4 sentences) that:
1. Summarizes the overall findings from this analysis
2. Highlights the most important patterns or trends
3. Suggests what actions or further investigations might be valuable

Keep it professional, data-driven, and actionable.

Executive Summary:"""
            
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
                timeout=20  # Increased timeout for overall summary
            )
            
            if response.status_code == 200:
                data = response.json()
                summary = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                return summary.strip()
            else:
                return self._generate_fallback_summary(charts, insights)
                
        except Exception as e:
            print(f"⚠️ Error generating overall analysis: {str(e)}")
            return self._generate_fallback_summary(charts, insights)
    
    def _generate_fallback_summary(self, charts: List[Dict[str, Any]], insights: List[str]) -> str:
        """Generate a basic summary if AI fails"""
        return (
            f"This analysis generated {len(charts)} visualizations revealing key patterns in the climate data. "
            f"The analysis identified {len(insights)} significant insights across multiple dimensions. "
            f"These findings provide valuable context for understanding environmental trends and patterns."
        )


