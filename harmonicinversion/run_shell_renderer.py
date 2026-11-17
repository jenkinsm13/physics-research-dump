#!/usr/bin/env python3
"""
Shell-Based Rendering System Launcher
=====================================
Choose your temporal rendering experience
"""

import sys
import subprocess
import os


def check_dependencies():
    """Check which rendering systems are available."""
    basic_deps = ['numpy', 'pygame', 'PyOpenGL']
    advanced_deps = ['moderngl', 'moderngl_window']
    optional_deps = ['numba', 'cupy', 'scipy', 'sympy']
    
    print("Checking dependencies...")
    
    # Check basic renderer deps
    basic_available = True
    for dep in basic_deps:
        try:
            __import__(dep)
            print(f"  ✓ {dep}")
        except ImportError:
            print(f"  ✗ {dep}")
            basic_available = False
    
    # Check advanced renderer deps
    advanced_available = True
    for dep in advanced_deps:
        try:
            __import__(dep)
            print(f"  ✓ {dep}")
        except ImportError:
            print(f"  ✗ {dep}")
            advanced_available = False
    
    # Check optional deps
    print("\nOptional enhancements:")
    for dep in optional_deps:
        try:
            __import__(dep)
            print(f"  ✓ {dep}")
        except ImportError:
            print(f"  ○ {dep} (not installed)")
    
    return basic_available, advanced_available


def install_dependencies():
    """Offer to install missing dependencies."""
    print("\nWould you like to install missing dependencies?")
    print("1. Basic renderer dependencies (pygame, PyOpenGL)")
    print("2. Advanced renderer dependencies (moderngl)")
    print("3. All dependencies")
    print("4. Skip installation")
    
    choice = input("\nChoice (1-4): ")
    
    if choice == '1':
        subprocess.run([sys.executable, '-m', 'pip', 'install', 
                       'numpy', 'pygame', 'PyOpenGL', 'PyOpenGL_accelerate'])
    elif choice == '2':
        subprocess.run([sys.executable, '-m', 'pip', 'install', 
                       'numpy', 'moderngl', 'moderngl-window', 'pyglet'])
    elif choice == '3':
        subprocess.run([sys.executable, '-m', 'pip', 'install', 
                       'numpy', 'pygame', 'PyOpenGL', 'PyOpenGL_accelerate',
                       'moderngl', 'moderngl-window', 'pyglet',
                       'scipy', 'sympy', 'numba'])
    
    return choice != '4'


def main():
    print("\n" + "█"*60)
    print("SHELL-BASED TEMPORAL RENDERING SYSTEM")
    print("Where Physics and Graphics are One")
    print("█"*60 + "\n")
    
    basic_available, advanced_available = check_dependencies()
    
    if not basic_available and not advanced_available:
        print("\nNo renderer available!")
        if install_dependencies():
            # Re-check after installation
            basic_available, advanced_available = check_dependencies()
        else:
            print("Cannot proceed without dependencies.")
            sys.exit(1)
    
    print("\n" + "─"*60)
    print("Available Renderers:")
    print("─"*60)
    
    options = []
    
    if basic_available:
        options.append("1. Temporal Field Renderer (PyGame/OpenGL)")
        print("1. Temporal Field Renderer")
        print("   - Real-time volumetric field visualization")
        print("   - See chronon flux as flowing colors")
        print("   - Interactive mass placement for gravity")
        print("   - Slice through the temporal manifold")
    
    if advanced_available:
        idx = len(options) + 1
        options.append(f"{idx}. Advanced Shell Renderer (ModernGL)")
        print(f"\n{idx}. Advanced Shell Renderer")
        print("   - GPU-accelerated shell dynamics")
        print("   - Compute shader field processing")
        print("   - Pure temporal geometry")
        print("   - No polygons - just time")
    
    print(f"\n{len(options)+1}. Exit")
    print("─"*60)
    
    while True:
        try:
            choice = int(input(f"\nSelect renderer (1-{len(options)+1}): "))
            
            if choice == len(options) + 1:
                print("Exiting...")
                break
            elif choice == 1 and basic_available:
                print("\nLaunching Temporal Field Renderer...")
                print("="*60)
                subprocess.run([sys.executable, "temporal_field_renderer.py"])
                break
            elif choice == 2 and advanced_available and len(options) >= 2:
                print("\nLaunching Advanced Shell Renderer...")
                print("="*60)
                subprocess.run([sys.executable, "advanced_shell_renderer.py"])
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Trying direct module import...")
            
            if choice == 1 and basic_available:
                from temporal_field_renderer import main as run_basic
                run_basic()
            elif choice == 2 and advanced_available:
                from advanced_shell_renderer import main as run_advanced
                run_advanced()


if __name__ == "__main__":
    main()