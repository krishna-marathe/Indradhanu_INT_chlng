"""
Test AccuWeather API Integration
"""
import sys
sys.path.append('backend')

from accuweather_service import AccuWeatherService

def test_accuweather():
    print("=" * 60)
    print("ACCUWEATHER API TEST")
    print("=" * 60)
    
    # Test coordinates (Mumbai, India)
    latitude = 19.0760
    longitude = 72.8777
    
    print(f"\n📍 Testing location: Mumbai, India")
    print(f"   Coordinates: {latitude}, {longitude}")
    print()
    
    try:
        service = AccuWeatherService()
        
        print("🔄 Fetching weather data...")
        weather_data = service.get_weather_data(latitude, longitude, hours_back=6)
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS - Weather Data Retrieved")
        print("=" * 60)
        
        # Display location info
        print(f"\n📍 Location Information:")
        print(f"   Latitude: {weather_data['location']['latitude']}")
        print(f"   Longitude: {weather_data['location']['longitude']}")
        print(f"   Location Key: {weather_data['location']['location_key']}")
        print(f"   Source: {weather_data.get('source', 'Unknown')}")
        
        # Display data points
        print(f"\n📊 Data Points: {weather_data['data_points']}")
        print(f"   Time Range: {weather_data['time_range']['start']} to {weather_data['time_range']['end']}")
        
        # Display atmospheric statistics
        if 'atmospheric' in weather_data['statistics']:
            print(f"\n🌤️ Atmospheric Conditions:")
            atm = weather_data['statistics']['atmospheric']
            
            if 'temperature' in atm:
                temp = atm['temperature']
                print(f"   Temperature: {temp['current']:.1f}°C (Min: {temp['min']:.1f}°C, Max: {temp['max']:.1f}°C)")
                print(f"   Trend: {temp['trend']}")
            
            if 'humidity' in atm:
                hum = atm['humidity']
                print(f"   Humidity: {hum['current']:.0f}% (Min: {hum['min']:.0f}%, Max: {hum['max']:.0f}%)")
            
            if 'wind_speed_10m' in atm:
                wind = atm['wind_speed_10m']
                print(f"   Wind Speed: {wind['current']:.1f} km/h (Max: {wind['max']:.1f} km/h)")
            
            if 'cloud_cover' in atm:
                cloud = atm['cloud_cover']
                print(f"   Cloud Cover: {cloud['current']:.0f}%")
        
        # Display hydrological statistics
        if 'hydrological' in weather_data['statistics']:
            print(f"\n💧 Hydrological Conditions:")
            hydro = weather_data['statistics']['hydrological']
            
            if 'rainfall' in hydro:
                rain = hydro['rainfall']
                print(f"   Total Rainfall: {rain['total_mm']:.1f} mm")
                print(f"   Hours with Rain: {rain['hours_with_rain']}")
            
            if 'sea_level_pressure' in hydro:
                pressure = hydro['sea_level_pressure']
                print(f"   Sea Level Pressure: {pressure['current_hpa']:.0f} hPa")
                print(f"   Trend: {pressure['trend']}")
        
        # Display environmental statistics
        if 'environmental' in weather_data['statistics'] and weather_data['statistics']['environmental']:
            print(f"\n🌿 Environmental Quality:")
            env = weather_data['statistics']['environmental']
            
            if 'air_quality_index' in env:
                aqi = env['air_quality_index']
                print(f"   Air Quality Index: {aqi.get('aqi', 'N/A')}")
                print(f"   Category: {aqi.get('category', 'Unknown').replace('_', ' ').title()}")
                print(f"   Description: {aqi.get('description', 'No description')}")
        
        # Display insights
        if weather_data['insights']:
            print(f"\n💡 Weather Insights ({len(weather_data['insights'])}):")
            for i, insight in enumerate(weather_data['insights'][:5], 1):
                print(f"   {i}. {insight}")
        
        print("\n" + "=" * 60)
        print("✅ ACCUWEATHER INTEGRATION TEST PASSED")
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
    success = test_accuweather()
    sys.exit(0 if success else 1)
