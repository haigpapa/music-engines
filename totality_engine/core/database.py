import networkx as nx

class GraphDatabase:
    _instance = None
    
    def __init__(self):
        self.graph = nx.Graph()
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
    def add_node(self, node_id, label, properties, **kwargs):
        # Merge properties and kwargs
        props = properties.copy()
        props.update(kwargs)
        self.graph.add_node(node_id, label=label, **props)
        
    def add_edge(self, source_id, target_id, relationship, properties=None, **kwargs):
        if properties is None:
            properties = {}
        props = properties.copy()
        props.update(kwargs)
        self.graph.add_edge(source_id, target_id, relationship=relationship, **props)
        
    def get_centrality(self):
        if len(self.graph) == 0:
            return {}
        return nx.degree_centrality(self.graph)
        
    def find_structural_holes(self):
        if len(self.graph) == 0:
            return {}
        # NetworkX constraint implementation for structural holes
        try:
            return nx.constraint(self.graph)
        except Exception:
             return {}

def get_graph_db():
    return GraphDatabase.get_instance()
