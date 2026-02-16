from totality_engine.core.graph_db import get_graph_db

class NetworkAnalyst:
    def __init__(self):
        self.db = get_graph_db()
        
    def analyze_network_health(self):
        """
        Calculates global network metrics using Neo4j.
        """
        # Count total nodes and potential clustering
        if not self.db.driver: return {}
        
        query = "MATCH (n) RETURN count(n) as total_nodes"
        res = self.db.execute_query(query)
        return {
            "total_nodes": res[0]['total_nodes'] if res else 0,
            "status": "connected"
        }
        
    def get_artist_centrality(self, artist_id: str):
        """
        Calculates Degree Centrality for an artist (Number of Tracks).
        """
        if not self.db.driver: return 0.0
        
        # Cypher: Count outgoing relationships (PERFORMED -> Track)
        query = """
        MATCH (a:Artist {id: $artist_id})-[r:PERFORMED]->(t:Track)
        RETURN count(r) as degree
        """
        res = self.db.execute_query(query, {"artist_id": artist_id})
        
        if res:
            degree = res[0]['degree']
            # Normalize? Let's just return degree for now.
            # Centrality 0.0 - 1.0 logic depends on total graph size.
            # For MVP, return raw count. Frontend can normalize if needed.
            return float(degree)
            
        return 0.0
