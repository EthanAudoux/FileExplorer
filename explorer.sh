#!/bin/bash

# Check if the directory venv is provided
if [ -e "./.venv" ]; then
    echo "Virtual environment already exists. Activating..."
    source .venv/bin/activate
else
    echo "Creating a new virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
fi


python3 ./main.py $1