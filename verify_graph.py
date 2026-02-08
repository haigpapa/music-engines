from totality_engine.core.graph_db import get_graph_db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_graph():
    print("--- Verifying Knowledge Graph ---")
    db = get_graph_db()
    
    if not db.driver:
        print("❌ FAILURE: Neo4j driver not connected.")
        return

    # Check for Track nodes
    tracks = db.execute_query("MATCH (t:Track) RETURN t.id, t.title, t.vibe LIMIT 5")
    print(f"Tracks Found: {len(tracks)}")
    for t in tracks:
        print(f" - {t['t.title']} ({t['t.vibe']})")
        
    # Check for Concepts (Vibe nodes)
    concepts = db.execute_query("MATCH (c:Concept) RETURN c.name LIMIT 5")
    print(f"Concepts Found: {len(concepts)}")
    for c in concepts:
        print(f" - {c['c.name']}")
        
    if len(tracks) > 0:
        print("✅ SUCCESS: Data exists in the Knowledge Graph.")
    else:
        print("⚠️ WARNING: Graph is empty. Run an analysis first.")

if __name__ == "__main__":
    verify_graph()
