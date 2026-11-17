#!/usr/bin/env python

import numpy as np
from dividebyzero.array import DimensionalArray, array
from dividebyzero.registry import ErrorRegistry, get_registry

def test_non_zero_division():
    """Test that non-zero division works correctly in the test cases."""
    print("Testing array division...")
    arr = array([[1, 2], [3, 4]])
    divisor = array([[0, 2], [3, 0]])
    result = arr / divisor
    
    print(f"arr = {arr.array}")
    print(f"divisor = {divisor.array}")
    print(f"result = {result.array}")
    
    print(f"result[0, 1] = {result.array[0, 1]}")
    print(f"result[1, 0] = {result.array[1, 0]}")
    
    # Check if array[0, 1] / divisor[0, 1] == 1.0
    expected = 1.0
    actual = result.array[0, 1]
    print(f"Expected: {expected}, Actual: {actual}")
    
    # Check higher dimensional case
    print("\nTesting 3D array division...")
    arr3d = array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    divisor3d = array([[[0, 2], [3, 0]], [[5, 0], [0, 8]]])
    result3d = arr3d / divisor3d
    
    print(f"arr3d.shape = {arr3d.shape}")
    print(f"divisor3d.shape = {divisor3d.shape}")
    print(f"result3d.shape = {result3d.shape}")
    
    print(f"result3d[0, 0, 1] = {result3d.array[0, 0, 1]}")
    print(f"arr3d[0, 0, 1] = {arr3d.array[0, 0, 1]}")
    print(f"divisor3d[0, 0, 1] = {divisor3d.array[0, 0, 1]}")
    
    # The expected value is 2/2 = 1.0
    expected3d = 1.0
    actual3d = result3d.array[0, 0, 1]
    print(f"Expected: {expected3d}, Actual: {actual3d}")
    
if __name__ == "__main__":
    test_non_zero_division()