from typing import Dict, Any, List
from totality_engine.core.engine import BaseEngine
from totality_engine.core.models import TotalitySong, AcousticFeatures

class ComparisonEngine(BaseEngine):
    """
    Engine for comparing two TotalitySong objects to find similarities and differences.
    """
    
    def analyze(self, input_data: Any) -> Dict[str, Any]:
        """
        Comparison engine expects input_data to be a tuple or list of two TotalitySong objects.
        """
        if not self.validate(input_data):
            return {"error": "Invalid input. Expected a list/tuple of two TotalitySong objects."}
            
        song_a, song_b = input_data
        return self.compare(song_a, song_b)

    def validate(self, input_data: Any) -> bool:
        if not isinstance(input_data, (list, tuple)) or len(input_data) != 2:
            return False
        return all(isinstance(s, TotalitySong) for s in input_data)

    def compare(self, song_a: TotalitySong, song_b: TotalitySong) -> Dict[str, Any]:
        """
        Detailed comparison logic.
        """
        return {
            "meta": {
                "song_a": song_a.title,
                "song_b": song_b.title
            },
            "acoustic_diff": self._compare_acoustic(song_a.acoustic, song_b.acoustic),
            "lyrical_overlap": self._compare_lyrical(song_a.lyrical, song_b.lyrical),
            "similarity_score": self._calculate_similarity(song_a, song_b)
        }

    def _compare_acoustic(self, a: AcousticFeatures, b: AcousticFeatures) -> Dict[str, Any]:
        return {
            "bpm_diff": round(abs(a.bpm - b.bpm), 2),
            "key_match": a.key == b.key,
            "energy_diff": round(abs(a.energy - b.energy), 2),
            "lufs_diff": round(abs(a.lufs - b.lufs), 2)
        }

    def _compare_lyrical(self, a: Any, b: Any) -> Dict[str, Any]:
        # Using Any type hint for sub-models to avoid strict dependency if models change
        common_themes = set(a.themes).intersection(set(b.themes))
        return {
            "common_themes": list(common_themes),
            "sentiment_gap": round(abs(a.sentiment_valence - b.sentiment_valence), 2)
        }

    def _calculate_similarity(self, a: TotalitySong, b: TotalitySong) -> float:
        """
        Weighted similarity score (0.0 to 1.0).
        """
        score = 0.0
        
        # BPM similarity (within 10 BPM is good)
        bpm_diff = abs(a.acoustic.bpm - b.acoustic.bpm)
        if bpm_diff < 5: score += 0.3
        elif bpm_diff < 15: score += 0.15
        
        # Key match
        if a.acoustic.key == b.acoustic.key:
            score += 0.2
            
        # Genre/Era match (implied by lack of explicit genre field, using simple checks)
        if a.historical.era == b.historical.era:
            score += 0.1
            
        # Lyrical commonality
        common_themes = set(a.lyrical.themes).intersection(set(b.lyrical.themes))
        if common_themes:
            score += 0.2
            
        return min(round(score, 2), 1.0)
