@echo off
title Music Disc Tracker

:: Check if venv exists
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing dependencies...
    venv\Scripts\pip install -r requirements.txt
)

:: Run the application
venv\Scripts\python.exe src\main.py
