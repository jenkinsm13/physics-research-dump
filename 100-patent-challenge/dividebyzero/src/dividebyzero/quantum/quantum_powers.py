"""
Quantum power operations for DivideByZero framework.

Implements power operations specific to quantum tensors, preserving
quantum mechanical properties and handling singular cases.
"""

import numpy as np
from typing import Optional, Union
from ..array import DimensionalArray
from .tensor import QuantumTensor, EntanglementSpectrum

def quantum_power(tensor, p):
    """
    Compute power of quantum tensor with singularity handling.
    
    For density matrices, uses spectral decomposition.
    For unitary operators, uses efficient exponentiation.
    
    Parameters:
        tensor: QuantumTensor input
        p: Power (scalar)
        
    Returns:
        QuantumTensor: Tensor raised to power p with singularity handling
    """
    from .tensor import QuantumTensor
    
    if not isinstance(tensor, QuantumTensor):
        raise TypeError("Input must be a QuantumTensor")
    
    # Check if the tensor represents a unitary operator
    # Use proper dimensional analysis instead of arbitrary thresholds
    product = tensor.data @ tensor.data.conj().T
    identity = np.eye(tensor.data.shape[0])
    # For exact unitarity, U†U = I; for numerical stability, use relative error analysis
    difference = product - identity
    relative_error = np.max(np.abs(difference)) / (np.max(np.abs(product)) + np.max(np.abs(identity)))
    is_unitary = relative_error < np.finfo(float).eps * 100
    
    if is_unitary:
        # For unitary operators, use efficient algorithm based on eigendecomposition
        eigvals, eigvecs = np.linalg.eigh(tensor.data)
        eigvals_power = np.power(eigvals, p)
        result = eigvecs @ np.diag(eigvals_power) @ eigvecs.conj().T
    else:
        # For general operators, use SVD-based approach
        U, s, Vh = np.linalg.svd(tensor.data, full_matrices=False)
        
        # Handle singular values using proper dimensional reduction
        from ..registry import ErrorData
        
        # Create proper error tracking
        error_data = ErrorData(
            original_shape=tensor.data.shape,
            error_tensor=s,
            reduction_type='quantum_power_svd',
            manifold_data={'power': p, 'singular_values': s}
        )
        error_id = tensor.error_registry.store(error_data)
        
        # Use proper framework power operation to handle singularities
        from ..powers import power as framework_power
        
        # Convert singular values to DimensionalArray for proper handling
        s_dim = DimensionalArray(s, tensor.error_registry)
        s_dim._error_id = error_id
        
        # Compute power using the framework's power operation
        # This ensures proper handling of zero/small singular values
        s_power_dim = framework_power(s_dim, p)
        s_power = s_power_dim.array
        
        # Reconstruct
        result = U @ np.diag(s_power) @ Vh
    
    return QuantumTensor(result, tensor.physical_dims, tensor.quantum_nums)