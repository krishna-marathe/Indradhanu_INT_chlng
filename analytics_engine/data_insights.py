def basic_summary(df):
    print("\n📋 BASIC SUMMARY:")
    print(df.describe(include='all'))
    print("\nColumns:", list(df.columns))
    print("\nMissing Values:\n", df.isnull().sum())

def correlation_analysis(df):
    print("\n🔍 Correlation Matrix:")
    corr = df.corr(numeric_only=True)
    print(corr)
    return corr

def generate_insights(df):
    """Generate key findings dynamically"""
    import numpy as np
    
    insights = []
    numeric_cols = df.select_dtypes(include=np.number).columns
    
    for col in numeric_cols:
        avg = df[col].mean()
        insights.append(f"📊 {col}: Average = {avg:.2f}")
    
    # Special case for AQI column
    if 'AQI' in df.columns:
        avg_aqi = df['AQI'].mean()
        if avg_aqi > 150:
            insights.append(f"⚠️ Poor air quality detected (Average AQI: {avg_aqi:.2f})")
        else:
            insights.append(f"🌿 Healthy air quality (Average AQI: {avg_aqi:.2f})")
    
    print("\n💡 KEY INSIGHTS:")
    for i in insights:
        print("-", i)
    
    return insights