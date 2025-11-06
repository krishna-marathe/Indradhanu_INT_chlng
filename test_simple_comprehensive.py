#!/usr/bin/env python3
"""
Simple test for comprehensive weather data
"""
import requests
import json

API_BASE_URL = "http://127.0.0.1:5000"

def test_comprehensive_weather():
    """Test comprehensive weather analysis"""
    print("🌍 Testing Comprehensive Weather Analysis")
    print("=" * 50)
    
    try:
        response = requests.post(f"{API_BASE_URL}/weather/analyze", 
                               json={
                                   'latitude': 40.7128,
                                   'longitude': -74.0060,
                                   'hours': 6
                               }, timeout=30)
        response.raise_for_status()
        
        data = response.json()['data']
        
        print(f"📍 Location: New York City")
        print(f"📊 Data points: {data['data_points']}")
        
        # Check categories
        categories = data.get('categories', {})
        print(f"\n📋 Available Categories:")
        for category, available in categories.items():
            status = "✅" if available else "❌"
            print(f"   {status} {category.title()}")
        
        # Check statistics
        stats = data.get('statistics', {})
        print(f"\n📈 Statistics Available:")
        for category, cat_stats in stats.items():
            if cat_stats:
                print(f"   ✅ {category.title()}: {len(cat_stats)} parameters")
                # Show sample parameters
                for param_name in list(cat_stats.keys())[:3]:
                    param_data = cat_stats[param_name]
                    if isinstance(param_data, dict) and 'current' in param_data:
                        current = param_data['current']
                        unit = param_data.get('unit', '')
                        print(f"      • {param_name}: {current} {unit}")
            else:
                print(f"   ❌ {category.title()}: No data")
        
        # Check charts
        charts = data.get('charts', [])
        print(f"\n📊 Generated Charts ({len(charts)}):")
        for chart in charts:
            category = chart.get('category', 'general')
            print(f"   📈 {chart['title']} ({category})")
        
        # Check insights
        insights = data.get('insights', [])
        print(f"\n💡 Generated Insights ({len(insights)}):")
        for i, insight in enumerate(insights[:5]):
            print(f"   {i+1}. {insight}")
        
        # Check sample data point
        if data['hourly_data']:
            sample = data['hourly_data'][0]
            print(f"\n🔍 Sample Data Point Parameters:")
            param_count = len([k for k, v in sample.items() if v is not None and k != 'timestamp'])
            print(f"   📊 Total parameters with data: {param_count}")
            
            # Show atmospheric parameters
            atm_params = ['temperature_2m', 'relative_humidity_2m', 'wind_speed_10m', 'cloud_cover']
            print(f"   🌤️ Atmospheric:")
            for param in atm_params:
                if param in sample and sample[param] is not None:
                    print(f"      ✅ {param}: {sample[param]}")
                else:
                    print(f"      ❌ {param}: Not available")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_comprehensive_weather()
    
    if success:
        print(f"\n🎉 Comprehensive weather analysis is working!")
    else:
        print(f"\n❌ Test failed")