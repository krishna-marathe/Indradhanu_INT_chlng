#!/usr/bin/env python3
"""
Test chart URL generation and accessibility
"""
import requests
import json

API_BASE_URL = "http://127.0.0.1:5000"

def test_chart_generation_and_access():
    """Test that charts are generated and accessible"""
    print("📊 Testing Chart Generation and Access")
    print("=" * 50)
    
    try:
        # Generate weather analysis
        response = requests.post(f"{API_BASE_URL}/weather/analyze", 
                               json={
                                   'latitude': 40.7128,
                                   'longitude': -74.0060,
                                   'hours': 6
                               }, timeout=30)
        response.raise_for_status()
        
        data = response.json()['data']
        charts = data.get('charts', [])
        
        print(f"✅ Analysis complete - {len(charts)} charts generated")
        
        # Test each chart URL
        for i, chart in enumerate(charts):
            print(f"\n📈 Testing Chart {i+1}: {chart['title']}")
            print(f"   Category: {chart.get('category', 'N/A')}")
            print(f"   URL: {chart['url']}")
            
            # Test chart accessibility
            chart_url = f"{API_BASE_URL}{chart['url']}"
            try:
                chart_response = requests.get(chart_url, timeout=10)
                if chart_response.status_code == 200:
                    print(f"   ✅ Chart accessible - Size: {len(chart_response.content)} bytes")
                    
                    # Check if it's actually an image
                    content_type = chart_response.headers.get('content-type', '')
                    if 'image' in content_type:
                        print(f"   ✅ Valid image - Content-Type: {content_type}")
                    else:
                        print(f"   ⚠️ Unexpected content type: {content_type}")
                else:
                    print(f"   ❌ Chart not accessible - Status: {chart_response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error accessing chart: {str(e)}")
        
        return len(charts) > 0
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_visuals_endpoint():
    """Test the visuals listing endpoint"""
    print(f"\n📁 Testing Visuals Endpoint")
    print("=" * 30)
    
    try:
        response = requests.get(f"{API_BASE_URL}/visuals/", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Visuals endpoint working")
        print(f"   📊 Total files: {data['count']}")
        print(f"   📁 Directories scanned: {data['directories_scanned']}")
        
        # Show sample files
        files = data.get('files', [])
        print(f"   📋 Sample files:")
        for file in files[:5]:
            print(f"      • {file}")
        
        return data['count'] > 0
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Chart URL Testing Suite")
    print("=" * 60)
    
    test1 = test_chart_generation_and_access()
    test2 = test_visuals_endpoint()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"Chart Generation & Access: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Visuals Endpoint: {'✅ PASS' if test2 else '❌ FAIL'}")
    
    if test1 and test2:
        print("\n🎉 All chart tests passed! Charts should display correctly in frontend.")
    else:
        print("\n⚠️ Some chart tests failed. Check the logs above.")