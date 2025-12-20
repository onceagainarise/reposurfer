from phase1.language_detector import is_python_file

print(is_python_file({"path": "src/main.py"}))    # True
print(is_python_file({"path": "README.md"}))     # False
