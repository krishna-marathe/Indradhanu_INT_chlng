import pandas as pd
import numpy as np

def analyze_satellite_data(df):
    """Analyze satellite/sensor CSV and prepare data for visualization."""
    results = {}
    
    # Detect columns
    columns = [c.lower() for c in df.columns]
    has_geo = 'latitude' in columns and 'longitude' in columns
    has_time = any(c in columns for c in ['timestamp', 'date', 'time'])
    
    # Identify numeric variables (NDVI, AOD, LST, etc.)
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    
    # Prepare geospatial data if available
    if has_geo:
        variable = None
        for col in ['ndvi', 'lst', 'rainfall', 'temperature', 'aod', 'solar_irradiance_wm2', 'albedo']:
            if col in df.columns:
                variable = col
                break
        if variable:
            geo_points = df[['latitude', 'longitude', variable]].dropna()
            geo_points = geo_points.rename(columns={variable: 'value'})
            results['geo_points'] = geo_points.to_dict(orient='records')
            results['hasGeoData'] = True
            results['geoVariable'] = variable
        else:
            results['geo_points'] = []
            results['hasGeoData'] = False
    else:
        results['geo_points'] = []
        results['hasGeoData'] = False
    
    # Time series preparation
    if has_time:
        time_col = [c for c in df.columns if c.lower() in ['timestamp', 'date', 'time']][0]
        df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
        time_series = {}
        for col in numeric_cols:
            if col.lower() not in ['latitude', 'longitude']:
                time_data = df[[time_col, col]].dropna()
                time_data = time_data.groupby(time_col)[col].mean().reset_index()
                time_data[time_col] = time_data[time_col].dt.strftime('%Y-%m-%d %H:%M')
                time_series[col] = time_data.to_dict(orient='records')
        results['time_series'] = time_series
        results['hasTimeData'] = True
    else:
        results['time_series'] = {}
        results['hasTimeData'] = False
    
    # Scatter plot data: solar_irradiance vs albedo
    if 'solar_irradiance_wm2' in df.columns and 'albedo' in df.columns:
        scatter_data = df[['solar_irradiance_wm2', 'albedo']].dropna()
        results['scatter_data'] = scatter_data.to_dict(orient='records')
        results['hasScatterData'] = True
    else:
        results['scatter_data'] = []
        results['hasScatterData'] = False
    
    # Additional scatter combinations for other variables
    scatter_combinations = [
        ('ndvi', 'lst'),
        ('temperature', 'humidity'),
        ('aod', 'rainfall')
    ]
    
    additional_scatters = []
    for x_col, y_col in scatter_combinations:
        if x_col in df.columns and y_col in df.columns:
            scatter_data = df[[x_col, y_col]].dropna()
            if len(scatter_data) > 0:
                additional_scatters.append({
                    'x_column': x_col,
                    'y_column': y_col,
                    'data': scatter_data.to_dict(orient='records')
                })
    
    results['additional_scatters'] = additional_scatters
    results['numeric_columns'] = numeric_cols
    results['total_rows'] = len(df)
    results['total_columns'] = len(df.columns)
    results['dataset_type'] = 'satellite_sensor'
    
    return results