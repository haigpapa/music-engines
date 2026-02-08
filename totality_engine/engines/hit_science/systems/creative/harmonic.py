import librosa
import numpy as np
import scipy.stats

class HarmonicAnalyzer:
    def __init__(self):
        pass
        
    def analyze_harmony(self, audio_path: str):
        try:
            y, sr = librosa.load(audio_path)
            chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
            
            # Calculate entropy of the chroma features over time
            # High entropy = high unpredictability in harmonic content
            entropy_per_frame = scipy.stats.entropy(chroma, axis=0)
            avg_entropy = np.mean(entropy_per_frame)
            
            # Expectancy Violation: 
            # This is hard to model without a trained discrete HMM. 
            # We will use the variance of the entropy as a proxy for "surprise"
            entropy_variance = np.var(entropy_per_frame)
            
            return {
                "harmonic_entropy": float(avg_entropy),
                "expectancy_violation_score": float(entropy_variance)
            }
        except Exception as e:
            print(f"Harmonic analysis failed: {e}")
            return {}
