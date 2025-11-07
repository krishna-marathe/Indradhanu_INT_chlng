#!/usr/bin/env python3

import requests
import json

def debug_upload():
    try:
        print("🔍 Testing research paper upload with detailed debugging...")
        
        with open("backend/sample_research_paper.txt", "rb") as f:
            files = {"file": ("sample_research_paper.txt", f, "text/plain")}
            response = requests.post("http://127.0.0.1:5000/upload_research_paper", files=files, timeout=60)
            
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS! Full response:")
            print(json.dumps(data, indent=2))
            
            # Check specific fields
            analysis = data.get('analysis', {})
            print(f"\n🔍 Analysis Summary: {analysis.get('summary', 'MISSING')}")
            print(f"🗺️ Regions: {analysis.get('regions', 'MISSING')}")
            print(f"📅 Years: {analysis.get('years', 'MISSING')}")
            print(f"📊 Word Count: {analysis.get('word_count', 'MISSING')}")
            
        else:
            print(f"❌ ERROR Response:")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_upload()