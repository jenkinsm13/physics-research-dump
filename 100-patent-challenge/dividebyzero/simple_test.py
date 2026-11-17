#!/usr/bin/env python3
"""
Simple test script to diagnose dividebyzero issues.
"""

import sys
import os
import numpy as np

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Step 1: Import core modules")
    from src.dividebyzero.exceptions import DimensionalError, ReconstructionError
    print("  ✓ Imported exceptions")
    
    from src.dividebyzero.registry import ErrorRegistry, ErrorData, get_registry
    print("  ✓ Imported registry module, including get_registry")
    
    from src.dividebyzero.array import DimensionalArray
    print("  ✓ Imported DimensionalArray")
    
    from src.dividebyzero.array import array
    print("  ✓ Imported array factory function")
    
    print("\nStep 2: Create and use registry")
    registry = get_registry()
    print(f"  ✓ Got registry: {registry}")
    
    print("\nStep 3: Create arrays with registry")
    arr = array([1, 2, 3], error_registry=registry)
    print(f"  ✓ Created array: shape={arr.shape}, registry={arr.error_registry}")
    
    print("\nStep 4: Basic operations")
    result = arr * 2
    print(f"  ✓ arr * 2 = {result.array}")
    result = arr + 1
    print(f"  ✓ arr + 1 = {result.array}")
    result = arr - 1
    print(f"  ✓ arr - 1 = {result.array}")
    
    print("\nStep 5: Division by zero (scalar)")
    a = array(5.0)
    result = a / 0
    print(f"  ✓ 5.0 / 0 produces: shape={result.shape}, error_id={result._error_id}")
    print(f"    Result value: {result.array}")
    elevated = result.elevate()
    print(f"  ✓ Elevated result: shape={elevated.shape}, array={elevated.array}")
    
    print("\nStep 6: Right division by zero (scalar)")
    b = array(0.0)
    right_div = 1.0 / b
    print(f"  ✓ 1.0 / 0.0 produces: shape={right_div.shape}, error_id={right_div._error_id}")
    print(f"    Result value: {right_div.array}")
    elevated = right_div.elevate()
    print(f"  ✓ Elevated result: shape={elevated.shape}, array={elevated.array}")
    
    print("\nStep 7: Partial division by zero (array)")
    a = array([1.0, 2.0, 3.0, 4.0, 5.0])
    b = array([1.0, 0.0, 3.0, 0.0, 5.0])
    result = a / b
    print(f"  ✓ Array division with zeros produces: shape={result.shape}, error_id={result._error_id}")
    print(f"    Result value: {result.array}")
    
    print("\nStep 8: Division by zero (matrix)")
    a = array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    result = a / 0
    print(f"  ✓ Matrix / 0 produces: shape={result.shape}, error_id={result._error_id}")
    print(f"    Result value: {result.array}")
    elevated = result.elevate()
    print(f"  ✓ Elevated result: shape={elevated.shape}")
    print(f"    Elevated matrix:\n{elevated.array}")
    
    print("\nStep 9: Partial division by zero (matrix)")
    a = array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    b = array([[1.0, 0.0, 3.0], [0.0, 5.0, 6.0], [7.0, 8.0, 0.0]])
    result = a / b
    print(f"  ✓ Matrix division with zeros produces: shape={result.shape}, error_id={result._error_id}")
    print(f"    Result matrix:\n{result.array}")
    
    print("\nAll tests passed successfully!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)