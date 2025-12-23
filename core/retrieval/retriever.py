from phase2.embedding_generator import EmbeddingGenerator
from phase2.graph_utils import (
    build_node_index,
    get_neighbors,
    compute_graph_score
)


class RepoRetriever:
    def __init__(self, vector_store, symbol_graph, embedder, alpha=0.7):
        self.vector_store = vector_store
        self.symbol_graph = symbol_graph
        self.embedder = embedder
        self.alpha = alpha  # weight for vector_score
        self.beta = 1 - alpha  # weight for graph_score
        self.node_index = build_node_index(symbol_graph)

    def query(self, text: str, top_k: int = 5):
        query_vector = self.embedder.embed([text])[0]
        hits = self.vector_store.search(query_vector, limit=top_k)
    
        expanded = {}
    
        for hit in hits:
            symbol_id = hit.payload["symbol_id"]
    
            vector_score = hit.score
            graph_score = compute_graph_score(
                self.symbol_graph, symbol_id, symbol_id
            )
    
            final_score = self.alpha * vector_score + self.beta * graph_score
    
            expanded[symbol_id] = {
                "id": hit.payload["symbol_id"],
                "type": hit.payload["symbol_type"],
                "file": hit.payload["file"],
                "score": final_score,
                "source": "vector"
            }

    
            # Graph expansion
            neighbors = get_neighbors(self.symbol_graph, symbol_id)
            for nid in neighbors:
                if nid in self.node_index and nid not in expanded:
                    g_score = compute_graph_score(
                        self.symbol_graph, symbol_id, nid
                    )
    
                    expanded[nid] = {
                        "id": nid,
                        "type": self.node_index[nid]["type"],
                        "file": self.node_index[nid]["file"],
                        "score": self.beta * g_score,
                        "source": "graph"
                    }

    
        return sorted(
            expanded.values(),
            key=lambda x: x["score"],
            reverse=True
        )
    