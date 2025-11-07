#!/usr/bin/env python3

import requests
import time

def test_upload():
    try:
        # Test basic connection first
        print("Testing basic connection...")
        response = requests.get("http://127.0.0.1:5000/", timeout=5)
        print(f"Basic connection: {response.status_code}")
        
        # Test research paper upload
        print("Testing research paper upload...")
        with open("backend/sample_research_paper.txt", "rb") as f:
            files = {"file": ("sample_research_paper.txt", f, "text/plain")}
            response = requests.post("http://127.0.0.1:5000/upload_research_paper", files=files, timeout=30)
            
        print(f"Upload response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(f"Analysis: {data.get('analysis', {}).get('summary', 'No summary')[:100]}...")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_upload()