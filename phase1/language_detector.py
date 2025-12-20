def is_python_file(file_entry: dict) -> bool:
    """Decide whether a tree.json entry represents a python source file."""
    return file_entry.get("path","").endswith(".py")