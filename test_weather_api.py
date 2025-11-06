#!/usr/bin/env python3
"""
Test script for the weather API functionality
"""
import requests
import json
import time

API_BASE_URL = "http://127.0.0.1:5000"

def test_weather_current():
    """Test the current weather endpoint"""
    print("🧪 Testing /weather/current endpoint...")
    
    url = f"{API_BASE_URL}/weather/current"
    params = {
        'lat': 52.52,
        'lon': 13.41,
        'hours': 6
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Success! Got {data['data']['data_points']} data points")
        print(f"📍 Location: {data['data']['location']['latitude']}, {data['data']['location']['longitude']}")
        print(f"🌡️ Current temp: {data['data']['statistics']['temperature']['current']}°C")
        print(f"💨 Wind speed: {data['data']['statistics']['wind']['current_speed']} km/h")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_weather_analyze():
    """Test the weather analysis endpoint"""
    print("\n🧪 Testing /weather/analyze endpoint...")
    
    url = f"{API_BASE_URL}/weather/analyze"
    payload = {
        'latitude': 52.52,
        'longitude': 13.41,
        'hours': 6
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Success! Generated {len(data['data']['charts'])} charts")
        
        for chart in data['data']['charts']:
            print(f"📊 Chart: {chart['title']} ({chart['type']})")
        
        print(f"💡 Insights: {len(data['data']['insights'])} generated")
        for insight in data['data']['insights'][:3]:  # Show first 3
            print(f"   • {insight}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_visual_access():
    """Test if generated visuals are accessible"""
    print("\n🧪 Testing visual file access...")
    
    try:
        # First get the list of visuals
        response = requests.get(f"{API_BASE_URL}/visuals/", timeout=10)
        response.raise_for_status()
        
        visuals = response.json()
        print(f"✅ Found {visuals['count']} visual files")
        
        if visuals['files']:
            # Test accessing the first visual
            first_visual = visuals['files'][0]
            visual_response = requests.get(f"{API_BASE_URL}/visuals/{first_visual}", timeout=10)
            visual_response.raise_for_status()
            
            print(f"✅ Successfully accessed visual: {first_visual}")
            print(f"📏 File size: {len(visual_response.content)} bytes")
            return True
        else:
            print("⚠️ No visual files found")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🌤️ Weather API Test Suite")
    print("=" * 50)
    
    # Test basic weather data
    test1 = test_weather_current()
    
    # Test weather analysis with charts
    test2 = test_weather_analyze()
    
    # Test visual file access
    test3 = test_visual_access()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"Current Weather API: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Weather Analysis API: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Visual File Access: {'✅ PASS' if test3 else '❌ FAIL'}")
    
    if all([test1, test2, test3]):
        print("\n🎉 All tests passed! Weather API is fully functional.")
    else:
        print("\n⚠️ Some tests failed. Check the logs above.")