#!/bin/bash

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p data/raw data/processed models

# Make sure data directory exists
if [ ! -f "data/energy_data.csv" ]; then
    echo "Creating empty energy_data.csv"
    echo "timestamp,watts" > data/energy_data.csv
fi

echo "Setup complete! To activate the environment, run:"
echo "source venv/bin/activate" 