#!/usr/bin/env python3
"""
Test script for DimensionalArray.
"""

import numpy as np
from src.dividebyzero.array import DimensionalArray

# Basic creation
print("Creating arrays...")
a = DimensionalArray(np.array([1.0, 2.0, 0.0]))
b = DimensionalArray(np.array([3.0, 0.0, 5.0]))

# Test basic operations
print("\nBasic operations:")
print(f"a = {a}")
print(f"b = {b}")
print(f"a + b = {a + b}")
print(f"a - b = {a - b}")
print(f"a * b = {a * b}")

# Test division
print("\nDivision operations:")
try:
    print(f"a / b = {a / b}")
except Exception as e:
    print(f"a / b error: {e}")
    
try:
    print(f"b / a = {b / a}")
except Exception as e:
    print(f"b / a error: {e}")

# Test scalar division
print("\nScalar division:")
try:
    print(f"a / 2 = {a / 2}")
except Exception as e:
    print(f"a / 2 error: {e}")
    
try:
    print(f"2 / a = {2 / a}")
except Exception as e:
    print(f"2 / a error: {e}")

# Test power operations
print("\nPower operations:")
try:
    print(f"a ** 2 = {a ** 2}")
except Exception as e:
    print(f"a ** 2 error: {e}")
    
try:
    print(f"2 ** a = {2 ** a}")
except Exception as e:
    print(f"2 ** a error: {e}")

# Test log operations
print("\nLog operations:")
try:
    print(f"log(a) = {a.log()}")
except Exception as e:
    print(f"log(a) error: {e}") 