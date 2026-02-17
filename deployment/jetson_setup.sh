#!/bin/bash

echo "Jetson Nano Setup Script"
echo "========================="

echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    python3-dev \
    libzbar0 \
    libopencv-dev \
    python3-opencv

echo "Installing Python packages..."
pip3 install --user \
    pyzbar \
    requests \
    Pillow \
    pyyaml \
    psutil

echo "Setting up directories..."
mkdir -p logs/csvs
mkdir -p logs/images
mkdir -p config
mkdir -p tests/test_images

echo "Configuring camera permissions..."
sudo usermod -a -G video $USER

echo "Testing camera..."
if v4l2-ctl --list-devices > /dev/null 2>&1; then
    echo "Camera detected!"
else
    echo "Warning: No camera detected"
fi

echo "Setup complete!"
echo "Please log out and back in for group changes to take effect"