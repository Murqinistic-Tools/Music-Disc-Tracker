#!/bin/bash
# Music Disc Tracker - Linux/macOS Launcher

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Installing dependencies..."
    ./venv/bin/pip install -r requirements.txt
fi

# Run the application
./venv/bin/python src/main.py
