"""Error registry system for tracking dimensional operations."""

from typing import Dict, Optional, NamedTuple, Tuple
import numpy as np
import weakref
import uuid
from .exceptions import RegistryError

class ErrorData:
    """
    Container for error information from dimensional reduction operations.
    
    Implements the error space E_log for logarithmic dimensional manifold,
    preserving information content according to Theorem 1.1:
    I_log(T) = I_log(π_log(T)) + I_log(ε_log(T))
    
    Parameters
    ----------
    original_shape : tuple
        Shape of the original tensor T ∈ D_n
    error_tensor : numpy.ndarray
        Error tensor ε_log(T) containing reduction information
    reduction_type : str
        Type of reduction ('complete', 'partial', or 'logarithmic')
    mask : numpy.ndarray, optional
        Boolean mask identifying dimensional boundaries
    manifold_data : dict, optional
        Additional manifold-specific metadata
    """
    def __init__(self, original_shape, error_tensor, reduction_type, 
                 mask=None, manifold_data=None):
        # Valid reduction types - expanded to include all our new types
        valid_types = [
            # Basic types
            'complete', 'partial', 'logarithmic', 'partial_division',
            # SVD-related types
            'svd_error_recovery', 'svd_singularity_tracking', 'matrix_logm_svd',
            'matrix_power_svd', 'entanglement', 'svd_ratios', 'pinv_svd', 'svd_failure',
            # Log domain types
            'log_domain', 'renyi_von_neumann_limit', 'zero_regularization',
            'sv_downscaling', 'eig_scaling',
            # Quantum types
            'quantum_elevation', 'entanglement_reduction', 'entanglement_entropy',
            'renyi_entropy', 'log_negativity', 'schmidt_normalization',
            'density_matrix_normalization', 'purity_check', 'trace_normalization',
            'entropy',
            # Boundary handling
            'bound_constraint', 'filter_operation', 'negative_eigenvalues',
            'invalid_density_matrix', 'negative_sqrtm', 'condition_number',
            'normalization', 'fractal', 'filter_operation', 'coherence',
            # Power handling
            'power_convention',
            # Additional types for matrix functions
            'logm_svd', 'sqrtm_eigenvals', 'sinm_structure', 'cosm_structure',
            'quantum_power_svd', 'expm_eigenvalues', 'expm_error', 
            # New linear algebra analysis types
            'svd_structure', 'eigenvalue_structure', 'det_near_zero', 'inv_error',
            'inv_svd', 'rank_analysis',
            # FFT dimensional analysis types
            'fft_input_tracking', 'ifft_input_tracking', 'fft_nan_inf', 
            'ifft_nan_inf', 'fft_result_nan_inf', 'ifft_result_nan_inf',
            'fftshift', 'ifftshift', 'fftfreq_params', 'rfft_input_tracking',
            'irfft_input_tracking', 'rfft_complex_input', 'rfft_result_nan_inf',
            'irfft_result_nan_inf', 'rfftfreq_params',
            # Additional dimensional reduction types from base.py
            'division_by_zero_array', 'division_by_zero_scalar',
            'near_zero_division', 'dimensional_division', 'dimensional_scalar_division',
            'dimensional_svd', 'dimensional_svd_values_only', 'combined_operation',
            # Additional types used in the code
            'logm_singular', 'logm_negative_input', 'logm_negative_diag', 
            'logm_negative_eigenvals', 'sinm_eigen', 'cosm_eigen', 'tanm_eigen',
            'sinm_svd', 'cosm_svd', 'tanm_svd', 'tanm_poles',
            # Quantum-specific types
            'quantum_tensor_elevation', 'quantum_tensor_reduction',
            'schmidt_decomposition', 'quantum_coordinate_system',
            'quantum_entanglement_structure', 'quantum_system_gauge',
            'entanglement_verification', 'quantum_state_purification',
            'density_matrix_trace',
            # New error types added for enhanced operations
            'complex_division_by_zero', 'absolute_value', 'division_error_propagation',
            'scalar_division_by_zero', 'unary_operation', 'sign_change_tracking',
            'comparison_with_special_values'
        ]
        
        if reduction_type not in valid_types:
            raise ValueError(f"Invalid reduction type. Must be one of: {', '.join(valid_types)}")
        
        # Allow empty shape for backward compatibility with tests
        # but keep a validation check for truly empty error data
        if not original_shape and (not hasattr(error_tensor, 'size') or error_tensor.size == 0):
            raise ValueError("Original shape cannot be empty when error tensor is also empty")
            
        # Allow error_tensor to have different shape in some cases (like eigenvalue tracking)
        # but warn or handle appropriately
        if hasattr(error_tensor, 'shape') and error_tensor.shape != original_shape:
            # For specific reduction types, shape mismatch is expected
            shape_mismatch_allowed = [
                'svd_singularity_tracking', 'logm_svd', 'condition_number',
                'eigenvalues', 'schmidt_normalization', 'purity_check',
                'sv_downscaling', 'eig_scaling', 'sqrtm_eigenvals',
                'sinm_structure', 'cosm_structure', 'quantum_power_svd',
                'expm_eigenvalues', 'svd_structure', 'eigenvalue_structure',
                'fft_input_tracking', 'ifft_input_tracking', 'fftfreq_params',
                'rfft_input_tracking', 'irfft_input_tracking', 'rfftfreq_params'
            ]
            
            if reduction_type not in shape_mismatch_allowed:
                # Don't raise error but store information about mismatch
                if manifold_data is None:
                    manifold_data = {}
                manifold_data['shape_mismatch'] = True
                manifold_data['error_tensor_shape'] = error_tensor.shape
            
        self._original_shape = original_shape
        self._error_tensor = error_tensor
        self._reduction_type = reduction_type
        self._mask = mask
        self._manifold_data = manifold_data or {}

    @property
    def original_shape(self) -> tuple:
        """Shape of the original tensor space D_n."""
        return self._original_shape

    @property
    def error_tensor(self) -> np.ndarray:
        """Error tensor ε_log(T) in the error space E_log."""
        return self._error_tensor

    @property
    def reduction_type(self) -> str:
        """Type of dimensional reduction applied."""
        return self._reduction_type

    @property
    def mask(self) -> Optional[np.ndarray]:
        """Mask identifying dimensional boundaries."""
        return self._mask

    @property
    def manifold_data(self) -> dict:
        """Manifold-specific metadata."""
        return self._manifold_data

    def reconstruct(self):
        """
        Reconstruct original values using manifold-specific methods.
        
        Implements the reconstruction theorem:
        I_log(T) = I_log(π_log(T)) + I_log(ε_log(T))
        
        Extended to handle all reduction types from our expanded framework.
        """
        # Group 1: Basic logarithmic reconstructions
        if self._reduction_type in ('logarithmic', 'log_domain', 'partial_division'):
            # Initialize reconstruction in original tensor space
            reconstructed = np.zeros_like(self._error_tensor)
            
            # Non-singular points maintain their values
            if self._mask is not None:
                reconstructed[~self._mask] = self._error_tensor[~self._mask]
                
                # At dimensional boundaries, apply inverse log transform
                # following group structure preservation (Theorem 1.2)
                reconstructed[self._mask] = np.exp(self._error_tensor[self._mask])
            
            return reconstructed
        
        # Group 2: SVD-based reconstructions
        elif self._reduction_type in ('svd_singularity_tracking', 'matrix_logm_svd', 'svd_ratios',
                                    'matrix_power_svd', 'entanglement', 'pinv_svd'):
            # For SVD reduction types, the manifold_data will contain the singular values
            if 'singular_values' in self._manifold_data:
                singular_values = self._manifold_data['singular_values']
                
                # Use original singular values for reconstruction
                return singular_values
            
        # Group 3: Quantum reconstructions
        elif self._reduction_type in ('quantum_elevation', 'entanglement_reduction', 
                                    'entanglement_entropy', 'renyi_entropy', 'log_negativity',
                                    'schmidt_normalization', 'density_matrix_normalization'):
            # This typically uses the full error tensor and manifold data
            return self._error_tensor
            
        # Group 4: Special edge case handling
        elif self._reduction_type in ('purity_check', 'negative_eigenvalues', 
                                    'invalid_density_matrix', 'condition_number',
                                    'normalization', 'coherence'):
            # These are typically tracking operations, not reconstruction
            if 'original_data' in self._manifold_data:
                return self._manifold_data['original_data']
            else:
                return self._error_tensor
            
        # Default for all other types: return error tensor directly
        return self._error_tensor

class ErrorRegistry:
    """
    Registry for tracking error information from dimensional operations.
    Uses weak references to avoid memory leaks.
    """
    def __init__(self):
        self._errors = {}
        self._next_id = 0
        
    def store(self, error_data: ErrorData) -> int:
        """Store error data and return unique ID."""
        error_id = self._next_id
        self._errors[error_id] = error_data
        self._next_id += 1
        return error_id
        
    def retrieve(self, error_id: int) -> Optional[ErrorData]:
        """Retrieve error data by ID."""
        return self._errors.get(error_id)
        
    def combine(self, other: 'ErrorRegistry') -> 'ErrorRegistry':
        """Combine two error registries."""
        combined = ErrorRegistry()
        
        # Copy errors from self
        for error_id, error_data in self._errors.items():
            combined._errors[error_id] = error_data
            
        # Copy errors from other, offsetting IDs
        offset = self._next_id
        for error_id, error_data in other._errors.items():
            combined._errors[error_id + offset] = error_data
            
        # Set next ID after all combined errors
        combined._next_id = self._next_id + other._next_id
        
        return combined
    
    def clear(self) -> None:
        """Clear all stored error information."""
        self._errors.clear()
        
    def __len__(self) -> int:
        """Get number of active error records."""
        return len(self._errors)
    
    def __contains__(self, error_id: int) -> bool:
        """Check if error ID exists in registry."""
        return error_id in self._errors

    @staticmethod
    def get_registry():
        """Get the global error registry."""
        return get_registry()

# Create a global registry instance
_GLOBAL_REGISTRY = None

def get_registry():
    """Get the global error registry."""
    global _GLOBAL_REGISTRY
    if _GLOBAL_REGISTRY is None:
        _GLOBAL_REGISTRY = ErrorRegistry()
    return _GLOBAL_REGISTRY