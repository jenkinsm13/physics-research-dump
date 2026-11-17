#!/bin/bash
# Script to run tests with coverage for dividebyzero package

# Navigate to the project directory
cd "$(dirname "$0")"

# Create the tests directory if it doesn't exist
mkdir -p tests

# Run tests with coverage and generate reports
python -m pytest tests/ \
    --cov=src/dividebyzero \
    --cov-report=term \
    --cov-report=html:coverage_html \
    --cov-report=xml:coverage.xml \
    --verbose

# Print success message with instructions to view the report
echo ""
echo "Coverage report generated!"
echo "View the HTML report by opening: coverage_html/index.html"
echo "XML report available at: coverage.xml" 