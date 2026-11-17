"""
FFT module for dividebyzero framework, providing FFT functions that preserve error tracking.

All functions implement the DivideByZero dimensional analysis approach, tracking
dimensional operations through the error registry and handling boundary cases properly.
"""

import numpy as np
from .registry import ErrorData, get_registry

def fft2(x):
    """
    2D FFT with proper dimensional analysis and error tracking.
    
    Parameters
    ----------
    x : array_like
        Input array (2D) for FFT
        
    Returns
    -------
    result : DimensionalArray
        2D FFT of the input with dimensional analysis
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    
    # Extract array and error registry
    if hasattr(x, 'array'):
        x_array = x.array
        error_registry = x.error_registry
        # Store original error_id if present
        original_error_id = getattr(x, '_error_id', None)
    else:
        x_array = np.asarray(x)
        error_registry = get_registry()
        original_error_id = None
    
    # Analyze input for dimensional tracking
    # Track shape and other properties
    shape_data = ErrorData(
        original_shape=x_array.shape,
        error_tensor=np.zeros(x_array.shape[0] if x_array.ndim > 0 else 1),
        reduction_type='fft_input_tracking',
        manifold_data={'input_shape': x_array.shape, 'input_dtype': str(x_array.dtype)}
    )
    shape_id = error_registry.store(shape_data)
    
    # Check for NaN/inf values in input
    has_nan = np.any(np.isnan(x_array))
    has_inf = np.any(np.isinf(x_array))
    
    if has_nan or has_inf:
        nan_inf_data = ErrorData(
            original_shape=x_array.shape,
            error_tensor=np.zeros(1),
            reduction_type='fft_nan_inf',
            manifold_data={'has_nan': has_nan, 'has_inf': has_inf}
        )
        error_id = error_registry.store(nan_inf_data)
    
    # Perform FFT
    fft_result = np.fft.fft2(x_array)
    
    # Check for error propagation
    has_nan_result = np.any(np.isnan(fft_result))
    has_inf_result = np.any(np.isinf(fft_result))
    
    if has_nan_result or has_inf_result:
        result_data = ErrorData(
            original_shape=fft_result.shape,
            error_tensor=np.zeros(1),
            reduction_type='fft_result_nan_inf',
            manifold_data={'has_nan': has_nan_result, 'has_inf': has_inf_result}
        )
        error_id = error_registry.store(result_data)
    
    # Create result object
    result = DimensionalArray(fft_result, error_registry)
    
    # Preserve original error_id if it exists
    if original_error_id is not None:
        result._error_id = original_error_id
    
    return result

def ifft2(x):
    """
    Inverse 2D FFT with proper dimensional analysis and error tracking.
    
    Parameters
    ----------
    x : array_like
        Input array (2D) for inverse FFT
        
    Returns
    -------
    result : DimensionalArray
        Inverse 2D FFT of the input with dimensional analysis
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    
    # Extract array and error registry
    if hasattr(x, 'array'):
        x_array = x.array
        error_registry = x.error_registry
        # Store original error_id if present
        original_error_id = getattr(x, '_error_id', None)
    else:
        x_array = np.asarray(x)
        error_registry = get_registry()
        original_error_id = None
    
    # Analyze input for dimensional tracking
    shape_data = ErrorData(
        original_shape=x_array.shape,
        error_tensor=np.zeros(x_array.shape[0] if x_array.ndim > 0 else 1),
        reduction_type='ifft_input_tracking',
        manifold_data={'input_shape': x_array.shape, 'input_dtype': str(x_array.dtype)}
    )
    shape_id = error_registry.store(shape_data)
    
    # Check for NaN/inf values in input
    has_nan = np.any(np.isnan(x_array))
    has_inf = np.any(np.isinf(x_array))
    
    if has_nan or has_inf:
        nan_inf_data = ErrorData(
            original_shape=x_array.shape,
            error_tensor=np.zeros(1),
            reduction_type='ifft_nan_inf',
            manifold_data={'has_nan': has_nan, 'has_inf': has_inf}
        )
        error_id = error_registry.store(nan_inf_data)
    
    # Perform inverse FFT
    ifft_result = np.fft.ifft2(x_array)
    
    # Check for error propagation
    has_nan_result = np.any(np.isnan(ifft_result))
    has_inf_result = np.any(np.isinf(ifft_result))
    
    if has_nan_result or has_inf_result:
        result_data = ErrorData(
            original_shape=ifft_result.shape,
            error_tensor=np.zeros(1),
            reduction_type='ifft_result_nan_inf',
            manifold_data={'has_nan': has_nan_result, 'has_inf': has_inf_result}
        )
        error_id = error_registry.store(result_data)
    
    # Create result object
    result = DimensionalArray(ifft_result, error_registry)
    
    # Preserve original error_id if it exists
    if original_error_id is not None:
        result._error_id = original_error_id
    
    return result

def fftshift(x):
    """
    Shift zero-frequency component to center of spectrum with dimensional analysis.
    
    Parameters
    ----------
    x : array_like
        Input array
        
    Returns
    -------
    result : DimensionalArray
        Shifted array with dimensional analysis
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    
    # Extract array and error registry
    if hasattr(x, 'array'):
        x_array = x.array
        error_registry = x.error_registry
        # Store original error_id if present
        original_error_id = getattr(x, '_error_id', None)
    else:
        x_array = np.asarray(x)
        error_registry = get_registry()
        original_error_id = None
    
    # Track shift operation
    shift_data = ErrorData(
        original_shape=x_array.shape,
        error_tensor=np.zeros(x_array.shape[0] if x_array.ndim > 0 else 1),
        reduction_type='fftshift',
        manifold_data={'dimensions': x_array.ndim}
    )
    shift_id = error_registry.store(shift_data)
    
    # Perform shift
    shifted = np.fft.fftshift(x_array)
    
    # Create result object
    result = DimensionalArray(shifted, error_registry)
    
    # Preserve original error_id if it exists
    if original_error_id is not None:
        result._error_id = original_error_id
    
    return result

def ifftshift(x):
    """
    Inverse shift zero-frequency component to center of spectrum with dimensional analysis.
    
    Parameters
    ----------
    x : array_like
        Input array
        
    Returns
    -------
    result : DimensionalArray
        Inverse shifted array with dimensional analysis
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    
    # Extract array and error registry
    if hasattr(x, 'array'):
        x_array = x.array
        error_registry = x.error_registry
        # Store original error_id if present
        original_error_id = getattr(x, '_error_id', None)
    else:
        x_array = np.asarray(x)
        error_registry = get_registry()
        original_error_id = None
    
    # Track shift operation
    shift_data = ErrorData(
        original_shape=x_array.shape,
        error_tensor=np.zeros(x_array.shape[0] if x_array.ndim > 0 else 1),
        reduction_type='ifftshift',
        manifold_data={'dimensions': x_array.ndim}
    )
    shift_id = error_registry.store(shift_data)
    
    # Perform inverse shift
    shifted = np.fft.ifftshift(x_array)
    
    # Create result object
    result = DimensionalArray(shifted, error_registry)
    
    # Preserve original error_id if it exists
    if original_error_id is not None:
        result._error_id = original_error_id
    
    return result

def fftfreq(n, d=1.0):
    """
    Return the Discrete Fourier Transform sample frequencies with dimensional analysis.
    
    Parameters
    ----------
    n : int
        Window length
    d : float, optional
        Sample spacing (inverse of the sampling rate)
        
    Returns
    -------
    f : DimensionalArray
        Array of length n containing the sample frequencies
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    
    # Get registry
    error_registry = get_registry()
    original_error_id = None
    
    # If we get a DimensionalArray as input, preserve its error_id
    if hasattr(n, '_error_id'):
        original_error_id = n._error_id
        error_registry = n.error_registry
    elif hasattr(d, '_error_id'):
        original_error_id = d._error_id
        error_registry = d.error_registry
    
    # Track frequency parameters
    freq_data = ErrorData(
        original_shape=(n,),
        error_tensor=np.zeros(1),
        reduction_type='fftfreq_params',
        manifold_data={'n': n, 'd': d}
    )
    freq_id = error_registry.store(freq_data)
    
    # Calculate frequencies
    freqs = np.fft.fftfreq(n, d)
    
    # Create result object
    result = DimensionalArray(freqs, error_registry)
    
    # Preserve original error_id if it exists
    if original_error_id is not None:
        result._error_id = original_error_id
    
    return result

def rfft2(x):
    """
    2D Real FFT with proper dimensional analysis and error tracking.
    
    Parameters
    ----------
    x : array_like
        Input array (2D) for real FFT
        
    Returns
    -------
    result : DimensionalArray
        2D Real FFT of the input with dimensional analysis
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    
    # Extract array and error registry
    if hasattr(x, 'array'):
        x_array = x.array
        error_registry = x.error_registry
        # Store original error_id if present
        original_error_id = getattr(x, '_error_id', None)
    else:
        x_array = np.asarray(x)
        error_registry = get_registry()
        original_error_id = None
    
    # Analyze input for dimensional tracking
    shape_data = ErrorData(
        original_shape=x_array.shape,
        error_tensor=np.zeros(x_array.shape[0] if x_array.ndim > 0 else 1),
        reduction_type='rfft_input_tracking',
        manifold_data={'input_shape': x_array.shape, 'input_dtype': str(x_array.dtype)}
    )
    shape_id = error_registry.store(shape_data)
    
    # Check if input is real-valued
    is_complex = np.iscomplexobj(x_array)
    if is_complex:
        complex_data = ErrorData(
            original_shape=x_array.shape,
            error_tensor=np.zeros(1),
            reduction_type='rfft_complex_input',
            manifold_data={'is_complex': is_complex}
        )
        error_id = error_registry.store(complex_data)
    
    # Perform real FFT
    rfft_result = np.fft.rfft2(x_array)
    
    # Check for error propagation
    has_nan_result = np.any(np.isnan(rfft_result))
    has_inf_result = np.any(np.isinf(rfft_result))
    
    if has_nan_result or has_inf_result:
        result_data = ErrorData(
            original_shape=rfft_result.shape,
            error_tensor=np.zeros(1),
            reduction_type='rfft_result_nan_inf',
            manifold_data={'has_nan': has_nan_result, 'has_inf': has_inf_result}
        )
        error_id = error_registry.store(result_data)
    
    # Create result object
    result = DimensionalArray(rfft_result, error_registry)
    
    # Preserve original error_id if it exists
    if original_error_id is not None:
        result._error_id = original_error_id
    
    return result

def irfft2(x):
    """
    Inverse 2D Real FFT with proper dimensional analysis and error tracking.
    
    Parameters
    ----------
    x : array_like
        Input array for inverse real FFT
        
    Returns
    -------
    result : DimensionalArray
        Inverse 2D Real FFT of the input with dimensional analysis
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    
    # Extract array and error registry
    if hasattr(x, 'array'):
        x_array = x.array
        error_registry = x.error_registry
        # Store original error_id if present
        original_error_id = getattr(x, '_error_id', None)
    else:
        x_array = np.asarray(x)
        error_registry = get_registry()
        original_error_id = None
    
    # Analyze input for dimensional tracking
    shape_data = ErrorData(
        original_shape=x_array.shape,
        error_tensor=np.zeros(x_array.shape[0] if x_array.ndim > 0 else 1),
        reduction_type='irfft_input_tracking',
        manifold_data={'input_shape': x_array.shape, 'input_dtype': str(x_array.dtype)}
    )
    shape_id = error_registry.store(shape_data)
    
    # Perform inverse real FFT
    irfft_result = np.fft.irfft2(x_array)
    
    # Check for error propagation
    has_nan_result = np.any(np.isnan(irfft_result))
    has_inf_result = np.any(np.isinf(irfft_result))
    
    if has_nan_result or has_inf_result:
        result_data = ErrorData(
            original_shape=irfft_result.shape,
            error_tensor=np.zeros(1),
            reduction_type='irfft_result_nan_inf',
            manifold_data={'has_nan': has_nan_result, 'has_inf': has_inf_result}
        )
        error_id = error_registry.store(result_data)
    
    # Create result object
    result = DimensionalArray(irfft_result, error_registry)
    
    # Preserve original error_id if it exists
    if original_error_id is not None:
        result._error_id = original_error_id
    
    return result

def rfftfreq(n, d=1.0):
    """
    Return the Real FFT sample frequencies with dimensional analysis.
    
    Parameters
    ----------
    n : int
        Window length
    d : float, optional
        Sample spacing (inverse of the sampling rate)
        
    Returns
    -------
    f : DimensionalArray
        Array containing the sample frequencies
    """
    # Import inside function to avoid circular imports
    from .array import DimensionalArray
    
    # Get registry
    error_registry = get_registry()
    original_error_id = None
    
    # If we get a DimensionalArray as input, preserve its error_id
    if hasattr(n, '_error_id'):
        original_error_id = n._error_id
        error_registry = n.error_registry
    elif hasattr(d, '_error_id'):
        original_error_id = d._error_id
        error_registry = d.error_registry
    
    # Track frequency parameters
    freq_data = ErrorData(
        original_shape=(n//2 + 1,),
        error_tensor=np.zeros(1),
        reduction_type='rfftfreq_params',
        manifold_data={'n': n, 'd': d}
    )
    freq_id = error_registry.store(freq_data)
    
    # Calculate frequencies
    freqs = np.fft.rfftfreq(n, d)
    
    # Create result object
    result = DimensionalArray(freqs, error_registry)
    
    # Preserve original error_id if it exists
    if original_error_id is not None:
        result._error_id = original_error_id
    
    return result

__all__ = [
    'fft2', 'ifft2', 'fftshift', 'ifftshift', 'fftfreq',
    'rfft2', 'irfft2', 'rfftfreq'
] 