import pandas as pd
import os

def load_dataset(file_path):
    """Loads CSV, Excel, or JSON dataset and returns DataFrame dynamically."""
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if ext == ".csv":
            df = pd.read_csv(file_path, encoding='utf-8', engine='python', on_bad_lines='skip')
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(file_path)
        elif ext == ".json":
            df = pd.read_json(file_path)
        else:
            raise ValueError("Unsupported format. Please upload CSV, Excel, or JSON.")
        
        # Basic cleanup - remove completely empty columns and rows
        df.dropna(how='all', axis=1, inplace=True)
        df.dropna(how='all', axis=0, inplace=True)
        
        # Clean column names - strip whitespace and replace problematic characters
        df.columns = [str(c).strip().replace(' ', '_').replace('-', '_') for c in df.columns]
        
        # Remove duplicate columns
        df = df.loc[:, ~df.columns.duplicated()]
        
        print(f"✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns.")
        print(f"📊 Columns: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None
