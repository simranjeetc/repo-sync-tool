import os
import shutil
import subprocess
from logger import log_info, log_error, log_debug, log_warning, log_critical, log_exception
from git import Repo, InvalidGitRepositoryError, GitCommandError
from config import (CLONE_METHOD, GIT_DEPTH)


class RepoCloner:
    def __init__(self):
        pass

    def clone_or_update_repo(self, repo_info, base_dir):
        repo_name = repo_info['name']
        clone_url = repo_info.get('ssh_url') if CLONE_METHOD == 'ssh' else repo_info.get('clone_url')
        repo_dir = os.path.join(base_dir, repo_name)
        if not os.path.exists(repo_dir):
            try:
                self.git_clone(clone_url, repo_dir, repo_info, repo_name)
            except GitCommandError as e:
                log_info(f"Failed to clone {repo_name}: {e}")
                if os.path.exists(repo_dir):
                    os.rmdir(repo_dir)
        else:
            try:
                self.get_fetch_and_reset(repo_dir, repo_info)
                log_info(f"Updated repository {repo_name}")
            except InvalidGitRepositoryError:
                log_warning(f"Invalid repository at {repo_dir}, recloning.")
                os.rmdir(repo_dir)
                self.clone_or_update_repo(repo_info, base_dir)
            except Exception as e:
                log_error(f"Failed to update {repo_name}: {e}")
                self.handle_repo_failure(repo_info, base_dir, repo_dir)

    def get_fetch_and_reset(self, repo_dir, repo_info):
        repo = Repo(repo_dir)
        origin = repo.remotes.origin
        origin.fetch(depth=GIT_DEPTH)  # Fetch with depth if provided
        default_branch = repo_info['default_branch']
        repo.git.reset('--hard', f'origin/{default_branch}')

    def git_clone(self, clone_url, repo_dir, repo_info, repo_name):
        if GIT_DEPTH:
            log_info(f"Cloning repository {repo_name} with depth of {GIT_DEPTH}")
            Repo.clone_from(
                clone_url, repo_dir, branch=repo_info['default_branch'], single_branch=True, depth=GIT_DEPTH)
        else:
            log_info(f"Cloning repository {repo_name}")
            Repo.clone_from(clone_url, repo_dir, branch=repo_info['default_branch'], single_branch=True)

    def handle_repo_failure(self, repo_info, base_dir, repo_dir):
        # Deletes the repo and reclones in case of failure
        print(f"Removing faulty repository: {repo_dir}")
        try:
            shutil.rmtree(repo_dir)
            # Reclone after deleting the faulty repo
            self.clone_or_update_repo(repo_info, base_dir)
        except Exception as e:
            print(f"Failed to repair repository: {repo_dir}, error: {e}")

    def clone_gitlab_repo(self, repo_info, base_dir):
        # Extract the namespace path from the repository info
        repo_namespace_path = repo_info['path_with_namespace']

        # Proceed with cloning
        path_parts = repo_namespace_path.split('/')
        repo_name = path_parts[-1]
        repo_path = os.path.join(base_dir, *path_parts[1:-1], repo_name)
        clone_url = repo_info['ssh_url_to_repo'] if CLONE_METHOD == 'ssh' else repo_info['http_url_to_repo']

        if not os.path.exists(repo_path):
            os.makedirs(os.path.dirname(repo_path), exist_ok=True)
            try:
                self.git_clone(clone_url, repo_path, repo_info, repo_name)
            except GitCommandError as e:
                log_error(f"Failed to clone {repo_name}: {e}")
                if os.path.exists(repo_path):
                    os.rmdir(repo_path)
        else:
            try:
                self.get_fetch_and_reset(repo_path, repo_info)
                log_info(f"Updated GitLab repository {repo_name}")
            except InvalidGitRepositoryError:
                log_warning(f"Invalid repository at {repo_path}, recloning.")
                os.rmdir(repo_path)
                self.clone_gitlab_repo(repo_info, base_dir)
            except Exception as e:
                log_error(f"Failed to update {repo_name}: {e}")
                self.handle_repo_failure(repo_info, base_dir, repo_path)
