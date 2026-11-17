#!/usr/bin/env python3
"""
Temporal Rendering System Launcher
==================================
Choose your temporal rendering experience
"""

import sys
import subprocess
import os


def main():
    print("\n" + "█"*60)
    print("TEMPORAL RENDERING SYSTEM")
    print("Where Physics Creates Visual Reality")
    print("█"*60 + "\n")
    
    print("\n" + "─"*60)
    print("\nAvailable Renderers:")
    print("─"*60)
    
    print("\n1. Temporal Field Renderer")
    print("   - Real-time volumetric field visualization")
    print("   - Chronon flux with artificial color mapping")
    print("   - Interactive mass placement for gravity")
    
    print("\n2. Advanced Shell Renderer")
    print("   - GPU-accelerated shell dynamics")
    print("   - Compute shader field processing")
    print("   - Pure temporal geometry")
    
    print("\n3. Emergent Color Qualia Renderer (NEW)")
    print("   - Colors emerge from entropy flow topology")
    print("   - Neural-temporal correspondence")
    print("   - No artificial color mapping")
    print("   - Consciousness physics visualization")
    
    print("\n4. Exit")
    print("─"*60)
    
    while True:
        try:
            choice = int(input(f"\nSelect renderer (1-4): "))
            
            if choice == 4:
                print("Exiting...")
                break
            elif choice == 1:
                print("\nLaunching Temporal Field Renderer...")
                print("="*60)
                try:
                    subprocess.run([sys.executable, "temporal_field_renderer.py"])
                except Exception as e:
                    print(f"Error: {e}")
                break
            elif choice == 2:
                print("\nLaunching Advanced Shell Renderer...")
                print("="*60)
                try:
                    subprocess.run([sys.executable, "advanced_shell_renderer.py"])
                except Exception as e:
                    print(f"Error: {e}")
                break
            elif choice == 3:
                print("\nLaunching Emergent Color Qualia Renderer...")
                print("="*60)
                try:
                    subprocess.run([sys.executable, "temporal_field_renderer_emergent_color.py"])
                except Exception as e:
                    print(f"Error: {e}")
                break
            else:
                print("Invalid choice. Please enter 1-4")
        except ValueError:
            print("Please enter a number.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()