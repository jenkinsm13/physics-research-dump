#!/usr/bin/env python3
"""
Quick launcher for the Matryoshka-Chronon Framework
Run this to explore temporal physics without institutional constraints
"""

import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed."""
    required = ['numpy', 'scipy', 'matplotlib', 'sympy']
    optional = ['moderngl', 'moderngl_window', 'pyrr', 'ipywidgets']
    
    missing_required = []
    missing_optional = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing_required.append(package)
    
    for package in optional:
        try:
            __import__(package)
        except ImportError:
            missing_optional.append(package)
    
    if missing_required:
        print("ERROR: Missing required packages:")
        for pkg in missing_required:
            print(f"  - {pkg}")
        print("\nInstall with: pip install " + " ".join(missing_required))
        return False
    
    if missing_optional:
        print("NOTE: Some optional packages are missing:")
        for pkg in missing_optional:
            print(f"  - {pkg}")
        print("\nFor full features, install with: pip install " + " ".join(missing_optional))
        print("(The framework will still run without these)\n")
    
    return True

def main():
    print("\n" + "▓" * 60)
    print("MATRYOSHKA-CHRONON TEMPORAL PHYSICS")
    print("Launching beyond institutional thinking...")
    print("▓" * 60 + "\n")
    
    if not check_dependencies():
        sys.exit(1)
    
    print("All systems ready. Initiating temporal mechanics...\n")
    
    # Import and run the main framework
    try:
        from matryoshka_chronon_framework import main as run_framework
        run_framework()
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nTrying direct execution...")
        subprocess.run([sys.executable, "matryoshka_chronon_framework.py"])

if __name__ == "__main__":
    main()