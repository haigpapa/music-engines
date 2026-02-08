import subprocess
import os
import shutil
from typing import Dict, Any, List
from totality_engine.core.engine import BaseEngine

class CompositionEngine(BaseEngine):
    """
    Engine for structural audio analysis (boredom detection, drop detection).
    """

    def __init__(self, config=None):
        super().__init__(config)
        self.ffmpeg_bin = self._get_ffmpeg_bin()

    def _get_ffmpeg_bin(self) -> str:
        paths = ["/opt/homebrew/bin/ffmpeg", "ffmpeg"]
        for p in paths:
            if shutil.which(p):
                return p
        return "ffmpeg"

    def validate(self, input_data: Any) -> bool:
        if not isinstance(input_data, str):
            return False
        return os.path.exists(input_data)

    def analyze(self, input_data: str) -> Dict[str, Any]:
        """
        Analyzes audio structure using ffmpeg volume profiling.
        """
        if not self.validate(input_data):
            return {"error": f"File not found: {input_data}"}

        timeseries = self._get_volume_profile(input_data)
        structure = self._analyze_structure(timeseries)
        
        return {
            "structural_profile": structure,
            "verdict": self._get_verdict(structure)
        }

    def _get_volume_profile(self, file_path: str) -> List[Dict[str, float]]:
        cmd = [
            self.ffmpeg_bin, 
            "-i", file_path, 
            "-af", "ebur128=framelog=verbose", 
            "-f", "null", 
            "-"
        ]
        
        try:
            process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)
            timeseries = []
            
            while True:
                line = process.stderr.readline()
                if not line:
                    break
                
                if "t:" in line and "M:" in line:
                    try:
                        parts = line.split()
                        t_index = parts.index("t:") + 1
                        m_index = parts.index("M:") + 1
                        
                        t = float(parts[t_index])
                        m = float(parts[m_index])
                        
                        if m > -70: 
                            timeseries.append({"t": t, "lufs": m})
                    except ValueError:
                        continue
            return timeseries
        except Exception as e:
            print(f"Error profiling audio: {e}")
            return []

    def _analyze_structure(self, timeseries: List[Dict[str, float]]) -> Dict[str, Any]:
        structure = {
            "boredom_flags": [],
            "drop_points": [],
            "stats": {"duration": 0, "variance": 0}
        }
        
        if not timeseries:
            return structure
            
        structure["stats"]["duration"] = timeseries[-1]["t"]
        
        # 1. Boredom Detector
        self._detect_boredom(timeseries, structure)

        # 2. Drop Detector
        self._detect_drops(timeseries, structure)
                     
        return structure

    def _detect_boredom(self, timeseries: List[Dict[str, float]], structure: Dict[str, Any]):
        WINDOW_SIZE_SEC = 20
        STEP_SEC = 5
        values = [x["lufs"] for x in timeseries]
        
        for i in range(0, len(timeseries), int(STEP_SEC * 10)):
            window_end_idx = min(i + int(WINDOW_SIZE_SEC * 10), len(timeseries))
            if window_end_idx <= i: break
            
            window_vals = values[i:window_end_idx]
            if not window_vals: continue
            
            _range = max(window_vals) - min(window_vals)
            
            if _range < 3.0: 
                start_t = timeseries[i]["t"]
                end_t = timeseries[window_end_idx-1]["t"]
                if not structure["boredom_flags"] or start_t > structure["boredom_flags"][-1]["end"] + 5:
                    structure["boredom_flags"].append({
                        "start": round(start_t, 1), 
                        "end": round(end_t, 1), 
                        "type": "Static Energy"
                    })

    def _detect_drops(self, timeseries: List[Dict[str, float]], structure: Dict[str, Any]):
        JUMP_THRESHOLD = 4.0
        for i in range(10, len(timeseries)):
            current = timeseries[i]
            prev = timeseries[max(0, i - 10)]
            
            delta = current["lufs"] - prev["lufs"]
            
            if delta > JUMP_THRESHOLD:
                t = current["t"]
                if not structure["drop_points"] or t > structure["drop_points"][-1]["timestamp"] + 5:
                     structure["drop_points"].append({
                         "timestamp": round(t, 1),
                         "magnitude": round(delta, 1)
                     })

    def _get_verdict(self, structure: Dict[str, Any]) -> List[str]:
        verdicts = []
        if len(structure["boredom_flags"]) > 0:
            verdicts.append(f"[WARN] Detected {len(structure['boredom_flags'])} sections of potential boredom (>20s static).")
        else:
            verdicts.append("[PASS] Good dynamic movement throughout.")
            
        if len(structure["drop_points"]) > 0:
            verdicts.append(f"[PASS] Detected {len(structure['drop_points'])} significant energy drops/impacts.")
        else:
            verdicts.append("[WARN] Flat energy. No significant drops detected.")
        return verdicts
