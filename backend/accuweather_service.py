"""
AccuWeather Service - AccuWeather API Integration
Fetches real-time weather data using AccuWeather API
"""
import requests
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AccuWeatherService:
    """Service for fetching and processing weather data from AccuWeather API"""
    
    BASE_URL = "http://dataservice.accuweather.com"
    
    def __init__(self):
        self.api_key = os.getenv('ACCUWEATHER_API_KEY', 'your_api_key_here')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Climate-Sphere/1.0'
        })
    
    def get_weather_data(self, latitude: float, longitude: float, hours_back: int = 6) -> Dict[str, Any]:
        """
        Fetch comprehensive weather data from AccuWeather
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate  
            hours_back: Number of hours to look back (default: 6)
            
        Returns:
            Dictionary containing weather data and metadata organized by categories
        """
        try:
            print(f"🌤️ Fetching AccuWeather data for coordinates ({latitude}, {longitude})")
            
            # Step 1: Get location key from coordinates
            location_key = self._get_location_key(latitude, longitude)
            
            if not location_key:
                raise Exception("Unable to get location key from coordinates")
            
            # Step 2: Fetch current conditions
            current_conditions = self._fetch_current_conditions(location_key)
            
            # Step 3: Fetch hourly forecast (12 hours)
            hourly_forecast = self._fetch_hourly_forecast(location_key, hours=12)
            
            # Step 4: Fetch daily forecast (5 days)
            daily_forecast = self._fetch_daily_forecast(location_key, days=5)
            
            # Step 5: Fetch air quality index
            air_quality = self._fetch_air_quality(location_key)
            
            # Process the comprehensive data
            processed_data = self._process_accuweather_data(
                location_key, latitude, longitude,
                current_conditions, hourly_forecast, daily_forecast, air_quality,
                hours_back
            )
            
            print(f"✅ AccuWeather data fetched successfully")
            
            return processed_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ AccuWeather API error: {str(e)}")
            raise Exception(f"Failed to fetch weather data: {str(e)}")
        except Exception as e:
            print(f"❌ Weather processing error: {str(e)}")
            raise Exception(f"Failed to process weather data: {str(e)}")
    
    def _get_location_key(self, latitude: float, longitude: float) -> Optional[str]:
        """Get AccuWeather location key from coordinates"""
        try:
            url = f"{self.BASE_URL}/locations/v1/cities/geoposition/search"
            params = {
                'apikey': self.api_key,
                'q': f"{latitude},{longitude}",
                'details': 'true'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            location_key = data.get('Key')
            
            print(f"📍 Location: {data.get('LocalizedName')}, {data.get('Country', {}).get('LocalizedName')}")
            print(f"🔑 Location Key: {location_key}")
            
            return location_key
            
        except Exception as e:
            print(f"❌ Error getting location key: {str(e)}")
            return None
    
    def _fetch_current_conditions(self, location_key: str) -> Optional[Dict]:
        """Fetch current weather conditions"""
        try:
            url = f"{self.BASE_URL}/currentconditions/v1/{location_key}"
            params = {
                'apikey': self.api_key,
                'details': 'true'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            print("✅ Current conditions fetched")
            return data[0] if data else None
            
        except Exception as e:
            print(f"⚠️ Error fetching current conditions: {str(e)}")
            return None
    
    def _fetch_hourly_forecast(self, location_key: str, hours: int = 12) -> Optional[List[Dict]]:
        """Fetch hourly forecast"""
        try:
            url = f"{self.BASE_URL}/forecasts/v1/hourly/12hour/{location_key}"
            params = {
                'apikey': self.api_key,
                'details': 'true',
                'metric': 'true'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            print(f"✅ Hourly forecast fetched ({len(data)} hours)")
            return data
            
        except Exception as e:
            print(f"⚠️ Error fetching hourly forecast: {str(e)}")
            return None
    
    def _fetch_daily_forecast(self, location_key: str, days: int = 5) -> Optional[Dict]:
        """Fetch daily forecast"""
        try:
            url = f"{self.BASE_URL}/forecasts/v1/daily/5day/{location_key}"
            params = {
                'apikey': self.api_key,
                'details': 'true',
                'metric': 'true'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            print(f"✅ Daily forecast fetched ({days} days)")
            return data
            
        except Exception as e:
            print(f"⚠️ Error fetching daily forecast: {str(e)}")
            return None
    
    def _fetch_air_quality(self, location_key: str) -> Optional[Dict]:
        """Fetch air quality index"""
        try:
            url = f"{self.BASE_URL}/indices/v1/daily/1day/{location_key}"
            params = {
                'apikey': self.api_key
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            print("✅ Air quality data fetched")
            return data
            
        except Exception as e:
            print(f"⚠️ Error fetching air quality: {str(e)}")
            return None
    
    def _process_accuweather_data(self, location_key: str, latitude: float, longitude: float,
                                  current: Optional[Dict], hourly: Optional[List[Dict]], 
                                  daily: Optional[Dict], air_quality: Optional[List[Dict]],
                                  hours_back: int) -> Dict[str, Any]:
        """Process AccuWeather data into structured format"""
        
        hourly_data = []
        
        # Process current conditions
        if current:
            current_data = {
                'timestamp': current.get('LocalObservationDateTime'),
                'temperature_2m': current.get('Temperature', {}).get('Metric', {}).get('Value'),
                'apparent_temperature': current.get('RealFeelTemperature', {}).get('Metric', {}).get('Value'),
                'relative_humidity_2m': current.get('RelativeHumidity'),
                'wind_speed_10m': current.get('Wind', {}).get('Speed', {}).get('Metric', {}).get('Value'),
                'wind_direction_10m': current.get('Wind', {}).get('Direction', {}).get('Degrees'),
                'wind_gusts_10m': current.get('WindGust', {}).get('Speed', {}).get('Metric', {}).get('Value'),
                'cloud_cover': current.get('CloudCover'),
                'pressure_msl': current.get('Pressure', {}).get('Metric', {}).get('Value'),
                'visibility': current.get('Visibility', {}).get('Metric', {}).get('Value'),
                'uv_index': current.get('UVIndex'),
                'precipitation': current.get('PrecipitationSummary', {}).get('Precipitation', {}).get('Metric', {}).get('Value'),
                'is_day': current.get('IsDayTime'),
                'weather_text': current.get('WeatherText'),
                'weather_icon': current.get('WeatherIcon')
            }
            hourly_data.append(current_data)
        
        # Process hourly forecast
        if hourly:
            for hour in hourly:
                hour_data = {
                    'timestamp': hour.get('DateTime'),
                    'temperature_2m': hour.get('Temperature', {}).get('Value'),
                    'apparent_temperature': hour.get('RealFeelTemperature', {}).get('Value'),
                    'relative_humidity_2m': hour.get('RelativeHumidity'),
                    'wind_speed_10m': hour.get('Wind', {}).get('Speed', {}).get('Value'),
                    'wind_direction_10m': hour.get('Wind', {}).get('Direction', {}).get('Degrees'),
                    'wind_gusts_10m': hour.get('WindGust', {}).get('Speed', {}).get('Value'),
                    'cloud_cover': hour.get('CloudCover'),
                    'visibility': hour.get('Visibility', {}).get('Value'),
                    'uv_index': hour.get('UVIndex'),
                    'precipitation': hour.get('TotalLiquid', {}).get('Value'),
                    'rain': hour.get('Rain', {}).get('Value'),
                    'snow': hour.get('Snow', {}).get('Value'),
                    'ice': hour.get('Ice', {}).get('Value'),
                    'precipitation_probability': hour.get('PrecipitationProbability'),
                    'is_day': hour.get('IsDaylight'),
                    'weather_text': hour.get('IconPhrase'),
                    'weather_icon': hour.get('WeatherIcon')
                }
                hourly_data.append(hour_data)
        
        # Generate statistics
        stats = self._generate_accuweather_stats(hourly_data, current, daily, air_quality)
        
        # Generate insights
        insights = self._generate_accuweather_insights(hourly_data, stats, current, daily)
        
        return {
            'location': {
                'latitude': latitude,
                'longitude': longitude,
                'location_key': location_key,
                'timezone': 'auto',
                'elevation': None
            },
            'hourly_data': hourly_data,
            'statistics': stats,
            'insights': insights,
            'data_points': len(hourly_data),
            'time_range': {
                'start': hourly_data[0]['timestamp'] if hourly_data else None,
                'end': hourly_data[-1]['timestamp'] if hourly_data else None,
                'hours_covered': len(hourly_data)
            },
            'categories': {
                'atmospheric': True,
                'hydrological': True,
                'oceanic': False,
                'environmental': air_quality is not None
            },
            'timestamp': datetime.now().isoformat(),
            'source': 'AccuWeather'
        }
    
    def _generate_accuweather_stats(self, hourly_data: List[Dict], current: Optional[Dict],
                                   daily: Optional[Dict], air_quality: Optional[List[Dict]]) -> Dict[str, Any]:
        """Generate statistics from AccuWeather data"""
        
        stats = {
            'atmospheric': {},
            'hydrological': {},
            'oceanic': {},
            'environmental': {}
        }
        
        if not hourly_data:
            return stats
        
        # Extract temperature data
        temps = [h['temperature_2m'] for h in hourly_data if h.get('temperature_2m') is not None]
        if temps:
            stats['atmospheric']['temperature'] = {
                'current': temps[0],
                'min': min(temps),
                'max': max(temps),
                'avg': sum(temps) / len(temps),
                'trend': self._calculate_simple_trend(temps),
                'unit': '°C'
            }
        
        # Extract humidity data
        humidity = [h['relative_humidity_2m'] for h in hourly_data if h.get('relative_humidity_2m') is not None]
        if humidity:
            stats['atmospheric']['humidity'] = {
                'current': humidity[0],
                'min': min(humidity),
                'max': max(humidity),
                'avg': sum(humidity) / len(humidity),
                'trend': self._calculate_simple_trend(humidity),
                'unit': '%'
            }
        
        # Extract wind data
        wind_speeds = [h['wind_speed_10m'] for h in hourly_data if h.get('wind_speed_10m') is not None]
        if wind_speeds:
            stats['atmospheric']['wind_speed_10m'] = {
                'current': wind_speeds[0],
                'max': max(wind_speeds),
                'avg': sum(wind_speeds) / len(wind_speeds),
                'min': min(wind_speeds),
                'unit': 'km/h'
            }
        
        # Extract cloud cover
        clouds = [h['cloud_cover'] for h in hourly_data if h.get('cloud_cover') is not None]
        if clouds:
            stats['atmospheric']['cloud_cover'] = {
                'current': clouds[0],
                'min': min(clouds),
                'max': max(clouds),
                'avg': sum(clouds) / len(clouds),
                'unit': '%'
            }
        
        # Extract precipitation data
        precip = [h['precipitation'] for h in hourly_data if h.get('precipitation') is not None]
        if precip:
            stats['hydrological']['rainfall'] = {
                'total_mm': sum(precip),
                'max_hourly_mm': max(precip),
                'avg_hourly_mm': sum(precip) / len(precip),
                'hours_with_rain': sum(1 for p in precip if p > 0),
                'unit': 'mm/h'
            }
        
        # Extract pressure data
        pressures = [h['pressure_msl'] for h in hourly_data if h.get('pressure_msl') is not None]
        if pressures:
            stats['hydrological']['sea_level_pressure'] = {
                'current_hpa': pressures[0],
                'current_pascal': pressures[0] * 100,
                'min_hpa': min(pressures),
                'max_hpa': max(pressures),
                'avg_hpa': sum(pressures) / len(pressures),
                'trend': self._calculate_simple_trend(pressures),
                'unit_hpa': 'hPa',
                'unit_pascal': 'Pa'
            }
        
        # Air quality from indices
        if air_quality and len(air_quality) > 0:
            # Find air quality index
            for index in air_quality:
                if index.get('Name') == 'Air Quality':
                    aqi_value = index.get('Value', 0)
                    category = index.get('Category', 'Unknown')
                    
                    stats['environmental']['air_quality_index'] = {
                        'aqi': aqi_value,
                        'category': category.lower().replace(' ', '_'),
                        'description': index.get('Text', 'No description available')
                    }
                    break
        
        return stats
    
    def _calculate_simple_trend(self, data: List[float]) -> str:
        """Calculate simple trend from data"""
        if len(data) < 2:
            return "stable"
        
        first_half = sum(data[:len(data)//2]) / (len(data)//2)
        second_half = sum(data[len(data)//2:]) / (len(data) - len(data)//2)
        
        diff = second_half - first_half
        
        if diff > 0.5:
            return "increasing"
        elif diff < -0.5:
            return "decreasing"
        else:
            return "stable"
    
    def _generate_accuweather_insights(self, hourly_data: List[Dict], stats: Dict[str, Any],
                                      current: Optional[Dict], daily: Optional[Dict]) -> List[str]:
        """Generate weather insights from AccuWeather data"""
        
        insights = []
        
        # Temperature insights
        if 'temperature' in stats.get('atmospheric', {}):
            temp_stats = stats['atmospheric']['temperature']
            temp_current = temp_stats['current']
            temp_trend = temp_stats['trend']
            
            if temp_current > 35:
                insights.append(f"⚠️ Very high temperature: {temp_current:.1f}°C - Heat wave conditions")
            elif temp_current > 30:
                insights.append(f"🌡️ High temperature: {temp_current:.1f}°C - Stay hydrated")
            elif temp_current < 0:
                insights.append(f"❄️ Freezing temperature: {temp_current:.1f}°C - Risk of ice formation")
            
            if temp_trend == "increasing":
                insights.append(f"📈 Temperature is rising (currently {temp_current:.1f}°C)")
            elif temp_trend == "decreasing":
                insights.append(f"📉 Temperature is falling (currently {temp_current:.1f}°C)")
        
        # Humidity insights
        if 'humidity' in stats.get('atmospheric', {}):
            humidity = stats['atmospheric']['humidity']['current']
            if humidity > 80:
                insights.append(f"💧 Very high humidity: {humidity:.0f}% - Uncomfortable conditions")
            elif humidity < 30:
                insights.append(f"🏜️ Low humidity: {humidity:.0f}% - Dry air conditions")
        
        # Wind insights
        if 'wind_speed_10m' in stats.get('atmospheric', {}):
            wind_speed = stats['atmospheric']['wind_speed_10m']['current']
            if wind_speed > 50:
                insights.append(f"💨 Strong winds: {wind_speed:.1f} km/h - Hazardous conditions")
            elif wind_speed > 30:
                insights.append(f"🌬️ Moderate winds: {wind_speed:.1f} km/h - Windy conditions")
        
        # Precipitation insights
        if 'rainfall' in stats.get('hydrological', {}):
            total_rain = stats['hydrological']['rainfall']['total_mm']
            if total_rain > 50:
                insights.append(f"🌧️ Heavy rainfall expected: {total_rain:.1f}mm total")
            elif total_rain > 10:
                insights.append(f"☔ Moderate rainfall expected: {total_rain:.1f}mm total")
            elif total_rain > 0:
                insights.append(f"🌦️ Light rainfall expected: {total_rain:.1f}mm total")
        
        # Current weather text
        if current and current.get('WeatherText'):
            insights.append(f"🌤️ Current conditions: {current['WeatherText']}")
        
        # Air quality insights
        if 'air_quality_index' in stats.get('environmental', {}):
            aqi_data = stats['environmental']['air_quality_index']
            category = aqi_data['category']
            
            if category == 'hazardous':
                insights.append(f"🚨 Hazardous air quality - Stay indoors")
            elif category == 'unhealthy':
                insights.append(f"⚠️ Unhealthy air quality - Limit outdoor activities")
            elif category == 'moderate':
                insights.append(f"😐 Moderate air quality - Sensitive groups should be cautious")
            elif category == 'good':
                insights.append(f"✅ Good air quality - Safe for outdoor activities")
        
        return insights


# Alias for backward compatibility
WeatherService = AccuWeatherService
