#!/bin/bash

# AI Transaction Validator - Quick Start Script for macOS/Linux

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   AI Transaction Validator - Starting Server             ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

# Check if requirements are installed
python3 -c "import fastapi" &> /dev/null
if [ $? -ne 0 ]; then
    echo "Installing required dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

# Start the application
echo "Starting FastAPI server..."
echo ""
echo "Server will be available at: http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn main:app --reload
