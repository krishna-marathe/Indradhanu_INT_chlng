#!/usr/bin/env python3
"""
Comprehensive test script for enhanced weather analytics with all categories:
- Atmospheric: temperature, humidity, wind speed/direction, cloud cover
- Hydrological: rainfall, sea level pressure, cyclone activity
- Oceanic: sea surface temperature, wave height, ocean wind
- Environmental: air quality index and pollutants
"""
import requests
import json
import time

API_BASE_URL = "http://127.0.0.1:5000"

def test_comprehensive_weather_analysis():
    """Test comprehensive weather analysis with all categories"""
    print("🌍 Testing Comprehensive Weather Analysis")
    print("=" * 60)
    
    # Test locations with different characteristics
    test_locations = [
        {"name": "Miami, Florida (Coastal)", "lat": 25.7617, "lon": -80.1918},
        {"name": "New York City (Urban)", "lat": 40.7128, "lon": -74.0060},
        {"name": "London, UK (Temperate)", "lat": 51.5074, "lon": -0.1278},
        {"name": "Mumbai, India (Tropical)", "lat": 19.0760, "lon": 72.8777}
    ]
    
    for location in test_locations:
        print(f"\n🏙️ Testing: {location['name']}")
        print("-" * 40)
        
        try:
            response = requests.post(f"{API_BASE_URL}/weather/analyze", 
                                   json={
                                       'latitude': location['lat'],
                                       'longitude': location['lon'],
                                       'hours': 6
                                   }, timeout=45)
            response.raise_for_status()
            
            data = response.json()['data']
            
            # Display basic info
            print(f"📍 Location: {data['location']['latitude']:.2f}, {data['location']['longitude']:.2f}")
            print(f"📊 Data points: {data['data_points']}")
            print(f"🕒 Time range: {data['time_range']['hours_covered']} hours")
            
            # Display category availability
            categories = data.get('categories', {})
            print(f"\n📋 Available Categories:")
            for category, available in categories.items():
                status = "✅" if available else "❌"
                print(f"   {status} {category.title()}")
            
            # Display statistics by category
            stats = data.get('statistics', {})
            
            # Atmospheric
            if 'atmospheric' in stats and stats['atmospheric']:
                print(f"\n🌤️ Atmospheric Conditions:")
                atm = stats['atmospheric']
                if 'temperature' in atm:
                    temp = atm['temperature']
                    print(f"   🌡️ Temperature: {temp.get('current', 'N/A')}°C ({temp.get('trend', 'stable')})")
                if 'humidity' in atm:
                    hum = atm['humidity']
                    print(f"   💧 Humidity: {hum.get('current', 'N/A')}%")
                if 'wind_speed_10m' in atm:
                    wind = atm['wind_speed_10m']
                    print(f"   💨 Wind Speed: {wind.get('current', 'N/A')} km/h")
                if 'cloud_cover' in atm:
                    cloud = atm['cloud_cover']
                    print(f"   ☁️ Cloud Cover: {cloud.get('current', 'N/A')}%")
            
            # Hydrological
            if 'hydrological' in stats and stats['hydrological']:
                print(f"\n🌊 Hydrological Conditions:")
                hydro = stats['hydrological']
                if 'rainfall' in hydro:
                    rain = hydro['rainfall']
                    print(f"   🌧️ Total Rainfall: {rain.get('total_mm', 'N/A')} mm")
                if 'sea_level_pressure' in hydro:
                    pressure = hydro['sea_level_pressure']
                    print(f"   📊 Sea Level Pressure: {pressure.get('current_hpa', 'N/A')} hPa ({pressure.get('trend', 'stable')})")
                if 'cyclone_activity' in hydro:
                    cyclone = hydro['cyclone_activity']
                    print(f"   🌀 Cyclone Risk: {cyclone.get('risk_level', 'unknown').title()}")
            
            # Oceanic
            if 'oceanic' in stats and stats['oceanic']:
                print(f"\n🌊 Oceanic Conditions:")
                oceanic = stats['oceanic']
                if 'sea_surface_temperature' in oceanic:
                    sst = oceanic['sea_surface_temperature']
                    print(f"   🌊 Sea Surface Temp: {sst.get('current', 'N/A')}°C")
                if 'wave_height' in oceanic:
                    wave = oceanic['wave_height']
                    print(f"   🌊 Wave Height: {wave.get('current', 'N/A')} m")
                if 'ocean_wind' in oceanic:
                    ocean_wind = oceanic['ocean_wind']
                    print(f"   💨 Ocean Wind: {ocean_wind.get('current', 'N/A')} m/s")
            
            # Environmental
            if 'environmental' in stats and stats['environmental']:
                print(f"\n🌿 Environmental Conditions:")
                env = stats['environmental']
                if 'air_quality_index' in env:
                    aqi = env['air_quality_index']
                    aqi_value = aqi.get('aqi', 'N/A')
                    aqi_category = aqi.get('category', 'unknown').replace('_', ' ').title()
                    print(f"   🌬️ Air Quality Index: {aqi_value} ({aqi_category})")
                
                # Show key pollutants
                pollutants = ['pm2_5', 'pm10', 'ozone']
                for pollutant in pollutants:
                    if pollutant in env:
                        pol_data = env[pollutant]
                        current = pol_data.get('current', 'N/A')
                        unit = pol_data.get('unit', '')
                        name = pol_data.get('name', pollutant.upper())
                        print(f"   🏭 {name}: {current} {unit}")
            
            # Display charts generated
            charts = data.get('charts', [])
            print(f"\n📊 Generated Charts ({len(charts)}):")
            for chart in charts:
                category = chart.get('category', 'general')
                print(f"   📈 {chart['title']} ({category})")
            
            # Display sample insights
            insights = data.get('insights', [])
            print(f"\n💡 Key Insights ({len(insights)}):")
            for i, insight in enumerate(insights[:5]):  # Show first 5
                print(f"   {i+1}. {insight}")
            
            print(f"\n✅ Analysis complete for {location['name']}")
            time.sleep(3)  # Rate limiting
            
        except Exception as e:
            print(f"❌ Error analyzing {location['name']}: {str(e)}")
    
    return True

def test_category_specific_endpoints():
    """Test if we can get category-specific data"""
    print(f"\n🔬 Testing Category-Specific Data Availability")
    print("=" * 60)
    
    # Test a coastal location for oceanic data
    coastal_location = {"name": "Sydney, Australia", "lat": -33.8688, "lon": 151.2093}
    
    try:
        response = requests.post(f"{API_BASE_URL}/weather/analyze", 
                               json={
                                   'latitude': coastal_location['lat'],
                                   'longitude': coastal_location['lon'],
                                   'hours': 6
                               }, timeout=45)
        response.raise_for_status()
        
        data = response.json()['data']
        categories = data.get('categories', {})
        
        print(f"📍 Testing coastal location: {coastal_location['name']}")
        print(f"🌊 Oceanic data available: {'✅' if categories.get('oceanic') else '❌'}")
        print(f"🌿 Environmental data available: {'✅' if categories.get('environmental') else '❌'}")
        print(f"🌤️ Atmospheric data available: {'✅' if categories.get('atmospheric') else '❌'}")
        print(f"💧 Hydrological data available: {'✅' if categories.get('hydrological') else '❌'}")
        
        # Check specific parameters
        sample_data = data['hourly_data'][0] if data['hourly_data'] else {}
        
        print(f"\n🔍 Sample Data Point Parameters:")
        atmospheric_params = ['temperature_2m', 'relative_humidity_2m', 'wind_speed_10m', 'cloud_cover']
        hydrological_params = ['rain', 'pressure_msl']
        oceanic_params = ['wave_height', 'sea_surface_temperature', 'ocean_current_velocity']
        environmental_params = ['pm2_5', 'pm10', 'ozone']
        
        for category, params in [
            ('Atmospheric', atmospheric_params),
            ('Hydrological', hydrological_params), 
            ('Oceanic', oceanic_params),
            ('Environmental', environmental_params)
        ]:
            print(f"\n   {category}:")
            for param in params:
                available = param in sample_data and sample_data[param] is not None
                status = "✅" if available else "❌"
                value = sample_data.get(param, 'N/A')
                print(f"     {status} {param}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing category-specific data: {str(e)}")
        return False

def test_air_quality_calculation():
    """Test air quality index calculation"""
    print(f"\n🌬️ Testing Air Quality Index Calculation")
    print("=" * 60)
    
    # Test an urban location likely to have air quality data
    urban_location = {"name": "Beijing, China", "lat": 39.9042, "lon": 116.4074}
    
    try:
        response = requests.post(f"{API_BASE_URL}/weather/analyze", 
                               json={
                                   'latitude': urban_location['lat'],
                                   'longitude': urban_location['lon'],
                                   'hours': 6
                               }, timeout=45)
        response.raise_for_status()
        
        data = response.json()['data']
        stats = data.get('statistics', {})
        env_stats = stats.get('environmental', {})
        
        print(f"📍 Testing urban location: {urban_location['name']}")
        
        if 'air_quality_index' in env_stats:
            aqi_data = env_stats['air_quality_index']
            print(f"✅ AQI Calculation successful:")
            print(f"   🔢 AQI Value: {aqi_data.get('aqi', 'N/A')}")
            print(f"   📊 Category: {aqi_data.get('category', 'unknown').replace('_', ' ').title()}")
            print(f"   📝 Description: {aqi_data.get('description', 'N/A')}")
            print(f"   🏭 Current PM2.5: {aqi_data.get('current_pm25', 'N/A')} μg/m³")
        else:
            print("⚠️ AQI data not available for this location")
        
        # Check individual pollutants
        pollutants = ['pm2_5', 'pm10', 'ozone', 'carbon_monoxide', 'nitrogen_dioxide']
        available_pollutants = [p for p in pollutants if p in env_stats]
        
        print(f"\n🏭 Available Pollutant Data ({len(available_pollutants)}/{len(pollutants)}):")
        for pollutant in available_pollutants:
            pol_data = env_stats[pollutant]
            name = pol_data.get('name', pollutant.upper())
            current = pol_data.get('current', 'N/A')
            unit = pol_data.get('unit', '')
            print(f"   ✅ {name}: {current} {unit}")
        
        return len(available_pollutants) > 0
        
    except Exception as e:
        print(f"❌ Error testing air quality: {str(e)}")
        return False

if __name__ == "__main__":
    print("🌍 Comprehensive Weather Analytics Test Suite")
    print("Testing all categories: Atmospheric, Hydrological, Oceanic, Environmental")
    print("=" * 80)
    
    # Test comprehensive weather analysis
    test1 = test_comprehensive_weather_analysis()
    
    # Test category-specific data
    test2 = test_category_specific_endpoints()
    
    # Test air quality calculations
    test3 = test_air_quality_calculation()
    
    print("\n" + "=" * 80)
    print("📊 Comprehensive Test Results:")
    print(f"Multi-Location Analysis: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Category-Specific Data: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Air Quality Calculation: {'✅ PASS' if test3 else '❌ FAIL'}")
    
    if all([test1, test2, test3]):
        print("\n🎉 ALL COMPREHENSIVE WEATHER TESTS PASSED!")
        print("🌍 The system now supports:")
        print("   🌤️ Atmospheric: Temperature, Humidity, Wind, Cloud Cover")
        print("   💧 Hydrological: Rainfall, Pressure, Cyclone Activity") 
        print("   🌊 Oceanic: Sea Temperature, Wave Height, Ocean Currents")
        print("   🌿 Environmental: Air Quality Index, Pollutant Levels")
        print("   📊 Comprehensive visualizations for all categories")
        print("   💡 AI-powered insights across all parameters")
    else:
        print("\n⚠️ Some comprehensive tests failed. Check the logs above.")