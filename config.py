import os

# GitHub Configuration
GITHUB_ORGS = os.getenv('GITHUB_ORGS', '').split(',')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
GITHUB_API_URL = 'https://api.github.com'

# GitLab Configuration
GITLAB_PROJECTS = os.getenv('GITLAB_PROJECTS', '').split(',')
GITLAB_TOKEN = os.getenv('GITLAB_TOKEN', '')
GITLAB_API_URL = 'https://gitlab.com/api/v4'

# Cloning Configuration
CLONE_METHOD = os.getenv('CLONE_METHOD', 'ssh')  # 'ssh' or 'http'
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '3600'))  # in seconds
SYNC_ENABLED = os.getenv('SYNC_ENABLED', 'true').lower() == 'true'

# Logging Configuration
LOG_DIR = os.getenv('LOG_DIR', '/logs')
