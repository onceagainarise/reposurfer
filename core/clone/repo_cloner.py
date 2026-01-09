import os 
from git import Repo
from tqdm import tqdm
from reposurfer.config import BASE_STORAGE_PATH

class RepoCloner:
    def __init__(self,base_path=BASE_STORAGE_PATH):
        self.base_path = base_path
    
    def _repo_dir_name(self,repo_url: str) -> str:
        """
        https://github.com/owner/repo -> owner_repo
        """
        path = repo_url.replace("https://github.com/", "")
        owner, repo = path.split("/")
        return f"{owner}_{repo}"
    
    def clone_repo(self, repo_url: str, target_path: str) -> str:

        """
        Clones repo if not already present.
        Returns local path to repo source.
        """
        repo_dir = self._repo_dir_name(repo_url)
        repo_base_path = os.path.join(self.base_path, repo_dir)
        source_path = os.path.join(target_path, "source")

        if os.path.exists(source_path):
            print(f"[RepoCloner] Repo already cloned: {source_path}")
            return source_path

        os.makedirs(repo_base_path, exist_ok=True)

        print(f"[RepoCloner] Cloning {repo_url} into {source_path}")
        
        # Clone with progress tracking
        try:
            # GitPython doesn't have built-in progress, so we'll show a simple progress
            with tqdm(total=100, desc="Cloning repository", unit="%") as pbar:
                pbar.set_description(f"Cloning {repo_dir}")
                
                # Update progress at key stages
                pbar.update(10)  # Starting
                
                Repo.clone_from(repo_url, source_path)
                
                pbar.update(80)  # Almost done
                pbar.set_postfix({"status": "finalizing"})
                pbar.update(10)  # Complete
                
                pbar.set_postfix({"status": "completed"})
                
        except Exception as e:
            print(f"[RepoCloner] Clone failed: {e}")
            raise

        print(f"[RepoCloner] Clone completed: {source_path}")
        return source_path
