from worker import celery
from totality_engine.engines.hit_science.pipeline import HitSciencePipeline
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to cache the pipeline model in the worker process
pipeline = None

def get_pipeline():
    """Lazy load the pipeline to avoid re-initializing heavy models on every task if feasible, 
       but for Celery prefork, it's often better to load at module level or inside task with a global cache."""
    global pipeline
    if pipeline is None:
        logger.info("Initializing HitSciencePipeline in Worker...")
        pipeline = HitSciencePipeline()
    return pipeline

@celery.task(bind=True)
def analyze_track_task(self, audio_path, artist_id, markets, lyrics=None):
    """
    Background task to run the full Hit Science analysis.
    """
    logger.info(f"Starting analysis for {audio_path}")
    
    try:
        # Load pipeline
        eng = get_pipeline()
        
        # Prepare metadata
        metadata = {
            "artist_id": artist_id,
            "markets": markets,
            "lyrics": lyrics
        }
        
        # Run analysis
        # Note: analyze_track might not be thread-safe if models are not, but Celery creates processes.
        result = eng.analyze_track(audio_path, metadata)
        
        # --- Persist to DB (Worker Side) ---
        from totality_engine.core.schema import AnalysisResult
        from sqlmodel import Session, create_engine
        import json
        import os
        
        # Re-create engine here (avoid sharing connection across processes)
        sqlite_url = f"sqlite:///totality.db" 
        db_engine = create_engine(sqlite_url)
        
        try:
            # Extract embeddings
            embedding = result.get("creative", {}).get("embedding")
            embedding_json = json.dumps(embedding) if embedding else None
            
            # Extract resonance
            resonance = result.get("resonance", {})
            
            with Session(db_engine) as session:
                db_result = AnalysisResult(
                    filename=os.path.basename(audio_path),
                    status="success",
                    raw_json=json.dumps(result),
                    embedding_json=embedding_json,
                    dissonance_score=resonance.get("dissonance_score"),
                    vibe_descriptor=resonance.get("vibe"),
                    lyrical_sentiment=resonance.get("lyrical_sentiment"),
                    artist_id=artist_id,
                    markets=",".join(markets)
                )
                session.add(db_result)
                session.commit()
                logger.info("Result saved to database (Worker).")
        except Exception as db_e:
            logger.error(f"Database save failed in worker: {db_e}")
            
        # Clean up temp file
        if os.path.exists(audio_path):
            os.remove(audio_path)
            logger.info(f"Cleaned up {audio_path}")
            
        # --- Persist to Graph (Phase 5) ---
        try:
            from totality_engine.engines.hit_science.systems.industry.graph_model import IndustryGraph
            graph = IndustryGraph()
            # Use filename as unique track ID for now (MVP)
            track_id = os.path.basename(audio_path)
            graph.add_track_node(
                track_id=track_id,
                metadata={"filename": track_id, "artist_id": artist_id},
                analysis_results=result
            )
            logger.info("Graph nodes created (Worker).")
        except Exception as graph_e:
            logger.error(f"Graph update failed: {graph_e}")
            
        logger.info(f"Analysis complete for {audio_path}")
        return {
            "status": "success",
            "results": result
        }
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return {
            "status": "failed",
            "error": str(e)
        }
