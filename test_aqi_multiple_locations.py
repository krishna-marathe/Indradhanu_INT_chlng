"""
Test AQI Endpoint with Multiple Locations
"""
import requests
import json

def test_location(name, latitude, longitude):
    """Test AQI for a specific location"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"Coordinates: {latitude}, {longitude}")
    print('='*60)
    
    try:
        url = "http://127.0.0.1:5000/aqi/current"
        params = {'lat': latitude, 'lon': longitude}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        aqi_data = data.get('data', {})
        
        print(f"\n✅ AQI: {aqi_data.get('aqi')} ({aqi_data.get('category')})")
        print(f"📍 Location: {aqi_data.get('location', {}).get('city')}")
        
        station_name = aqi_data.get('location', {}).get('station_name')
        station_distance = aqi_data.get('location', {}).get('station_distance_km')
        
        if station_name:
            print(f"🔬 Monitoring Station: {station_name}")
            if station_distance and station_distance > 0:
                print(f"   Distance: {station_distance} km away")
        
        print(f"🔬 Dominant Pollutant: {aqi_data.get('dominant_pollutant')}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("AQI MULTIPLE LOCATIONS TEST")
    print("=" * 60)
    
    # Test various locations
    locations = [
        ("Mumbai, India", 19.0760, 72.8777),
        ("Delhi, India", 28.6139, 77.2090),
        ("New York, USA", 40.7128, -74.0060),
        ("London, UK", 51.5074, -0.1278),
        ("Tokyo, Japan", 35.6762, 139.6503),
        ("Sydney, Australia", -33.8688, 151.2093),
        ("Paris, France", 48.8566, 2.3522),
        ("Berlin, Germany", 52.5200, 13.4050)
    ]
    
    results = []
    for name, lat, lon in locations:
        success = test_location(name, lat, lon)
        results.append((name, success))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} passed")
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
