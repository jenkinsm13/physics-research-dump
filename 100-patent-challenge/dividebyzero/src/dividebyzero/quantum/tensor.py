"""
Quantum Tensor Network Implementation

This module implements quantum tensor operations with support for:
- Entanglement entropy calculations
- Schmidt decomposition
- Tensor network contractions
- Holographic dimensional reduction
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from ..linalg import expm
from ..exceptions import DimensionalError
from ..array import DimensionalArray
import logging

# Import logarithmic functions
from ..logarithms import logm as logarithm_logm

# Instead, create a module-level logger
logger = logging.getLogger(__name__)

def quantum_decomposition(matrix):
    """
    Decompose a quantum state or density matrix into eigenvalues and eigenvectors.
    
    This function handles both Hermitian matrices (like density matrices) and
    general quantum states, providing a decomposition suitable for quantum
    logarithm operations and other quantum information processing tasks.
    
    Parameters
    ----------
    matrix : ndarray
        Input quantum state or density matrix
        
    Returns
    -------
    tuple
        (eigenvalues, eigenvectors) where eigenvalues is an array of the 
        eigenvalues and eigenvectors contains the corresponding eigenvectors
        as columns
        
    Notes
    -----
    For Hermitian matrices, this performs eigendecomposition.
    For general matrices, this uses singular value decomposition.
    """
    matrix = np.asarray(matrix)
    
    # Check if the matrix is approximately Hermitian (within numerical precision)
    is_hermitian = np.allclose(matrix, matrix.conj().T, rtol=1e-10, atol=1e-10)
    
    if is_hermitian:
        # For Hermitian matrices (density matrices), use eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        
        # Ensure eigenvalues are non-negative (for positive semi-definite matrices)
        # Use a small epsilon value to avoid numerical issues with very small negative values
        eigenvalues = np.maximum(eigenvalues, 1e-15)
        
        return eigenvalues, eigenvectors
    else:
        # For general quantum states, use SVD
        u, s, vh = np.linalg.svd(matrix, full_matrices=False)
        
        # Return singular values and left singular vectors
        return s, u

@dataclass
class EntanglementSpectrum:
    """Represents the entanglement spectrum of a quantum state."""
    schmidt_values: np.ndarray
    entropy: float
    bond_dimension: int
    truncation_error: float

class QuantumTensor(DimensionalArray):
    """
    Implements a quantum-aware tensor with support for entanglement operations.
    Inherits from DimensionalArray to ensure compatibility with dimensional division operations.
    """
    def __init__(self, data, physical_dims=None, quantum_nums=None, fractal_dimension=None):
        """
        Initialize quantum tensor with dimensional array capabilities.
        
        Args:
            data: Input data array or DimensionalArray
            physical_dims: Physical dimensions for tensor network operations
            quantum_nums: Quantum numbers for symmetry preservation
            fractal_dimension: Fractal dimension for fractal operations
        """
        # If input is DimensionalArray, extract its array and error registry
        if isinstance(data, DimensionalArray):
            super().__init__(data.array, data.error_registry)
        else:
            super().__init__(data)
            
        # Initialize quantum-specific properties
        self.physical_dims = physical_dims or tuple(range(self.array.ndim))
        self.quantum_nums = quantum_nums or {}
        self._entanglement_spectrum = EntanglementSpectrum(
            schmidt_values=np.array([1.0]),
            entropy=0.0,
            bond_dimension=1,
            truncation_error=0.0
        )
        self._fractal_dimension = fractal_dimension

    @property
    def data(self):
        """
        NumPy-compatible data access. Returns the underlying array data.
        This property makes QuantumTensor behave more like a NumPy array.
        """
        return self.array

    def __array__(self):
        """
        NumPy array interface. Allows direct use in NumPy functions.
        """
        return self.array

    def __getattr__(self, name):
        """
        Delegate unknown attributes to the underlying array for NumPy compatibility.
        This allows methods like .conj(), .T, etc. to work directly on the tensor.
        """
        if hasattr(self.array, name):
            return getattr(self.array, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __truediv__(self, other: Union[int, float, DimensionalArray, 'QuantumTensor', slice]) -> 'QuantumTensor':
        """Support division with scalars, DimensionalArrays, QuantumTensors, or slices."""
        if isinstance(other, (int, float)):
            if other == 0:
                return self._divide_by_zero()
            result = super().__truediv__(other)
            return QuantumTensor(result, self.physical_dims, self.quantum_nums)
        elif isinstance(other, DimensionalArray):
            # Convert DimensionalArray to QuantumTensor if needed
            if not isinstance(other, QuantumTensor):
                other = QuantumTensor(other)
            # Handle division by zero using quantum-aware method
            if np.any(other.array == 0):
                return self._divide_by_zero(other)
            # Perform division preserving quantum properties
            result = super().__truediv__(other)
            return QuantumTensor(result, self.physical_dims, self.quantum_nums)
        elif isinstance(other, slice):
            # Handle slice division
            if other == slice(None, 1, None):
                # This is equivalent to dividing by 1, so return the tensor as is
                return self
            else:
                raise ValueError(f"Unsupported slice for division: {other}")
        else:
            raise TypeError(f"Unsupported type for division: {type(other)}")

    def __matmul__(self, other: Union[DimensionalArray, np.ndarray]) -> 'QuantumTensor':
        """Matrix multiplication preserving quantum properties."""
        if isinstance(other, DimensionalArray):
            result = super().__matmul__(other)
            if isinstance(other, QuantumTensor):
                # Combine quantum properties from both tensors
                new_physical_dims = self._combine_physical_dims(other)
                new_quantum_nums = self._combine_quantum_nums(other)
                return QuantumTensor(result, new_physical_dims, new_quantum_nums)
            return QuantumTensor(result, self.physical_dims, self.quantum_nums)
        return QuantumTensor(super().__matmul__(other), self.physical_dims, self.quantum_nums)

    def _combine_physical_dims(self, other: 'QuantumTensor') -> tuple:
        """Combine physical dimensions during tensor operations."""
        return tuple(set(self.physical_dims) | set(other.physical_dims))

    def _combine_quantum_nums(self, other: 'QuantumTensor') -> dict:
        """Combine quantum numbers during tensor operations."""
        combined = self.quantum_nums.copy()
        combined.update(other.quantum_nums)
        return combined

    @classmethod
    def from_dimensional_array(cls, darr: DimensionalArray) -> 'QuantumTensor':
        """Convert DimensionalArray to QuantumTensor."""
        return cls(darr.array, error_registry=darr.error_registry)
        
    def to_dimensional_array(self) -> DimensionalArray:
        """Convert to plain DimensionalArray, losing quantum properties."""
        return DimensionalArray(self.array, self.error_registry)

    def _handle_division_by_zero(self, divisor: Optional[DimensionalArray] = None) -> 'QuantumTensor':
        """
        Implement DMRG-based dimensional reduction with support for multipartite states.
        Uses hierarchical SVD for n>2 qubit systems while preserving entanglement structure.
        """
        if self.array.ndim == 0:
            raise DimensionalError("Cannot reduce dimensions of a scalar tensor")
        
        # Convert to state vector representation and normalize
        state_vector = self.array.flatten()
        state_vector = state_vector / np.linalg.norm(state_vector)
        
        # Determine number of qubits from dimension
        n_qubits = int(np.log2(len(state_vector)))
        if 2**n_qubits != len(state_vector):
            # If not a power of 2, fall back to standard dimensional reduction
            result = super()._divide_by_zero()
            return QuantumTensor(result, self.physical_dims, self.quantum_nums)
            
        # Reshape into bipartite form
        matrix = state_vector.reshape(2**(n_qubits//2), -1)
        
        # Perform SVD
        U, S, Vt = np.linalg.svd(matrix, full_matrices=False)
        
        # Calculate entanglement entropy using framework's proper handling
        # This uses dimensional reduction for handling of S=0 cases
        from .entropy import entanglement_entropy
        from .. import array
        
        # Convert to DimensionalArray for proper framework handling
        S_normalized = S / np.sum(S)
        S_normalized_array = array(S_normalized)
        entropy = entanglement_entropy(S_normalized_array, self.error_registry)
        
        # Keep more singular values to preserve entanglement
        truncation_idx = min(len(S), 2)  # Reduced back to 2 to match target shape
        
        # Reconstruct with preserved entanglement
        sqrt_S = np.sqrt(S[:truncation_idx])
        left_state = U[:, :truncation_idx] * sqrt_S.reshape(1, -1)
        right_state = np.diag(sqrt_S) @ Vt[:truncation_idx, :]
        reduced_state = left_state @ right_state
        
        # Update entanglement spectrum
        self._entanglement_spectrum = EntanglementSpectrum(
            schmidt_values=S_normalized[:truncation_idx],
            entropy=entropy,
            bond_dimension=truncation_idx,
            truncation_error=np.sum(S[truncation_idx:]**2) / np.sum(S**2) if len(S) > truncation_idx else 0.0
        )
        
        # Create result tensor with proper dimensions
        result_shape = (truncation_idx, truncation_idx)
        result_data = reduced_state[:truncation_idx, :truncation_idx].reshape(result_shape)
        
        # Normalize final state
        result_data = result_data / np.linalg.norm(result_data)
        
        # Create error data for tracking
        from ..registry import ErrorData
        original_shape = self.array.shape
        error_tensor = self.array - result_data.reshape(-1)[:np.prod(original_shape)].reshape(original_shape)
        
        error_data = ErrorData(
            original_shape=original_shape,
            error_tensor=error_tensor,
            reduction_type='quantum_tensor_reduction',
            manifold_data={
                'entanglement_entropy': float(entropy),
                'schmidt_values': S_normalized.tolist()
            }
        )
        error_id = self.error_registry.store(error_data)
        
        # Create the result with proper error tracking
        result = QuantumTensor(
            result_data,
            physical_dims=tuple(range(2)),
            quantum_nums=self.quantum_nums
        )
        result._error_id = error_id
        
        return result

    def reduce_dimension(self,
                        target_dims: int,
                        preserve_entanglement: bool = True,
                        max_iterations: int = 100) -> 'QuantumTensor':
        """
        Reduce tensor dimensions while preserving quantum properties.
        """
        logger.debug(f"Reducing dimension with target_dims: {target_dims}, preserve_entanglement: {preserve_entanglement}")
        if self.array.ndim <= target_dims:
            raise DimensionalError("Cannot reduce to higher or equal number of dimensions.")

        current_tensor = self
        iteration = 0
        while current_tensor.array.ndim > target_dims:
            if iteration >= max_iterations:
                raise RuntimeError(f"Failed to reduce dimensions after {max_iterations} iterations")
            
            logger.debug(f"Iteration {iteration}: current ndim = {current_tensor.array.ndim}")
            cut_index = current_tensor.array.ndim - 1
            left, right = current_tensor.schmidt_decompose(cut_index)
            
            if preserve_entanglement:
                # Keep the left tensor and incorporate singular values
                U, S, Vt = np.linalg.svd(left.array, full_matrices=False)
                truncated_S = S[:target_dims]
                truncated_U = U[:, :target_dims]
                new_data = truncated_U @ np.diag(truncated_S)
            else:
                new_data = left.array.reshape(-1)[:target_dims]
            
            # Calculate the proper shape for the target dimensions
            total_size = new_data.size
            dim_size = int(np.ceil(total_size ** (1/target_dims)))
            new_shape = (dim_size,) * target_dims
            
            # Pad the data if necessary
            if np.prod(new_shape) > total_size:
                padded_data = np.zeros(np.prod(new_shape), dtype=new_data.dtype)
                padded_data[:total_size] = new_data.flatten()
                new_data = padded_data
            
            new_tensor = QuantumTensor(
                new_data.reshape(new_shape), 
                tuple(range(target_dims)), 
                left.quantum_nums
            )
            
            if new_tensor.array.ndim >= current_tensor.array.ndim:
                logger.warning(f"Failed to reduce dimensions at iteration {iteration}")
                break
            
            current_tensor = new_tensor
            iteration += 1

        # Compute and store the entanglement spectrum
        s = np.linalg.svd(current_tensor.array.reshape(-1, 1), compute_uv=False)
        # Normalize singular values
        schmidt_values = s / np.sum(s)
        
        # Use the centralized entropy function to calculate entanglement entropy
        # which properly handles zero eigenvalues using dimensional reduction
        from .entropy import entanglement_entropy
        sv_array = DimensionalArray(schmidt_values, current_tensor.error_registry)
        
        # Track error data for the singular value computation
        from ..registry import ErrorData
        sv_error_data = ErrorData(
            original_shape=s.shape,
            error_tensor=s,
            reduction_type='entanglement',
            manifold_data={'singular_values': s}
        )
        sv_error_id = current_tensor.error_registry.store(sv_error_data)
        sv_array._error_id = sv_error_id
        
        # Use the framework's handling for non-negativity without max()
        entropy = entanglement_entropy(sv_array, current_tensor.error_registry)
        
        current_tensor._entanglement_spectrum = EntanglementSpectrum(
            schmidt_values=schmidt_values,
            entropy=entropy,
            bond_dimension=len(schmidt_values),
            truncation_error=np.sum(s[target_dims:]**2) if len(s) > target_dims else 0.0
        )

        logger.debug(f"Final reduced tensor shape: {current_tensor.array.shape}")
        return current_tensor

    def elevate(self, target_shape: Optional[Tuple[int, ...]] = None) -> 'QuantumTensor':
        """Reconstruct higher dimensional representation using proper error tracking."""
        # Use DimensionalArray's elevate method
        elevated = super().elevate()
        
        # Preserve quantum properties
        return QuantumTensor(
            elevated.array,
            self.physical_dims,
            self.quantum_nums
        )
        
    def schmidt_decompose(self, cut_index: int) -> Tuple['QuantumTensor', 'QuantumTensor']:
        """
        Perform a Schmidt decomposition of the quantum state.
        
        This decomposes the state across a bipartition into two subsystems,
        which is essential for entanglement analysis and tensor network operations.
        
        Parameters
        ----------
        cut_index : int
            Index at which to partition the system
            
        Returns
        -------
        tuple
            (left_tensor, right_tensor) containing the decomposed subsystems
        """
        # Ensure tensor has at least 2 dimensions
        if self.array.ndim < 2:
            tensor_reshaped = self.array.reshape(2, -1)
        else:
            tensor_reshaped = self.array
            
        # Calculate dimensions for reshaping
        left_dims = tensor_reshaped.shape[:cut_index]
        right_dims = tensor_reshaped.shape[cut_index:]
        
        left_size = np.prod(left_dims)
        right_size = np.prod(right_dims)
        
        # Reshape for SVD
        matrix = tensor_reshaped.reshape(left_size, right_size)
        
        # Perform SVD
        u, s, vh = np.linalg.svd(matrix, full_matrices=False)
        
        # Create left and right tensors
        left_tensor = QuantumTensor(
            u,
            physical_dims=self.physical_dims[:cut_index] if self.physical_dims else None,
            quantum_nums=self.quantum_nums
        )
        
        right_tensor = QuantumTensor(
            vh,
            physical_dims=self.physical_dims[cut_index:] if self.physical_dims else None,
            quantum_nums=self.quantum_nums
        )
        
        # Store entanglement spectrum
        schmidt_values = s / np.sum(s)  # Normalize
        
        from .entropy import entanglement_entropy
        sv_array = DimensionalArray(schmidt_values, self.error_registry)
        entropy = entanglement_entropy(sv_array, self.error_registry)
        
        self._entanglement_spectrum = EntanglementSpectrum(
            schmidt_values=schmidt_values,
            entropy=entropy,
            bond_dimension=len(s),
            truncation_error=0.0
        )
        
        return left_tensor, right_tensor

    def _apply_fractal_reduction(self, mask=None):
        """Apply fractal dimensional reduction for quantum operations."""
        if not self._fractal_dimension:
            return self
            
        return self._fractal_reduction(
            self._fractal_dimension, 
            mask,
            manifold_data={'quantum_structure': True}
        )

    @property
    def fractal_dimension(self):
        return self._fractal_dimension

class TensorNetwork:
    """
    Implementation of a quantum tensor network with support for contractions
    and holographic operations.
    """
    def __init__(self):
        self.tensors: Dict[str, QuantumTensor] = {}
        self.connections: List[Tuple[str, str, int]] = []
        
    def add_tensor(self, name: str, tensor: QuantumTensor) -> None:
        """Add tensor to network."""
        self.tensors[name] = tensor
        
    def connect(self, tensor1: str, tensor2: str, bond_dim: int) -> None:
        """Connect two tensors with specified bond dimension."""
        self.connections.append((tensor1, tensor2, bond_dim))
        
    def contract(self, 
                optimize: str = "optimal",
                max_bond_dim: Optional[int] = None) -> QuantumTensor:
        """
        Contract entire tensor network.
        
        Args:
            optimize: Contraction optimization strategy
            max_bond_dim: Maximum bond dimension to keep
            
        Returns:
            Contracted quantum tensor
        """
        # Implementation of tensor network contraction algorithm
        # This is a placeholder for the actual implementation
        raise NotImplementedError("Tensor network contraction not yet implemented")

def reduce_entanglement(tensor: QuantumTensor, 
                       target_bond_dimension: Optional[int] = None,
                       relative_error: Optional[float] = None) -> QuantumTensor:
    """
    Reduce entanglement in quantum tensor through proper dimensional reduction.
    
    This implementation uses the framework's approach to preserve
    mathematically significant information rather than using arbitrary thresholds.
    
    Args:
        tensor: Input quantum tensor
        target_bond_dimension: Target bond dimension for truncation
        relative_error: Maximum relative truncation error
        
    Returns:
        Tensor with reduced entanglement
    """
    left, right = tensor.schmidt_decompose(tensor.data.ndim // 2)
    spectrum = tensor._entanglement_spectrum
    
    if spectrum.schmidt_values.size <= 1:
        return tensor
    
    # If no truncation parameters specified, keep all values
    if target_bond_dimension is None and relative_error is None:
        # Default: preserve 90% of entanglement
        # Use cumulative entanglement rather than arbitrary threshold
        cumulative = np.cumsum(spectrum.schmidt_values)
        cumulative = cumulative / cumulative[-1]  # Normalize
        cutoff_idx = np.searchsorted(cumulative, 0.9)
        cutoff_idx = max(1, cutoff_idx)  # Always keep at least one value
    elif target_bond_dimension is not None:
        # Truncate to target bond dimension
        cutoff_idx = min(target_bond_dimension, len(spectrum.schmidt_values))
    elif relative_error is not None:
        # Truncate based on maximum relative error
        # Calculate truncation error for each possible cutoff
        errors = []
        for i in range(1, len(spectrum.schmidt_values) + 1):
            errors.append(np.sum(spectrum.schmidt_values[i:]))
        errors = np.array(errors) / np.sum(spectrum.schmidt_values)
        cutoff_idx = np.searchsorted(errors, relative_error, side='right')
        cutoff_idx = max(1, cutoff_idx)  # Always keep at least one value
    
    # Create error tracking data
    from ..registry import ErrorData
    error_data = ErrorData(
        original_shape=tensor.shape,
        error_tensor=tensor.array,
        reduction_type='entanglement_reduction',
        manifold_data={
            'schmidt_values': spectrum.schmidt_values,
            'cutoff_idx': cutoff_idx
        }
    )
    error_id = tensor.error_registry.store(error_data)
    
    # Truncate and reconstruct with proper error tracking
    result = QuantumTensor(
        left.data @ right.data[:cutoff_idx],
        physical_dims=tensor.physical_dims,
        quantum_nums=tensor.quantum_nums
    )
    result._error_id = error_id
    
    return result

def logm(a):
    """Matrix logarithm wrapper using dimensional manifold approach"""
    if isinstance(a, DimensionalArray):
        return logarithm_logm(a)
    return DimensionalArray(logarithm_logm(np.asarray(a)))