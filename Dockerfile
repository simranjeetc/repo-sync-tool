FROM python:3.9-slim

WORKDIR /app

# Accept proxy settings as build arguments
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY

# Set the proxy environment variables
ENV http_proxy=${HTTP_PROXY}
ENV https_proxy=${HTTPS_PROXY}
ENV no_proxy=${NO_PROXY}

# Install git and clean up to reduce image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    openssh-client \
    curl \
    inetutils-ping \
    net-tools \
    iproute2 \
    dnsutils && \
    rm -rf /var/lib/apt/lists/*

# Copy only necessary files
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY config.py logger.py main.py github_manager.py gitlab_manager.py repo_cloner.py entrypoint.sh ./

RUN chmod a+x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

