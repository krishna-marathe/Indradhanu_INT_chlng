"""
Flask Application for Environmental Analysis
Interactive map selection and AI-powered insights
"""
from flask import Flask, render_template, request, jsonify
from llm_analyzer import LLMAnalyzer
from gee_processor import GEEProcessor
from gee_predictor import GEEPredictor
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='.')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize processors
gee_processor = None
gee_predictor = None
llm_analyzer = None

try:
    print("Initializing GEE Processor...")
    gee_processor = GEEProcessor()
    print("✓ GEE Processor initialized")
    
    print("Initializing GEE Predictor...")
    gee_predictor = GEEPredictor(gee_processor)
    print("✓ GEE Predictor initialized")
except Exception as e:
    print(f"✗ GEE Initialization error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("Initializing LLM Analyzer...")
    llm_analyzer = LLMAnalyzer()
    print("✓ LLM Analyzer initialized")
except Exception as e:
    print(f"✗ LLM Initialization error: {e}")
    import traceback
    traceback.print_exc()

if gee_processor and gee_predictor and llm_analyzer:
    print("✓ All processors initialized successfully")
else:
    print("⚠ Warning: Some processors failed to initialize")

@app.route('/')
def index():
    """Render the main dashboard"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_area():
    """
    Analyze a selected area on the map
    
    Expected JSON:
    {
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[lon, lat], ...]]
        }
    }
    """
    try:
        data = request.get_json()
        geometry = data.get('geometry')
        
        if not geometry:
            return jsonify({
                'success': False,
                'error': 'No geometry provided'
            }), 400
        
        # Extract environmental data
        if not gee_processor:
            return jsonify({
                'success': False,
                'error': 'GEE processor not initialized'
            }), 500
        
        gee_result = gee_processor.extract_data(geometry)
        
        if not gee_result['success']:
            return jsonify(gee_result), 500
        
        # Analyze with LLM
        if not llm_analyzer:
            return jsonify({
                'success': False,
                'error': 'LLM analyzer not initialized'
            }), 500
        
        analysis_result = llm_analyzer.analyze_environmental_data(gee_result['data'])
        
        # Combine results
        response = {
            'success': True,
            'environmental_data': gee_result['data'],
            'ai_analysis': analysis_result.get('analysis'),
            'raw_analysis': analysis_result.get('raw_response')
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/compare', methods=['POST'])
def compare_areas():
    """
    Compare multiple selected areas
    
    Expected JSON:
    {
        "areas": [
            {"geometry": {...}},
            {"geometry": {...}}
        ]
    }
    """
    try:
        data = request.get_json()
        areas = data.get('areas', [])
        
        if len(areas) < 2:
            return jsonify({
                'success': False,
                'error': 'Need at least 2 areas to compare'
            }), 400
        
        # Extract data for all areas
        area_data = []
        for area in areas:
            result = gee_processor.extract_data(area['geometry'])
            if result['success']:
                area_data.append(result['data'])
        
        # Generate comparison
        comparison = llm_analyzer.generate_comparison(area_data)
        
        return jsonify({
            'success': True,
            'areas_data': area_data,
            'comparison': comparison
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/historical-trends', methods=['POST'])
def historical_trends():
    """
    Get historical trends for selected area
    
    Expected JSON:
    {
        "geometry": {...},
        "start_year": 2015,
        "end_year": 2024
    }
    """
    try:
        data = request.get_json()
        geometry = data.get('geometry')
        start_year = data.get('start_year', 2015)
        end_year = data.get('end_year', 2024)
        
        if not geometry:
            return jsonify({'success': False, 'error': 'No geometry provided'}), 400
        
        if not gee_processor:
            return jsonify({'success': False, 'error': 'GEE processor not initialized'}), 500
        
        # Get historical data
        trends = gee_processor.get_historical_trends(geometry, start_year, end_year)
        
        # Generate AI insights on trends
        if llm_analyzer and trends.get('success'):
            insights = llm_analyzer.analyze_trends(trends['data'])
            trends['ai_insights'] = insights
        
        return jsonify(trends)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/time-series', methods=['POST'])
def time_series():
    """
    Get time series data for specific parameters
    
    Expected JSON:
    {
        "geometry": {...},
        "parameters": ["ndvi", "temperature", "precipitation"],
        "start_year": 2015,
        "end_year": 2024
    }
    """
    try:
        data = request.get_json()
        geometry = data.get('geometry')
        parameters = data.get('parameters', ['ndvi', 'temperature', 'precipitation'])
        start_year = data.get('start_year', 2015)
        end_year = data.get('end_year', 2024)
        
        if not geometry:
            return jsonify({'success': False, 'error': 'No geometry provided'}), 400
        
        if not gee_processor:
            return jsonify({'success': False, 'error': 'GEE processor not initialized'}), 500
        
        # Get time series data
        time_series_data = gee_processor.get_time_series(geometry, parameters, start_year, end_year)
        
        return jsonify(time_series_data)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/seasonal-analysis', methods=['POST'])
def seasonal_analysis():
    """
    Get comprehensive seasonal patterns analysis
    
    Expected JSON:
    {
        "geometry": {...},
        "years": 5
    }
    """
    try:
        data = request.get_json()
        geometry = data.get('geometry')
        years = data.get('years', 5)
        
        if not geometry:
            return jsonify({'success': False, 'error': 'No geometry provided'}), 400
        
        if not gee_processor:
            return jsonify({'success': False, 'error': 'GEE processor not initialized'}), 500
        
        # Get seasonal patterns for all parameters
        seasonal_result = gee_processor.get_seasonal_patterns(geometry, years)
        
        if not seasonal_result['success']:
            return jsonify(seasonal_result), 500
        
        # Generate AI insights on seasonal patterns
        if llm_analyzer:
            insights = llm_analyzer.analyze_seasonal_patterns(seasonal_result['data'])
            seasonal_result['ai_insights'] = insights
        
        return jsonify(seasonal_result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export-data', methods=['POST'])
def export_data():
    """
    Export analysis data in various formats
    
    Expected JSON:
    {
        "geometry": {...},
        "format": "csv" | "json" | "excel"
    }
    """
    try:
        data = request.get_json()
        geometry = data.get('geometry')
        export_format = data.get('format', 'json')
        
        if not geometry:
            return jsonify({'success': False, 'error': 'No geometry provided'}), 400
        
        if not gee_processor:
            return jsonify({'success': False, 'error': 'GEE processor not initialized'}), 500
        
        # Get comprehensive data
        result = gee_processor.extract_data(geometry)
        
        if export_format == 'csv':
            csv_data = _convert_to_csv(result['data'])
            return jsonify({'success': True, 'data': csv_data, 'format': 'csv'})
        elif export_format == 'json':
            return jsonify({'success': True, 'data': result['data'], 'format': 'json'})
        else:
            return jsonify({'success': False, 'error': 'Unsupported format'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def _convert_to_csv(data):
    """Convert data dictionary to CSV format"""
    csv_lines = ["Parameter,Value,Unit,Dataset"]
    
    # Vegetation & Climate
    csv_lines.append(f"NDVI,{data.get('ndvi', 'N/A')},,MODIS MOD13Q1 (250m)")
    csv_lines.append(f"Land Surface Temperature,{data.get('temperature', 'N/A')},°C,MODIS MOD11A2 (1km)")
    csv_lines.append(f"Air Temperature,{data.get('air_temperature', 'N/A')},°C,ERA5-Land (10km)")
    csv_lines.append(f"Precipitation,{data.get('precipitation', 'N/A')},mm,CHIRPS Daily (5km)")
    csv_lines.append(f"Land Cover,{data.get('land_cover', 'N/A')},,MODIS MCD12Q1 (500m)")
    
    # Air Quality
    csv_lines.append(f"CO (Carbon Monoxide),{data.get('co_concentration', 'N/A')},mol/m²,Sentinel-5P TROPOMI (5-10km)")
    csv_lines.append(f"NO2,{data.get('no2', 'N/A')},mol/m²,Sentinel-5P (5-10km)")
    csv_lines.append(f"SO2,{data.get('so2', 'N/A')},mol/m²,Sentinel-5P (5-10km)")
    csv_lines.append(f"O3,{data.get('ozone', 'N/A')},mol/m²,Sentinel-5P (5-10km)")
    csv_lines.append(f"Aerosol Index,{data.get('aerosol', 'N/A')},,Sentinel-5P (5-10km)")
    
    # Soil & Water
    csv_lines.append(f"Soil Moisture,{data.get('soil_moisture', 'N/A')},%,SMAP (10km)")
    csv_lines.append(f"Evapotranspiration,{data.get('evapotranspiration', 'N/A')},mm,MODIS MOD16A2 (1km)")
    
    # Advanced Climate Parameters
    land_use = data.get('land_use_change')
    if land_use:
        csv_lines.append(f"Land Use Change,{land_use.get('changed', False)},,MODIS MCD12Q1")
        if land_use.get('changed'):
            csv_lines.append(f"Land Use Past,{land_use.get('past', 'N/A')},,")
            csv_lines.append(f"Land Use Recent,{land_use.get('recent', 'N/A')},,")
    
    uhi = data.get('urban_heat_island')
    if uhi:
        csv_lines.append(f"Urban Heat Island Intensity,{uhi.get('intensity', 'N/A')},°C,MODIS MOD11A2")
    
    water = data.get('water_body_change')
    if water:
        csv_lines.append(f"Water Occurrence,{water.get('water_occurrence', 'N/A')},%,JRC Global Surface Water")
        csv_lines.append(f"Water Status,{water.get('status', 'N/A')},,")
    
    rainfall = data.get('rainfall_trend')
    if rainfall:
        csv_lines.append(f"Rainfall Trend,{rainfall.get('trend', 'N/A')},,CHIRPS (10-year)")
        csv_lines.append(f"Rainfall Change Rate,{rainfall.get('change_rate', 'N/A')},mm/year,")
    
    vuln = data.get('vulnerability')
    if vuln:
        csv_lines.append(f"Drought Risk,{vuln.get('drought_risk', 'N/A')},,SMAP + CHIRPS")
        csv_lines.append(f"Flood Risk,{vuln.get('flood_risk', 'N/A')},,")
    
    # Metadata
    csv_lines.append(f"Area,{data.get('area', 'N/A')},km²,")
    csv_lines.append(f"Data Availability,{data.get('data_availability', 'N/A')},,")
    
    return "\n".join(csv_lines)

@app.route('/api/heatmap-tiles', methods=['POST'])
def get_heatmap_tiles():
    """
    Get Earth Engine tile URLs for heatmaps
    
    Expected JSON:
    {
        "geometry": {...},
        "parameters": ["ndvi", "temperature", "precipitation", "co"]
    }
    """
    try:
        data = request.get_json()
        geometry = data.get('geometry')
        parameters = data.get('parameters', ['ndvi', 'temperature', 'precipitation', 'co'])
        
        if not geometry:
            return jsonify({'success': False, 'error': 'No geometry provided'}), 400
        
        if not gee_processor:
            return jsonify({'success': False, 'error': 'GEE processor not initialized'}), 500
        
        # Get tile URLs for each parameter
        tiles = gee_processor.get_heatmap_tiles(geometry, parameters)
        
        return jsonify(tiles)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/predict/comprehensive', methods=['POST'])
def predict_comprehensive():
    """
    Generate comprehensive environmental predictions
    
    Expected JSON:
    {
        "geometry": {...},
        "years_ahead": 5
    }
    """
    try:
        data = request.get_json()
        geometry = data.get('geometry')
        years_ahead = data.get('years_ahead', 5)
        
        if not geometry:
            return jsonify({
                'success': False,
                'error': 'No geometry provided'
            }), 400
        
        if not gee_predictor:
            return jsonify({
                'success': False,
                'error': 'GEE predictor not initialized'
            }), 500
        
        # Generate predictions
        predictions = gee_predictor.predict_comprehensive(geometry, years_ahead)
        
        return jsonify(predictions)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/predict/ndvi', methods=['POST'])
def predict_ndvi():
    """
    Predict NDVI (vegetation health) trends
    
    Expected JSON:
    {
        "geometry": {...},
        "years_ahead": 5,
        "historical_years": 10
    }
    """
    try:
        data = request.get_json()
        geometry = data.get('geometry')
        years_ahead = data.get('years_ahead', 5)
        historical_years = data.get('historical_years', 10)
        
        if not geometry:
            return jsonify({
                'success': False,
                'error': 'No geometry provided'
            }), 400
        
        if not gee_predictor:
            return jsonify({
                'success': False,
                'error': 'GEE predictor not initialized'
            }), 500
        
        # Generate NDVI prediction
        prediction = gee_predictor.predict_ndvi_trend(geometry, years_ahead, historical_years)
        
        return jsonify(prediction)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/predict/temperature', methods=['POST'])
def predict_temperature():
    """
    Predict temperature trends
    
    Expected JSON:
    {
        "geometry": {...},
        "years_ahead": 5,
        "historical_years": 10
    }
    """
    try:
        data = request.get_json()
        geometry = data.get('geometry')
        years_ahead = data.get('years_ahead', 5)
        historical_years = data.get('historical_years', 10)
        
        if not geometry:
            return jsonify({
                'success': False,
                'error': 'No geometry provided'
            }), 400
        
        if not gee_predictor:
            return jsonify({
                'success': False,
                'error': 'GEE predictor not initialized'
            }), 500
        
        # Generate temperature prediction
        prediction = gee_predictor.predict_temperature_trend(geometry, years_ahead, historical_years)
        
        return jsonify(prediction)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/predict/precipitation', methods=['POST'])
def predict_precipitation():
    """
    Predict precipitation trends
    
    Expected JSON:
    {
        "geometry": {...},
        "years_ahead": 5,
        "historical_years": 10
    }
    """
    try:
        data = request.get_json()
        geometry = data.get('geometry')
        years_ahead = data.get('years_ahead', 5)
        historical_years = data.get('historical_years', 10)
        
        if not geometry:
            return jsonify({
                'success': False,
                'error': 'No geometry provided'
            }), 400
        
        if not gee_predictor:
            return jsonify({
                'success': False,
                'error': 'GEE predictor not initialized'
            }), 500
        
        # Generate precipitation prediction
        prediction = gee_predictor.predict_precipitation_trend(geometry, years_ahead, historical_years)
        
        return jsonify(prediction)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'gee_initialized': gee_processor is not None,
        'gee_predictor_initialized': gee_predictor is not None,
        'llm_initialized': llm_analyzer is not None
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"\n{'='*50}")
    print(f"🌍 Environmental Analysis System")
    print(f"{'='*50}")
    print(f"Server: http://localhost:{port}")
    print(f"Debug Mode: {debug}")
    print(f"{'='*50}\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
