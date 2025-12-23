import os
import json

from phase1.symbol_loader import load_symbols
from phase1.graph_builder import (
    build_contains_edges,
    add_import_edges,
    add_inherits_edges,
)

from phase0.utils import save_json


def run_phase1_7(repo_path: str):
    symbols_path = os.path.join(repo_path, "symbols.json")
    output_path = os.path.join(repo_path, "symbol_graph.json")

    symbols = load_symbols(symbols_path)

    graph = build_contains_edges(symbols)
    add_import_edges(graph, symbols)
    add_inherits_edges(graph, symbols)

    save_json(output_path, graph.to_dict())
    print("[Phase1.7] Symbol graph created successfully")


if __name__ == "__main__":
    run_phase1_7("storage/repos/psf__requests")
