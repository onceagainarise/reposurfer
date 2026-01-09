import json
import os
from tqdm import tqdm
from reposurfer.core.embeddings.symbol_chunk_builder import SymbolChunkBuilder

def run_phase2(repo_path: str):
    print(f"[Phase2] Starting symbol chunking...")
    
    graph_path = os.path.join(repo_path, "symbol_graph.json")

    with open(graph_path, "r") as f:
        symbol_graph = json.load(f)

    nodes = symbol_graph.get("nodes", [])
    print(f"[Phase2] Processing {len(nodes)} symbol nodes...")

    builder = SymbolChunkBuilder(repo_path)
    
    # Progress bar for chunk building
    with tqdm(nodes, desc="Building symbol chunks", unit="node") as pbar:
        chunks = []
        for node in pbar:
            if node["type"] in {"class", "method", "function"}:
                chunk = builder._build_chunk(node)
                if chunk:
                    chunks.append(chunk)
            pbar.set_postfix({"chunks": len(chunks), "valid": node["type"] in {"class", "method", "function"}})

    out_path = os.path.join(repo_path, "symbol_chunks.json")
    with open(out_path, "w") as f:
        json.dump(chunks, f, indent=2)

    print(f"[Phase2] Built {len(chunks)} symbol chunks")

if __name__ == "__main__":
    run_phase2("storage/repos/psf__requests")
