from typing import Dict, List

class PlatformOptimizer:
    def __init__(self):
        pass
        
    def get_optimizations(self, track_features: Dict, platform: str) -> List[str]:
        recommendations = []
        
        if platform.lower() == "spotify":
            if track_features.get("duration_ms", 0) > 210000: # 3:30
                recommendations.append("Consider a 'Radio Edit' under 3:00 to increase replay ratio.")
            if track_features.get("intro_length", 0) > 15:
                recommendations.append("Intro is too long (>15s). High skip risk. Cut to <5s.")
                
        elif platform.lower() == "tiktok":
            if not track_features.get("has_high_energy_drop", False):
                 recommendations.append("Lack of distinct 'drop' or 'hook' moment. Create a remix with higher onset strength variance.")
            if track_features.get("tempo", 120) < 110:
                recommendations.append("Tempo is low. Release a 'Sped Up' version (+15-20%) for higher energy.")
                
        return recommendations
