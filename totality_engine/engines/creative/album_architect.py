import os
import statistics
import json
from typing import Dict, Any, List
from totality_engine.core.engine import BaseEngine
from totality_engine.engines.creative.audioscape import AudioscapeEngine

class AlbumArchitectEngine(BaseEngine):
    """
    Engine for analyzing cohesion across a collection of tracks.
    """

    def __init__(self, config=None):
        super().__init__(config)
        self.audioscape = AudioscapeEngine(config)

    def validate(self, input_data: Any) -> bool:
        if not isinstance(input_data, str):
            return False
        return os.path.exists(input_data) and os.path.isdir(input_data)

    def analyze(self, input_data: str) -> Dict[str, Any]:
        """
        Analyzes a directory of audio files for cohesion.
        """
        directory = input_data
        files = self._get_audio_files(directory)
        
        if not files:
            return {"error": "No audio files found in directory"}

        tracks_data = []
        lufs_values = []
        
        for f in files:
            result = self.audioscape.analyze(f)
            if "technical_profile" in result:
                tech = result["technical_profile"]
                tracks_data.append({
                    "file": os.path.basename(f),
                    "lufs": tech.get('lufs_i', 0),
                    "lra": tech.get('lra', 0)
                })
                lufs_values.append(tech.get('lufs_i', 0))
            
        if not lufs_values:
             return {"error": "Could not extract data from tracks"}

        structure = self._calculate_cohesion(lufs_values, tracks_data, len(files))
        
        return {
            "album_profile": structure,
            "verdict": self._get_verdict(structure)
        }

    def _get_audio_files(self, directory: str) -> List[str]:
        files = []
        for f in os.listdir(directory):
            if f.lower().endswith(('.wav', '.mp3', '.aiff', '.flac')):
                files.append(os.path.join(directory, f))
        return sorted(files)

    def _calculate_cohesion(self, lufs_values: List[float], tracks_data: List[Dict], count: int) -> Dict[str, Any]:
        # Cohesion Logic
        avg_lufs = statistics.mean(lufs_values)
        lufs_std_dev = statistics.stdev(lufs_values) if count > 1 else 0
        lufs_range = max(lufs_values) - min(lufs_values)

        return {
            "track_count": count,
            "average_lufs": round(avg_lufs, 2),
            "consistency_score": "High" if lufs_std_dev < 1.0 else "Low", 
            "lufs_range": round(lufs_range, 2),
            "std_dev": round(lufs_std_dev, 2),
            "tracks": tracks_data
        }

    def _get_verdict(self, structure: Dict[str, Any]) -> List[str]:
        verdicts = []
        if structure["lufs_range"] > 2.0:
            verdicts.append(f"[WARN] Inconsistent Loudness. Range is {structure['lufs_range']:.1f} LU (max diff).")
            verdicts.append("-> Listener will have to adjust volume between tracks.")
        else:
            verdicts.append(f"[PASS] Excellent Cohesion. Range is {structure['lufs_range']:.1f} LU.")
        return verdicts
