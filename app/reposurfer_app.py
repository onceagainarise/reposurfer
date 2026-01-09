from pathlib import Path
from tqdm import tqdm
from reposurfer.core.clone.phase0_runner import run_phase0
from reposurfer.core.symbol_graph.phase1_runner import run_phase1
from reposurfer.core.symbol_graph.phase1_graph_runner import run_phase1_7
from reposurfer.core.embeddings.phase2_runner import run_phase2
from reposurfer.core.embeddings.phase2_embed_runner import run_embedding
from reposurfer.core.reasoning.phase3_runner import run_phase3

class RepoSurferApp:
    def __init__(self, storage_root: str = "storage/repos"):
        self.storage_root = Path(storage_root)

    def index_repo(self, repo_url: str):
        """
        Full indexing pipeline (Phase 0 → Phase 2.3) with progress tracking
        """
        print("🚀 Starting repository indexing...")
        
        # Progress tracking
        phases = [
            ("📥 Phase 0: Cloning repository...", "Cloning and fetching metadata"),
            ("🔍 Phase 1: Analyzing code structure...", "Parsing Python files and extracting symbols"),
            ("🔗 Phase 1.7: Building symbol graph...", "Creating symbol relationships"),
            ("🧠 Phase 2: Building semantic index...", "Creating symbol chunks"),
            ("⚡ Phase 2.3: Generating embeddings...", "Vectorizing symbols and storing in database")
        ]
        
        with tqdm(phases, desc="RepoSurfer Progress", unit="phase") as pbar:
            # Phase 0: Clone and fetch metadata
            pbar.set_description(phases[0][0])
            run_phase0(repo_url)
            pbar.update(1)

            owner, name = repo_url.rstrip("/").split("/")[-2:]
            repo_dir = self.storage_root / f"{owner}__{name}"

            # Phase 1: Static analysis
            pbar.set_description(phases[1][0])
            run_phase1(str(repo_dir))
            pbar.update(1)
            
            # Phase 1.7: Graph building
            pbar.set_description(phases[2][0])
            run_phase1_7(str(repo_dir))
            pbar.update(1)

            # Phase 2: Semantic processing
            pbar.set_description(phases[3][0])
            run_phase2(str(repo_dir))
            pbar.update(1)
            
            # Phase 2.3: Embeddings
            pbar.set_description(phases[4][0])
            run_embedding(str(repo_dir))
            pbar.update(1)

        print(f"\n✅ Repository '{owner}/{name}' indexed successfully!")
        print(f"📍 Stored at: {repo_dir}")
        print("\nYou can now:")
        print(f"  • reposurfer chat {name} \"your question\"")
        print(f"  • reposurfer interactive {name}")

    def query(self, repo_path: str, issue: str, mode: str = "auto"):
        """
        Enhanced query with multiple modes
        """
        run_phase3(repo_path, issue, mode)
    
    def interactive(self, repo_path: str):
        """
        Start interactive session
        """
        from reposurfer.core.reasoning.phase3_runner import run_interactive_mode
        run_interactive_mode(repo_path)
    
    def list_repositories(self):
        """List all indexed repositories"""
        if not self.storage_root.exists():
            print("📁 No repositories found. Use 'index_repo' to add repositories.")
            return
        
        repos = [p for p in self.storage_root.iterdir() if p.is_dir()]
        if not repos:
            print("📁 No repositories found. Use 'index_repo' to add repositories.")
            return
        
        print("📚 Indexed repositories:")
        for repo in repos:
            print(f"  • {repo.name}")
    
    def get_repo_path(self, repo_name: str) -> str:
        """Get repository path by name"""
        # Try exact match
        exact_path = self.storage_root / repo_name
        if exact_path.exists():
            return str(exact_path)
        
        # Try pattern matching
        for path in self.storage_root.iterdir():
            if path.is_dir() and repo_name.lower() in path.name.lower():
                return str(path)
        
        return None
