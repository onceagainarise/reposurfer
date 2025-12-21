import os
import ast

class SymbolChunkBuilder:
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self._ast_cache = {}
        self._source_cache = {}

    def build_chunks(self, symbol_graph: dict):
        chunks = []

        for node in symbol_graph.get("nodes", []):
            if node["type"] not in {"class", "method", "function"}:
                continue

            chunk = self._build_chunk(node)
            if chunk:
                chunks.append(chunk)

        return chunks

    def _build_chunk(self, node: dict):
        rel_path = node["file"]
        abs_path = os.path.join(self.repo_root, "source", rel_path)
    
        if not os.path.exists(abs_path):
            return None
    
        tree, source_lines = self._parse_file(abs_path)
    
        # -------- CLASS SUPPORT --------
        if node["type"] == "class":
            for ast_node in ast.walk(tree):
                if isinstance(ast_node, ast.ClassDef) and ast_node.name == node["id"]:
                    return self._make_chunk(
                        symbol_id=node["id"],
                        symbol_type="class",
                        ast_node=ast_node,
                        source_lines=source_lines,
                        rel_path=rel_path,
                        metadata={}
                    )
    
        # -------- FUNCTION SUPPORT --------
        if node["type"] == "function":
            for ast_node in ast.walk(tree):
                if isinstance(ast_node, ast.FunctionDef) and ast_node.name == node["id"]:
                    return self._make_chunk(
                        symbol_id=node["id"],
                        symbol_type="function",
                        ast_node=ast_node,
                        source_lines=source_lines,
                        rel_path=rel_path,
                        metadata={}
                    )
        # -------- METHOD SUPPORT --------
        if node["type"] == "method":
            if "." not in node["id"]:
                return None
    
            class_name, method_name = node["id"].split(".", 1)
    
            for ast_node in ast.walk(tree):
                if isinstance(ast_node, ast.ClassDef) and ast_node.name == class_name:
                    for body_item in ast_node.body:
                        if isinstance(body_item, ast.FunctionDef) and body_item.name == method_name:
                            return self._make_chunk(
                                symbol_id=node["id"],
                                symbol_type="method",
                                ast_node=body_item,
                                source_lines=source_lines,
                                rel_path=rel_path,
                                metadata={
                                    "parent_class": class_name
                                }
                            )
    
        
            return None
    
    def _make_chunk(
        self,
        symbol_id: str,
        symbol_type: str,
        ast_node,
        source_lines,
        rel_path: str,
        metadata: dict
):    
        docstring = ast.get_docstring(ast_node)
        code_text = self._extract_node_text(ast_node, source_lines)
        if len(code_text.strip()) < 30:
            return None

        text_parts = [
            f"{symbol_type.capitalize()} {symbol_id} defined in {rel_path}"
        ]
    
        if docstring:
            text_parts.append(f"Docstring:\n{docstring}")
    
        text_parts.append("Code:\n" + code_text)
    
        return {
            "symbol_id": symbol_id,
            "symbol_type": symbol_type,
            "file": rel_path,
            "text": "\n\n".join(text_parts),
            "metadata": metadata
        }
    


    def _parse_file(self, file_path: str):
        if file_path in self._ast_cache:
            return self._ast_cache[file_path], self._source_cache[file_path]

        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)
        self._ast_cache[file_path] = tree
        self._source_cache[file_path] = source.splitlines()

        return tree, self._source_cache[file_path]

    def _extract_node_text(self, ast_node, source_lines):
        start = ast_node.lineno - 1
        end = ast_node.end_lineno
        return "\n".join(source_lines[start:end])
