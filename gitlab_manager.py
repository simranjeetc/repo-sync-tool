import requests
import re
from logger import log_info, log_error, log_debug, log_warning, log_critical, log_exception
from config import GITLAB_TOKEN, GITLAB_API_URL

class GitLabManager:
    def __init__(self, projects):
        self.allowed_projects = [project.strip() for project in projects if project.strip()]
        self.headers = {'PRIVATE-TOKEN': GITLAB_TOKEN}

    def get_repositories(self):
        repos = []
        url = f"{GITLAB_API_URL}/projects"
        params = {
            'pagination': 'keyset',
            'per_page': 100,
            'order_by': 'id',
            'sort': 'asc',
            'include_subgroups': True
        }

        while True:
            try:
                # Send the request. Use params only for the first request, then use 'url' directly if it's updated.
                response = requests.get(url, headers=self.headers, params=params if 'params' in locals() else None,
                                        timeout=40, verify=False)
                if response.status_code != 200:
                    log_error(f"Failed to fetch repos for gitlab projects: {response.status_code}")
                    break

                # Parse the response data
                data = response.json()
                if not data:
                    break

                # Process the repositories
                for repo in data:
                    if not repo['archived']:
                        if any(repo['path_with_namespace'].startswith(allowed_project) for allowed_project in
                               self.allowed_projects):
                            repos.append({
                                'name': repo['name'],
                                'ssh_url_to_repo': repo['ssh_url_to_repo'],
                                'http_url_to_repo': repo['http_url_to_repo'],
                                'default_branch': repo['default_branch'],
                                'name_with_namespace': repo['name_with_namespace'],
                                'path_with_namespace': repo['path_with_namespace']
                            })
                        else:
                            log_info(
                                f"Skipping repository {repo['path_with_namespace']} as it does not fall under the allowed projects.")

                # Extract the next page URL from the 'Link' header
                link_header = response.headers.get('Link', None)
                if link_header and 'rel="next"' in link_header:
                    url = self.extract_next_page_url(link_header)
                    if not url:
                        log_error("Failed to extract the next page URL, stopping pagination.")
                        break

                    # From this point on, don't use 'params' anymore
                    params = None
                else:
                    break

            except requests.exceptions.Timeout:
                log_error(f"Request timed out while fetching repositories for gitlab projects")
                break

            except requests.exceptions.SSLError as ssl_error:
                log_error(f"SSL error occurred while fetching repositories for gitlab project: {ssl_error}")
                break

            except requests.exceptions.RequestException as e:
                log_exception(f"An error occurred while fetching repositories for gitlab project: {e}")
                break

        return repos

    def extract_next_page_url(self, link_header):
        """
        Extracts the URL for the next page from the 'Link' header.
        """
        try:
            # The 'Link' header contains URLs with rel="next", rel="prev", etc.
            match = re.search(r'<([^>]+)>;\s*rel="next"', link_header)
            if match:
                return match.group(1)  # Return the next page URL
            else:
                log_error("Next page URL not found in Link header.")
                return None
        except Exception as e:
            log_error(f"Failed to extract next page URL from Link header: {e}")
            return None

