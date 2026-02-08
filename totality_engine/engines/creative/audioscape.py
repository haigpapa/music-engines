import subprocess
import json
import os
import shutil
from typing import Dict, Any, List, Optional
from totality_engine.core.engine import BaseEngine

class AudioscapeEngine(BaseEngine):
    """
    Engine for technical audio analysis (Loudness, LRA, True Peak).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.ffmpeg_bin = self._get_ffmpeg_bin()
        self.criteria = self.config.get("audioscape", {
            "streaming": {"target_lufs": -14, "tolerance": 2, "true_peak_max": -1.0},
            "club": {"target_lufs": -9, "tolerance": 2, "true_peak_max": -1.0},
            "lra": {"min": 3, "max": 15}
        })

    def _get_ffmpeg_bin(self) -> str:
        # Check for ffmpeg in common locations or path
        paths = ["/opt/homebrew/bin/ffmpeg", "ffmpeg"]
        for p in paths:
            if shutil.which(p):
                return p
        return "ffmpeg" # Hope it's in path if checking fails

    def validate(self, input_data: Any) -> bool:
        if not isinstance(input_data, str):
            return False
        if not os.path.exists(input_data):
            return False
        return True

    def analyze(self, input_data: str) -> Dict[str, Any]:
        """
        Runs ffmpeg ebur128 filter to extract Integrated Loudness (I), LRA, and True Peak.
        
        Args:
            input_data: Path to the audio file.
        """
        if not self.validate(input_data):
             return {"error": f"File not found or invalid: {input_data}"}

        stats = self._run_ffmpeg_analysis(input_data)
        if "error" in stats:
            return stats
            
        evaluation = self._evaluate(stats)
        return {
            "technical_profile": stats,
            "verdict": evaluation
        }

    def _run_ffmpeg_analysis(self, file_path: str) -> Dict[str, Any]:
        cmd = [
            self.ffmpeg_bin, 
            "-i", file_path, 
            "-af", "ebur128=peak=true", 
            "-f", "null", 
            "-"
        ]
        
        try:
            # ffmpeg outputs stats to stderr
            result = subprocess.run(cmd, capture_output=True, text=True)
            stderr = result.stderr
            
            stats = {}
            lines = stderr.split('\n')
            for line in lines:
                if "I:" in line and "LUFS" in line:
                    stats['lufs_i'] = float(line.split("I:")[1].split("LUFS")[0].strip())
                if "LRA:" in line and "LU" in line and "LRA low" not in line:
                    stats['lra'] = float(line.split("LRA:")[1].split("LU")[0].strip())
                if "True peak:" in line and "dBTP" in line:
                     stats['true_peak'] = float(line.split("True peak:")[1].split("dBTP")[0].strip())
            
            # Basic validation that we got data
            if not stats:
                 return {"error": "Failed to parse ffmpeg output", "raw_stderr": stderr[:200]}

            return stats

        except Exception as e:
            return {"error": str(e)}

    def _evaluate(self, stats: Dict[str, float]) -> Dict[str, Any]:
        report = {"passed": True, "checks": []}
        
        # 1. Loudness Check (Streaming)
        lufs = stats.get('lufs_i', -99)
        target = self.criteria['streaming']['target_lufs']
        tolerance = self.criteria['streaming']['tolerance']
        
        diff = abs(lufs - target)
        if diff <= tolerance:
            report['checks'].append(f"[PASS] Loudness ({lufs} LUFS) is close to Streaming Target ({target}).")
        elif lufs > target: 
            report['checks'].append(f"[WARN] Loudness ({lufs} LUFS) is louder than Streaming Target.")
        else:
            report['checks'].append(f"[FAIL] Loudness ({lufs} LUFS) is too quiet for Streaming.")
            report['passed'] = False

        # 2. Dynamic Range Check
        lra = stats.get('lra', 0)
        min_lra = self.criteria['lra']['min']
        
        if lra < min_lra:
            report['checks'].append(f"[WARN] LRA ({lra} LU) is crushed/smashed (< {min_lra}).")
        else:
            report['checks'].append(f"[PASS] LRA ({lra} LU) is healthy.")
            
        return report
