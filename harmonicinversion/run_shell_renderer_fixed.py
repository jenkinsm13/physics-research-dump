#!/usr/bin/env python3
"""
Shell-Based Rendering System Launcher (Fixed)
=============================================
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
            if dep == 'PyOpenGL':
                # Special check for PyOpenGL
                import OpenGL.GL
                print(f"  ✓ {dep}")
            else:
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


def main():
    print("\n" + "█"*60)
    print("SHELL-BASED TEMPORAL RENDERING SYSTEM")
    print("Where Physics and Graphics are One")
    print("█"*60 + "\n")
    
    basic_available, advanced_available = check_dependencies()
    
    print("\n" + "─"*60)
    print("Available Renderers:")
    print("─"*60)
    
    renderers = []
    
    if basic_available:
        renderers.append('basic')
        print("\n1. Temporal Field Renderer (PyGame/OpenGL)")
        print("   - Real-time volumetric field visualization")
        print("   - See chronon flux as flowing colors")
        print("   - Interactive mass placement for gravity")
        print("   - Slice through the temporal manifold")
    
    if advanced_available:
        if basic_available:
            idx = 2
        else:
            idx = 1
        renderers.append('advanced')
        print(f"\n{idx}. Advanced Shell Renderer (ModernGL)")
        print("   - GPU-accelerated shell dynamics")
        print("   - Compute shader field processing")
        print("   - Pure temporal geometry")
        print("   - No polygons - just time")
    
    exit_idx = len(renderers) + 1
    print(f"\n{exit_idx}. Exit")
    print("─"*60)
    
    if not renderers:
        print("\nNo renderers available! Please install dependencies:")
        print("  pip install pygame PyOpenGL PyOpenGL_accelerate")
        print("  pip install moderngl moderngl-window")
        sys.exit(1)
    
    while True:
        try:
            choice = int(input(f"\nSelect renderer (1-{exit_idx}): "))
            
            if choice == exit_idx:
                print("Exiting...")
                break
            elif choice > 0 and choice <= len(renderers):
                selected = renderers[choice - 1]
                
                if selected == 'basic':
                    print("\nLaunching Temporal Field Renderer...")
                    print("="*60)
                    try:
                        subprocess.run([sys.executable, "temporal_field_renderer.py"])
                    except Exception as e:
                        print(f"Error launching: {e}")
                        print("Trying direct import...")
                        from temporal_field_renderer import main as run_basic
                        run_basic()
                    break
                elif selected == 'advanced':
                    print("\nLaunching Advanced Shell Renderer...")
                    print("="*60)
                    try:
                        subprocess.run([sys.executable, "advanced_shell_renderer.py"])
                    except Exception as e:
                        print(f"Error launching: {e}")
                        print("Trying direct import...")
                        from advanced_shell_renderer import main as run_advanced
                        run_advanced()
                    break
            else:
                print(f"Invalid choice. Please enter 1-{exit_idx}")
        except ValueError:
            print("Please enter a number.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()