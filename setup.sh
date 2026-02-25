#!/bin/bash
# Quick Setup Script for Canary Scanners

set -e

echo "=================================="
echo "Canary Scanners - Quick Setup"
echo "=================================="
echo ""

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

echo "✓ Python3 found: $(python3 --version)"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "✓ .env file already exists"
else
    echo "Creating .env file for credentials..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your Canary credentials:"
    echo "   nano .env"
    echo ""
    echo "   Set these values:"
    echo "   - CANARY_CONSOLE_DOMAIN (e.g., 1234abc.canary.tools)"
    echo "   - CANARY_API_KEY (from your Canary console)"
fi

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials: nano .env"
echo "2. Run the script: python3 canary_events.py"
echo ""
echo "The script will automatically load credentials from .env file."
echo ""
