"""
Basic test script to verify the functionality of the DivideByZero framework.
"""

import sys
import os
import numpy as np

# Import core modules directly from the package
try:
    from dividebyzero.array import DimensionalArray, array
    from dividebyzero.exceptions import DimensionalError
    import dividebyzero as dbz
    
    print("Successfully imported core modules.")
except ImportError as e:
    print(f"Error importing core modules: {e}")
    sys.exit(1)

# Test 1: Basic array creation
try:
    a = array([1, 2, 3])
    b = array([[1, 2], [3, 4]])
    print(f"Test 1: Created arrays - shapes: {a.shape}, {b.shape}")
    print("Test 1: Passed")
except Exception as e:
    print(f"Test 1 failed: {e}")
    sys.exit(1)

# Test 2: Basic arithmetic operations
try:
    a = array([1, 2, 3])
    b = array([4, 5, 6])
    c = a + b
    d = a * b
    e = a - b
    print(f"Test 2: Arithmetic results: {c.array}, {d.array}, {e.array}")
    print("Test 2: Passed")
except Exception as e:
    print(f"Test 2 failed: {e}")
    sys.exit(1)

# Test 3: Division by zero
try:
    a = array([1, 2, 3])
    b = array([1, 0, 3])
    c = a / b
    print(f"Test 3: Division by zero handled - result shape: {c.shape}")
    print("Test 3: Passed")
except Exception as e:
    print(f"Test 3 failed: {e}")
    sys.exit(1)

# Test 4: Logarithm of zero
try:
    from dividebyzero import log
    
    a = array([1, 0, 3])
    b = log(a)
    print(f"Test 4: Logarithm of zero handled - result shape: {b.shape}")
    print("Test 4: Passed")
except Exception as e:
    print(f"Test 4 failed: {e}")
    sys.exit(1)

# Test 5: Matrix operations
try:
    from dividebyzero import logm
    
    a = array([[1, 2], [3, 4]])
    b = logm(a)
    
    # Singular matrix
    c = array([[1, 2], [2, 4]])  # determinant is zero
    d = logm(c)
    
    print(f"Test 5: Matrix logarithm handled - result shapes: {b.shape}, {d.shape}")
    print("Test 5: Passed")
except Exception as e:
    print(f"Test 5 failed: {e}")
    sys.exit(1)

# Test 6: Power operations
try:
    from dividebyzero import power
    
    a = array([0, 1, 2])
    
    # Test 0^0
    b = power(array(0), array(0))
    
    # Test 0^(-1)
    c = power(array(0), array(-1))
    
    # Test (-1)^(0.5)
    d = power(array(-1), array(0.5))
    
    print(f"Test 6: Power operations handled - results: {b.array}, {c.array}, {d.array}")
    print("Test 6: Passed")
except Exception as e:
    print(f"Test 6 failed: {e}")
    sys.exit(1)

# Test 7: Quantum operations
try:
    from dividebyzero.quantum.tensor import QuantumTensor
    
    # Create quantum tensor
    qt = QuantumTensor(np.array([[1, 0], [0, 0]]))
    
    # Division by zero
    qt_div = qt / 0
    
    # Elevation
    qt_elevated = qt_div.elevate()
    
    print(f"Test 7: Quantum operations handled - shapes: {qt_div.shape}, {qt_elevated.shape}")
    print("Test 7: Passed")
except Exception as e:
    print(f"Test 7 failed: {e}")
    sys.exit(1)

# Test 8: Entropy calculations
try:
    from dividebyzero.quantum.entropy import von_neumann_entropy, renyi_entropy
    from dividebyzero.quantum.fractal import QuantumDensityMatrix
    
    # Create a density matrix
    rho = QuantumDensityMatrix(np.array([[0.5, 0], [0, 0.5]]))
    
    # Calculate entropies
    vn_entropy = von_neumann_entropy(rho)
    renyi_ent = renyi_entropy(rho, alpha=2.0)
    
    print(f"Test 8: Entropy calculations - results: VN={vn_entropy}, Renyi={renyi_ent}")
    print("Test 8: Passed")
except Exception as e:
    print(f"Test 8 failed: {e}")
    sys.exit(1)

print("\nAll tests passed! The DivideByZero framework is functioning correctly.")