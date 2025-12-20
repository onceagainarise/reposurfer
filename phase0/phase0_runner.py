import os
from phase0.github_client import GitHubClient
from phase0.repo_cloner import RepoCloner
from phase0.tree_builder import FileTreeBuilder
from phase0.metadata_extractor import MetadataExtractor
from phase0.utils import save_json
from config import BASE_STORAGE_PATH


def run_phase0(repo_url: str):
    print(f"[Phase0] Processing {repo_url}")

    client = GitHubClient()
    cloner = RepoCloner()
    tree_builder = FileTreeBuilder()
    metadata_extractor = MetadataExtractor()

    repo = client.get_repo(repo_url)

    owner, name = repo.full_name.split("/")
    repo_dir = f"{owner}__{name}"
    base_path = os.path.join(BASE_STORAGE_PATH, repo_dir)

    # --- GitHub data ---
    save_json(f"{base_path}/metadata.json",
              metadata_extractor.extract(repo))

    save_json(f"{base_path}/commits.json",
              client.get_commits(repo))

    save_json(f"{base_path}/issues.json",
              client.get_issues(repo))

    save_json(f"{base_path}/pull_requests.json",
              client.get_pull_requests(repo))

    save_json(f"{base_path}/branches.json",
              client.get_branches(repo))

    save_json(f"{base_path}/tags.json",
              client.get_tags(repo))

    # --- Clone + tree ---
    source_path = cloner.clone_repo(repo_url)
    tree = tree_builder.build_tree(source_path)

    save_json(f"{base_path}/tree.json", tree)

    print("[Phase0] Completed successfully")


if __name__ == "__main__":
    run_phase0("https://github.com/psf/requests")
