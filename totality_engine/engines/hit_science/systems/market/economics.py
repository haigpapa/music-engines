from typing import Dict, List

class EconomicsEngine:
    def __init__(self):
        # Average Per-Stream Payout (blended) estimates
        self.payout_rates = {
            "US": 0.0035,
            "GB": 0.0031,
            "DE": 0.0030,
            "BR": 0.0012,
            "IN": 0.0006,
            "PH": 0.0005
        }
        
    def calculate_revenue_potential(self, forecasted_streams: Dict[str, int]) -> float:
        """
        Calculates Revenue Potential (RP) = Sum(Streams_i * Payout_i)
        """
        total_revenue = 0.0
        for country, streams in forecasted_streams.items():
            rate = self.payout_rates.get(country, 0.0010) # Default global avg
            total_revenue += streams * rate
            
        return total_revenue
