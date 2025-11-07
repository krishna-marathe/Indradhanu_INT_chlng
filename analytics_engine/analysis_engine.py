"""
Dynamic Analytics Engine - Main orchestrator for data analysis pipeline
"""
from typing import Dict, List, Any, Tuple
import os
from datetime import datetime


class AnalysisEngine:
    """
    Main analytics engine that orchestrates the entire analysis pipeline
    """
    
    def __init__(self, output_dir: str = "visuals"):
        self.output_dir = output_dir
        self._components_initialized = False
    
    def _init_components(self):
        """Lazy initialization of analysis components"""
        if not self._components_initialized:
            from .data_summary import DataSummary
            from .chart_generator import ChartGenerator
            from .insights_generator import InsightsGenerator
            from .ai_chart_explainer import AIChartExplainer
            
            self.data_summary = DataSummary()
            self.chart_generator = ChartGenerator(self.output_dir)
            self.insights_generator = InsightsGenerator()
            self.ai_explainer = AIChartExplainer()
            self._components_initialized = True
    
    def get_chart_generator(self):
        """Get the chart generator instance"""
        self._init_components()
        return self.chart_generator
        
    def analyze_dataset(self, file_path: str, filename: str) -> Dict[str, Any]:
        """
        Complete analysis pipeline for any dataset
        
        Args:
            file_path: Path to the dataset file
            filename: Unique filename identifier
            
        Returns:
            Dictionary containing all analysis results
        """
        print(f"🔍 Starting dynamic analysis for: {filename}")
        
        # Initialize components lazily
        self._init_components()
        
        # Lazy import heavy libraries
        import pandas as pd
        
        # Step 1: Load and clean data
        from .data_loader import load_dataset
        from .data_cleaner import clean_data
        
        df = load_dataset(file_path)
        if df is None or df.empty:
            raise ValueError("Failed to load dataset or dataset is empty")
            
        df = clean_data(df)
        print(f"📊 Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Step 2: Analyze dataset structure
        schema = self._analyze_schema(df)
        print(f"🔬 Schema detected: {schema['summary']}")
        
        # Step 3: Generate descriptive statistics
        statistics = self.data_summary.generate_summary(df, schema)
        
        # Step 4: Generate dynamic visualizations
        charts = self.chart_generator.generate_charts(df, schema, filename)
        
        # Step 4.5: Generate AI explanations for charts (with timeout protection)
        try:
            print(f"🤖 Generating AI explanations for up to 15 charts...")
            charts_with_explanations = self.ai_explainer.explain_multiple_charts(charts, statistics, max_charts=15)
        except Exception as e:
            print(f"⚠️ AI explanation generation failed: {str(e)}")
            print("⚠️ Continuing without AI explanations...")
            charts_with_explanations = charts
        
        # Step 5: Generate insights
        insights = self.insights_generator.generate_insights(df, schema, statistics)
        
        # Step 5.5: Generate comprehensive AI analysis (with timeout protection)
        try:
            print("🤖 Generating comprehensive AI analysis...")
            ai_detailed_analysis = self.ai_explainer.generate_detailed_analysis(charts_with_explanations, insights, statistics)
            ai_summary = ai_detailed_analysis.get('executive_summary', '')
        except Exception as e:
            print(f"⚠️ AI analysis generation failed: {str(e)}")
            ai_summary = f"Analysis generated {len(charts)} visualizations and {len(insights)} key insights from the data."
            ai_detailed_analysis = {
                'executive_summary': ai_summary,
                'key_trends': insights[:5],
                'recommendations': [],
                'data_quality': 'Analysis completed successfully.'
            }
        
        # Step 6: Compile results
        results = {
            'filename': filename,
            'timestamp': datetime.now().isoformat(),
            'dataset_info': {
                'rows': len(df),
                'columns': len(df.columns),
                'size_mb': round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
            },
            'schema': schema,
            'statistics': statistics,
            'charts': charts_with_explanations,  # Charts now include AI explanations
            'insights': insights,
            'ai_summary': ai_summary,  # Overall AI analysis summary (backward compatibility)
            'ai_detailed_analysis': ai_detailed_analysis,  # Comprehensive AI analysis
            'column_info': self._get_column_info(df)
        }
        
        print(f"✅ Analysis complete: {len(charts)} charts, {len(insights)} insights")
        return results
    
    def _analyze_schema(self, df) -> Dict[str, Any]:
        """
        Automatically detect column types and data structure
        """
        import pandas as pd
        
        schema = {
            'numeric_columns': [],
            'categorical_columns': [],
            'datetime_columns': [],
            'text_columns': [],
            'boolean_columns': [],
            'summary': {}
        }
        
        for column in df.columns:
            col_data = df[column]
            
            # Check for datetime
            if pd.api.types.is_datetime64_any_dtype(col_data):
                schema['datetime_columns'].append(column)
            # Check for boolean
            elif pd.api.types.is_bool_dtype(col_data):
                schema['boolean_columns'].append(column)
            # Check for numeric
            elif pd.api.types.is_numeric_dtype(col_data):
                schema['numeric_columns'].append(column)
            # Check for categorical (low cardinality strings)
            elif col_data.dtype == 'object':
                unique_ratio = col_data.nunique() / len(col_data)
                if unique_ratio < 0.5 and col_data.nunique() < 50:  # Heuristic for categorical
                    schema['categorical_columns'].append(column)
                else:
                    schema['text_columns'].append(column)
            else:
                # Default to categorical for unknown types
                schema['categorical_columns'].append(column)
        
        # Generate summary
        schema['summary'] = {
            'numeric': len(schema['numeric_columns']),
            'categorical': len(schema['categorical_columns']),
            'datetime': len(schema['datetime_columns']),
            'text': len(schema['text_columns']),
            'boolean': len(schema['boolean_columns'])
        }
        
        return schema
    
    def _get_column_info(self, df) -> Dict[str, Dict]:
        """
        Get detailed information about each column
        """
        import pandas as pd
        
        column_info = {}
        
        for column in df.columns:
            col_data = df[column]
            info = {
                'dtype': str(col_data.dtype),
                'non_null_count': col_data.count(),
                'null_count': col_data.isnull().sum(),
                'unique_count': col_data.nunique(),
                'memory_usage': col_data.memory_usage(deep=True)
            }
            
            # Add type-specific info
            if pd.api.types.is_numeric_dtype(col_data):
                info.update({
                    'min': col_data.min(),
                    'max': col_data.max(),
                    'mean': col_data.mean(),
                    'std': col_data.std()
                })
            elif col_data.dtype == 'object':
                info.update({
                    'most_frequent': col_data.mode().iloc[0] if not col_data.mode().empty else None,
                    'avg_length': col_data.astype(str).str.len().mean()
                })
            
            column_info[column] = info
            
        return column_info