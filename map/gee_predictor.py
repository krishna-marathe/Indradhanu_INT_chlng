"""
Google Earth Engine Prediction Module
Forecasts environmental trends using historical satellite data
"""
import ee
import numpy as np
from datetime import datetime, timedelta
from scipy import stats


class GEEPredictor:
    """
    Prediction engine for environmental forecasting using GEE data
    """
    
    def __init__(self, gee_processor):
        """
        Initialize predictor with GEE processor instance
        
        Args:
            gee_processor: Instance of GEEProcessor
        """
        self.gee = gee_processor
    
    def predict_ndvi_trend(self, geometry, years_ahead=5, historical_years=10):
        """
        Predict NDVI (vegetation health) trend for future years
        
        Args:
            geometry: GeoJSON geometry
            years_ahead: Number of years to predict
            historical_years: Years of historical data to use
        
        Returns:
            dict: Prediction results with trend analysis
        """
        try:
            # Convert geometry
            if isinstance(geometry, dict):
                ee_geometry = ee.Geometry(geometry)
            else:
                ee_geometry = geometry
            
            current_year = datetime.now().year
            start_year = current_year - historical_years
            
            # Collect historical NDVI data
            years = []
            ndvi_values = []
            
            print(f"Collecting {historical_years} years of NDVI data...")
            
            for year in range(start_year, current_year):
                try:
                    ndvi_col = ee.ImageCollection('MODIS/006/MOD13Q1') \
                        .select('NDVI') \
                        .filterDate(f'{year}-01-01', f'{year}-12-31') \
                        .filterBounds(ee_geometry)
                    
                    if ndvi_col.size().getInfo() > 0:
                        ndvi_val = ndvi_col.mean().multiply(0.0001).reduceRegion(
                            reducer=ee.Reducer.mean(),
                            geometry=ee_geometry,
                            scale=250,
                            maxPixels=1e9
                        ).get('NDVI').getInfo()
                        
                        if ndvi_val:
                            years.append(year)
                            ndvi_values.append(ndvi_val)
                except Exception as e:
                    print(f"Error fetching NDVI for {year}: {e}")
                    continue
            
            if len(years) < 3:
                return {
                    'success': False,
                    'error': 'Insufficient historical data for prediction'
                }
            
            # Perform linear regression
            slope, intercept, r_value, p_value, std_err = stats.linregress(years, ndvi_values)
            
            # Generate predictions
            future_years = list(range(current_year, current_year + years_ahead + 1))
            predictions = [slope * year + intercept for year in future_years]
            
            # Calculate confidence intervals
            confidence_95 = 1.96 * std_err
            
            # Determine trend
            if slope > 0.001:
                trend = "improving"
                trend_description = "Vegetation health is expected to improve"
            elif slope < -0.001:
                trend = "declining"
                trend_description = "Vegetation health is expected to decline"
            else:
                trend = "stable"
                trend_description = "Vegetation health is expected to remain stable"
            
            return {
                'success': True,
                'parameter': 'NDVI',
                'historical_data': {
                    'years': years,
                    'values': [round(v, 4) for v in ndvi_values]
                },
                'predictions': {
                    'years': future_years,
                    'values': [round(v, 4) for v in predictions],
                    'confidence_interval': round(confidence_95, 4)
                },
                'trend_analysis': {
                    'trend': trend,
                    'slope': round(slope, 6),
                    'description': trend_description,
                    'r_squared': round(r_value ** 2, 4),
                    'p_value': round(p_value, 4),
                    'confidence': 'high' if r_value ** 2 > 0.7 else 'moderate' if r_value ** 2 > 0.4 else 'low'
                },
                'current_value': round(ndvi_values[-1], 4),
                'predicted_value_5y': round(predictions[5], 4) if len(predictions) > 5 else None
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def predict_temperature_trend(self, geometry, years_ahead=5, historical_years=10):
        """
        Predict temperature trend for future years
        
        Args:
            geometry: GeoJSON geometry
            years_ahead: Number of years to predict
            historical_years: Years of historical data to use
        
        Returns:
            dict: Temperature prediction results
        """
        try:
            if isinstance(geometry, dict):
                ee_geometry = ee.Geometry(geometry)
            else:
                ee_geometry = geometry
            
            current_year = datetime.now().year
            start_year = current_year - historical_years
            
            years = []
            temp_values = []
            
            print(f"Collecting {historical_years} years of temperature data...")
            
            for year in range(start_year, current_year):
                try:
                    temp_col = ee.ImageCollection('MODIS/006/MOD11A2') \
                        .select('LST_Day_1km') \
                        .filterDate(f'{year}-01-01', f'{year}-12-31') \
                        .filterBounds(ee_geometry)
                    
                    if temp_col.size().getInfo() > 0:
                        temp_val = temp_col.mean().multiply(0.02).subtract(273.15).reduceRegion(
                            reducer=ee.Reducer.mean(),
                            geometry=ee_geometry,
                            scale=1000,
                            maxPixels=1e9
                        ).get('LST_Day_1km').getInfo()
                        
                        if temp_val:
                            years.append(year)
                            temp_values.append(temp_val)
                except Exception as e:
                    print(f"Error fetching temperature for {year}: {e}")
                    continue
            
            if len(years) < 3:
                return {
                    'success': False,
                    'error': 'Insufficient historical data for prediction'
                }
            
            # Linear regression
            slope, intercept, r_value, p_value, std_err = stats.linregress(years, temp_values)
            
            # Predictions
            future_years = list(range(current_year, current_year + years_ahead + 1))
            predictions = [slope * year + intercept for year in future_years]
            
            confidence_95 = 1.96 * std_err
            
            # Trend analysis
            if slope > 0.05:
                trend = "warming"
                trend_description = f"Temperature is increasing by {abs(slope):.3f}°C per year"
            elif slope < -0.05:
                trend = "cooling"
                trend_description = f"Temperature is decreasing by {abs(slope):.3f}°C per year"
            else:
                trend = "stable"
                trend_description = "Temperature is relatively stable"
            
            return {
                'success': True,
                'parameter': 'Temperature',
                'unit': '°C',
                'historical_data': {
                    'years': years,
                    'values': [round(v, 2) for v in temp_values]
                },
                'predictions': {
                    'years': future_years,
                    'values': [round(v, 2) for v in predictions],
                    'confidence_interval': round(confidence_95, 2)
                },
                'trend_analysis': {
                    'trend': trend,
                    'rate_of_change': round(slope, 4),
                    'description': trend_description,
                    'r_squared': round(r_value ** 2, 4),
                    'confidence': 'high' if r_value ** 2 > 0.7 else 'moderate' if r_value ** 2 > 0.4 else 'low'
                },
                'current_value': round(temp_values[-1], 2),
                'predicted_value_5y': round(predictions[5], 2) if len(predictions) > 5 else None,
                'total_change_predicted': round(predictions[-1] - temp_values[-1], 2)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def predict_precipitation_trend(self, geometry, years_ahead=5, historical_years=10):
        """
        Predict precipitation trend for future years
        
        Args:
            geometry: GeoJSON geometry
            years_ahead: Number of years to predict
            historical_years: Years of historical data to use
        
        Returns:
            dict: Precipitation prediction results
        """
        try:
            if isinstance(geometry, dict):
                ee_geometry = ee.Geometry(geometry)
            else:
                ee_geometry = geometry
            
            current_year = datetime.now().year
            start_year = current_year - historical_years
            
            years = []
            precip_values = []
            
            print(f"Collecting {historical_years} years of precipitation data...")
            
            for year in range(start_year, current_year):
                try:
                    precip_col = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
                        .select('precipitation') \
                        .filterDate(f'{year}-01-01', f'{year}-12-31') \
                        .filterBounds(ee_geometry)
                    
                    if precip_col.size().getInfo() > 0:
                        precip_val = precip_col.sum().reduceRegion(
                            reducer=ee.Reducer.mean(),
                            geometry=ee_geometry,
                            scale=5000,
                            maxPixels=1e9
                        ).get('precipitation').getInfo()
                        
                        if precip_val:
                            years.append(year)
                            precip_values.append(precip_val)
                except Exception as e:
                    print(f"Error fetching precipitation for {year}: {e}")
                    continue
            
            if len(years) < 3:
                return {
                    'success': False,
                    'error': 'Insufficient historical data for prediction'
                }
            
            # Linear regression
            slope, intercept, r_value, p_value, std_err = stats.linregress(years, precip_values)
            
            # Predictions
            future_years = list(range(current_year, current_year + years_ahead + 1))
            predictions = [slope * year + intercept for year in future_years]
            
            confidence_95 = 1.96 * std_err
            
            # Trend analysis
            if slope > 10:
                trend = "increasing"
                trend_description = f"Rainfall is increasing by {abs(slope):.1f}mm per year"
            elif slope < -10:
                trend = "decreasing"
                trend_description = f"Rainfall is decreasing by {abs(slope):.1f}mm per year"
            else:
                trend = "stable"
                trend_description = "Rainfall patterns are relatively stable"
            
            return {
                'success': True,
                'parameter': 'Precipitation',
                'unit': 'mm/year',
                'historical_data': {
                    'years': years,
                    'values': [round(v, 1) for v in precip_values]
                },
                'predictions': {
                    'years': future_years,
                    'values': [round(v, 1) for v in predictions],
                    'confidence_interval': round(confidence_95, 1)
                },
                'trend_analysis': {
                    'trend': trend,
                    'rate_of_change': round(slope, 2),
                    'description': trend_description,
                    'r_squared': round(r_value ** 2, 4),
                    'confidence': 'high' if r_value ** 2 > 0.7 else 'moderate' if r_value ** 2 > 0.4 else 'low'
                },
                'current_value': round(precip_values[-1], 1),
                'predicted_value_5y': round(predictions[5], 1) if len(predictions) > 5 else None,
                'drought_risk': 'high' if predictions[-1] < 500 else 'moderate' if predictions[-1] < 800 else 'low'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def predict_comprehensive(self, geometry, years_ahead=5):
        """
        Generate comprehensive predictions for multiple parameters
        
        Args:
            geometry: GeoJSON geometry
            years_ahead: Number of years to predict
        
        Returns:
            dict: Comprehensive prediction results
        """
        print("🔮 Generating comprehensive environmental predictions...")
        
        results = {
            'success': True,
            'geometry': geometry,
            'prediction_horizon': years_ahead,
            'generated_at': datetime.now().isoformat(),
            'predictions': {}
        }
        
        # NDVI Prediction
        print("  📊 Predicting vegetation health (NDVI)...")
        ndvi_pred = self.predict_ndvi_trend(geometry, years_ahead)
        if ndvi_pred['success']:
            results['predictions']['ndvi'] = ndvi_pred
        
        # Temperature Prediction
        print("  🌡️ Predicting temperature trends...")
        temp_pred = self.predict_temperature_trend(geometry, years_ahead)
        if temp_pred['success']:
            results['predictions']['temperature'] = temp_pred
        
        # Precipitation Prediction
        print("  🌧️ Predicting precipitation patterns...")
        precip_pred = self.predict_precipitation_trend(geometry, years_ahead)
        if precip_pred['success']:
            results['predictions']['precipitation'] = precip_pred
        
        # Generate summary
        results['summary'] = self._generate_prediction_summary(results['predictions'])
        
        print("✅ Comprehensive predictions generated successfully!")
        
        return results
    
    def _generate_prediction_summary(self, predictions):
        """Generate a summary of all predictions"""
        summary = {
            'parameters_predicted': len(predictions),
            'key_findings': [],
            'risk_assessment': {}
        }
        
        # Analyze NDVI
        if 'ndvi' in predictions and predictions['ndvi']['success']:
            ndvi = predictions['ndvi']
            if ndvi['trend_analysis']['trend'] == 'declining':
                summary['key_findings'].append(
                    f"⚠️ Vegetation health declining at {abs(ndvi['trend_analysis']['slope']):.4f} per year"
                )
                summary['risk_assessment']['vegetation_degradation'] = 'high'
            elif ndvi['trend_analysis']['trend'] == 'improving':
                summary['key_findings'].append(
                    f"✅ Vegetation health improving at {ndvi['trend_analysis']['slope']:.4f} per year"
                )
                summary['risk_assessment']['vegetation_degradation'] = 'low'
        
        # Analyze Temperature
        if 'temperature' in predictions and predictions['temperature']['success']:
            temp = predictions['temperature']
            if temp['trend_analysis']['trend'] == 'warming':
                summary['key_findings'].append(
                    f"🌡️ Temperature rising by {temp['trend_analysis']['rate_of_change']:.3f}°C per year"
                )
                summary['risk_assessment']['heat_stress'] = 'high'
            elif temp['trend_analysis']['trend'] == 'cooling':
                summary['key_findings'].append(
                    f"❄️ Temperature decreasing by {abs(temp['trend_analysis']['rate_of_change']):.3f}°C per year"
                )
        
        # Analyze Precipitation
        if 'precipitation' in predictions and predictions['precipitation']['success']:
            precip = predictions['precipitation']
            if precip['trend_analysis']['trend'] == 'decreasing':
                summary['key_findings'].append(
                    f"💧 Rainfall decreasing by {abs(precip['trend_analysis']['rate_of_change']):.1f}mm per year"
                )
                summary['risk_assessment']['drought'] = precip.get('drought_risk', 'moderate')
            elif precip['trend_analysis']['trend'] == 'increasing':
                summary['key_findings'].append(
                    f"🌧️ Rainfall increasing by {precip['trend_analysis']['rate_of_change']:.1f}mm per year"
                )
                summary['risk_assessment']['flooding'] = 'moderate'
        
        return summary
