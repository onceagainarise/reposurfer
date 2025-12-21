def build_node_index(symbol_graph: dict):
    return {node["id"]: node for node in symbol_graph.get("nodes",[])}

def build_adjacency(symbol_graph: dict):
    adjacency = {}

    for edge in symbol_graph.get("edges", []):
        src = edge["source"]
        dst = edge["target"]

        adjacency.setdefault(src, set()).add(dst)
        adjacency.setdefault(dst, set()).add(src)

    return adjacency


def get_neighbors(symbol_graph: dict, symbol_id: str):
    adjacency = build_adjacency(symbol_graph)
    return adjacency.get(symbol_id, set())


def compute_graph_score(symbol_graph: dict, center_id: str, target_id: str):
    """
    Simple graph scoring:
    - same node → 1.0
    - direct neighbor → 0.6
    - otherwise → 0.0
    """
    if center_id == target_id:
        return 1.0

    neighbors = get_neighbors(symbol_graph, center_id)
    if target_id in neighbors:
        return 0.6

    return 0.0

