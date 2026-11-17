"""
Dividebyzero: A framework for handling singularities in numerical computations.
"""

import numpy as np
# Use relative imports for package structure
from .array import DimensionalArray
from .registry import ErrorRegistry, ErrorData
from .exceptions import DimensionalError, ReconstructionError
from . import numpy_compat  # This will register all numpy functions
from .numpy_registry import _numpy_functions, _numpy_attributes
from . import quantum
from . import linalg
from . import random
from . import fft  # Add FFT module
import logging

# Import from consolidated logarithms module
from .logarithms import (
    log, log2, log10, logm, log1p, log_entropy,
    matrix_logm_divide, quantum_log_entropy, log_negativity,
    extend_dimensional_array, extend_quantum_tensor
)

# Log a notice about the old modules being removed
logging.warning(
    "The logarithmic_functions.py and logarithm_extensions.py modules "
    "have been removed. Please use the consolidated logarithms.py module instead."
)

from .powers import power, matrix_power

# Create a module-level registry
_REGISTRY = ErrorRegistry()

# Apply extensions
extend_dimensional_array()
extend_quantum_tensor()

# Add mathematical constants
pi = np.pi
e = np.e
inf = np.inf
nan = np.nan

# Add newaxis attribute
newaxis = None

# Add commonly used functions
zeros = lambda *args, **kwargs: array(np.zeros(*args, **kwargs))
ones = lambda *args, **kwargs: array(np.ones(*args, **kwargs))
eye = lambda *args, **kwargs: array(np.eye(*args, **kwargs))
zeros_like = lambda *args, **kwargs: array(np.zeros_like(*args, **kwargs))
ones_like = lambda *args, **kwargs: array(np.ones_like(*args, **kwargs))

# Add commonly used mathematical functions
abs = lambda x: array(np.abs(x.array if isinstance(x, DimensionalArray) else x))
sin = lambda x: array(np.sin(x.array if isinstance(x, DimensionalArray) else x))
cos = lambda x: array(np.cos(x.array if isinstance(x, DimensionalArray) else x))
tan = lambda x: array(np.tan(x.array if isinstance(x, DimensionalArray) else x))
exp = lambda x: array(np.exp(x.array if isinstance(x, DimensionalArray) else x))
sqrt = lambda x: array(np.sqrt(x.array if isinstance(x, DimensionalArray) else x))

# Add complex number functions
conj = lambda x: array(np.conj(x.array if isinstance(x, DimensionalArray) else x))
angle = lambda x: array(np.angle(x.array if isinstance(x, DimensionalArray) else x))
real = lambda x: array(np.real(x.array if isinstance(x, DimensionalArray) else x))
imag = lambda x: array(np.imag(x.array if isinstance(x, DimensionalArray) else x))

# Add array manipulation functions
sum = lambda x, *args, **kwargs: array(np.sum(x.array if isinstance(x, DimensionalArray) else x, *args, **kwargs))
where = lambda cond, x, y: array(np.where(
    cond.array if isinstance(cond, DimensionalArray) else cond,
    x.array if isinstance(x, DimensionalArray) else x,
    y.array if isinstance(y, DimensionalArray) else y
))
isnan = lambda x: array(np.isnan(x.array if isinstance(x, DimensionalArray) else x))
einsum = lambda subscripts, *operands: array(np.einsum(subscripts, *(
    x.array if isinstance(x, DimensionalArray) else x for x in operands
)))

# Add NumPy dtype aliases
float32 = np.float32
float64 = np.float64
int32 = np.int32
int64 = np.int64
uint8 = np.uint8
uint16 = np.uint16
uint32 = np.uint32
uint64 = np.uint64
complex64 = np.complex64
complex128 = np.complex128
bool_ = np.bool_

def get_registry():
    """Get the global error registry."""
    return _REGISTRY

def array(array_like, dtype=None, error_registry=None):
    """Create a DimensionalArray."""
    if error_registry is None:
        error_registry = _REGISTRY
    return DimensionalArray(array_like, error_registry=error_registry, dtype=dtype)

# New code:
filtered_numpy_functions = {k: v for k, v in _numpy_functions.items() if k.lower() != 'linalg'}
filtered_numpy_attributes = {k: v for k, v in _numpy_attributes.items() if k.lower() != 'linalg'}
globals().update(filtered_numpy_functions)
globals().update(filtered_numpy_attributes)

# Apply extensions
extend_dimensional_array()
extend_quantum_tensor()

# Build __all__ list
base_exports = [
    'array', 'zeros', 'ones', 'eye', 'zeros_like', 'ones_like',
    'DimensionalArray', 'ErrorRegistry', 'ErrorData',
    'DimensionalError', 'ReconstructionError',
    'get_registry', 'quantum', 'linalg', 'random', 'fft',  # Add fft to exports
    'pi', 'e', 'inf', 'nan', 'newaxis',
    'sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'logm',
    'linspace', 'arange', 'abs',
    'conj', 'angle', 'real', 'imag',  # Add complex functions
    'sum', 'where', 'isnan', 'einsum',
    'float32', 'float64', 'int32', 'int64',
    'uint8', 'uint16', 'uint32', 'uint64',
    'complex64', 'complex128', 'bool_', 'asnumpy',
    'log', 'log2', 'log10', 'logm', 'log1p', 'log_entropy',
    'matrix_logm_divide', 'quantum_log_entropy', 'log_negativity', 
    'power', 'matrix_power',
    # Add commonly used interpolation functions from old version
    'interp', 'lerp', 'logspace', 'geomspace', 'meshgrid',
    'broadcast_arrays', 'mgrid', 'ogrid'
]

__all__ = base_exports + [
    name for name in (_numpy_functions.keys() | _numpy_attributes.keys())
    if name not in base_exports
]
def set_log_level(level):
    """
    Set the logging level for the entire dividebyzero library.
    
    Args:
        level: The logging level to set. Can be a string ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
               or a corresponding integer value.
    """
    logger = logging.getLogger('dividebyzero')
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)

# Set default logging level to WARNING
set_log_level(logging.WARNING)

def asnumpy(x):
    """Convert array to numpy array."""
    if isinstance(x, DimensionalArray):
        return x.array
    return np.asarray(x)

# Add interpolation functions
interp = lambda x, xp, fp, left=None, right=None, period=None: array(
    np.interp(
        x.array if isinstance(x, DimensionalArray) else x,
        xp.array if isinstance(xp, DimensionalArray) else xp,
        fp.array if isinstance(fp, DimensionalArray) else fp,
        left=left, right=right, period=period
    )
)

def lerp(start, stop, fraction):
    """Linear interpolation between start and stop points.
    
    Parameters
    ----------
    start : array_like or scalar
        The starting point(s)
    stop : array_like or scalar
        The ending point(s)
    fraction : array_like or scalar
        The interpolation fraction(s), typically in range [0, 1]
        
    Returns
    -------
    result : DimensionalArray
        The interpolated value(s)
    """
    start_arr = start.array if isinstance(start, DimensionalArray) else start
    stop_arr = stop.array if isinstance(stop, DimensionalArray) else stop
    fraction_arr = fraction.array if isinstance(fraction, DimensionalArray) else fraction
    
    return array(start_arr * (1 - fraction_arr) + stop_arr * fraction_arr)

logspace = lambda *args, **kwargs: array(np.logspace(*args, **kwargs))

geomspace = lambda *args, **kwargs: array(np.geomspace(*args, **kwargs))

def meshgrid(*xi, indexing='xy', sparse=False, copy=True):
    """Return coordinate matrices from coordinate vectors.
    
    Makes N-D coordinate arrays for vectorized evaluations of N-D scalar/vector
    fields over N-D grids, given one-dimensional coordinate arrays x1, x2,..., xn.
    """
    # Convert any DimensionalArray inputs to numpy arrays
    xi_arrays = [x.array if isinstance(x, DimensionalArray) else x for x in xi]
    
    # Call numpy's meshgrid
    outputs = np.meshgrid(*xi_arrays, indexing=indexing, sparse=sparse, copy=copy)
    
    # Convert results back to DimensionalArray
    return tuple(array(x) for x in outputs)

def broadcast_arrays(*args):
    """Broadcast arrays to a common shape.
    
    Parameters
    ----------
    *args : array_like
        The arrays to broadcast.
        
    Returns
    -------
    result : tuple of DimensionalArrays
        Broadcasted arrays.
    """
    # Convert inputs to numpy arrays
    arrays = [x.array if isinstance(x, DimensionalArray) else x for x in args]
    
    # Broadcast arrays using numpy
    result = np.broadcast_arrays(*arrays)
    
    # Convert back to DimensionalArray
    return tuple(array(x) for x in result)

mgrid = lambda *args, **kwargs: array(np.mgrid[args])
ogrid = lambda *args, **kwargs: array(np.ogrid[args])
