# Copyright 2024 DeepMind Technologies Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
# Run with source setup.sh

# Create a virtual environment
if [[ ! -d "venv" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created successfully."
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if activation was successful
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Virtual environment activated successfully."
else
    echo "Failed to activate virtual environment."
    exit 1
fi
# Check if requirements.txt exists
if [[ -f "requirements.txt" ]]; then
    echo "Installing requirements from requirements.txt..."
    pip install -r requirements.txt
    echo "Requirements installed successfully."
else
    echo "requirements.txt not found. Skipping package installation."
fi

echo "Setup process completed successfully."
echo "You can now run the ECS Editor and Simulation Stream application."
echo
echo "Usage instructions:"
echo "1. To launch the web interface:"
echo "   python app.py --web --model=MODEL_NAME --api_key=YOUR_API_KEY"
echo
echo "2. To launch the web interface with an ECS config:"
echo "   python app.py path/to/ecs_config.py --web --model=MODEL_NAME --api_key=YOUR_API_KEY"
echo
echo "3. To run a simulation from the command line with custom metrics:"
echo "   python app.py path/to/ecs_config.py --steps=10 --metrics=path/to/metrics_file.json --model=MODEL_NAME --api_key=YOUR_API_KEY"
