"""
Google Earth Engine Data Processor
Extracts environmental data for selected areas
"""
import ee
import os
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta

load_dotenv()

class GEEProcessor:
    def __init__(self):
        """Initialize Google Earth Engine"""
        self._authenticate()
        self._set_date_range()
    
    def _authenticate(self):
        """Authenticate with Google Earth Engine"""
        try:
            service_account = os.getenv('GEE_SERVICE_ACCOUNT')
            key_path = os.getenv('GEE_PRIVATE_KEY_PATH')
            
            credentials = ee.ServiceAccountCredentials(service_account, key_path)
            ee.Initialize(credentials)
            print("GEE Authentication successful")
        except Exception as e:
            print(f"GEE Authentication failed: {e}")
            raise
    
    def _set_date_range(self, months_back=12):
        """Set dynamic date range for data extraction"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months_back * 30)
        
        self.start_date = start_date.strftime('%Y-%m-%d')
        self.end_date = end_date.strftime('%Y-%m-%d')
        print(f"Date range: {self.start_date} to {self.end_date}")
    
    def extract_data(self, geometry):
        """
        Extract environmental data for a given geometry
        
        Args:
            geometry (dict): GeoJSON geometry (polygon or point)
        
        Returns:
            dict: Environmental metrics
        """
        try:
            # Convert GeoJSON to EE geometry
            if geometry['type'] == 'Polygon':
                ee_geometry = ee.Geometry.Polygon(geometry['coordinates'])
            else:
                ee_geometry = ee.Geometry.Point(geometry['coordinates'])
            
            # Extract metrics
            print(f"Extracting data for area: {ee_geometry.area().divide(1000000).getInfo():.2f} km²")
            
            # Vegetation & Climate
            ndvi = self._get_ndvi(ee_geometry)
            temperature = self._get_temperature(ee_geometry)
            air_temperature = self._get_air_temperature(ee_geometry)
            precipitation = self._get_precipitation(ee_geometry)
            land_cover = self._get_land_cover(ee_geometry)
            
            # Air Quality & Pollution
            co_concentration = self._get_co_concentration(ee_geometry)
            no2 = self._get_no2(ee_geometry)
            so2 = self._get_so2(ee_geometry)
            ozone = self._get_ozone(ee_geometry)
            aerosol = self._get_aerosol(ee_geometry)
            
            # Soil & Water
            soil_moisture = self._get_soil_moisture(ee_geometry)
            evapotranspiration = self._get_evapotranspiration(ee_geometry)
            
            # Advanced Climate Parameters (with progress logging)
            print("Extracting advanced climate parameters...")
            
            print("  - Land use change...")
            land_use_change = self._get_land_use_change(ee_geometry)
            print(f"    Result: {land_use_change is not None}")
            
            print("  - Urban heat island...")
            urban_heat_island = self._get_urban_heat_island(ee_geometry)
            print(f"    Result: {urban_heat_island is not None}")
            
            print("  - Water body change...")
            water_body_change = self._get_water_body_change(ee_geometry)
            print(f"    Result: {water_body_change is not None}")
            
            print("  - Rainfall trend...")
            rainfall_trend = self._get_rainfall_trend(ee_geometry)
            print(f"    Result: {rainfall_trend is not None}")
            
            print("  - Vulnerability assessment...")
            vulnerability = self._get_flood_drought_vulnerability(ee_geometry)
            print(f"    Result: {vulnerability is not None}")
            
            area = ee_geometry.area().divide(1000000).getInfo()  # km²
            
            # Count available parameters
            available_params = sum([
                ndvi is not None,
                temperature is not None,
                air_temperature is not None,
                precipitation is not None,
                land_cover != "Unknown",
                co_concentration is not None,
                no2 is not None,
                so2 is not None,
                ozone is not None,
                aerosol is not None,
                soil_moisture is not None,
                evapotranspiration is not None,
                land_use_change is not None,
                urban_heat_island is not None,
                water_body_change is not None,
                rainfall_trend is not None,
                vulnerability is not None
            ])
            
            print(f"Data extraction complete: {available_params}/18 parameters available")
            
            return {
                'success': True,
                'data': {
                    # Vegetation & Climate
                    'ndvi': round(ndvi, 3) if ndvi else None,
                    'temperature': round(temperature, 2) if temperature else None,
                    'air_temperature': round(air_temperature, 2) if air_temperature else None,
                    'precipitation': round(precipitation, 2) if precipitation else None,
                    'land_cover': land_cover,
                    
                    # Air Quality & Pollution
                    'co_concentration': round(co_concentration, 6) if co_concentration else None,
                    'no2': round(no2, 6) if no2 else None,
                    'so2': round(so2, 6) if so2 else None,
                    'ozone': round(ozone, 4) if ozone else None,
                    'aerosol': round(aerosol, 3) if aerosol else None,
                    
                    # Soil & Water
                    'soil_moisture': round(soil_moisture, 3) if soil_moisture else None,
                    'evapotranspiration': round(evapotranspiration, 2) if evapotranspiration else None,
                    
                    # Advanced Climate Parameters
                    'land_use_change': land_use_change,
                    'urban_heat_island': urban_heat_island,
                    'water_body_change': water_body_change,
                    'rainfall_trend': rainfall_trend,
                    'vulnerability': vulnerability,
                    
                    # Metadata
                    'area': round(area, 2),
                    'geometry': geometry,
                    'data_availability': f"{available_params}/18",
                    'datasets_used': {
                        'ndvi': 'MODIS MOD13Q1 (250m)',
                        'temperature': 'MODIS MOD11A2 (1km)',
                        'air_temperature': 'ERA5-Land (10km)',
                        'precipitation': 'CHIRPS Daily (5km)',
                        'co_concentration': 'Sentinel-5P TROPOMI CO (5-10km)',
                        'air_pollution': 'Sentinel-5P TROPOMI (5-10km)',
                        'land_cover': 'MODIS MCD12Q1 (500m)',
                        'water_bodies': 'JRC Global Surface Water (30m)',
                        'vulnerability': 'SMAP + CHIRPS'
                    }
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_ndvi(self, geometry):
        """Get NDVI from MODIS MOD13Q1 (250m, vegetation health)"""
        try:
            ndvi = ee.ImageCollection('MODIS/006/MOD13Q1') \
                .select('NDVI') \
                .filterDate(self.start_date, self.end_date) \
                .filterBounds(geometry) \
                .mean() \
                .multiply(0.0001)
            
            value = ndvi.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=250,  # 250m optimal resolution
                maxPixels=1e9
            ).get('NDVI').getInfo()
            
            return value if value is not None else None
        except Exception as e:
            print(f"NDVI extraction error: {e}")
            return None
    
    def _get_temperature(self, geometry):
        """Get Land Surface Temperature from MODIS MOD11A2 (1km, daytime & nighttime)"""
        try:
            temp = ee.ImageCollection('MODIS/006/MOD11A2') \
                .select('LST_Day_1km') \
                .filterDate(self.start_date, self.end_date) \
                .filterBounds(geometry) \
                .mean() \
                .multiply(0.02) \
                .subtract(273.15)
            
            value = temp.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=1000,  # 1km optimal resolution
                maxPixels=1e9
            ).get('LST_Day_1km').getInfo()
            
            return value if value is not None else None
        except Exception as e:
            print(f"Temperature extraction error: {e}")
            return None
    
    def _get_air_temperature(self, geometry):
        """Get Air Temperature from ERA5-Land hourly (10km, reanalysis climate model)"""
        try:
            air_temp = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY') \
                .select('temperature_2m') \
                .filterDate(self.start_date, self.end_date) \
                .filterBounds(geometry) \
                .mean() \
                .subtract(273.15)  # Convert Kelvin to Celsius
            
            value = air_temp.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=10000,  # 10km optimal resolution
                maxPixels=1e9
            ).get('temperature_2m').getInfo()
            
            return value if value is not None else None
        except Exception as e:
            print(f"Air temperature extraction error: {e}")
            return None
    
    def _get_precipitation(self, geometry):
        """Get Precipitation from CHIRPS Daily (5km, excellent climate rainfall dataset)"""
        try:
            precip = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
                .select('precipitation') \
                .filterDate(self.start_date, self.end_date) \
                .filterBounds(geometry) \
                .sum()
            
            value = precip.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=5000,  # 5km optimal resolution
                maxPixels=1e9
            ).get('precipitation').getInfo()
            
            return value if value is not None else None
        except Exception as e:
            print(f"Precipitation extraction error: {e}")
            return None
    
    def _get_land_cover(self, geometry):
        """Get Land Cover from MODIS MCD12Q1 (500m, land classification)"""
        try:
            # Try multiple years to find available data
            current_year = datetime.now().year
            for year_offset in range(0, 3):
                try:
                    year = current_year - year_offset
                    land_cover_start = f'{year}-01-01'
                    land_cover_end = f'{year}-12-31'
                    
                    land_cover = ee.ImageCollection('MODIS/006/MCD12Q1') \
                        .select('LC_Type1') \
                        .filterDate(land_cover_start, land_cover_end) \
                        .filterBounds(geometry) \
                        .first()
                    
                    value = land_cover.reduceRegion(
                        reducer=ee.Reducer.mode(),
                        geometry=geometry,
                        scale=500,  # 500m optimal resolution
                        maxPixels=1e9
                    ).get('LC_Type1').getInfo()
                    
                    if value is not None:
                        return self._decode_land_cover(value)
                except:
                    continue
            
            return "Unknown"
        except Exception as e:
            print(f"Land cover extraction error: {e}")
            return "Unknown"
    
    def _get_co_concentration(self, geometry):
        """Get CO (Carbon Monoxide) concentration from Sentinel-5P TROPOMI (5-10km, air pollution)"""
        try:
            # Sentinel-5P CO data - works well for India
            co = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_CO') \
                .select('CO_column_number_density') \
                .filterDate(self.start_date, self.end_date) \
                .filterBounds(geometry) \
                .mean()
            
            value = co.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=7500,  # 5-10km optimal resolution
                maxPixels=1e9,
                bestEffort=True
            ).get('CO_column_number_density').getInfo()
            
            return value if value is not None else None
        except Exception as e:
            print(f"CO concentration extraction error: {e}")
            return None
    
    def _get_no2(self, geometry):
        """Get NO2 from Sentinel-5P TROPOMI (5-10km, air pollution)"""
        try:
            no2 = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2') \
                .select('NO2_column_number_density') \
                .filterDate(self.start_date, self.end_date) \
                .filterBounds(geometry) \
                .mean()
            
            value = no2.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=7500,  # 5-10km optimal resolution (using 7.5km average)
                maxPixels=1e9
            ).get('NO2_column_number_density').getInfo()
            
            return value if value is not None else None
        except Exception as e:
            print(f"NO2 extraction error: {e}")
            return None
    
    def _get_so2(self, geometry):
        """Get SO2 from Sentinel-5P TROPOMI (5-10km, air pollution)"""
        try:
            so2 = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_SO2') \
                .select('SO2_column_number_density') \
                .filterDate(self.start_date, self.end_date) \
                .filterBounds(geometry) \
                .mean()
            
            value = so2.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=7500,  # 5-10km optimal resolution
                maxPixels=1e9
            ).get('SO2_column_number_density').getInfo()
            
            return value if value is not None else None
        except Exception as e:
            print(f"SO2 extraction error: {e}")
            return None
    

    
    def _get_ozone(self, geometry):
        """Get O3 (Ozone) from Sentinel-5P TROPOMI (5-10km, air pollution)"""
        try:
            o3 = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_O3') \
                .select('O3_column_number_density') \
                .filterDate(self.start_date, self.end_date) \
                .filterBounds(geometry) \
                .mean()
            
            value = o3.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=7500,  # 5-10km optimal resolution
                maxPixels=1e9
            ).get('O3_column_number_density').getInfo()
            
            return value if value is not None else None
        except Exception as e:
            print(f"O3 extraction error: {e}")
            return None
    
    def _get_land_use_change(self, geometry):
        """Detect land use/land cover change over time"""
        try:
            current_year = datetime.now().year
            
            # Get land cover from 5 years ago
            past_lc = ee.ImageCollection('MODIS/006/MCD12Q1') \
                .select('LC_Type1') \
                .filterDate(f'{current_year-5}-01-01', f'{current_year-5}-12-31') \
                .filterBounds(geometry) \
                .first()
            
            # Get recent land cover
            recent_lc = ee.ImageCollection('MODIS/006/MCD12Q1') \
                .select('LC_Type1') \
                .filterDate(f'{current_year-1}-01-01', f'{current_year-1}-12-31') \
                .filterBounds(geometry) \
                .first()
            
            if past_lc and recent_lc:
                past_mode = past_lc.reduceRegion(
                    reducer=ee.Reducer.mode(),
                    geometry=geometry,
                    scale=500,
                    maxPixels=1e9
                ).get('LC_Type1').getInfo()
                
                recent_mode = recent_lc.reduceRegion(
                    reducer=ee.Reducer.mode(),
                    geometry=geometry,
                    scale=500,
                    maxPixels=1e9
                ).get('LC_Type1').getInfo()
                
                if past_mode and recent_mode:
                    return {
                        'past': self._decode_land_cover(past_mode),
                        'recent': self._decode_land_cover(recent_mode),
                        'changed': past_mode != recent_mode
                    }
            
            return None
        except Exception as e:
            print(f"Land use change detection error: {e}")
            return None
    
    def _get_urban_heat_island(self, geometry):
        """Calculate Urban Heat Island Index"""
        try:
            # Get temperature for the area
            temp = ee.ImageCollection('MODIS/006/MOD11A2') \
                .select('LST_Day_1km') \
                .filterDate(self.start_date, self.end_date) \
                .filterBounds(geometry) \
                .mean() \
                .multiply(0.02) \
                .subtract(273.15)
            
            # Get statistics
            stats = temp.reduceRegion(
                reducer=ee.Reducer.mean().combine(ee.Reducer.stdDev()).combine(ee.Reducer.minMax()),
                geometry=geometry,
                scale=1000,
                maxPixels=1e9
            ).getInfo()
            
            mean_temp = stats.get('LST_Day_1km_mean')
            max_temp = stats.get('LST_Day_1km_max')
            min_temp = stats.get('LST_Day_1km_min')
            
            if mean_temp and max_temp and min_temp:
                # UHI intensity = max - min temperature
                uhi_intensity = max_temp - min_temp
                return {
                    'intensity': round(uhi_intensity, 2),
                    'mean_temp': round(mean_temp, 2),
                    'max_temp': round(max_temp, 2),
                    'min_temp': round(min_temp, 2)
                }
            
            return None
        except Exception as e:
            print(f"Urban heat island calculation error: {e}")
            return None
    
    def _get_water_body_change(self, geometry):
        """Detect water body changes using JRC Global Surface Water"""
        try:
            # Get water occurrence (percentage of time water was present)
            water = ee.Image('JRC/GSW1_4/GlobalSurfaceWater') \
                .select('occurrence')
            
            stats = water.reduceRegion(
                reducer=ee.Reducer.mean().combine(ee.Reducer.minMax()),
                geometry=geometry,
                scale=30,
                maxPixels=1e9
            ).getInfo()
            
            occurrence = stats.get('occurrence')
            
            if occurrence is not None:
                return {
                    'water_occurrence': round(occurrence, 2),
                    'status': 'permanent' if occurrence > 75 else 
                             'seasonal' if occurrence > 25 else 
                             'rare' if occurrence > 5 else 'minimal'
                }
            
            return None
        except Exception as e:
            print(f"Water body change detection error: {e}")
            return None
    
    def _get_rainfall_trend(self, geometry):
        """Calculate simplified 5-year rainfall trend (faster)"""
        try:
            current_year = datetime.now().year
            start_year = current_year - 5  # Reduced from 10 to 5 years for speed
            
            # Get all data in one query
            precip_col = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
                .select('precipitation') \
                .filterDate(f'{start_year}-01-01', f'{current_year-1}-12-31') \
                .filterBounds(geometry)
            
            # Calculate annual sums more efficiently
            def get_annual_sum(year):
                year_data = precip_col.filterDate(f'{year}-01-01', f'{year}-12-31').sum()
                return year_data.reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=geometry,
                    scale=5000,
                    maxPixels=1e9,
                    bestEffort=True
                ).get('precipitation')
            
            # Get recent 3 years vs older 2 years
            recent_years = list(range(current_year-3, current_year))
            older_years = list(range(start_year, current_year-3))
            
            recent_sum = 0
            older_sum = 0
            
            for year in recent_years:
                val = get_annual_sum(year).getInfo()
                if val:
                    recent_sum += val
            
            for year in older_years:
                val = get_annual_sum(year).getInfo()
                if val:
                    older_sum += val
            
            if recent_sum > 0 and older_sum > 0:
                recent_avg = recent_sum / len(recent_years)
                older_avg = older_sum / len(older_years)
                
                # Simple trend detection
                change = recent_avg - older_avg
                trend = 'increasing' if change > 50 else 'decreasing' if change < -50 else 'stable'
                
                return {
                    'trend': trend,
                    'change_rate': round(change / 5, 2),  # Per year
                    'recent_avg': round(recent_avg, 1),
                    'long_term_avg': round((recent_sum + older_sum) / 5, 1)
                }
            
            return None
        except Exception as e:
            print(f"Rainfall trend calculation error: {e}")
            return None
    
    def _get_flood_drought_vulnerability(self, geometry):
        """Assess flood and drought vulnerability"""
        try:
            # Get soil moisture for drought assessment
            soil = ee.ImageCollection('NASA_USDA/HSL/SMAP10KM_soil_moisture') \
                .select('ssm') \
                .filterDate(self.start_date, self.end_date) \
                .filterBounds(geometry) \
                .mean()
            
            soil_stats = soil.reduceRegion(
                reducer=ee.Reducer.mean().combine(ee.Reducer.stdDev()),
                geometry=geometry,
                scale=10000,
                maxPixels=1e9
            ).getInfo()
            
            soil_moisture = soil_stats.get('ssm')
            
            # Get precipitation for flood assessment
            precip = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
                .select('precipitation') \
                .filterDate(self.start_date, self.end_date) \
                .filterBounds(geometry)
            
            precip_stats = precip.sum().reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=5000,
                maxPixels=1e9
            ).getInfo()
            
            total_precip = precip_stats.get('precipitation')
            
            vulnerability = {
                'drought_risk': 'high' if soil_moisture and soil_moisture < 10 else
                               'moderate' if soil_moisture and soil_moisture < 20 else 'low',
                'flood_risk': 'high' if total_precip and total_precip > 1500 else
                             'moderate' if total_precip and total_precip > 1000 else 'low',
                'soil_moisture': round(soil_moisture, 2) if soil_moisture else None,
                'total_precipitation': round(total_precip, 1) if total_precip else None
            }
            
            return vulnerability
        except Exception as e:
            print(f"Vulnerability assessment error: {e}")
            return None
    
    def _get_aerosol(self, geometry):
        """Get Aerosol Index from Sentinel-5P TROPOMI (5-10km, air pollution)"""
        try:
            aerosol = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_AER_AI') \
                .select('absorbing_aerosol_index') \
                .filterDate(self.start_date, self.end_date) \
                .filterBounds(geometry) \
                .mean()
            
            value = aerosol.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=7500,  # 5-10km optimal resolution
                maxPixels=1e9
            ).get('absorbing_aerosol_index').getInfo()
            
            return value if value is not None else None
        except Exception as e:
            print(f"Aerosol extraction error: {e}")
            return None
    
    def _get_soil_moisture(self, geometry):
        """Get Soil Moisture from SMAP"""
        try:
            soil = ee.ImageCollection('NASA_USDA/HSL/SMAP10KM_soil_moisture') \
                .select('ssm') \
                .filterDate(self.start_date, self.end_date) \
                .filterBounds(geometry) \
                .mean()
            
            value = soil.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=10000,
                maxPixels=1e9
            ).get('ssm').getInfo()
            
            return value if value is not None else None
        except Exception as e:
            print(f"Soil moisture extraction error: {e}")
            return None
    
    def _get_evapotranspiration(self, geometry):
        """Get Evapotranspiration from MODIS"""
        try:
            et = ee.ImageCollection('MODIS/006/MOD16A2') \
                .select('ET') \
                .filterDate(self.start_date, self.end_date) \
                .filterBounds(geometry) \
                .mean() \
                .multiply(0.1)
            
            value = et.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=1000,
                maxPixels=1e9
            ).get('ET').getInfo()
            
            return value if value is not None else None
        except Exception as e:
            print(f"Evapotranspiration extraction error: {e}")
            return None
    
    def get_historical_trends(self, geometry, start_year=2015, end_year=2024):
        """Get historical trends for multiple years"""
        try:
            if isinstance(geometry, dict):
                ee_geometry = ee.Geometry(geometry)
            else:
                ee_geometry = geometry
            
            years = list(range(start_year, end_year + 1))
            annual_data = {
                'years': years,
                'ndvi': [],
                'temperature': [],
                'precipitation': []
            }
            
            print(f"Fetching historical data from {start_year} to {end_year}...")
            
            for year in years:
                year_start = f'{year}-01-01'
                year_end = f'{year}-12-31'
                
                # NDVI
                try:
                    ndvi_col = ee.ImageCollection('MODIS/006/MOD13A2') \
                        .select('NDVI') \
                        .filterDate(year_start, year_end) \
                        .filterBounds(ee_geometry)
                    
                    if ndvi_col.size().getInfo() > 0:
                        ndvi_val = ndvi_col.mean().multiply(0.0001).reduceRegion(
                            reducer=ee.Reducer.mean(),
                            geometry=ee_geometry,
                            scale=1000,
                            maxPixels=1e9
                        ).get('NDVI').getInfo()
                        annual_data['ndvi'].append(round(ndvi_val, 4) if ndvi_val else None)
                    else:
                        annual_data['ndvi'].append(None)
                except:
                    annual_data['ndvi'].append(None)
                
                # Temperature
                try:
                    temp_col = ee.ImageCollection('MODIS/006/MOD11A2') \
                        .select('LST_Day_1km') \
                        .filterDate(year_start, year_end) \
                        .filterBounds(ee_geometry)
                    
                    if temp_col.size().getInfo() > 0:
                        temp_val = temp_col.mean().multiply(0.02).subtract(273.15).reduceRegion(
                            reducer=ee.Reducer.mean(),
                            geometry=ee_geometry,
                            scale=1000,
                            maxPixels=1e9
                        ).get('LST_Day_1km').getInfo()
                        annual_data['temperature'].append(round(temp_val, 2) if temp_val else None)
                    else:
                        annual_data['temperature'].append(None)
                except:
                    annual_data['temperature'].append(None)
                
                # Precipitation
                try:
                    precip_col = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
                        .select('precipitation') \
                        .filterDate(year_start, year_end) \
                        .filterBounds(ee_geometry)
                    
                    if precip_col.size().getInfo() > 0:
                        precip_val = precip_col.sum().reduceRegion(
                            reducer=ee.Reducer.mean(),
                            geometry=ee_geometry,
                            scale=5000,
                            maxPixels=1e9
                        ).get('precipitation').getInfo()
                        annual_data['precipitation'].append(round(precip_val, 1) if precip_val else None)
                    else:
                        annual_data['precipitation'].append(None)
                except:
                    annual_data['precipitation'].append(None)
                
                print(f"  {year}: NDVI={annual_data['ndvi'][-1]}, Temp={annual_data['temperature'][-1]}, Precip={annual_data['precipitation'][-1]}")
            
            # Calculate trends
            trends = self._calculate_trends(annual_data)
            
            return {
                'success': True,
                'data': {
                    **annual_data,
                    'trends': trends
                }
            }
        
        except Exception as e:
            print(f"Historical trends error: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_time_series(self, geometry, parameters, start_year, end_year):
        """Get monthly time series data"""
        try:
            if isinstance(geometry, dict):
                ee_geometry = ee.Geometry(geometry)
            else:
                ee_geometry = geometry
            
            time_series = {}
            
            for param in parameters:
                time_series[param] = {
                    'dates': [],
                    'values': []
                }
                
                for year in range(start_year, end_year + 1):
                    for month in range(1, 13):
                        date_str = f'{year}-{month:02d}'
                        start_date = f'{year}-{month:02d}-01'
                        
                        if month == 12:
                            end_date = f'{year + 1}-01-01'
                        else:
                            end_date = f'{year}-{month + 1:02d}-01'
                        
                        try:
                            if param == 'ndvi':
                                col = ee.ImageCollection('MODIS/006/MOD13A2') \
                                    .select('NDVI') \
                                    .filterDate(start_date, end_date) \
                                    .filterBounds(ee_geometry)
                                
                                if col.size().getInfo() > 0:
                                    val = col.mean().multiply(0.0001).reduceRegion(
                                        reducer=ee.Reducer.mean(),
                                        geometry=ee_geometry,
                                        scale=1000,
                                        maxPixels=1e9
                                    ).get('NDVI').getInfo()
                                    
                                    if val:
                                        time_series[param]['dates'].append(date_str)
                                        time_series[param]['values'].append(round(val, 4))
                            
                            elif param == 'temperature':
                                col = ee.ImageCollection('MODIS/006/MOD11A2') \
                                    .select('LST_Day_1km') \
                                    .filterDate(start_date, end_date) \
                                    .filterBounds(ee_geometry)
                                
                                if col.size().getInfo() > 0:
                                    val = col.mean().multiply(0.02).subtract(273.15).reduceRegion(
                                        reducer=ee.Reducer.mean(),
                                        geometry=ee_geometry,
                                        scale=1000,
                                        maxPixels=1e9
                                    ).get('LST_Day_1km').getInfo()
                                    
                                    if val:
                                        time_series[param]['dates'].append(date_str)
                                        time_series[param]['values'].append(round(val, 2))
                            
                            elif param == 'precipitation':
                                col = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
                                    .select('precipitation') \
                                    .filterDate(start_date, end_date) \
                                    .filterBounds(ee_geometry)
                                
                                if col.size().getInfo() > 0:
                                    val = col.sum().reduceRegion(
                                        reducer=ee.Reducer.mean(),
                                        geometry=ee_geometry,
                                        scale=5000,
                                        maxPixels=1e9
                                    ).get('precipitation').getInfo()
                                    
                                    if val:
                                        time_series[param]['dates'].append(date_str)
                                        time_series[param]['values'].append(round(val, 1))
                        
                        except:
                            continue
            
            return {'success': True, 'data': time_series}
        
        except Exception as e:
            print(f"Time series error: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_seasonal_patterns(self, geometry, years=5):
        """Analyze comprehensive seasonal patterns for all parameters"""
        try:
            if isinstance(geometry, dict):
                ee_geometry = ee.Geometry(geometry)
            else:
                ee_geometry = geometry
            
            current_year = datetime.now().year
            start_year = current_year - years
            
            print(f"Analyzing seasonal patterns from {start_year} to {current_year}...")
            
            # Initialize monthly averages for all parameters
            monthly_data = {month: {
                'ndvi': [], 'temperature': [], 'precipitation': [],
                'co': [], 'no2': [], 'aerosol': []
            } for month in range(1, 13)}
            
            # Collect data for each year and month
            for year in range(start_year, current_year):
                for month in range(1, 13):
                    start_date = f'{year}-{month:02d}-01'
                    end_date = f'{year}-{month:02d}-28'
                    
                    # NDVI
                    try:
                        ndvi_col = ee.ImageCollection('MODIS/006/MOD13Q1') \
                            .select('NDVI') \
                            .filterDate(start_date, end_date) \
                            .filterBounds(ee_geometry)
                        
                        if ndvi_col.size().getInfo() > 0:
                            val = ndvi_col.mean().multiply(0.0001).reduceRegion(
                                reducer=ee.Reducer.mean(),
                                geometry=ee_geometry,
                                scale=250,
                                maxPixels=1e9,
                                bestEffort=True
                            ).get('NDVI').getInfo()
                            if val:
                                monthly_data[month]['ndvi'].append(val)
                    except:
                        pass
                    
                    # Temperature
                    try:
                        temp_col = ee.ImageCollection('MODIS/006/MOD11A2') \
                            .select('LST_Day_1km') \
                            .filterDate(start_date, end_date) \
                            .filterBounds(ee_geometry)
                        
                        if temp_col.size().getInfo() > 0:
                            val = temp_col.mean().multiply(0.02).subtract(273.15).reduceRegion(
                                reducer=ee.Reducer.mean(),
                                geometry=ee_geometry,
                                scale=1000,
                                maxPixels=1e9,
                                bestEffort=True
                            ).get('LST_Day_1km').getInfo()
                            if val:
                                monthly_data[month]['temperature'].append(val)
                    except:
                        pass
                    
                    # Precipitation
                    try:
                        precip_col = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
                            .select('precipitation') \
                            .filterDate(start_date, end_date) \
                            .filterBounds(ee_geometry)
                        
                        if precip_col.size().getInfo() > 0:
                            val = precip_col.sum().reduceRegion(
                                reducer=ee.Reducer.mean(),
                                geometry=ee_geometry,
                                scale=5000,
                                maxPixels=1e9,
                                bestEffort=True
                            ).get('precipitation').getInfo()
                            if val:
                                monthly_data[month]['precipitation'].append(val)
                    except:
                        pass
                    
                    # CO (Air Quality)
                    try:
                        co_col = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_CO') \
                            .select('CO_column_number_density') \
                            .filterDate(start_date, end_date) \
                            .filterBounds(ee_geometry)
                        
                        if co_col.size().getInfo() > 0:
                            val = co_col.mean().reduceRegion(
                                reducer=ee.Reducer.mean(),
                                geometry=ee_geometry,
                                scale=7500,
                                maxPixels=1e9,
                                bestEffort=True
                            ).get('CO_column_number_density').getInfo()
                            if val:
                                monthly_data[month]['co'].append(val)
                    except:
                        pass
                    
                    # NO2
                    try:
                        no2_col = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2') \
                            .select('NO2_column_number_density') \
                            .filterDate(start_date, end_date) \
                            .filterBounds(ee_geometry)
                        
                        if no2_col.size().getInfo() > 0:
                            val = no2_col.mean().reduceRegion(
                                reducer=ee.Reducer.mean(),
                                geometry=ee_geometry,
                                scale=7500,
                                maxPixels=1e9,
                                bestEffort=True
                            ).get('NO2_column_number_density').getInfo()
                            if val:
                                monthly_data[month]['no2'].append(val)
                    except:
                        pass
                    
                    # Aerosol
                    try:
                        aerosol_col = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_AER_AI') \
                            .select('absorbing_aerosol_index') \
                            .filterDate(start_date, end_date) \
                            .filterBounds(ee_geometry)
                        
                        if aerosol_col.size().getInfo() > 0:
                            val = aerosol_col.mean().reduceRegion(
                                reducer=ee.Reducer.mean(),
                                geometry=ee_geometry,
                                scale=7500,
                                maxPixels=1e9,
                                bestEffort=True
                            ).get('absorbing_aerosol_index').getInfo()
                            if val:
                                monthly_data[month]['aerosol'].append(val)
                    except:
                        pass
            
            # Calculate monthly averages
            seasonal_data = {
                'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                'ndvi': [],
                'temperature': [],
                'precipitation': [],
                'co': [],
                'no2': [],
                'aerosol': []
            }
            
            for month in range(1, 13):
                for param in ['ndvi', 'temperature', 'precipitation', 'co', 'no2', 'aerosol']:
                    if monthly_data[month][param]:
                        avg = sum(monthly_data[month][param]) / len(monthly_data[month][param])
                        seasonal_data[param].append(round(avg, 6))
                    else:
                        seasonal_data[param].append(None)
            
            # Identify patterns
            patterns = self._identify_seasonal_patterns(seasonal_data)
            seasonal_data['patterns'] = patterns
            
            print(f"Seasonal analysis complete. Patterns identified.")
            
            return {'success': True, 'data': seasonal_data}
        
        except Exception as e:
            print(f"Seasonal analysis error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _identify_seasonal_patterns(self, seasonal_data):
        """Identify key seasonal patterns"""
        patterns = {}
        
        # Find peak months
        if seasonal_data['ndvi'] and any(seasonal_data['ndvi']):
            valid_ndvi = [(i, v) for i, v in enumerate(seasonal_data['ndvi']) if v is not None]
            if valid_ndvi:
                peak_idx = max(valid_ndvi, key=lambda x: x[1])[0]
                low_idx = min(valid_ndvi, key=lambda x: x[1])[0]
                patterns['vegetation_peak'] = seasonal_data['months'][peak_idx]
                patterns['vegetation_low'] = seasonal_data['months'][low_idx]
        
        if seasonal_data['temperature'] and any(seasonal_data['temperature']):
            valid_temp = [(i, v) for i, v in enumerate(seasonal_data['temperature']) if v is not None]
            if valid_temp:
                peak_idx = max(valid_temp, key=lambda x: x[1])[0]
                patterns['hottest_month'] = seasonal_data['months'][peak_idx]
        
        if seasonal_data['precipitation'] and any(seasonal_data['precipitation']):
            valid_precip = [(i, v) for i, v in enumerate(seasonal_data['precipitation']) if v is not None]
            if valid_precip:
                peak_idx = max(valid_precip, key=lambda x: x[1])[0]
                low_idx = min(valid_precip, key=lambda x: x[1])[0]
                patterns['wettest_month'] = seasonal_data['months'][peak_idx]
                patterns['driest_month'] = seasonal_data['months'][low_idx]
        
        if seasonal_data['co'] and any(seasonal_data['co']):
            valid_co = [(i, v) for i, v in enumerate(seasonal_data['co']) if v is not None]
            if valid_co:
                peak_idx = max(valid_co, key=lambda x: x[1])[0]
                patterns['highest_pollution'] = seasonal_data['months'][peak_idx]
        
        return patterns
    
    def _calculate_trends(self, annual_data):
        """Calculate trend statistics"""
        trends = {}
        
        for param in ['ndvi', 'temperature', 'precipitation']:
            values = [v for v in annual_data[param] if v is not None]
            
            if len(values) < 3:
                trends[param] = {'trend': 'insufficient_data', 'change': 0}
                continue
            
            # Simple linear trend
            n = len(values)
            x = list(range(n))
            y = values
            
            x_mean = sum(x) / n
            y_mean = sum(y) / n
            
            numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
            denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
            
            if denominator == 0:
                slope = 0
            else:
                slope = numerator / denominator
            
            # Interpret trend
            if param == 'ndvi':
                if slope > 0.001:
                    trend_dir = 'increasing'
                elif slope < -0.001:
                    trend_dir = 'decreasing'
                else:
                    trend_dir = 'stable'
                change = slope * 100  # Percentage per year
            
            elif param == 'temperature':
                if slope > 0.05:
                    trend_dir = 'warming'
                elif slope < -0.05:
                    trend_dir = 'cooling'
                else:
                    trend_dir = 'stable'
                change = slope  # Degrees per year
            
            else:  # precipitation
                if slope > 2:
                    trend_dir = 'increasing'
                elif slope < -2:
                    trend_dir = 'decreasing'
                else:
                    trend_dir = 'stable'
                change = slope  # mm per year
            
            trends[param] = {
                'trend': trend_dir,
                'change': round(change, 3)
            }
        
        return trends
    
    def get_heatmap_tiles(self, geometry, parameters):
        """Generate Earth Engine tile URLs for heatmaps"""
        try:
            if isinstance(geometry, dict):
                ee_geometry = ee.Geometry(geometry)
            else:
                ee_geometry = geometry
            
            tiles = {'success': True, 'tiles': {}}
            
            # Get bounds for centering
            bounds = ee_geometry.bounds().getInfo()
            coords = bounds['coordinates'][0]
            center = {
                'lat': (coords[0][1] + coords[2][1]) / 2,
                'lng': (coords[0][0] + coords[2][0]) / 2
            }
            tiles['center'] = center
            
            # NDVI Heatmap
            if 'ndvi' in parameters:
                ndvi = ee.ImageCollection('MODIS/006/MOD13Q1') \
                    .select('NDVI') \
                    .filterDate(self.start_date, self.end_date) \
                    .mean() \
                    .multiply(0.0001) \
                    .clip(ee_geometry)
                
                ndvi_vis = {
                    'min': 0,
                    'max': 1,
                    'palette': ['red', 'yellow', 'green', 'darkgreen']
                }
                tiles['tiles']['ndvi'] = ndvi.getMapId(ndvi_vis)
            
            # Temperature Heatmap
            if 'temperature' in parameters:
                temp = ee.ImageCollection('MODIS/006/MOD11A2') \
                    .select('LST_Day_1km') \
                    .filterDate(self.start_date, self.end_date) \
                    .mean() \
                    .multiply(0.02) \
                    .subtract(273.15) \
                    .clip(ee_geometry)
                
                temp_vis = {
                    'min': 10,
                    'max': 45,
                    'palette': ['blue', 'cyan', 'yellow', 'orange', 'red']
                }
                tiles['tiles']['temperature'] = temp.getMapId(temp_vis)
            
            # Precipitation Heatmap
            if 'precipitation' in parameters:
                precip = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
                    .select('precipitation') \
                    .filterDate(self.start_date, self.end_date) \
                    .sum() \
                    .clip(ee_geometry)
                
                precip_vis = {
                    'min': 0,
                    'max': 1000,
                    'palette': ['white', 'lightblue', 'blue', 'darkblue']
                }
                tiles['tiles']['precipitation'] = precip.getMapId(precip_vis)
            
            # CO Heatmap
            if 'co' in parameters:
                co = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_CO') \
                    .select('CO_column_number_density') \
                    .filterDate(self.start_date, self.end_date) \
                    .mean() \
                    .clip(ee_geometry)
                
                co_vis = {
                    'min': 0.01,
                    'max': 0.05,
                    'palette': ['blue', 'cyan', 'green', 'yellow', 'orange', 'red']
                }
                tiles['tiles']['co'] = co.getMapId(co_vis)
            
            return tiles
        
        except Exception as e:
            print(f"Heatmap tile generation error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _decode_land_cover(self, code):
        """Decode MODIS land cover codes"""
        land_cover_types = {
            1: "Evergreen Needleleaf Forest",
            2: "Evergreen Broadleaf Forest",
            3: "Deciduous Needleleaf Forest",
            4: "Deciduous Broadleaf Forest",
            5: "Mixed Forest",
            6: "Closed Shrublands",
            7: "Open Shrublands",
            8: "Woody Savannas",
            9: "Savannas",
            10: "Grasslands",
            11: "Permanent Wetlands",
            12: "Croplands",
            13: "Urban and Built-up",
            14: "Cropland/Natural Vegetation Mosaic",
            15: "Snow and Ice",
            16: "Barren or Sparsely Vegetated",
            17: "Water Bodies"
        }
        return land_cover_types.get(code, "Unknown")
