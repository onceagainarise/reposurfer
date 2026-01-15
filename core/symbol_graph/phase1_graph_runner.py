import os
import json
from tqdm import tqdm

from reposurfer.core.symbol_graph.symbol_loader import load_symbols
from reposurfer.core.symbol_graph.graph_builder import (
    SymbolGraph,
    GraphNode,
    GraphEdge,
    add_import_edges,
    add_inherits_edges,
)

from reposurfer.core.clone.utils import save_json


def run_phase1_7(repo_path: str):
    print(f"[Phase1.7] Building symbol graph...")
    
    symbols_path = os.path.join(repo_path, "symbols.json")
    output_path = os.path.join(repo_path, "symbol_graph.json")

    symbols = load_symbols(symbols_path)
    print(f"[Phase1.7] Processing {len(symbols)} symbols...")

    # Initialize graph once
    graph = SymbolGraph()
    
    # Progress bar for adding nodes
    with tqdm(symbols, desc="Adding symbol nodes", unit="symbol") as pbar:
        for sym in pbar:
            symbol_id = sym["symbol_id"]
            symbol_type = sym["type"]
            file_path = sym["file"]

            # Add symbol node
            graph.add_node(
                GraphNode(
                    id=symbol_id,
                    type=symbol_type,
                    file=file_path,
                )
            )

            # Add file node if not already added
            if file_path not in graph.nodes:
                graph.add_node(
                    GraphNode(
                        id=file_path,
                        type="file",
                        file=file_path,
                    )
                )

            # Add containment edge
            if sym["parent"]:
                graph.add_edge(
                    GraphEdge(
                        type="CONTAINS",
                        source=sym["parent"],
                        target=symbol_id,
                    )
                )
            else:
                graph.add_edge(
                    GraphEdge(
                        type="CONTAINS",
                        source=file_path,
                        target=symbol_id,
                    )
                )
            
            pbar.set_postfix({"nodes": len(graph.nodes), "edges": len(graph.edges)})

    # Add import edges
    print(f"[Phase1.7] Adding import relationships...")
    with tqdm(symbols, desc="Adding import edges", unit="symbol") as pbar:
        for sym in pbar:
            if sym.get("imports"):
                for imp in sym["imports"]:
                    graph.add_edge(
                        GraphEdge(
                            type="IMPORTS",
                            source=symbol_id,
                            target=imp,
                        )
                    )
                pbar.set_postfix({"imports": len(sym.get("imports", []))})

    # Add inheritance edges
    print(f"[Phase1.7] Adding inheritance relationships...")
    add_inherits_edges(graph, symbols)

    save_json(output_path, graph.to_dict())
    print(f"[Phase1.7] ✅ Symbol graph created: {len(graph.nodes)} nodes, {len(graph.edges)} edges")


if __name__ == "__main__":
    run_phase1_7("storage/repos/psf__requests")
