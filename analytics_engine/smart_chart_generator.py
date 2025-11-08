"""
Smart Chart Generator - Combines LLM intelligence with Python visualization libraries
"""
import os
from typing import Dict, List, Any
from analytics_engine.llm_chart_advisor import LLMChartAdvisor


class SmartChartGenerator:
    """
    Intelligent chart generation using LLM recommendations + Python libraries
    """
    
    def __init__(self, output_dir: str = "visuals"):
        self.output_dir = output_dir
        self.llm_advisor = LLMChartAdvisor()
        self.ensure_output_dir()
        self._imports_loaded = False
        
    def ensure_output_dir(self):
        """Ensure output directory exists"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def _load_imports(self):
        """Lazy loading of heavy libraries"""
        if not self._imports_loaded:
            import pandas as pd
            import numpy as np
            import warnings
            warnings.filterwarnings('ignore')
            
            import matplotlib
            matplotlib.use('Agg')
            
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            plt.style.use('default')
            sns.set_palette("husl")
            
            self.pd = pd
            self.np = np
            self.plt = plt
            self.sns = sns
            
            self._imports_loaded = True
    
    def generate_smart_charts(self, df, schema: Dict[str, Any], filename: str) -> List[Dict[str, Any]]:
        """
        Generate charts using LLM recommendations
        
        Args:
            df: pandas DataFrame with data
            schema: Data schema with column types
            filename: Base filename for saving charts
            
        Returns:
            List of generated chart metadata
        """
        self._load_imports()
        
        print("🤖 Asking LLM for chart recommendations...")
        
        # Get LLM recommendations
        recommendations = self.llm_advisor.analyze_and_recommend_charts(schema)
        
        print(f"✅ LLM recommended {recommendations['total_recommended']} charts")
        
        charts = []
        
        # Generate each recommended chart
        for i, rec in enumerate(recommendations['recommendations'], 1):
            print(f"📊 Generating chart {i}/{recommendations['total_recommended']}: {rec.get('title', 'Chart')}")
            
            chart_info = self._generate_chart_from_recommendation(df, rec, filename, i)
            
            if chart_info:
                # Add LLM insight to chart
                chart_info['ai_insight'] = rec.get('insight', '')
                chart_info['priority'] = rec.get('priority', 'MEDIUM')
                charts.append(chart_info)
        
        print(f"✅ Successfully generated {len(charts)} AI-recommended charts")
        return charts
    
    def _generate_chart_from_recommendation(self, df, rec: Dict[str, Any], 
                                           filename: str, index: int) -> Dict[str, Any]:
        """Generate a single chart based on LLM recommendation"""
        
        chart_type = rec.get('type', 'line')
        x_col = rec.get('x_column')
        y_col = rec.get('y_column')
        title = rec.get('title', 'Chart')
        
        try:
            # Route to appropriate chart generator
            if chart_type == 'histogram':
                return self._create_histogram(df, x_col, title, filename, index)
            elif chart_type == 'scatter':
                return self._create_scatter(df, x_col, y_col, title, filename, index)
            elif chart_type == 'line':
                return self._create_line(df, x_col, y_col, title, filename, index)
            elif chart_type == 'bar':
                return self._create_bar(df, x_col, title, filename, index)
            elif chart_type == 'heatmap':
                return self._create_heatmap(df, title, filename, index)
            elif chart_type == 'boxplot':
                return self._create_boxplot(df, x_col, y_col, title, filename, index)
            else:
                print(f"⚠️ Unknown chart type: {chart_type}")
                return None
                
        except Exception as e:
            print(f"❌ Error generating {chart_type} chart: {str(e)}")
            return None
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize filename"""
        import re
        sanitized = re.sub(r'[^\w\s-]', '_', name)
        sanitized = re.sub(r'[\s_]+', '_', sanitized)
        return sanitized
    
    def _create_histogram(self, df, column: str, title: str, filename: str, index: int) -> Dict[str, Any]:
        """Create histogram chart"""
        if column not in df.columns:
            return None
            
        safe_name = self._sanitize_filename(f"{index}_{title}")
        chart_path = os.path.join(self.output_dir, f"{safe_name}_{filename}.png")
        
        self.plt.figure(figsize=(10, 6))
        self.plt.hist(df[column].dropna(), bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        self.plt.title(title, fontsize=14, fontweight='bold')
        self.plt.xlabel(column, fontsize=12)
        self.plt.ylabel('Frequency', fontsize=12)
        self.plt.grid(True, alpha=0.3)
        self.plt.tight_layout()
        self.plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        self.plt.close()
        
        return {
            'type': 'histogram',
            'title': title,
            'url': f'/visuals/{os.path.basename(chart_path)}',
            'filename': os.path.basename(chart_path),
            'variables': [column]
        }
    
    def _create_scatter(self, df, x_col: str, y_col: str, title: str, filename: str, index: int) -> Dict[str, Any]:
        """Create scatter plot"""
        if x_col not in df.columns or y_col not in df.columns:
            return None
            
        safe_name = self._sanitize_filename(f"{index}_{title}")
        chart_path = os.path.join(self.output_dir, f"{safe_name}_{filename}.png")
        
        self.plt.figure(figsize=(10, 8))
        self.plt.scatter(df[x_col], df[y_col], alpha=0.6, s=50, color='coral')
        self.plt.title(title, fontsize=14, fontweight='bold')
        self.plt.xlabel(x_col, fontsize=12)
        self.plt.ylabel(y_col, fontsize=12)
        self.plt.grid(True, alpha=0.3)
        
        # Add trend line
        try:
            z = self.np.polyfit(df[x_col].dropna(), df[y_col].dropna(), 1)
            p = self.np.poly1d(z)
            self.plt.plot(df[x_col], p(df[x_col]), "r--", alpha=0.8, linewidth=2, label='Trend')
            self.plt.legend()
        except:
            pass
        
        self.plt.tight_layout()
        self.plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        self.plt.close()
        
        return {
            'type': 'scatter',
            'title': title,
            'url': f'/visuals/{os.path.basename(chart_path)}',
            'filename': os.path.basename(chart_path),
            'variables': [x_col, y_col]
        }
    
    def _create_line(self, df, x_col: str, y_col: str, title: str, filename: str, index: int) -> Dict[str, Any]:
        """Create line chart"""
        if y_col not in df.columns:
            return None
            
        safe_name = self._sanitize_filename(f"{index}_{title}")
        chart_path = os.path.join(self.output_dir, f"{safe_name}_{filename}.png")
        
        self.plt.figure(figsize=(12, 6))
        
        if x_col and x_col in df.columns:
            self.plt.plot(df[x_col], df[y_col], linewidth=2, marker='o', markersize=4)
            self.plt.xlabel(x_col, fontsize=12)
        else:
            self.plt.plot(df[y_col], linewidth=2, marker='o', markersize=4)
            self.plt.xlabel('Index', fontsize=12)
        
        self.plt.title(title, fontsize=14, fontweight='bold')
        self.plt.ylabel(y_col, fontsize=12)
        self.plt.grid(True, alpha=0.3)
        self.plt.tight_layout()
        self.plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        self.plt.close()
        
        return {
            'type': 'line',
            'title': title,
            'url': f'/visuals/{os.path.basename(chart_path)}',
            'filename': os.path.basename(chart_path),
            'variables': [x_col, y_col] if x_col else [y_col]
        }
    
    def _create_bar(self, df, column: str, title: str, filename: str, index: int) -> Dict[str, Any]:
        """Create bar chart"""
        if column not in df.columns:
            return None
            
        safe_name = self._sanitize_filename(f"{index}_{title}")
        chart_path = os.path.join(self.output_dir, f"{safe_name}_{filename}.png")
        
        value_counts = df[column].value_counts().head(10)
        
        self.plt.figure(figsize=(12, 6))
        bars = self.plt.bar(range(len(value_counts)), value_counts.values, 
                      color=self.plt.cm.Set3(self.np.linspace(0, 1, len(value_counts))))
        self.plt.title(title, fontsize=14, fontweight='bold')
        self.plt.xlabel(column, fontsize=12)
        self.plt.ylabel('Count', fontsize=12)
        self.plt.xticks(range(len(value_counts)), value_counts.index, rotation=45, ha='right')
        
        # Add value labels
        for bar, value in zip(bars, value_counts.values):
            self.plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01*max(value_counts.values),
                    str(value), ha='center', va='bottom')
        
        self.plt.grid(True, alpha=0.3, axis='y')
        self.plt.tight_layout()
        self.plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        self.plt.close()
        
        return {
            'type': 'bar',
            'title': title,
            'url': f'/visuals/{os.path.basename(chart_path)}',
            'filename': os.path.basename(chart_path),
            'variables': [column]
        }
    
    def _create_heatmap(self, df, title: str, filename: str, index: int) -> Dict[str, Any]:
        """Create correlation heatmap"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_cols) < 2:
            return None
            
        safe_name = self._sanitize_filename(f"{index}_{title}")
        chart_path = os.path.join(self.output_dir, f"{safe_name}_{filename}.png")
        
        self.plt.figure(figsize=(12, 10))
        correlation_matrix = df[numeric_cols].corr()
        
        mask = self.np.triu(self.np.ones_like(correlation_matrix, dtype=bool))
        self.sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='coolwarm', 
                   center=0, square=True, fmt='.2f', cbar_kws={"shrink": .8})
        self.plt.title(title, fontsize=14, fontweight='bold')
        self.plt.tight_layout()
        self.plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        self.plt.close()
        
        return {
            'type': 'heatmap',
            'title': title,
            'url': f'/visuals/{os.path.basename(chart_path)}',
            'filename': os.path.basename(chart_path),
            'variables': numeric_cols
        }
    
    def _create_boxplot(self, df, x_col: str, y_col: str, title: str, filename: str, index: int) -> Dict[str, Any]:
        """Create boxplot"""
        if y_col not in df.columns:
            return None
            
        safe_name = self._sanitize_filename(f"{index}_{title}")
        chart_path = os.path.join(self.output_dir, f"{safe_name}_{filename}.png")
        
        self.plt.figure(figsize=(12, 8))
        
        if x_col and x_col in df.columns:
            df.boxplot(column=y_col, by=x_col, figsize=(12, 8))
            self.plt.xlabel(x_col, fontsize=12)
        else:
            df.boxplot(column=y_col, figsize=(12, 8))
        
        self.plt.title(title, fontsize=14, fontweight='bold')
        self.plt.suptitle('')
        self.plt.ylabel(y_col, fontsize=12)
        self.plt.grid(True, alpha=0.3)
        self.plt.tight_layout()
        self.plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        self.plt.close()
        
        return {
            'type': 'boxplot',
            'title': title,
            'url': f'/visuals/{os.path.basename(chart_path)}',
            'filename': os.path.basename(chart_path),
            'variables': [x_col, y_col] if x_col else [y_col]
        }
