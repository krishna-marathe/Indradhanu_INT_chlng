"""
Climate Sphere Analytics Engine Package
Dynamic data analysis and visualization toolkit
"""

__version__ = "1.0.0"
__author__ = "Climate Sphere Team"

# Lazy imports to avoid startup delays
def get_analysis_engine():
    """Get AnalysisEngine with lazy import"""
    from .analysis_engine import AnalysisEngine
    return AnalysisEngine

def get_chart_generator():
    """Get ChartGenerator with lazy import"""
    from .chart_generator import ChartGenerator
    return ChartGenerator

def get_data_summary():
    """Get DataSummary with lazy import"""
    from .data_summary import DataSummary
    return DataSummary

def get_insights_generator():
    """Get InsightsGenerator with lazy import"""
    from .insights_generator import InsightsGenerator
    return InsightsGenerator

# Export main classes for direct import if needed
__all__ = [
    'get_analysis_engine',
    'get_chart_generator', 
    'get_data_summary',
    'get_insights_generator'
]