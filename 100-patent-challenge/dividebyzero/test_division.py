#!/usr/bin/env python
"""
Test script specifically for division by zero operations.
"""

import numpy as np
from dividebyzero.array import DimensionalArray, array
from dividebyzero.registry import ErrorRegistry

def test_scalar_division():
    print("Testing scalar division by zero...")
    a = array(5.0)
    result = a / 0
    print(f"5.0 / 0 = {result.array}")
    
    # Check that we can elevate the result back
    elevated = result.elevate()
    print(f"Elevated result: {elevated.array}")
    
    # Also test right division by zero
    b = array(0.0)
    right_div = 1.0 / b
    print(f"1.0 / 0.0 = {right_div.array}")
    
    return True

def test_array_division():
    print("\nTesting array division by zero...")
    a = array([1.0, 2.0, 3.0, 4.0, 5.0])
    b = array([1.0, 0.0, 3.0, 0.0, 5.0])
    
    # Divide a by b (which has zeros)
    result = a / b
    print(f"[1,2,3,4,5] / [1,0,3,0,5] = {result.array}")
    
    # Also test dividing by a zero scalar
    result2 = a / 0
    print(f"[1,2,3,4,5] / 0 = {result2.array}")
    
    return True

def test_matrix_division():
    print("\nTesting matrix division by zero...")
    a = array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    b = array([[1.0, 0.0, 3.0], [0.0, 5.0, 6.0], [7.0, 8.0, 0.0]])
    
    # Divide a by b (which has zeros)
    result = a / b
    print("Matrix a / b (with zeros) = ")
    print(result.array)
    
    # Also test dividing by a zero scalar
    result2 = a / 0
    print("Matrix a / 0 = ")
    print(result2.array)
    
    # Try to elevate the result
    elevated = result2.elevate()
    print("Elevated matrix:")
    print(elevated.array)
    
    return True

if __name__ == "__main__":
    test_scalar_division()
    test_array_division()
    test_matrix_division()
    print("\nAll division tests completed!")