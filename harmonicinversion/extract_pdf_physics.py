#!/usr/bin/env python3
"""
Extract key physics from PDF papers using pdftotext
"""

import subprocess
import os

# List of PDFs to extract
pdf_files = [
    "Quantum Gravity as Inverse Temporal Flow - A Matryoshka Model.pdf",
    "Matryoshka-Chronon Framework - Documentary Interview Talking Points.pdf"
]

# Extract text from PDFs
for pdf in pdf_files:
    pdf_path = f"/Users/erickgeisler/Downloads/HarmonicInversion/{pdf}"
    txt_path = pdf_path.replace('.pdf', '.txt')
    
    if os.path.exists(pdf_path):
        print(f"Extracting {pdf}...")
        try:
            subprocess.run(['pdftotext', pdf_path, txt_path], check=True)
            print(f"Extracted to {txt_path}")
            
            # Read and display key sections
            with open(txt_path, 'r') as f:
                content = f.read()
                
            # Look for key physics sections
            if "temporal flow" in content.lower():
                print("\nFound temporal flow physics:")
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if "temporal flow" in line.lower() and "asymmetr" in line.lower():
                        # Print context
                        start = max(0, i-2)
                        end = min(len(lines), i+3)
                        for j in range(start, end):
                            print(f"  {lines[j]}")
                        print()
                        
        except subprocess.CalledProcessError:
            print(f"Error extracting {pdf}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"PDF not found: {pdf_path}")