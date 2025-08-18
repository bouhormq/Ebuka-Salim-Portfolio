#!/bin/bash

# This script runs the tests locally without using Docker.
# It assumes you have a virtual environment set up and activated.

# Ensure the script stops if any command fails
set -e

echo "Installing dependencies..."
# Install the required Python packages
pip install -r requirements.txt

echo "Running tests..."
# Set the TESTING environment variable to true and run the tests
TESTING=true python -m unittest discover -v tests/

echo "Tests completed successfully!"