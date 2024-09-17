# Repository Synchronization Tool

This tool automates the cloning and synchronization of repositories from specified GitHub organizations and GitLab projects. It periodically checks for updates, new repositories, and handles synchronization tasks efficiently.

## Features

- **Clone Repositories**: Clones all repositories from specified GitHub organizations and GitLab projects.
- **Periodic Sync**: Periodically checks for updates and synchronizes repositories.
- **Self-Repairing**: Automatically detects and fixes corrupted repositories without manual intervention.
- **Configurable Cloning Method**: Supports both SSH and HTTP cloning methods.
- **Customizable Logging**: Logs are stored in a specified directory, omitting sensitive information.
- **Flexible Configuration**: All settings are configurable via environment variables.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [Setting Environment Variables](#setting-environment-variables)
- [Usage](#usage)
  - [Running the Docker Container](#running-the-docker-container)
- [Logging](#logging)
- [SSH Keys](#ssh-keys)
  - [SSH Cloning](#ssh-cloning)
- [Notes](#notes)
- [License](#license)

## Prerequisites

- **Docker**: Ensure Docker is installed on your system.
- **GitHub Access Token**: Required for accessing GitHub APIs.
- **GitLab Access Token**: Required for accessing GitLab APIs.
- **SSH Keys**: Necessary if using the SSH cloning method.

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/repo-sync-tool.git
cd repo-sync-tool
```

### Build the Docker Image

```bash
docker build -t repo-sync-tool .
```

## Configuration

All configurations are managed via environment variables.

### Environment Variables

- `GITHUB_ORGS`: Comma-separated list of GitHub organizations.

  Example: `"FileAnalysisSuite,CAFDataProcessing"`

- `GITHUB_TOKEN`: GitHub access token.
- `GITLAB_PROJECTS`: Comma-separated list of GitLab projects.

  Example: `"CyberSecurity Enterprise / Structured Data Manager,CyberSecurity Enterprise / Core Data Discovery and Risk Insights"`

- `GITLAB_TOKEN`: GitLab access token.
- `CLONE_METHOD`: Cloning method, `"ssh"` or `"http"`. Default is `"ssh"`.
- `CHECK_INTERVAL`: Interval for periodic checks in seconds. Default is `3600` (1 hour).
- `SYNC_ENABLED`: Enable or disable periodic sync. `"true"` or `"false"`. Default is `"true"`.
- `LOG_DIR`: Directory to store logs inside the container. Default is `/app/logs`.

### Setting Environment Variables

You can set environment variables by:

- Using the `-e` flag in the `docker run` command.
- Providing an `.env` file and using the `--env-file` flag.

## Usage

### Running the Docker Container

```bash
docker run -d \
  -v /path/to/ssh/keys:/tmp/ssh_keys_mount:ro  \
  -v /path/to/logs:/app/logs \
  -v /path/to/github_repos:/app/github_repos \
  -v /path/to/gitlab_repos:/app/gitlab_repos \
  -e GITHUB_ORGS="CAFApi,CAFDataProcessing" \
  -e GITHUB_TOKEN="your_github_access_token" \
  -e GITLAB_PROJECTS="Enterprise/project1,Enterprise/project2``" \
  -e GITLAB_TOKEN="your_gitlab_access_token" \
  -e CLONE_METHOD="ssh" \
  -e CHECK_INTERVAL="3600" \
  -e SYNC_ENABLED="true" \
  repo-sync-tool
```

**Notes:**

- Ensure that the SSH keys have the correct permissions (`chmod 600`).
- Replace placeholders with your actual paths and tokens.
- Mount directories for logs and cloned repositories to access them outside the container.

## Logging

Logs are stored in the directory specified by `LOG_DIR`.

- To access logs outside the container, mount the log directory using `-v /path/to/logs:/app/logs`.
- The tool ensures that no sensitive information (like tokens or passwords) is logged.

## SSH Keys

### SSH Cloning

If `CLONE_METHOD` is set to `"ssh"`, you need to provide SSH keys.

- **Mount SSH Keys**: Mount your SSH keys directory into the container at `/root/.ssh`.

  ```bash
  -v /path/to/ssh/keys:/root/.ssh
  ```

- **Permissions**: Set the correct permissions for your SSH keys (`chmod 600`).

## Notes

- **Cloning Repositories**: Repositories are cloned into `/app/github_repos` and `/app/gitlab_repos` inside the container.
- **Self-Repairing Mechanism**: The tool automatically reclones repositories if corruption is detected.
- **Archived Repositories**: The tool does not clone archived repositories.
- **Customization**: Adjust environment variables to suit your needs.

## License

This project is licensed under the MIT License.