import pandas as pd
import numpy as np

def compute_climate_metrics(df, baseline_df=None):
    """Compute rainfall, anomaly, heatwave, drought, and flood indices."""
    results = {}
    
    # Convert column names to lowercase for comparison
    cols = [c.lower() for c in df.columns]
    has_region = any(c in cols for c in ['region', 'district', 'state', 'city'])
    has_time = any(c in cols for c in ['timestamp', 'date', 'time'])
    
    # --- Convert timestamp ---
    if has_time:
        time_col = [c for c in df.columns if c.lower() in ['timestamp', 'date', 'time']][0]
        df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
        df['date'] = df[time_col].dt.date
        df['month'] = df[time_col].dt.month
        df['year'] = df[time_col].dt.year
    
    # Find actual column names (case-insensitive)
    rainfall_col = None
    temp_col = None
    soil_moisture_col = None
    region_col = None
    
    for col in df.columns:
        col_lower = col.lower()
        if 'rainfall' in col_lower or col_lower == 'precipitation':
            rainfall_col = col
        elif 'temperature' in col_lower or col_lower in ['temp', 'temp_c']:
            temp_col = col
        elif 'soil_moisture' in col_lower or 'moisture' in col_lower:
            soil_moisture_col = col
        elif col_lower in ['region', 'district', 'state', 'city']:
            region_col = col
    
    # --- 1️⃣ TOTAL RAINFALL ---
    if rainfall_col:
        total_rainfall = df[rainfall_col].sum()
        results['total_rainfall_mm'] = round(float(total_rainfall), 2)
        results['avg_rainfall_mm'] = round(float(df[rainfall_col].mean()), 2)
    else:
        results['total_rainfall_mm'] = None
        results['avg_rainfall_mm'] = None
    
    # --- 2️⃣ RAINFALL ANOMALY ---
    if rainfall_col:
        baseline = None
        if baseline_df is not None and rainfall_col in baseline_df.columns:
            baseline = baseline_df[rainfall_col].mean()
        else:
            # Use historical mean from the same dataset
            baseline = df[rainfall_col].mean()
        
        if baseline and baseline > 0:
            current_mean = df[rainfall_col].mean()
            anomaly = ((current_mean - baseline) / baseline) * 100
            results['rainfall_anomaly_pct'] = round(float(anomaly), 2)
        else:
            results['rainfall_anomaly_pct'] = 0.0
    else:
        results['rainfall_anomaly_pct'] = None
    
    # --- 3️⃣ HEATWAVE DAYS ---
    if temp_col and has_time:
        threshold = df[temp_col].quantile(0.95)  # 95th percentile as heatwave threshold
        daily_max = df.groupby('date')[temp_col].max().reset_index()
        heatwave_days = len(daily_max[daily_max[temp_col] > threshold])
        results['heatwave_days'] = int(heatwave_days)
        results['heatwave_threshold_C'] = round(float(threshold), 2)
        results['max_temperature_C'] = round(float(df[temp_col].max()), 2)
        results['avg_temperature_C'] = round(float(df[temp_col].mean()), 2)
    else:
        results['heatwave_days'] = None
        results['heatwave_threshold_C'] = None
        results['max_temperature_C'] = None
        results['avg_temperature_C'] = None
    
    # --- 4️⃣ DROUGHT RISK INDEX (Simplified SPI using rainfall anomaly) ---
    if rainfall_col:
        try:
            rainfall_std = df[rainfall_col].std()
            if rainfall_std > 0:
                spi = (df[rainfall_col] - df[rainfall_col].mean()) / rainfall_std
                # Convert SPI to 0-100 scale (lower SPI = higher drought risk)
                drought_score = np.clip(100 - ((spi.mean() + 2) * 25), 0, 100)
                results['drought_risk_index'] = round(float(drought_score), 2)
            else:
                results['drought_risk_index'] = 50.0  # Neutral risk
        except:
            results['drought_risk_index'] = 50.0
    else:
        results['drought_risk_index'] = None
    
    # --- 5️⃣ FLOOD RISK INDEX ---
    if rainfall_col and soil_moisture_col:
        try:
            rainfall_max = df[rainfall_col].max()
            soil_max = df[soil_moisture_col].max()
            
            if rainfall_max > 0 and soil_max > 0:
                flood_index = (
                    0.6 * (df[rainfall_col].mean() / rainfall_max) +
                    0.4 * (df[soil_moisture_col].mean() / soil_max)
                ) * 100
                results['flood_risk_index'] = round(float(flood_index), 2)
            else:
                results['flood_risk_index'] = 0.0
        except:
            results['flood_risk_index'] = 0.0
    elif rainfall_col:
        # Simplified flood risk based on rainfall only
        try:
            rainfall_95th = df[rainfall_col].quantile(0.95)
            if rainfall_95th > 0:
                flood_index = (df[rainfall_col].mean() / rainfall_95th) * 100
                results['flood_risk_index'] = round(float(flood_index), 2)
            else:
                results['flood_risk_index'] = 0.0
        except:
            results['flood_risk_index'] = 0.0
    else:
        results['flood_risk_index'] = None
    
    # --- 6️⃣ REGION-LEVEL COMPARISON ---
    if has_region and region_col:
        try:
            agg_dict = {}
            if rainfall_col:
                agg_dict[rainfall_col] = ['sum', 'mean']
            if temp_col:
                agg_dict[temp_col] = 'mean'
            if soil_moisture_col:
                agg_dict[soil_moisture_col] = 'mean'
            
            if agg_dict:
                regional_stats = df.groupby(region_col).agg(agg_dict).reset_index()
                
                # Flatten column names
                regional_data = []
                for _, row in regional_stats.iterrows():
                    region_data = {'region': row[region_col]}
                    
                    if rainfall_col:
                        if (rainfall_col, 'sum') in regional_stats.columns:
                            region_data['total_rainfall'] = round(float(row[(rainfall_col, 'sum')]), 2)
                        if (rainfall_col, 'mean') in regional_stats.columns:
                            region_data['avg_rainfall'] = round(float(row[(rainfall_col, 'mean')]), 2)
                        elif rainfall_col in regional_stats.columns:
                            region_data['rainfall'] = round(float(row[rainfall_col]), 2)
                    
                    if temp_col and temp_col in regional_stats.columns:
                        region_data['avg_temperature'] = round(float(row[temp_col]), 2)
                    
                    if soil_moisture_col and soil_moisture_col in regional_stats.columns:
                        region_data['avg_soil_moisture'] = round(float(row[soil_moisture_col]), 2)
                    
                    regional_data.append(region_data)
                
                results['regional_stats'] = regional_data
                results['regions_count'] = len(regional_data)
        except Exception as e:
            print(f"Regional analysis error: {e}")
            results['regional_stats'] = []
            results['regions_count'] = 0
    else:
        results['regional_stats'] = []
        results['regions_count'] = 0
    
    # --- 7️⃣ Generate insights ---
    insights = []
    
    if results.get('rainfall_anomaly_pct') is not None:
        anomaly = results['rainfall_anomaly_pct']
        if anomaly > 20:
            insights.append("⚠️ Rainfall significantly above normal: potential flood conditions.")
        elif anomaly < -20:
            insights.append("⚠️ Rainfall deficit detected: possible drought risk.")
        elif -10 <= anomaly <= 10:
            insights.append("✅ Rainfall levels are near normal range.")
    
    if results.get('heatwave_days') is not None and results['heatwave_days'] > 5:
        insights.append(f"🔥 {results['heatwave_days']} heatwave days detected (> {results['heatwave_threshold_C']}°C).")
    
    if results.get('drought_risk_index') is not None:
        drought_risk = results['drought_risk_index']
        if drought_risk > 70:
            insights.append("🌵 High drought risk detected - monitor water resources closely.")
        elif drought_risk > 40:
            insights.append("⚠️ Moderate drought risk - consider water conservation measures.")
    
    if results.get('flood_risk_index') is not None:
        flood_risk = results['flood_risk_index']
        if flood_risk > 70:
            insights.append("💧 High flood risk - prepare drainage and emergency measures.")
        elif flood_risk > 40:
            insights.append("⚠️ Moderate flood risk - monitor rainfall and soil saturation.")
    
    if results.get('regions_count', 0) > 1:
        insights.append(f"📊 Regional analysis available for {results['regions_count']} areas.")
    
    results['insights'] = insights
    results['has_climate_data'] = any([
        results.get('total_rainfall_mm') is not None,
        results.get('heatwave_days') is not None,
        results.get('drought_risk_index') is not None,
        results.get('flood_risk_index') is not None
    ])
    
    # Add metadata
    results['analysis_timestamp'] = pd.Timestamp.now().isoformat()
    results['data_period'] = {
        'start_date': df['date'].min().isoformat() if has_time and 'date' in df.columns else None,
        'end_date': df['date'].max().isoformat() if has_time and 'date' in df.columns else None,
        'total_days': len(df['date'].unique()) if has_time and 'date' in df.columns else len(df)
    }
    
    return results