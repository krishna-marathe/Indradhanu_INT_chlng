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