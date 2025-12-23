from phase1.symbol_graph import SymbolGraph, GraphNode, GraphEdge


def build_contains_edges(symbols):
    graph = SymbolGraph()

    for sym in symbols:
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

        # Add file node
        graph.add_node(
            GraphNode(
                id=file_path,
                type="file",
                file=file_path,
            )
        )

        # Containment logic
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

    return graph

def add_import_edges(graph: SymbolGraph, symbols):
    for sym in symbols:
        file_node = sym["file"]

        for module in sym.get("imports", []):
            graph.add_node(
                GraphNode(
                    id=module,
                    type="module",
                    file="",
                )
            )

            graph.add_edge(
                GraphEdge(
                    type="IMPORTS",
                    source=file_node,
                    target=module,
                )
            )

def add_inherits_edges(graph: SymbolGraph, symbols):
    for sym in symbols:
        if sym["type"] != "class":
            continue

        for base in sym.get("bases", []):
            graph.add_edge(
                GraphEdge(
                    type="INHERITS",
                    source=sym["symbol_id"],
                    target=base,
                )
            )

def add_call_edges(graph: SymbolGraph, call_map):
    for caller, callees in call_map.items():
        for callee in callees:
            graph.add_edge(
                GraphEdge(
                    type="CALLS",
                    source=caller,
                    target=callee,
                )
            )
