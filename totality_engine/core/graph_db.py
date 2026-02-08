from neo4j import GraphDatabase
import os
import logging

logger = logging.getLogger(__name__)

class GraphDB:
    _instance = None
    
    def __init__(self):
        uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
        user = os.environ.get("NEO4J_USER", "neo4j")
        password = os.environ.get("NEO4J_PASSWORD", "password") # Default community password
        
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            logger.info(f"Connected to Neo4j at {uri}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            self.driver = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def close(self):
        if self.driver:
            self.driver.close()
            
    def get_session(self):
        if self.driver:
            return self.driver.session()
        return None

    def execute_query(self, query, parameters=None):
        """
        Execute a Cypher query and return the results as a list of dictionaries.
        """
        if not self.driver:
            logger.warning("Neo4j driver not initialized.")
            return []
            
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

# Global accessor
def get_graph_db():
    return GraphDB.get_instance()
