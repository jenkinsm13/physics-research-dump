"""
Quantum entropy calculations with proper dimensional reduction handling.

This module implements various quantum entropy calculations using the DivideByZero
framework's dimensional reduction approach to properly handle mathematical singularities.
It provides a unified interface for entropy calculations while maintaining mathematical
correctness and information conservation.
"""

import numpy as np
from typing import Optional, Union, Tuple
from ..array import DimensionalArray
from ..registry import ErrorData
from ..exceptions import DimensionalError

# Import specialized framework functions for proper singularity handling
from ..logarithms import log
from ..powers import power

class EntropyOperator:
    """
    Operator for calculating quantum entropy measures with proper dimensional handling.
    
    This class implements various quantum entropy calculations using the DivideByZero
    framework's dimensional reduction approach to properly handle mathematical singularities
    and maintain information conservation across different entropy measures.
    
    Attributes:
        error_registry: Registry for tracking dimensional operations and singularities
    """
    
    def __init__(self, error_registry=None):
        """
        Initialize the entropy operator.
        
        Parameters:
            error_registry: Registry for tracking dimensional operations
        """
        self.error_registry = error_registry
    
    def von_neumann(self, rho: DimensionalArray) -> float:
        """
        Calculate von Neumann entropy S(ρ) = -Tr(ρ log ρ).
        
        Parameters:
            rho: Density matrix
            
        Returns:
            float: von Neumann entropy
        """
        return von_neumann_entropy(rho, self.error_registry)
    
    def renyi(self, rho: DimensionalArray, alpha: float = 2.0) -> float:
        """
        Calculate Rényi entropy of order alpha.
        
        Parameters:
            rho: Density matrix
            alpha: Rényi parameter (α ≠ 1)
            
        Returns:
            float: Rényi entropy of order alpha
        """
        return renyi_entropy(rho, alpha, self.error_registry)
    
    def log_negativity(self, rho: DimensionalArray, dims: Optional[Tuple[int, int]] = None) -> float:
        """
        Calculate logarithmic negativity for entanglement quantification.
        
        Parameters:
            rho: Density matrix for a bipartite system
            dims: Dimensions of the two subsystems, inferred from shape if not provided
            
        Returns:
            float: Logarithmic negativity
        """
        return log_negativity(rho, dims, self.error_registry)
    
    def entanglement(self, schmidt_values: DimensionalArray) -> float:
        """
        Calculate entanglement entropy from Schmidt values.
        
        Parameters:
            schmidt_values: Schmidt values (normalized)
            
        Returns:
            float: Entanglement entropy
        """
        return entanglement_entropy(schmidt_values, self.error_registry)
    
    def relative(self, rho: DimensionalArray, sigma: DimensionalArray) -> float:
        """
        Calculate quantum relative entropy S(ρ||σ) = Tr[ρ(log ρ - log σ)].
        
        Parameters:
            rho: First density matrix
            sigma: Second density matrix
            
        Returns:
            float: Relative entropy
        """
        return relative_entropy(rho, sigma, self.error_registry)

def von_neumann_entropy(rho: DimensionalArray, error_registry=None) -> float:
    """
    Calculate von Neumann entropy S(ρ) = -Tr(ρ log ρ).
    
    This implementation properly handles zero eigenvalues through the DivideByZero
    framework's dimensional reduction approach, preserving the mathematical
    property that lim(x→0) x*log(x) = 0 while maintaining information conservation.
    
    Parameters
    ----------
    rho : DimensionalArray
        Density matrix
    error_registry : ErrorRegistry, optional
        Registry for tracking dimensional operations
        
    Returns
    -------
    float
        von Neumann entropy
    """
    from .. import linalg, sum
    
    # Ensure proper error registry
    if error_registry is None and hasattr(rho, 'error_registry'):
        error_registry = rho.error_registry
    
    # Convert to proper array type if needed
    if not isinstance(rho, DimensionalArray):
        from .. import array
        rho = array(rho)
    
    # Ensure normalization using proper framework approach
    trace = np.trace(rho.array)
    
    # Track normalization information
    norm_data = ErrorData(
        original_shape=(1,),
        error_tensor=np.array([float(trace)]),
        reduction_type='density_matrix_normalization',
        manifold_data={'target_trace': 1.0}
    )
    
    # Normalize without arbitrary threshold
    if trace != 1.0:
        # Use framework division to maintain dimensional consistency
        rho = rho / trace
        
        if error_registry is not None:
            error_registry.store(norm_data)
    
    # Compute eigenvalues
    eigenvalues = linalg.eigvalsh(rho)
    
    # Convert to DimensionalArray for proper framework handling
    eig_array = DimensionalArray(eigenvalues, error_registry)
    
    # Check for pure state (single eigenvalue = 1)
    # This is a physics optimization based on mathematical properties
    # Pure states have only one eigenvalue=1 (all others=0)
    
    # Use dimensional analysis rather than arbitrary thresholds
    # Sort eigenvalues in descending order
    sorted_eigs = np.sort(eigenvalues.array)[::-1]
    
    # For pure states, first eigenvalue ≈ 1, all others ≈ 0
    # Check using the ratio between largest and second-largest eigenvalue
    if len(sorted_eigs) > 1:
        # Compute the ratio of the second eigenvalue to the first
        # Pure states have eigenvalue structure [1, 0, 0, ...] in theory
        purity_ratio = sorted_eigs[1] / sorted_eigs[0] if sorted_eigs[0] != 0 else 0
        
        # Track eigenvalue structure via error registry
        if error_registry is not None:
            purity_data = ErrorData(
                original_shape=(1,),
                error_tensor=np.array([purity_ratio]),
                reduction_type='purity_check',
                manifold_data={'max_eigenvalue': sorted_eigs[0], 
                              'second_eigenvalue': sorted_eigs[1]}
            )
            error_registry.store(purity_data)
        
        # Pure state has exactly one non-zero eigenvalue
        # Use exact check rather than arbitrary threshold
        if sorted_eigs[1] == 0.0:
            return 0.0
    
    # Calculate entropy: S = -∑ λ log λ
    # using framework's logarithmic operations for proper handling of singularities
    entropy = 0.0
    for eig in eigenvalues:
        if eig <= 0:  # Handle negative eigenvalues (numerical artifacts)
            continue
            
        # Use framework's dimensional array and log function
        eig_dim = DimensionalArray(eig, error_registry)
        log_eig = log(eig_dim)
        term = -eig * log_eig.array
        entropy += float(term)
    
    # Store error information if error_registry available
    if error_registry is not None:
        error_data = ErrorData(
            original_shape=rho.shape,
            error_tensor=rho.array,
            reduction_type='entropy',
            manifold_data={'eigenvalues': eigenvalues}
        )
        error_id = error_registry.store(error_data)
    
    return entropy


def renyi_entropy(rho: DimensionalArray, alpha: float = 2.0, error_registry=None) -> float:
    """
    Calculate Rényi entropy of order alpha.
    
    S_α = (1/(1-α)) log Tr(ρ^α)
    
    This implementation properly handles zero eigenvalues through the DivideByZero
    framework's dimensional reduction approach, maintaining mathematical correctness.
    
    Parameters
    ----------
    rho : DimensionalArray
        Density matrix
    alpha : float
        Rényi parameter (α ≠ 1)
    error_registry : ErrorRegistry, optional
        Registry for tracking dimensional operations
        
    Returns
    -------
    float
        Rényi entropy of order alpha
    """
    from .. import linalg, sum
    
    # Ensure proper error registry
    if error_registry is None and hasattr(rho, 'error_registry'):
        error_registry = rho.error_registry
    
    # Convert to proper array type if needed
    if not isinstance(rho, DimensionalArray):
        from .. import array
        rho = array(rho)
    
    # For α very close to 1, use von Neumann entropy (limiting case)
    # Instead of using arbitrary threshold, track the situation through error registry
    # This properly handles the mathematical relationship between Renyi and von Neumann entropy
    # as the Renyi parameter approaches 1
    from ..registry import ErrorData
    
    # Calculate how close alpha is to 1 and track it
    alpha_diff = alpha - 1.0
    
    # Store information about proximity to limiting case
    if error_registry is not None:
        limit_data = ErrorData(
            original_shape=(1,),
            error_tensor=np.array([alpha_diff]),
            reduction_type='renyi_von_neumann_limit',
            manifold_data={'alpha': alpha}
        )
        error_registry.store(limit_data)
    
    # Only use the limiting case for exact matches
    if alpha == 1.0:
        return von_neumann_entropy(rho, error_registry)
    
    # Ensure normalization using proper framework approach
    trace = np.trace(rho.array)
    
    # Track normalization information
    norm_data = ErrorData(
        original_shape=(1,),
        error_tensor=np.array([float(trace)]),
        reduction_type='density_matrix_normalization',
        manifold_data={'target_trace': 1.0}
    )
    
    # Normalize without arbitrary threshold
    if trace != 1.0:
        # Use framework division to maintain dimensional consistency
        rho = rho / trace
        
        if error_registry is not None:
            error_registry.store(norm_data)
    
    # Compute eigenvalues
    eigenvalues = linalg.eigvalsh(rho)
    
    # Handle negative eigenvalues using proper error handling
    # Rather than simply filtering, use the framework's error tracking mechanism
    if np.any(eigenvalues.array < 0):
        # Create error data for tracking this numerical situation
        error_data = ErrorData(
            original_shape=rho.shape,
            error_tensor=eigenvalues.array,
            reduction_type='negative_eigenvalues',
            manifold_data={'negative_count': np.sum(eigenvalues.array < 0)}
        )
        neg_error_id = error_registry.store(error_data)
        
        # Only use strictly positive eigenvalues for calculations
        positive_mask = eigenvalues.array > 0
        eigenvalues_filtered = eigenvalues.array[positive_mask]
        
        # If no positive eigenvalues, this is an invalid density matrix
        if len(eigenvalues_filtered) == 0:
            # Create error data to track this exceptional case
            error_data = ErrorData(
                original_shape=rho.shape,
                error_tensor=eigenvalues.array,
                reduction_type='invalid_density_matrix',
                manifold_data={'max_eigenvalue': np.max(eigenvalues.array)}
            )
            invalid_error_id = error_registry.store(error_data)
            return 0.0
        
        # Create a new DimensionalArray with error tracking
        eigenvalues = DimensionalArray(eigenvalues_filtered, error_registry)
        eigenvalues._error_id = neg_error_id
    else:
        # No negative eigenvalues - ensure we're still working with positive values only
        positive_mask = eigenvalues.array > 0
        if not np.all(positive_mask):
            # We have zero eigenvalues - handle with framework's approach
            eigenvalues = DimensionalArray(eigenvalues.array[positive_mask], error_registry)
        
    # Convert eigenvalues to DimensionalArray for proper framework handling
    eig_array = DimensionalArray(eigenvalues, error_registry)
    
    # Use framework's power function for proper handling of singularities
    powered_eigenvalues = power(eig_array, alpha)
    
    # Sum the powered eigenvalues
    trace_powered = sum(powered_eigenvalues)
    
    # Create DimensionalArray for the trace and use framework's log function
    # Check if trace_powered is DimensionalArray or a scalar
    trace_dim = DimensionalArray(
        trace_powered.array if hasattr(trace_powered, 'array') else trace_powered, 
        error_registry)
    log_trace = log(trace_dim)
    
    # Complete the Rényi entropy formula
    renyi_result = (1.0 / (1.0 - alpha)) * log_trace.array
    
    # Store error information if error_registry available
    if error_registry is not None:
        error_data = ErrorData(
            original_shape=rho.shape,
            error_tensor=rho.array,
            reduction_type='renyi_entropy',
            manifold_data={'alpha': alpha, 'eigenvalues': eigenvalues}
        )
        error_id = error_registry.store(error_data)
    
    return float(renyi_result)


def log_negativity(rho: DimensionalArray, dims: Optional[Tuple[int, int]] = None, error_registry=None) -> float:
    """
    Calculate logarithmic negativity for entanglement quantification.
    
    Uses the formula: EN(ρ) = log₂(||ρᵀᴬ||₁)
    
    Parameters
    ----------
    rho : DimensionalArray
        Density matrix for a bipartite system
    dims : Tuple[int, int], optional
        Dimensions of the two subsystems, inferred from shape if not provided
    error_registry : ErrorRegistry, optional
        Registry for tracking dimensional operations
        
    Returns
    -------
    float
        Logarithmic negativity
    """
    from .. import log2
    
    # Ensure proper error registry
    if error_registry is None and hasattr(rho, 'error_registry'):
        error_registry = rho.error_registry
    
    # Convert to proper array type if needed
    if not isinstance(rho, DimensionalArray):
        from .. import array
        rho = array(rho)
    
    # Ensure proper shape for bipartite density matrix
    if rho.array.ndim == 1:  # State vector
        state = rho.array / np.linalg.norm(rho.array)
        density_matrix = np.outer(state, state.conj())
    else:
        density_matrix = rho.array
    
    # Determine dimensions
    if dims is None:
        # Assume square matrix for density matrix
        total_dim = int(np.sqrt(density_matrix.shape[0]))
        # For equal bipartite split
        dim = int(np.sqrt(total_dim))
        dims = (dim, dim)
    else:
        # Verify dimensions match density matrix size
        if dims[0] * dims[1] != density_matrix.shape[0]:
            raise DimensionalError(f"Dimensions {dims} don't match density matrix shape {density_matrix.shape}")
    
    # Reshape for partial transpose if needed
    if density_matrix.shape != (dims[0] * dims[1], dims[0] * dims[1]):
        density_matrix = density_matrix.reshape(dims[0], dims[1], dims[0], dims[1])
    
    # Compute partial transpose
    if density_matrix.ndim == 2:
        # Reshape to 4D tensor for partial transpose
        reshaped = density_matrix.reshape(dims[0], dims[1], dims[0], dims[1])
        # Transpose the first subsystem (A)
        pt_reshaped = np.transpose(reshaped, (1, 0, 2, 3))
        # Reshape back to matrix
        pt_matrix = pt_reshaped.reshape(dims[0] * dims[1], dims[0] * dims[1])
    else:
        # Already a 4D tensor
        pt_reshaped = np.transpose(density_matrix, (1, 0, 2, 3))
        pt_matrix = pt_reshaped.reshape(dims[0] * dims[1], dims[0] * dims[1])
    
    # Compute eigenvalues of partial transpose
    eigenvalues = np.linalg.eigvals(pt_matrix)
    
    # Calculate the trace norm ||ρᵀᴬ||₁
    trace_norm = np.sum(np.abs(eigenvalues))
    
    # Compute logarithmic negativity
    # Using framework's log2 function for proper handling of singularities
    if trace_norm > 1.0:
        log_negativity_value = log2(DimensionalArray(trace_norm, error_registry)).array
    else:
        # No entanglement detected
        log_negativity_value = 0.0
    
    # Store error information if error_registry available
    if error_registry is not None:
        error_data = ErrorData(
            original_shape=rho.shape,
            error_tensor=rho.array,
            reduction_type='log_negativity',
            manifold_data={'trace_norm': trace_norm, 'dims': dims}
        )
        error_id = error_registry.store(error_data)
    
    return float(log_negativity_value)


def entanglement_entropy(schmidt_values, error_registry=None) -> float:
    """
    Calculate entanglement entropy from Schmidt values.
    
    Parameters
    ----------
    schmidt_values : array_like
        Schmidt values (normalized)
    error_registry : ErrorRegistry, optional
        Registry for tracking dimensional operations
        
    Returns
    -------
    float
        Entanglement entropy
    """
    # Convert to proper array type if needed
    if not isinstance(schmidt_values, DimensionalArray):
        from .. import array
        schmidt_values = array(schmidt_values)
    
    # Ensure proper error registry
    if error_registry is None and hasattr(schmidt_values, 'error_registry'):
        error_registry = schmidt_values.error_registry
    
    # Ensure normalization using proper framework approach
    norm = np.sum(schmidt_values.array)
    
    # Use proper dimensional approach with error tracking
    from ..registry import ErrorData
    
    # Track normalization information
    norm_data = ErrorData(
        original_shape=(1,),
        error_tensor=np.array([float(norm)]),
        reduction_type='schmidt_normalization',
        manifold_data={'target_norm': 1.0}
    )
    
    # Only normalize if needed, using error tracking
    if norm != 1.0:
        schmidt_values = schmidt_values / norm
        
        # Store normalization error data
        if error_registry is not None:
            error_registry.store(norm_data)
    
    # Calculate entropy: S = -∑ λ log₂ λ
    # using framework's logarithmic operations for proper handling of singularities
    
    # Import directly from logarithmic_functions for consistent framework usage
    from ..logarithms import log2 as log2_func
    
    # Create a single DimensionalArray for all Schmidt values
    # Rather than processing one at a time, which can lose dimensional context
    full_sv_array = schmidt_values
    
    # Use the framework's log2 function directly - this properly handles zeros
    # through dimensional reduction instead of filtering them out
    log2_values = log2_func(full_sv_array)
    
    # Compute entropy term: -∑ λ log₂ λ
    # Multiplication preserves the dimensional structure
    entropy_terms = -full_sv_array * log2_values
    
    # Sum all entropy contributions
    # The framework properly handles 0*log(0)=0 through its dimensional approach
    from .. import sum as sum_func
    sum_result = sum_func(entropy_terms)
    # Check if result is a DimensionalArray or a scalar
    entropy = float(sum_result.array if hasattr(sum_result, 'array') else sum_result)
    
    # Store error information if error_registry available
    if error_registry is not None:
        error_data = ErrorData(
            original_shape=schmidt_values.shape,
            error_tensor=schmidt_values.array,
            reduction_type='entanglement_entropy'
        )
        error_id = error_registry.store(error_data)
    
    return entropy


def relative_entropy(rho: DimensionalArray, sigma: DimensionalArray, error_registry=None) -> float:
    """
    Calculate quantum relative entropy S(ρ||σ) = Tr[ρ(log ρ - log σ)].
    
    This implementation properly handles zero eigenvalues through the DivideByZero
    framework's dimensional reduction approach.
    
    Parameters
    ----------
    rho : DimensionalArray
        First density matrix
    sigma : DimensionalArray
        Second density matrix
    error_registry : ErrorRegistry, optional
        Registry for tracking dimensional operations
        
    Returns
    -------
    float
        Relative entropy
    """
    from .. import linalg, sum, trace
    
    # Ensure proper error registry
    if error_registry is None:
        if hasattr(rho, 'error_registry'):
            error_registry = rho.error_registry
        elif hasattr(sigma, 'error_registry'):
            error_registry = sigma.error_registry
    
    # Convert to proper array type if needed
    if not isinstance(rho, DimensionalArray):
        from .. import array
        rho = array(rho)
    
    if not isinstance(sigma, DimensionalArray):
        from .. import array
        sigma = array(sigma)
    
    # Ensure matrices have the same shape
    if rho.shape != sigma.shape:
        raise DimensionalError(f"Density matrices must have the same shape: {rho.shape} vs {sigma.shape}")
    
    # Compute eigendecompositions
    rho_eigvals, rho_eigvecs = linalg.eigh(rho)
    sigma_eigvals, sigma_eigvecs = linalg.eigh(sigma)
    
    # Calculate log(rho) and log(sigma) using eigendecomposition
    log_rho = np.zeros_like(rho.array)
    log_sigma = np.zeros_like(sigma.array)
    
    # Compute log(rho) using eigendecomposition
    for i, eigval in enumerate(rho_eigvals.array):
        if eigval > 0:  # Only consider positive eigenvalues
            eigvec = rho_eigvecs.array[:, i:i+1]
            log_rho += np.log(eigval) * eigvec @ eigvec.T.conj()
    
    # Compute log(sigma) using eigendecomposition
    for i, eigval in enumerate(sigma_eigvals.array):
        if eigval > 0:  # Only consider positive eigenvalues
            eigvec = sigma_eigvecs.array[:, i:i+1]
            log_sigma += np.log(eigval) * eigvec @ eigvec.T.conj()
    
    # Calculate Tr[ρ(log ρ - log σ)]
    diff = log_rho - log_sigma
    product = rho.array @ diff
    rel_entropy = np.trace(product).real
    
    # Handle special case: support of rho not contained in support of sigma
    # This results in infinite relative entropy
    if np.any(sigma_eigvals.array <= 0) and np.any(rho_eigvals.array > 0):
        # Check if there's any overlap in the zero eigenspaces
        for i, sigma_val in enumerate(sigma_eigvals.array):
            if sigma_val <= 0:
                # Get the corresponding eigenvector
                sigma_vec = sigma_eigvecs.array[:, i]
                # Check if this vector has non-zero overlap with rho
                overlap = np.abs(rho.array @ sigma_vec)
                if np.any(overlap > 1e-10):  # Non-zero overlap detected
                    # Store error information
                    if error_registry is not None:
                        error_data = ErrorData(
                            original_shape=rho.shape,
                            error_tensor=np.array([float(overlap.max())]),
                            reduction_type='infinite_relative_entropy',
                            manifold_data={'max_overlap': float(overlap.max())}
                        )
                        error_id = error_registry.store(error_data)
                    return float('inf')
    
    # Store error information if error_registry available
    if error_registry is not None:
        error_data = ErrorData(
            original_shape=rho.shape,
            error_tensor=np.array([float(rel_entropy)]),
            reduction_type='relative_entropy'
        )
        error_id = error_registry.store(error_data)
    
    return float(rel_entropy)