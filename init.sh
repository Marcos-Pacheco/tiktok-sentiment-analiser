#!/bin/bash
REQUIRED_VERSION="3.10.12"

# Check if Python is installed and get the version
if command -v python3 &> /dev/null; then
    INSTALLED_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
elif command -v python &> /dev/null; then
    INSTALLED_VERSION=$(python --version 2>&1 | awk '{print $2}')
elif command -v py &> /dev/null; then
    INSTALLED_VERSION=$(py --version 2>&1 | awk '{print $2}')
else
    echo "Python is not installed."
    exit 1
fi

# Compare installed version with the required version
if [ "$INSTALLED_VERSION" = "$REQUIRED_VERSION" ]; then
    echo "Correct Python version is installed: $INSTALLED_VERSION"
else
    echo "Incorrect Python version. Installed: $INSTALLED_VERSION, Required: $REQUIRED_VERSION"
    exit 1
fi

# Create virtual env
virtualenv env --python="$REQUIRED_VERSION"

# Start enviroment
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install the webdrivers
sudo $(which python) -m webdrivermanager 'firefox:latest' 'chrome:latest' --linkpath /usr/local/bin