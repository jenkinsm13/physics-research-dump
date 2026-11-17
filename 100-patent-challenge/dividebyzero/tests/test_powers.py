"""
Unit tests for power operations in DivideByZero framework.
"""

import pytest
import numpy as np
import dividebyzero as dbz

def test_basic_power():
    """Test basic power operations with non-singular cases."""
    x = dbz.array([1.0, 2.0, 3.0])
    y = x ** 2
    assert np.allclose(y.array, np.array([1.0, 4.0, 9.0]))

def test_zero_power():
    """Test power operations with zero base."""
    x = dbz.array([0.0, 1.0, 2.0])
    
    # 0^0 should be 1 by convention
    y = x ** 0
    assert np.allclose(y.array, np.array([1.0, 1.0, 1.0]))
    
    # 0^2 should be 0
    y = x ** 2
    assert np.allclose(y.array, np.array([0.0, 1.0, 4.0]))
    
    # 0^(-1) should be handled by dimensional reduction
    y = x ** (-1)
    # Check non-zero elements
    assert np.allclose(y.array[1:], np.array([1.0, 0.5]))
    # First element should be finite (regularized)
    assert np.isfinite(y.array[0])

def test_negative_base():
    """Test power with negative base."""
    x = dbz.array([-1.0, -2.0, 2.0])
    
    # Integer powers should work normally
    y = x ** 2
    assert np.allclose(y.array, np.array([1.0, 4.0, 4.0]))
    
    # Non-integer powers with negative base should use dimensional reduction
    y = x ** 0.5
    # Check positive elements
    assert np.allclose(y.array[2:], np.array([np.sqrt(2.0)]))
    # Check negative elements are handled properly
    assert np.isfinite(y.array[0])
    assert np.isfinite(y.array[1])

def test_matrix_power():
    """Test matrix power operations."""
    A = dbz.array([[1.0, 2.0], [3.0, 4.0]])
    
    # Integer power
    B = dbz.matrix_power(A, 2)
    expected = np.array([[7.0, 10.0], [15.0, 22.0]])
    assert np.allclose(B.array, expected)
    
    # Zero power
    C = dbz.matrix_power(A, 0)
    assert np.allclose(C.array, np.eye(2))
    
    # Negative power
    D = dbz.matrix_power(A, -1)
    expected_inv = np.array([[-2.0, 1.0], [1.5, -0.5]])
    assert np.allclose(D.array, expected_inv)

def test_singular_matrix_power():
    """Test power operations with singular matrices."""
    # Singular matrix
    A = dbz.array([[1.0, 0.0], [0.0, 0.0]])
    
    # For singular matrix, A^0 should be regularized identity
    B = dbz.matrix_power(A, 0)
    assert np.allclose(B.array, np.eye(2))
    
    # For singular matrix, A^(-1) should use regularization
    C = dbz.matrix_power(A, -1)
    # Result should be finite
    assert np.all(np.isfinite(C.array))
    # A * A^(-1) should approximate identity for non-zero elements
    approx_identity = A.array @ C.array
    assert np.isclose(approx_identity[0, 0], 1.0)

# Add tests for quantum_power as well