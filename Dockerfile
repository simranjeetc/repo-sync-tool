FROM python:3.9-slim

WORKDIR /app

# Install git and clean up to reduce image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends git openssh-client && \
    rm -rf /var/lib/apt/lists/*

# Copy only necessary files
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY config.py logger.py main.py github_manager.py gitlab_manager.py repo_cloner.py entrypoint.sh ./

RUN chmod a+x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

