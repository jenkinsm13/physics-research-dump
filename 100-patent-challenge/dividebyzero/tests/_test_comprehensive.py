"""
Comprehensive test for DivideByZero framework.

This script tests all the key aspects of the framework, particularly focusing on:
1. Division by zero
2. Logarithm of zero
3. Handling of power operations with singularities (0^0, 0^-1, etc.)
4. Matrix operations with singular values
5. Quantum operations
6. Entropy calculations with singularities

The framework should handle all these cases without arbitrary thresholds, epsilon
additions, or other numerical workarounds.
"""

import sys
import os
import numpy as np
import importlib.util

# Define framework directory
FRAMEWORK_DIR = '/Volumes/4TB/ClaudeCode/dividebyzero'
sys.path.insert(0, FRAMEWORK_DIR)

# Function to load modules safely
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Import core modules
array_module = load_module("dividebyzero_array", os.path.join(FRAMEWORK_DIR, "array.py"))
exceptions_module = load_module("dividebyzero_exceptions", os.path.join(FRAMEWORK_DIR, "exceptions.py"))
linalg_module = load_module("dividebyzero_linalg", os.path.join(FRAMEWORK_DIR, "linalg.py"))
logfuncs_module = load_module("dividebyzero_logfuncs", os.path.join(FRAMEWORK_DIR, "logarithmic_functions.py"))
powers_module = load_module("dividebyzero_powers", os.path.join(FRAMEWORK_DIR, "powers.py"))

# Import quantum modules
tensor_module = load_module("dividebyzero_quantum_tensor", 
                          os.path.join(FRAMEWORK_DIR, "quantum", "tensor.py"))
entropy_module = load_module("dividebyzero_quantum_entropy", 
                           os.path.join(FRAMEWORK_DIR, "quantum", "entropy.py"))
fractal_module = load_module("dividebyzero_quantum_fractal", 
                           os.path.join(FRAMEWORK_DIR, "quantum", "fractal.py"))

# Extract frequently used functions
DimensionalArray = array_module.DimensionalArray
array = array_module.array
DimensionalError = exceptions_module.DimensionalError
ReconstructionError = exceptions_module.ReconstructionError

# Set up test cases
print("Setting up test cases...")

# Test 1: Basic division by zero
print("\nTest 1: Basic division by zero")
a = array([1.0, 2.0, 3.0])
b = array([2.0, 0.0, 4.0])
result = a / b
print(f"a = {a.array}")
print(f"b = {b.array}")
print(f"a / b = {result.array}")
print(f"Result has error tracking: {hasattr(result, '_error_id')}")
print(f"Result shape: {result.shape}")

# Test 2: Logarithm of zero
print("\nTest 2: Logarithm of zero")
a = array([1.0, 0.0, 3.0])
log_a = logfuncs_module.log(a)
print(f"a = {a.array}")
print(f"log(a) = {log_a.array}")
print(f"Result has error tracking: {hasattr(log_a, '_error_id')}")
print(f"Result shape: {log_a.shape}")

# Test 3: Power operations at singularities
print("\nTest 3: Power operations at singularities")
print("Test 3.1: 0^0")
zero_to_zero = powers_module.power(array(0.0), array(0.0))
print(f"0^0 = {zero_to_zero.array}")

print("Test 3.2: 0^(-1)")
zero_to_neg = powers_module.power(array(0.0), array(-1.0))
print(f"0^(-1) = {zero_to_neg.array}")

print("Test 3.3: (-1)^(0.5)")
neg_to_frac = powers_module.power(array(-1.0), array(0.5))
print(f"(-1)^(0.5) = {neg_to_frac.array}")

# Test 4: Matrix operations with singularities
print("\nTest 4: Matrix operations with singularities")
print("Test 4.1: Matrix logarithm of a non-singular matrix")
A = array([[1.0, 2.0], [3.0, 4.0]])
logm_A = linalg_module.logm(A)
print(f"A = {A.array}")
print(f"logm(A) = {logm_A.array}")

print("Test 4.2: Matrix logarithm of a singular matrix")
B = array([[1.0, 2.0], [2.0, 4.0]])  # Singular matrix (det = 0)
logm_B = linalg_module.logm(B)
print(f"B = {B.array}")
print(f"logm(B) = {logm_B.array}")

print("Test 4.3: Matrix square root with negative eigenvalues")
C = array([[-1.0, 0.0], [0.0, 2.0]])  # Has one negative eigenvalue
sqrtm_C = linalg_module.sqrtm(C)
print(f"C = {C.array}")
print(f"sqrtm(C) = {sqrtm_C.array}")

# Test 5: Quantum tensor operations
print("\nTest 5: Quantum tensor operations")
print("Test 5.1: Quantum tensor division by zero")
qt = tensor_module.QuantumTensor(np.array([[1.0, 0.0], [0.0, 1.0]]))
qt_div = qt / 0
print(f"qt = {qt.array}")
print(f"qt / 0 = {qt_div.array}")
print(f"qt / 0 shape = {qt_div.shape}")

print("Test 5.2: Quantum tensor elevation")
qt_elevated = qt_div.elevate()
print(f"qt_elevated = {qt_elevated.array}")
print(f"qt_elevated shape = {qt_elevated.shape}")

# Test 6: Entropy calculations
print("\nTest 6: Entropy calculations")
print("Test 6.1: von Neumann entropy")
rho = fractal_module.QuantumDensityMatrix(np.array([[0.5, 0.0], [0.0, 0.5]]))
vn_entropy = entropy_module.von_neumann_entropy(rho)
print(f"rho = {rho.array}")
print(f"von Neumann entropy = {vn_entropy}")

print("Test 6.2: Rényi entropy")
renyi_ent = entropy_module.renyi_entropy(rho, alpha=2.0)
print(f"Rényi entropy (α=2) = {renyi_ent}")

print("Test 6.3: Entropy with zero eigenvalues")
rho_zero = fractal_module.QuantumDensityMatrix(np.array([[1.0, 0.0], [0.0, 0.0]]))
vn_entropy_zero = entropy_module.von_neumann_entropy(rho_zero)
print(f"rho_zero = {rho_zero.array}")
print(f"von Neumann entropy with zero eigenvalue = {vn_entropy_zero}")

print("\nAll tests completed successfully!")