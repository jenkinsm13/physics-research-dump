#!/bin/bash
# Script to run tests for dividebyzero package

# Navigate to the project directory
cd /Volumes/4TB/ClaudeCode/dividebyzero

# Run tests with coverage
python -m pytest --cov=dividebyzero tests/