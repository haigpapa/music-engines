import numpy as np
import librosa
from typing import Dict, Any

class AudioAnalyzer:
    def __init__(self):
        pass

    def analyze(self, audio_path: str) -> Dict[str, Any]:
        """
        Main entry point for audio analysis.
        """
        try:
            y, sr = librosa.load(audio_path)
        except Exception as e:
            print(f"Error loading audio: {e}")
            return {}

        features = {}
        
        # 1.1 Onset Strength & Spectral Flux
        features.update(self._current_flux_analysis(y, sr))
        
        # 1.1 Microtiming / Groove (Simplified)
        features.update(self._groove_analysis(y, sr))
        
        return features

    def _current_flux_analysis(self, y, sr) -> Dict[str, float]:
        """
        Computes Onset Strength and Spectral Flux to detect 'Muddy' mixes.
        """
        # Compute onset strength envelope
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        
        # Spectral Flux is essentially the onset strength
        avg_flux = np.mean(onset_env)
        var_flux = np.var(onset_env)
        
        # "Muddy" Fragility: Low variance in onset strength implies smeared transients
        is_muddy = var_flux < 1.0 # Threshold would need calibration
        
        return {
            "spectral_flux_mean": float(avg_flux),
            "spectral_flux_variance": float(var_flux),
            "is_muddy_mix": bool(is_muddy)
        }

    def _groove_analysis(self, y, sr) -> Dict[str, float]:
        """
        Analyzes rhythmic properties.
        """
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        
        # Microtiming deviation would require comparing detected onsets to a rigid grid
        # For prototype, we return basic rhythm features
        return {
            "tempo": float(tempo),
            "beat_strength": float(np.mean(librosa.util.normalize(librosa.onset.onset_strength(y=y, sr=sr)[beat_frames]))) if len(beat_frames) > 0 else 0.0
        }
