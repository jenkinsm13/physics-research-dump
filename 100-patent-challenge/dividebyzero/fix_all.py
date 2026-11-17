#!/usr/bin/env python
"""
Fix script for the dividebyzero library.

This script identifies and fixes common issues with the library,
including import problems, registration of functions, and test failures.
"""

import os
import sys
import re
import importlib
import importlib.util
from pathlib import Path

def fix_registry_module():
    """Fix the registry.py module."""
    print("Fixing registry.py...")
    registry_path = Path("src/dividebyzero/registry.py")
    if not registry_path.exists():
        print(f"  Error: {registry_path} does not exist!")
        return False

    with open(registry_path, "r") as f:
        content = f.read()

    # Make sure imports are correct
    if "from exceptions import" in content:
        content = content.replace("from exceptions import", "from .exceptions import")
        print("  Fixed relative imports in registry.py")

    # Make sure ErrorRegistry is defined before get_registry
    class_pos = content.find("class ErrorRegistry")
    get_registry_pos = content.find("def get_registry")
    
    if class_pos > 0 and get_registry_pos > 0 and get_registry_pos < class_pos:
        print("  Fixing ErrorRegistry and get_registry order")
        # Extract the parts
        parts = re.split(r'(class ErrorRegistry.*?)\s+(# Create a global registry.*?def get_registry.*?return _GLOBAL_REGISTRY)', 
                         content, flags=re.DOTALL)
        if len(parts) >= 4:
            # Reorder them
            content = parts[0] + parts[2] + "\n\n" + parts[1] + parts[3]
    
    # Ensure get_registry is properly defined
    if "_GLOBAL_REGISTRY = None" not in content:
        registry_part = "# Create a global registry instance\n_GLOBAL_REGISTRY = None\n\ndef get_registry():\n    \"\"\"Get the global error registry.\"\"\"\n    global _GLOBAL_REGISTRY\n    if _GLOBAL_REGISTRY is None:\n        _GLOBAL_REGISTRY = ErrorRegistry()\n    return _GLOBAL_REGISTRY\n\n"
        if "def get_registry" not in content:
            # Add get_registry right after ErrorRegistry class
            content = re.sub(r"(class ErrorRegistry.*?)(\s+def \w+|\s*$)", r"\1\n\n" + registry_part + r"\2", content, flags=re.DOTALL)
            print("  Added get_registry function")
        
    # Write the fixed content
    with open(registry_path, "w") as f:
        f.write(content)
    
    return True

def fix_array_module():
    """Fix the array.py module."""
    print("Fixing array.py...")
    array_path = Path("src/dividebyzero/array.py")
    if not array_path.exists():
        print(f"  Error: {array_path} does not exist!")
        return False

    with open(array_path, "r") as f:
        content = f.read()

    # Fix imports
    if "import registry" in content:
        content = content.replace("import registry", "from . import registry")
        print("  Fixed registry import")
    
    if "from powers import" in content:
        content = content.replace("from powers import", "from .powers import")
        print("  Fixed powers import")
        
    if "from logarithmic_functions import" in content:
        content = content.replace("from logarithmic_functions import", "from .logarithmic_functions import")
        print("  Fixed logarithmic_functions import")

    # Fix duplicate array function
    if "return DimensionalArray(array_like, error_registry=error_registry, dtype=dtype)\n    return DimensionalArray" in content:
        content = content.replace("return DimensionalArray(array_like, error_registry=error_registry, dtype=dtype)\n    return DimensionalArray", 
                                 "return DimensionalArray(array_like, error_registry=error_registry, dtype=dtype)")
        print("  Fixed duplicate return statement in array function")

    # Write the fixed content
    with open(array_path, "w") as f:
        f.write(content)
    
    return True

def fix_init_module():
    """Fix the __init__.py module."""
    print("Fixing __init__.py...")
    init_path = Path("src/dividebyzero/__init__.py")
    if not init_path.exists():
        print(f"  Error: {init_path} does not exist!")
        return False

    with open(init_path, "r") as f:
        content = f.read()

    # Fix imports
    import_map = {
        "from array import": "from .array import",
        "from registry import": "from .registry import",
        "from exceptions import": "from .exceptions import",
        "import numpy_compat": "from . import numpy_compat",
        "from numpy_registry import": "from .numpy_registry import",
        "import quantum": "from . import quantum",
        "import linalg": "from . import linalg",
        "import random": "from . import random",
        "import fft": "from . import fft",
        "from logarithmic_functions import": "from .logarithmic_functions import",
        "from logarithm_extensions import": "from .logarithm_extensions import",
        "from powers import": "from .powers import"
    }
    
    for old, new in import_map.items():
        if old in content and new not in content:
            content = content.replace(old, new)
            print(f"  Fixed import: {old} -> {new}")

    # Fix array function
    if "def array(array_like, dtype=None):" in content:
        content = content.replace(
            "def array(array_like, dtype=None):",
            "def array(array_like, dtype=None, error_registry=None):"
        )
        content = content.replace(
            "    return DimensionalArray(array_like, error_registry=_REGISTRY, dtype=dtype)",
            "    if error_registry is None:\n        error_registry = _REGISTRY\n    return DimensionalArray(array_like, error_registry=error_registry, dtype=dtype)"
        )
        print("  Fixed array function definition to handle error_registry parameter")

    # Write the fixed content
    with open(init_path, "w") as f:
        f.write(content)
    
    return True

def run_tests():
    """Run the tests to verify fixes."""
    print("\nRunning tests...")
    try:
        # Try importing the library
        sys.path.insert(0, os.getcwd())
        import dividebyzero as dbz
        from dividebyzero.array import DimensionalArray
        from dividebyzero.exceptions import DimensionalError
        
        # Create a simple array
        a = dbz.array([1, 2, 3])
        print(f"Created array with shape {a.shape}")
        
        # Test division by zero
        b = a / 0
        print(f"Division by zero worked, created array with shape {b.shape}")
        
        # Test elevation
        c = b.elevate()
        print(f"Elevation worked, created array with shape {c.shape}")
        
        print("All basic tests passed!")
        return True
    except Exception as e:
        print(f"Test failed: {e}")
        return False

def main():
    """Main function to run all fixes."""
    print("Fixing dividebyzero library...")
    
    # Run fixes
    registry_fixed = fix_registry_module()
    array_fixed = fix_array_module()
    init_fixed = fix_init_module()
    
    # Run tests
    if registry_fixed and array_fixed and init_fixed:
        print("\nAll fixes applied. Testing...")
        test_result = run_tests()
        if test_result:
            print("\nAll fixes successful!")
        else:
            print("\nSome tests failed even after fixes.")
    else:
        print("\nSome fixes could not be applied.")

if __name__ == "__main__":
    main()