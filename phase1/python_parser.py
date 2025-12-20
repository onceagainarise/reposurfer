import ast

class PythonASTParser:
    def parse(self, file_path: str,content: str):
        """Parse python source code into an AST.
           Returns None if parsing fails"""
        try:
            return ast.parse(content)
        except SyntaxError as e:
            print(f"[Phase1][AST] SynataxError in {file_path}:{e}")
            return None
        except Exception as e:
            print(f"[Phase][AST] Failed to parse {file_path}:{e}")
            return None