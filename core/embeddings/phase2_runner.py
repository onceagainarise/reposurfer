import json
import os
from phase2.symbol_chunk_builder import SymbolChunkBuilder

def run_phase2(repo_path: str):
    graph_path = os.path.join(repo_path, "symbol_graph.json")

    with open(graph_path, "r") as f:
        symbol_graph = json.load(f)

    builder = SymbolChunkBuilder(repo_path)
    chunks = builder.build_chunks(symbol_graph)

    out_path = os.path.join(repo_path, "symbol_chunks.json")
    with open(out_path, "w") as f:
        json.dump(chunks, f, indent=2)

    print(f"[Phase2] Built {len(chunks)} symbol chunks")

if __name__ == "__main__":
    run_phase2("storage/repos/psf__requests")
