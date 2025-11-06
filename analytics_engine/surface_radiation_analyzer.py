import pandas as pd
import numpy as np
from scipy import stats

def analyze_surface_radiation(df):
    """Analyze surface temperature and radiation relationships."""
    results = {}
    
    # Convert column names to lowercase for comparison
    cols = [c.lower() for c in df.columns]
    
    # Detect required columns
    has_time = any(c in cols for c in ['timestamp', 'date', 'time'])
    
    if has_time:
        time_col = [c for c in df.columns if c.lower() in ['timestamp', 'date', 'time']][0]
        df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
        
        # Find the actual column names (case-insensitive)
        temp_col = None
        solar_col = None
        albedo_col = None
        
        for col in df.columns:
            col_lower = col.lower()
            if 'surface_temp' in col_lower or col_lower == 'surface_temp_c':
                temp_col = col
            elif 'solar_irradiance' in col_lower or col_lower == 'solar_irradiance_wm2':
                solar_col = col
            elif col_lower == 'albedo':
                albedo_col = col
        
        if temp_col and solar_col and albedo_col:
            # Clean numeric data
            clean_df = df[[time_col, temp_col, solar_col, albedo_col]].dropna()
            
            if len(clean_df) > 1:
                # Trend data: surface temperature vs time
                trend_data = clean_df.groupby(time_col)[temp_col].mean().reset_index()
                trend_data[time_col] = trend_data[time_col].dt.strftime('%Y-%m-%d %H:%M')
                results['trend_data'] = trend_data.to_dict(orient='records')
                
                # Scatter data: solar irradiance vs surface temperature
                scatter_data = clean_df[[solar_col, temp_col, albedo_col]].copy()
                scatter_data.columns = ['solar_irradiance_wm2', 'surface_temp_c', 'albedo']
                results['scatter_data'] = scatter_data.to_dict(orient='records')
                
                # Additional scatter: albedo vs surface temperature
                albedo_temp_scatter = clean_df[[albedo_col, temp_col]].copy()
                albedo_temp_scatter.columns = ['albedo', 'surface_temp_c']
                results['albedo_temp_scatter'] = albedo_temp_scatter.to_dict(orient='records')
                
                # Compute regression between solar irradiance and surface temperature
                if len(clean_df) > 2:
                    try:
                        slope, intercept, r_value, p_value, std_err = stats.linregress(
                            clean_df[solar_col], clean_df[temp_col]
                        )
                        results['solar_temp_regression'] = {
                            'slope': round(float(slope), 4),
                            'intercept': round(float(intercept), 2),
                            'r_value': round(float(r_value), 3),
                            'r_squared': round(float(r_value**2), 3),
                            'p_value': round(float(p_value), 4)
                        }
                        
                        # Compute regression between albedo and surface temperature
                        slope2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(
                            clean_df[albedo_col], clean_df[temp_col]
                        )
                        results['albedo_temp_regression'] = {
                            'slope': round(float(slope2), 4),
                            'intercept': round(float(intercept2), 2),
                            'r_value': round(float(r_value2), 3),
                            'r_squared': round(float(r_value2**2), 3),
                            'p_value': round(float(p_value2), 4)
                        }
                        
                        # Generate human-readable insights
                        correlation_strength = (
                            "strong" if abs(r_value) > 0.7 else
                            "moderate" if abs(r_value) > 0.4 else
                            "weak"
                        )
                        direction = "positive" if r_value > 0 else "negative"
                        
                        albedo_correlation_strength = (
                            "strong" if abs(r_value2) > 0.7 else
                            "moderate" if abs(r_value2) > 0.4 else
                            "weak"
                        )
                        albedo_direction = "positive" if r_value2 > 0 else "negative"
                        
                        results['insights'] = [
                            f"Solar irradiance shows a {correlation_strength} {direction} correlation with surface temperature (R² = {results['solar_temp_regression']['r_squared']}).",
                            f"Albedo shows a {albedo_correlation_strength} {albedo_direction} correlation with surface temperature (R² = {results['albedo_temp_regression']['r_squared']})."
                        ]
                        
                        # Statistical significance
                        if p_value < 0.05:
                            results['insights'].append("The solar irradiance-temperature relationship is statistically significant (p < 0.05).")
                        if p_value2 < 0.05:
                            results['insights'].append("The albedo-temperature relationship is statistically significant (p < 0.05).")
                            
                    except Exception as e:
                        print(f"Regression analysis error: {e}")
                        results['regression_error'] = str(e)
                
                results['has_surface_radiation_data'] = True
                results['data_points'] = len(clean_df)
                results['column_names'] = {
                    'temperature': temp_col,
                    'solar_irradiance': solar_col,
                    'albedo': albedo_col,
                    'time': time_col
                }
            else:
                results['message'] = "Insufficient data points for analysis."
                results['has_surface_radiation_data'] = False
        else:
            missing_cols = []
            if not temp_col:
                missing_cols.append('surface_temp_C')
            if not solar_col:
                missing_cols.append('solar_irradiance_Wm2')
            if not albedo_col:
                missing_cols.append('albedo')
            
            results['message'] = f"Required columns not found: {', '.join(missing_cols)}"
            results['has_surface_radiation_data'] = False
    else:
        results['message'] = "No timestamp column found for trend analysis."
        results['has_surface_radiation_data'] = False
    
    return results