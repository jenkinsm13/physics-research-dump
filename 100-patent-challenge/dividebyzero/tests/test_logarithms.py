import numpy as np
import pytest
from dividebyzero.array import DimensionalArray
from dividebyzero.logarithms import (
    log, log2, log10, logm, log_boundary, 
    quantum_log
)


def test_log_with_zeros():
    """Test logarithm with zeros using dimensional division."""
    # Create array with zeros
    x = DimensionalArray(np.array([0, 1, 2, 3]))
    result = log(x)
    
    # Check that result exists and maintains shape
    assert result is not None
    assert result.array.shape == x.array.shape
    
    # Verify non-zero values are processed
    assert not np.isnan(result.array[1:]).any(), "Log of non-zero values should not be NaN"
    assert not np.isinf(result.array[1:]).any(), "Log of non-zero values should not be Inf"
    
    # Verify error tracking for zero
    assert hasattr(result, '_error_id')


def test_log_boundary_function():
    """Test explicit boundary transition operator."""
    # Test with zeros and infinities
    x = DimensionalArray(np.array([0, 1, 2, np.inf]))
    result = log_boundary(x)
    
    # Check result properties
    assert result is not None
    assert result.array.shape == x.array.shape
    
    # Check error tracking
    assert hasattr(result, '_error_id')
    
    # Verify standard logarithm for non-boundary elements
    np.testing.assert_allclose(
        result.array[1:2], 
        np.log(x.array[1:2])
    )


def test_simple_information_conservation():
    """Test basic information-preserving properties of logarithm."""
    # Create test array without zeros
    x = DimensionalArray(np.array([[1, 2], [3, 4]]))
    
    # Apply logarithm
    log_x = log(x)
    
    # Basic checks for information preservation
    assert log_x.array.shape == x.array.shape
    assert not np.isnan(log_x.array).any()
    assert not np.isinf(log_x.array).any()
    
    # Verify log values are increasing when input values increase
    assert np.all(np.diff(log_x.array.flatten()) > 0)


def test_simple_group_structure():
    """Test basic group structure properties of logarithm."""
    # Create simple test arrays
    x = DimensionalArray(np.array([1, 2, 3]))
    y = DimensionalArray(np.array([2, 3, 4]))
    
    # Calculate log(x * y) and log(x) + log(y)
    product = x * y
    log_product = log(product)
    log_sum = log(x) + log(y)
    
    # Check basic group property: log(a*b) ≈ log(a) + log(b)
    # Use a relaxed tolerance for numerical precision
    np.testing.assert_allclose(
        log_product.array,
        log_sum.array,
        rtol=1e-5  # Relative tolerance
    )


def test_quantum_log():
    """Test quantum logarithm with density matrix."""
    # Skip if quantum submodule not available
    try:
        from dividebyzero.quantum.tensor import quantum_decomposition
    except ImportError:
        pytest.skip("Quantum module not available")
    
    # Create density matrix (must be Hermitian and positive semi-definite)
    density_matrix = np.array([[0.8, 0.1], [0.1, 0.2]])
    x = DimensionalArray(density_matrix)
    
    # Apply quantum logarithm
    result = quantum_log(x)
    
    # Check result properties
    assert result is not None
    assert result.array.shape == x.array.shape
    
    # Verify result is still Hermitian 
    diff = result.array - result.array.conj().T
    assert np.allclose(diff, 0, atol=1e-8)


def test_logm_with_singular_matrix():
    """Test matrix logarithm with singular matrix."""
    # Create singular matrix
    singular_matrix = np.array([[1, 0], [0, 0]])
    x = DimensionalArray(singular_matrix)
    
    # Apply matrix logarithm
    result = logm(x)
    
    # Check result properties
    assert result is not None
    assert result.array.shape == x.array.shape
    
    # Verify error tracking for singularity
    assert hasattr(result, '_error_id')


def test_log2_and_log10():
    """Test base-2 and base-10 logarithms."""
    x = DimensionalArray(np.array([1, 2, 4, 8]))
    
    # Test log2
    log2_result = log2(x)
    np.testing.assert_allclose(
        log2_result.array,
        np.array([0, 1, 2, 3])
    )
    
    # Test log10
    log10_result = log10(x)
    np.testing.assert_allclose(
        log10_result.array,
        np.log10(x.array)
    ) 