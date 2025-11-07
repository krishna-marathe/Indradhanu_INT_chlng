#!/usr/bin/env python3

import requests
import json

def test_complete_flow():
    """Test the complete research paper upload and dashboard flow"""
    
    print("🧪 Testing complete research paper flow...")
    print("=" * 60)
    
    # Step 1: Upload research paper
    print("\n1️⃣ BACKEND UPLOAD TEST")
    print("-" * 30)
    
    with open("test_document.txt", "rb") as f:
        files = {"file": ("test_document.txt", f, "text/plain")}
        response = requests.post("http://127.0.0.1:5000/upload_research_paper", files=files, timeout=60)
    
    if response.status_code != 200:
        print(f"❌ Backend upload failed: {response.text}")
        return
    
    data = response.json()
    print(f"✅ Backend upload successful!")
    print(f"📊 Status: {data.get('status')}")
    print(f"📄 Filename: {data.get('filename')}")
    print(f"📋 Original filename: {data.get('original_filename')}")
    print(f"🔍 Has analysis: {bool(data.get('analysis'))}")
    
    # Step 2: Check analysis content
    print(f"\n2️⃣ ANALYSIS CONTENT CHECK")
    print("-" * 30)
    
    if data.get('analysis'):
        analysis = data['analysis']
        print(f"✅ Analysis found!")
        print(f"📝 Summary: {analysis.get('summary', 'MISSING')}")
        print(f"🗺️ Regions: {analysis.get('regions', [])}")
        print(f"📅 Years: {analysis.get('years', [])}")
        print(f"📊 Word count: {analysis.get('word_count', 'MISSING')}")
        print(f"🌍 Climate keywords: {len(analysis.get('climate_keywords', []))} found")
        print(f"🔬 Research methods: {len(analysis.get('research_methods', []))} found")
        print(f"📈 Key trends: {len(analysis.get('key_trends', []))} found")
    else:
        print("❌ No analysis found in response!")
        return
    
    # Step 3: Frontend data structure simulation
    print(f"\n3️⃣ FRONTEND DATA FLOW SIMULATION")
    print("-" * 30)
    
    # This is what ResearchPaperUploader sends to dashboard
    navigation_state = {
        "paperAnalysis": data
    }
    
    print(f"📤 ResearchPaperUploader sends:")
    print(f"   navigate('/dashboard', {{ state: {{ paperAnalysis: data }} }})")
    
    # This is what AnalyticsDashboard receives
    print(f"\n📥 AnalyticsDashboard receives:")
    print(f"   location.state.paperAnalysis = {bool(navigation_state.get('paperAnalysis'))}")
    
    # This is what gets set as currentUpload
    current_upload = navigation_state['paperAnalysis']
    print(f"   setCurrentUpload(location.state.paperAnalysis)")
    print(f"   currentUpload.analysis = {bool(current_upload.get('analysis'))}")
    
    # This is the condition check
    print(f"\n🔍 Dashboard condition check:")
    print(f"   upload.analysis ? → {bool(current_upload.get('analysis'))}")
    
    if current_upload.get('analysis'):
        print(f"   ✅ Should show ResearchPaperInsights")
        print(f"   📄 Component receives: data={{")
        print(f"        status: '{current_upload.get('status')}'")
        print(f"        analysis: {{ ... }} (with {len(current_upload['analysis'])} fields)")
        print(f"      }}")
    else:
        print(f"   ❌ Would show dataset analysis instead")
    
    # Step 4: ResearchPaperInsights component check
    print(f"\n4️⃣ COMPONENT COMPATIBILITY CHECK")
    print("-" * 30)
    
    # This is what ResearchPaperInsights expects
    component_data = current_upload
    component_analysis = component_data.get('analysis')
    
    print(f"📄 ResearchPaperInsights component:")
    print(f"   Receives: data = {bool(component_data)}")
    print(f"   Checks: data.analysis = {bool(component_analysis)}")
    
    if component_analysis:
        print(f"   ✅ Component should render successfully!")
        print(f"   📊 Will display:")
        print(f"      - Summary: {component_analysis.get('summary', 'MISSING')[:50]}...")
        print(f"      - Regions: {len(component_analysis.get('regions', []))} items")
        print(f"      - Years: {len(component_analysis.get('years', []))} items")
        print(f"      - Word count: {component_analysis.get('word_count', 'MISSING')}")
    else:
        print(f"   ❌ Component would return null!")
    
    print(f"\n" + "=" * 60)
    print(f"🎯 CONCLUSION:")
    
    if (data.get('analysis') and 
        navigation_state.get('paperAnalysis') and 
        current_upload.get('analysis') and 
        component_analysis):
        print(f"✅ ALL CHECKS PASSED - Frontend should work correctly!")
        print(f"📋 Next steps:")
        print(f"   1. Upload a file through the frontend")
        print(f"   2. Check browser console for debug logs")
        print(f"   3. Verify dashboard displays analysis")
    else:
        print(f"❌ ISSUE FOUND - Check the failed conditions above")
    
    print(f"=" * 60)

if __name__ == "__main__":
    test_complete_flow()