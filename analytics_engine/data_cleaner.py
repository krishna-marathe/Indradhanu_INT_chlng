def clean_data(df):
    """Performs basic cleaning and handles missing data"""
    import pandas as pd
    import numpy as np
    
    print("🧹 Cleaning data...")
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Fill missing values for numeric columns with mean
    for col in df.select_dtypes(include=np.number).columns:
        df[col] = df[col].fillna(df[col].mean())
    
    # Fill missing values for non-numeric columns with mode
    for col in df.select_dtypes(exclude=np.number).columns:
        if not df[col].mode().empty:
            df[col] = df[col].fillna(df[col].mode()[0])
    
    print("✅ Cleaning completed successfully.")
    return df