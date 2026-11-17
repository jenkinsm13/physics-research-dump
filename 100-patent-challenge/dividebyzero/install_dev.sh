#!/bin/bash
# Script to install the dividebyzero package in development mode

# Navigate to the project directory
cd /Volumes/4TB/ClaudeCode/dividebyzero

# Install the package in development mode with quantum and test dependencies
pip install -e ".[quantum,test]"