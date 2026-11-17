"""
Power operations module for DivideByZero framework.

This module implements various power functions with dimensional reduction
capabilities for handling singularities such as 0^0, negative bases with
non-integer exponents, and singular matrix powers.
"""

import numpy as np
from typing import Optional, Tuple, Union
from .array import DimensionalArray
from .registry import ErrorData
from .exceptions import DimensionalError

def power(x, p, handle_indeterminate=True):
    """
    Compute element-wise power with singularity handling.
    
    Parameters:
        x: DimensionalArray base or scalar
        p: DimensionalArray or scalar exponent
        handle_indeterminate: Whether to handle indeterminate forms
        
    Returns:
        DimensionalArray: Result with dimensional reduction at singularities
    """
    from .array import DimensionalArray
    
    # Handle scalar base raised to DimensionalArray power (for __rpow__ support)
    if not isinstance(x, DimensionalArray) and isinstance(p, DimensionalArray):
        # Convert scalar to array for consistent handling
        x_scalar = x
        x = DimensionalArray(np.full_like(p.array, x_scalar), p.error_registry)
        
        # Handle special cases efficiently
        if x_scalar == 0:
            # 0^p: 0 for p>0, 1 for p=0, dimensional reduction for p<0
            result = np.zeros_like(p.array, dtype=float)
            zero_mask = (p.array == 0)
            pos_mask = (p.array > 0)
            neg_mask = (p.array < 0)
            
            result[zero_mask] = 1.0  # 0^0 = 1
            result[pos_mask] = 0.0   # 0^positive = 0
            
            # For negative exponents, use dimensional reduction
            if np.any(neg_mask):
                # Create error data for tracking
                error_data = ErrorData(
                    original_shape=p.array.shape,
                    error_tensor=neg_mask.astype(float),
                    reduction_type='power_convention',
                    manifold_data={'base': 0.0, 'negative_exponents': True}
                )
                error_id = p.error_registry.store(error_data)
                
                # Use small values that preserve dimensional relationships
                result[neg_mask] = np.finfo(float).eps
                
                # Return with proper error tracking
                power_result = DimensionalArray(result, p.error_registry)
                power_result._error_id = error_id
                return power_result
            
            return DimensionalArray(result, p.error_registry)
        
        elif x_scalar == 1:
            # 1^anything = 1
            return DimensionalArray(np.ones_like(p.array), p.error_registry)
        
        elif x_scalar < 0:
            # Handle negative base with non-integer exponents
            result = np.zeros_like(p.array, dtype=complex)
            integer_mask = np.array([float(p_val).is_integer() for p_val in p.array.flat]).reshape(p.array.shape)
            non_integer_mask = ~integer_mask
            
            # For integer exponents, compute directly
            result[integer_mask] = x_scalar ** p.array[integer_mask]
            
            # For non-integer exponents, use complex domain
            if np.any(non_integer_mask):
                # Track these special cases
                error_data = ErrorData(
                    original_shape=p.array.shape,
                    error_tensor=non_integer_mask.astype(float),
                    reduction_type='complex_power',
                    manifold_data={'negative_base': x_scalar}
                )
                error_id = p.error_registry.store(error_data)
                
                # Compute in complex domain: (-a)^b = |a|^b * exp(i*π*b)
                result[non_integer_mask] = (abs(x_scalar) ** p.array[non_integer_mask]) * np.exp(1j * np.pi * p.array[non_integer_mask])
                
                # If result is all real, convert back to real domain
                if np.all(np.imag(result) == 0):
                    result = np.real(result)
                
                # Return with proper error tracking
                power_result = DimensionalArray(result, p.error_registry)
                power_result._error_id = error_id
                return power_result
            
            return DimensionalArray(result, p.error_registry)
        
        # Standard case: use numpy broadcasting
        return DimensionalArray(np.power(x_scalar, p.array), p.error_registry)
    
    # Original implementation for DimensionalArray base
    if isinstance(x, DimensionalArray):
        # Detect singular cases using proper dimensional criteria
        singular_mask = np.zeros_like(x.array, dtype=bool)
        
        # Case 1: Zero base with non-positive exponent
        # Use exact zero detection for dimensional correctness
        if isinstance(p, (int, float, complex)):
            if p <= 0:
                singular_mask |= (x.array == 0)
        else:
            # Vector-valued exponent
            p_array = p.array if isinstance(p, DimensionalArray) else p
            singular_mask |= np.logical_and(x.array == 0, p_array <= 0)
        
        # Case 2: Negative base with non-integer exponent
        if isinstance(p, (int, float, complex)):
            if not float(p).is_integer():
                singular_mask |= (x.array < 0)
        else:
            # Vector-valued exponent
            p_array = p.array if isinstance(p, DimensionalArray) else p
            non_integer_mask = ~np.array([float(p_val).is_integer() 
                                        for p_val in p_array.flat]).reshape(p_array.shape)
            singular_mask |= np.logical_and(x.array < 0, non_integer_mask)
        
        # Handle singularities
        if np.any(singular_mask):
            return _dimensional_power_reduction(x, p, singular_mask)
        
        # Standard power for non-singular inputs
        if isinstance(p, DimensionalArray):
            return DimensionalArray(np.power(x.array, p.array), x.error_registry)
        return DimensionalArray(np.power(x.array, p), x.error_registry)
    
    # Handle standard numpy arrays
    return np.power(x, p)

def _dimensional_power_reduction(x, p, singular_mask):
    """
    Implement dimensional reduction for power operations at singularities.
    
    Parameters:
        x: DimensionalArray base
        p: Exponent (scalar or DimensionalArray)
        singular_mask: Boolean mask identifying singular elements
        
    Returns:
        DimensionalArray with singular elements dimensionally reduced
    """
    # Create result array initialized with standard power operation
    # where it's well-defined
    result = np.zeros_like(x.array, dtype=complex)
    non_singular = ~singular_mask
    
    if isinstance(p, DimensionalArray):
        p_array = p.array
        # Apply standard power operation to non-singular elements
        result[non_singular] = np.power(x.array[non_singular], 
                                     p_array[non_singular] if p_array.shape == x.array.shape 
                                     else p_array)
    else:
        # Scalar exponent
        result[non_singular] = np.power(x.array[non_singular], p)
    
    # Ensure singular_mask is at least 1-dimensional for np.where
    if singular_mask.ndim == 0:
        # Handle scalar case
        if singular_mask:  # If True for scalar
            # For scalar case, we're already dealing with the single value
            # Just apply the specific reduction directly without using indices
            base = x.array.item() if hasattr(x.array, 'item') else x.array
            exponent = p.array.item() if isinstance(p, DimensionalArray) and hasattr(p.array, 'item') else p
            
            # Handle 0^0 case for scalar
            if base == 0 and exponent == 0:
                result = np.array(1.0)
                
                # Store dimensional information for this mathematical convention
                # Ensure shape is not empty for scalar values
                original_shape = x.array.shape if x.array.shape else (1,)
                convention_data = ErrorData(
                    original_shape=original_shape,
                    error_tensor=np.array([0.0, 0.0]),  # Store 0^0 values
                    reduction_type='power_convention',
                    manifold_data={'base': 0.0, 'exponent': 0.0}
                )
                x.error_registry.store(convention_data)
                
                # Create result with error tracking
                return DimensionalArray(result, x.error_registry)
            
            # Handle 0^negative case for scalar
            elif base == 0 and exponent < 0:
                # Use dimensional analysis to compute appropriate value
                reduced_dim = x._divide_by_zero()
                # Convert to float to avoid integer power error
                float_reduced = reduced_dim.array.astype(float)
                result = float_reduced ** float(exponent)
                return DimensionalArray(result, x.error_registry)
                
            # Handle negative^non-integer case for scalar
            elif base < 0 and not float(exponent).is_integer():
                result = np.array(complex(np.abs(base) ** exponent) * np.exp(1j * np.pi * exponent))
                return DimensionalArray(result, x.error_registry)
                
        # If not a singular case, just return the regular power
        return DimensionalArray(np.power(x.array, p.array if isinstance(p, DimensionalArray) else p), x.error_registry)
    
    # For array cases, continue with the original approach 
    singular_indices = np.where(singular_mask)
    
    # Extract singular elements for processing
    singular_values = x.array[singular_indices]
    
    # Depending on the nature of the singularity, apply appropriate reduction
    for i, idx in enumerate(zip(*singular_indices)):
        # Get the specific base and exponent at this position
        base = x.array[idx]
        exponent = p_array[idx] if isinstance(p, DimensionalArray) and p_array.shape == x.array.shape else p
        
        # Apply dimensional reduction for singularity handling
        if base == 0 and exponent <= 0:
            # Zero raised to non-positive power
            # Use dimensional reduction approach
            if exponent == 0:
                # Indeterminate form 0^0, conventionally set to 1
                # This is mathematically correct as lim(x→0) x^0 = 1
                result[idx] = 1.0
                
                # Store dimensional information for this mathematical convention
                convention_data = ErrorData(
                    original_shape=x.array.shape,
                    error_tensor=np.array([0.0, 0.0]),  # Store 0^0 values
                    reduction_type='power_convention',
                    manifold_data={'base': 0.0, 'exponent': 0.0}
                )
                convention_id = x.error_registry.store(convention_data)
            else:
                # 0^negative is a true dimensional reduction case
                # Use dimensional analysis to compute appropriate value
                # Create reduced dimension that preserves scaling properties
                
                # Compute dimensional relationship using structural components
                # This is equivalent to 0^p = lim(x→0) x^p but preserves scaling
                # Use x's _divide_by_zero method to get proper dimensionality
                reduced_dim = x._divide_by_zero()
                
                # Use the reduced dimension to compute power with proper scaling
                result[idx] = reduced_dim ** exponent
        elif base < 0 and not float(exponent).is_integer():
            # Negative base with non-integer exponent
            # Project onto complex domain
            result[idx] = complex(np.abs(base) ** exponent) * \
                         np.exp(1j * np.pi * exponent)
    
    # Store error information for reconstruction
    error_tensor = x.array.copy()
    error_tensor[non_singular] = 0  # Zero out non-singular elements
    
    error_data = ErrorData(
        original_shape=x.array.shape,
        error_tensor=error_tensor,
        reduction_type='partial',
        mask=singular_mask
    )
    error_id = x.error_registry.store(error_data)
    
    # Convert result to appropriate type
    if np.all(np.imag(result) == 0):
        result = np.real(result)
    
    # Create result with error tracking
    power_result = DimensionalArray(result, x.error_registry)
    power_result._error_id = error_id
    
    return power_result

def matrix_power(A, n, handle_singularity=True):
    """
    Compute matrix power A^n with dimensional reduction for singular matrices.
    
    Parameters:
        A: Input matrix (DimensionalArray)
        n: Power (integer or float)
        handle_singularity: Whether to handle singular matrices
        
    Returns:
        DimensionalArray: Matrix power using dimensional reduction if necessary
    """
    from .array import DimensionalArray
    
    if isinstance(A, DimensionalArray):
        A_array = A.array
    else:
        A_array = np.asarray(A)
    
    # For integer powers, use more efficient algorithms
    if isinstance(n, (int, np.integer)):
        if n >= 0:
            # Handle special cases
            if n == 0:
                # A^0 = I, except for singular matrices
                if handle_singularity and np.linalg.matrix_rank(A_array) < min(A_array.shape):
                    # For singular matrices, use regularization
                    return _regularized_matrix_power(A, 0)
                return DimensionalArray(np.eye(A_array.shape[0], dtype=A_array.dtype))
            elif n == 1:
                return A if isinstance(A, DimensionalArray) else DimensionalArray(A_array)
            elif n == 2:
                return DimensionalArray(A_array @ A_array)
            else:
                # Use binary exponentiation for efficiency
                return DimensionalArray(np.linalg.matrix_power(A_array, n))
        else:
            # Negative power: compute inverse then positive power
            # For singular matrices, use regularization
            if handle_singularity and np.linalg.matrix_rank(A_array) < min(A_array.shape):
                return _regularized_matrix_power(A, n)
            
            # For non-singular matrices, use standard approach
            inv_A = np.linalg.inv(A_array)
            return DimensionalArray(np.linalg.matrix_power(inv_A, -n))
    
    # For non-integer powers, use eigendecomposition
    if handle_singularity and np.linalg.matrix_rank(A_array) < min(A_array.shape):
        return _regularized_matrix_power(A, n)
    
    # For well-conditioned matrices, use eigendecomposition
    eigvals, eigvecs = np.linalg.eigh(A_array)
    eigvals_power = np.power(eigvals, n)
    result = eigvecs @ np.diag(eigvals_power) @ np.linalg.inv(eigvecs)
    
    return DimensionalArray(result)

def _regularized_matrix_power(A, n):
    """
    Compute regularized matrix power for singular matrices.
    
    Uses dimensional reduction via SVD to handle singularities.
    
    Parameters:
        A: Input matrix (DimensionalArray)
        n: Power (integer or float)
        
    Returns:
        DimensionalArray: Regularized matrix power
    """
    from .array import DimensionalArray
    
    A_array = A.array if isinstance(A, DimensionalArray) else np.asarray(A)
    
    # Compute SVD
    U, s, Vh = np.linalg.svd(A_array, full_matrices=False)
    
    # Use proper dimensional approach instead of arbitrary threshold
    # Create dimensional array representation
    from .registry import ErrorRegistry, ErrorData
    from . import get_registry
    error_registry = get_registry()
    
    # Store singular value structure
    sv_data = ErrorData(
        original_shape=s.shape,
        error_tensor=s,
        reduction_type='matrix_power_svd',
        manifold_data={'singular_values': s}
    )
    error_id = error_registry.store(sv_data)
    
    # Look for actual zeros
    zero_mask = (s == 0)
    
    # Handle singular values using matrix's own structure
    s_reg = s.copy()
    
    # Proper handling for zeros
    if np.any(zero_mask):
        # Find smallest non-zero value for structural reference
        if np.any(~zero_mask):
            min_nonzero = np.min(s[~zero_mask])
            # Use a structurally derived value instead of arbitrary threshold
            s_reg[zero_mask] = min_nonzero * min_nonzero / np.max(s)
        else:
            # All values are zero - use tiny value
            s_reg[zero_mask] = np.finfo(float).tiny
    
    # Compute power of singular values
    s_power = np.power(s_reg, n)
    
    # Reconstruct matrix
    if n >= 0:
        # Positive power
        result = U @ np.diag(s_power) @ Vh
    else:
        # Negative power (pseudo-inverse technique)
        result = U @ np.diag(1 / s_power) @ Vh
    
    # Store error information
    if isinstance(A, DimensionalArray):
        error_tensor = A_array - U @ np.diag(s_reg) @ Vh
        
        error_data = ErrorData(
            original_shape=A_array.shape,
            error_tensor=error_tensor,
            reduction_type='complete'
        )
        error_id = A.error_registry.store(error_data)
        
        power_result = DimensionalArray(result, A.error_registry)
        power_result._error_id = error_id
        
        return power_result
    
    return DimensionalArray(result)

def matrix_exp(A, handle_singularity=True):
    """
    Compute matrix exponential exp(A) with dimensional reduction where needed.
    
    Parameters:
        A: Input matrix (DimensionalArray)
        handle_singularity: Whether to handle problematic matrices
        
    Returns:
        DimensionalArray: Matrix exponential using dimensional framework
    """
    from .linalg import expm
    return expm(A)
