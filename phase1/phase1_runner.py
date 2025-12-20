# this is a temporary file to test
import os
import json

from phase1.language_detector import is_python_file
from phase1.python_parser import PythonASTParser

def run_phase1(repo_path:str):
    tree_file  = os.path.join(repo_path,"tree.json")
    source_root = os.path.join(repo_path,"source")

    if not os.path.exists(tree_file):
        raise FileNotFoundError("tree.json not found")
    
    with open(tree_file,"r") as f:
        tree = json.load(f)
    
    parser = PythonASTParser()
    parsed_count = 0
    failed_count = 0

    for entry in tree:
        if not is_python_file(entry):
            continue
        
        file_path = os.path.join(source_root, entry["path"])

        if not os.path.exists(file_path):
            print(f"[Phase1][Runner] File not found: {file_path}")
            continue

        try:
            with open(file_path, "r", encoding = "utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"[Phase1][Runner] Failed to read {file_path}: {e}")
            failed_count+=1
            continue

        ast_tree = parser.parse(entry["path"], content)
        if ast_tree is None:
            failed_count+=1
            continue
        
        parsed_count+=1
    print(f"[Phase1] Parsed files: {parsed_count}")
    print(f"[Phase1] Failed files: {failed_count}")


if __name__ == "__main__":

    REPO_PATH = "storage/repos/owner_repo"
    run_phase1(REPO_PATH)