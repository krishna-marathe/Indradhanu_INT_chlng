"""
Geocoding Service - Convert location names to coordinates
Uses OpenStreetMap Nominatim API (free, no API key required)
"""
import requests
import time
from typing import Dict, List, Optional, Tuple
import urllib.parse


class GeocodingService:
    """Service for converting location names to coordinates"""
    
    BASE_URL = "https://nominatim.openstreetmap.org/search"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Climate-Sphere/1.0 (Environmental Data Analysis)'
        })
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Nominatim requires 1 second between requests
    
    def _rate_limit(self):
        """Ensure we don't exceed rate limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def search_location(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search for locations by name
        
        Args:
            query: Location name (e.g., "New York", "London, UK", "Tokyo, Japan")
            limit: Maximum number of results to return
            
        Returns:
            List of location dictionaries with coordinates and details
        """
        try:
            self._rate_limit()
            
            params = {
                'q': query,
                'format': 'json',
                'limit': limit,
                'addressdetails': 1,
                'extratags': 1,
                'namedetails': 1
            }
            
            print(f"🔍 Searching for location: {query}")
            
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            results = response.json()
            
            locations = []
            for result in results:
                location = {
                    'name': result.get('display_name', ''),
                    'latitude': float(result.get('lat', 0)),
                    'longitude': float(result.get('lon', 0)),
                    'type': result.get('type', ''),
                    'class': result.get('class', ''),
                    'importance': float(result.get('importance', 0)),
                    'country': '',
                    'state': '',
                    'city': ''
                }
                
                # Extract address components
                address = result.get('address', {})
                location['country'] = address.get('country', '')
                location['state'] = address.get('state', address.get('province', ''))
                location['city'] = address.get('city', address.get('town', address.get('village', '')))
                
                # Create a clean display name
                location['clean_name'] = self._create_clean_name(location)
                
                locations.append(location)
            
            print(f"✅ Found {len(locations)} locations for '{query}'")
            return locations
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Geocoding API error: {str(e)}")
            raise Exception(f"Failed to search location: {str(e)}")
        except Exception as e:
            print(f"❌ Geocoding processing error: {str(e)}")
            raise Exception(f"Failed to process location search: {str(e)}")
    
    def get_coordinates(self, location_name: str) -> Tuple[float, float]:
        """
        Get coordinates for a single location (returns the best match)
        
        Args:
            location_name: Name of the location
            
        Returns:
            Tuple of (latitude, longitude)
        """
        results = self.search_location(location_name, limit=1)
        
        if not results:
            raise Exception(f"Location '{location_name}' not found")
        
        best_match = results[0]
        return best_match['latitude'], best_match['longitude']
    
    def _create_clean_name(self, location: Dict) -> str:
        """Create a clean, readable location name"""
        parts = []
        
        # Add city/town
        if location['city']:
            parts.append(location['city'])
        
        # Add state/province if different from city
        if location['state'] and location['state'] != location['city']:
            parts.append(location['state'])
        
        # Add country
        if location['country']:
            parts.append(location['country'])
        
        if parts:
            return ', '.join(parts)
        else:
            # Fallback to display name
            return location['name'].split(',')[0] if location['name'] else 'Unknown Location'
    
    def get_popular_locations(self) -> List[Dict]:
        """Get a list of popular locations for quick access"""
        popular_cities = [
            "New York, USA",
            "London, UK", 
            "Tokyo, Japan",
            "Paris, France",
            "Berlin, Germany",
            "Sydney, Australia",
            "Mumbai, India",
            "São Paulo, Brazil",
            "Cairo, Egypt",
            "Moscow, Russia",
            "Beijing, China",
            "Los Angeles, USA",
            "Dubai, UAE",
            "Singapore",
            "Toronto, Canada"
        ]
        
        locations = []
        for city in popular_cities:
            try:
                results = self.search_location(city, limit=1)
                if results:
                    locations.append(results[0])
                time.sleep(0.1)  # Small delay between requests
            except Exception as e:
                print(f"⚠️ Could not fetch {city}: {str(e)}")
                continue
        
        return locations
    
    def reverse_geocode(self, latitude: float, longitude: float) -> Dict:
        """
        Convert coordinates back to location name
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Location information dictionary
        """
        try:
            self._rate_limit()
            
            url = "https://nominatim.openstreetmap.org/reverse"
            params = {
                'lat': latitude,
                'lon': longitude,
                'format': 'json',
                'addressdetails': 1
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            location = {
                'name': result.get('display_name', ''),
                'latitude': latitude,
                'longitude': longitude,
                'country': '',
                'state': '',
                'city': ''
            }
            
            # Extract address components
            address = result.get('address', {})
            location['country'] = address.get('country', '')
            location['state'] = address.get('state', address.get('province', ''))
            location['city'] = address.get('city', address.get('town', address.get('village', '')))
            location['clean_name'] = self._create_clean_name(location)
            
            return location
            
        except Exception as e:
            print(f"❌ Reverse geocoding error: {str(e)}")
            return {
                'name': f"Location ({latitude:.2f}, {longitude:.2f})",
                'latitude': latitude,
                'longitude': longitude,
                'clean_name': f"({latitude:.2f}, {longitude:.2f})"
            }