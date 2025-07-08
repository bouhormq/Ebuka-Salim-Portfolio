#!/bin/bash

PROJECT_DIR="$HOME/Ebuka-Salim-Portfolio"

VENV_DIR="python3-virtualenv"

FLASK_START_COMMAND="flask run --host=0.0.0.0"

echo "Starting redeployment process..."

echo "1. Killing all existing tmux sessions..."
tmux kill-server || true

echo "2. Changing into project directory: $PROJECT_DIR"
cd "$PROJECT_DIR" || { echo "Error: Project directory not found at $PROJECT_DIR. Exiting."; exit 1; }

echo "3. Fetching latest changes from GitHub and hard resetting..."
git fetch origin
git reset origin/main --hard || { echo "Error: Git reset failed. Check your repository and branch. Exiting."; exit 1; }
echo "Git repository updated."

echo "4. Activating Python virtual environment and installing dependencies..."
# Check if the virtual environment activation script exists
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "Error: Virtual environment activation script not found at $VENV_DIR/bin/activate. Exiting."
    exit 1
fi
source "$VENV_DIR/bin/activate"

# Explicitly use the pip from the virtual environment
if [ ! -f "$VENV_DIR/bin/pip" ]; then
    echo "Error: pip executable not found in virtual environment at $VENV_DIR/bin/pip. Exiting."
    exit 1
fi
"$VENV_DIR/bin/pip" install -r requirements.txt || { echo "Error: Failed to install Python dependencies. Exiting."; exit 1; }
echo "Python dependencies installed."

echo "5. Starting Flask server in a new detached Tmux session..."
tmux new-session -d -s flask_app -c "$PROJECT_DIR" "source $VENV_DIR/bin/activate && $FLASK_START_COMMAND"

echo "Flask server should now be running in a detached tmux session named 'flask_app'."
echo "You can reattach to it using: tmux attach -t flask_app"
echo "Redeployment complete!"
