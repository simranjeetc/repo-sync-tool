import requests
from logger import log_info, log_error, log_debug, log_warning, log_critical, log_exception
from urllib.parse import quote
from config import GITLAB_TOKEN, GITLAB_API_URL

class GitLabManager:
    def __init__(self, projects):
        self.projects = [proj.strip() for proj in projects if proj.strip()]
        self.headers = {'PRIVATE-TOKEN': GITLAB_TOKEN}

    def get_repositories(self):
        repos = []
        for project in self.projects:
            encoded_project = quote(project, safe='')
            page = 1
            while True:
                url = f"{GITLAB_API_URL}/groups/{encoded_project}/projects"
                params = {'per_page': 100, 'page': page, 'include_subgroups': True}
                response = requests.get(url, headers=self.headers, params=params)
                if response.status_code != 200:
                    log_error(f"Failed to fetch repos for project {project}: {response.status_code}")
                    break
                data = response.json()
                if not data:
                    break
                for repo in data:
                    if not repo['archived']:
                        repos.append({
                            'name': repo['name'],
                            'ssh_url_to_repo': repo['ssh_url_to_repo'],
                            'http_url_to_repo': repo['http_url_to_repo'],
                            'default_branch': repo['default_branch'],
                            'name_with_namespace': repo['name_with_namespace']
                        })
                page += 1
        return repos
