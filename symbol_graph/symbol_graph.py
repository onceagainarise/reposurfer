from dataclasses import dataclass
from typing import List, Dict

@dataclass
class GraphNode:
    id: str
    type: str
    file: str

@dataclass
class GraphEdge:
    type: str
    source: str
    target: str

class SymbolGraph:
    def __init__(self):
        self.nodes: Dict[str, GraphNode] ={}
        self.edges: List[GraphEdge] = []
    
    def add_node(self, node: GraphNode):
        self.nodes[node.id]=node
    
    def add_edge(self, edge: GraphEdge):
        self.edges.append(edge)

    def to_dict(self):
        return {
            "nodes": [vars(n) for n in self.nodes.values()],
            "edges": [vars(e) for e in self.edges], 
        }