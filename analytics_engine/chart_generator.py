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

    def generate_weather_charts(self, df, filename_prefix: str) -> List[Dict[str, str]]:
        """Generate comprehensive weather charts organized by categories"""
        # Lazy import heavy libraries
        self._load_imports()
        
        charts = []
        
        try:
            # ATMOSPHERIC CHARTS
            # Temperature and humidity chart
            if 'temperature_2m' in df.columns:
                chart_path = self._create_atmospheric_chart(
                    df, f"{filename_prefix}_atmospheric.png"
                )
                if chart_path:
                    charts.append({
                        'title': 'Atmospheric Conditions (Temperature, Humidity, Cloud Cover)',
                        'type': 'multi_line',
                        'category': 'atmospheric',
                        'url': f'/visuals/{os.path.basename(chart_path)}'
                    })
            
            # Wind analysis chart
            wind_cols = [col for col in df.columns if 'wind_speed' in col]
            if wind_cols:
                chart_path = self._create_wind_analysis_chart(
                    df, f"{filename_prefix}_wind_analysis.png"
                )
                if chart_path:
                    charts.append({
                        'title': 'Wind Speed & Direction Analysis',
                        'type': 'wind_analysis',
                        'category': 'atmospheric',
                        'url': f'/visuals/{os.path.basename(chart_path)}'
                    })
            
            # HYDROLOGICAL CHARTS
            # Precipitation and pressure chart
            hydro_cols = ['rain', 'precipitation', 'pressure_msl']
            available_hydro = [col for col in hydro_cols if col in df.columns]
            if available_hydro:
                chart_path = self._create_hydrological_chart(
                    df, available_hydro, f"{filename_prefix}_hydrological.png"
                )
                if chart_path:
                    charts.append({
                        'title': 'Hydrological Parameters (Rainfall, Pressure)',
                        'type': 'multi_line',
                        'category': 'hydrological',
                        'url': f'/visuals/{os.path.basename(chart_path)}'
                    })
            
            # OCEANIC CHARTS
            oceanic_cols = ['wave_height', 'sea_surface_temperature', 'ocean_current_velocity']
            available_oceanic = [col for col in oceanic_cols if col in df.columns]
            if available_oceanic:
                chart_path = self._create_oceanic_chart(
                    df, available_oceanic, f"{filename_prefix}_oceanic.png"
                )
                if chart_path:
                    charts.append({
                        'title': 'Oceanic & Coastal Conditions',
                        'type': 'multi_line',
                        'category': 'oceanic',
                        'url': f'/visuals/{os.path.basename(chart_path)}'
                    })
            
            # ENVIRONMENTAL CHARTS
            env_cols = ['pm2_5', 'pm10', 'ozone', 'carbon_monoxide']
            available_env = [col for col in env_cols if col in df.columns]
            if available_env:
                chart_path = self._create_environmental_chart(
                    df, available_env, f"{filename_prefix}_environmental.png"
                )
                if chart_path:
                    charts.append({
                        'title': 'Air Quality & Environmental Parameters',
                        'type': 'multi_line',
                        'category': 'environmental',
                        'url': f'/visuals/{os.path.basename(chart_path)}'
                    })
            
            # COMPREHENSIVE OVERVIEW CHART
            # Create a summary chart with key parameters from all categories
            key_params = []
            if 'temperature_2m' in df.columns:
                key_params.append('temperature_2m')
            if 'pressure_msl' in df.columns:
                key_params.append('pressure_msl')
            if 'wind_speed_10m' in df.columns:
                key_params.append('wind_speed_10m')
            if 'relative_humidity_2m' in df.columns:
                key_params.append('relative_humidity_2m')
            
            if len(key_params) >= 2:
                chart_path = self._create_comprehensive_overview(
                    df, key_params, f"{filename_prefix}_overview.png"
                )
                if chart_path:
                    charts.append({
                        'title': 'Comprehensive Weather Overview',
                        'type': 'overview',
                        'category': 'overview',
                        'url': f'/visuals/{os.path.basename(chart_path)}'
                    })
            
        except Exception as e:
            print(f"❌ Error generating comprehensive weather charts: {str(e)}")
        
        return charts
    
    def _create_weather_line_chart(self, df, column: str, title: str, filename: str) -> str:
        """Create a line chart for weather parameter"""
        try:
            self.plt.figure(figsize=(12, 6))
            self.plt.plot(df.index, df[column], linewidth=2, marker='o', markersize=4)
            self.plt.title(title, fontsize=14, fontweight='bold')
            self.plt.xlabel('Time')
            self.plt.ylabel(title.split('(')[0].strip())
            self.plt.grid(True, alpha=0.3)
            self.plt.xticks(rotation=45)
            self.plt.tight_layout()
            
            filepath = os.path.join(self.output_dir, filename)
            self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
            self.plt.close()
            
            return filepath
        except Exception as e:
            print(f"❌ Error creating weather line chart: {str(e)}")
            return None
    
    def _create_multi_weather_chart(self, df, parameters: List[str], filename: str) -> str:
        """Create multi-parameter weather chart with subplots"""
        try:
            fig, axes = self.plt.subplots(len(parameters), 1, figsize=(12, 4 * len(parameters)))
            if len(parameters) == 1:
                axes = [axes]
            
            param_labels = {
                'temperature_2m': 'Temperature (°C)',
                'pressure_msl': 'Pressure (hPa)',
                'wind_speed_80m': 'Wind Speed (km/h)',
                'rain': 'Rainfall (mm)'
            }
            
            for i, param in enumerate(parameters):
                axes[i].plot(df.index, df[param], linewidth=2, marker='o', markersize=3)
                axes[i].set_title(param_labels.get(param, param), fontweight='bold')
                axes[i].grid(True, alpha=0.3)
                axes[i].tick_params(axis='x', rotation=45)
            
            self.plt.tight_layout()
            
            filepath = os.path.join(self.output_dir, filename)
            self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
            self.plt.close()
            
            return filepath
        except Exception as e:
            print(f"❌ Error creating multi-weather chart: {str(e)}")
            return None
    
    def _create_weather_bar_chart(self, df, column: str, title: str, filename: str) -> str:
        """Create bar chart for weather parameter"""
        try:
            self.plt.figure(figsize=(12, 6))
            self.plt.bar(range(len(df)), df[column], alpha=0.7)
            self.plt.title(title, fontsize=14, fontweight='bold')
            self.plt.xlabel('Time')
            self.plt.ylabel(title.split('(')[0].strip())
            self.plt.xticks(range(len(df)), [t.strftime('%H:%M') for t in df.index], rotation=45)
            self.plt.grid(True, alpha=0.3, axis='y')
            self.plt.tight_layout()
            
            filepath = os.path.join(self.output_dir, filename)
            self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
            self.plt.close()
            
            return filepath
        except Exception as e:
            print(f"❌ Error creating weather bar chart: {str(e)}")
            return None
    
    def _create_wind_chart(self, df, filename: str) -> str:
        """Create wind speed and direction chart"""
        try:
            fig, (ax1, ax2) = self.plt.subplots(2, 1, figsize=(12, 8))
            
            # Wind speed over time
            ax1.plot(df.index, df['wind_speed_80m'], linewidth=2, marker='o', markersize=4, color='blue')
            ax1.set_title('Wind Speed Over Time', fontweight='bold')
            ax1.set_ylabel('Wind Speed (km/h)')
            ax1.grid(True, alpha=0.3)
            ax1.tick_params(axis='x', rotation=45)
            
            # Wind direction over time
            ax2.plot(df.index, df['wind_direction_80m'], linewidth=2, marker='s', markersize=4, color='red')
            ax2.set_title('Wind Direction Over Time', fontweight='bold')
            ax2.set_ylabel('Wind Direction (°)')
            ax2.set_xlabel('Time')
            ax2.grid(True, alpha=0.3)
            ax2.tick_params(axis='x', rotation=45)
            ax2.set_ylim(0, 360)
            
            self.plt.tight_layout()
            
            filepath = os.path.join(self.output_dir, filename)
            self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
            self.plt.close()
            
            return filepath
        except Exception as e:
            print(f"❌ Error creating wind chart: {str(e)}")
            return None
    
    def _create_atmospheric_chart(self, df, filename: str) -> str:
        """Create atmospheric conditions chart"""
        try:
            fig, axes = self.plt.subplots(3, 1, figsize=(14, 12))
            
            # Temperature
            if 'temperature_2m' in df.columns:
                axes[0].plot(df.index, df['temperature_2m'], linewidth=2, marker='o', markersize=4, color='red', label='Temperature')
                if 'apparent_temperature' in df.columns:
                    axes[0].plot(df.index, df['apparent_temperature'], linewidth=2, linestyle='--', color='orange', label='Feels Like')
                axes[0].set_title('Temperature (°C)', fontweight='bold')
                axes[0].set_ylabel('Temperature (°C)')
                axes[0].grid(True, alpha=0.3)
                axes[0].legend()
            
            # Humidity and Cloud Cover
            if 'relative_humidity_2m' in df.columns:
                axes[1].plot(df.index, df['relative_humidity_2m'], linewidth=2, marker='s', markersize=4, color='blue', label='Humidity')
            if 'cloud_cover' in df.columns:
                axes[1].plot(df.index, df['cloud_cover'], linewidth=2, marker='^', markersize=4, color='gray', label='Cloud Cover')
            axes[1].set_title('Humidity & Cloud Cover (%)', fontweight='bold')
            axes[1].set_ylabel('Percentage (%)')
            axes[1].grid(True, alpha=0.3)
            axes[1].legend()
            
            # UV Index and Visibility
            if 'uv_index' in df.columns:
                axes[2].plot(df.index, df['uv_index'], linewidth=2, marker='D', markersize=4, color='purple', label='UV Index')
            if 'visibility' in df.columns:
                # Convert visibility to km for better readability
                visibility_km = df['visibility'] / 1000
                ax2_twin = axes[2].twinx()
                ax2_twin.plot(df.index, visibility_km, linewidth=2, marker='v', markersize=4, color='green', label='Visibility (km)')
                ax2_twin.set_ylabel('Visibility (km)')
                ax2_twin.legend(loc='upper right')
            
            axes[2].set_title('UV Index & Visibility', fontweight='bold')
            axes[2].set_ylabel('UV Index')
            axes[2].set_xlabel('Time')
            axes[2].grid(True, alpha=0.3)
            axes[2].legend(loc='upper left')
            
            for ax in axes:
                ax.tick_params(axis='x', rotation=45)
            
            self.plt.tight_layout()
            
            filepath = os.path.join(self.output_dir, filename)
            self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
            self.plt.close()
            
            return filepath
        except Exception as e:
            print(f"❌ Error creating atmospheric chart: {str(e)}")
            return None
    
    def _create_wind_analysis_chart(self, df, filename: str) -> str:
        """Create comprehensive wind analysis chart"""
        try:
            fig, axes = self.plt.subplots(2, 2, figsize=(16, 10))
            
            # Wind speed comparison (10m vs 80m)
            wind_cols = [col for col in df.columns if 'wind_speed' in col]
            for i, col in enumerate(wind_cols[:2]):
                height = '10m' if '10m' in col else '80m'
                color = 'blue' if '10m' in col else 'red'
                axes[0, 0].plot(df.index, df[col], linewidth=2, marker='o', markersize=3, 
                               color=color, label=f'Wind Speed {height}')
            
            axes[0, 0].set_title('Wind Speed Comparison', fontweight='bold')
            axes[0, 0].set_ylabel('Wind Speed (km/h)')
            axes[0, 0].grid(True, alpha=0.3)
            axes[0, 0].legend()
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # Wind direction
            dir_cols = [col for col in df.columns if 'wind_direction' in col]
            if dir_cols:
                axes[0, 1].plot(df.index, df[dir_cols[0]], linewidth=2, marker='s', markersize=3, color='green')
                axes[0, 1].set_title('Wind Direction', fontweight='bold')
                axes[0, 1].set_ylabel('Direction (°)')
                axes[0, 1].set_ylim(0, 360)
                axes[0, 1].grid(True, alpha=0.3)
                axes[0, 1].tick_params(axis='x', rotation=45)
            
            # Wind gusts if available
            if 'wind_gusts_10m' in df.columns:
                axes[1, 0].plot(df.index, df['wind_gusts_10m'], linewidth=2, marker='^', markersize=3, color='orange', label='Wind Gusts')
                if 'wind_speed_10m' in df.columns:
                    axes[1, 0].plot(df.index, df['wind_speed_10m'], linewidth=2, marker='o', markersize=3, color='blue', label='Sustained Wind')
                axes[1, 0].set_title('Wind Gusts vs Sustained Wind', fontweight='bold')
                axes[1, 0].set_ylabel('Wind Speed (km/h)')
                axes[1, 0].grid(True, alpha=0.3)
                axes[1, 0].legend()
                axes[1, 0].tick_params(axis='x', rotation=45)
            
            # Wind rose (simplified)
            if dir_cols and wind_cols:
                # Create a simple wind distribution
                wind_dir = df[dir_cols[0]].dropna()
                wind_speed = df[wind_cols[0]].dropna()
                
                # Bin wind directions
                dir_bins = np.arange(0, 361, 45)
                dir_labels = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
                
                binned_speeds = []
                for i in range(len(dir_bins)-1):
                    mask = (wind_dir >= dir_bins[i]) & (wind_dir < dir_bins[i+1])
                    avg_speed = wind_speed[mask].mean() if mask.any() else 0
                    binned_speeds.append(avg_speed)
                
                axes[1, 1].bar(dir_labels, binned_speeds, color='skyblue', alpha=0.7)
                axes[1, 1].set_title('Wind Speed by Direction', fontweight='bold')
                axes[1, 1].set_ylabel('Average Wind Speed (km/h)')
                axes[1, 1].grid(True, alpha=0.3, axis='y')
            
            self.plt.tight_layout()
            
            filepath = os.path.join(self.output_dir, filename)
            self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
            self.plt.close()
            
            return filepath
        except Exception as e:
            print(f"❌ Error creating wind analysis chart: {str(e)}")
            return None
    
    def _create_hydrological_chart(self, df, parameters: List[str], filename: str) -> str:
        """Create hydrological parameters chart"""
        try:
            fig, axes = self.plt.subplots(len(parameters), 1, figsize=(14, 4 * len(parameters)))
            if len(parameters) == 1:
                axes = [axes]
            
            param_info = {
                'rain': {'label': 'Rainfall (mm/h)', 'color': 'blue', 'type': 'bar'},
                'precipitation': {'label': 'Total Precipitation (mm/h)', 'color': 'navy', 'type': 'bar'},
                'pressure_msl': {'label': 'Sea Level Pressure (hPa)', 'color': 'red', 'type': 'line'},
                'surface_pressure': {'label': 'Surface Pressure (hPa)', 'color': 'darkred', 'type': 'line'},
                'snowfall': {'label': 'Snowfall (cm/h)', 'color': 'lightblue', 'type': 'bar'}
            }
            
            for i, param in enumerate(parameters):
                info = param_info.get(param, {'label': param, 'color': 'black', 'type': 'line'})
                
                if info['type'] == 'bar':
                    axes[i].bar(range(len(df)), df[param], alpha=0.7, color=info['color'])
                    axes[i].set_xticks(range(len(df)))
                    axes[i].set_xticklabels([t.strftime('%H:%M') for t in df.index], rotation=45)
                else:
                    axes[i].plot(df.index, df[param], linewidth=2, marker='o', markersize=4, color=info['color'])
                    axes[i].tick_params(axis='x', rotation=45)
                
                axes[i].set_title(info['label'], fontweight='bold')
                axes[i].set_ylabel(info['label'].split('(')[1].replace(')', '') if '(' in info['label'] else '')
                axes[i].grid(True, alpha=0.3)
            
            axes[-1].set_xlabel('Time')
            self.plt.tight_layout()
            
            filepath = os.path.join(self.output_dir, filename)
            self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
            self.plt.close()
            
            return filepath
        except Exception as e:
            print(f"❌ Error creating hydrological chart: {str(e)}")
            return None
    
    def _create_oceanic_chart(self, df, parameters: List[str], filename: str) -> str:
        """Create oceanic and coastal conditions chart"""
        try:
            fig, axes = self.plt.subplots(len(parameters), 1, figsize=(14, 4 * len(parameters)))
            if len(parameters) == 1:
                axes = [axes]
            
            param_info = {
                'wave_height': {'label': 'Wave Height (m)', 'color': 'blue'},
                'swell_wave_height': {'label': 'Swell Wave Height (m)', 'color': 'navy'},
                'sea_surface_temperature': {'label': 'Sea Surface Temperature (°C)', 'color': 'red'},
                'ocean_current_velocity': {'label': 'Ocean Current Velocity (m/s)', 'color': 'green'},
                'wave_period': {'label': 'Wave Period (s)', 'color': 'purple'}
            }
            
            for i, param in enumerate(parameters):
                info = param_info.get(param, {'label': param, 'color': 'black'})
                
                axes[i].plot(df.index, df[param], linewidth=2, marker='o', markersize=4, color=info['color'])
                axes[i].set_title(info['label'], fontweight='bold')
                axes[i].set_ylabel(info['label'].split('(')[1].replace(')', '') if '(' in info['label'] else '')
                axes[i].grid(True, alpha=0.3)
                axes[i].tick_params(axis='x', rotation=45)
            
            axes[-1].set_xlabel('Time')
            self.plt.tight_layout()
            
            filepath = os.path.join(self.output_dir, filename)
            self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
            self.plt.close()
            
            return filepath
        except Exception as e:
            print(f"❌ Error creating oceanic chart: {str(e)}")
            return None
    
    def _create_environmental_chart(self, df, parameters: List[str], filename: str) -> str:
        """Create air quality and environmental parameters chart"""
        try:
            fig, axes = self.plt.subplots(2, 1, figsize=(14, 10))
            
            # Particulate matter (PM2.5, PM10)
            pm_params = [p for p in parameters if p.startswith('pm')]
            if pm_params:
                for param in pm_params:
                    color = 'red' if '2_5' in param else 'orange'
                    label = 'PM2.5' if '2_5' in param else 'PM10'
                    axes[0].plot(df.index, df[param], linewidth=2, marker='o', markersize=4, 
                                color=color, label=f'{label} (μg/m³)')
                
                axes[0].set_title('Particulate Matter Concentration', fontweight='bold')
                axes[0].set_ylabel('Concentration (μg/m³)')
                axes[0].grid(True, alpha=0.3)
                axes[0].legend()
                axes[0].tick_params(axis='x', rotation=45)
            
            # Gaseous pollutants
            gas_params = [p for p in parameters if not p.startswith('pm')]
            if gas_params:
                colors = ['blue', 'green', 'purple', 'brown', 'pink']
                for i, param in enumerate(gas_params):
                    color = colors[i % len(colors)]
                    label = param.replace('_', ' ').title()
                    axes[1].plot(df.index, df[param], linewidth=2, marker='s', markersize=4, 
                                color=color, label=f'{label} (ppb)')
                
                axes[1].set_title('Gaseous Pollutants', fontweight='bold')
                axes[1].set_ylabel('Concentration (ppb)')
                axes[1].set_xlabel('Time')
                axes[1].grid(True, alpha=0.3)
                axes[1].legend()
                axes[1].tick_params(axis='x', rotation=45)
            
            self.plt.tight_layout()
            
            filepath = os.path.join(self.output_dir, filename)
            self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
            self.plt.close()
            
            return filepath
        except Exception as e:
            print(f"❌ Error creating environmental chart: {str(e)}")
            return None
    
    def _create_comprehensive_overview(self, df, parameters: List[str], filename: str) -> str:
        """Create comprehensive overview chart with normalized parameters"""
        try:
            fig, ax = self.plt.subplots(1, 1, figsize=(16, 8))
            
            # Normalize all parameters to 0-1 scale for comparison
            colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
            
            for i, param in enumerate(parameters):
                if param in df.columns and not df[param].isna().all():
                    data = df[param].dropna()
                    if len(data) > 0:
                        # Normalize to 0-1 scale
                        normalized = (data - data.min()) / (data.max() - data.min()) if data.max() != data.min() else data * 0
                        
                        # Create label with units
                        labels = {
                            'temperature_2m': 'Temperature (°C)',
                            'pressure_msl': 'Pressure (hPa)',
                            'wind_speed_10m': 'Wind Speed (km/h)',
                            'relative_humidity_2m': 'Humidity (%)',
                            'cloud_cover': 'Cloud Cover (%)'
                        }
                        
                        label = labels.get(param, param.replace('_', ' ').title())
                        color = colors[i % len(colors)]
                        
                        ax.plot(data.index, normalized, linewidth=2, marker='o', markersize=4, 
                               color=color, label=label, alpha=0.8)
            
            ax.set_title('Comprehensive Weather Overview (Normalized)', fontweight='bold', fontsize=16)
            ax.set_ylabel('Normalized Values (0-1 scale)', fontsize=12)
            ax.set_xlabel('Time', fontsize=12)
            ax.grid(True, alpha=0.3)
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.tick_params(axis='x', rotation=45)
            
            # Add note about normalization
            ax.text(0.02, 0.98, 'Note: All parameters normalized to 0-1 scale for comparison', 
                   transform=ax.transAxes, fontsize=10, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            self.plt.tight_layout()
            
            filepath = os.path.join(self.output_dir, filename)
            self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
            self.plt.close()
            
            return filepath
        except Exception as e:
            print(f"❌ Error creating comprehensive overview chart: {str(e)}")
            return None    

    def _generate_simple_weather_charts(self, df, filename_prefix: str) -> List[Dict[str, str]]:
        """Generate simple weather charts as fallback"""
        # Lazy import heavy libraries
        self._load_imports()
        
        charts = []
        
        try:
            # Temperature trend chart
            if 'temperature_2m' in df.columns:
                chart_path = self._create_weather_line_chart(
                    df, 'temperature_2m', 'Temperature Trend (°C)', 
                    f"{filename_prefix}_temperature.png"
                )
                if chart_path:
                    charts.append({
                        'title': 'Temperature Trend (Past 6 Hours)',
                        'type': 'line',
                        'category': 'atmospheric',
                        'url': f'/visuals/{os.path.basename(chart_path)}'
                    })
            
            # Multi-parameter weather chart
            weather_params = ['temperature_2m', 'pressure_msl', 'wind_speed_10m']
            available_params = [p for p in weather_params if p in df.columns]
            
            if len(available_params) >= 2:
                chart_path = self._create_multi_weather_chart(
                    df, available_params, f"{filename_prefix}_multi.png"
                )
                if chart_path:
                    charts.append({
                        'title': 'Weather Parameters Overview',
                        'type': 'multi_line',
                        'category': 'overview',
                        'url': f'/visuals/{os.path.basename(chart_path)}'
                    })
            
            # Rain chart if available
            if 'rain' in df.columns and df['rain'].sum() > 0:
                chart_path = self._create_weather_bar_chart(
                    df, 'rain', 'Rainfall (mm)', f"{filename_prefix}_rain.png"
                )
                if chart_path:
                    charts.append({
                        'title': 'Hourly Rainfall',
                        'type': 'bar',
                        'category': 'hydrological',
                        'url': f'/visuals/{os.path.basename(chart_path)}'
                    })
            
            # Wind direction chart if available
            if 'wind_direction_10m' in df.columns and 'wind_speed_10m' in df.columns:
                chart_path = self._create_simple_wind_chart(
                    df, f"{filename_prefix}_wind.png"
                )
                if chart_path:
                    charts.append({
                        'title': 'Wind Speed & Direction',
                        'type': 'wind',
                        'category': 'atmospheric',
                        'url': f'/visuals/{os.path.basename(chart_path)}'
                    })
            
        except Exception as e:
            print(f"❌ Error generating simple weather charts: {str(e)}")
        
        return charts
    
    def _create_simple_wind_chart(self, df, filename: str) -> str:
        """Create simple wind speed and direction chart"""
        try:
            fig, (ax1, ax2) = self.plt.subplots(2, 1, figsize=(12, 8))
            
            # Wind speed over time
            if 'wind_speed_10m' in df.columns:
                ax1.plot(df.index, df['wind_speed_10m'], linewidth=2, marker='o', markersize=4, color='blue')
                ax1.set_title('Wind Speed Over Time', fontweight='bold')
                ax1.set_ylabel('Wind Speed (km/h)')
                ax1.grid(True, alpha=0.3)
                ax1.tick_params(axis='x', rotation=45)
            
            # Wind direction over time
            if 'wind_direction_10m' in df.columns:
                ax2.plot(df.index, df['wind_direction_10m'], linewidth=2, marker='s', markersize=4, color='red')
                ax2.set_title('Wind Direction Over Time', fontweight='bold')
                ax2.set_ylabel('Wind Direction (°)')
                ax2.set_xlabel('Time')
                ax2.grid(True, alpha=0.3)
                ax2.tick_params(axis='x', rotation=45)
                ax2.set_ylim(0, 360)
            
            self.plt.tight_layout()
            
            filepath = os.path.join(self.output_dir, filename)
            self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
            self.plt.close()
            
            return filepath
        except Exception as e:
            print(f"❌ Error creating simple wind chart: {str(e)}")
            return None