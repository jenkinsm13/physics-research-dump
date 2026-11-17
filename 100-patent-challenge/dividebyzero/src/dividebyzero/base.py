"""
Core dimensional array implementation with division by zero support.
"""

import numpy as np
from typing import Union, Optional, Tuple, Any
import copy

from .registry import ErrorRegistry, ErrorData
from .exceptions import ReconstructionError, DimensionalError

class DimensionalArray:
    """
    Array class supporting division by zero through dimensional reduction.
    """
    def __init__(self, 
                 array_like: Union[np.ndarray, list, tuple, 'DimensionalArray'],
                 error_registry: Optional[ErrorRegistry] = None,
                 dtype: Any = None):
        """
        Initialize a DimensionalArray.
        
        Parameters:
            array_like: Input array or array-like object
            error_registry: Optional error registry for tracking dimensional operations
            dtype: Data type for the array (numpy dtype)
        """
        if isinstance(array_like, DimensionalArray):
            self.array = array_like.array.astype(dtype) if dtype else array_like.array.copy()
            self._right_singular_vector = getattr(array_like, '_right_singular_vector', None)
        else:
            # Handle numpy dtype objects directly
            if isinstance(dtype, type) and issubclass(dtype, np.generic):
                self.array = np.array(array_like, dtype=dtype)
            else:
                self.array = np.array(array_like, dtype=dtype)
            self._right_singular_vector = None
            
        
        self.error_registry = error_registry if error_registry is not None else ErrorRegistry.get_registry()
        self._error_id = None

    def __setitem__(self, key, value):
        """Support item assignment."""
        if isinstance(value, DimensionalArray):
            self.array[key] = value.array
        else:
            self.array[key] = value

    def __getitem__(self, key):
        """Support item access."""
        result = self.array[key]
        if isinstance(result, np.ndarray):
            return DimensionalArray(result, self.error_registry)
        return result
    
    def __array_function__(self, func, types, args, kwargs):
        """Implement numpy function protocol."""
        def convert_to_array(obj):
            if isinstance(obj, DimensionalArray):
                return obj.array
            elif isinstance(obj, (list, tuple)):
                return type(obj)(convert_to_array(x) for x in obj)
            return obj
        
        # Convert inputs to numpy arrays, handling nested structures
        args = tuple(convert_to_array(arg) for arg in args)
        kwargs = {k: convert_to_array(v) for k, v in kwargs.items()}
        
        # Call the numpy function directly
        result = func(*args, **kwargs)
        
        # Convert result back to DimensionalArray if needed
        if isinstance(result, np.ndarray):
            return DimensionalArray(result, self.error_registry)
        elif isinstance(result, tuple):
            return tuple(DimensionalArray(r, self.error_registry) if isinstance(r, np.ndarray) else r for r in result)
        return result
    
    def __mul__(self, other: Union[int, float, complex, 'DimensionalArray']) -> 'DimensionalArray':
        """Support multiplication with scalars (including complex) or other DimensionalArray instances."""
        if isinstance(other, DimensionalArray):
            # Combine registries if needed
            combined_registry = self.error_registry
            if self.error_registry is not other.error_registry:
                combined_registry = self.error_registry.combine(other.error_registry)
                
            result = DimensionalArray(self.array * other.array, combined_registry)
            
            # Propagate error information properly
            if self._error_id is not None or (hasattr(other, '_error_id') and other._error_id is not None):
                return self.propagate_error(other)._with_array(result.array)
            
            return result
        
        # For scalar multiplication, just propagate our error info
        result = DimensionalArray(self.array * other, self.error_registry)
        if self._error_id is not None:
            result._error_id = self._error_id
        return result

    def __rmul__(self, other: Union[int, float, complex]) -> 'DimensionalArray':
        """Support right multiplication with scalars (including complex)."""
        result = DimensionalArray(other * self.array, self.error_registry)
        if self._error_id is not None:
            result._error_id = self._error_id
        return result

    def __rtruediv__(self, other: Union[int, float, complex]) -> 'DimensionalArray':
        """Support right division (other / self)."""
        # Handle division by zero using dimensional reduction if needed
        if np.any(self.array == 0):
            mask = self.array == 0
            result = np.zeros_like(self.array, dtype=float)
            non_zero_mask = ~mask
            result[non_zero_mask] = other / self.array[non_zero_mask]
            # For zero elements, use dimensional reduction
            if np.any(mask):
                reduced = self._partial_divide_by_zero(mask)
                result[mask] = other / reduced.array[mask]
            return DimensionalArray(result, self.error_registry)
        return DimensionalArray(other / self.array, self.error_registry)

    def _divide_by_zero(self) -> 'DimensionalArray':
        """Implement complete division by zero"""
        original_shape = self.array.shape
        ndim = self.array.ndim
        
        if ndim == 0:  # scalar case
            result = np.array([np.abs(self.array)])
            error = np.array([self.array - result[0]])
            original_shape = (1,)  # Use (1,) as the shape for scalars
        elif ndim == 1:
            # For 1D arrays, reduce to a single value
            mean_val = np.abs(self.array).mean()
            result = np.array([mean_val])  # Reduce to scalar
            error = self.array - mean_val
        else:
            # For higher dimensions, use SVD and reduce rank
            from . import linalg  # Import here to avoid circular imports
            reshaped = self.array.reshape(original_shape[0], -1)
            try:
                U, S, Vt = linalg.svd(reshaped, full_matrices=False)
                # Use proper dimensional reduction for singularity handling
                # This preserves mathematical structure without arbitrary thresholds
                smallest_nonzero_sv = np.min(S[S > 0]) if np.any(S > 0) else S[0]
                S_ratio = S / S[0]  # Get singular value ratios
                
                # Store the ratio structure as it contains core dimensional information
                error_data = ErrorData(
                    original_shape=(S.shape,),
                    error_tensor=S,
                    reduction_type='svd_ratios',
                    manifold_data={'ratios': S_ratio}
                )
                sv_error_id = self.error_registry.store(error_data)
                
                # Use first singular value and vector, preserving mathematical structure
                result = U[:, 0] * S[0]
                self._right_singular_vector = Vt[0, :]
                # Compute error using truncated reconstruction
                reconstructed = np.outer(result, Vt[0, :]).reshape(original_shape)
                error = self.array - reconstructed
            except np.linalg.LinAlgError:
                raise DimensionalError("SVD failed during division by zero")
        
        # Store error information
        error_data = ErrorData(
            original_shape=original_shape,
            error_tensor=error,
            reduction_type='complete'
        )
        error_id = self.error_registry.store(error_data)
        
        reduced = DimensionalArray(result, self.error_registry)
        reduced._error_id = error_id
        reduced._right_singular_vector = getattr(self, '_right_singular_vector', None)
        return reduced
    
    def _partial_divide_by_zero(self, mask: np.ndarray) -> 'DimensionalArray':
        """Handle partial division by zero with proper dimensional reduction."""
        result = np.zeros_like(self.array, dtype=float)
        non_zero_mask = ~mask
        
        # Correct division implementation
        if np.any(non_zero_mask):
            result[non_zero_mask] = self.array[non_zero_mask]
        
        # Handle zero-division cases with proper broadcasting
        if self.array.ndim <= 2:
            # For 1D and 2D arrays, use direct mean
            non_zero_elements = self.array[non_zero_mask]
            if non_zero_elements.size > 0:
                result[mask] = np.mean(np.abs(non_zero_elements))  # Use absolute values for stability
            else:
                # If no non-zero elements, use a finite number based on machine precision
                result[mask] = np.finfo(float).eps  # Small but non-zero value
        else:
            # For higher dimensions, handle each slice properly
            for idx in np.ndindex(self.array.shape[:-1]):
                slice_mask = mask[idx]
                if np.any(slice_mask):
                    slice_data = self.array[idx]
                    non_zero_slice = slice_data[~slice_mask]
                    if non_zero_slice.size > 0:
                        result[idx][slice_mask] = np.mean(np.abs(non_zero_slice))
                    else:
                        # If no non-zero elements in this slice, use a finite number
                        result[idx][slice_mask] = np.finfo(float).eps
        
        # Store error information
        error_data = ErrorData(
            original_shape=self.array.shape,
            error_tensor=self.array - result,
            reduction_type='partial'
        )
        error_id = self.error_registry.store(error_data)
        
        reduced = DimensionalArray(result, self.error_registry)
        reduced._error_id = error_id
        return reduced

    def __pow__(self, power, modulo=None):
        """Support power operation with dimensional reduction at singularities."""
        if modulo is not None:
            # Apply elementwise power with modulo since numpy doesn't support 3-arg pow directly
            result_array = np.zeros_like(self.array)
            for idx in np.ndindex(self.array.shape):
                result_array[idx] = pow(int(self.array[idx]), power, modulo)
            return DimensionalArray(result_array, self.error_registry)
        
        # Import powers module for special handling of edge cases
        from . import powers  # Import here to avoid circular imports
        
        # Handle power operation directly here to avoid circular imports
        try:
            # Handle special cases like 0^0 and 0^negative using dimensional framework
            # Check for potential division by zero in negative powers
            if isinstance(power, (int, float)) and power < 0:
                zero_mask = self.array == 0
                if np.any(zero_mask):
                    # Track detailed information about singularities
                    error_data = ErrorData(
                        original_shape=self.array.shape,
                        error_tensor=zero_mask.astype(float),
                        reduction_type='power_convention',
                        manifold_data={
                            'exponent': power,
                            'zero_indices': np.where(zero_mask)
                        }
                    )
                    error_id = self.error_registry.store(error_data)
                    
                    # Handle zeros specially before raising to negative power
                    temp_array = self.array.copy()
                    # Apply dimensional reduction for zero values
                    reduced = self._partial_divide_by_zero(zero_mask)
                    temp_array[zero_mask] = reduced.array[zero_mask]
                    
                    # Now compute power
                    if isinstance(power, DimensionalArray):
                        result_array = np.power(temp_array, power.array)
                    else:
                        result_array = np.power(temp_array, power)
                        
                    # Create result with proper error tracking
                    result = DimensionalArray(result_array, self.error_registry)
                    result._error_id = error_id
                    return result
            
            # Standard power operation for normal cases
            if isinstance(power, DimensionalArray):
                result_array = np.power(self.array, power.array)
            else:
                result_array = np.power(self.array, power)
                
            # Create the result with proper error tracking
            result = DimensionalArray(result_array, self.error_registry)
            
            # Propagate error information
            if self._error_id is not None:
                result._error_id = self._error_id
                
            return result
        except:
            # Fall back to a more direct implementation
            try:
                # Try using the powers module for more robust handling
                return powers.power(self, power)
            except ImportError:
                # If powers module not available, use basic implementation
                return DimensionalArray(self.array ** power, self.error_registry)
    
    def __rpow__(self, base):
        """Support right power operation (base ** self)."""
        try:
            # Convert base to numpy array if not already
            base_array = np.array(base) if not isinstance(base, np.ndarray) else base
            
            # Apply power operation directly
            result_array = np.power(base_array, self.array)
            
            # Create result with proper error tracking
            result = DimensionalArray(result_array, self.error_registry)
            
            # Propagate error information
            if self._error_id is not None:
                result._error_id = self._error_id
                
            return result
        except:
            # Fall back to a more direct implementation
            if not isinstance(base, DimensionalArray):
                base_dim = DimensionalArray(base, self.error_registry)
                return DimensionalArray(base ** self.array, self.error_registry)
            return DimensionalArray(base.array ** self.array, self.error_registry)
    
    def elevate(self, 
                target_shape: Optional[Tuple[int, ...]] = None) -> 'DimensionalArray':
        """
        Reconstruct higher dimensional representation using the dimensional
        structure and error information tracked during reduction.
        
        Parameters:
            target_shape: Optional shape for reconstruction
        """
        if not self._error_id:
            raise ReconstructionError("No error information available for elevation")
            
        error_data = self.error_registry.retrieve(self._error_id)
        if not error_data:
            raise ReconstructionError("Error information has been garbage collected")
        
        if error_data.reduction_type == 'complete':
            return self._complete_elevation(error_data)
        else:
            return self._partial_elevation(error_data)
        
    @staticmethod
    def elevate_dimension(reduced: 'DimensionalArray', 
                        error: 'DimensionalArray', 
                        original_shape: Tuple[int, ...]) -> 'DimensionalArray':
        """
        Reconstruct the original dimensional array from its reduced form and error tensor.
        Uses the error tensor directly without arbitrary scaling.
        """
        reconstructed = reduced.array.reshape(original_shape)
        elevated = reconstructed + error.array
        return DimensionalArray(elevated, reduced.error_registry)
    
    def _complete_elevation(self, 
                          error_data: ErrorData) -> 'DimensionalArray':
        """Handle elevation for complete reduction using proper error information"""
        # Use error data to reconstruct without arbitrary noise
        # This preserves mathematical structure
        
        if self.array.size == 1:  # scalar case
            reconstructed = np.full(error_data.original_shape, self.array[0])
        elif self.array.ndim == 1 and self._right_singular_vector is not None:
            # Reconstruct matrix from vector using outer product
            reconstructed = np.outer(self.array, self._right_singular_vector)
            reconstructed = reconstructed.reshape(error_data.original_shape)
        else:
            # For other cases, reshape and broadcast
            reconstructed = np.broadcast_to(
                self.array.reshape(*self.array.shape, 1),
                error_data.original_shape
            )
            
        # Use error data directly rather than with random noise
        # This maintains proper error structure
        if hasattr(error_data, 'manifold_data') and error_data.manifold_data:
            # Use manifold data if available for more precise reconstruction
            result = reconstructed + error_data.error_tensor
        else:
            result = reconstructed
        return DimensionalArray(result, self.error_registry)
    
    def _partial_elevation(self,
                         error_data: ErrorData) -> 'DimensionalArray':
        """Handle elevation for partial reduction using proper error information"""
        result = self.array.copy()
        
        # Apply elevation using error data without arbitrary noise
        # This preserves mathematical structure
        mask = error_data.mask
        
        # Use error tensor directly to preserve mathematical structure
        if mask is not None and hasattr(error_data, 'error_tensor'):
            # Use direct error data for reconstruction
            modified = result.copy()
            modified[mask] = error_data.error_tensor[mask]
            result = modified
        
        return DimensionalArray(result, self.error_registry)
    
    def __getattr__(self, name: str) -> Any:
        """Get attribute from underlying numpy array if not found in DimensionalArray."""
        if name == '_left_singular_vector':
            return self._left_singular_vector
        if name == '_right_singular_vector':
            return self._right_singular_vector
        if name == '_error_registry':
            return self._error_registry
        if name == '_array':
            return self._array
        
        # Try to get attribute from numpy array
        try:
            attr = getattr(self.array, name)
            
            # If the attribute is a method, wrap it to return DimensionalArray
            if callable(attr):
                def wrapped_method(*args, **kwargs):
                    result = attr(*args, **kwargs)
                    if isinstance(result, np.ndarray):
                        return DimensionalArray(result, self.error_registry)
                    return result
                return wrapped_method
            
            return attr
        except AttributeError:
            raise AttributeError(f"Neither DimensionalArray nor its underlying numpy array has attribute {name}")
            
    def __repr__(self) -> str:
        return f"DimensionalArray({self.array.__repr__()})"
    
    @property
    def shape(self) -> Tuple[int, ...]:
        return self.array.shape
    
    @property
    def ndim(self) -> int:
        return self.array.ndim
    
    # Note: __mul__ and __rmul__ are already defined above
        
    def __truediv__(self, other: Union[int, float, np.generic, 'DimensionalArray']) -> 'DimensionalArray':
        """Support division using the dimensional divide algorithm."""
        if isinstance(other, DimensionalArray):
            zero_indices = np.isclose(other.array, 0.0)
            
            # Check if any divisors are zero
            if np.any(zero_indices):
                # For complex numbers, track the information but don't apply SVD
                if np.issubdtype(self.array.dtype, np.complexfloating) or np.issubdtype(other.array.dtype, np.complexfloating):
                    result_array = self.array / other.array  # This will give inf or nan for zeros
                    result = DimensionalArray(result_array, self.error_registry)
                    
                    # Track error information for divisions by zero
                    error_data = ErrorData(
                        original_shape=other.array.shape,
                        error_tensor=zero_indices.astype(float),
                        reduction_type='complex_division_by_zero',
                        manifold_data={
                            'dividend_values': self.array[zero_indices].tolist() if np.any(zero_indices) else [],
                            'complex_division': True
                        }
                    )
                    result._error_id = self.error_registry.store(error_data)
                    return result
                else:
                    # For real numbers, use the dimensional divide algorithm
                    return self.dimensional_divide(other)
            else:
                # No zeros in divisor, perform normal division
                result = DimensionalArray(self.array / other.array, self.error_registry)
                
                # Propagate error information if either operand has it
                if self._error_id is not None or other._error_id is not None:
                    # Create a new error data that combines information from both operands
                    error_ids = [id for id in [self._error_id, other._error_id] if id is not None]
                    if error_ids:
                        error_data = ErrorData(
                            original_shape=result.array.shape,
                            error_tensor=np.zeros_like(result.array, dtype=float),
                            reduction_type='division_error_propagation',
                            manifold_data={'source_error_ids': error_ids}
                        )
                        result._error_id = self.error_registry.store(error_data)
                return result
        else:
            # Division by scalar
            if other == 0:
                # For division by scalar zero, create a special error
                error_data = ErrorData(
                    original_shape=self.array.shape,
                    error_tensor=np.ones_like(self.array, dtype=float),
                    reduction_type='scalar_division_by_zero',
                    manifold_data={'dividend_shape': self.array.shape}
                )
                result = DimensionalArray(np.full_like(self.array, np.inf), self.error_registry)
                result._error_id = self.error_registry.store(error_data)
                return result
            
            result = DimensionalArray(self.array / other, self.error_registry)
            # Propagate error information
            if self._error_id is not None:
                result._error_id = self._error_id
            return result
    
    def __add__(self, other: Union[int, float, complex, 'DimensionalArray']) -> 'DimensionalArray':
        """Support addition with scalars or other DimensionalArray instances."""
        if isinstance(other, DimensionalArray):
            # Combine error registries if different
            combined_registry = self.error_registry
            if self.error_registry is not other.error_registry:
                combined_registry = self.error_registry.combine(other.error_registry)
                
            result = DimensionalArray(self.array + other.array, combined_registry)
            
            # Propagate error information properly
            if self._error_id is not None or (hasattr(other, '_error_id') and other._error_id is not None):
                return self.propagate_error(other)._with_array(result.array)
                
            return result
        
        # Handle scalar addition
        result = DimensionalArray(self.array + other, self.error_registry)
        if self._error_id is not None:
            result._error_id = self._error_id
        return result
    
    def __radd__(self, other: Union[int, float, complex]) -> 'DimensionalArray':
        """Support right addition with scalars."""
        return DimensionalArray(other + self.array, self.error_registry)
    
    def __sub__(self, other: Union[int, float, complex, 'DimensionalArray']) -> 'DimensionalArray':
        """Support subtraction with scalars or other DimensionalArray instances."""
        if isinstance(other, DimensionalArray):
            # Combine error registries if different
            combined_registry = self.error_registry
            if self.error_registry is not other.error_registry:
                combined_registry = self.error_registry.combine(other.error_registry)
                
            result = DimensionalArray(self.array - other.array, combined_registry)
            
            # Propagate error information properly
            if self._error_id is not None or (hasattr(other, '_error_id') and other._error_id is not None):
                return self.propagate_error(other)._with_array(result.array)
                
            return result
        
        # Handle scalar subtraction
        result = DimensionalArray(self.array - other, self.error_registry)
        if self._error_id is not None:
            result._error_id = self._error_id
        return result
    
    def __rsub__(self, other: Union[int, float, complex]) -> 'DimensionalArray':
        """Support right subtraction (other - self)."""
        return DimensionalArray(other - self.array, self.error_registry)

    @property
    def error_id(self) -> Optional[int]:
        """Access the error ID associated with this array."""
        return self._error_id
        
    @error_id.setter
    def error_id(self, value: Optional[int]) -> None:
        """Set the error ID for this array."""
        self._error_id = value
        
    def with_error_id(self, error_id: Optional[int]) -> 'DimensionalArray':
        """Create a copy of this array with the specified error ID."""
        result = DimensionalArray(self.array.copy(), self.error_registry)
        result._error_id = error_id
        return result
        
    def propagate_error(self, other: Optional['DimensionalArray'] = None) -> 'DimensionalArray':
        """
        Propagate error information from this array and optionally another array.
        Returns a new array with combined error information.
        
        Parameters:
            other: Optional second array to propagate errors from
        """
        result = DimensionalArray(self.array.copy(), self.error_registry)
        
        # Propagate error from self
        if self._error_id is not None:
            result._error_id = self._error_id
            
        # Additionally propagate from other if provided
        if other is not None and hasattr(other, '_error_id') and other._error_id is not None:
            # If we already have an error ID, create a combined error
            if result._error_id is not None:
                error_data_self = self.error_registry.retrieve(self._error_id)
                error_data_other = other.error_registry.retrieve(other._error_id)
                
                if error_data_self and error_data_other:
                    # Create a combined error data
                    combined_data = ErrorData(
                        original_shape=self.array.shape,
                        error_tensor=np.zeros_like(self.array),
                        reduction_type='combined_operation',
                        manifold_data={
                            'source_ids': [self._error_id, other._error_id],
                            'operation': 'propagate'
                        }
                    )
                    result._error_id = self.error_registry.store(combined_data)
            else:
                # If we don't have an error ID yet, just use the other's
                result._error_id = other._error_id
                
        return result

    def _with_array(self, array):
        """
        Internal method to create a new DimensionalArray with the same error information
        but different array data.
        """
        result = DimensionalArray(array, self.error_registry)
        result._error_id = self._error_id
        result._right_singular_vector = self._right_singular_vector
        return result

    def __matmul__(self, other: Union['DimensionalArray', np.ndarray]) -> 'DimensionalArray':
        """Support matrix multiplication with @ operator."""
        if isinstance(other, DimensionalArray):
            # Combine registries if needed
            combined_registry = self.error_registry
            if self.error_registry is not other.error_registry:
                combined_registry = self.error_registry.combine(other.error_registry)
                
            result = DimensionalArray(self.array @ other.array, combined_registry)
            
            # Propagate error information properly
            if self._error_id is not None or (hasattr(other, '_error_id') and other._error_id is not None):
                return self.propagate_error(other)._with_array(result.array)
            
            return result
        
        # For numpy array, convert to our type first
        return self @ DimensionalArray(other, self.error_registry)
    
    def __rmatmul__(self, other: np.ndarray) -> 'DimensionalArray':
        """Support right matrix multiplication with @ operator."""
        # Convert other to DimensionalArray and use our matmul
        return DimensionalArray(other, self.error_registry) @ self
    
    def __array__(self, dtype=None) -> np.ndarray:
        """Support numpy's array protocol."""
        if dtype is None:
            return self.array
        return self.array.astype(dtype)
    
    # Add common comparison operators
    def __eq__(self, other):
        """Support equality comparison."""
        if isinstance(other, DimensionalArray):
            result = DimensionalArray(self.array == other.array, self.error_registry)
            
            # Track special values (NaN, inf) for dimensional consistency
            if np.any(np.isnan(self.array)) or np.any(np.isnan(other.array)) or \
               np.any(np.isinf(self.array)) or np.any(np.isinf(other.array)):
                error_data = ErrorData(
                    original_shape=result.array.shape,
                    error_tensor=np.zeros_like(result.array),
                    reduction_type='comparison_with_special_values',
                    manifold_data={
                        'operation': 'equal',
                        'has_nan': np.any(np.isnan(self.array)) or np.any(np.isnan(other.array)),
                        'has_inf': np.any(np.isinf(self.array)) or np.any(np.isinf(other.array))
                    }
                )
                result._error_id = self.error_registry.store(error_data)
            
            return result
        
        result = DimensionalArray(self.array == other, self.error_registry)
        
        # Track special values for scalar comparisons
        if np.any(np.isnan(self.array)) or np.isnan(other) if isinstance(other, float) else False or \
           np.any(np.isinf(self.array)) or np.isinf(other) if isinstance(other, float) else False:
            error_data = ErrorData(
                original_shape=result.array.shape,
                error_tensor=np.zeros_like(result.array),
                reduction_type='comparison_with_special_values',
                manifold_data={
                    'operation': 'equal',
                    'has_nan': np.any(np.isnan(self.array)) or np.isnan(other) if isinstance(other, float) else False,
                    'has_inf': np.any(np.isinf(self.array)) or np.isinf(other) if isinstance(other, float) else False
                }
            )
            result._error_id = self.error_registry.store(error_data)
        
        return result
    
    def __ne__(self, other):
        """Support inequality comparison."""
        if isinstance(other, DimensionalArray):
            return DimensionalArray(self.array != other.array, self.error_registry)
        return DimensionalArray(self.array != other, self.error_registry)
    
    def __lt__(self, other):
        """Support less than comparison."""
        if isinstance(other, DimensionalArray):
            return DimensionalArray(self.array < other.array, self.error_registry)
        return DimensionalArray(self.array < other, self.error_registry)
    
    def __le__(self, other):
        """Support less than or equal comparison."""
        if isinstance(other, DimensionalArray):
            return DimensionalArray(self.array <= other.array, self.error_registry)
        return DimensionalArray(self.array <= other, self.error_registry)
    
    def __gt__(self, other):
        """Support greater than comparison."""
        if isinstance(other, DimensionalArray):
            return DimensionalArray(self.array > other.array, self.error_registry)
        return DimensionalArray(self.array > other, self.error_registry)
    
    def __ge__(self, other):
        """Support greater than or equal comparison."""
        if isinstance(other, DimensionalArray):
            return DimensionalArray(self.array >= other.array, self.error_registry)
        return DimensionalArray(self.array >= other, self.error_registry)
    
    def __neg__(self):
        """Support unary negation (-x)."""
        result = DimensionalArray(-self.array, self.error_registry)
        # Propagate error information
        if self._error_id is not None:
            result._error_id = self._error_id
        return result

    def __pos__(self):
        """Support unary positive (+x)."""
        result = DimensionalArray(+self.array, self.error_registry)
        # Propagate error information
        if self._error_id is not None:
            result._error_id = self._error_id
        return result

    def __abs__(self):
        """Support absolute value (abs(x))."""
        result = DimensionalArray(np.abs(self.array), self.error_registry)
        # Track information about sign changes
        sign_changes = np.sum(self.array < 0)
        if sign_changes > 0:
            error_data = ErrorData(
                original_shape=self.array.shape,
                error_tensor=(self.array < 0).astype(float),
                reduction_type='absolute_value',
                manifold_data={'sign_changes': sign_changes}
            )
            result._error_id = self.error_registry.store(error_data)
        elif self._error_id is not None:
            # Propagate existing error information
            result._error_id = self._error_id
        return result
    
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        """Support numpy's universal functions."""
        # Convert all inputs to numpy arrays
        numpy_inputs = []
        for input_obj in inputs:
            if isinstance(input_obj, DimensionalArray):
                numpy_inputs.append(input_obj.array)
            else:
                numpy_inputs.append(input_obj)
        
        # Apply the ufunc
        result = getattr(ufunc, method)(*numpy_inputs, **kwargs)
        
        # Convert result back to DimensionalArray if needed
        if isinstance(result, np.ndarray):
            return DimensionalArray(result, self.error_registry)
        elif isinstance(result, tuple):
            return tuple(DimensionalArray(r, self.error_registry) if isinstance(r, np.ndarray) else r for r in result)
        return result

    def dimensional_divide(self, other: Union['DimensionalArray', int, float, complex]) -> 'DimensionalArray':
        """
        Perform dimensionally-aware division that automatically selects the
        appropriate dimensional reduction for singularities.
        
        This method enhances the standard division operator with more comprehensive
        dimensional analysis and error tracking.
        
        Parameters:
            other: The divisor
            
        Returns:
            DimensionalArray: Result of division with dimensional handling
        """
        # Import registry items here to avoid circular imports
        from .registry import ErrorData
        
        if isinstance(other, DimensionalArray):
            # Analyze divisor for zeros or near-zeros using dimensional approach
            if np.any(np.isclose(other.array, 0)):
                # Create a mask of exact zeros and near-zeros
                exact_zeros = other.array == 0
                near_zeros = np.isclose(other.array, 0) & ~exact_zeros
                
                # Handle exact zeros through dimensional reduction
                result = np.zeros_like(self.array, dtype=float)
                
                # Process non-zero elements normally
                non_zero_mask = ~(exact_zeros | near_zeros)
                if np.any(non_zero_mask):
                    result[non_zero_mask] = self.array[non_zero_mask] / other.array[non_zero_mask]
                
                # Process near-zeros with scaling based on their proximity to zero
                if np.any(near_zeros):
                    # Use dimensional analysis to determine appropriate scaling
                    near_zero_values = other.array[near_zeros]
                    scales = np.abs(near_zero_values)
                    
                    # Track this special handling
                    near_zero_data = ErrorData(
                        original_shape=other.array.shape,
                        error_tensor=near_zero_values,
                        reduction_type='near_zero_division',
                        manifold_data={
                            'near_zero_indices': np.where(near_zeros),
                            'scales': scales
                        }
                    )
                    near_zero_id = self.error_registry.store(near_zero_data)
                    
                    # Apply scaled division for near-zeros
                    result[near_zeros] = (self.array[near_zeros] / scales) * (scales / near_zero_values)
                
                # Handle exact zeros with dimensional reduction
                if np.any(exact_zeros):
                    reduced = other._partial_divide_by_zero(exact_zeros)
                    result[exact_zeros] = self.array[exact_zeros] / reduced.array[exact_zeros]
                
                # Combine error registries
                combined_registry = self.error_registry.combine(other.error_registry)
                
                # Track the overall division operation
                div_data = ErrorData(
                    original_shape=self.array.shape,
                    error_tensor=np.zeros_like(self.array),
                    reduction_type='dimensional_division',
                    manifold_data={
                        'exact_zeros': np.sum(exact_zeros),
                        'near_zeros': np.sum(near_zeros),
                        'source_shapes': (self.array.shape, other.array.shape)
                    }
                )
                div_id = combined_registry.store(div_data)
                
                # Create result with proper error tracking
                dimensional_result = DimensionalArray(result, combined_registry)
                dimensional_result._error_id = div_id
                return dimensional_result
            
            # Normal division for non-zero divisors
            return self.__truediv__(other)
        
        # Handle scalar division
        if isinstance(other, (int, float, complex)) and other == 0:
            result = self._divide_by_zero()
            
            # Create specific error data
            error_data = ErrorData(
                original_shape=self.array.shape,
                error_tensor=np.zeros_like(self.array),
                reduction_type='dimensional_scalar_division',
                manifold_data={
                    'divisor': 0.0,
                    'source_error_id': self._error_id
                }
            )
            result._error_id = self.error_registry.store(error_data)
            return result
            
        # Normal scalar division
        return self.__truediv__(other)
    
    def dimensional_svd(self, full_matrices=True, compute_uv=True):
        """
        Perform dimensionally-aware SVD that tracks singular value structure.
        
        This method enhances the standard SVD with comprehensive dimensional
        analysis and error tracking for singular or near-singular matrices.
        
        Parameters:
            full_matrices: Whether to compute full U and Vt matrices
            compute_uv: Whether to compute U and Vt in addition to s
            
        Returns:
            tuple: (U, s, Vt) or s, depending on compute_uv
        """
        # Import registry items here to avoid circular imports
        from .registry import ErrorData
        from . import linalg  # Import here to avoid circular imports
        
        # Use our own SVD implementation
        if compute_uv:
            U, s, Vt = linalg.svd(self.array, full_matrices=full_matrices)
            
            # Analyze singular value structure
            sv_ratio = s / s[0] if s.size > 0 and s[0] > 0 else np.zeros_like(s)
            
            # Identify near-zero singular values using dimensional approach
            # instead of arbitrary thresholds
            is_rank_deficient = False
            min_nonzero_ratio = None
            
            if s.size > 1:
                # Find smallest non-zero singular value ratio
                nonzero_ratios = sv_ratio[sv_ratio > 0]
                if nonzero_ratios.size > 0:
                    min_nonzero_ratio = np.min(nonzero_ratios)
                    
                    # Check for rank deficiency based on structure
                    gaps = np.diff(np.log10(s[s > 0]) if np.any(s > 0) else [])
                    if gaps.size > 0 and np.max(gaps) > 3:  # Gap of 3 orders of magnitude
                        is_rank_deficient = True
            
            # Track singular value structure
            sv_data = ErrorData(
                original_shape=s.shape,
                error_tensor=s,
                reduction_type='dimensional_svd',
                manifold_data={
                    'singular_values': s,
                    'sv_ratio': sv_ratio,
                    'is_rank_deficient': is_rank_deficient,
                    'min_nonzero_ratio': min_nonzero_ratio
                }
            )
            sv_id = self.error_registry.store(sv_data)
            
            # Create dimensional results
            u_dim = DimensionalArray(U, self.error_registry)
            s_dim = DimensionalArray(s, self.error_registry)
            vt_dim = DimensionalArray(Vt, self.error_registry)
            
            # Set error IDs
            s_dim._error_id = sv_id
            
            return u_dim, s_dim, vt_dim
        else:
            s = linalg.svd(self.array, compute_uv=False)
            
            # Track singular values
            sv_data = ErrorData(
                original_shape=s.shape,
                error_tensor=s,
                reduction_type='dimensional_svd_values_only',
                manifold_data={'singular_values': s}
            )
            sv_id = self.error_registry.store(sv_data)
            
            # Create dimensional result
            s_dim = DimensionalArray(s, self.error_registry)
            s_dim._error_id = sv_id
            
            return s_dim

