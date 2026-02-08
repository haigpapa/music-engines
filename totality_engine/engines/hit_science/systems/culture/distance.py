import numpy as np
from typing import Dict, List

class CulturalDistanceEngine:
    def __init__(self):
        # Mock centroids for different markets based on "acousticness", "energy", "valence"
        self.market_centroids = {
            "TW": np.array([0.7, 0.4, 0.5]), # High acousticness
            "JP": np.array([0.2, 0.9, 0.8]), # High energy
            "US": np.array([0.3, 0.7, 0.6]),
            "BR": np.array([0.4, 0.8, 0.9])
        }
        
    def calculate_distance(self, track_vector: np.array, target_market: str) -> float:
        """
        Calculates Euclidean distance between track and market norm.
        Vector: [Acousticness, Energy, Valence]
        """
        centroid = self.market_centroids.get(target_market)
        if centroid is None:
            return 0.0 # Default / Unknown
            
        distance = np.linalg.norm(track_vector - centroid)
        return float(distance)
        
    def interpret_distance(self, distance: float) -> str:
        if distance < 0.2:
            return "Low Distance (Safe/Generic)"
        elif distance < 0.5:
            return "Moderate Distance (Sweet Spot)"
        else:
            return "High Distance (Outlier/Risk)"
