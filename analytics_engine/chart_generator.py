"""
Dynamic Chart Generator - Creates visualizations based on data types and structure
Optimized for fast startup with lazy imports
"""
from typing import Dict, List, Any, Tuple
import os


class ChartGenerator:
    """
    Dynamically generates appropriate visualizations based on data types and structure
    """
    
    def __init__(self, output_dir: str = "visuals"):
        self.output_dir = output_dir
        self.ensure_output_dir()
        self._matplotlib_initialized = False
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
            matplotlib.use('Agg')  # Set backend to avoid GUI issues
            
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            plt.style.use('default')
            sns.set_palette("husl")
            
            # Store references
            self.pd = pd
            self.np = np
            self.plt = plt
            self.sns = sns
            
            self._imports_loaded = True
    
    def generate_charts(self, df, schema: Dict[str, Any], filename: str) -> List[Dict[str, Any]]:
        """
        Generate all appropriate charts for the dataset
        """
        # Lazy import heavy libraries
        self._load_imports()
        
        charts = []
        
        # 1. Numeric variable visualizations
        charts.extend(self._generate_numeric_charts(df, schema, filename))
        
        # 2. Categorical variable visualizations
        charts.extend(self._generate_categorical_charts(df, schema, filename))
        
        # 3. Relationship visualizations
        charts.extend(self._generate_relationship_charts(df, schema, filename))
        
        # 4. Distribution visualizations
        charts.extend(self._generate_distribution_charts(df, schema, filename))
        
        # 5. Correlation visualizations
        charts.extend(self._generate_correlation_charts(df, schema, filename))
        
        print(f"📊 Generated {len(charts)} dynamic charts")
        return charts
    
    def _generate_numeric_charts(self, df, schema: Dict[str, Any], filename: str) -> List[Dict[str, Any]]:
        """Generate charts for numeric variables"""
        charts = []
        numeric_cols = schema['numeric_columns']
        
        if not numeric_cols:
            return charts
        
        # Histograms for each numeric variable
        for col in numeric_cols[:6]:  # Limit to first 6 to avoid too many charts
            chart_path = f"{self.output_dir}/histogram_{col}_{filename}.png"
            
            self.plt.figure(figsize=(10, 6))
            self.plt.hist(df[col].dropna(), bins=30, alpha=0.7, color='skyblue', edgecolor='black')
            self.plt.title(f'Distribution of {col}', fontsize=14, fontweight='bold')
            self.plt.xlabel(col, fontsize=12)
            self.plt.ylabel('Frequency', fontsize=12)
            self.plt.grid(True, alpha=0.3)
            self.plt.tight_layout()
            self.plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            self.plt.close()
            
            charts.append({
                'type': 'histogram',
                'title': f'Distribution of {col}',
                'url': f'/visuals/histogram_{col}_{filename}.png',
                'filename': f'histogram_{col}_{filename}.png',
                'variables': [col],
                'description': f'Frequency distribution of {col} values'
            })
        
        # Box plots for numeric variables
        if len(numeric_cols) > 1:
            chart_path = f"{self.output_dir}/boxplot_comparison_{filename}.png"
            
            self.plt.figure(figsize=(12, 8))
            # Normalize data for comparison if scales are very different
            df_normalized = df[numeric_cols].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
            df_normalized.boxplot(figsize=(12, 8))
            self.plt.title('Box Plot Comparison (Normalized)', fontsize=14, fontweight='bold')
            self.plt.xticks(rotation=45)
            self.plt.ylabel('Normalized Values', fontsize=12)
            self.plt.grid(True, alpha=0.3)
            self.plt.tight_layout()
            self.plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            self.plt.close()
            
            charts.append({
                'type': 'boxplot',
                'title': 'Box Plot Comparison',
                'url': f'/visuals/boxplot_comparison_{filename}.png',
                'filename': f'boxplot_comparison_{filename}.png',
                'variables': numeric_cols,
                'description': 'Comparison of distributions and outliers across numeric variables'
            })
        
        return charts
    
    def _generate_categorical_charts(self, df, schema: Dict[str, Any], filename: str) -> List[Dict[str, Any]]:
        """Generate charts for categorical variables"""
        charts = []
        categorical_cols = schema['categorical_columns']
        
        for col in categorical_cols[:4]:  # Limit to first 4
            value_counts = df[col].value_counts().head(10)  # Top 10 categories
            
            if len(value_counts) > 1:
                # Bar chart
                chart_path = f"{self.output_dir}/bar_{col}_{filename}.png"
                
                self.plt.figure(figsize=(12, 6))
                bars = self.plt.bar(range(len(value_counts)), value_counts.values, 
                              color=self.plt.cm.Set3(self.np.linspace(0, 1, len(value_counts))))
                self.plt.title(f'Distribution of {col}', fontsize=14, fontweight='bold')
                self.plt.xlabel(col, fontsize=12)
                self.plt.ylabel('Count', fontsize=12)
                self.plt.xticks(range(len(value_counts)), value_counts.index, rotation=45, ha='right')
                
                # Add value labels on bars
                for bar, value in zip(bars, value_counts.values):
                    self.plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01*max(value_counts.values),
                            str(value), ha='center', va='bottom')
                
                self.plt.grid(True, alpha=0.3, axis='y')
                self.plt.tight_layout()
                self.plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                self.plt.close()
                
                charts.append({
                    'type': 'bar',
                    'title': f'Distribution of {col}',
                    'url': f'/visuals/bar_{col}_{filename}.png',
                    'filename': f'bar_{col}_{filename}.png',
                    'variables': [col],
                    'description': f'Frequency distribution of {col} categories'
                })
                
                # Pie chart if reasonable number of categories
                if 2 <= len(value_counts) <= 8:
                    chart_path = f"{self.output_dir}/pie_{col}_{filename}.png"
                    
                    self.plt.figure(figsize=(10, 8))
                    colors = self.plt.cm.Set3(self.np.linspace(0, 1, len(value_counts)))
                    wedges, texts, autotexts = self.plt.pie(value_counts.values, labels=value_counts.index, 
                                                      autopct='%1.1f%%', colors=colors, startangle=90)
                    self.plt.title(f'Proportion of {col}', fontsize=14, fontweight='bold')
                    
                    # Improve text readability
                    for autotext in autotexts:
                        autotext.set_color('white')
                        autotext.set_fontweight('bold')
                    
                    self.plt.axis('equal')
                    self.plt.tight_layout()
                    self.plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                    self.plt.close()
                    
                    charts.append({
                        'type': 'pie',
                        'title': f'Proportion of {col}',
                        'url': f'/visuals/pie_{col}_{filename}.png',
                        'filename': f'pie_{col}_{filename}.png',
                        'variables': [col],
                        'description': f'Proportional distribution of {col} categories'
                    })
        
        return charts
    
    def _generate_relationship_charts(self, df, schema: Dict[str, Any], filename: str) -> List[Dict[str, Any]]:
        """Generate charts showing relationships between variables"""
        charts = []
        numeric_cols = schema['numeric_columns']
        categorical_cols = schema['categorical_columns']
        
        # Scatter plots for numeric vs numeric
        if len(numeric_cols) >= 2:
            for i, col1 in enumerate(numeric_cols[:3]):  # Limit combinations
                for col2 in numeric_cols[i+1:4]:
                    chart_path = f"{self.output_dir}/scatter_{col1}_vs_{col2}_{filename}.png"
                    
                    self.plt.figure(figsize=(10, 8))
                    self.plt.scatter(df[col1], df[col2], alpha=0.6, s=50)
                    self.plt.title(f'{col1} vs {col2}', fontsize=14, fontweight='bold')
                    self.plt.xlabel(col1, fontsize=12)
                    self.plt.ylabel(col2, fontsize=12)
                    self.plt.grid(True, alpha=0.3)
                    
                    # Add trend line
                    z = self.np.polyfit(df[col1].dropna(), df[col2].dropna(), 1)
                    p = self.np.poly1d(z)
                    self.plt.plot(df[col1], p(df[col1]), "r--", alpha=0.8, linewidth=2)
                    
                    self.plt.tight_layout()
                    self.plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                    self.plt.close()
                    
                    charts.append({
                        'type': 'scatter',
                        'title': f'{col1} vs {col2}',
                        'url': f'/visuals/scatter_{col1}_vs_{col2}_{filename}.png',
                        'filename': f'scatter_{col1}_vs_{col2}_{filename}.png',
                        'variables': [col1, col2],
                        'description': f'Relationship between {col1} and {col2}'
                    })
        
        # Box plots for categorical vs numeric
        if categorical_cols and numeric_cols:
            for cat_col in categorical_cols[:2]:
                for num_col in numeric_cols[:2]:
                    if df[cat_col].nunique() <= 10:  # Reasonable number of categories
                        chart_path = f"{self.output_dir}/boxplot_{cat_col}_vs_{num_col}_{filename}.png"
                        
                        self.plt.figure(figsize=(12, 8))
                        df.boxplot(column=num_col, by=cat_col, figsize=(12, 8))
                        self.plt.title(f'{num_col} by {cat_col}', fontsize=14, fontweight='bold')
                        self.plt.suptitle('')  # Remove default title
                        self.plt.xticks(rotation=45)
                        self.plt.ylabel(num_col, fontsize=12)
                        self.plt.xlabel(cat_col, fontsize=12)
                        self.plt.grid(True, alpha=0.3)
                        self.plt.tight_layout()
                        self.plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                        self.plt.close()
                        
                        charts.append({
                            'type': 'boxplot_grouped',
                            'title': f'{num_col} by {cat_col}',
                            'url': f'/visuals/boxplot_{cat_col}_vs_{num_col}_{filename}.png',
                            'filename': f'boxplot_{cat_col}_vs_{num_col}_{filename}.png',
                            'variables': [cat_col, num_col],
                            'description': f'Distribution of {num_col} across {cat_col} categories'
                        })
        
        return charts
    
    def _generate_distribution_charts(self, df, schema: Dict[str, Any], filename: str) -> List[Dict[str, Any]]:
        """Generate distribution comparison charts"""
        charts = []
        numeric_cols = schema['numeric_columns']
        
        if len(numeric_cols) > 1:
            # Violin plots for distribution comparison
            chart_path = f"{self.output_dir}/violin_distributions_{filename}.png"
            
            self.plt.figure(figsize=(14, 8))
            # Normalize data for comparison
            df_normalized = df[numeric_cols].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
            
            # Melt data for violin plot
            df_melted = df_normalized.melt(var_name='Variable', value_name='Normalized_Value')
            
            self.sns.violinplot(data=df_melted, x='Variable', y='Normalized_Value')
            self.plt.title('Distribution Comparison (Violin Plot)', fontsize=14, fontweight='bold')
            self.plt.xticks(rotation=45)
            self.plt.ylabel('Normalized Values', fontsize=12)
            self.plt.grid(True, alpha=0.3, axis='y')
            self.plt.tight_layout()
            self.plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            self.plt.close()
            
            charts.append({
                'type': 'violin',
                'title': 'Distribution Comparison',
                'url': f'/visuals/violin_distributions_{filename}.png',
                'filename': f'violin_distributions_{filename}.png',
                'variables': numeric_cols,
                'description': 'Comparison of value distributions across numeric variables'
            })
        
        return charts
    
    def _generate_correlation_charts(self, df, schema: Dict[str, Any], filename: str) -> List[Dict[str, Any]]:
        """Generate correlation visualizations"""
        charts = []
        numeric_cols = schema['numeric_columns']
        
        if len(numeric_cols) > 1:
            # Correlation heatmap
            chart_path = f"{self.output_dir}/correlation_heatmap_{filename}.png"
            
            self.plt.figure(figsize=(12, 10))
            correlation_matrix = df[numeric_cols].corr()
            
            mask = self.np.triu(self.np.ones_like(correlation_matrix, dtype=bool))
            self.sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='coolwarm', 
                       center=0, square=True, fmt='.2f', cbar_kws={"shrink": .8})
            self.plt.title('Correlation Matrix', fontsize=14, fontweight='bold')
            self.plt.tight_layout()
            self.plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            self.plt.close()
            
            charts.append({
                'type': 'heatmap',
                'title': 'Correlation Matrix',
                'url': f'/visuals/correlation_heatmap_{filename}.png',
                'filename': f'correlation_heatmap_{filename}.png',
                'variables': numeric_cols,
                'description': 'Correlation coefficients between numeric variables'
            })
        
        return charts