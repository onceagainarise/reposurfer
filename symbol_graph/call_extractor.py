import ast


class CallExtractor(ast.NodeVisitor):
    def __init__(self):
        self.calls = []
        self.current_symbol = None

    def visit_FunctionDef(self, node):
        self.current_symbol = node.name
        self.generic_visit(node)
        self.current_symbol = None

    def visit_Call(self, node):
        if not self.current_symbol:
            return

        if isinstance(node.func, ast.Name):
            self.calls.append((self.current_symbol, node.func.id))

        elif isinstance(node.func, ast.Attribute):
            self.calls.append((self.current_symbol, node.func.attr))

        self.generic_visit(node)
