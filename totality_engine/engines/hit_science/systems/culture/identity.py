from typing import Dict

class IdentityEngine:
    def __init__(self):
        pass
        
    def check_brand_dissonance(self, artist_brand_keywords: list, track_sentiment: str, explicitness_score: float) -> Dict:
        """
        Checks if the track clashes with the artist's established brand.
        """
        dissonance = False
        reasons = []
        
        # Heuristic: Family-friendly artist releasing explicit track
        if "family-friendly" in artist_brand_keywords and explicitness_score > 0.0:
            dissonance = True
            reasons.append("Explicit content clashes with 'family-friendly' brand tag.")
            
        # Heuristic: Mood mismatch
        # e.g., "Wholesome" artist releasing "Dark/Aggressive" track
        if "wholesome" in artist_brand_keywords and track_sentiment == "Aggressive":
            dissonance = True
            reasons.append("Aggressive sentiment clashes with 'wholesome' brand tag.")
            
        return {
            "has_dissonance": dissonance,
            "reasons": reasons
        }
