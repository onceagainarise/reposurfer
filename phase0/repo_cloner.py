import os 
from git import Repo
from config import BASE_STORAGE_PATH

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
    
    def clone_repo(self, repo_url: str) -> str:
        """
        Clones the repo if not already present.
        Returns local path to repo source.
        """
        repo_dir = self._repo_dir_name(repo_url)
        repo_base_path = os.path.join(self.base_path, repo_dir)
        source_path = os.path.join(repo_base_path, "source")

        if os.path.exists(source_path):
            print(f"[RepoCloner] Repo already cloned: {source_path}")
            return source_path

        os.makedirs(repo_base_path, exist_ok=True)

        print(f"[RepoCloner] Cloning {repo_url} into {source_path}")
        Repo.clone_from(repo_url, source_path)

        return source_path
    

    
    

