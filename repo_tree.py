import os
import argparse

EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".reposurfer",
    ".idea",
    ".vscode"
}

EXCLUDE_FILES = {
    ".DS_Store"
}


def build_tree(root, prefix="", show_size=False):
    entries = sorted(os.listdir(root))
    entries = [
        e for e in entries
        if e not in EXCLUDE_DIRS and e not in EXCLUDE_FILES
    ]

    for index, entry in enumerate(entries):
        path = os.path.join(root, entry)
        connector = "└── " if index == len(entries) - 1 else "├── "

        if os.path.isdir(path):
            print(prefix + connector + entry + "/")
            new_prefix = prefix + ("    " if index == len(entries) - 1 else "│   ")
            build_tree(path, new_prefix, show_size)
        else:
            size = ""
            if show_size:
                size = f" ({os.path.getsize(path)} bytes)"
            print(prefix + connector + entry + size)


def main():
    parser = argparse.ArgumentParser(description="Generate repo tree structure")
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root directory of the repository"
    )
    parser.add_argument(
        "--size",
        action="store_true",
        help="Show file sizes"
    )
    parser.add_argument(
        "--out",
        help="Write output to a file"
    )

    args = parser.parse_args()

    if args.out:
        with open(args.out, "w") as f:
            import sys
            original_stdout = sys.stdout
            sys.stdout = f
            print(os.path.abspath(args.path))
            build_tree(args.path, show_size=args.size)
            sys.stdout = original_stdout
    else:
        print(os.path.abspath(args.path))
        build_tree(args.path, show_size=args.size)


if __name__ == "__main__":
    main()
