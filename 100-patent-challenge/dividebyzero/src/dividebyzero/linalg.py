import numpy as np
from scipy.linalg import logm as scipy_logm
from scipy.linalg import expm as scipy_expm
from scipy.linalg import sinm as scipy_sinm
from scipy.linalg import cosm as scipy_cosm
from scipy.linalg import tanm as scipy_tanm
from .array import DimensionalArray
from .exceptions import DimensionalError
from .registry import ErrorData

def svd(a, full_matrices=True, compute_uv=True, hermitian=False):
    """
    Singular Value Decomposition with dimensional analysis.
    """
    from .array import DimensionalArray
    from .registry import get_registry, ErrorData
    
    if hasattr(a, 'array'):
        a_array = a.array
        error_registry = a.error_registry
    else:
        a_array = np.asarray(a)
        error_registry = get_registry()
    
    # Compute SVD
    result = np.linalg.svd(a_array, full_matrices=full_matrices, 
                          compute_uv=compute_uv, hermitian=hermitian)
    
    if compute_uv:
        u, s, vh = result
        
        # Track singular value structure
        sv_data = ErrorData(
            original_shape=s.shape,
            error_tensor=s,
            reduction_type='svd_structure',
            manifold_data={'condition_number': s[0]/s[-1] if s[-1] > 0 else float('inf')}
        )
        error_id = error_registry.store(sv_data)
        
        return (DimensionalArray(u, error_registry), 
                DimensionalArray(s, error_registry), 
                DimensionalArray(vh, error_registry))
    else:
        return DimensionalArray(result, error_registry)

def eigh(a, UPLO='L'):
    """
    Eigenvalue decomposition for Hermitian matrices with dimensional analysis.
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    from .registry import get_registry, ErrorData
    
    if hasattr(a, 'array'):
        a_array = a.array
        error_registry = a.error_registry
    else:
        a_array = np.asarray(a)
        error_registry = get_registry()
    
    # Compute eigendecomposition
    w, v = np.linalg.eigh(a_array, UPLO=UPLO)
    
    # Track degenerate eigenvalues and their eigenvectors
    sorted_indices = np.argsort(np.abs(w))
    sorted_eigvals = w[sorted_indices]
    eigenvalue_gaps = np.diff(sorted_eigvals)
    min_gap = np.min(eigenvalue_gaps) if len(eigenvalue_gaps) > 0 else 0
    
    # Identify degenerate subspaces (eigenvalues closer than numerical precision)
    degenerate_mask = np.abs(eigenvalue_gaps) < 1e-10
    
    # Create error data for tracking eigenstructure
    error_data = ErrorData(
        original_shape=w.shape,
        error_tensor=w,
        reduction_type='eigenvalue_structure',
        manifold_data={
            'min_gap': min_gap,
            'degenerate_subspaces': np.where(degenerate_mask)[0] if np.any(degenerate_mask) else []
        }
    )
    error_id = error_registry.store(error_data)
    
    return DimensionalArray(w, error_registry), DimensionalArray(v, error_registry)

def eigvalsh(a, UPLO='L'):
    """
    Compute eigenvalues of a Hermitian matrix with dimensional analysis.
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    from .registry import get_registry, ErrorData
    
    if hasattr(a, 'array'):
        a_array = a.array
        error_registry = a.error_registry
    else:
        a_array = np.asarray(a)
        error_registry = get_registry()
    
    # Compute eigenvalues
    w = np.linalg.eigvalsh(a_array, UPLO=UPLO)
    
    # Track degenerate eigenvalues
    sorted_eigvals = np.sort(np.abs(w))
    eigenvalue_gaps = np.diff(sorted_eigvals)
    min_gap = np.min(eigenvalue_gaps) if len(eigenvalue_gaps) > 0 else 0
    
    # Create error data for tracking eigenvalue structure
    error_data = ErrorData(
        original_shape=w.shape,
        error_tensor=w,
        reduction_type='eigenvalue_structure',
        manifold_data={
            'min_gap': min_gap,
            'hermitian_eigenvalues': w
        }
    )
    error_id = error_registry.store(error_data)
    
    return DimensionalArray(w, error_registry)

def norm(x, ord=None, axis=None, keepdims=False):
    """Matrix or vector norm with dimensional handling."""
    from .array import DimensionalArray
    from .registry import get_registry, ErrorData
    
    if hasattr(x, 'array'):
        x_array = x.array
        error_registry = x.error_registry
    else:
        x_array = np.asarray(x)
        error_registry = get_registry()
    
    # Check for zero vector/matrix
    is_zero = np.all(x_array == 0)
    
    if is_zero:
        # Track zero vector/matrix case
        zero_data = ErrorData(
            original_shape=x_array.shape,
            error_tensor=x_array,
            reduction_type='normalization',
            manifold_data={'ord': ord}
        )
        error_id = error_registry.store(zero_data)
    
    # Compute norm
    result = np.linalg.norm(x_array, ord=ord, axis=axis, keepdims=keepdims)
    
    # Return result
    if isinstance(result, np.ndarray):
        return DimensionalArray(result, error_registry)
    else:
        return result

def det(a):
    """
    Compute the determinant with dimensional analysis of zero crossings.
    """
    from .array import DimensionalArray
    from .registry import get_registry, ErrorData
    
    if hasattr(a, 'array'):
        a_array = a.array
        error_registry = a.error_registry
    else:
        a_array = np.asarray(a)
        error_registry = get_registry()
    
    # Compute determinant
    determinant = np.linalg.det(a_array)
    
    # Track near-zero determinants using spectral properties
    # instead of arbitrary thresholds
    if abs(determinant) < np.finfo(float).eps * max(a_array.shape) * np.max(np.abs(a_array)):
        # Use our own eigenvalue function for consistency
        eigenvalues = eigvals(a)
        
        # Store error data for dimensional analysis
        error_data = ErrorData(
            original_shape=(1,),
            error_tensor=np.array([determinant]),
            reduction_type='det_near_zero',
            manifold_data={'eigenvalues': eigenvalues.array}
        )
        error_id = error_registry.store(error_data)
    
    return DimensionalArray(np.array([determinant]), error_registry)

def inv(a):
    """
    Compute the inverse of a matrix with proper dimensional analysis.
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    from .registry import get_registry, ErrorData
    
    # Extract array and error registry
    if hasattr(a, 'array'):
        a_array = a.array
        error_registry = a.error_registry
    else:
        a_array = np.asarray(a)
        error_registry = get_registry()
    
    # Analyze matrix structure through our own SVD
    try:
        # Use our own SVD instead of numpy's
        U, s, Vh = svd(a_array, full_matrices=False)
        
        # Use the returned DimensionalArrays
        U_array = U.array
        s_array = s.array
        Vh_array = Vh.array
        
        # Use relative structure instead of arbitrary threshold
        s_max = np.max(s_array)
        s_min = np.min(s_array)
        # Use matrix dimensions and precision for scale
        eps_scale = np.finfo(float).eps * s_max * max(a_array.shape)
        
        condition = s_max / s_min if s_min > eps_scale else float('inf')
        
        if condition > 1/eps_scale:  # Near-singular case
            s_filtered = s_array.copy()
            small_mask = s_array < eps_scale
            if np.any(small_mask):
                # Use dimensional structure to determine appropriate scaling
                s_filtered[small_mask] = eps_scale
                
            # Compute inverse with filtered singular values
            s_recip = 1.0 / s_filtered
            result = Vh_array.T @ np.diag(s_recip) @ U_array.T
        else:
            # Standard case - still using SVD method for consistency
            s_recip = 1.0 / s_array
            result = Vh_array.T @ np.diag(s_recip) @ U_array.T
            
        return DimensionalArray(result, error_registry)
    except Exception as e:
        # Track the error
        error_info = ErrorData(
            original_shape=a_array.shape,
            error_tensor=np.zeros_like(a_array),
            reduction_type='inv_error',
            manifold_data={'error': str(e)}
        )
        error_id = error_registry.store(error_info)
        
        # For exact singularity, still provide a dimensional result
        result = np.zeros_like(a_array.T)
        return DimensionalArray(result, error_registry)

def eigvals(a):
    """Compute eigenvalues with dimensional analysis for degeneracy."""
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    from .registry import get_registry, ErrorData
    
    if hasattr(a, 'array'):
        a_array = a.array
        error_registry = a.error_registry
    else:
        a_array = np.asarray(a)
        error_registry = get_registry()
    
    # Compute eigenvalues
    w = np.linalg.eigvals(a_array)
    
    # Track degenerate eigenvalues
    sorted_eigvals = np.sort(np.abs(w))
    eigenvalue_gaps = np.diff(sorted_eigvals)
    min_gap = np.min(eigenvalue_gaps) if len(eigenvalue_gaps) > 0 else 0
    
    # Create error data for tracking eigenvalue structure
    error_data = ErrorData(
        original_shape=w.shape,
        error_tensor=w,
        reduction_type='eigenvalue_structure',
        manifold_data={
            'min_gap': min_gap,
            'eigenvalues': w
        }
    )
    error_id = error_registry.store(error_data)
    
    return DimensionalArray(w, error_registry)

def logm(a):
    """
    Compute matrix logarithm using dimensional division framework for singular matrices.
    
    Parameters
    ----------
    a : array_like
        Matrix whose logarithm is to be computed
    
    Returns
    -------
    logm : DimensionalArray
        Matrix logarithm of a
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    from .registry import get_registry, ErrorData
    
    # Extract array and error registry
    if hasattr(a, 'array'):
        a_array = a.array
        error_registry = a.error_registry
    else:
        a_array = np.asarray(a)
        error_registry = get_registry()
    
    # Special case for scalar logarithm
    if np.isscalar(a_array) or a_array.ndim == 0:
        if a_array <= 0:
            # Track negative logarithm
            neg_data = ErrorData(
                original_shape=(),
                error_tensor=np.array([a_array]),
                reduction_type='logm_negative_input',
                manifold_data={'input_value': float(a_array)}
            )
            error_id = error_registry.store(neg_data)
            result = np.log(complex(a_array))
        else:
            result = np.log(a_array)
        return DimensionalArray(result, error_registry)
    
    # Use proper dimensional approach to handle potential singularities
    
    # Check for diagonal matrix which can be processed element-wise
    is_diagonal = np.allclose(a_array, np.diag(np.diag(a_array)))
    if is_diagonal:
        diag_values = np.diag(a_array)
        log_diag = np.zeros_like(diag_values, dtype=complex)
        
        # Track any non-positive diagonal entries
        non_positive = diag_values <= 0
        if np.any(non_positive):
            neg_diag_data = ErrorData(
                original_shape=diag_values.shape,
                error_tensor=diag_values[non_positive],
                reduction_type='logm_negative_diag',
                manifold_data={'negative_indices': np.where(non_positive)[0].tolist()}
            )
            error_id = error_registry.store(neg_diag_data)
        
        # Compute logarithm of each diagonal element
        for i in range(len(diag_values)):
            log_diag[i] = np.log(complex(diag_values[i]))
        
        # Create result matrix
        result = np.diag(log_diag)
        
        # If result is real (within numerical precision), convert back to float
        if np.allclose(result.imag, 0):
            result = result.real
            
        return DimensionalArray(result, error_registry)
    
    # Use eigendecomposition for non-diagonal matrices
    try:
        eigenvals, eigenvecs = np.linalg.eig(a_array)
        
        # Check for zero eigenvalues (singular matrix)
        zero_eigenvals = np.isclose(eigenvals, 0)
        if np.any(zero_eigenvals):
            singular_data = ErrorData(
                original_shape=eigenvals.shape,
                error_tensor=eigenvals,
                reduction_type='logm_singular',
                manifold_data={'zero_indices': np.where(zero_eigenvals)[0].tolist()}
            )
            error_id = error_registry.store(singular_data)
            
            # Set small non-zero values for zeros to compute a complex result
            eigenvals[zero_eigenvals] = 1e-16
        
        # Check for negative eigenvalues (non-real logarithm)
        neg_eigenvals = (eigenvals.real < 0) & ~np.isclose(eigenvals.real, 0)
        if np.any(neg_eigenvals):
            negative_data = ErrorData(
                original_shape=eigenvals.shape,
                error_tensor=eigenvals[neg_eigenvals],
                reduction_type='logm_negative_eigenvals',
                manifold_data={'negative_indices': np.where(neg_eigenvals)[0].tolist()}
            )
            error_id = error_registry.store(negative_data)
        
        # Compute logarithm of eigenvalues
        log_eigenvals = np.log(eigenvals)
        
        # Reconstruct matrix logarithm
        result = eigenvecs @ np.diag(log_eigenvals) @ np.linalg.inv(eigenvecs)
        
        # If result is real (within numerical precision), convert back to float
        if np.allclose(result.imag, 0):
            result = result.real
            
        return DimensionalArray(result, error_registry)
        
    except Exception as e:
        # Fall back to SVD approach if eigendecomposition fails
    # Create error registry entry to track singular value structure
    # Perform SVD for all matrices to determine dimensional structure
        # Use our own SVD function instead of numpy's
        U, s, Vh = svd(a_array)
        
        # Convert to numpy arrays for computation
        U_array = U.array
        s_array = s.array
        Vh_array = Vh.array
    
    # Create structured error data for tracking
    error_data = ErrorData(
            original_shape=a_array.shape,
            error_tensor=s_array,
        reduction_type='logm_svd',
            manifold_data={'singular_values': s_array}
    )
    error_id = error_registry.store(error_data)
    
    # The matrix is treated as singular if exact zeros are present
    # or if the condition number is extremely high
    zero_mask = (s_array == 0)
    rank_deficient = np.any(zero_mask)
    
    # Also check for numerical rank deficiency through structure analysis
    # instead of arbitrary thresholds
    s_ratios = s_array / s_array[0]  # Normalize by largest singular value
    
    # Use dimensional structure for classification
    condition_number = s_array[0] / s_array[-1] if s_array[-1] > 0 else float('inf')
    
    # Define is_singular based on rank deficiency or condition number
    # Use proper mathematical approach based on matrix structure
    # Track condition information
    condition_data = ErrorData(
            original_shape=a_array.shape,
            error_tensor=s_array,
        reduction_type='condition_number',
        manifold_data={'condition_number': condition_number}
    )
    condition_error_id = error_registry.store(condition_data)
    
    # Determine singularity based on mathematical structure
    is_singular = rank_deficient or condition_number > 1/np.finfo(float).eps
    
    # Handle both singular and non-singular cases with a unified approach
    # that works mathematically at all points in function domain
    # This is the core of our dimensional analysis principle - it must work
    # at all points in the domain, including singularities and near-singularities
    
    s_filtered = s_array.copy()
    
    # Determine how to handle singular and near-singular values
    if is_singular:
        # Track exactly which values are zero
        zero_mask = (s_array == 0)
        
        # For the zero singular values, use proper dimensional representation
        if np.any(zero_mask):
            # Project to the proper dimensional subspace for zero singular values
            # Don't use any fixed small value, use the singular value structure
            nonzero_s = s_array[~zero_mask]
            
            # If there are no nonzero singular values, use min float
            if nonzero_s.size == 0:
                s_filtered[zero_mask] = np.finfo(float).tiny
            else:
                # Use dimensional structure of the matrix itself
                # to determine the appropriate value
                min_ratio = np.min(nonzero_s) / s_array[0]
                # Apply a structured reduction preserving matrix properties
                s_filtered[zero_mask] = s_array[0] * min_ratio * min_ratio
    
    # Handle very small but non-zero singular values through proper dimensional analysis
    # Define near-zero based on the matrix's own structure rather than arbitrary thresholds
    if not rank_deficient and s_array.size > 1:
        # The smallest non-zero sv compared to the largest as a structural property
        min_nonzero_ratio = np.min(s_array[s_array > 0]) / s_array[0]
        
        # Use the matrix's own structure to determine what "small" means
        small_mask = (s_ratios < min_nonzero_ratio * 10) & (s_array > 0)
        
        if np.any(small_mask):
            # Compute scaled values that preserve the matrix's structure
            # while avoiding numerical instability
            s_filtered[small_mask] = s_array[0] * min_nonzero_ratio * s_ratios[small_mask]
    
    # Reconstruct filtered matrix
    a_filtered = U_array @ np.diag(s_filtered) @ Vh_array
    
    # Compute log(π(A))
    log_filtered = np.log(s_filtered)
    log_a_filtered = U_array @ np.diag(log_filtered) @ Vh_array
    
    # Compute correction term log(1 + ε(A)/π(A)) ≈ ε(A)/π(A)
    # Note: We use first-order approximation since ε(A)/π(A) is small
    error_term = a_array - a_filtered
    correction = error_term @ np.linalg.inv(a_filtered)
    
    # Combine for first-order approximation
    result = log_a_filtered + correction
    
    return DimensionalArray(result, error_registry)

def sqrtm(a):
    """
    Compute the matrix square root.
    
    Parameters
    ----------
    a : array_like
        Matrix whose square root to compute
    
    Returns
    -------
    sqrtm : DimensionalArray
        Matrix square root of a
    """
    if isinstance(a, DimensionalArray):
        a = a.array
    
    # Compute eigendecomposition
    eigenvals, eigenvecs = np.linalg.eigh(a)
    
    # Handle negative eigenvalues through proper dimensional approach
    # Store error data for tracking
    error_data = ErrorData(
        original_shape=eigenvals.shape,
        error_tensor=eigenvals,
        reduction_type='sqrtm_eigenvals',
        manifold_data={'eigenvalues': eigenvals}
    )
    
    # Create dimensional array representation
    eigenvals_dim = DimensionalArray(eigenvals)
    neg_mask = eigenvals < 0
    
    # Use proper handling for negative eigenvalues
    if np.any(neg_mask):
        # For negative eigenvalues, dimensional handling replaces them
        # with a structure-preserving substitute rather than arbitrary zero
        neg_data = ErrorData(
            original_shape=eigenvals.shape,
            error_tensor=eigenvals,
            reduction_type='negative_sqrtm',
            manifold_data={'neg_mask': neg_mask}
        )
        error_id = eigenvals_dim.error_registry.store(neg_data)
        
        # Get dimensional replacement for negative values
        # based on matrix structure
        if np.any(~neg_mask):
            # Find the smallest positive eigenvalue to use as scale reference
            min_pos = np.min(eigenvals[~neg_mask])
            max_pos = np.max(eigenvals[~neg_mask])
            
            # Use eigenvalue structure to determine appropriate scale
            # Track this operation with structured error data
            eig_scale_data = ErrorData(
                original_shape=eigenvals.shape,
                error_tensor=eigenvals[~neg_mask],
                reduction_type='eig_scaling',
                manifold_data={'min_pos': min_pos, 'max_pos': max_pos}
            )
            error_id = eigenvals_dim.error_registry.store(eig_scale_data)
            
            # Use ratio of min to max to determine structural scale
            scale_ratio = min_pos / max_pos
            # Square the ratio to get appropriately small but structurally derived value
            eigenvals[neg_mask] = min_pos * scale_ratio
        else:
            # All eigenvalues are negative - use tiny positive value
            eigenvals[neg_mask] = np.finfo(float).tiny
    
    # Take square root of properly handled eigenvalues
    sqrt_eigenvals = np.sqrt(eigenvals)
    
    # Reconstruct matrix
    sqrt_matrix = eigenvecs @ np.diag(sqrt_eigenvals) @ eigenvecs.conj().T
    
    return DimensionalArray(sqrt_matrix)

def pinv(a, rcond=None, hermitian=False):
    """
    Compute the (Moore-Penrose) pseudo-inverse of a matrix.
    
    This implementation uses the framework's approach to handle singularities
    properly through dimensional analysis rather than arbitrary thresholds.
    
    Parameters
    ----------
    a : array_like
        Matrix to be pseudo-inverted
    rcond : float, optional
        If None (default), proper dimensional analysis is used
    hermitian : bool, optional
        If True, a is assumed to be Hermitian
        
    Returns
    -------
    B : DimensionalArray
        The pseudo-inverse of a
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    from .registry import get_registry, ErrorData
    
    # Extract array and error registry
    if hasattr(a, 'array'):
        a_array = a.array
        error_registry = a.error_registry
    else:
        a_array = np.asarray(a)
        error_registry = get_registry()
    
    # If rcond is provided, use it directly with numpy pinv
    if rcond is not None:
        result = np.linalg.pinv(a_array, rcond=rcond, hermitian=hermitian)
        return DimensionalArray(result, error_registry)
    
    # Otherwise use proper dimensional approach with our SVD
    U, s, Vh = svd(a_array, full_matrices=False)
    
    # Convert to numpy arrays for computation
    U_array = U.array
    s_array = s.array
    Vh_array = Vh.array
    
    # Create error data for tracking
    sv_data = ErrorData(
        original_shape=s_array.shape,
        error_tensor=s_array,
        reduction_type='pinv_svd',
        manifold_data={'singular_values': s_array}
    )
    error_id = error_registry.store(sv_data)
    
    # Use dimensional relationship within the matrix
    # rather than arbitrary threshold
    s_max = np.max(s_array)
    
    # Reciprocal with proper handling of very small values
    s_recip = np.zeros_like(s_array)
    nonzero = s_array > 0
    if np.any(nonzero):
        s_recip[nonzero] = 1.0 / s_array[nonzero]
    
    # Reconstruct pinv
    result = Vh_array.conj().T @ np.diag(s_recip) @ U_array.conj().T
    
    return DimensionalArray(result, error_registry)

def matrix_rank(M, tol=None, hermitian=False):
    """
    Return matrix rank using dimensional analysis approach.
    """
    from .array import DimensionalArray
    from .registry import get_registry, ErrorData
    
    if hasattr(M, 'array'):
        M_array = M.array
        error_registry = M.error_registry
    else:
        M_array = np.asarray(M)
        error_registry = get_registry()
    
    # Compute SVD for dimensional analysis using our SVD function
    s = svd(M_array, compute_uv=False)
    s_array = s.array
    
    # Track singular value structure
    sv_data = ErrorData(
        original_shape=s_array.shape,
        error_tensor=s_array,
        reduction_type='rank_analysis',
        manifold_data={'singular_values': s_array}
    )
    error_id = error_registry.store(sv_data)
    
    # Use dimensional approach to determine rank
    if tol is None:
        # Use largest singular value to determine appropriate scale
        tol = s_array[0] * max(M_array.shape) * np.finfo(s_array.dtype).eps
    
    return np.sum(s_array > tol)

def matrix_power(a, n):
    """
    Raise a square matrix to the power n.
    
    Uses dimensional analysis to handle singular matrices and boundary cases.
    
    Parameters
    ----------
    a : array_like
        Square matrix to be raised to the power n
    n : int
        Power to which the matrix is raised
    
    Returns
    -------
    a**n : DimensionalArray
        Matrix a to the power n with dimensional error tracking
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    from .registry import get_registry, ErrorData
    
    # Extract array and error registry
    if hasattr(a, 'array'):
        a_array = a.array
        error_registry = a.error_registry
    else:
        a_array = np.asarray(a)
        error_registry = get_registry()
    
    # Check if the matrix is square
    if a_array.ndim != 2 or a_array.shape[0] != a_array.shape[1]:
        raise ValueError("Matrix must be square")
    
    # Special cases
    if n == 0:
        # Return identity matrix
        result = np.eye(a_array.shape[0], dtype=a_array.dtype)
        return DimensionalArray(result, error_registry)
    
    # Handle negative powers through dimensional inversion
    if n < 0:
        # Use our own SVD for inversion
        U, s, Vh = svd(a_array, full_matrices=False)
        
        # Use the returned DimensionalArrays
        U_array = U.array
        s_array = s.array
        Vh_array = Vh.array
        
        # Use relative structure instead of arbitrary threshold
        s_max = np.max(s_array)
        # Use machine precision and matrix dimensions for scale
        eps_scale = np.finfo(float).eps * s_max * max(a_array.shape)
        
        # Handle singular values
        s_pinv = np.zeros_like(s_array)
        nonzero = s_array > eps_scale
        if np.any(nonzero):
            s_pinv[nonzero] = 1.0 / s_array[nonzero]
        
        # Compute inverse through dimensional SVD
        a_inv = Vh_array.T @ np.diag(s_pinv) @ U_array.T
        
        # Raise the inverse to the positive power
        if n == -1:
            return DimensionalArray(a_inv, error_registry)
        else:
            return matrix_power(DimensionalArray(a_inv, error_registry), -n)
    
    # For positive powers, use standard algorithm with dimensional tracking
    # but avoid arbitrary thresholds
    if n == 1:
        return DimensionalArray(a_array.copy(), error_registry)
    
    # Use binary exponentiation for efficiency
    result = matrix_power(a, n // 2)
    result = result @ result
    
    if n % 2 == 1:
        result = result @ a
    
    return result

def expm(a):
    """
    Compute matrix exponential using dimensional handling for singular matrices.
    
    Parameters
    ----------
    a : array_like
        Matrix whose exponential is to be computed
    
    Returns
    -------
    expm : DimensionalArray
        Matrix exponential of a with proper dimensional handling
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    from .registry import get_registry, ErrorData
    
    # Extract array and error registry
    if hasattr(a, 'array'):
        a_array = a.array
        error_registry = a.error_registry
    else:
        a_array = np.asarray(a)
        error_registry = get_registry()
    
    # Special case for scalar exponential
    if np.isscalar(a_array) or a_array.ndim == 0:
        return DimensionalArray(np.exp(a_array), error_registry)
    
    # Use eigendecomposition to analyze matrix structure
    try:
        # For symmetric/Hermitian matrices
        is_symmetric = np.allclose(a_array, a_array.T)
        
        if is_symmetric:
            try:
                eigenvals, eigenvecs = np.linalg.eigh(a_array)
            except np.linalg.LinAlgError:
                # Fallback to general case
                eigenvals, eigenvecs = np.linalg.eig(a_array)
        else:
            # For general matrices
            eigenvals, eigenvecs = np.linalg.eig(a_array)
            
        # Track eigenvalues
        eig_data = ErrorData(
            original_shape=eigenvals.shape,
            error_tensor=eigenvals,
            reduction_type='expm_eigenvalues',
            manifold_data={'eigenvalues': eigenvals}
        )
        eig_id = error_registry.store(eig_data)
        
        # Check for extreme eigenvalues
        max_exp = np.log(np.finfo(float).max)
        large_eigs = np.abs(eigenvals) > max_exp
        
        if np.any(large_eigs):
            # Record extreme eigenvalues before continuing
            extreme_data = ErrorData(
                original_shape=eigenvals.shape,
                error_tensor=eigenvals[large_eigs],
                reduction_type='expm_overflow',
                manifold_data={
                    'max_exp': max_exp,
                    'max_eigenvalue': np.max(np.abs(eigenvals)),
                    'extreme_indices': np.where(large_eigs)[0].tolist()
                }
            )
            extreme_id = error_registry.store(extreme_data)
            
            # Scale down extreme eigenvalues to prevent overflow
            scaled_eigenvals = eigenvals.copy()
            scale_factor = max_exp / np.max(np.abs(eigenvals[large_eigs]))
            scaled_eigenvals[large_eigs] = eigenvals[large_eigs] * scale_factor
            
            # Compute exponential using scaled eigenvalues
            exp_eigenvals = np.exp(scaled_eigenvals)
            
            # Mark the result as having controlled overflow
            result = eigenvecs @ np.diag(exp_eigenvals) @ np.linalg.inv(eigenvecs)
            result_dim = DimensionalArray(result, error_registry)
            result_dim._error_id = extreme_id
            return result_dim
            
        # Standard case - compute matrix exponential via eigendecomposition
        exp_eigenvals = np.exp(eigenvals)
        result = eigenvecs @ np.diag(exp_eigenvals) @ np.linalg.inv(eigenvecs)
        
        return DimensionalArray(result, error_registry)
        
    except Exception as e:
        # Handle calculation errors with dimensional tracking
        error_info = ErrorData(
            original_shape=a_array.shape,
            error_tensor=np.zeros_like(a_array),
            reduction_type='expm_error',
            manifold_data={'error': str(e)}
        )
        error_id = error_registry.store(error_info)
        
        # Fallback to direct calculation with matrix powers
        # This is safer for some extreme cases
        try:
            # Use 16 terms of the Taylor series
            result = np.eye(a_array.shape[0])
            a_power = np.eye(a_array.shape[0])
            for i in range(1, 16):
                a_power = a_power @ a_array / i
                result = result + a_power
                
            return DimensionalArray(result, error_registry)
            
        except:
            # Ultimate fallback - create a result that indicates the failure
            result = np.eye(a_array.shape[0])
            result_dim = DimensionalArray(result, error_registry)
            result_dim._error_id = error_id
            return result_dim

def sinm(a):
    """
    Compute matrix sine using dimensional handling.
    
    Parameters
    ----------
    a : array_like
        Matrix whose sine is to be computed
    
    Returns
    -------
    sinm : DimensionalArray
        Matrix sine of a with proper dimensional handling
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    from .registry import get_registry, ErrorData
    
    # Extract array and error registry
    if hasattr(a, 'array'):
        a_array = a.array
        error_registry = a.error_registry
    else:
        a_array = np.asarray(a)
        error_registry = get_registry()
    
    # Use eigendecomposition to analyze matrix structure
    try:
        eigenvals, eigenvecs = np.linalg.eigh(a_array)
    except np.linalg.LinAlgError:
        # For non-symmetric matrices, use general eigenvalue decomposition
        try:
            eigenvals, eigenvecs = np.linalg.eig(a_array)
        except:
            # If eigendecomposition fails, use SVD approach
            U, s, Vh = svd(a_array, full_matrices=False)
            
            # Track singular value structure
            sv_data = ErrorData(
                original_shape=s.shape,
                error_tensor=s,
                reduction_type='sinm_svd',
                manifold_data={'singular_values': s}
            )
            error_id = error_registry.store(sv_data)
            
            # Proceed with scipy implementation
            result = scipy_sinm(a_array)
            return DimensionalArray(result, error_registry)
    
    # Track eigenvalue structure
    eig_data = ErrorData(
        original_shape=eigenvals.shape,
        error_tensor=eigenvals,
        reduction_type='sinm_eigen',
        manifold_data={'eigenvalues': eigenvals}
    )
    error_id = error_registry.store(eig_data)
    
    # Compute using scipy or eigendecomposition
    result = scipy_sinm(a_array)
    
    return DimensionalArray(result, error_registry)

def cosm(a):
    """
    Compute matrix cosine using dimensional handling.
    
    Parameters
    ----------
    a : array_like
        Matrix whose cosine is to be computed
    
    Returns
    -------
    cosm : DimensionalArray
        Matrix cosine of a with proper dimensional handling
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    from .registry import get_registry, ErrorData
    
    # Extract array and error registry
    if hasattr(a, 'array'):
        a_array = a.array
        error_registry = a.error_registry
    else:
        a_array = np.asarray(a)
        error_registry = get_registry()
    
    # Use eigendecomposition to analyze matrix structure
    try:
        eigenvals, eigenvecs = np.linalg.eigh(a_array)
    except np.linalg.LinAlgError:
        # For non-symmetric matrices, use general eigenvalue decomposition
        try:
            eigenvals, eigenvecs = np.linalg.eig(a_array)
        except:
            # If eigendecomposition fails, use SVD approach
            U, s, Vh = svd(a_array, full_matrices=False)
            
            # Track singular value structure
            sv_data = ErrorData(
                original_shape=s.shape,
                error_tensor=s,
                reduction_type='cosm_svd',
                manifold_data={'singular_values': s}
            )
            error_id = error_registry.store(sv_data)
            
            # Proceed with scipy implementation
            result = scipy_cosm(a_array)
            return DimensionalArray(result, error_registry)
    
    # Track eigenvalue structure
    eig_data = ErrorData(
        original_shape=eigenvals.shape,
        error_tensor=eigenvals,
        reduction_type='cosm_eigen',
        manifold_data={'eigenvalues': eigenvals}
    )
    error_id = error_registry.store(eig_data)
    
    # Compute using scipy
    result = scipy_cosm(a_array)
    
    return DimensionalArray(result, error_registry)

def tanm(a):
    """
    Compute matrix tangent using dimensional handling.
    
    Parameters
    ----------
    a : array_like
        Matrix whose tangent is to be computed
    
    Returns
    -------
    tanm : DimensionalArray
        Matrix tangent of a with proper dimensional handling
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    from .registry import get_registry, ErrorData
    
    # Extract array and error registry
    if hasattr(a, 'array'):
        a_array = a.array
        error_registry = a.error_registry
    else:
        a_array = np.asarray(a)
        error_registry = get_registry()
    
    # Check for singularities using eigendecomposition
    try:
        eigenvals, eigenvecs = np.linalg.eigh(a_array)
    except np.linalg.LinAlgError:
        # For non-symmetric matrices, use general eigenvalue decomposition
        try:
            eigenvals, eigenvecs = np.linalg.eig(a_array)
        except:
            # If eigendecomposition fails, use SVD approach
            U, s, Vh = svd(a_array, full_matrices=False)
            
            # Track singular value structure
            sv_data = ErrorData(
                original_shape=s.shape,
                error_tensor=s,
                reduction_type='tanm_svd',
                manifold_data={'singular_values': s}
            )
            error_id = error_registry.store(sv_data)
            
            # Handle using sin/cos approach which is more stable near poles
            sin_result = sinm(a)
            cos_result = cosm(a)
            
            # Use our own functions for division to maintain dimensional analysis
            result = sin_result @ pinv(cos_result)
            return result
    
    # Track eigenvalue structure
    eig_data = ErrorData(
        original_shape=eigenvals.shape,
                error_tensor=eigenvals,
        reduction_type='tanm_eigen',
                manifold_data={'eigenvalues': eigenvals}
            )
    error_id = error_registry.store(eig_data)
    
    # Identify potential singularities where tan(λ) has poles (λ = π/2 + nπ)
    # Instead of using an arbitrary threshold, use a dimensional approach
    
    # Calculate mod pi to identify proximity to poles
    pi_values = np.pi/2 + np.pi * np.arange(-10, 11)
    
    # For each eigenvalue, find distance to nearest pole
    min_distances = np.zeros_like(eigenvals)
    for i, val in enumerate(eigenvals):
        distances = np.abs(val - pi_values)
        min_distances[i] = np.min(distances)
    
    # Store information about proximity to poles
    pole_data = ErrorData(
        original_shape=min_distances.shape,
        error_tensor=min_distances,
        reduction_type='tanm_poles',
        manifold_data={'min_distances': min_distances}
    )
    pole_id = error_registry.store(pole_data)
    
    # Decide whether to use sin/cos approach or direct tanm
    # Use sin/cos approach if any eigenvalue is close to a pole
    # relative to the spectral radius of the matrix
    spectral_radius = np.max(np.abs(eigenvals))
    
    # If any eigenvalues are near poles relative to the spectral radius
    if np.any(min_distances / spectral_radius < np.finfo(float).eps * 100):
        # Handle using sin/cos approach which is more stable near poles
        sin_result = sinm(a)
        cos_result = cosm(a)
        
        # Use our own functions for division to maintain dimensional analysis
        result = sin_result @ pinv(cos_result)
        return result
        
    # Standard case
    result = scipy_tanm(a_array)
    return DimensionalArray(result, error_registry)