#!/usr/bin/env python

import numpy as np
from dividebyzero.array import DimensionalArray, array
from dividebyzero.registry import ErrorRegistry, get_registry

def debug_array_test_cases():
    """Debug the specific test cases that are failing."""
    # First failing test case
    print("Debugging test_partial_division_by_zero")
    arr1 = array([[1, 2], [3, 4]])
    divisor1 = array([[0, 2], [3, 0]])
    result1 = arr1 / divisor1
    
    print(f"arr1 = \n{arr1.array}")
    print(f"divisor1 = \n{divisor1.array}")
    print(f"result1 = \n{result1.array}")
    print(f"result1[0, 1] = {result1.array[0, 1]}")
    print(f"result1[1, 0] = {result1.array[1, 0]}")
    
    # Print array and divisor objects to see their exact types
    print(f"\narr1 type: {type(arr1)}")
    print(f"divisor1 type: {type(divisor1)}")
    print(f"arr1 is DimensionalArray: {isinstance(arr1, DimensionalArray)}")
    print(f"divisor1 is DimensionalArray: {isinstance(divisor1, DimensionalArray)}")
    
    # Print array values for comparison
    print(f"\narr1.array = {arr1.array}")
    print(f"arr1.array type: {type(arr1.array)}")
    print(f"divisor1.array = {divisor1.array}")
    print(f"divisor1.array type: {type(divisor1.array)}")
    print(f"array_equal check: {np.array_equal(divisor1.array, np.array([[0, 2], [3, 0]]))}")
    
    # Second failing test case
    print("\nDebugging test_partial_division_higher_dims")
    arr2 = array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    divisor2 = array([[[0, 2], [3, 0]], [[5, 0], [0, 8]]])
    result2 = arr2 / divisor2
    
    print(f"arr2.shape = {arr2.shape}")
    print(f"divisor2.shape = {divisor2.shape}")
    print(f"result2.shape = {result2.shape}")
    
    print(f"result2[0, 0, 1] = {result2.array[0, 0, 1]}")
    print(f"arr2[0, 0, 1] = {arr2.array[0, 0, 1]}")
    print(f"divisor2[0, 0, 1] = {divisor2.array[0, 0, 1]}")
    
    # Print array and divisor objects to see their exact types
    print(f"\narr2 type: {type(arr2)}")
    print(f"divisor2 type: {type(divisor2)}")
    print(f"arr2 is DimensionalArray: {isinstance(arr2, DimensionalArray)}")
    print(f"divisor2 is DimensionalArray: {isinstance(divisor2, DimensionalArray)}")
    
    # Print array values for comparison
    print(f"\ndivisor2.array = {divisor2.array}")
    print(f"Expected divisor check: {np.array_equal(divisor2.array, np.array([[[0, 2], [3, 0]], [[5, 0], [0, 8]]]))}")

if __name__ == "__main__":
    debug_array_test_cases()