"""
LLM Analyzer for Environmental Data
Uses Google Gemini for AI-powered insights
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

class LLMAnalyzer:
    def __init__(self):
        """Initialize the LLM analyzer with Gemini API"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_environmental_data(self, data):
        """
        Analyze environmental data and generate insights
        
        Args:
            data (dict): Environmental metrics including NDVI, temperature, precipitation, land cover
        
        Returns:
            dict: Analysis results with insights and recommendations
        """
        prompt = self._create_analysis_prompt(data)
        
        try:
            response = self.model.generate_content(prompt)
            
            # Generate structured insights
            structured_insights = self._generate_structured_insights(data)
            
            analysis = self._parse_response(response.text)
            return {
                'success': True,
                'analysis': analysis,
                'raw_response': response.text,
                'structured_insights': structured_insights,
                'alerts': self._generate_alerts(data),
                'health_score': self._calculate_health_score(data)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'analysis': None
            }
    
    def _generate_structured_insights(self, data):
        """Generate structured, real-time insights based on data values"""
        insights = {
            'vegetation': self._analyze_vegetation(data),
            'climate': self._analyze_climate(data),
            'air_quality': self._analyze_air_quality(data),
            'water': self._analyze_water(data),
            'advanced': self._analyze_advanced_parameters(data)
        }
        return insights
    
    def _analyze_advanced_parameters(self, data):
        """Analyze advanced climate parameters"""
        insights = []
        
        # Land use change
        land_use = data.get('land_use_change')
        if land_use and land_use.get('changed'):
            insights.append(f"🏗️ Land use changed: {land_use['past']} → {land_use['recent']}")
        
        # Urban heat island
        uhi = data.get('urban_heat_island')
        if uhi:
            intensity = uhi.get('intensity', 0)
            if intensity > 5:
                insights.append(f"🌡️ Strong urban heat island effect ({intensity}°C) - Cities heating faster than surroundings")
            elif intensity > 2:
                insights.append(f"Moderate urban heat island ({intensity}°C)")
        
        # Water body change
        water = data.get('water_body_change')
        if water:
            occurrence = water.get('water_occurrence', 0)
            status = water.get('status', '')
            if occurrence > 75:
                insights.append(f"💧 Permanent water body detected ({occurrence}% occurrence)")
            elif occurrence > 25:
                insights.append(f"💧 Seasonal water body ({occurrence}% occurrence)")
            elif occurrence < 5:
                insights.append(f"⚠️ Minimal water presence ({occurrence}%) - Groundwater recharge concern")
        
        # Rainfall trend
        rainfall = data.get('rainfall_trend')
        if rainfall:
            trend = rainfall.get('trend', '')
            change = rainfall.get('change_rate', 0)
            if trend == 'decreasing':
                insights.append(f"📉 Monsoon shift detected: Rainfall declining by {abs(change):.1f}mm/year")
            elif trend == 'increasing':
                insights.append(f"📈 Rainfall increasing by {change:.1f}mm/year")
        
        # Vulnerability
        vuln = data.get('vulnerability')
        if vuln:
            drought_risk = vuln.get('drought_risk', '')
            flood_risk = vuln.get('flood_risk', '')
            
            if drought_risk == 'high':
                insights.append(f"🌵 HIGH DROUGHT RISK - Community vulnerable to water stress")
            if flood_risk == 'high':
                insights.append(f"🌊 HIGH FLOOD RISK - Sensitive region, prepare for extreme rainfall")
        
        return {'insights': insights}
    
    def _analyze_vegetation(self, data):
        """Analyze vegetation health"""
        ndvi = data.get('ndvi')
        if ndvi is None:
            return {'status': 'unknown', 'message': 'No vegetation data available'}
        
        if ndvi > 0.6:
            status = 'excellent'
            message = f'Dense, healthy vegetation (NDVI: {ndvi:.3f}). Excellent photosynthetic activity.'
        elif ndvi > 0.4:
            status = 'good'
            message = f'Moderate vegetation cover (NDVI: {ndvi:.3f}). Healthy but not dense.'
        elif ndvi > 0.2:
            status = 'fair'
            message = f'Sparse vegetation (NDVI: {ndvi:.3f}). May indicate stress or seasonal dormancy.'
        elif ndvi > 0:
            status = 'poor'
            message = f'Very sparse vegetation (NDVI: {ndvi:.3f}). Possible degradation or barren land.'
        else:
            status = 'critical'
            message = f'No vegetation detected (NDVI: {ndvi:.3f}). Water, snow, or bare soil.'
        
        return {'status': status, 'message': message, 'value': ndvi}
    
    def _analyze_climate(self, data):
        """Analyze climate conditions"""
        temp = data.get('temperature')
        air_temp = data.get('air_temperature')
        precip = data.get('precipitation')
        
        insights = []
        
        if temp is not None:
            if temp > 35:
                insights.append(f'⚠️ High surface temperature ({temp:.1f}°C) - Heat stress risk')
            elif temp > 25:
                insights.append(f'Warm conditions ({temp:.1f}°C) - Suitable for most crops')
            elif temp < 0:
                insights.append(f'❄️ Freezing conditions ({temp:.1f}°C) - Frost risk')
            else:
                insights.append(f'Moderate temperature ({temp:.1f}°C)')
        
        if air_temp is not None:
            if air_temp > 30:
                insights.append(f'High air temperature ({air_temp:.1f}°C) - Increased evaporation')
            elif air_temp < 5:
                insights.append(f'Cold air temperature ({air_temp:.1f}°C) - Reduced growth')
        
        if precip is not None:
            if precip > 1000:
                insights.append(f'💧 High rainfall ({precip:.0f}mm) - Abundant water, possible flooding')
            elif precip > 500:
                insights.append(f'Adequate rainfall ({precip:.0f}mm) - Good water availability')
            elif precip > 200:
                insights.append(f'Moderate rainfall ({precip:.0f}mm) - May need irrigation')
            else:
                insights.append(f'⚠️ Low rainfall ({precip:.0f}mm) - Drought risk, irrigation needed')
        
        return {
            'insights': insights,
            'temperature': temp,
            'air_temperature': air_temp,
            'precipitation': precip
        }
    
    def _analyze_air_quality(self, data):
        """Analyze air quality and pollution levels"""
        insights = []
        status = 'good'
        
        co_concentration = data.get('co_concentration')
        no2 = data.get('no2')
        so2 = data.get('so2')
        ozone = data.get('ozone')
        aerosol = data.get('aerosol')
        
        if co_concentration is not None:
            # CO levels interpretation (mol/m²)
            if co_concentration > 0.04:
                insights.append(f'🚨 Very High CO levels ({co_concentration:.4f} mol/m²) - Severe pollution from vehicles/industry')
                status = 'poor'
            elif co_concentration > 0.03:
                insights.append(f'⚠️ High CO levels ({co_concentration:.4f} mol/m²) - Significant pollution detected')
                status = 'moderate'
            elif co_concentration > 0.02:
                insights.append(f'Moderate CO levels ({co_concentration:.4f} mol/m²) - Some pollution present')
                status = 'moderate'
            else:
                insights.append(f'✅ Low CO levels ({co_concentration:.4f} mol/m²) - Good air quality')
        
        if no2 is not None:
            if no2 > 1e-4:
                insights.append(f'🏭 High NO2 levels - Industrial/traffic pollution detected')
                status = 'poor'
            elif no2 > 5e-5:
                insights.append(f'Moderate NO2 levels - Some pollution present')
                if status == 'good':
                    status = 'moderate'
        
        if so2 is not None and so2 > 1e-4:
            insights.append(f'⚠️ Elevated SO2 - Possible industrial emissions')
            status = 'poor'
        
        if aerosol is not None:
            if abs(aerosol) > 2:
                insights.append(f'High aerosol index ({aerosol:.2f}) - Dust or smoke present')
                if status == 'good':
                    status = 'moderate'
        
        if not insights:
            insights.append('✅ Air quality appears good - Low pollution levels')
        
        return {
            'status': status,
            'insights': insights,
            'pollutants': {
                'co_concentration': co_concentration,
                'no2': no2,
                'so2': so2,
                'ozone': ozone,
                'aerosol': aerosol
            }
        }
    
    def _analyze_water(self, data):
        """Analyze water and soil conditions"""
        insights = []
        
        soil_moisture = data.get('soil_moisture')
        evapotranspiration = data.get('evapotranspiration')
        
        if soil_moisture is not None:
            if soil_moisture > 30:
                insights.append(f'💧 High soil moisture ({soil_moisture:.1f}%) - Well hydrated')
            elif soil_moisture > 15:
                insights.append(f'Adequate soil moisture ({soil_moisture:.1f}%)')
            elif soil_moisture > 5:
                insights.append(f'⚠️ Low soil moisture ({soil_moisture:.1f}%) - Irrigation recommended')
            else:
                insights.append(f'🌵 Very dry soil ({soil_moisture:.1f}%) - Severe water stress')
        
        if evapotranspiration is not None:
            if evapotranspiration > 100:
                insights.append(f'High evapotranspiration ({evapotranspiration:.0f}mm) - High water demand')
            elif evapotranspiration > 50:
                insights.append(f'Moderate evapotranspiration ({evapotranspiration:.0f}mm)')
            else:
                insights.append(f'Low evapotranspiration ({evapotranspiration:.0f}mm)')
        
        return {
            'insights': insights,
            'soil_moisture': soil_moisture,
            'evapotranspiration': evapotranspiration
        }
    
    def _generate_alerts(self, data):
        """Generate critical alerts based on data"""
        alerts = []
        
        # Vegetation alerts
        ndvi = data.get('ndvi')
        if ndvi is not None and ndvi < 0.2:
            alerts.append({
                'level': 'warning',
                'category': 'vegetation',
                'message': 'Low vegetation health detected - possible degradation'
            })
        
        # Temperature alerts
        temp = data.get('temperature')
        if temp is not None and temp > 40:
            alerts.append({
                'level': 'critical',
                'category': 'climate',
                'message': f'Extreme heat detected ({temp:.1f}°C) - Heat stress risk'
            })
        
        # Precipitation alerts
        precip = data.get('precipitation')
        if precip is not None and precip < 200:
            alerts.append({
                'level': 'warning',
                'category': 'climate',
                'message': f'Low precipitation ({precip:.0f}mm) - Drought conditions'
            })
        
        # Air quality alerts
        co_concentration = data.get('co_concentration')
        if co_concentration is not None and co_concentration > 0.04:
            alerts.append({
                'level': 'critical',
                'category': 'air_quality',
                'message': f'Very high CO pollution ({co_concentration:.4f} mol/m²) - Health risk'
            })
        
        no2 = data.get('no2')
        if no2 is not None and no2 > 1e-4:
            alerts.append({
                'level': 'warning',
                'category': 'air_quality',
                'message': 'High NO2 pollution detected - Health concerns'
            })
        
        return alerts
    
    def _calculate_health_score(self, data):
        """Calculate overall environmental health score (0-100)"""
        scores = []
        
        # Vegetation score
        ndvi = data.get('ndvi')
        if ndvi is not None:
            veg_score = min(100, max(0, ndvi * 150))  # Scale NDVI to 0-100
            scores.append(veg_score)
        
        # Air quality score (inverse of pollution)
        co_concentration = data.get('co_concentration')
        if co_concentration is not None:
            # CO: 0.01-0.05 mol/m² typical range
            air_score = max(0, 100 - (co_concentration * 2000))  # Lower pollution = higher score
            scores.append(air_score)
        
        # Water availability score
        precip = data.get('precipitation')
        if precip is not None:
            water_score = min(100, (precip / 10))  # Scale precipitation
            scores.append(water_score)
        
        if scores:
            overall_score = sum(scores) / len(scores)
            return {
                'score': round(overall_score, 1),
                'grade': self._get_grade(overall_score),
                'components': len(scores)
            }
        
        return {'score': None, 'grade': 'Unknown', 'components': 0}
    
    def _get_grade(self, score):
        """Convert score to letter grade"""
        if score >= 90:
            return 'A - Excellent'
        elif score >= 80:
            return 'B - Good'
        elif score >= 70:
            return 'C - Fair'
        elif score >= 60:
            return 'D - Poor'
        else:
            return 'F - Critical'
    
    def _create_analysis_prompt(self, data):
        """Create a detailed, data-driven prompt for environmental analysis"""
        
        # Get advanced parameters
        land_use_change = data.get('land_use_change', {})
        uhi = data.get('urban_heat_island', {})
        water_change = data.get('water_body_change', {})
        rainfall_trend = data.get('rainfall_trend', {})
        vulnerability = data.get('vulnerability', {})
        
        prompt = f"""
You are an expert environmental scientist. Provide a DETAILED, DATA-DRIVEN analysis with specific numbers and actionable insights.

**AREA PROFILE:**
- Size: {data.get('area', 'N/A')} km²
- Land Cover: {data.get('land_cover', 'N/A')}

**VEGETATION STATUS:**
- NDVI: {data.get('ndvi', 'N/A')} (Scale: -1 to 1)
- Status: {"Dense vegetation" if data.get('ndvi', 0) > 0.6 else "Moderate" if data.get('ndvi', 0) > 0.4 else "Sparse" if data.get('ndvi', 0) > 0.2 else "Minimal"}

**CLIMATE DATA:**
- Surface Temp: {data.get('temperature', 'N/A')}°C
- Air Temp: {data.get('air_temperature', 'N/A')}°C
- Precipitation: {data.get('precipitation', 'N/A')} mm
- Soil Moisture: {data.get('soil_moisture', 'N/A')}%

**AIR QUALITY:**
- CO: {data.get('co_concentration', 'N/A')} mol/m²
- NO2: {data.get('no2', 'N/A')} mol/m²
- SO2: {data.get('so2', 'N/A')} mol/m²

**PROVIDE ANALYSIS IN THESE SECTIONS:**

1. **EXECUTIVE SUMMARY** (2-3 sentences): Overall status and key finding

2. **VEGETATION & ECOSYSTEM**: Interpret NDVI, land cover, ecosystem health

3. **CLIMATE & WATER**: Temperature patterns, precipitation, drought/flood risk

4. **AIR QUALITY**: Pollution levels, health impacts, sources

5. **KEY RISKS** (List 3-5 specific risks with severity)

6. **RECOMMENDATIONS** (Immediate, short-term, long-term actions)

Be specific with numbers. Provide context for Indian conditions.
"""
        return prompt
    
    def _parse_response(self, response_text):
        """Parse the LLM response into structured data"""
        return {
            'summary': response_text,
            'timestamp': self._get_timestamp()
        }
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def generate_comparison(self, data_list):
        """
        Compare multiple areas
        
        Args:
            data_list (list): List of environmental data dictionaries
        
        Returns:
            dict: Comparative analysis
        """
        if len(data_list) < 2:
            return {
                'success': False,
                'error': 'Need at least 2 areas to compare'
            }
        
        prompt = f"""
Compare the following environmental areas and identify key differences:

"""
        for i, data in enumerate(data_list, 1):
            prompt += f"""
Area {i}:
- NDVI: {data.get('ndvi', 'N/A')}
- Temperature: {data.get('temperature', 'N/A')}°C
- Precipitation: {data.get('precipitation', 'N/A')} mm
- Land Cover: {data.get('land_cover', 'N/A')}
- CO2: {data.get('co2', 'N/A')} ppm
- NO2: {data.get('no2', 'N/A')} mol/m²
- Soil Moisture: {data.get('soil_moisture', 'N/A')} %

"""
        
        prompt += """
Provide a comparative analysis highlighting:
1. Which area has better vegetation health
2. Climate differences
3. Land use patterns
4. Recommendations for each area
"""
        
        try:
            response = self.model.generate_content(prompt)
            return {
                'success': True,
                'comparison': response.text
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_seasonal_patterns(self, seasonal_data):
        """
        Analyze seasonal patterns and provide insights
        
        Args:
            seasonal_data (dict): Seasonal pattern data for all parameters
        
        Returns:
            dict: Seasonal analysis insights
        """
        patterns = seasonal_data.get('patterns', {})
        months = seasonal_data.get('months', [])
        
        prompt = f"""
Analyze the following seasonal patterns across multiple environmental parameters:

**SEASONAL PATTERNS IDENTIFIED:**
- Vegetation Peak: {patterns.get('vegetation_peak', 'N/A')}
- Vegetation Low: {patterns.get('vegetation_low', 'N/A')}
- Hottest Month: {patterns.get('hottest_month', 'N/A')}
- Wettest Month: {patterns.get('wettest_month', 'N/A')}
- Driest Month: {patterns.get('driest_month', 'N/A')}
- Highest Pollution: {patterns.get('highest_pollution', 'N/A')}

**MONTHLY DATA AVAILABLE FOR:**
- NDVI (Vegetation Health)
- Temperature
- Precipitation
- CO (Carbon Monoxide)
- NO2 (Nitrogen Dioxide)
- Aerosol Index

**PROVIDE DETAILED SEASONAL ANALYSIS:**

1. **GROWING SEASON ANALYSIS**
   - Identify the growing season months
   - Explain vegetation cycles
   - Agricultural implications

2. **MONSOON & RAINFALL PATTERNS**
   - Monsoon timing and intensity
   - Dry season characteristics
   - Water availability throughout the year

3. **TEMPERATURE VARIATIONS**
   - Summer and winter patterns
   - Heat stress periods
   - Comfortable months

4. **AIR QUALITY SEASONALITY**
   - When pollution is highest/lowest
   - Seasonal factors (crop burning, winter inversion, etc.)
   - Health advisory for different months

5. **SEASONAL RISKS**
   - Drought-prone months
   - Flood risk periods
   - Heat wave timing
   - Air pollution episodes

6. **MONTH-BY-MONTH RECOMMENDATIONS**
   - Best months for outdoor activities
   - Agricultural calendar
   - Health precautions by season
   - Environmental management priorities

Provide specific, actionable insights for planning and decision-making.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return {
                'success': True,
                'insights': response.text,
                'patterns': patterns,
                'timestamp': self._get_timestamp()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_trends(self, trend_data):
        """
        Analyze historical trends and provide insights
        
        Args:
            trend_data (dict): Historical trend data
        
        Returns:
            dict: Trend analysis insights
        """
        trends = trend_data.get('trends', {})
        years = trend_data.get('years', [])
        
        # Generate structured trend insights
        structured_insights = self._analyze_trend_patterns(trend_data)
        
        prompt = f"""
Analyze the following environmental trends over {len(years)} years ({years[0]}-{years[-1]}):

**NDVI (Vegetation) Trend:**
- Direction: {trends.get('ndvi', {}).get('trend', 'N/A')}
- Change Rate: {trends.get('ndvi', {}).get('change', 'N/A')}% per year

**Temperature Trend:**
- Direction: {trends.get('temperature', {}).get('trend', 'N/A')}
- Change Rate: {trends.get('temperature', {}).get('change', 'N/A')}°C per year

**Precipitation Trend:**
- Direction: {trends.get('precipitation', {}).get('trend', 'N/A')}
- Change Rate: {trends.get('precipitation', {}).get('change', 'N/A')} mm per year

**Analysis Requirements:**
1. Interpret what these trends mean for the environment
2. Identify any concerning patterns or positive developments
3. Explain potential causes of these trends
4. Predict likely future scenarios if trends continue
5. Provide actionable recommendations for land management
6. Assess climate change impacts based on these trends

Provide a comprehensive analysis in clear, structured format.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return {
                'success': True,
                'insights': response.text,
                'structured_insights': structured_insights,
                'timestamp': self._get_timestamp()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _analyze_trend_patterns(self, trend_data):
        """Analyze trend patterns and generate real-time insights"""
        trends = trend_data.get('trends', {})
        years = trend_data.get('years', [])
        
        insights = {
            'summary': [],
            'concerns': [],
            'positives': [],
            'predictions': []
        }
        
        # NDVI trend analysis
        ndvi_trend = trends.get('ndvi', {})
        if ndvi_trend.get('trend') == 'increasing':
            insights['positives'].append(f"✅ Vegetation improving by {abs(ndvi_trend.get('change', 0)):.2f}% per year")
            insights['predictions'].append("Continued greening expected if current conditions persist")
        elif ndvi_trend.get('trend') == 'decreasing':
            insights['concerns'].append(f"⚠️ Vegetation declining by {abs(ndvi_trend.get('change', 0)):.2f}% per year")
            insights['predictions'].append("Risk of further degradation without intervention")
        else:
            insights['summary'].append("Vegetation health remains stable")
        
        # Temperature trend analysis
        temp_trend = trends.get('temperature', {})
        if temp_trend.get('trend') == 'warming':
            change = abs(temp_trend.get('change', 0))
            insights['concerns'].append(f"🌡️ Warming trend: +{change:.2f}°C per year")
            if change > 0.1:
                insights['concerns'].append("⚠️ Rapid warming detected - Climate change signal")
            insights['predictions'].append(f"Temperature could increase by {change * 10:.1f}°C over next decade")
        elif temp_trend.get('trend') == 'cooling':
            insights['summary'].append(f"Cooling trend: {temp_trend.get('change', 0):.2f}°C per year")
        
        # Precipitation trend analysis
        precip_trend = trends.get('precipitation', {})
        if precip_trend.get('trend') == 'decreasing':
            change = abs(precip_trend.get('change', 0))
            insights['concerns'].append(f"💧 Declining rainfall: -{change:.1f}mm per year")
            if change > 10:
                insights['concerns'].append("⚠️ Significant drying trend - Drought risk increasing")
            insights['predictions'].append("Water stress likely to intensify")
        elif precip_trend.get('trend') == 'increasing':
            insights['positives'].append(f"💧 Increasing rainfall: +{abs(precip_trend.get('change', 0)):.1f}mm per year")
        
        # Combined analysis
        if ndvi_trend.get('trend') == 'decreasing' and temp_trend.get('trend') == 'warming':
            insights['concerns'].append("🚨 Combined stress: Warming + vegetation decline")
        
        if precip_trend.get('trend') == 'decreasing' and temp_trend.get('trend') == 'warming':
            insights['concerns'].append("🚨 Drought conditions intensifying")
        
        return insights
