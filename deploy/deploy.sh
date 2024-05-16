#!/bin/bash

apt install python3.11-venv

echo "Creating venv..."
python3 -m venv .venv
echo "Activating venv..."
source .venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

echo "Telling Flask it is behind a proxy..."
touch src/proxy


