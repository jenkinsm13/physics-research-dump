"""
Transfinite tensor operations for quantum calculations.

This module extends the tensor framework to handle operations on tensors with
transfinite dimensions, particularly useful for calculations involving
quantum fields in infinite-dimensional spaces and cosmological constants.
"""

import numpy as np
from typing import Union, Optional, List, Tuple, Dict
from .ordinal import Ordinal, TransfiniteSum
from .tensor import QuantumTensor
from ..array import DimensionalArray
from ..exceptions import DimensionalError
import mpmath as mp

class TransfiniteTensor(QuantumTensor):
    """
    Tensor class that properly handles transfinite dimensions.
    
    Extends QuantumTensor to work with infinite-dimensional spaces,
    implementing proper handling of operations that extend beyond
    finite dimensions.
    """
    
    def __init__(self, data: Union[np.ndarray, List],
                 ordinal_dims: Optional[List[Ordinal]] = None,
                 convergence_rates: Optional[Dict[int, float]] = None):
        """
        Initialize a transfinite tensor.
        
        Parameters
        ----------
        data : array_like
            Tensor data for finite part
        ordinal_dims : list of Ordinal, optional
            Ordinal dimensions for each axis
        convergence_rates : dict, optional
            Convergence rates for each transfinite dimension
        """
        super().__init__(data)
        self.ordinal_dims = ordinal_dims or [Ordinal(d) for d in data.shape]
        self.convergence_rates = convergence_rates or {}
        
        # Validate dimensions
        if any(not isinstance(d, Ordinal) for d in self.ordinal_dims):
            raise DimensionalError("All dimensions must be Ordinal objects")
    
    def _extend_to_transfinite(self, axis: int, limit: Ordinal) -> 'TransfiniteTensor':
        """
        Extend tensor along specified axis to transfinite dimension.
        
        Uses convergence properties to properly handle the extension.
        """
        if axis >= len(self.ordinal_dims):
            raise DimensionalError(f"Invalid axis {axis}")
        
        # Get convergence rate for this axis
        rate = self.convergence_rates.get(axis, 1.0)
        
        # Create extension function
        def extend_func(idx: Union[int, Ordinal]) -> np.ndarray:
            if isinstance(idx, (int, float)):
                if idx < self.shape[axis]:
                    return self.take(idx, axis)
                # Exponential decay for extension
                scale = np.exp(-rate * (idx - self.shape[axis]))
                return self.take(-1, axis) * scale
            else:
                # Handle transfinite index
                if idx.is_finite:
                    return extend_func(idx.value)
                # Rapid decay for transfinite indices
                scale = np.exp(-rate * idx.base_omega_multiple)
                return self.take(-1, axis) * scale
        
        # Create extended tensor
        extended_shape = list(self.shape)
        extended_shape[axis] = float('inf')
        extended_data = np.zeros(extended_shape)
        
        # Fill finite part
        for i in range(self.shape[axis]):
            extended_data[..., i, ...] = self.take(i, axis)
        
        # Create new tensor with extended data
        extended_dims = self.ordinal_dims.copy()
        extended_dims[axis] = limit
        
        return TransfiniteTensor(extended_data, 
                               ordinal_dims=extended_dims,
                               convergence_rates=self.convergence_rates)
    
    def contract(self, other: 'TransfiniteTensor', 
                axes: Tuple[int, int]) -> 'TransfiniteTensor':
        """
        Contract this tensor with another along specified axes.
        
        Properly handles contraction when one or both axes are transfinite.
        """
        axis1, axis2 = axes
        
        # Check if either dimension is transfinite
        dim1 = self.ordinal_dims[axis1]
        dim2 = other.ordinal_dims[axis2]
        
        if dim1.is_finite and dim2.is_finite:
            # Standard finite contraction
            return super().contract(other, axes)
        
        # At least one dimension is transfinite
        # Use TransfiniteSum for the contraction
        def contract_term(idx: Union[int, Ordinal]) -> np.ndarray:
            slice1 = self.take(idx, axis1)
            slice2 = other.take(idx, axis2)
            return np.tensordot(slice1, slice2, 0)
        
        # Create transfinite sum object
        sum_obj = TransfiniteSum(
            contract_term,
            ordinal_start=0,
            ordinal_limit=max(dim1, dim2, key=lambda x: x.base_omega_multiple),
            convergence_rate=min(self.convergence_rates.get(axis1, 1.0),
                               other.convergence_rates.get(axis2, 1.0))
        )
        
        # Evaluate the contraction
        result = sum_obj.evaluate()
        
        # Create new tensor with contracted dimensions removed
        new_shape = list(self.shape)
        new_shape.pop(axis1)
        new_dims = self.ordinal_dims.copy()
        new_dims.pop(axis1)
        
        return TransfiniteTensor(result,
                               ordinal_dims=new_dims,
                               convergence_rates=self.convergence_rates)
    
    def trace(self, axis1: int, axis2: int) -> 'TransfiniteTensor':
        """
        Compute trace along two axes.
        
        Handles traces involving transfinite dimensions using proper
        limit operations.
        """
        # Check if dimensions match
        if self.ordinal_dims[axis1] != self.ordinal_dims[axis2]:
            raise DimensionalError("Trace axes must have same dimension")
        
        dim = self.ordinal_dims[axis1]
        if dim.is_finite:
            # Standard finite trace
            return super().trace(axis1, axis2)
        
        # Transfinite trace
        def trace_term(idx: Union[int, Ordinal]) -> np.ndarray:
            return np.trace(self.take(idx, axis1), axis1=0, axis2=1)
        
        # Create transfinite sum
        sum_obj = TransfiniteSum(
            trace_term,
            ordinal_start=0,
            ordinal_limit=dim,
            convergence_rate=self.convergence_rates.get(axis1, 1.0)
        )
        
        # Evaluate trace
        result = sum_obj.evaluate()
        
        # Remove traced dimensions
        new_shape = list(self.shape)
        new_shape.pop(max(axis1, axis2))
        new_shape.pop(min(axis1, axis2))
        new_dims = self.ordinal_dims.copy()
        new_dims.pop(max(axis1, axis2))
        new_dims.pop(min(axis1, axis2))
        
        return TransfiniteTensor(result,
                               ordinal_dims=new_dims,
                               convergence_rates=self.convergence_rates)
    
    def norm(self, ord: Optional[Union[int, float, str]] = None) -> float:
        """
        Compute norm of tensor, properly handling transfinite dimensions.
        
        Uses convergence properties to compute meaningful norms even
        for infinite-dimensional tensors.
        """
        if all(d.is_finite for d in self.ordinal_dims):
            # Standard finite norm
            return super().norm(ord)
        
        # For transfinite dimensions, use convergence properties
        # to compute a finite norm
        def norm_term(idx: Union[int, Ordinal]) -> float:
            if isinstance(idx, (int, float)):
                slice_data = self.take(idx, 0)
                return float(np.linalg.norm(slice_data, ord=ord))
            else:
                # Rapid decay for transfinite indices
                rate = self.convergence_rates.get(0, 1.0)
                scale = np.exp(-rate * idx.base_omega_multiple)
                return float(np.linalg.norm(self.take(-1, 0), ord=ord)) * scale
        
        # Sum over all dimensions
        sum_obj = TransfiniteSum(
            norm_term,
            ordinal_start=0,
            ordinal_limit=max(self.ordinal_dims, key=lambda x: x.base_omega_multiple),
            convergence_rate=min(self.convergence_rates.values())
        )
        
        return sum_obj.evaluate()
    
    def to_matrix(self) -> np.ndarray:
        """
        Convert to matrix representation if possible.
        
        For transfinite tensors, returns the finite part with
        a warning about truncation.
        """
        if all(d.is_finite for d in self.ordinal_dims):
            return super().to_matrix()
        
        print("Warning: Converting transfinite tensor to matrix. "
              "Only finite part will be returned.")
        return self.data
    
    def __str__(self) -> str:
        """String representation of transfinite tensor"""
        dims_str = ' × '.join(str(d) for d in self.ordinal_dims)
        return f"TransfiniteTensor of shape {dims_str}"
    
    def __repr__(self) -> str:
        return str(self)

def shell_coupling_tensor(n_shells: int,
                        coupling_func: callable,
                        extend_to_transfinite: bool = False) -> TransfiniteTensor:
    """
    Create a tensor representing coupling between temporal shells.
    
    Parameters
    ----------
    n_shells : int
        Number of finite shells
    coupling_func : callable
        Function computing coupling strength between shells
    extend_to_transfinite : bool
        Whether to extend to transfinite shells
    
    Returns
    -------
    TransfiniteTensor
        Tensor representing shell couplings
    """
    # Create coupling matrix for finite shells
    coupling_matrix = np.zeros((n_shells, n_shells))
    for i in range(n_shells):
        for j in range(n_shells):
            coupling_matrix[i, j] = coupling_func(i, j)
    
    # Create basic tensor
    tensor = TransfiniteTensor(
        coupling_matrix,
        ordinal_dims=[Ordinal(n_shells), Ordinal(n_shells)]
    )
    
    if extend_to_transfinite:
        # Extend to transfinite dimensions
        tensor = tensor._extend_to_transfinite(0, Ordinal('w'))
        tensor = tensor._extend_to_transfinite(1, Ordinal('w'))
    
    return tensor

def compute_shell_flow(coupling_tensor: TransfiniteTensor,
                      direction: str = 'forward') -> TransfiniteTensor:
    """
    Compute temporal flow between shells.
    
    Parameters
    ----------
    coupling_tensor : TransfiniteTensor
        Tensor of shell couplings
    direction : str
        'forward' for future→past or 'inverse' for past→future
    
    Returns
    -------
    TransfiniteTensor
        Tensor representing flow between shells
    """
    if direction not in ['forward', 'inverse']:
        raise ValueError("direction must be 'forward' or 'inverse'")
    
    # Create flow tensor
    def flow_func(i: Union[int, Ordinal], j: Union[int, Ordinal]) -> float:
        if isinstance(i, (int, float)) and isinstance(j, (int, float)):
            if direction == 'forward' and i >= j:
                return 0.0
            if direction == 'inverse' and i <= j:
                return 0.0
            return float(coupling_tensor.data[int(i), int(j)])
        
        # Handle transfinite indices
        if not isinstance(i, Ordinal):
            i = Ordinal(i)
        if not isinstance(j, Ordinal):
            j = Ordinal(j)
        
        if direction == 'forward' and i >= j:
            return 0.0
        if direction == 'inverse' and i <= j:
            return 0.0
        
        # Compute flow with rapid decay for transfinite indices
        base_flow = coupling_tensor.data[-1, -1]
        scale = np.exp(-abs(i.base_omega_multiple - j.base_omega_multiple))
        return float(base_flow * scale)
    
    # Create tensor with same dimensions as coupling tensor
    flow_tensor = TransfiniteTensor(
        np.zeros_like(coupling_tensor.data),
        ordinal_dims=coupling_tensor.ordinal_dims,
        convergence_rates=coupling_tensor.convergence_rates
    )
    
    # Fill tensor
    for i in range(flow_tensor.shape[0]):
        for j in range(flow_tensor.shape[1]):
            flow_tensor.data[i, j] = flow_func(i, j)
    
    return flow_tensor 