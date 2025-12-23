import os

IGNORE_DIRS={
    ".git",
    "node_modules",
    ".venv",
    "__pycache__",
    "dist",
    "build"   
}

EXTENSION_LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".go": "go",
    ".rs": "rust",
    ".md": "markdown"
}

class FileTreeBuilder:
    def build_tree(self,repo_source_path: str):
        tree=[]
        for root, dirs, files in os.walk(repo_source_path):
            dirs[:]= [d for d in dirs if d not in IGNORE_DIRS]
            
            for name in files:
                full_path = os.path.join(root,name)
                rel_path = os.path.relpath(full_path,repo_source_path)
                ext= os.path.splitext(name)[1]
                language= EXTENSION_LANGUAGE_MAP.get(ext,"unknown")

                tree.append({
                    "path": rel_path.replace("\\", "/"),
                    "type": "file",
                    "extension": ext,
                    "language": language,
                    "size_bytes": os.path.getsize(full_path)
                })
        return tree
    
