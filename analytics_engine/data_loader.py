import pandas as pd
import os

def load_dataset(file_path):
    """Loads dataset and returns DataFrame safely"""
    try:
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return None

        ext = file_path.lower()
        if ext.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='utf-8', engine='python', on_bad_lines='skip')
        elif ext.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        elif ext.endswith('.json'):
            df = pd.read_json(file_path)
        else:
            raise ValueError("Unsupported file format! Upload CSV, XLSX, or JSON.")

        # Drop completely empty columns
        df.dropna(how='all', axis=1, inplace=True)

        print(f"✅ Loaded dataset — Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        return df

    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None
