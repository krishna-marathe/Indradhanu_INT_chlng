"""
Test AQI Endpoint
"""
import requests
import json

def test_aqi_endpoint():
    print("=" * 60)
    print("AQI ENDPOINT TEST")
    print("=" * 60)
    
    # Test coordinates (Mumbai, India)
    latitude = 19.0760
    longitude = 72.8777
    
    print(f"\n📍 Testing location: Mumbai, India")
    print(f"   Coordinates: {latitude}, {longitude}")
    print()
    
    try:
        url = "http://127.0.0.1:5000/aqi/current"
        params = {
            'lat': latitude,
            'lon': longitude
        }
        
        print("🔄 Fetching AQI data...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS - AQI Data Retrieved")
        print("=" * 60)
        
        aqi_data = data.get('data', {})
        
        # Display AQI information
        print(f"\n🌬️ Air Quality Index: {aqi_data.get('aqi')}")
        print(f"   Category: {aqi_data.get('category')}")
        print(f"   Color: {aqi_data.get('color')}")
        print(f"   Dominant Pollutant: {aqi_data.get('dominant_pollutant')}")
        
        # Display location
        location = aqi_data.get('location', {})
        print(f"\n📍 Location:")
        print(f"   City: {location.get('city')}")
        print(f"   Coordinates: {location.get('latitude')}, {location.get('longitude')}")
        
        # Display health implications
        print(f"\n💡 Health Implications:")
        print(f"   {aqi_data.get('health_implications')}")
        
        # Display cautionary statement
        if aqi_data.get('cautionary_statement') != 'None':
            print(f"\n⚠️ Cautionary Statement:")
            print(f"   {aqi_data.get('cautionary_statement')}")
        
        # Display pollutants
        pollutants = aqi_data.get('pollutants', {})
        if pollutants:
            print(f"\n📊 Pollutant Breakdown:")
            for key, pollutant in pollutants.items():
                print(f"   {pollutant['name']}: {pollutant['value']} {pollutant['unit']}")
        
        # Display update time
        print(f"\n🕐 Last Update: {aqi_data.get('last_update')}")
        
        print("\n" + "=" * 60)
        print("✅ AQI ENDPOINT TEST PASSED")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ TEST FAILED")
        print("=" * 60)
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    success = test_aqi_endpoint()
    sys.exit(0 if success else 1)
