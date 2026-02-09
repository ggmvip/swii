#!/bin/bash
# Development Environment Setup

set -e

echo "========================================="
echo "Setting up Barcode Detection Environment"
echo "========================================="

# Check Python version
echo "Checking Python version..."
python3 --version

# Check if running on Jetson
if [ -f "/etc/nv_tegra_release" ]; then
    echo "✓ Detected: NVIDIA Jetson Nano"
    export PLATFORM=jetson
else
    echo "✓ Detected: Desktop/Other platform"
    export PLATFORM=desktop
fi

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env from template if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created - please edit with your settings"
fi

# Create necessary directories
echo "Creating directory structure..."
mkdir -p data/curated_dataset
mkdir -p data/train_images
mkdir -p data/val_images
mkdir -p data/test_images
mkdir -p data/model
mkdir -p logs
mkdir -p checkpoints
mkdir -p reports

# Git setup
if [ -d ".git" ]; then
    echo "Git repository already initialized"
else
    echo "Initializing Git repository..."
    git init
    git checkout -b dev
    echo "✓ Git initialized with 'dev' branch"
fi

echo ""
echo "========================================="
echo "Environment Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env with your configuration"
echo "2. Place curated dataset in data/curated_dataset/"
echo "3. Run: source venv/bin/activate"
echo "4. Run baseline tests: python3 scripts/run_baseline_tests.py"
echo ""
