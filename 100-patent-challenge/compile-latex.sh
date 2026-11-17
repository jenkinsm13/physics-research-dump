#!/bin/bash

# Get the filename from the arguments
FILENAME="$1"

# Run pdflatex on the file
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error "$FILENAME"

# Return the exit code of pdflatex
exit $? 