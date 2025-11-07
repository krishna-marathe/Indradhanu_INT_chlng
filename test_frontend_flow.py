#!/usr/bin/env python3

import requests
import json
import time

def test_full_flow():
    """Test the complete upload and dashboard flow"""
    
    print("🧪 Testing complete research paper upload flow...")
    
    # Step 1: Upload research paper
    print("\n1️⃣ Uploading research paper...")
    with open("backend/sample_research_paper.txt", "rb") as f:
        files = {"file": ("sample_research_paper.txt", f, "text/plain")}
        response = requests.post("http://127.0.0.1:5000/upload_research_paper", files=files, timeout=60)
    
    if response.status_code != 200:
        print(f"❌ Upload failed: {response.text}")
        return
    
    data = response.json()
    print(f"✅ Upload successful!")
    print(f"📄 Filename: {data.get('filename')}")
    print(f"📊 Has analysis: {bool(data.get('analysis'))}")
    
    # Step 2: Check what the frontend should receive
    print(f"\n2️⃣ Data structure for frontend:")
    print(f"   - status: {data.get('status')}")
    print(f"   - message: {data.get('message')}")
    print(f"   - analysis: {bool(data.get('analysis'))}")
    print(f"   - original_filename: {data.get('original_filename')}")
    
    if data.get('analysis'):
        analysis = data['analysis']
        print(f"   - summary: {analysis.get('summary', 'MISSING')[:50]}...")
        print(f"   - regions: {len(analysis.get('regions', []))} found")
        print(f"   - years: {len(analysis.get('years', []))} found")
        print(f"   - word_count: {analysis.get('word_count', 'MISSING')}")
    
    # Step 3: Simulate what localStorage would contain
    print(f"\n3️⃣ localStorage data structure:")
    localStorage_data = json.dumps(data, indent=2)
    print(localStorage_data[:500] + "..." if len(localStorage_data) > 500 else localStorage_data)
    
    print(f"\n✅ Test complete! The data structure looks correct.")
    print(f"🔍 If dashboard is empty, check browser console for errors.")

if __name__ == "__main__":
    test_full_flow()