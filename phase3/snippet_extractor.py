class SnippetExtractor:
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
    
    def extract(self, file_path: str, max_lines: int = 40):
        abs_path = f"{self.repo_root}/source/{file_path}"

        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception :
            return ""
        
        return "".join(lines[:max_lines])
    