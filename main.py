import os
import time
import threading
import logging
from config import (
    GITHUB_ORGS, GITLAB_PROJECTS, CHECK_INTERVAL, SYNC_ENABLED
)
from github_manager import GitHubManager
from gitlab_manager import GitLabManager
from repo_cloner import RepoCloner

def clone_github_repos():
    github_manager = GitHubManager(GITHUB_ORGS)
    repos = github_manager.get_repositories()
    cloner = RepoCloner()
    for repo in repos:
        base_dir = os.path.join('github_repos', repo['organization'])
        os.makedirs(base_dir, exist_ok=True)
        cloner.clone_or_update_repo(repo, base_dir)

def clone_gitlab_repos():
    gitlab_manager = GitLabManager(GITLAB_PROJECTS)
    repos = gitlab_manager.get_repositories()
    cloner = RepoCloner()
    for repo in repos:
        base_dir = 'gitlab_repos'
        cloner.clone_gitlab_repo(repo, base_dir)

def periodic_task():
    while SYNC_ENABLED:
        logging.info("Starting periodic sync.")
        clone_github_repos()
        clone_gitlab_repos()
        logging.info("Periodic sync completed.")
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    logging.info("Starting the repository synchronization tool.")
    clone_github_repos()
    clone_gitlab_repos()
    if SYNC_ENABLED:
        threading.Thread(target=periodic_task).start()
