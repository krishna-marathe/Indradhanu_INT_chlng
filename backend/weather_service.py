"""
Weather Service - Open-Meteo API Integration
Fetches real-time weather data for the past 6 hours
"""
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import numpy as np


class WeatherService:
    """Service for fetching and processing weather data from Open-Meteo API"""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Indradhanu-Analytics/1.0'
        })
    
    def get_weather_data(self, latitude: float, longitude: float, hours_back: int = 6) -> Dict[str, Any]:
        """
        Fetch comprehensive weather data for the past N hours
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate  
            hours_back: Number of hours to look back (default: 6)
            
        Returns:
            Dictionary containing weather data and metadata organized by categories
        """
        try:
            # Calculate time range
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=hours_back)
            
            # Format dates for API
            start_date = start_time.strftime('%Y-%m-%d')
            end_date = end_time.strftime('%Y-%m-%d')
            
            # Reliable API parameters organized by categories
            hourly_params = [
                # Core Atmospheric Parameters
                'temperature_2m',           # Temperature (°C)
                'relative_humidity_2m',     # Humidity (%)
                'wind_speed_10m',          # Wind speed at 10m (km/h)
                'wind_direction_10m',      # Wind direction at 10m (°)
                'cloud_cover',             # Cloud cover (%)
                
                # Hydrological Parameters
                'rain',                    # Rainfall (mm/h)
                'precipitation',           # Total precipitation (mm/h)
                'pressure_msl',           # Sea level pressure (hPa)
                
                # Additional Atmospheric (if available)
                'apparent_temperature',    # Feels like temperature (°C)
                'wind_gusts_10m',         # Wind gusts (km/h)
                'uv_index'               # UV Index
            ]
            
            # Marine parameters (if available for coastal areas)
            marine_params = [
                'wave_height',            # Wave height (m)
                'wave_direction',         # Wave direction (°)
                'wave_period',           # Wave period (s)
                'swell_wave_height',     # Swell wave height (m)
                'swell_wave_direction',  # Swell wave direction (°)
                'swell_wave_period'      # Swell wave period (s)
            ]
            
            # API parameters
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'hourly': ','.join(hourly_params),
                'start_date': start_date,
                'end_date': end_date,
                'timezone': 'auto',
                'models': 'best_match'  # Use best available model
            }
            
            print(f"🌤️ Fetching comprehensive weather data for coordinates ({latitude}, {longitude})")
            
            # Make primary API request
            response = self.session.get(self.BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            # Try to get marine data if location is coastal
            marine_data = None
            if self._is_coastal_location(latitude, longitude):
                marine_data = self._fetch_marine_data(latitude, longitude, start_date, end_date)
            
            # Try to get air quality data
            air_quality_data = self._fetch_air_quality_data(latitude, longitude, start_date, end_date)
            
            # Process the comprehensive data
            processed_data = self._process_comprehensive_weather_data(
                data, marine_data, air_quality_data, hours_back
            )
            
            print(f"✅ Comprehensive weather data fetched: {len(processed_data['hourly_data'])} data points")
            
            return processed_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Weather API error: {str(e)}")
            raise Exception(f"Failed to fetch weather data: {str(e)}")
        except Exception as e:
            print(f"❌ Weather processing error: {str(e)}")
            raise Exception(f"Failed to process weather data: {str(e)}")
    
    def _is_coastal_location(self, latitude: float, longitude: float) -> bool:
        """Check if location is coastal (simplified heuristic)"""
        # This is a simplified check - in production, you'd use a proper coastline database
        # For now, we'll try to fetch marine data for all locations and handle errors gracefully
        return True
    
    def _fetch_marine_data(self, latitude: float, longitude: float, start_date: str, end_date: str) -> Optional[Dict]:
        """Fetch marine/oceanic data"""
        try:
            marine_url = "https://marine-api.open-meteo.com/v1/marine"
            marine_params = {
                'latitude': latitude,
                'longitude': longitude,
                'hourly': 'wave_height,wave_direction,wave_period,swell_wave_height,swell_wave_direction,swell_wave_period,ocean_current_velocity,ocean_current_direction,sea_surface_temperature',
                'start_date': start_date,
                'end_date': end_date,
                'timezone': 'auto'
            }
            
            response = self.session.get(marine_url, params=marine_params, timeout=10)
            if response.status_code == 200:
                print("🌊 Marine data fetched successfully")
                return response.json()
            else:
                print("⚠️ Marine data not available for this location")
                return None
                
        except Exception as e:
            print(f"⚠️ Marine data fetch failed: {str(e)}")
            return None
    
    def _fetch_air_quality_data(self, latitude: float, longitude: float, start_date: str, end_date: str) -> Optional[Dict]:
        """Fetch air quality data"""
        try:
            air_quality_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
            air_quality_params = {
                'latitude': latitude,
                'longitude': longitude,
                'hourly': 'pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,aerosol_optical_depth,dust,uv_index,ammonia',
                'start_date': start_date,
                'end_date': end_date,
                'timezone': 'auto'
            }
            
            response = self.session.get(air_quality_url, params=air_quality_params, timeout=10)
            if response.status_code == 200:
                print("🌬️ Air quality data fetched successfully")
                return response.json()
            else:
                print("⚠️ Air quality data not available for this location")
                return None
                
        except Exception as e:
            print(f"⚠️ Air quality data fetch failed: {str(e)}")
            return None
    
    def _process_comprehensive_weather_data(self, raw_data: Dict, marine_data: Optional[Dict], 
                                          air_quality_data: Optional[Dict], hours_back: int) -> Dict[str, Any]:
        """Process comprehensive weather data into structured format organized by categories"""
        
        hourly = raw_data.get('hourly', {})
        
        # Extract time series data
        times = hourly.get('time', [])
        
        # Filter to last N hours
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(hours=hours_back)
        
        filtered_data = []
        for i, time_str in enumerate(times):
            time_obj = datetime.fromisoformat(time_str.replace('T', ' '))
            
            if time_obj >= cutoff_time:
                data_point = {'timestamp': time_str}
                
                # Atmospheric Parameters
                data_point.update({
                    'temperature_2m': self._safe_get(hourly.get('temperature_2m', []), i),
                    'relative_humidity_2m': self._safe_get(hourly.get('relative_humidity_2m', []), i),
                    'wind_speed_10m': self._safe_get(hourly.get('wind_speed_10m', []), i),
                    'wind_speed_80m': self._safe_get(hourly.get('wind_speed_80m', []), i),
                    'wind_direction_10m': self._safe_get(hourly.get('wind_direction_10m', []), i),
                    'wind_direction_80m': self._safe_get(hourly.get('wind_direction_80m', []), i),
                    'cloud_cover': self._safe_get(hourly.get('cloud_cover', []), i),
                    'dew_point_2m': self._safe_get(hourly.get('dew_point_2m', []), i),
                    'apparent_temperature': self._safe_get(hourly.get('apparent_temperature', []), i),
                    'wind_gusts_10m': self._safe_get(hourly.get('wind_gusts_10m', []), i),
                    'visibility': self._safe_get(hourly.get('visibility', []), i),
                    'uv_index': self._safe_get(hourly.get('uv_index', []), i),
                    'is_day': self._safe_get(hourly.get('is_day', []), i)
                })
                
                # Hydrological Parameters
                data_point.update({
                    'rain': self._safe_get(hourly.get('rain', []), i),
                    'precipitation': self._safe_get(hourly.get('precipitation', []), i),
                    'snowfall': self._safe_get(hourly.get('snowfall', []), i)
                })
                
                # Pressure Parameters
                data_point.update({
                    'pressure_msl': self._safe_get(hourly.get('pressure_msl', []), i),
                    'surface_pressure': self._safe_get(hourly.get('surface_pressure', []), i)
                })
                
                filtered_data.append(data_point)
        
        # Add marine data if available
        if marine_data:
            filtered_data = self._merge_marine_data(filtered_data, marine_data, cutoff_time)
        
        # Add air quality data if available
        if air_quality_data:
            filtered_data = self._merge_air_quality_data(filtered_data, air_quality_data, cutoff_time)
        
        # Create DataFrame for analysis
        df = pd.DataFrame(filtered_data)
        
        # Generate comprehensive statistics by category
        stats = self._generate_comprehensive_stats(df)
        
        # Generate comprehensive insights
        insights = self._generate_comprehensive_insights(df, stats)
        
        return {
            'location': {
                'latitude': raw_data.get('latitude'),
                'longitude': raw_data.get('longitude'),
                'timezone': raw_data.get('timezone'),
                'elevation': raw_data.get('elevation')
            },
            'hourly_data': filtered_data,
            'statistics': stats,
            'insights': insights,
            'data_points': len(filtered_data),
            'time_range': {
                'start': filtered_data[0]['timestamp'] if filtered_data else None,
                'end': filtered_data[-1]['timestamp'] if filtered_data else None,
                'hours_covered': hours_back
            },
            'categories': {
                'atmospheric': self._has_atmospheric_data(df),
                'hydrological': self._has_hydrological_data(df),
                'oceanic': self._has_oceanic_data(df),
                'environmental': self._has_environmental_data(df)
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def _safe_get(self, data_list: List, index: int):
        """Safely get item from list"""
        return data_list[index] if index < len(data_list) else None
    
    def _merge_marine_data(self, filtered_data: List[Dict], marine_data: Dict, cutoff_time: datetime) -> List[Dict]:
        """Merge marine data with weather data"""
        try:
            marine_hourly = marine_data.get('hourly', {})
            marine_times = marine_hourly.get('time', [])
            
            # Create a mapping of timestamps to marine data
            marine_map = {}
            for i, time_str in enumerate(marine_times):
                time_obj = datetime.fromisoformat(time_str.replace('T', ' '))
                if time_obj >= cutoff_time:
                    marine_map[time_str] = {
                        'wave_height': self._safe_get(marine_hourly.get('wave_height', []), i),
                        'wave_direction': self._safe_get(marine_hourly.get('wave_direction', []), i),
                        'wave_period': self._safe_get(marine_hourly.get('wave_period', []), i),
                        'swell_wave_height': self._safe_get(marine_hourly.get('swell_wave_height', []), i),
                        'swell_wave_direction': self._safe_get(marine_hourly.get('swell_wave_direction', []), i),
                        'swell_wave_period': self._safe_get(marine_hourly.get('swell_wave_period', []), i),
                        'ocean_current_velocity': self._safe_get(marine_hourly.get('ocean_current_velocity', []), i),
                        'ocean_current_direction': self._safe_get(marine_hourly.get('ocean_current_direction', []), i),
                        'sea_surface_temperature': self._safe_get(marine_hourly.get('sea_surface_temperature', []), i)
                    }
            
            # Merge marine data with weather data
            for data_point in filtered_data:
                timestamp = data_point['timestamp']
                if timestamp in marine_map:
                    data_point.update(marine_map[timestamp])
            
            return filtered_data
            
        except Exception as e:
            print(f"⚠️ Error merging marine data: {str(e)}")
            return filtered_data
    
    def _merge_air_quality_data(self, filtered_data: List[Dict], air_quality_data: Dict, cutoff_time: datetime) -> List[Dict]:
        """Merge air quality data with weather data"""
        try:
            aq_hourly = air_quality_data.get('hourly', {})
            aq_times = aq_hourly.get('time', [])
            
            # Create a mapping of timestamps to air quality data
            aq_map = {}
            for i, time_str in enumerate(aq_times):
                time_obj = datetime.fromisoformat(time_str.replace('T', ' '))
                if time_obj >= cutoff_time:
                    aq_map[time_str] = {
                        'pm10': self._safe_get(aq_hourly.get('pm10', []), i),
                        'pm2_5': self._safe_get(aq_hourly.get('pm2_5', []), i),
                        'carbon_monoxide': self._safe_get(aq_hourly.get('carbon_monoxide', []), i),
                        'nitrogen_dioxide': self._safe_get(aq_hourly.get('nitrogen_dioxide', []), i),
                        'sulphur_dioxide': self._safe_get(aq_hourly.get('sulphur_dioxide', []), i),
                        'ozone': self._safe_get(aq_hourly.get('ozone', []), i),
                        'aerosol_optical_depth': self._safe_get(aq_hourly.get('aerosol_optical_depth', []), i),
                        'dust': self._safe_get(aq_hourly.get('dust', []), i),
                        'ammonia': self._safe_get(aq_hourly.get('ammonia', []), i)
                    }
            
            # Merge air quality data with weather data
            for data_point in filtered_data:
                timestamp = data_point['timestamp']
                if timestamp in aq_map:
                    data_point.update(aq_map[timestamp])
            
            return filtered_data
            
        except Exception as e:
            print(f"⚠️ Error merging air quality data: {str(e)}")
            return filtered_data
    
    def _has_atmospheric_data(self, df: pd.DataFrame) -> bool:
        """Check if atmospheric data is available"""
        atmospheric_cols = ['temperature_2m', 'relative_humidity_2m', 'wind_speed_10m', 'cloud_cover']
        return any(col in df.columns and not df[col].isna().all() for col in atmospheric_cols)
    
    def _has_hydrological_data(self, df: pd.DataFrame) -> bool:
        """Check if hydrological data is available"""
        hydro_cols = ['rain', 'precipitation', 'snowfall']
        return any(col in df.columns and not df[col].isna().all() for col in hydro_cols)
    
    def _has_oceanic_data(self, df: pd.DataFrame) -> bool:
        """Check if oceanic data is available"""
        oceanic_cols = ['wave_height', 'sea_surface_temperature', 'ocean_current_velocity']
        return any(col in df.columns and not df[col].isna().all() for col in oceanic_cols)
    
    def _has_environmental_data(self, df: pd.DataFrame) -> bool:
        """Check if environmental data is available"""
        env_cols = ['pm10', 'pm2_5', 'ozone', 'carbon_monoxide']
        return any(col in df.columns and not df[col].isna().all() for col in env_cols)
    
    def _generate_comprehensive_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive statistical summary organized by categories"""
        
        if df.empty:
            return {}
        
        stats = {
            'atmospheric': {},
            'hydrological': {},
            'oceanic': {},
            'environmental': {}
        }
        
        # ATMOSPHERIC PARAMETERS
        # Temperature
        if 'temperature_2m' in df.columns and not df['temperature_2m'].isna().all():
            temp_data = df['temperature_2m'].dropna()
            stats['atmospheric']['temperature'] = {
                'current': float(temp_data.iloc[-1]) if not temp_data.empty else None,
                'min': float(temp_data.min()),
                'max': float(temp_data.max()),
                'avg': float(temp_data.mean()),
                'trend': self._calculate_trend(temp_data),
                'unit': '°C'
            }
        
        # Humidity
        if 'relative_humidity_2m' in df.columns and not df['relative_humidity_2m'].isna().all():
            humidity_data = df['relative_humidity_2m'].dropna()
            stats['atmospheric']['humidity'] = {
                'current': float(humidity_data.iloc[-1]) if not humidity_data.empty else None,
                'min': float(humidity_data.min()),
                'max': float(humidity_data.max()),
                'avg': float(humidity_data.mean()),
                'trend': self._calculate_trend(humidity_data),
                'unit': '%'
            }
        
        # Wind Speed and Direction
        wind_cols = ['wind_speed_10m', 'wind_speed_80m']
        for wind_col in wind_cols:
            if wind_col in df.columns and not df[wind_col].isna().all():
                wind_data = df[wind_col].dropna()
                height = '10m' if '10m' in wind_col else '80m'
                stats['atmospheric'][f'wind_speed_{height}'] = {
                    'current': float(wind_data.iloc[-1]) if not wind_data.empty else None,
                    'max': float(wind_data.max()),
                    'avg': float(wind_data.mean()),
                    'min': float(wind_data.min()),
                    'unit': 'km/h'
                }
                
                # Wind direction
                dir_col = wind_col.replace('speed', 'direction')
                if dir_col in df.columns and not df[dir_col].isna().all():
                    wind_dir = df[dir_col].dropna()
                    stats['atmospheric'][f'wind_direction_{height}'] = {
                        'current': float(wind_dir.iloc[-1]) if not wind_dir.empty else None,
                        'avg': float(wind_dir.mean()),
                        'unit': '°'
                    }
        
        # Cloud Cover
        if 'cloud_cover' in df.columns and not df['cloud_cover'].isna().all():
            cloud_data = df['cloud_cover'].dropna()
            stats['atmospheric']['cloud_cover'] = {
                'current': float(cloud_data.iloc[-1]) if not cloud_data.empty else None,
                'min': float(cloud_data.min()),
                'max': float(cloud_data.max()),
                'avg': float(cloud_data.mean()),
                'unit': '%'
            }
        
        # HYDROLOGICAL PARAMETERS
        # Rainfall
        if 'rain' in df.columns and not df['rain'].isna().all():
            rain_data = df['rain'].dropna()
            stats['hydrological']['rainfall'] = {
                'total_mm': float(rain_data.sum()),
                'max_hourly_mm': float(rain_data.max()),
                'avg_hourly_mm': float(rain_data.mean()),
                'hours_with_rain': int((rain_data > 0).sum()),
                'unit': 'mm/h'
            }
        
        # Total Precipitation
        if 'precipitation' in df.columns and not df['precipitation'].isna().all():
            precip_data = df['precipitation'].dropna()
            stats['hydrological']['precipitation'] = {
                'total_mm': float(precip_data.sum()),
                'max_hourly_mm': float(precip_data.max()),
                'avg_hourly_mm': float(precip_data.mean()),
                'unit': 'mm/h'
            }
        
        # Sea Level Pressure (in Pascal and hPa)
        if 'pressure_msl' in df.columns and not df['pressure_msl'].isna().all():
            pressure_data = df['pressure_msl'].dropna()
            stats['hydrological']['sea_level_pressure'] = {
                'current_hpa': float(pressure_data.iloc[-1]) if not pressure_data.empty else None,
                'current_pascal': float(pressure_data.iloc[-1] * 100) if not pressure_data.empty else None,
                'min_hpa': float(pressure_data.min()),
                'max_hpa': float(pressure_data.max()),
                'avg_hpa': float(pressure_data.mean()),
                'trend': self._calculate_trend(pressure_data),
                'unit_hpa': 'hPa',
                'unit_pascal': 'Pa'
            }
            
            # Cyclone activity indicator (low pressure + high wind)
            if 'wind_speed_80m' in df.columns:
                wind_data = df['wind_speed_80m'].dropna()
                if not wind_data.empty:
                    cyclone_indicator = self._calculate_cyclone_activity(pressure_data, wind_data)
                    stats['hydrological']['cyclone_activity'] = cyclone_indicator
        
        # OCEANIC AND COASTAL PARAMETERS
        # Sea Surface Temperature
        if 'sea_surface_temperature' in df.columns and not df['sea_surface_temperature'].isna().all():
            sst_data = df['sea_surface_temperature'].dropna()
            stats['oceanic']['sea_surface_temperature'] = {
                'current': float(sst_data.iloc[-1]) if not sst_data.empty else None,
                'min': float(sst_data.min()),
                'max': float(sst_data.max()),
                'avg': float(sst_data.mean()),
                'trend': self._calculate_trend(sst_data),
                'unit': '°C'
            }
        
        # Wave Height
        if 'wave_height' in df.columns and not df['wave_height'].isna().all():
            wave_data = df['wave_height'].dropna()
            stats['oceanic']['wave_height'] = {
                'current': float(wave_data.iloc[-1]) if not wave_data.empty else None,
                'max': float(wave_data.max()),
                'avg': float(wave_data.mean()),
                'min': float(wave_data.min()),
                'unit': 'm'
            }
        
        # Ocean Wind (from ocean current data)
        if 'ocean_current_velocity' in df.columns and not df['ocean_current_velocity'].isna().all():
            ocean_wind_data = df['ocean_current_velocity'].dropna()
            stats['oceanic']['ocean_wind'] = {
                'current': float(ocean_wind_data.iloc[-1]) if not ocean_wind_data.empty else None,
                'max': float(ocean_wind_data.max()),
                'avg': float(ocean_wind_data.mean()),
                'unit': 'm/s'
            }
        
        # ENVIRONMENTAL PARAMETERS
        # Air Quality Index (calculated from PM2.5 and PM10)
        if 'pm2_5' in df.columns and not df['pm2_5'].isna().all():
            pm25_data = df['pm2_5'].dropna()
            aqi = self._calculate_aqi(pm25_data)
            stats['environmental']['air_quality_index'] = aqi
        
        # Individual pollutants
        pollutants = {
            'pm10': 'PM10',
            'pm2_5': 'PM2.5',
            'ozone': 'Ozone',
            'carbon_monoxide': 'Carbon Monoxide',
            'nitrogen_dioxide': 'Nitrogen Dioxide',
            'sulphur_dioxide': 'Sulphur Dioxide'
        }
        
        for col, name in pollutants.items():
            if col in df.columns and not df[col].isna().all():
                pollutant_data = df[col].dropna()
                stats['environmental'][col] = {
                    'current': float(pollutant_data.iloc[-1]) if not pollutant_data.empty else None,
                    'max': float(pollutant_data.max()),
                    'avg': float(pollutant_data.mean()),
                    'min': float(pollutant_data.min()),
                    'name': name,
                    'unit': 'μg/m³' if col.startswith('pm') else 'ppb'
                }
        
        return stats
    
    def _calculate_trend(self, data: pd.Series) -> str:
        """Calculate trend direction for a time series"""
        if len(data) < 2:
            return "stable"
        
        # Simple linear trend
        x = np.arange(len(data))
        slope = np.polyfit(x, data, 1)[0]
        
        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"
    
    def _calculate_cyclone_activity(self, pressure_data: pd.Series, wind_data: pd.Series) -> Dict[str, Any]:
        """Calculate cyclone activity indicator based on pressure and wind"""
        try:
            current_pressure = pressure_data.iloc[-1] if not pressure_data.empty else None
            current_wind = wind_data.iloc[-1] if not wind_data.empty else None
            
            # Cyclone indicators
            low_pressure_threshold = 1000  # hPa
            high_wind_threshold = 60  # km/h
            
            cyclone_risk = "low"
            if current_pressure and current_wind:
                if current_pressure < 980 and current_wind > 100:
                    cyclone_risk = "very_high"
                elif current_pressure < 990 and current_wind > 80:
                    cyclone_risk = "high"
                elif current_pressure < low_pressure_threshold and current_wind > high_wind_threshold:
                    cyclone_risk = "moderate"
            
            return {
                'risk_level': cyclone_risk,
                'current_pressure_hpa': float(current_pressure) if current_pressure else None,
                'current_wind_kmh': float(current_wind) if current_wind else None,
                'pressure_trend': self._calculate_trend(pressure_data),
                'wind_trend': self._calculate_trend(wind_data),
                'description': self._get_cyclone_description(cyclone_risk)
            }
            
        except Exception as e:
            print(f"⚠️ Error calculating cyclone activity: {str(e)}")
            return {'risk_level': 'unknown', 'description': 'Unable to calculate cyclone activity'}
    
    def _get_cyclone_description(self, risk_level: str) -> str:
        """Get description for cyclone risk level"""
        descriptions = {
            'low': 'Normal weather conditions, no cyclone activity detected',
            'moderate': 'Some cyclonic conditions present - monitor weather updates',
            'high': 'Significant cyclonic activity - take precautions',
            'very_high': 'Severe cyclonic conditions - seek shelter immediately',
            'unknown': 'Cyclone activity assessment unavailable'
        }
        return descriptions.get(risk_level, 'Unknown risk level')
    
    def _calculate_aqi(self, pm25_data: pd.Series) -> Dict[str, Any]:
        """Calculate Air Quality Index from PM2.5 data"""
        try:
            current_pm25 = pm25_data.iloc[-1] if not pm25_data.empty else None
            avg_pm25 = pm25_data.mean() if not pm25_data.empty else None
            
            if current_pm25 is None:
                return {'aqi': None, 'category': 'unknown', 'description': 'No PM2.5 data available'}
            
            # AQI calculation based on PM2.5 (simplified US EPA standard)
            if current_pm25 <= 12:
                aqi = int((50 / 12) * current_pm25)
                category = 'good'
                description = 'Air quality is satisfactory'
            elif current_pm25 <= 35.4:
                aqi = int(50 + ((100 - 50) / (35.4 - 12)) * (current_pm25 - 12))
                category = 'moderate'
                description = 'Air quality is acceptable for most people'
            elif current_pm25 <= 55.4:
                aqi = int(100 + ((150 - 100) / (55.4 - 35.4)) * (current_pm25 - 35.4))
                category = 'unhealthy_for_sensitive'
                description = 'Sensitive groups may experience health effects'
            elif current_pm25 <= 150.4:
                aqi = int(150 + ((200 - 150) / (150.4 - 55.4)) * (current_pm25 - 55.4))
                category = 'unhealthy'
                description = 'Everyone may experience health effects'
            elif current_pm25 <= 250.4:
                aqi = int(200 + ((300 - 200) / (250.4 - 150.4)) * (current_pm25 - 150.4))
                category = 'very_unhealthy'
                description = 'Health alert: everyone may experience serious health effects'
            else:
                aqi = int(300 + ((500 - 300) / (500.4 - 250.4)) * (current_pm25 - 250.4))
                category = 'hazardous'
                description = 'Health warnings of emergency conditions'
            
            return {
                'aqi': min(aqi, 500),  # Cap at 500
                'category': category,
                'description': description,
                'current_pm25': float(current_pm25),
                'avg_pm25': float(avg_pm25),
                'unit': 'μg/m³'
            }
            
        except Exception as e:
            print(f"⚠️ Error calculating AQI: {str(e)}")
            return {'aqi': None, 'category': 'unknown', 'description': 'Unable to calculate AQI'}
    
    def _generate_comprehensive_insights(self, df: pd.DataFrame, stats: Dict) -> List[str]:
        """Generate comprehensive human-readable insights from all weather categories"""
        
        insights = []
        
        if df.empty or not stats:
            return insights
        
        # ATMOSPHERIC INSIGHTS
        atmospheric = stats.get('atmospheric', {})
        
        # Temperature insights
        if 'temperature' in atmospheric:
            temp_stats = atmospheric['temperature']
            temp_range = temp_stats['max'] - temp_stats['min']
            insights.append(f"🌡️ Temperature varied by {temp_range:.1f}°C over the past 6 hours")
            
            if temp_stats['trend'] == 'increasing':
                insights.append("🔥 Temperature is trending upward")
            elif temp_stats['trend'] == 'decreasing':
                insights.append("❄️ Temperature is trending downward")
            
            current_temp = temp_stats.get('current')
            if current_temp:
                if current_temp > 30:
                    insights.append("🌡️ Very warm conditions detected")
                elif current_temp > 25:
                    insights.append("☀️ Warm weather conditions")
                elif current_temp < 0:
                    insights.append("🧊 Freezing conditions detected")
                elif current_temp < 5:
                    insights.append("🥶 Cold weather conditions")
        
        # Humidity insights
        if 'humidity' in atmospheric:
            humidity_stats = atmospheric['humidity']
            current_humidity = humidity_stats.get('current')
            if current_humidity:
                if current_humidity > 80:
                    insights.append("💧 Very high humidity levels - feels muggy")
                elif current_humidity < 30:
                    insights.append("🏜️ Low humidity levels - dry conditions")
        
        # Wind insights
        wind_keys = [k for k in atmospheric.keys() if k.startswith('wind_speed')]
        for wind_key in wind_keys:
            wind_stats = atmospheric[wind_key]
            height = wind_key.split('_')[-1]
            if wind_stats['max'] > 50:
                insights.append(f"💨 Strong winds detected at {height} - max speed {wind_stats['max']:.1f} km/h")
            elif wind_stats['avg'] < 5:
                insights.append(f"🍃 Calm wind conditions at {height}")
        
        # Cloud cover insights
        if 'cloud_cover' in atmospheric:
            cloud_stats = atmospheric['cloud_cover']
            current_clouds = cloud_stats.get('current')
            if current_clouds:
                if current_clouds > 80:
                    insights.append("☁️ Heavily overcast skies")
                elif current_clouds < 20:
                    insights.append("☀️ Clear skies with minimal cloud cover")
        
        # HYDROLOGICAL INSIGHTS
        hydrological = stats.get('hydrological', {})
        
        # Rainfall insights
        if 'rainfall' in hydrological:
            rain_stats = hydrological['rainfall']
            if rain_stats['total_mm'] > 0:
                insights.append(f"🌧️ Total rainfall: {rain_stats['total_mm']:.1f}mm over {rain_stats['hours_with_rain']} hours")
                if rain_stats['max_hourly_mm'] > 10:
                    insights.append("⛈️ Heavy rainfall detected in some hours")
            else:
                insights.append("🌤️ No rainfall recorded in the past 6 hours")
        
        # Pressure and cyclone insights
        if 'sea_level_pressure' in hydrological:
            pressure_stats = hydrological['sea_level_pressure']
            if pressure_stats['trend'] == 'decreasing':
                insights.append("📉 Atmospheric pressure dropping - weather may be changing")
            elif pressure_stats['trend'] == 'increasing':
                insights.append("📈 Atmospheric pressure rising - weather stabilizing")
            
            current_pressure = pressure_stats.get('current_hpa')
            if current_pressure:
                if current_pressure > 1020:
                    insights.append("🔒 High pressure indicates stable weather conditions")
                elif current_pressure < 1000:
                    insights.append("⚠️ Low pressure may indicate stormy weather")
        
        # Cyclone activity insights
        if 'cyclone_activity' in hydrological:
            cyclone_stats = hydrological['cyclone_activity']
            risk_level = cyclone_stats.get('risk_level', 'unknown')
            if risk_level in ['high', 'very_high']:
                insights.append(f"🌀 {cyclone_stats.get('description', 'Cyclonic activity detected')}")
            elif risk_level == 'moderate':
                insights.append("🌪️ Some cyclonic conditions present - monitor weather")
        
        # OCEANIC INSIGHTS
        oceanic = stats.get('oceanic', {})
        
        # Sea surface temperature
        if 'sea_surface_temperature' in oceanic:
            sst_stats = oceanic['sea_surface_temperature']
            current_sst = sst_stats.get('current')
            if current_sst:
                if current_sst > 25:
                    insights.append("🌊 Warm sea surface temperatures detected")
                elif current_sst < 15:
                    insights.append("🧊 Cool sea surface temperatures")
        
        # Wave conditions
        if 'wave_height' in oceanic:
            wave_stats = oceanic['wave_height']
            max_wave = wave_stats.get('max')
            if max_wave:
                if max_wave > 3:
                    insights.append(f"🌊 High waves detected - maximum {max_wave:.1f}m")
                elif max_wave < 0.5:
                    insights.append("🏖️ Calm sea conditions with low waves")
        
        # ENVIRONMENTAL INSIGHTS
        environmental = stats.get('environmental', {})
        
        # Air quality insights
        if 'air_quality_index' in environmental:
            aqi_stats = environmental['air_quality_index']
            aqi = aqi_stats.get('aqi')
            category = aqi_stats.get('category', 'unknown')
            
            if aqi:
                if category == 'good':
                    insights.append(f"🌿 Good air quality (AQI: {aqi})")
                elif category == 'moderate':
                    insights.append(f"🟡 Moderate air quality (AQI: {aqi})")
                elif category in ['unhealthy_for_sensitive', 'unhealthy']:
                    insights.append(f"🔶 Poor air quality detected (AQI: {aqi}) - sensitive groups should limit outdoor activities")
                elif category in ['very_unhealthy', 'hazardous']:
                    insights.append(f"🔴 Hazardous air quality (AQI: {aqi}) - avoid outdoor activities")
        
        # Pollutant insights
        if 'pm2_5' in environmental:
            pm25_stats = environmental['pm2_5']
            current_pm25 = pm25_stats.get('current')
            if current_pm25 and current_pm25 > 35:
                insights.append(f"⚠️ High PM2.5 levels detected ({current_pm25:.1f} μg/m³)")
        
        return insights
    
    def get_location_name(self, latitude: float, longitude: float) -> str:
        """Get a human-readable location name (simplified)"""
        # This is a simplified version - in production you might use a geocoding service
        return f"Location ({latitude:.2f}, {longitude:.2f})"