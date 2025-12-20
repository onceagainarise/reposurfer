class MetadataExtractor:
    def extract(self, repo):
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "open_issues": repo.open_issues_count,
            "default_branch": repo.default_branch,
            "language": repo.language,
            "updated_at": repo.updated_at.isoformat()
        }
