from reposurfer.core.embeddings.embedding_generator import EmbeddingGenerator
from reposurfer.core.retrieval.graph_utils import (
    build_node_index,
    get_neighbors,
    compute_graph_score
)
import json
from pathlib import Path


class RepoRetriever:
    def __init__(self, vector_store, symbol_graph, embedder, alpha=0.7):
        self.vector_store = vector_store
        self.symbol_graph = symbol_graph
        self.embedder = embedder
        self.alpha = alpha  # weight for vector_score
        self.beta = 1 - alpha  # weight for graph_score
        self.node_index = build_node_index(symbol_graph)
        
        # Load symbol chunks for text content
        self.repo_name = vector_store.collection
        self.chunks_file = Path(f"storage/repos/{self.repo_name}/symbol_chunks.json")
        self.symbol_chunks = {}
        if self.chunks_file.exists():
            with open(self.chunks_file, 'r') as f:
                chunks = json.load(f)
                for chunk in chunks:
                    self.symbol_chunks[chunk['symbol_id']] = chunk

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
    
            # Get text content from symbol chunks
            symbol_chunk = self.symbol_chunks.get(symbol_id, {})
            
            expanded[symbol_id] = {
                "id": hit.payload["symbol_id"],
                "type": hit.payload["symbol_type"],
                "file": hit.payload["file"],
                "text": symbol_chunk.get("text", ""),
                "start_line": symbol_chunk.get("start_line"),
                "end_line": symbol_chunk.get("end_line"),
                "confidence": final_score,
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
                    
                    # Get text content for neighbor
                    neighbor_chunk = self.symbol_chunks.get(nid, {})
    
                    expanded[nid] = {
                        "id": nid,
                        "type": self.node_index[nid]["type"],
                        "file": self.node_index[nid]["file"],
                        "text": neighbor_chunk.get("text", ""),
                        "start_line": neighbor_chunk.get("start_line"),
                        "end_line": neighbor_chunk.get("end_line"),
                        "confidence": self.beta * g_score,
                        "score": self.beta * g_score,
                        "source": "graph"
                    }
    
    
        return sorted(
            expanded.values(),
            key=lambda x: x["score"],
            reverse=True
        )[:top_k]