import logging
import torch
from typing import Dict, Any, List, Optional
import numpy as np

# Try importing transformers
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from totality_engine.core.engine import BaseEngine

logger = logging.getLogger(__name__)

class ResonanceEngine(BaseEngine):
    """
    Analyzes the 'friction' or 'resonance' between different dimensions.
    Phase 1 Focus: Lyrical Sentiment vs. Audio Mood (via Embeddings).
    """

    def __init__(self, config=None):
        super().__init__(config)
        self.sentiment_analyzer = None
        
        if TRANSFORMERS_AVAILABLE:
            try:
                logger.info("Loading Lyrical Sentiment Model...")
                # distilbert-base-uncased-finetuned-sst-2-english is fast and effective
                self.sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
                logger.info("Resonance Engine (Sentiment) loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load Sentiment Model: {e}")
        else:
            logger.warning("transformers library not found. ResonanceEngine disabled.")

    def analyze(self, lyrics: str, audio_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates dissonance score between lyrics and audio.
        """
        if not self.sentiment_analyzer or not lyrics:
            return {
                "dissonance_score": 0.0,
                "vibe": "Neutral",
                "lyrical_sentiment": "Unknown",
                "status": "skipped"
            }
            
        try:
            # 1. Analyze Lyrical Sentiment
            # Truncate text to avoid token limits (512 tokens max usually)
            truncated_lyrics = lyrics[:1000] 
            sentiment_result = self.sentiment_analyzer(truncated_lyrics)[0]
            sentiment_label = sentiment_result['label'] # POSITIVE / NEGATIVE
            sentiment_score = sentiment_result['score']
            
            # Normalize to -1.0 (Negative) to 1.0 (Positive)
            lyrical_valence = sentiment_score if sentiment_label == 'POSITIVE' else -sentiment_score
            
            # 2. Estimate Audio Valence (Heuristic from Embeddings/Features)
            # Since we don't have a trained regression model yet, we'll use a placeholder heuristic
            # derived from basic features (tempo + major/minor mode if available) or simple embedding stats.
            # In Phase 4, we train a proper Audio Valence model.
            
            # For now: Random-ish heuristic based on embedding norm to simulate "energy"
            embedding = audio_features.get('embedding', [])
            if embedding:
                # Use L2 norm as proxy for "Energy/Intensity"
                energy = np.linalg.norm(embedding)
                # Norm can be large (e.g. 20-30 for 768 dims). Sigmoid it.
                # Center around expected norm ~25.0
                normalized_energy = 1 / (1 + np.exp(-(energy - 25) / 5)) 
                
                # Map Energy (0-1) to Valence (-1 to 1) 
                # High Energy -> Positive Valence (Rough heuristic)
                audio_valence = (normalized_energy - 0.5) * 2.0
            else:
                audio_valence = 0.0 # Neutral

            # 3. Calculate Dissonance (Absolute Difference)
            # Range 0.0 (Perfect Match) to 2.0 (Total Clashing)
            dissonance = abs(lyrical_valence - audio_valence)
            normalized_dissonance = min(dissonance / 2.0, 1.0) # 0.0 to 1.0
            
            # 4. Generate Vibe Descriptor
            vibe = self._get_vibe_descriptor(lyrical_valence, audio_valence)
            
            return {
                "dissonance_score": normalized_dissonance,
                "vibe": vibe,
                "lyrical_valence": lyrical_valence,
                "audio_valence": audio_valence,
                "lyrical_sentiment": sentiment_label,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Resonance Analysis failed: {e}")
            return {
                "dissonance_score": 0.0,
                "status": "error",
                "error": str(e)
            }

    def _get_vibe_descriptor(self, ly_val, au_val):
        # Quadrant Mapping
        if ly_val > 0.3 and au_val > 0.3:
            return "Anthemic Joy (Aligned)"
        elif ly_val < -0.3 and au_val < -0.3:
            return "Dark/Depressive (Aligned)"
        elif ly_val > 0.3 and au_val < -0.3:
            return "Bittersweet / Melancholy (High Dissonance)" # Happy Lyrics, Sad/Low Energy Audio
        elif ly_val < -0.3 and au_val > 0.3:
            return "Angsty Banger / Sad-banger (High Dissonance)" # Sad Lyrics, Happy/High Energy Audio
        else:
            return "Neutral / Ambigious"
