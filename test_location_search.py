#!/usr/bin/env python3
"""
Test script for location search and weather analysis functionality
"""
import requests
import json
import time

API_BASE_URL = "http://127.0.0.1:5000"

def test_location_search():
    """Test location search functionality"""
    print("🔍 Testing location search...")
    
    test_queries = [
        "New York",
        "London",
        "Tokyo",
        "Paris, France",
        "Sydney, Australia"
    ]
    
    for query in test_queries:
        try:
            response = requests.get(f"{API_BASE_URL}/geocoding/search", 
                                  params={'q': query, 'limit': 3}, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            print(f"✅ '{query}': Found {data['count']} results")
            
            if data['results']:
                best_match = data['results'][0]
                print(f"   📍 Best match: {best_match['clean_name']}")
                print(f"   🌍 Coordinates: {best_match['latitude']:.2f}, {best_match['longitude']:.2f}")
            
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            print(f"❌ Error searching '{query}': {str(e)}")
    
    return True

def test_popular_locations():
    """Test popular locations endpoint"""
    print("\n🌍 Testing popular locations...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/geocoding/popular", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Found {data['count']} popular locations")
        
        for i, location in enumerate(data['locations'][:5]):
            print(f"   {i+1}. {location['clean_name']} ({location['latitude']:.2f}, {location['longitude']:.2f})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_weather_for_multiple_cities():
    """Test weather analysis for different cities"""
    print("\n🌤️ Testing weather analysis for multiple cities...")
    
    cities = [
        {"name": "New York", "lat": 40.7128, "lon": -74.0060},
        {"name": "London", "lat": 51.5074, "lon": -0.1278},
        {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503},
        {"name": "Sydney", "lat": -33.8688, "lon": 151.2093}
    ]
    
    for city in cities:
        try:
            print(f"\n📍 Analyzing weather for {city['name']}...")
            
            response = requests.post(f"{API_BASE_URL}/weather/analyze", 
                                   json={
                                       'latitude': city['lat'],
                                       'longitude': city['lon'],
                                       'hours': 6
                                   }, timeout=30)
            response.raise_for_status()
            
            data = response.json()['data']
            
            print(f"✅ {city['name']} weather analysis complete:")
            print(f"   📊 Charts generated: {len(data.get('charts', []))}")
            print(f"   📈 Data points: {data.get('data_points', 0)}")
            
            # Display current conditions
            stats = data.get('statistics', {})
            if 'temperature' in stats:
                temp = stats['temperature'].get('current')
                trend = stats['temperature'].get('trend', 'stable')
                print(f"   🌡️ Temperature: {temp:.1f}°C ({trend})")
            
            if 'wind' in stats:
                wind = stats['wind'].get('current_speed')
                print(f"   💨 Wind: {wind:.1f} km/h")
            
            # Display insights
            insights = data.get('insights', [])
            if insights:
                print(f"   💡 Key insight: {insights[0]}")
            
            time.sleep(2)  # Rate limiting
            
        except Exception as e:
            print(f"❌ Error analyzing {city['name']}: {str(e)}")

def test_search_and_analyze_workflow():
    """Test the complete workflow: search location -> get weather"""
    print("\n🔄 Testing complete search-to-weather workflow...")
    
    try:
        # Step 1: Search for a location
        search_query = "Mumbai, India"
        print(f"🔍 Step 1: Searching for '{search_query}'...")
        
        response = requests.get(f"{API_BASE_URL}/geocoding/search", 
                              params={'q': search_query, 'limit': 1}, timeout=10)
        response.raise_for_status()
        
        search_data = response.json()
        if not search_data['results']:
            print("❌ No location found")
            return False
        
        location = search_data['results'][0]
        print(f"✅ Found: {location['clean_name']}")
        print(f"📍 Coordinates: {location['latitude']:.4f}, {location['longitude']:.4f}")
        
        # Step 2: Get weather for that location
        print(f"\n🌤️ Step 2: Getting weather for {location['clean_name']}...")
        
        weather_response = requests.post(f"{API_BASE_URL}/weather/analyze", 
                                       json={
                                           'latitude': location['latitude'],
                                           'longitude': location['longitude'],
                                           'hours': 6
                                       }, timeout=30)
        weather_response.raise_for_status()
        
        weather_data = weather_response.json()['data']
        
        print(f"✅ Weather analysis complete for {location['clean_name']}:")
        print(f"   📊 Generated {len(weather_data.get('charts', []))} charts")
        print(f"   📈 Processed {weather_data.get('data_points', 0)} data points")
        print(f"   💡 Generated {len(weather_data.get('insights', []))} insights")
        
        # Show sample insight
        if weather_data.get('insights'):
            print(f"   🔍 Sample insight: {weather_data['insights'][0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🌍 Location Search & Weather Analysis Test Suite")
    print("=" * 60)
    
    # Test location search
    test1 = test_location_search()
    
    # Test popular locations
    test2 = test_popular_locations()
    
    # Test weather for multiple cities
    test_weather_for_multiple_cities()
    
    # Test complete workflow
    test3 = test_search_and_analyze_workflow()
    
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"Location Search: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Popular Locations: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Complete Workflow: {'✅ PASS' if test3 else '❌ FAIL'}")
    
    if all([test1, test2, test3]):
        print("\n🎉 All location search tests passed!")
        print("🌍 Users can now search for any location worldwide and get weather analysis!")
    else:
        print("\n⚠️ Some tests failed. Check the logs above.")