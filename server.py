import os
import io
import json
import logging
import traceback
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import sys

# Ensure project root is in path so imports work
sys.path.append(os.getcwd())

from totality_engine.core.schema import AnalysisResult
from sqlmodel import SQLModel, create_engine, Session, select
from worker import celery
from celery.result import AsyncResult

# Database Setup
sqlite_file_name = "totality.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

create_db_and_tables()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) 

# Note: We no longer load the Pipeline here. It lives in the Worker.

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'aiff', 'flac', 'ogg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    # Basic check
    return jsonify({"status": "healthy", "mode": "async"})

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Save explicitly to a temp dir (Shared with Worker)
        # Ideally use a shared volume or object store, but local fs works for single machine
        temp_dir = os.path.join(os.getcwd(), 'temp_uploads')
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, filename)
        
        try:
            file.save(file_path)
            logger.info(f"File saved to {file_path}")
            
            # Extract metadata
            artist_id = request.form.get('artist_id', 'unknown_artist')
            markets = request.form.get('target_markets', 'US').split(",")
            lyrics = request.form.get('lyrics', "")
            
            # Trigger Async Task
            # We pass file_path (which worker must be able to access)
            task = celery.send_task('tasks.analyze_track_task', args=[file_path, artist_id, markets, lyrics])
            
            return jsonify({
                "job_id": task.id,
                "status": "queued"
            }), 202
            
        except Exception as e:
            logger.error(f"Failed to queue task: {e}")
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "File type not allowed"}), 400

@app.route('/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """
    Check the status of a Celery task.
    """
    task_result = AsyncResult(job_id, app=celery)
    
    response = {
        "job_id": job_id,
        "status": task_result.status.lower(), # PENDING, STARTED, SUCCESS, FAILURE
    }
    
    if task_result.state == 'PENDING':
        response["status"] = "queued"
    elif task_result.state == 'STARTED':
        response["status"] = "processing"
    elif task_result.state == 'SUCCESS':
        response["status"] = "completed"
        # The worker returns { "status": "success", "results": ... }
        # Task result value is in task_result.result
        data = task_result.result
        if data and "results" in data:
            response["result"] = data["results"]
    elif task_result.state == 'FAILURE':
        response["status"] = "failed"
        response["error"] = str(task_result.result)
        
    return jsonify(response)

@app.route('/history', methods=['GET'])
def get_history():
    try:
        with Session(engine) as session:
            statement = select(AnalysisResult).order_by(AnalysisResult.timestamp.desc()).limit(20)
            results = session.exec(statement).all()
            
            history = []
            for r in results:
                history.append({
                    "id": r.id,
                    "filename": r.filename,
                    "timestamp": r.timestamp.isoformat(),
                    "artist_id": r.artist_id
                })
            return jsonify(history)
    except Exception as e:
        logger.error(f"History fetch failed: {e}")
        return jsonify({"error": str(e)}), 500

# Serve Frontend
@app.route('/')
def index():
    return send_from_directory('frontend/dist', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend/dist', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
