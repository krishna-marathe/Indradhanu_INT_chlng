#!/usr/bin/env python3

import requests
import os

def test_dataset_upload():
    """Test the dataset upload endpoint with real data."""
    
    url = "http://127.0.0.1:5000/upload"
    file_path = "backend/satellite_test.csv"
    
    if not os.path.exists(file_path):
        print(f"❌ Test file not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': ('satellite_test.csv', f, 'text/csv')}
            
            print(f"📤 Uploading {file_path} to {url}")
            response = requests.post(url, files=files, timeout=60)
            
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Upload successful!")
                print(f"📄 Filename: {data.get('filename', 'N/A')}")
                print(f"📊 Rows: {data.get('rows', 'N/A')}")
                print(f"📈 Columns: {data.get('columns', 'N/A')}")
                
                # Check if we have real statistics
                stats = data.get('statistics', {}).get('descriptive_stats', {})
                if stats:
                    print(f"📈 Real statistics found for {len(stats)} columns:")
                    for col, values in list(stats.items())[:3]:  # Show first 3
                        if isinstance(values, dict) and 'mean' in values:
                            print(f"   {col}: mean={values['mean']:.2f}, std={values.get('std', 0):.2f}")
                else:
                    print("⚠️ No statistics found")
                
                return True
            else:
                print(f"❌ Upload failed: {response.text}")
                return False
                
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is Flask running on http://127.0.0.1:5000?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_dataset_upload()