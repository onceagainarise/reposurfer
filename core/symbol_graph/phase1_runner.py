# this is a temporary file to test
import os
import json
from tqdm import tqdm

from reposurfer.core.clone.utils import save_json
from reposurfer.core.symbol_graph.language_detector import is_python_file
from reposurfer.core.symbol_graph.python_parser import PythonASTParser
from reposurfer.core.symbol_graph.python_symbol_extractor import PythonSymbolExtractor


def run_phase1(repo_path:str):
    tree_file  = os.path.join(repo_path,"tree.json")
    source_root = os.path.join(repo_path,"source")

    if not os.path.exists(tree_file):
        raise FileNotFoundError("tree.json not found")
    
    with open(tree_file,"r") as f:
        tree = json.load(f)
    
    # Filter Python files
    python_files = [entry for entry in tree if is_python_file(entry)]
    print(f"[Phase1] Found {len(python_files)} Python files to analyze")
    
    parser = PythonASTParser()
    parsed_count = 0
    failed_count = 0
    all_symbols = []
    
    # Progress bar for file processing
    with tqdm(python_files, desc="Parsing Python files", unit="file") as pbar:
        for entry in pbar:
            file_path = os.path.join(source_root, entry["path"])

            if not os.path.exists(file_path):
                pbar.set_postfix({"status": "not found"})
                continue

            try:
                with open(file_path, "r", encoding = "utf-8") as f:
                    content = f.read()
            except Exception as e:
                pbar.set_postfix({"status": "read error"})
                failed_count+=1
                continue

            ast_tree = parser.parse(entry["path"], content)
            if ast_tree is None:
                pbar.set_postfix({"status": "parse error"})
                failed_count+=1
                continue
            
            extractor = PythonSymbolExtractor(entry["path"])
            extractor.visit(ast_tree)
            
            for s in extractor.symbols:
                s["imports"] = extractor.imports
                all_symbols.append(s)

            parsed_count+=1
            pbar.set_postfix({"status": "success", "symbols": len(all_symbols)})
    
    save_json(os.path.join(repo_path, "symbols.json"), all_symbols)

    print(f"[Phase1] ✅ Parsed files: {parsed_count}")
    print(f"[Phase1] ❌ Failed files: {failed_count}")
    print(f"[Phase1] 📊 Total symbols extracted: {len(all_symbols)}")


if __name__ == "__main__":

    REPO_PATH = "storage/repos/psf__requests"
    run_phase1(REPO_PATH)