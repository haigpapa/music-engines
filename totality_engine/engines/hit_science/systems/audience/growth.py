class GrowthAIEngine:
    def __init__(self):
        pass
        
    def calculate_k_factor(self, invites_sent: int, conversion_rate: float) -> float:
        """
        k = i * c
        """
        return invites_sent * conversion_rate
        
    def recommend_intervention(self, k_factor: float) -> str:
        if k_factor < 1.0:
            return "Viral Loop Broken. Recommended: Launch 'Remix Challenge' to boost 'invites' (shares)."
        else:
            return "Viral Loop Healthy. Recommended: Scale ad spend to fuel the fire."
