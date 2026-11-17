"""Tests for the quantum_powers module."""
import pytest
import numpy as np
from dividebyzero.quantum import QuantumTensor
from dividebyzero.quantum.quantum_powers import quantum_power
from dividebyzero import array

@pytest.fixture
def unitary_tensor():
    """Create a test unitary quantum tensor."""
    # Create a unitary matrix using a rotation
    theta = np.pi / 4
    unitary = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]
    ])
    return QuantumTensor(unitary, physical_dims=(2, 2))

@pytest.fixture
def general_tensor():
    """Create a test general quantum tensor."""
    # Non-unitary tensor
    data = np.array([
        [1.0, 0.5],
        [0.5, 2.0]
    ])
    return QuantumTensor(data, physical_dims=(2, 2))

@pytest.fixture
def singular_tensor():
    """Create a test singular quantum tensor."""
    # Singular matrix with zero eigenvalue
    data = np.array([
        [1.0, 2.0],
        [0.5, 1.0]
    ])
    return QuantumTensor(data, physical_dims=(2, 2))

def test_quantum_power_unitary(unitary_tensor):
    """Test quantum power for unitary operators."""
    # Test integer powers
    for power in [1, 2, 3]:
        result = quantum_power(unitary_tensor, power)
        
        # Verify result is a QuantumTensor
        assert isinstance(result, QuantumTensor)
        
        # Verify shape is preserved
        assert result.data.shape == unitary_tensor.data.shape
        
        # For unitary operator U, U^n * U^(-n) should be close to identity
        inverse = quantum_power(unitary_tensor, -power)
        product = result.data @ inverse.data
        identity = np.eye(product.shape[0])
        assert np.allclose(product, identity, atol=1e-10)
        
    # Test fractional power
    sqrt_result = quantum_power(unitary_tensor, 0.5)
    # Squaring the sqrt should give back original
    squared = quantum_power(sqrt_result, 2)
    assert np.allclose(squared.data, unitary_tensor.data, atol=1e-10)

def test_quantum_power_general(general_tensor):
    """Test quantum power for general operators."""
    # Test integer powers
    for power in [1, 2, 3]:
        result = quantum_power(general_tensor, power)
        
        # Verify result is a QuantumTensor
        assert isinstance(result, QuantumTensor)
        
        # Verify shape is preserved
        assert result.data.shape == general_tensor.data.shape
        
        # For integer powers, we can verify by matrix multiplication
        expected = np.linalg.matrix_power(general_tensor.data, power)
        assert np.allclose(result.data, expected, atol=1e-10)
    
    # Test zero power (should give identity)
    zero_power = quantum_power(general_tensor, 0)
    assert np.allclose(zero_power.data, np.eye(general_tensor.data.shape[0]), atol=1e-10)
    
    # Test negative power
    neg_power = quantum_power(general_tensor, -1)
    # A^(-1) * A should be close to identity
    product = neg_power.data @ general_tensor.data
    assert np.allclose(product, np.eye(product.shape[0]), atol=1e-10)

def test_quantum_power_singular(singular_tensor):
    """Test quantum power for singular operators."""
    # Test power 1 (should return original)
    power_one = quantum_power(singular_tensor, 1)
    assert np.allclose(power_one.data, singular_tensor.data, atol=1e-10)
    
    # Test power 0 (should return identity-like)
    power_zero = quantum_power(singular_tensor, 0)
    assert np.allclose(power_zero.data, np.eye(singular_tensor.data.shape[0]), atol=1e-10)
    
    # Test negative power (should handle singularity)
    neg_power = quantum_power(singular_tensor, -1)
    # Check that we got a result without NaN or inf values
    assert not np.any(np.isnan(neg_power.data))
    assert not np.any(np.isinf(neg_power.data))
    
    # Test fractional power
    frac_power = quantum_power(singular_tensor, 0.5)
    # Check that we got a result without NaN or inf values
    assert not np.any(np.isnan(frac_power.data))
    assert not np.any(np.isinf(frac_power.data))

def test_quantum_power_error_handling():
    """Test error handling in quantum_power function."""
    # Test with non-QuantumTensor input
    non_quantum = array(np.eye(2))
    with pytest.raises(TypeError):
        quantum_power(non_quantum, 2)

def test_quantum_power_svd():
    """Test SVD-based quantum power approach."""
    # Create a tensor with known singular values
    s_values = np.array([2.0, 0.5])
    U = np.eye(2)
    Vh = np.eye(2)
    data = U @ np.diag(s_values) @ Vh
    tensor = QuantumTensor(data, physical_dims=(2, 2))
    
    # Test integer power
    power = 2
    result = quantum_power(tensor, power)
    
    # Expected: same eigenvectors with eigenvalues raised to power
    expected_s = s_values ** power
    expected = U @ np.diag(expected_s) @ Vh
    assert np.allclose(result.data, expected, atol=1e-10)
    
    # Test zero singular value handling
    tensor_with_zero = QuantumTensor(
        np.array([[1.0, 0.0], [0.0, 0.0]]),
        physical_dims=(2, 2)
    )
    result = quantum_power(tensor_with_zero, 2)
    # Result should have same zero pattern
    assert np.allclose(result.data, np.array([[1.0, 0.0], [0.0, 0.0]]), atol=1e-10)
    
    # Test negative power with zero singular value
    result = quantum_power(tensor_with_zero, -1)
    # Result should handle singularity without NaNs or infs
    assert not np.any(np.isnan(result.data))
    assert not np.any(np.isinf(result.data))

def test_quantum_power_preserves_properties():
    """Test that quantum_power preserves key quantum properties."""
    # Create a density matrix (positive semidefinite with trace 1)
    pure_state = np.array([[1], [0]])
    density = pure_state @ pure_state.T.conj()
    tensor = QuantumTensor(density, physical_dims=(2, 2))
    
    # Test various powers
    for power in [0.5, 1, 2]:
        result = quantum_power(tensor, power)
        
        # Density matrix properties:
        # 1. Hermitian (self-adjoint)
        assert np.allclose(result.data, result.data.conj().T, atol=1e-10)
        
        # 2. Positive semidefinite
        eigvals = np.linalg.eigvalsh(result.data)
        assert np.all(eigvals >= -1e-10)  # Allow for tiny numerical errors
        
        # 3. Trace close to 1 for some powers (trace may change for arbitrary powers)
        if power == 1:
            assert np.isclose(np.trace(result.data), 1.0, atol=1e-10) 