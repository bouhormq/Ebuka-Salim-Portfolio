#!/bin/bash

# IMPORTANT: Replace /path/to/your/project with the actual path to your project on the server
PROJECT_DIR="/root/myportfolio"

# Ensure the script stops if any command fails
set -e

# Navigate to the project directory
cd "$PROJECT_DIR"

echo "Fetching latest changes from GitHub..."
# Fetch the latest changes from the main branch on GitHub and reset the local branch
git fetch origin main && git reset --hard origin/main

echo "Spinning down existing containers..."
# Stop and remove the old containers to prevent resource conflicts
docker compose -f docker-compose.prod.yml down

echo "Building and starting new containers..."
# Build the new image and start the containers in detached mode
docker compose -f docker-compose.prod.yml up -d --build

echo "Deployment complete!"
