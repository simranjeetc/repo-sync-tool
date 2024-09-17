import os
import subprocess
import logging
from git import Repo, InvalidGitRepositoryError, GitCommandError
from config import CLONE_METHOD

class RepoCloner:
    def __init__(self):
        pass

    def clone_or_update_repo(self, repo_info, base_dir):
        repo_name = repo_info['name']
        clone_url = repo_info.get('ssh_url') if CLONE_METHOD == 'ssh' else repo_info.get('clone_url')
        repo_dir = os.path.join(base_dir, repo_name)
        if not os.path.exists(repo_dir):
            try:
                logging.info(f"Cloning repository {repo_name}")
                Repo.clone_from(clone_url, repo_dir, branch=repo_info['default_branch'], single_branch=True)
            except GitCommandError as e:
                logging.error(f"Failed to clone {repo_name}: {e}")
                if os.path.exists(repo_dir):
                    os.rmdir(repo_dir)
        else:
            try:
                repo = Repo(repo_dir)
                origin = repo.remotes.origin
                origin.pull()
                logging.info(f"Updated repository {repo_name}")
            except InvalidGitRepositoryError:
                logging.warning(f"Invalid repository at {repo_dir}, recloning.")
                os.rmdir(repo_dir)
                self.clone_or_update_repo(repo_info, base_dir)
            except GitCommandError as e:
                logging.error(f"Failed to update {repo_name}: {e}")

    def clone_gitlab_repo(self, repo_info, base_dir):
        path_parts = repo_info['name_with_namespace'].split(' / ')
        repo_name = path_parts[-1]
        repo_path = os.path.join(base_dir, *path_parts[1:-1], repo_name)
        clone_url = repo_info['ssh_url_to_repo'] if CLONE_METHOD == 'ssh' else repo_info['http_url_to_repo']
        if not os.path.exists(repo_path):
            os.makedirs(os.path.dirname(repo_path), exist_ok=True)
            try:
                logging.info(f"Cloning GitLab repository {repo_name}")
                Repo.clone_from(clone_url, repo_path, branch=repo_info['default_branch'], single_branch=True)
            except GitCommandError as e:
                logging.error(f"Failed to clone {repo_name}: {e}")
                if os.path.exists(repo_path):
                    os.rmdir(repo_path)
        else:
            try:
                repo = Repo(repo_path)
                origin = repo.remotes.origin
                origin.pull()
                logging.info(f"Updated GitLab repository {repo_name}")
            except InvalidGitRepositoryError:
                logging.warning(f"Invalid repository at {repo_path}, recloning.")
                os.rmdir(repo_path)
                self.clone_gitlab_repo(repo_info, base_dir)
            except GitCommandError as e:
                logging.error(f"Failed to update {repo_name}: {e}")
