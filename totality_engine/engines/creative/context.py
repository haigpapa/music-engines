import os
import json
from typing import Dict, Any, List
from totality_engine.core.engine import BaseEngine
from totality_engine.engines.creative.audioscape import AudioscapeEngine

class ContextEngine(BaseEngine):
    """
    Engine using reference standards to benchmark tracks.
    """

    def __init__(self, config=None):
        super().__init__(config)
        self.audioscape = AudioscapeEngine(config)
        # Load standards from config or use defaults/file
        # Assuming config loader handles this, or we load a local json for now as fallback
        self.standards = self._load_standards()

    def _load_standards(self) -> Dict[str, Any]:
        # For now, hardcode or load from sibling file if exists (mimicking old behavior but cleaner)
        # Ideally this goes into engines_config.yaml
        script_dir = os.path.dirname(os.path.realpath(__file__))
        standards_file = os.path.join(script_dir, "reference_standards.json")
        if os.path.exists(standards_file):
            with open(standards_file, 'r') as f:
                return json.load(f)
        return {"standards": {}} # Fallback

    def validate(self, input_data: Any) -> bool:
        if not isinstance(input_data, dict):
            return False
        return "file_path" in input_data and "genre_key" in input_data

    def analyze(self, input_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Benchmarks a track against a genre standard.
        Input: {"file_path": str, "genre_key": str}
        """
        file_path = input_data["file_path"]
        genre_key = input_data["genre_key"]

        if not os.path.exists(file_path):
             return {"error": f"File not found: {file_path}"}
        
        if genre_key not in self.standards.get("standards", {}):
             return {"error": f"Genre '{genre_key}' not found in standards."}

        # Run Audio Analysis
        audio_result = self.audioscape.analyze(file_path)
        if "error" in audio_result:
            return audio_result
            
        stats = audio_result.get("technical_profile", {})
        
        # Benchmark
        result = self._benchmark(stats, genre_key)
        
        return {
            "market_readiness_score": result["score"],
            "genre": genre_key,
            "report": result["report"]
        }

    def _benchmark(self, track_stats: Dict[str, float], genre_key: str) -> Dict[str, Any]:
        std = self.standards['standards'][genre_key]
        
        track_lufs = track_stats.get('lufs_i', -99)
        track_lra = track_stats.get('lra', 0)
        
        score = 100
        report = []
        
        # 1. Loudness Check
        lufs_diff = abs(track_lufs - std['lufs_target'])
        if lufs_diff <= std['lufs_tolerance']:
            report.append(f"[PASS] Loudness {track_lufs} is within tolerance of {std['lufs_target']}.")
        else:
            penalty = min(20, lufs_diff * 2)
            score -= penalty
            report.append(f"[FAIL] Loudness {track_lufs} deviates from target {std['lufs_target']} (Diff: {lufs_diff:.1f}). Penalty: -{int(penalty)}")

        # 2. LRA Check
        if std['lra_min'] <= track_lra <= std['lra_max']:
            report.append(f"[PASS] Dynamics {track_lra} LU is within range [{std['lra_min']}-{std['lra_max']}].")
        else:
            score -= 10
            report.append(f"[WARN] Dynamics {track_lra} LU is outside range [{std['lra_min']}-{std['lra_max']}]. Penalty: -10")
            
        return {
            "score": max(0, int(score)),
            "report": report
        }
