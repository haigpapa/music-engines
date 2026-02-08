import torch
import librosa
import numpy as np
import logging
from typing import Dict, Any, List

# Try importing transformers, but don't crash if missing (though it should be installed)
try:
    from transformers import AutoFeatureExtractor, ASTModel
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from totality_engine.core.engine import BaseEngine

logger = logging.getLogger(__name__)

class DeepListeningEngine(BaseEngine):
    """
    Uses Deep Learning (AST - Audio Spectrogram Transformer) to generate 
    high-dimensional embeddings for audio tracks.
    """
    
    MODEL_NAME = "MIT/ast-finetuned-audioset-10-10-0.4593"

    def __init__(self, config=None):
        super().__init__(config)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.feature_extractor = None
        self.embedding_dim = 768 # AST base dimension
        
        if TRANSFORMERS_AVAILABLE:
            try:
                logger.info(f"Loading Deep Listening Model: {self.MODEL_NAME}...")
                self.feature_extractor = AutoFeatureExtractor.from_pretrained(self.MODEL_NAME)
                self.model = ASTModel.from_pretrained(self.MODEL_NAME).to(self.device)
                self.model.eval() # Inference mode
                logger.info("Deep Listening Model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load Deep Listening Model: {e}")
                logger.warning("DeepListeningEngine will run in fallback mode (zero embeddings).")
        else:
            logger.warning("transformers library not found. DeepListeningEngine disabled.")

    def analyze(self, input_data: str) -> Dict[str, Any]:
        """
        Generates an embedding for the audio file.
        input_data: path to audio file.
        """
        audio_path = input_data
        
        if not self.model or not self.feature_extractor:
            return {
                "embedding": [0.0] * self.embedding_dim,
                "status": "fallback",
                "model": "none"
            }
            
        try:
            # 1. Load Audio (Resample to 16kHz as required by AST)
            y, sr = librosa.load(audio_path, sr=16000, duration=10.0) # Limit to 10s for speed/memory in MVP
            
            # 2. Prepare Inputs
            inputs = self.feature_extractor(y, sampling_rate=sr, return_tensors="pt").to(self.device)
            
            # 3. Inference
            with torch.no_grad():
                outputs = self.model(**inputs)
                
            # 4. Extract Embedding (Pooler output or Mean of Last Hidden State)
            # ASTModel output has 'last_hidden_state' [batch, sequences, hidden]
            # and 'pooler_output' [batch, hidden] usually if configured, 
            # let's check attributes. ASTModel outputs BaseModelOutputWithPooling
            
            if hasattr(outputs, 'pooler_output') and outputs.pooler_output is not None:
                embedding = outputs.pooler_output
            else:
                # Average pooling over sequence dimension
                embedding = outputs.last_hidden_state.mean(dim=1)
                
            # Convert to list
            embedding_vector = embedding.cpu().numpy()[0].tolist()
            
            return {
                "embedding": embedding_vector,
                "status": "success",
                "model": self.MODEL_NAME,
                "dimensions": len(embedding_vector)
            }
            
        except Exception as e:
            logger.error(f"Deep Listening Analysis failed: {e}")
            return {
                "embedding": [0.0] * self.embedding_dim,
                "status": "error",
                "error": str(e)
            }
