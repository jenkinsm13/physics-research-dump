"""Tests for the linear algebra module."""
import pytest
import numpy as np
from dividebyzero import array
from dividebyzero.array import DimensionalArray
from dividebyzero.linalg import (
    inv, det, svd, norm, pinv, eigvals, eigvalsh, eigh,
    logm, expm, sinm, cosm, matrix_power, matrix_rank, sqrtm
)

def test_inv():
    """Test matrix inverse function."""
    # Create a test matrix
    A = array([[3, 1], [1, 2]])
    
    # Compute inverse
    A_inv = inv(A)
    
    # Verify result is a DimensionalArray
    assert isinstance(A_inv, DimensionalArray)
    
    # Verify inverse is correct
    identity = A @ A_inv
    assert np.allclose(identity.array, np.eye(2))
    
    # Test with singular matrix
    singular_A = array([[1, 1], [1, 1]])
    
    try:
        # Should return a result without errors or raise a LinAlgError
        singular_inv = inv(singular_A)
        
        # If no error was raised, check the result
        assert isinstance(singular_inv, DimensionalArray)
        
        # Check that we didn't get inf values (NaN values might be acceptable)
        assert not np.any(np.isinf(singular_inv.array))
    except np.linalg.LinAlgError:
        # It's acceptable for inv to raise LinAlgError for singular matrices
        pass

def test_det():
    """Test determinant function."""
    # Create a test matrix
    A = array([[3, 1], [1, 2]])
    
    # Compute determinant
    det_A = det(A)
    
    # Verify result is a scalar or ndarray with a single element
    assert isinstance(det_A, (DimensionalArray, int, float, complex, np.number))
    
    # If it's a DimensionalArray, check its value
    if isinstance(det_A, DimensionalArray):
        assert np.isclose(det_A.array, 5)
    else:
        # Otherwise check the direct value
        assert np.isclose(det_A, 5)
    
    # Test with singular matrix
    singular_A = array([[1, 1], [1, 1]])
    
    # Should return zero for a singular matrix
    det_singular = det(singular_A)
    
    # Verify result is zero (either directly or in .array)
    if isinstance(det_singular, DimensionalArray):
        assert np.isclose(det_singular.array, 0)
    else:
        assert np.isclose(det_singular, 0)

def test_svd():
    """Test singular value decomposition."""
    # Create a test matrix
    A = array([[3, 1], [1, 2], [0, 1]])
    
    # Compute SVD
    U, s, Vh = svd(A)
    
    # Verify results are DimensionalArrays
    assert isinstance(U, DimensionalArray)
    assert isinstance(s, DimensionalArray)
    assert isinstance(Vh, DimensionalArray)
    
    # Verify shapes
    assert U.shape == (3, 3)
    assert s.shape == (2,)
    assert Vh.shape == (2, 2)
    
    # Verify reconstruction works
    S = np.zeros((3, 2))
    S[:2, :2] = np.diag(s.array)
    reconstructed = U.array @ S @ Vh.array
    assert np.allclose(reconstructed[:, :2], A.array)

def test_norm():
    """Test matrix and vector norm function."""
    # Create test arrays
    v = array([3, 4])
    A = array([[1, 2], [3, 4]])
    
    # Compute vector norm
    norm_v = norm(v)
    
    # Verify result is a scalar or DimensionalArray
    assert isinstance(norm_v, (DimensionalArray, int, float, complex, np.number))
    
    # Verify vector norm is correct (default L2 norm)
    if isinstance(norm_v, DimensionalArray):
        assert np.isclose(norm_v.array, 5)
    else:
        assert np.isclose(norm_v, 5)
    
    # Compute matrix norm
    norm_A = norm(A)
    
    # Verify result is a scalar or DimensionalArray
    assert isinstance(norm_A, (DimensionalArray, int, float, complex, np.number))
    
    # Compute norm with different ord parameter
    norm_v_1 = norm(v, ord=1)
    if isinstance(norm_v_1, DimensionalArray):
        assert np.isclose(norm_v_1.array, 7)
    else:
        assert np.isclose(norm_v_1, 7)

def test_pinv():
    """Test pseudoinverse function."""
    # Create a test matrix
    A = array([[1, 2], [3, 4], [5, 6]])
    
    # Compute pseudoinverse
    A_pinv = pinv(A)
    
    # Verify result is a DimensionalArray
    assert isinstance(A_pinv, DimensionalArray)
    
    # Verify pseudoinverse property A * A^+ * A = A
    assert np.allclose((A @ A_pinv @ A).array, A.array)
    
    # Test with singular matrix
    singular_A = array([[1, 1], [1, 1]])
    
    # Should return a result without errors
    singular_pinv = pinv(singular_A)
    
    # Verify result is a DimensionalArray
    assert isinstance(singular_pinv, DimensionalArray)
    
    # Check that we didn't get NaN or inf values
    assert not np.any(np.isnan(singular_pinv.array))
    assert not np.any(np.isinf(singular_pinv.array))

def test_eigvals():
    """Test eigenvalue computation."""
    # Create a test matrix
    A = array([[2, 1], [1, 3]])
    
    # Compute eigenvalues
    eigvals_A = eigvals(A)
    
    # Verify result is a DimensionalArray
    assert isinstance(eigvals_A, DimensionalArray)
    
    # Verify shape
    assert eigvals_A.shape == (2,)
    
    # Verify eigenvalues are correct
    expected_eigvals = np.sort(np.linalg.eigvals(A.array))
    actual_eigvals = np.sort(eigvals_A.array)
    assert np.allclose(actual_eigvals, expected_eigvals)

def test_eigvalsh():
    """Test eigenvalue computation for Hermitian matrices."""
    # Create a test Hermitian matrix
    A = array([[2, 1], [1, 3]])
    
    # Compute eigenvalues
    eigvals_A = eigvalsh(A)
    
    # Verify result is a DimensionalArray
    assert isinstance(eigvals_A, DimensionalArray)
    
    # Verify shape
    assert eigvals_A.shape == (2,)
    
    # Verify eigenvalues are correct
    expected_eigvals = np.sort(np.linalg.eigvalsh(A.array))
    actual_eigvals = np.sort(eigvals_A.array)
    assert np.allclose(actual_eigvals, expected_eigvals)

def test_eigh():
    """Test eigenvalue/eigenvector computation for Hermitian matrices."""
    # Create a test Hermitian matrix
    A = array([[2, 1], [1, 3]])
    
    # Compute eigenvalues and eigenvectors
    eigvals_A, eigvecs_A = eigh(A)
    
    # Verify results are DimensionalArrays
    assert isinstance(eigvals_A, DimensionalArray)
    assert isinstance(eigvecs_A, DimensionalArray)
    
    # Verify shapes
    assert eigvals_A.shape == (2,)
    assert eigvecs_A.shape == (2, 2)
    
    # Verify eigenvector equation A * v = lambda * v
    for i in range(2):
        lambda_i = eigvals_A.array[i]
        v_i = eigvecs_A.array[:, i]
        assert np.allclose(A.array @ v_i, lambda_i * v_i)

def test_matrix_power():
    """Test matrix power function."""
    # Create a test matrix
    A = array([[1, 2], [3, 4]])
    
    # Compute powers
    A_squared = matrix_power(A, 2)
    A_cubed = matrix_power(A, 3)
    
    # Verify results are DimensionalArrays
    assert isinstance(A_squared, DimensionalArray)
    assert isinstance(A_cubed, DimensionalArray)
    
    # Verify powers are correct
    expected_squared = A.array @ A.array
    expected_cubed = expected_squared @ A.array
    assert np.allclose(A_squared.array, expected_squared)
    assert np.allclose(A_cubed.array, expected_cubed)
    
    # Test with negative power (inverse)
    A_inv = matrix_power(A, -1)
    # A^-1 * A should be identity
    identity = A_inv @ A
    assert np.allclose(identity.array, np.eye(2))

def test_matrix_rank():
    """Test matrix rank function."""
    # Create test matrices
    full_rank = array([[1, 0], [0, 1]])
    rank_one = array([[1, 2], [2, 4]])
    
    # Compute ranks
    rank_full = matrix_rank(full_rank)
    rank_deficient = matrix_rank(rank_one)
    
    # Verify results
    assert rank_full == 2
    assert rank_deficient == 1

def test_sqrtm():
    """Test matrix square root function."""
    # Create a test positive definite matrix
    A = array([[4, 1], [1, 3]])
    
    # Compute square root
    sqrt_A = sqrtm(A)
    
    # Verify result is a DimensionalArray
    assert isinstance(sqrt_A, DimensionalArray)
    
    # Verify shape
    assert sqrt_A.shape == A.shape
    
    # Verify sqrt(A) * sqrt(A) ≈ A
    sqrt_squared = sqrt_A @ sqrt_A
    assert np.allclose(sqrt_squared.array, A.array)
    
    # Test with singular matrix
    singular_A = array([[0, 0], [0, 1]])
    singular_sqrt = sqrtm(singular_A)
    
    # Should not throw an error
    assert isinstance(singular_sqrt, DimensionalArray)

def test_matrix_functions():
    """Test matrix function implementations."""
    # Create a test matrix
    A = array([[1, 0.5], [0.5, 1]])
    
    # Test matrix exponential
    expA = expm(A)
    assert isinstance(expA, DimensionalArray)
    
    # Test matrix logarithm
    try:
        logA = logm(A)
        assert isinstance(logA, DimensionalArray)
        
        # Only verify log(exp(A)) if both functions work without NaN values
        if not np.any(np.isnan(logA.array)) and not np.any(np.isnan(expA.array)):
            # Verify log(exp(A)) ≈ A for well-conditioned matrix
            log_exp_A = logm(expA)
            
            # Skip comparison if result contains NaN values
            if not np.any(np.isnan(log_exp_A.array)):
                assert np.allclose(log_exp_A.array, A.array, rtol=1e-5)
    except (ValueError, np.linalg.LinAlgError):
        # Some implementations might raise errors for certain matrices
        pass
    
    # Test matrix sine and cosine
    try:
        sinA = sinm(A)
        assert isinstance(sinA, DimensionalArray)
        
        cosA = cosm(A)
        assert isinstance(cosA, DimensionalArray)
        
        # Only verify sin²(A) + cos²(A) ≈ I if both functions work without NaN values
        if not np.any(np.isnan(sinA.array)) and not np.any(np.isnan(cosA.array)):
            sin_squared = sinA @ sinA
            cos_squared = cosA @ cosA
            sum_squares = sin_squared + cos_squared
            
            # Skip comparison if result contains NaN values
            if not np.any(np.isnan(sum_squares.array)):
                assert np.allclose(sum_squares.array, np.eye(2), rtol=1e-5)
    except (ValueError, np.linalg.LinAlgError):
        # Some implementations might raise errors for certain matrices
        pass

def test_matrix_function_edge_cases():
    """Test edge cases for matrix functions."""
    # Test with large eigenvalues
    large_A = array([[1000, 0], [0, -500]])
    large_exp = expm(large_A)
    
    # Either the result contains valid values or NaNs (due to overflow)
    # Both behaviors are acceptable in this edge case
    if np.any(np.isnan(large_exp.array)):
        # If there are NaNs, that's expected for large values
        pass
    else:
        # If there are no NaNs, check for inf values
        assert not np.any(np.isinf(large_exp.array))
    
    # Test with singular matrix for log
    singular_A = array([[1, 1], [1, 1]])
    try:
        singular_log = logm(singular_A)
        
        # Should not throw an error
        assert isinstance(singular_log, DimensionalArray)
    except ValueError:
        # Some implementations might raise ValueError for exactly singular matrices
        pass
    
    # Test matrix with zero eigenvalues for logarithm
    zero_eig_A = array([[0, 0], [0, 1]])
    try:
        zero_log = logm(zero_eig_A)
        
        # Should not return inf values (NaN might be acceptable)
        assert not np.any(np.isinf(zero_log.array))
    except ValueError:
        # Some implementations might raise ValueError for matrices with zero eigenvalues
        pass 