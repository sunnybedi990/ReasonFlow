#!/bin/bash
# ReasonFlow Installation Script

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install wheel if not present
pip install wheel

# Install the package
pip install dist/*.whl

echo "ReasonFlow installed successfully!"
