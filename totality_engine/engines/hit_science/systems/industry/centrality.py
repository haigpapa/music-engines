from totality_engine.core.database import get_graph_db

class NetworkAnalyst:
    def __init__(self):
        self.db = get_graph_db()
        
    def analyze_network_health(self):
        """
        Calculates centrality and structural holes.
        """
        centrality_scores = self.db.get_centrality()
        constraint_scores = self.db.find_structural_holes()
        
        return {
            "centrality_metrics": centrality_scores,
            "structural_holes": constraint_scores
        }
        
    def get_artist_centrality(self, artist_id: str):
        scores = self.db.get_centrality()
        return scores.get(artist_id, 0.0)
