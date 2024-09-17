#!/bin/bash

# Ensure the .ssh directory exists
mkdir -p /root/.ssh

# Copy SSH keys and config to /root/.ssh
cp -r /tmp/ssh_keys_mount/* /root/.ssh/

# Set permissions for SSH keys and config file
chmod 600 /root/.ssh/id_rsa
chmod 644 /root/.ssh/id_rsa.pub
chmod 600 /root/.ssh/config

# Start the main application
exec python main.py
