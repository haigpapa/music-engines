from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os
import json
from datetime import date
from typing import List

# --- Totality Engine Imports ---
from totality_engine.core.models import (
    TotalitySong, AcousticFeatures, LyricalContent, 
    CulturalContext, NeuroResponse, EconomicStats, 
    SocialContext, HistoricalContext
)
# Removed unused import
from totality_engine.engines.hit_science.pipeline import HitSciencePipeline

app = FastAPI(title="Totality Engine API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Hit Science Pipeline ---
hit_pipeline = HitSciencePipeline()

# --- Job Store (In-Memory for MVP) ---
JOBS = {}

from uuid import uuid4
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Create a thread pool for heavy audio processing
audio_processor = ThreadPoolExecutor(max_workers=2)

def run_analysis_task(job_id: str, temp_file: str, metadata: dict):
    """
    Wrapper to run the synchronous pipeline in a separate thread.
    """
    try:
        JOBS[job_id]["status"] = "processing"
        
        # Run Analysis (Blocking Call)
        print(f"Job {job_id}: Starting analysis on {temp_file}...")
        results = hit_pipeline.analyze_track(temp_file, metadata)
        
        JOBS[job_id]["status"] = "completed"
        JOBS[job_id]["result"] = results
        print(f"Job {job_id}: Completed successfully.")
        
    except Exception as e:
        print(f"Job {job_id}: Failed with error: {str(e)}")
        JOBS[job_id]["status"] = "failed"
        JOBS[job_id]["error"] = str(e)
        
    finally:
        # Cleanup temp file
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception as cleanup_err:
                print(f"Job {job_id}: Error cleaning up file {temp_file}: {cleanup_err}")

@app.post("/hit-science/analyze")
async def analyze_track_async(
    file: UploadFile = File(...),
    artist_id: str = Body("unknown"),
    platform: str = Body("Spotify"),
    target_markets: str = Body("US,UK")
):
    """
    Async Job Submission: Uploads file and starts analysis in background.
    Returns: {"job_id": "..."}
    """
    job_id = str(uuid4())
    temp_filename = f"temp_{job_id}_{file.filename}"
    temp_path = os.path.join("temp_uploads", temp_filename)
    
    # Ensure temp dir exists
    os.makedirs("temp_uploads", exist_ok=True)
    
    try:
        # Save upload to temp file (awaitable)
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        metadata = {
            "artist_id": artist_id,
            "platform": platform,
            "target_markets": target_markets.split(","),
            "lyrics": "" 
        }
        
        # Initialize Job
        JOBS[job_id] = {
            "status": "queued", 
            "submitted_at": date.today().isoformat(),
            "metadata": metadata
        }
        
        # Offload to ThreadPool
        loop = asyncio.get_event_loop()
        loop.run_in_executor(
            audio_processor, 
            run_analysis_task, 
            job_id, 
            temp_path, 
            metadata
        )
        
        return {"job_id": job_id, "status": "queued", "message": "Analysis started in background."}
        
    except Exception as e:
        # Cleanup if submission fails
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Submission failed: {str(e)}")

@app.get("/hit-science/jobs/{job_id}")
async def get_job_status(job_id: str):
    """
    Poll this endpoint to check analysis status.
    """
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    response = {
        "job_id": job_id,
        "status": job["status"],
        "submitted_at": job.get("submitted_at")
    }
    
    if job["status"] == "completed":
        response["result"] = job["result"]
    elif job["status"] == "failed":
        response["error"] = job.get("error")
        
    return response

# --- Legacy/Mock Data for Comparison ---
MOCK_SONGS = {
    "song_001": TotalitySong(
        id="song_001",
        title="Neon Nights",
        artist="RetroWave Bot",
        release_date=date(2024, 1, 1),
        acoustic=AcousticFeatures(bpm=120.0, key="C Major", lufs=-9.0, duration_ms=200000, danceability=0.8, energy=0.7),
        lyrical=LyricalContent(themes=["City", "Future"], sentiment_valence=0.8),
        cultural=CulturalContext(origin_city="LA", origin_country="USA", language="English"),
        neuro=NeuroResponse(predicted_emotions=["Joy"], stimulation_score=0.7),
        economic=EconomicStats(label_type="Indie"),
        social=SocialContext(identity_markers=["Cyberpunk"]),
        historical=HistoricalContext(era="2020s")
    ),
    "song_002": TotalitySong(
        id="song_002",
        title="Dark Matter",
        artist="Abyss Walker",
        release_date=date(2023, 10, 31),
        acoustic=AcousticFeatures(bpm=140.0, key="D Minor", lufs=-12.0, duration_ms=240000, danceability=0.4, energy=0.5),
        lyrical=LyricalContent(themes=["Space", "Void"], sentiment_valence=-0.5),
        cultural=CulturalContext(origin_city="Berlin", origin_country="Germany", language="English"),
        neuro=NeuroResponse(predicted_emotions=["Fear"], stimulation_score=0.4),
        economic=EconomicStats(label_type="Major"),
        social=SocialContext(identity_markers=["Goth"]),
        historical=HistoricalContext(era="2020s")
    )
}

@app.get("/songs/{song_id}", response_model=TotalitySong)
def get_song(song_id: str):
    song = MOCK_SONGS.get(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@app.post("/compare")
def compare_endpoints(id_a: str, id_b: str):
    song_a = MOCK_SONGS.get(id_a) or MOCK_SONGS["song_001"]
    song_b = MOCK_SONGS.get(id_b)
    
    if not song_b:
        from copy import deepcopy
        song_b = deepcopy(song_a)
        song_b.id = "song_002"
        song_b.title = "Techno Bunker"
        song_b.acoustic.bpm = 140
    
    from totality_engine.engines.comparison import ComparisonEngine
    engine = ComparisonEngine()
    return engine.compare(song_a, song_b)


# --- Serve Frontend (Must be last) ---
if os.path.exists("frontend/dist"):
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
else:
    print("Warning: frontend/dist not found. Run 'npm run build' in frontend/.")
