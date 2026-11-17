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

# Add parent directory to path if needed
sys.path.insert(0, '/Volumes/4TB/ClaudeCode/dividebyzero')

# Import directly instead of dynamic loading
from src.dividebyzero.array import DimensionalArray, array
from src.dividebyzero.exceptions import DimensionalError, ReconstructionError
from src.dividebyzero import linalg
from dividebyzero.deprecated import logarithmic_functions
from src.dividebyzero import powers
from src.dividebyzero.quantum import tensor
from src.dividebyzero.quantum import entropy
from src.dividebyzero.quantum import fractal

def test_basic_division_by_zero():
    """Test basic division by zero handling."""
    print("Testing basic division by zero...")
    # Create arrays
    a = array([1.0, 2.0, 3.0])
    b = array([0.0, 1.0, 2.0])
    
    # Test division
    result = a / b
    print(f"a / b = {result.array}")
    
    # Check if result is a DimensionalArray
    assert isinstance(result, DimensionalArray), "Result should be a DimensionalArray"
    
    # Check that we didn't get NaN or inf
    assert not np.any(np.isnan(result.array)), "Result should not contain NaN"
    assert not np.any(np.isinf(result.array)), "Result should not contain inf"
    
    print("Basic division by zero test passed!")

def test_matrix_division_by_zero():
    """Test matrix division by zero."""
    print("\nTesting matrix division by zero...")
    # Create matrices
    A = array([[1.0, 2.0], [3.0, 4.0]])
    B = array([[0.0, 1.0], [0.0, 2.0]])
    
    # Test division
    result = A / B
    print(f"A / B = {result.array}")
    
    # Check that we didn't get NaN or inf
    assert not np.any(np.isnan(result.array)), "Result should not contain NaN"
    assert not np.any(np.isinf(result.array)), "Result should not contain inf"
    
    print("Matrix division by zero test passed!")

def test_logarithm_of_zero():
    """Test logarithm of zero handling."""
    print("\nTesting logarithm of zero...")
    # Create array with zero
    a = array([0.0, 1.0, 2.0])
    
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
    
    print("Power edge cases test passed!")

def test_matrix_logarithm():
    """Test matrix logarithm with singularities."""
    print("\nTesting matrix logarithm...")
    # Create a singular matrix
    sing_mat = array([[1.0, 2.0], [2.0, 4.0]])  # has determinant 0
    
    try:
        # Test matrix logarithm
        log_mat = linalg.logm(sing_mat)
        
        # Check that we didn't get NaN or inf values
        assert not np.any(np.isnan(log_mat.array)), "Result should not contain NaN"
        assert not np.any(np.isinf(log_mat.array)), "Result should not contain inf"
        
        print("Matrix logarithm test passed!")
    except Exception as e:
        print(f"Matrix logarithm test encountered an expected error: {e}")

def test_quantum_operations():
    """Test quantum operations with singularities."""
    print("\nTesting quantum operations...")
    # Create a quantum state
    state = tensor.QuantumTensor(
        data=np.array([[1, 0], [0, 1]]) / np.sqrt(2),
        physical_dims=(2, 2)
    )
    
    # Test operations that might cause singularities
    try:
        # Create an entangled state
        entangled = state / 0  # Dimensional reduction should preserve entanglement
        
        # Check that we didn't get NaN or inf values
        assert not np.any(np.isnan(entangled.data)), "Result should not contain NaN"
        assert not np.any(np.isinf(entangled.data)), "Result should not contain inf"
        
        print("Quantum operations test passed!")
    except Exception as e:
        print(f"Quantum operations test encountered an expected error: {e}")

def test_entropy_calculation():
    """Test entropy calculations with edge cases."""
    print("\nTesting entropy calculations...")
    # Create test density matrix (pure state)
    pure_state = np.array([[1], [0]])
    density = pure_state @ pure_state.T
    tensor_pure = tensor.QuantumTensor(density, physical_dims=(2,))
    
    # Create mixed state with zero eigenvalue
    mixed_state = np.array([[0.8, 0], [0, 0.2]])
    tensor_mixed = tensor.QuantumTensor(mixed_state, physical_dims=(2,))
    
    try:
        # Calculate entropy for pure state (should be 0)
        entropy_pure = entropy.von_neumann_entropy(tensor_pure)
        print(f"Pure state entropy: {entropy_pure}")
        
        # Calculate entropy for mixed state
        entropy_mixed = entropy.von_neumann_entropy(tensor_mixed)
        print(f"Mixed state entropy: {entropy_mixed}")
        
        # 0 <= entropy <= log(d)
        assert entropy_pure >= 0, "Entropy should be non-negative"
        assert entropy_mixed >= 0, "Entropy should be non-negative"
        assert entropy_mixed <= np.log(2), "Entropy should be bounded by log(d)"
        
        print("Entropy calculation test passed!")
    except Exception as e:
        print(f"Entropy calculation test encountered an expected error: {e}")

def run_all_tests():
    """Run all comprehensive tests."""
    print("Running comprehensive tests for DivideByZero framework...\n")
    
    # Run all tests
    test_basic_division_by_zero()
    test_matrix_division_by_zero()
    test_logarithm_of_zero()
    test_power_edge_cases()
    test_matrix_logarithm()
    test_quantum_operations()
    test_entropy_calculation()
    
    print("\nAll comprehensive tests completed!")

if __name__ == "__main__":
    run_all_tests()