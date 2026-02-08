from totality_engine.core.graph_db import get_graph_db
import logging

logger = logging.getLogger(__name__)

class IndustryGraph:
    def __init__(self):
        self.db = get_graph_db()
        self.create_constraints()
        
    def create_constraints(self):
        """Ensure uniqueness for core entities"""
        if not self.db.driver: return
        
        queries = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (a:Artist) REQUIRE a.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (t:Track) REQUIRE t.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (g:Genre) REQUIRE g.name IS UNIQUE"
        ]
        
        with self.db.driver.session() as session:
            for q in queries:
                try:
                    session.run(q)
                except Exception as e:
                    logger.warning(f"Constraint creation failed: {e}")

    def add_track_node(self, track_id: str, metadata: dict, analysis_results: dict):
        """
        Create a full graph representation of the track analysis.
        """
        if not self.db.driver: return
        
        with self.db.driver.session() as session:
            # 1. Create Track Node
            session.run("""
                MERGE (t:Track {id: $id})
                SET t.title = $title, 
                    t.timestamp = datetime(),
                    t.vibe = $vibe,
                    t.dissonance = $dissonance
            """, {
                "id": track_id,
                "title": metadata.get("filename", "Unknown Track"),
                "vibe": analysis_results.get("resonance", {}).get("vibe", "Unknown"),
                "dissonance": analysis_results.get("resonance", {}).get("dissonance_score", 0.0)
            })
            
            # 2. Link Artist
            artist_id = metadata.get("artist_id", "unknown")
            session.run("""
                MERGE (a:Artist {id: $artist_id})
                MERGE (t:Track {id: $track_id})
                MERGE (a)-[:PERFORMED]->(t)
            """, {"artist_id": artist_id, "track_id": track_id})
            
            # 3. Create 'Vibe' Node (Concept)
            vibe = analysis_results.get("resonance", {}).get("vibe")
            if vibe:
                # Simplify vibe string "Anthemic Joy (Aligned)" -> "Anthemic Joy"
                vibe_concept = vibe.split("(")[0].strip()
                session.run("""
                    MERGE (c:Concept {name: $name})
                    MERGE (t:Track {id: $track_id})
                    MERGE (t)-[:HAS_VIBE]->(c)
                """, {"name": vibe_concept, "track_id": track_id})
                
            logger.info(f"Graph nodes created for Track {track_id}")

