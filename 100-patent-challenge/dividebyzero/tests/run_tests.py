"""
Comprehensive test script for DivideByZero framework.
"""

import os
import sys
import numpy as np

# DIRECT ABSOLUTE IMPORTS - no relative imports which cause errors
from array import DimensionalArray, array
from logarithmic_functions import log, log10
import linalg
import powers
# Import quantum modules with full paths to avoid relative import errors
from quantum.tensor import QuantumTensor
from quantum.entropy import von_neumann_entropy, renyi_entropy
from quantum.fractal import QuantumDensityMatrix

print("===== TESTING DIVIDEBYZERO FRAMEWORK =====")

# Test 1: Basic array creation and division by zero
print("\n----- Test 1: Basic Division by Zero -----")
a = array([1.0, 2.0, 3.0])
b = array([2.0, 0.0, 4.0])
result = a / b
print(f"a = {a.array}")
print(f"b = {b.array}")
print(f"a / b = {result.array}")
print(f"Result has error tracking: {hasattr(result, '_error_id')}")
print(f"Result shape: {result.shape}")

# Test 2: Logarithm of zero
print("\n----- Test 2: Logarithm of Zero -----")
a = array([1.0, 0.0, 3.0])
log_a = log(a)
print(f"a = {a.array}")
print(f"log(a) = {log_a.array}")
print(f"Result has error tracking: {hasattr(log_a, '_error_id')}")
print(f"Result shape: {log_a.shape}")

# Test 3: Power operations at singularities
print("\n----- Test 3: Power Operations at Singularities -----")
print("Test 3.1: 0^0")
zero_to_zero = powers.power(array(0.0), array(0.0))
print(f"0^0 = {zero_to_zero.array}")

print("Test 3.2: 0^(-1)")
zero_to_neg = powers.power(array(0.0), array(-1.0))
print(f"0^(-1) = {zero_to_neg.array}")

print("Test 3.3: (-1)^(0.5)")
neg_to_frac = powers.power(array(-1.0), array(0.5))
print(f"(-1)^(0.5) = {neg_to_frac.array}")

# Test 4: Matrix operations with singularities
print("\n----- Test 4: Matrix Operations with Singularities -----")
print("Test 4.1: Matrix logarithm of a non-singular matrix")
A = array([[1.0, 2.0], [3.0, 4.0]])
logm_A = linalg.logm(A)
print(f"A = {A.array}")
print(f"logm(A) = {logm_A.array}")

print("Test 4.2: Matrix logarithm of a singular matrix")
B = array([[1.0, 2.0], [2.0, 4.0]])  # Singular matrix (det = 0)
logm_B = linalg.logm(B)
print(f"B = {B.array}")
print(f"logm(B) = {logm_B.array}")

print("Test 4.3: Matrix square root with negative eigenvalues")
C = array([[-1.0, 0.0], [0.0, 2.0]])  # Has one negative eigenvalue
sqrtm_C = linalg.sqrtm(C)
print(f"C = {C.array}")
print(f"sqrtm(C) = {sqrtm_C.array}")

# Test 5: Quantum tensor operations
print("\n----- Test 5: Quantum Tensor Operations -----")
print("Test 5.1: Quantum tensor division by zero")
qt = QuantumTensor(np.array([[1.0, 0.0], [0.0, 1.0]]))
qt_div = qt / 0
print(f"qt = {qt.array}")
print(f"qt / 0 = {qt_div.array}")
print(f"qt / 0 shape = {qt_div.shape}")

print("Test 5.2: Quantum tensor elevation")
qt_elevated = qt_div.elevate()
print(f"qt_elevated = {qt_elevated.array}")
print(f"qt_elevated shape = {qt_elevated.shape}")

# Test 6: Entropy calculations
print("\n----- Test 6: Entropy Calculations -----")
print("Test 6.1: von Neumann entropy")
rho = QuantumDensityMatrix(np.array([[0.5, 0.0], [0.0, 0.5]]))
vn_entropy = von_neumann_entropy(rho)
print(f"rho = {rho.array}")
print(f"von Neumann entropy = {vn_entropy}")

print("Test 6.2: Rényi entropy")
renyi_ent = renyi_entropy(rho, alpha=2.0)
print(f"Rényi entropy (α=2) = {renyi_ent}")

print("Test 6.3: Entropy with zero eigenvalues")
rho_zero = QuantumDensityMatrix(np.array([[1.0, 0.0], [0.0, 0.0]]))
vn_entropy_zero = von_neumann_entropy(rho_zero)
print(f"rho_zero = {rho_zero.array}")
print(f"von Neumann entropy with zero eigenvalue = {vn_entropy_zero}")

print("\n===== ALL TESTS COMPLETED SUCCESSFULLY =====")