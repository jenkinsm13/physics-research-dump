#!/usr/bin/env python3
# convert_to_pdf.py - Convert the Matryoshka theory Markdown report to PDF

import os
import sys
import subprocess

def check_pandoc_installed():
    """Check if pandoc is installed on the system."""
    try:
        subprocess.run(['pandoc', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def convert_markdown_to_pdf(markdown_file, output_pdf=None):
    """Convert a Markdown file to PDF using pandoc."""
    if not os.path.exists(markdown_file):
        print(f"Error: File {markdown_file} not found.")
        return False
    
    if output_pdf is None:
        output_pdf = os.path.splitext(markdown_file)[0] + ".pdf"
    
    # Pandoc command with options for nice formatting
    cmd = [
        'pandoc',
        '--pdf-engine=xelatex',  # Use xelatex for better Unicode support
        '--variable', 'geometry=margin=1in',  # Set margins
        '--variable', 'fontsize=11pt',  # Set font size
        '--highlight-style=tango',  # Code highlighting style
        '-s',  # Standalone document
        '--toc',  # Include table of contents
        '--toc-depth=2',  # ToC depth
        '--number-sections',  # Number sections
        '-o', output_pdf,  # Output file
        markdown_file  # Input file
    ]
    
    try:
        print(f"Converting {markdown_file} to PDF...")
        subprocess.run(cmd, check=True)
        print(f"Successfully created PDF: {output_pdf}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error converting to PDF: {e}")
        return False

def main():
    """Main function to convert the Matryoshka theory report to PDF."""
    # Check for pandoc
    if not check_pandoc_installed():
        print("Error: pandoc is not installed. Please install it to convert to PDF.")
        print("Installation instructions: https://pandoc.org/installing.html")
        sys.exit(1)
    
    # Default markdown file
    markdown_file = "matryoshka_theory_report.md"
    
    # If a filename is provided as an argument, use that instead
    if len(sys.argv) > 1:
        markdown_file = sys.argv[1]
    
    # Convert to PDF
    success = convert_markdown_to_pdf(markdown_file)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main() 