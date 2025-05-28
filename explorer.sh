#!/bin/bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

# Check if the directory venv is provided
if [ -e "$SCRIPT_DIR/.venv" ]; then
    echo "Virtual environment already exists. Activating..."
    source $SCRIPT_DIR/.venv/bin/activate
    echo "Virtual environment activated."
else
    echo "Creating a new virtual environment..."
    python3 -m venv $SCRIPT_DIR/.venv
    echo "Virtual environment created at $SCRIPT_DIR/.venv"
    echo
    echo "Activating the virtual environment..."
    source $SCRIPT_DIR/.venv/bin/activate
    echo "Virtual environment activated."
    echo
    echo "Installing required packages..."
    pip install -r $SCRIPT_DIR/requirements.txt
    echo "Required packages installed."
fi

echo 

MAIN_PATH="$SCRIPT_DIR/main.py"


python3 $MAIN_PATH $1