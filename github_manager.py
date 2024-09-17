import requests
from logger import log_info, log_error, log_debug, log_warning, log_critical, log_exception
from config import GITHUB_TOKEN, GITHUB_API_URL

class GitHubManager:
    def __init__(self, organizations):
        self.organizations = [org.strip() for org in organizations if org.strip()]
        self.headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def get_repositories(self):
        repos = []
        for org in self.organizations:
            page = 1
            while True:
                url = f"{GITHUB_API_URL}/orgs/{org}/repos"
                params = {'per_page': 100, 'page': page}
                response = requests.get(url, headers=self.headers, params=params)
                if response.status_code != 200:
                    log_error(f"Failed to fetch repos for org {org}: {response.status_code}")
                    break
                data = response.json()
                if not data:
                    break
                for repo in data:
                    if not repo['archived']:
                        repos.append({
                            'name': repo['name'],
                            'ssh_url': repo['ssh_url'],
                            'clone_url': repo['clone_url'],
                            'default_branch': repo['default_branch'],
                            'organization': org.lower()
                        })
                page += 1
        return repos
