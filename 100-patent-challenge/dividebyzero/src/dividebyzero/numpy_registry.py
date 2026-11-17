"""
Registry for numpy function compatibility.
"""

import numpy as np
from typing import Optional, Dict, Callable, Any
from functools import wraps
from numpy import dtype as np_dtype

_numpy_functions: Dict[str, Callable] = {}
_numpy_attributes: Dict[str, Any] = {}

def register_numpy_attribute(name: str, value: Any) -> None:
    """Register a numpy attribute (like dtypes, constants)."""
    if isinstance(value, np_dtype):
        # For dtype objects, store the actual type
        _numpy_attributes[name] = value.type
    else:
        _numpy_attributes[name] = value

def register_numpy_function(name: str, func: Callable) -> None:
    """Register a numpy function with its wrapped version."""
    _numpy_functions[name] = func

def get_numpy_attribute(name: str) -> Optional[Any]:
    """Get a registered numpy attribute if it exists."""
    return _numpy_attributes.get(name)

def get_numpy_function(name: str) -> Optional[Callable]:
    """Get the wrapped version of a numpy function if it exists."""
    return _numpy_functions.get(name)

def wrap_and_register_numpy_function(np_func: Callable) -> Callable:
    """
    Enhanced wrapper with specialized handling for logarithmic functions.
    Implements dimensional reduction for logarithmic singularities across
    all NumPy function calls.
    """
    from .array import DimensionalArray
    
    # Identify functions that require special handling
    log_functions = {
        'log', 'log2', 'log10', 'log1p', 'logaddexp', 'logaddexp2',
        'logspace'
    }
    
    # Functions that handle singularities like divisions by zero
    singularity_functions = {
        'power', 'sqrt'
    }
    
    func_name = np_func.__name__
    is_log_function = func_name in log_functions
    is_singularity_function = func_name in singularity_functions
    
    @wraps(np_func)
    def wrapper(*args, **kwargs):
        # Special handling for logarithmic functions
        if is_log_function and isinstance(args[0], DimensionalArray):
            # Use our logarithmic functions directly
            from .logarithms import log, log2, log10, log1p
            if func_name == 'log':
                return log(args[0])
            elif func_name == 'log2':
                return log2(args[0])
            elif func_name == 'log10':
                return log10(args[0])
            elif func_name == 'log1p':
                return log1p(args[0])
        
        # Special handling for power functions
        if is_singularity_function and len(args) >= 2:
            from .powers import power
            if func_name == 'power' and isinstance(args[0], DimensionalArray) or isinstance(args[1], DimensionalArray):
                return power(args[0], args[1])
            elif func_name == 'sqrt' and isinstance(args[0], DimensionalArray):
                return power(args[0], 0.5)
        
        # Convert dbz arrays to numpy arrays for input
        args = [(arg.array if isinstance(arg, DimensionalArray) else arg) for arg in args]
        kwargs = {k: (v.array if isinstance(v, DimensionalArray) else v) for k, v in kwargs.items()}
        
        # Special handling for division operations
        if func_name in {'divide', 'true_divide'}:
            dividend, divisor = args[:2]
            # Convert to array objects if needed
            div_array = getattr(divisor, 'array', divisor)
            # Check for zeros specifically 
            if np.any(np.isclose(div_array, 0)):
                # Force dimensional divide path
                return DimensionalArray(dividend).dimensional_divide(divisor)
        
        # Standard execution for non-logarithmic functions
        result = np_func(*args, **kwargs)
        
        # Convert result back to dbz array
        if isinstance(result, np.ndarray):
            return DimensionalArray(result)
        elif isinstance(result, tuple):
            return tuple(DimensionalArray(r) if isinstance(r, np.ndarray) else r for r in result)
        return result
    
    register_numpy_function(np_func.__name__, wrapper)
    return wrapper

# Register core numpy operations
register_numpy_function('divide', wrap_and_register_numpy_function(np.divide))
register_numpy_function('true_divide', wrap_and_register_numpy_function(np.true_divide))
register_numpy_function('log', wrap_and_register_numpy_function(np.log))
register_numpy_function('log2', wrap_and_register_numpy_function(np.log2))
register_numpy_function('log10', wrap_and_register_numpy_function(np.log10))
register_numpy_function('log1p', wrap_and_register_numpy_function(np.log1p))
register_numpy_function('logaddexp', wrap_and_register_numpy_function(np.logaddexp))
register_numpy_function('logaddexp2', wrap_and_register_numpy_function(np.logaddexp2))
register_numpy_function('power', wrap_and_register_numpy_function(np.power))
register_numpy_function('sqrt', wrap_and_register_numpy_function(np.sqrt)) 