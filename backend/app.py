"""
Indradhanu Analytics Backend
Optimized Flask server with fast startup and efficient file serving
"""
import time
import os
import sys
import uuid
import traceback
import json
import numpy as np
from datetime import datetime

# Track startup time
startup_start = time.time()

# Core Flask imports
from flask import Flask, request, jsonify, send_from_directory, abort
from flask_cors import CORS

print(f"⏱️ Core imports loaded in {time.time() - startup_start:.3f}s")

# Add analytics_engine to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Comprehensive NumPy JSON encoder to handle all NumPy data types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif hasattr(obj, 'isoformat'):
            return obj.isoformat()
        elif hasattr(obj, 'item'):  # Handle other numpy scalars
            return obj.item()
        return super(NumpyEncoder, self).default(obj)

# Initialize Flask app with proper static configuration
app = Flask(__name__)
app.json_encoder = NumpyEncoder
CORS(app, origins="*", methods=["GET", "POST", "HEAD", "OPTIONS"])

# Configuration
UPLOAD_FOLDER = "uploads"
VISUALS_FOLDER = "visuals"  # Local visuals folder in backend
ANALYTICS_VISUALS = "../analytics_engine/visuals"  # Analytics engine visuals

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(VISUALS_FOLDER, exist_ok=True)
os.makedirs(ANALYTICS_VISUALS, exist_ok=True)

print(f"⏱️ Directories setup completed in {time.time() - startup_start:.3f}s")

# Global analysis engine (lazy loaded)
analysis_engine = None

def get_analysis_engine():
    """Lazy initialization of analysis engine"""
    global analysis_engine
    if analysis_engine is None:
        print("🔧 Initializing analysis engine...")
        engine_start = time.time()
        from analytics_engine.analysis_engine import AnalysisEngine
        analysis_engine = AnalysisEngine(output_dir=ANALYTICS_VISUALS)
        print(f"✅ Analysis engine ready in {time.time() - engine_start:.3f}s")
    return analysis_engine

def log_request_time(route_name, start_time, extra_info=""):
    """Log request execution time"""
    duration = time.time() - start_time
    print(f"📊 {route_name} completed in {duration:.3f}s {extra_info}")
    return duration

def convert_numpy_types(obj):
    """Recursively convert numpy types to native Python types"""
    if isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_numpy_types(item) for item in obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif hasattr(obj, 'item'):  # Handle other numpy scalars
        return obj.item()
    else:
        return obj

def safe_json_response(data, status_code=200):
    """Create a safe JSON response that handles NumPy types"""
    try:
        response = app.response_class(
            response=json.dumps(data, cls=NumpyEncoder),
            status=status_code,
            mimetype='application/json'
        )
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        print(f"❌ JSON serialization error: {str(e)}")
        error_data = {"error": "JSON serialization failed", "details": str(e)}
        return app.response_class(
            response=json.dumps(error_data),
            status=500,
            mimetype='application/json'
        )

# ============================================================================
# CORE ROUTES
# ============================================================================

@app.route("/")
def home():
    """Health check endpoint"""
    return jsonify({
        "message": "🌍 Indradhanu Analytics API is running!",
        "version": "1.0.0",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

# ============================================================================
# OPTIMIZED VISUALS ROUTES - FIXED FOR HEAD REQUESTS
# ============================================================================

@app.route("/visuals/", methods=["GET", "HEAD"])
def list_visuals():
    """List available visual files with proper HEAD support"""
    request_start = time.time()
    
    try:
        # For HEAD request — return headers only, no data computation
        if request.method == "HEAD":
            response = app.response_class(status=200)
            response.headers.update({
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            })
            log_request_time("HEAD /visuals/", request_start)
            return response
        
        # Check both local visuals and analytics visuals
        visual_dirs = [VISUALS_FOLDER, ANALYTICS_VISUALS]
        all_files = []
        
        for visual_dir in visual_dirs:
            if os.path.exists(visual_dir):
                files = [f for f in os.listdir(visual_dir) 
                        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif'))]
                all_files.extend(files)
        
        # Remove duplicates and sort
        unique_files = sorted(list(set(all_files)))
        
        # Handle GET request with full JSON response
        response_data = {
            "count": len(unique_files),
            "files": unique_files,
            "directories_scanned": len([d for d in visual_dirs if os.path.exists(d)]),
            "timestamp": datetime.now().isoformat()
        }
        
        response = jsonify(response_data)
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        })
        
        log_request_time("GET /visuals/", request_start, f"({len(unique_files)} files)")
        return response
        
    except Exception as e:
        print(f"❌ Error in /visuals/: {str(e)}")
        if request.method == "HEAD":
            response = app.response_class(status=500)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        
        error_response = jsonify({"error": str(e), "timestamp": datetime.now().isoformat()})
        error_response.headers['Access-Control-Allow-Origin'] = '*'
        return error_response, 500

@app.route("/visuals/<path:filename>", methods=["GET", "HEAD"])
def serve_visual(filename):
    """Serve individual visual files with security and performance optimization"""
    request_start = time.time()
    
    try:
        # Security: Validate filename
        if '..' in filename or filename.startswith('/') or '\\' in filename:
            print(f"⚠️ Blocked unsafe filename: {filename}")
            abort(403)
        
        # Security: Only allow image extensions
        allowed_extensions = {'.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp'}
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            print(f"⚠️ Blocked non-image file: {filename}")
            abort(403)
        
        # Try to find file in multiple locations
        search_paths = [
            os.path.join(VISUALS_FOLDER, filename),
            os.path.join(ANALYTICS_VISUALS, filename)
        ]
        
        file_path = None
        for path in search_paths:
            if os.path.exists(path) and os.path.isfile(path):
                file_path = path
                break
        
        if not file_path:
            print(f"⚠️ File not found: {filename}")
            abort(404)
        
        # Get file directory for send_from_directory
        file_dir = os.path.dirname(file_path)
        
        # Handle HEAD request
        if request.method == "HEAD":
            file_stat = os.stat(file_path)
            response = app.response_class(status=200)
            response.headers.update({
                'Content-Type': f'image/{file_ext[1:]}',
                'Content-Length': str(file_stat.st_size),
                'Access-Control-Allow-Origin': '*',
                'Last-Modified': datetime.fromtimestamp(file_stat.st_mtime).strftime('%a, %d %b %Y %H:%M:%S GMT')
            })
            log_request_time(f"HEAD /visuals/{filename}", request_start)
            return response
        
        # Serve file for GET request
        response = send_from_directory(file_dir, filename)
        response.headers['Access-Control-Allow-Origin'] = '*'
        
        log_request_time(f"GET /visuals/{filename}", request_start)
        return response
        
    except Exception as e:
        print(f"❌ Error serving {filename}: {str(e)}")
        if request.method == "HEAD":
            return app.response_class(status=500)
        abort(500)

# ============================================================================
# GEOCODING ROUTES
# ============================================================================

@app.route("/geocoding/search", methods=["GET"])
def search_locations():
    """Search for locations by name"""
    request_start = time.time()
    
    try:
        query = request.args.get('q', '').strip()
        limit = request.args.get('limit', 5, type=int)
        
        if not query:
            return jsonify({
                "error": "Missing required parameter: q (query)",
                "error_code": "MISSING_QUERY"
            }), 400
        
        if len(query) < 2:
            return jsonify({
                "error": "Query must be at least 2 characters long",
                "error_code": "QUERY_TOO_SHORT"
            }), 400
        
        # Limit results to reasonable range
        limit = max(1, min(limit, 10))
        
        # Import geocoding service
        from geocoding_service import GeocodingService
        geocoding_service = GeocodingService()
        
        # Search for locations
        locations = geocoding_service.search_location(query, limit)
        
        log_request_time("GET /geocoding/search", request_start, 
                        f"({len(locations)} results for '{query}')")
        
        return jsonify({
            "message": "Location search completed successfully",
            "query": query,
            "results": locations,
            "count": len(locations)
        }), 200
        
    except Exception as e:
        print(f"❌ Geocoding search error: {str(e)}")
        return jsonify({
            "error": "Failed to search locations",
            "error_code": "GEOCODING_SEARCH_ERROR",
            "details": str(e)
        }), 500

@app.route("/geocoding/popular", methods=["GET"])
def get_popular_locations():
    """Get popular locations for quick access"""
    request_start = time.time()
    
    try:
        # Import geocoding service
        from geocoding_service import GeocodingService
        geocoding_service = GeocodingService()
        
        # Get popular locations (cached or pre-defined)
        popular_locations = [
            {"name": "New York, USA", "latitude": 40.7128, "longitude": -74.0060, "clean_name": "New York, New York, USA"},
            {"name": "London, UK", "latitude": 51.5074, "longitude": -0.1278, "clean_name": "London, England, UK"},
            {"name": "Tokyo, Japan", "latitude": 35.6762, "longitude": 139.6503, "clean_name": "Tokyo, Japan"},
            {"name": "Paris, France", "latitude": 48.8566, "longitude": 2.3522, "clean_name": "Paris, France"},
            {"name": "Berlin, Germany", "latitude": 52.5200, "longitude": 13.4050, "clean_name": "Berlin, Germany"},
            {"name": "Sydney, Australia", "latitude": -33.8688, "longitude": 151.2093, "clean_name": "Sydney, Australia"},
            {"name": "Mumbai, India", "latitude": 19.0760, "longitude": 72.8777, "clean_name": "Mumbai, India"},
            {"name": "São Paulo, Brazil", "latitude": -23.5505, "longitude": -46.6333, "clean_name": "São Paulo, Brazil"},
            {"name": "Cairo, Egypt", "latitude": 30.0444, "longitude": 31.2357, "clean_name": "Cairo, Egypt"},
            {"name": "Moscow, Russia", "latitude": 55.7558, "longitude": 37.6176, "clean_name": "Moscow, Russia"},
            {"name": "Beijing, China", "latitude": 39.9042, "longitude": 116.4074, "clean_name": "Beijing, China"},
            {"name": "Los Angeles, USA", "latitude": 34.0522, "longitude": -118.2437, "clean_name": "Los Angeles, California, USA"},
            {"name": "Dubai, UAE", "latitude": 25.2048, "longitude": 55.2708, "clean_name": "Dubai, UAE"},
            {"name": "Singapore", "latitude": 1.3521, "longitude": 103.8198, "clean_name": "Singapore"},
            {"name": "Toronto, Canada", "latitude": 43.6532, "longitude": -79.3832, "clean_name": "Toronto, Canada"}
        ]
        
        log_request_time("GET /geocoding/popular", request_start, 
                        f"({len(popular_locations)} popular locations)")
        
        return jsonify({
            "message": "Popular locations retrieved successfully",
            "locations": popular_locations,
            "count": len(popular_locations)
        }), 200
        
    except Exception as e:
        print(f"❌ Popular locations error: {str(e)}")
        return jsonify({
            "error": "Failed to retrieve popular locations",
            "error_code": "POPULAR_LOCATIONS_ERROR",
            "details": str(e)
        }), 500

@app.route("/geocoding/reverse", methods=["GET"])
def reverse_geocode():
    """Convert coordinates to location name"""
    request_start = time.time()
    
    try:
        latitude = request.args.get('lat', type=float)
        longitude = request.args.get('lon', type=float)
        
        if latitude is None or longitude is None:
            return jsonify({
                "error": "Missing required parameters: lat and lon",
                "error_code": "MISSING_COORDINATES"
            }), 400
        
        # Validate coordinates
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            return jsonify({
                "error": "Invalid coordinates. Latitude must be -90 to 90, longitude -180 to 180",
                "error_code": "INVALID_COORDINATES"
            }), 400
        
        # Import geocoding service
        from geocoding_service import GeocodingService
        geocoding_service = GeocodingService()
        
        # Reverse geocode
        location = geocoding_service.reverse_geocode(latitude, longitude)
        
        log_request_time("GET /geocoding/reverse", request_start, 
                        f"({location['clean_name']})")
        
        return jsonify({
            "message": "Reverse geocoding completed successfully",
            "location": location
        }), 200
        
    except Exception as e:
        print(f"❌ Reverse geocoding error: {str(e)}")
        return jsonify({
            "error": "Failed to reverse geocode location",
            "error_code": "REVERSE_GEOCODING_ERROR",
            "details": str(e)
        }), 500

# ============================================================================
# WEATHER DATA ROUTES
# ============================================================================

@app.route("/weather/current", methods=["GET"])
def get_current_weather():
    """Get current weather data for specified coordinates"""
    request_start = time.time()
    
    try:
        # Get coordinates from query parameters
        latitude = request.args.get('lat', type=float)
        longitude = request.args.get('lon', type=float)
        hours_back = request.args.get('hours', default=6, type=int)
        
        if latitude is None or longitude is None:
            return jsonify({
                "error": "Missing required parameters: lat and lon",
                "error_code": "MISSING_COORDINATES"
            }), 400
        
        # Validate coordinates
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            return jsonify({
                "error": "Invalid coordinates. Latitude must be -90 to 90, longitude -180 to 180",
                "error_code": "INVALID_COORDINATES"
            }), 400
        
        # Validate hours_back
        if not (1 <= hours_back <= 24):
            return jsonify({
                "error": "Hours parameter must be between 1 and 24",
                "error_code": "INVALID_HOURS"
            }), 400
        
        # Import weather service
        from weather_service import WeatherService
        weather_service = WeatherService()
        
        # Fetch weather data
        weather_data = weather_service.get_weather_data(latitude, longitude, hours_back)
        
        # Convert numpy types for JSON serialization
        weather_data = convert_numpy_types(weather_data)
        
        log_request_time("GET /weather/current", request_start, 
                        f"({weather_data['data_points']} data points)")
        
        return safe_json_response({
            "message": "Weather data retrieved successfully",
            "data": weather_data
        }, 200)
        
    except Exception as e:
        print(f"❌ Weather API error: {str(e)}")
        return jsonify({
            "error": "Failed to fetch weather data",
            "error_code": "WEATHER_FETCH_ERROR",
            "details": str(e)
        }), 500

@app.route("/weather/analyze", methods=["POST"])
def analyze_weather_data():
    """Analyze weather data and generate visualizations"""
    request_start = time.time()
    
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                "error": "No JSON data provided",
                "error_code": "NO_DATA"
            }), 400
        
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        hours_back = data.get('hours', 6)
        
        if latitude is None or longitude is None:
            return jsonify({
                "error": "Missing required fields: latitude and longitude",
                "error_code": "MISSING_COORDINATES"
            }), 400
        
        # Import services
        from weather_service import WeatherService
        weather_service = WeatherService()
        
        # Fetch weather data
        weather_data = weather_service.get_weather_data(latitude, longitude, hours_back)
        
        # Generate visualizations using analytics engine
        engine = get_analysis_engine()
        
        # Convert weather data to DataFrame for analysis
        import pandas as pd
        df = pd.DataFrame(weather_data['hourly_data'])
        
        if not df.empty:
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.set_index('timestamp')
            
            # Generate weather-specific charts
            filename = f"weather_{latitude}_{longitude}_{int(time.time())}"
            chart_generator = engine.get_chart_generator()
            
            # Use the original working weather chart method
            print("🔄 Using original weather charts")
            
            # Create simple charts that we know work
            charts = []
            
            # Temperature chart
            if 'temperature_2m' in df.columns:
                temp_data = df['temperature_2m']
                trend = "↗️ Rising" if temp_data.iloc[-1] > temp_data.iloc[0] else "↘️ Falling" if temp_data.iloc[-1] < temp_data.iloc[0] else "➡️ Stable"
                temp_chart = {
                    'title': f'🌡️ Temperature Analysis - {temp_data.iloc[-1]:.1f}°C',
                    'type': 'line',
                    'category': 'atmospheric',
                    'description': f'Current: {temp_data.iloc[-1]:.1f}°C | Range: {temp_data.min():.1f}°C to {temp_data.max():.1f}°C | Trend: {trend} | Variation: {temp_data.max() - temp_data.min():.1f}°C over 6 hours',
                    'url': None  # No image URL, will show data summary
                }
                charts.append(temp_chart)
            
            # Humidity chart
            if 'relative_humidity_2m' in df.columns:
                humidity_data = df['relative_humidity_2m']
                humidity_level = "High" if humidity_data.iloc[-1] > 70 else "Moderate" if humidity_data.iloc[-1] > 40 else "Low"
                trend = "↗️ Rising" if humidity_data.iloc[-1] > humidity_data.iloc[0] else "↘️ Falling" if humidity_data.iloc[-1] < humidity_data.iloc[0] else "➡️ Stable"
                humidity_chart = {
                    'title': f'💧 Humidity Analysis - {humidity_data.iloc[-1]:.0f}%',
                    'type': 'line', 
                    'category': 'atmospheric',
                    'description': f'Current: {humidity_data.iloc[-1]:.0f}% ({humidity_level}) | Range: {humidity_data.min():.0f}% to {humidity_data.max():.0f}% | Trend: {trend} | Average: {humidity_data.mean():.0f}%',
                    'url': None
                }
                charts.append(humidity_chart)
            
            # Wind chart
            if 'wind_speed_10m' in df.columns:
                wind_data = df['wind_speed_10m']
                wind_level = "Strong" if wind_data.iloc[-1] > 25 else "Moderate" if wind_data.iloc[-1] > 10 else "Light"
                direction = f" from {df['wind_direction_10m'].iloc[-1]:.0f}°" if 'wind_direction_10m' in df.columns else ""
                wind_chart = {
                    'title': f'💨 Wind Analysis - {wind_data.iloc[-1]:.1f} km/h',
                    'type': 'line',
                    'category': 'atmospheric', 
                    'description': f'Current: {wind_data.iloc[-1]:.1f} km/h ({wind_level}){direction} | Max: {wind_data.max():.1f} km/h | Average: {wind_data.mean():.1f} km/h | Gusts detected: {"Yes" if wind_data.max() > wind_data.mean() * 1.5 else "No"}',
                    'url': None
                }
                charts.append(wind_chart)
            
            # Pressure chart
            if 'pressure_msl' in df.columns:
                pressure_data = df['pressure_msl']
                pressure_level = "High" if pressure_data.iloc[-1] > 1020 else "Normal" if pressure_data.iloc[-1] > 1000 else "Low"
                trend = "↗️ Rising" if pressure_data.iloc[-1] > pressure_data.iloc[0] else "↘️ Falling" if pressure_data.iloc[-1] < pressure_data.iloc[0] else "➡️ Stable"
                weather_indication = "Stable weather expected" if pressure_level == "High" else "Weather may change" if pressure_level == "Low" else "Normal conditions"
                pressure_chart = {
                    'title': f'📊 Pressure Analysis - {pressure_data.iloc[-1]:.0f} hPa',
                    'type': 'line',
                    'category': 'hydrological',
                    'description': f'Current: {pressure_data.iloc[-1]:.0f} hPa ({pressure_level}) | Range: {pressure_data.min():.0f} to {pressure_data.max():.0f} hPa | Trend: {trend} | {weather_indication}',
                    'url': None
                }
                charts.append(pressure_chart)
            
            # Rain chart
            if 'rain' in df.columns:
                rain_data = df['rain']
                total_rain = rain_data.sum()
                hours_with_rain = (rain_data > 0).sum()
                rain_intensity = "Heavy" if rain_data.max() > 10 else "Moderate" if rain_data.max() > 2 else "Light" if total_rain > 0 else "None"
                rain_chart = {
                    'title': f'🌧️ Rainfall Analysis - {total_rain:.1f} mm total',
                    'type': 'bar',
                    'category': 'hydrological',
                    'description': f'Total: {total_rain:.1f} mm over {hours_with_rain} hours | Max hourly: {rain_data.max():.1f} mm/h | Intensity: {rain_intensity} | {"Dry conditions" if total_rain == 0 else f"Wet period with {hours_with_rain}h of rain"}',
                    'url': None
                }
                charts.append(rain_chart)
            
            # Add charts to weather data
            weather_data['charts'] = charts
        
        # Convert numpy types
        weather_data = convert_numpy_types(weather_data)
        
        log_request_time("POST /weather/analyze", request_start,
                        f"({len(weather_data.get('charts', []))} charts)")
        
        return safe_json_response({
            "message": "Weather analysis completed successfully",
            "data": weather_data
        }, 200)
        
    except Exception as e:
        print(f"❌ Weather analysis error: {str(e)}")
        return jsonify({
            "error": "Failed to analyze weather data",
            "error_code": "WEATHER_ANALYSIS_ERROR",
            "details": str(e)
        }), 500

# ============================================================================
# ANALYTICS ROUTES
# ============================================================================

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file upload and trigger dynamic analysis"""
    request_start = time.time()
    
    try:
        # Validate request
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded!", "error_code": "NO_FILE"}), 400
        
        file = request.files['file']
        if file.filename == "":
            return jsonify({"error": "Empty filename!", "error_code": "EMPTY_FILENAME"}), 400
        
        # Validate file type
        allowed_extensions = {'.csv', '.xlsx', '.json'}
        file_ext = '.' + file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if file_ext not in allowed_extensions:
            return jsonify({
                "error": f"Invalid file type. Only {', '.join(allowed_extensions)} files are allowed.",
                "error_code": "INVALID_FILE_TYPE"
            }), 400
        
        # Check file size (100MB limit)
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > 100 * 1024 * 1024:  # 100MB
            return jsonify({
                "error": "File too large. Maximum size is 100MB.",
                "error_code": "FILE_TOO_LARGE"
            }), 400
        
        # Save file with unique name
        filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        print(f"📁 File saved: {filename} ({file_size} bytes)")
        
        # Run dynamic analytics pipeline
        engine = get_analysis_engine()
        analysis_results = engine.analyze_dataset(file_path, filename)
        
        # Format response and convert numpy types
        response_data = {
            "message": "✅ File processed successfully with dynamic analysis!",
            "filename": filename,
            "original_filename": file.filename,
            "timestamp": analysis_results['timestamp'],
            "dataset_info": convert_numpy_types(analysis_results['dataset_info']),
            "rows": int(analysis_results['dataset_info']['rows']),
            "columns": int(analysis_results['dataset_info']['columns']),
            "schema": convert_numpy_types(analysis_results['schema']),
            "statistics": convert_numpy_types(analysis_results['statistics']),
            "charts": convert_numpy_types(analysis_results['charts']),
            "insights": analysis_results['insights'],
            "column_info": convert_numpy_types(analysis_results['column_info'])
        }
        
        log_request_time("POST /upload", request_start, 
                        f"({len(analysis_results['charts'])} charts, {len(analysis_results['insights'])} insights)")
        
        return safe_json_response(response_data, 200)
        
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            "error": "Failed to process file",
            "error_code": "PROCESSING_ERROR",
            "details": str(e)
        }), 500

@app.route('/report/<filename>', methods=['GET'])
def get_analysis_report(filename):
    """Get detailed analysis report for a specific file"""
    request_start = time.time()
    
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        if not os.path.exists(file_path):
            return jsonify({
                "error": "File not found",
                "error_code": "FILE_NOT_FOUND"
            }), 404
        
        # Generate fresh analysis
        engine = get_analysis_engine()
        analysis_results = engine.analyze_dataset(file_path, filename)
        
        log_request_time(f"GET /report/{filename}", request_start)
        
        return jsonify({
            "message": "Analysis report generated successfully",
            "report": convert_numpy_types(analysis_results)
        }), 200
        
    except Exception as e:
        print(f"❌ Report error: {str(e)}")
        return jsonify({
            "error": "Failed to generate analysis report",
            "error_code": "REPORT_GENERATION_ERROR",
            "details": str(e)
        }), 500

@app.route('/analyze', methods=['POST'])
def analyze_file():
    """Advanced analysis with satellite/sensor data, geospatial and anomaly detection"""
    try:
        data = request.get_json()
        filename = data.get('filename')
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        from analytics_engine.data_loader import load_dataset
        from analytics_engine.anomaly_detector import detect_anomalies
        from analytics_engine.satellite_data_analyzer import analyze_satellite_data
        from analytics_engine.surface_radiation_analyzer import analyze_surface_radiation
        
        df = load_dataset(file_path)
        if df is None:
            return jsonify({'error': 'Failed to load dataset'}), 400
        
        # 🛰️ SATELLITE/SENSOR DATA ANALYSIS
        analysis_result = analyze_satellite_data(df)
        
        # 🌡️ SURFACE TEMPERATURE & RADIATION ANALYSIS
        surface_radiation_analysis = analyze_surface_radiation(df)
        analysis_result['surface_radiation_analysis'] = surface_radiation_analysis
        
        # ⚠️ ANOMALY DETECTION
        anomalies = {}
        numeric_cols = df.select_dtypes(include=np.number).columns
        for col in numeric_cols:
            if col not in ['latitude', 'longitude']:  # Skip geo coordinates
                anomalies[col] = detect_anomalies(df, col)
        
        alerts = []
        for col, records in anomalies.items():
            if len(records) > 0:
                alerts.append(f"⚠️ Sudden spike detected in {col}: {len(records)} unusual readings.")
        
        analysis_result['anomalies'] = convert_numpy_types(anomalies)
        analysis_result['alerts'] = alerts
        
        return safe_json_response(analysis_result, 200)
        
    except Exception as e:
        print(f"❌ Error in analysis: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/uploads', methods=['GET'])
def list_uploads():
    """List all uploaded files with basic metadata"""
    request_start = time.time()
    
    try:
        uploads = []
        
        if os.path.exists(UPLOAD_FOLDER):
            for filename in os.listdir(UPLOAD_FOLDER):
                if filename.endswith(('.csv', '.xlsx', '.json')):
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file_stat = os.stat(file_path)
                    
                    upload_data = {
                        '_id': filename.replace('.', '_'),
                        'filename': filename,
                        'upload_timestamp': datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                        'file_size': file_stat.st_size,
                        'has_analysis': True
                    }
                    uploads.append(upload_data)
        
        # Sort by upload time (newest first)
        uploads.sort(key=lambda x: x['upload_timestamp'], reverse=True)
        
        log_request_time("GET /uploads", request_start, f"({len(uploads)} files)")
        
        return jsonify(uploads), 200
        
    except Exception as e:
        print(f"❌ Error listing uploads: {str(e)}")
        return jsonify({
            "error": "Failed to retrieve upload history",
            "error_code": "HISTORY_FETCH_ERROR"
        }), 500

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found", "error_code": "NOT_FOUND"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error", "error_code": "INTERNAL_ERROR"}), 500

@app.errorhandler(403)
def forbidden(error):
    return jsonify({"error": "Access forbidden", "error_code": "FORBIDDEN"}), 403

# ============================================================================
# STARTUP AND MAIN
# ============================================================================

def create_app():
    """Application factory for production deployment"""
    return app

if __name__ == "__main__":
    total_startup_time = time.time() - startup_start
    print(f"✅ Server initialized in {total_startup_time:.3f} seconds")
    print("🚀 Starting Flask development server on http://127.0.0.1:5000")
    
    # Run with optimized settings
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        threaded=True,
        use_reloader=True
    )