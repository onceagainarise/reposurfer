import argparse
import sys
from pathlib import Path
from reposurfer.app.reposurfer_app import RepoSurferApp
from reposurfer.core.reasoning.phase3_runner import run_interactive_mode

def main():
    parser = argparse.ArgumentParser(
        "RepoSurfer",
        description="AI-powered codebase understanding and exploration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  reposurfer index https://github.com/psf/requests
  reposurfer chat requests "Unable to override cookie policy"
  reposurfer interactive requests
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Index command
    index_parser = subparsers.add_parser("index", help="Index a GitHub repository")
    index_parser.add_argument("repo_url", help="GitHub repository URL")
    
    # Chat command (simplified query)
    chat_parser = subparsers.add_parser("chat", help="Ask a question about a repository")
    chat_parser.add_argument("repo_name", help="Repository name (e.g., 'requests')")
    chat_parser.add_argument("query", nargs="+", help="Your question or issue description")
    chat_parser.add_argument("--mode", choices=["investigate", "qa"], default="auto", 
                           help="Analysis mode (default: auto-detect)")
    
    # Interactive command
    interactive_parser = subparsers.add_parser("interactive", help="Start interactive Q&A session")
    interactive_parser.add_argument("repo_name", help="Repository name (e.g., 'requests')")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all indexed repositories")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    app = RepoSurferApp()
    
    if args.command == "index":
        print(f"🔄 Indexing repository: {args.repo_url}")
        app.index_repo(args.repo_url)
    
    elif args.command == "chat":
        # Find repository path
        repo_path = find_repo_path(args.repo_name)
        if not repo_path:
            print(f"❌ Repository '{args.repo_name}' not found. Available repositories:")
            list_repositories()
            sys.exit(1)
        
        query = " ".join(args.query)
        print(f"🤖 Processing: {query}")
        
        from reposurfer.core.reasoning.phase3_runner import run_phase3
        mode = args.mode if args.mode != "auto" else None
        run_phase3(repo_path, query, mode=mode)
    
    elif args.command == "interactive":
        repo_path = find_repo_path(args.repo_name)
        if not repo_path:
            print(f"❌ Repository '{args.repo_name}' not found. Available repositories:")
            list_repositories()
            sys.exit(1)
        
        run_interactive_mode(repo_path)
    
    elif args.command == "list":
        list_repositories()

def find_repo_path(repo_name: str) -> str:
    """Find repository path by name with better matching"""
    storage_root = Path("storage/repos")
    
    # Try exact match first
    exact_path = storage_root / repo_name
    if exact_path.exists():
        return str(exact_path)
    
    # Try pattern matching (owner__repo format)
    for path in storage_root.iterdir():
        if path.is_dir():
            # Check if repo_name matches any part of the directory name
            dir_name = path.name.lower()
            search_name = repo_name.lower()
            
            # Handle various separators
            normalized_dir = dir_name.replace("__", "/").replace("_", "/").replace("-", "/")
            normalized_search = search_name.replace("__", "/").replace("_", "/").replace("-", "/")
            
            # Check if search name is contained in dir name or vice versa
            if (search_name in dir_name.lower() or 
                dir_name.lower() in search_name or
                normalized_search in normalized_dir or
                normalized_dir in normalized_search):
                return str(path)
    
    return None

def list_repositories():
    """List all indexed repositories"""
    storage_root = Path("storage/repos")
    if not storage_root.exists():
        print("📁 No repositories found. Use 'reposurfer index <url>' to add repositories.")
        return
    
    repos = [p for p in storage_root.iterdir() if p.is_dir()]
    if not repos:
        print("📁 No repositories found. Use 'reposurfer index <url>' to add repositories.")
        return
    
    print("📚 Indexed repositories:")
    for repo in repos:
        print(f"  • {repo.name}")

if __name__ == "__main__":
    main()
