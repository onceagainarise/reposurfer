import ast

class PythonSymbolExtractor(ast.NodeVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.imports = []
        self.symbols = []
        self.current_class = None
    
    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.append(node.module)
            self.generic_visit(node)

    def visit_FunctionDef(self, node):
        parent = self.current_class
    
        symbol_type = "method" if parent else "function"
    
        symbol_id = (
            f"{parent}.{node.name}"
            if parent else node.name
        )
    
        self.symbols.append({
            "symbol_id": symbol_id,
            "type": symbol_type,
            "name": node.name,
            "file": self.file_path,
            "start_line": node.lineno,
            "end_line": node.end_lineno,
            "parent": parent,
            "docstring": ast.get_docstring(node),
        })
    
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        class_name = node.name
        prev_class = self.current_class
        self.current_class = class_name
    
        self.symbols.append({
            "symbol_id": class_name,
            "type": "class",
            "name": class_name,
            "file": self.file_path,
            "start_line": node.lineno,
            "end_line": node.end_lineno,
            "parent": None,
            "docstring": ast.get_docstring(node),
        })
    
        self.generic_visit(node)
        self.current_class = prev_class
