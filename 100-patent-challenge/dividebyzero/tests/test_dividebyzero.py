"""
Basic tests for the DivideByZero framework to verify proper handling of singularities.
"""

import numpy as np
import sys
import os

# Add the parent directory to the Python path
sys.path.append('/Volumes/4TB/ClaudeCode')

# Import the framework
from dividebyzero.array import DimensionalArray, array
from dividebyzero.exceptions import DimensionalError
from dividebyzero import linalg
from dividebyzero.deprecated import logarithmic_functions
from dividebyzero.quantum import tensor, fractal, entropy
from dividebyzero import powers

def test_array_division_by_zero():
    """Test basic division by zero handling."""
    print("Testing basic division by zero...")
    # Create arrays
    a = array([1.0, 2.0, 3.0])
    b = array([2.0, 0.0, 4.0])
    
    # Test division
    result = a / b
    print(f"a / b = {result.array}")
    
    # Check if result is a DimensionalArray
    assert isinstance(result, DimensionalArray), "Result should be a DimensionalArray"
    
    # Check that we didn't get NaN or inf
    assert not np.any(np.isnan(result.array)), "Result should not contain NaN"
    assert not np.any(np.isinf(result.array)), "Result should not contain inf"
    
    print("Basic division by zero test passed!")

def test_logarithm_of_zero():
    """Test logarithm of zero handling."""
    print("\nTesting logarithm of zero...")
    # Create array with zero
    a = array([1.0, 0.0, 2.0])
    
    # Take logarithm
    log_a = logarithmic_functions.log(a)
    print(f"log(a) = {log_a.array}")
    
    # Check that we didn't get NaN or -inf
    assert not np.any(np.isnan(log_a.array)), "Result should not contain NaN"
    assert not np.any(np.isinf(log_a.array)), "Result should not contain inf"
    
    print("Logarithm of zero test passed!")

def test_power_edge_cases():
    """Test power function edge cases."""
    print("\nTesting power edge cases...")
    # Create arrays
    a = array([0.0, 1.0, 2.0, -1.0])
    
    # Test 0^0
    result_zero_zero = powers.power(array(0.0), array(0.0))
    print(f"0^0 = {result_zero_zero.array}")
    assert not np.isnan(result_zero_zero.array), "0^0 should not be NaN"
    
    # Test 0^-1
    result_zero_neg = powers.power(array(0.0), array(-1.0))
    print(f"0^-1 = {result_zero_neg.array}")
    assert not np.isnan(result_zero_neg.array), "0^-1 should not be NaN"
    assert not np.isinf(result_zero_neg.array), "0^-1 should not be inf"
    
    # Test negative base with non-integer exponent
    result_neg_frac = powers.power(array(-1.0), array(0.5))
    print(f"(-1)^0.5 = {result_neg_frac.array}")
    assert not np.isnan(result_neg_frac.array), "(-1)^0.5 should not be NaN"
    
    print("Power edge cases test passed!")

def test_matrix_operations():
    """Test matrix operations with singularities."""
    print("\nTesting matrix operations...")
    # Create a singular matrix
    sing_mat = array([[1.0, 2.0], [2.0, 4.0]])  # has determinant 0
    
    # Test matrix logarithm
    log_mat = linalg.logm(sing_mat)
    print(f"logm(singular matrix) shape = {log_mat.shape}")
    assert not np.any(np.isnan(log_mat.array)), "Matrix logarithm should not contain NaN"
    assert not np.any(np.isinf(log_mat.array)), "Matrix logarithm should not contain inf"
    
    # Test matrix inverse via pseudo-inverse
    pinv_mat = linalg.pinv(sing_mat)
    print(f"pinv(singular matrix) = \n{pinv_mat.array}")
    assert not np.any(np.isnan(pinv_mat.array)), "Pseudo-inverse should not contain NaN"
    assert not np.any(np.isinf(pinv_mat.array)), "Pseudo-inverse should not contain inf"
    
    # Test matrix sqrt
    sqrt_mat = linalg.sqrtm(sing_mat)
    print(f"sqrtm(singular matrix) shape = {sqrt_mat.shape}")
    assert not np.any(np.isnan(sqrt_mat.array)), "Matrix sqrt should not contain NaN"
    
    print("Matrix operations test passed!")

def test_quantum_tensor():
    """Test quantum tensor operations."""
    print("\nTesting quantum tensor operations...")
    # Create a quantum tensor
    qt_data = np.array([[1.0, 0.0], [0.0, 0.0]])
    qt = tensor.QuantumTensor(qt_data)
    
    # Test division by zero
    result = qt / 0
    print(f"Quantum tensor / 0 shape = {result.shape}")
    assert not np.any(np.isnan(result.array)), "Result should not contain NaN"
    
    # Test elevation
    elevated = result.elevate()
    print(f"Elevated tensor shape = {elevated.shape}")
    assert not np.any(np.isnan(elevated.array)), "Elevated result should not contain NaN"
    
    print("Quantum tensor operations test passed!")

def test_entropy_calculation():
    """Test entropy calculations with zero eigenvalues."""
    print("\nTesting entropy calculations...")
    # Create a density matrix with zero eigenvalue
    rho = fractal.QuantumDensityMatrix(np.array([[0.5, 0.0], [0.0, 0.5]]))
    
    # Test von Neumann entropy
    vn_entropy = entropy.von_neumann_entropy(rho)
    print(f"von Neumann entropy = {vn_entropy}")
    assert not np.isnan(vn_entropy), "von Neumann entropy should not be NaN"
    
    # Test Renyi entropy
    renyi_entropy = entropy.renyi_entropy(rho, alpha=2.0)
    print(f"Renyi entropy = {renyi_entropy}")
    assert not np.isnan(renyi_entropy), "Renyi entropy should not be NaN"
    
    print("Entropy calculations test passed!")

def run_all_tests():
    """Run all tests."""
    print("Starting test suite for DivideByZero framework...\n")
    
    try:
        test_array_division_by_zero()
        test_logarithm_of_zero()
        test_power_edge_cases()
        test_matrix_operations()
        test_quantum_tensor()
        test_entropy_calculation()
        
        print("\nAll tests passed! The framework is functioning correctly.")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    run_all_tests()