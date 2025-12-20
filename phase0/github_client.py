from github import Github
from config import GITHUB_TOKEN

class GitHubClient:
    def __init__(self):
        if not GITHUB_TOKEN:
            raise ValueError("Github token not found")
        self.client = Github(GITHUB_TOKEN)
    def get_repo(self, repo_url:str):
        """
        repo_url: https://github.com/owner/repo
        """
        path = repo_url.replace("https://github.com/","")
        return self.client.get_repo(path)
    def get_commits(self,repo):
        return [
            {
                "sha": c.sha,
                "author": c.commit.author.name if c.commit.author else None,
                "date": c.commit.author.date.isoformat(),
                "message": c.commit.message

            }
            for c in repo.get_commits()
        ]
    def get_issues(self,repo):
        return [
            {
                "id": i.id,
                "number": i.number,
                "title": i.title,
                "state": i.state,
                "created_at": i.created_at.isoformat(),
                "closed_at": i.closed_at.isoformat() if i.closed_at else None,
                "labels": [l.name for l in i.labels]
            }
            for i in repo.get_issues(state="all")
        ]
    def get_pull_requests(self,repo):
        return [
            {
                "id": pr.id,
                "number": pr.number,
                "title": pr.title,
                "state": pr.state,
                "created_at": pr.created_at.isoformat(),
                "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
                "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
            }
            for pr in repo.get_pulls(state="all")
        ]
    def get_branches(self,repo):
        return [b.name for b in repo.get_branches()]
    def get_tags(self,repo):
        return [t.name for t in repo.get_tags()]