#!/bin/bash


# Check if the directory venv is provided
if [ -e "$SCRIPT_DIR/.venv" ]; then
    echo "Virtual environment already exists. Activating..."
    source $SCRIPT_DIR/.venv/bin/activate
else
    echo "Creating a new virtual environment..."
    python3 -m venv $SCRIPT_DIR/.venv
    source $SCRIPT_DIR/.venv/bin/activate
    pip install -r $SCRIPT_DIR/requirements.txt
fi

MAIN_PATH="$SCRIPT_DIR/main.py"


python3 $MAIN_PATH $1