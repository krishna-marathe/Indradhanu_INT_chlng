#!/usr/bin/env python3

import requests
import os

def test_research_paper_upload():
    """Test the research paper upload endpoint."""
    
    url = "http://127.0.0.1:5000/upload_research_paper"
    file_path = "backend/sample_research_paper.txt"
    
    if not os.path.exists(file_path):
        print(f"❌ Test file not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': ('sample_research_paper.txt', f, 'text/plain')}
            
            print(f"📤 Uploading {file_path} to {url}")
            response = requests.post(url, files=files, timeout=30)
            
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Upload successful!")
                print(f"📄 Filename: {data.get('filename', 'N/A')}")
                print(f"📊 Analysis summary: {data.get('analysis', {}).get('summary', 'N/A')[:100]}...")
                print(f"🗺️ Regions found: {len(data.get('analysis', {}).get('regions', []))}")
                print(f"📅 Years found: {len(data.get('analysis', {}).get('years', []))}")
                print(f"🔬 Methods found: {len(data.get('analysis', {}).get('research_methods', []))}")
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
    test_research_paper_upload()