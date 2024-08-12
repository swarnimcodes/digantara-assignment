#! /bin/env bash

# Clone the repo
git clone "https://github.com/swarnimcodes/digantara-assignment.git" 

# CD into the project
cd digantara-assignment || exit

# Make virtual environment
python3 -m venv .venv

# Source the virtual environment
source .venv/bin/activate

# Install the requirements
pip install -r requirements.txt

# Run the server
python3 -m uvicorn scheduler:app --reload
