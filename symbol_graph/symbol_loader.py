import json
from typing import List, Dict

def load_symbols(path: str)-> List[Dict]:
    with open(path, "r") as f:
        return json.load(f)

