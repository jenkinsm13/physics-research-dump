 # Create new test file to verify all matrix functions handle singularities properly

import numpy as np
import dividebyzero as dbz

def test_matrix_exponential_singularity_handling():
    """Test that matrix exponential properly handles edge cases."""
    
    # Create a matrix with extremely large eigenvalues
    A = np.diag([1000, -500, 300])
    
    # This should succeed with dimensional handling
    result = dbz.linalg.expm(A)
    
    # Verify it's a DimensionalArray
    assert isinstance(result, dbz.array.DimensionalArray)
    
    # Test that the exponential followed by logarithm recovers original
    log_result = dbz.linalg.logm(result)
    
    # Should be approximately equal to original
    assert np.allclose(log_result.array, A, rtol=1e-10)

def test_matrix_function_consistency():
    """Test consistency between direct and composition approaches."""
    
    # Create a test matrix
    A = np.array([[1.0, 0.5], [0.5, 2.0]])
    
    # Test that sin²(A) + cos²(A) ≈ I
    sin_A = dbz.linalg.sinm(A)
    cos_A = dbz.linalg.cosm(A)
    
    identity = sin_A @ sin_A + cos_A @ cos_A
    
    # Should approximate identity matrix
    assert np.allclose(identity.array, np.eye(2), rtol=1e-10)