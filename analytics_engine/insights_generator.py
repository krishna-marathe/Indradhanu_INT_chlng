"""
Dynamic Insights Generator - Generates contextual insights based on data analysis
"""
from typing import Dict, List, Any


class InsightsGenerator:
    """
    Generates meaningful insights from data analysis results
    """
    
    def generate_insights(self, df, schema: Dict[str, Any], statistics: Dict[str, Any]) -> List[str]:
        """
        Generate comprehensive insights based on data analysis
        """
        insights = []
        
        # Dataset overview insights
        insights.extend(self._dataset_overview_insights(df, schema))
        
        # Statistical insights
        insights.extend(self._statistical_insights(df, schema, statistics))
        
        # Data quality insights
        insights.extend(self._data_quality_insights(df, statistics))
        
        # Correlation insights
        insights.extend(self._correlation_insights(statistics))
        
        # Distribution insights
        insights.extend(self._distribution_insights(statistics))
        
        # Outlier insights
        insights.extend(self._outlier_insights(statistics))
        
        return insights
    
    def _dataset_overview_insights(self, df, schema: Dict[str, Any]) -> List[str]:
        """Generate insights about dataset structure and composition"""
        insights = []
        
        total_cols = len(df.columns)
        total_rows = len(df)
        
        insights.append(f"📊 Dataset contains {total_rows:,} records across {total_cols} variables")
        
        # Column type distribution
        type_summary = schema['summary']
        if type_summary['numeric'] > 0:
            insights.append(f"🔢 {type_summary['numeric']} numeric variables detected for quantitative analysis")
        
        if type_summary['categorical'] > 0:
            insights.append(f"🏷️ {type_summary['categorical']} categorical variables identified for grouping analysis")
        
        if type_summary['datetime'] > 0:
            insights.append(f"📅 {type_summary['datetime']} datetime variables found for temporal analysis")
        
        # Data density insight
        memory_usage = df.memory_usage(deep=True).sum() / 1024 / 1024  # MB
        insights.append(f"💾 Dataset size: {memory_usage:.2f} MB in memory")
        
        return insights
    
    def _statistical_insights(self, df, schema: Dict[str, Any], statistics: Dict[str, Any]) -> List[str]:
        """Generate insights from descriptive statistics"""
        insights = []
        
        desc_stats = statistics.get('descriptive_stats', {})
        
        for column in schema['numeric_columns'][:5]:  # Limit to first 5 columns
            if column in desc_stats:
                stats = desc_stats[column]
                mean_val = stats['mean']
                median_val = stats['median']
                std_val = stats['std']
                
                # Central tendency insight
                if abs(mean_val - median_val) / max(abs(mean_val), abs(median_val), 1) > 0.1:
                    if mean_val > median_val:
                        insights.append(f"📈 {column}: Right-skewed distribution (mean {mean_val:.2f} > median {median_val:.2f})")
                    else:
                        insights.append(f"📉 {column}: Left-skewed distribution (mean {mean_val:.2f} < median {median_val:.2f})")
                else:
                    insights.append(f"⚖️ {column}: Symmetric distribution (mean ≈ median ≈ {mean_val:.2f})")
                
                # Variability insight
                cv = std_val / abs(mean_val) if mean_val != 0 else 0
                if cv > 1:
                    insights.append(f"📊 {column}: High variability detected (CV = {cv:.2f})")
                elif cv < 0.1:
                    insights.append(f"📏 {column}: Low variability, values are consistent (CV = {cv:.2f})")
        
        # Categorical insights
        for column in schema['categorical_columns'][:3]:
            if column in desc_stats:
                stats = desc_stats[column]
                unique_count = stats['unique_count']
                total_count = stats['count']
                most_frequent = stats['most_frequent']
                most_frequent_count = stats['most_frequent_count']
                
                diversity = unique_count / total_count
                dominance = most_frequent_count / total_count
                
                if diversity > 0.8:
                    insights.append(f"🌈 {column}: High diversity with {unique_count} unique categories")
                elif dominance > 0.7:
                    insights.append(f"🎯 {column}: Dominated by '{most_frequent}' ({dominance:.1%} of records)")
                else:
                    insights.append(f"🏷️ {column}: Balanced distribution across {unique_count} categories")
        
        return insights
    
    def _data_quality_insights(self, df, statistics: Dict[str, Any]) -> List[str]:
        """Generate insights about data quality"""
        insights = []
        
        missing_info = statistics.get('missing_data', {})
        summary = missing_info.get('summary', {})
        
        overall_missing = summary.get('overall_missing_percentage', 0)
        columns_with_missing = summary.get('columns_with_missing', 0)
        
        if overall_missing == 0:
            insights.append("✅ Excellent data quality: No missing values detected")
        elif overall_missing < 5:
            insights.append(f"✅ Good data quality: Only {overall_missing:.1f}% missing values")
        elif overall_missing < 15:
            insights.append(f"⚠️ Moderate data quality: {overall_missing:.1f}% missing values need attention")
        else:
            insights.append(f"🚨 Poor data quality: {overall_missing:.1f}% missing values require significant cleaning")
        
        if columns_with_missing > 0:
            insights.append(f"🔍 {columns_with_missing} columns contain missing values")
        
        # Identify columns with high missing rates
        high_missing_cols = []
        for col, info in missing_info.items():
            if isinstance(info, dict) and info.get('missing_percentage', 0) > 20:
                high_missing_cols.append(col)
        
        if high_missing_cols:
            insights.append(f"⚠️ High missing rates in: {', '.join(high_missing_cols[:3])}")
        
        return insights
    
    def _correlation_insights(self, statistics: Dict[str, Any]) -> List[str]:
        """Generate insights from correlation analysis"""
        insights = []
        
        correlations = statistics.get('correlations', {})
        strong_correlations = correlations.get('strong_correlations', [])
        
        if not strong_correlations:
            insights.append("🔍 No strong correlations detected between numeric variables")
        else:
            for corr in strong_correlations[:3]:  # Limit to top 3
                col1, col2 = corr['column1'], corr['column2']
                corr_value = corr['correlation']
                strength = corr['strength']
                
                if corr_value > 0:
                    insights.append(f"📈 Strong positive correlation between {col1} and {col2} (r = {corr_value:.3f})")
                else:
                    insights.append(f"📉 Strong negative correlation between {col1} and {col2} (r = {corr_value:.3f})")
        
        return insights
    
    def _distribution_insights(self, statistics: Dict[str, Any]) -> List[str]:
        """Generate insights about data distributions"""
        insights = []
        
        distributions = statistics.get('distributions', {})
        
        normal_vars = []
        skewed_vars = []
        
        for column, dist_info in distributions.items():
            normality = dist_info.get('normality_test', {})
            if normality.get('is_normal', False):
                normal_vars.append(column)
            else:
                skewed_vars.append(column)
        
        if normal_vars:
            insights.append(f"📊 Normal distributions detected in: {', '.join(normal_vars[:3])}")
        
        if skewed_vars:
            insights.append(f"📐 Non-normal distributions in: {', '.join(skewed_vars[:3])} - consider transformations")
        
        return insights
    
    def _outlier_insights(self, statistics: Dict[str, Any]) -> List[str]:
        """Generate insights about outliers"""
        insights = []
        
        outliers = statistics.get('outliers', {})
        
        high_outlier_cols = []
        clean_cols = []
        
        for column, outlier_info in outliers.items():
            outlier_percentage = outlier_info.get('outlier_percentage', 0)
            if outlier_percentage > 5:
                high_outlier_cols.append((column, outlier_percentage))
            elif outlier_percentage == 0:
                clean_cols.append(column)
        
        if clean_cols:
            insights.append(f"✅ No outliers detected in: {', '.join(clean_cols[:3])}")
        
        if high_outlier_cols:
            for col, percentage in high_outlier_cols[:3]:
                insights.append(f"🎯 {col}: {percentage:.1f}% outliers detected - investigate extreme values")
        
        return insights