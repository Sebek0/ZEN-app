#!/bin/bash
# Author: fibleep
# Date: 18/06/2023
# Description: Entrypoint for the docker container

######################

# Check if python is installed
if ! command -v python &> /dev/null
then
    apt-get update
    apt-get install -y python3 python3-pip
fi

# Activate the virtual environment
source .venv/bin/activate

# Install requirements
pip3 install -r requirements.txt

# Download the manifest
python3 zen_api/manifest.py

uvicorn zen_api.main:app --host 0.0.0.0 --port 8000 
