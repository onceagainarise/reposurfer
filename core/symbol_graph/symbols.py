from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Symbol:
    symbol_id: str
    name: str
    type: str              # function | class | method
    file: str
    start_line: int
    end_line: int
    parent: Optional[str]
    docstring: Optional[str]
    imports: List[str]

