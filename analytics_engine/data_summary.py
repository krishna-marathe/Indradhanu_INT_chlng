"""
Dynamic Data Summary Generator
"""
from typing import Dict, List, Any


class DataSummary:
    """
    Generates comprehensive descriptive statistics for any dataset
    """
    
    def generate_summary(self, df, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive summary statistics from real data only - NO MOCK DATA
        """
        # Lazy import heavy libraries
        import pandas as pd
        import numpy as np
        from scipy import stats
        
        # Only generate summary if we have actual data
        if df is None or df.empty:
            return {
                'descriptive_stats': {},
                'correlations': {},
                'distributions': {},
                'missing_data': {},
                'outliers': {}
            }
        
        summary = {
            'descriptive_stats': self._descriptive_statistics(df, schema),
            'correlations': self._correlation_analysis(df, schema),
            'distributions': self._distribution_analysis(df, schema),
            'missing_data': self._missing_data_analysis(df),
            'outliers': self._outlier_analysis(df, schema)
        }
        
        return summary
    
    def _descriptive_statistics(self, df, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate descriptive statistics for numeric columns - REAL DATA ONLY
        """
        stats = {}
        
        # Only process numeric columns that actually exist and have data
        for column in schema.get('numeric_columns', []):
            if column in df.columns:
                col_data = df[column].dropna()
                if len(col_data) > 0:
                    try:
                        stats[column] = {
                            'count': int(len(col_data)),
                            'mean': float(col_data.mean()),
                            'median': float(col_data.median()),
                            'mode': float(col_data.mode().iloc[0]) if not col_data.mode().empty else None,
                            'std': float(col_data.std()) if len(col_data) > 1 else 0.0,
                            'var': float(col_data.var()) if len(col_data) > 1 else 0.0,
                            'min': float(col_data.min()),
                            'max': float(col_data.max()),
                            'q25': float(col_data.quantile(0.25)),
                            'q75': float(col_data.quantile(0.75)),
                            'iqr': float(col_data.quantile(0.75) - col_data.quantile(0.25)),
                            'skewness': float(col_data.skew()) if len(col_data) > 1 else 0.0,
                            'kurtosis': float(col_data.kurtosis()) if len(col_data) > 1 else 0.0
                        }
                    except Exception as e:
                        print(f"⚠️ Error calculating stats for {column}: {e}")
                        continue
        
        # Categorical statistics - REAL DATA ONLY
        for column in schema.get('categorical_columns', []):
            if column in df.columns:
                col_data = df[column].dropna()
                if len(col_data) > 0:
                    try:
                        value_counts = col_data.value_counts()
                        stats[column] = {
                            'count': int(len(col_data)),
                            'unique_count': int(col_data.nunique()),
                            'most_frequent': str(value_counts.index[0]) if len(value_counts) > 0 else None,
                            'most_frequent_count': int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                            'frequency_distribution': {str(k): int(v) for k, v in value_counts.head(10).to_dict().items()}
                        }
                    except Exception as e:
                        print(f"⚠️ Error calculating categorical stats for {column}: {e}")
                        continue
        
        return stats
    
    def _correlation_analysis(self, df, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze correlations between numeric variables
        """
        correlations = {}
        
        numeric_df = df[schema['numeric_columns']]
        if len(schema['numeric_columns']) > 1:
            # Pearson correlation
            pearson_corr = numeric_df.corr(method='pearson')
            correlations['pearson'] = pearson_corr.to_dict()
            
            # Spearman correlation (rank-based)
            spearman_corr = numeric_df.corr(method='spearman')
            correlations['spearman'] = spearman_corr.to_dict()
            
            # Find strong correlations
            strong_correlations = []
            for i, col1 in enumerate(schema['numeric_columns']):
                for j, col2 in enumerate(schema['numeric_columns']):
                    if i < j:  # Avoid duplicates
                        corr_value = pearson_corr.loc[col1, col2]
                        if abs(corr_value) > 0.7:  # Strong correlation threshold
                            strong_correlations.append({
                                'column1': col1,
                                'column2': col2,
                                'correlation': float(corr_value),
                                'strength': 'strong' if abs(corr_value) > 0.8 else 'moderate'
                            })
            
            correlations['strong_correlations'] = strong_correlations
        
        return correlations
    
    def _distribution_analysis(self, df, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze distributions of numeric variables
        """
        distributions = {}
        
        for column in schema['numeric_columns']:
            col_data = df[column].dropna()
            if len(col_data) > 10:  # Need sufficient data for distribution analysis
                # Test for normality
                from scipy import stats
                shapiro_stat, shapiro_p = stats.shapiro(col_data.sample(min(5000, len(col_data))))
                
                distributions[column] = {
                    'normality_test': {
                        'shapiro_stat': float(shapiro_stat),
                        'shapiro_p_value': float(shapiro_p),
                        'is_normal': shapiro_p > 0.05
                    },
                    'histogram_bins': self._calculate_optimal_bins(col_data),
                    'distribution_type': self._identify_distribution_type(col_data)
                }
        
        return distributions
    
    def _missing_data_analysis(self, df) -> Dict[str, Any]:
        """
        Analyze missing data patterns
        """
        missing_info = {}
        
        for column in df.columns:
            missing_count = df[column].isnull().sum()
            missing_percentage = (missing_count / len(df)) * 100
            
            missing_info[column] = {
                'missing_count': int(missing_count),
                'missing_percentage': float(missing_percentage),
                'has_missing': missing_count > 0
            }
        
        # Overall missing data summary
        total_missing = df.isnull().sum().sum()
        total_cells = df.shape[0] * df.shape[1]
        
        missing_info['summary'] = {
            'total_missing_values': int(total_missing),
            'total_cells': int(total_cells),
            'overall_missing_percentage': float((total_missing / total_cells) * 100),
            'columns_with_missing': int(sum(1 for col in df.columns if df[col].isnull().any()))
        }
        
        return missing_info
    
    def _outlier_analysis(self, df, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect outliers in numeric columns using IQR method
        """
        outliers = {}
        
        for column in schema['numeric_columns']:
            col_data = df[column].dropna()
            if len(col_data) > 0:
                Q1 = col_data.quantile(0.25)
                Q3 = col_data.quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outlier_mask = (col_data < lower_bound) | (col_data > upper_bound)
                outlier_count = outlier_mask.sum()
                
                outliers[column] = {
                    'outlier_count': int(outlier_count),
                    'outlier_percentage': float((outlier_count / len(col_data)) * 100),
                    'lower_bound': float(lower_bound),
                    'upper_bound': float(upper_bound),
                    'has_outliers': outlier_count > 0
                }
        
        return outliers
    
    def _calculate_optimal_bins(self, data) -> int:
        """
        Calculate optimal number of bins for histogram using Sturges' rule
        """
        import numpy as np
        n = len(data)
        bins = int(np.ceil(np.log2(n) + 1))
        return max(5, min(bins, 50))  # Ensure reasonable range
    
    def _identify_distribution_type(self, data) -> str:
        """
        Identify the likely distribution type based on skewness and kurtosis
        """
        skewness = data.skew()
        kurtosis = data.kurtosis()
        
        if abs(skewness) < 0.5 and abs(kurtosis) < 0.5:
            return "normal"
        elif skewness > 1:
            return "right_skewed"
        elif skewness < -1:
            return "left_skewed"
        elif kurtosis > 3:
            return "heavy_tailed"
        elif kurtosis < -1:
            return "light_tailed"
        else:
            return "unknown"