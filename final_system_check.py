#!/usr/bin/env python3

import requests
import json

def final_system_check():
    """Comprehensive system check"""
    
    print("=" * 70)
    print("🔍 FINAL SYSTEM CHECK - Research Paper Analysis")
    print("=" * 70)
    
    # Test 1: Backend Health
    print("\n1️⃣ BACKEND HEALTH CHECK")
    print("-" * 40)
    try:
        response = requests.get("http://127.0.0.1:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend is not accessible: {e}")
        return False
    
    # Test 2: Research Paper Upload
    print("\n2️⃣ RESEARCH PAPER UPLOAD TEST")
    print("-" * 40)
    try:
        with open("test_document.txt", "rb") as f:
            files = {"file": ("test_document.txt", f, "text/plain")}
            response = requests.post("http://127.0.0.1:5000/upload_research_paper", files=files, timeout=60)
        
        if response.status_code != 200:
            print(f"❌ Upload failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        data = response.json()
        print("✅ Upload successful")
        print(f"   Status: {data.get('status')}")
        print(f"   Has analysis: {bool(data.get('analysis'))}")
        
        if not data.get('analysis'):
            print("❌ No analysis in response!")
            return False
        
        analysis = data['analysis']
        print(f"   Summary length: {len(analysis.get('summary', ''))}")
        print(f"   Word count: {analysis.get('word_count')}")
        print(f"   Regions: {len(analysis.get('regions', []))}")
        print(f"   Years: {len(analysis.get('years', []))}")
        
    except Exception as e:
        print(f"❌ Upload test failed: {e}")
        return False
    
    # Test 3: Data Structure Validation
    print("\n3️⃣ DATA STRUCTURE VALIDATION")
    print("-" * 40)
    
    required_fields = ['summary', 'regions', 'years', 'word_count', 'climate_keywords', 
                      'research_methods', 'key_findings', 'document_type', 'analysis_confidence']
    
    missing_fields = []
    for field in required_fields:
        if field not in analysis:
            missing_fields.append(field)
            print(f"❌ Missing field: {field}")
        else:
            value = analysis[field]
            if isinstance(value, list):
                print(f"✅ {field}: {len(value)} items")
            elif isinstance(value, str):
                print(f"✅ {field}: {len(value)} chars")
            else:
                print(f"✅ {field}: {value}")
    
    if missing_fields:
        print(f"\n❌ Missing {len(missing_fields)} required fields!")
        return False
    
    # Test 4: Frontend Accessibility
    print("\n4️⃣ FRONTEND ACCESSIBILITY CHECK")
    print("-" * 40)
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
        else:
            print(f"⚠️ Frontend returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend is not accessible: {e}")
        return False
    
    # Test 5: Sample Data Display
    print("\n5️⃣ SAMPLE DATA FOR FRONTEND")
    print("-" * 40)
    print(f"Summary: {analysis['summary'][:100]}...")
    print(f"Regions: {analysis['regions']}")
    print(f"Years: {analysis['years']}")
    print(f"Word Count: {analysis['word_count']}")
    
    # Final Summary
    print("\n" + "=" * 70)
    print("🎯 SYSTEM CHECK COMPLETE")
    print("=" * 70)
    print("✅ Backend: Working")
    print("✅ Analysis: Complete")
    print("✅ Data Structure: Valid")
    print("✅ Frontend: Accessible")
    print("\n📋 NEXT STEPS:")
    print("1. Open http://localhost:3000 in your browser")
    print("2. Upload a research paper (.txt file)")
    print("3. Open browser console (F12)")
    print("4. Check for logs starting with 🔍, 📄, 📊")
    print("5. Verify dashboard displays the analysis")
    print("\n💡 If dashboard is empty, check browser console for errors!")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        success = final_system_check()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ System check failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)