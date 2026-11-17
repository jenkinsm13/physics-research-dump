"""
Quantum analysis module for DivideByZero framework.

This module provides quantum-specific functionality, including:
- Quantum tensor operations
- Fractal analysis
- Ordinal arithmetic and transfinite operations
- Quantum state analysis
"""

from .tensor import QuantumTensor, EntanglementSpectrum
from .fractal import QuantumStateVector
from .ordinal import Ordinal, TransfiniteSum, ordinal_distance, ordinal_logarithm
from .transfinite_tensor import TransfiniteTensor, shell_coupling_tensor, compute_shell_flow
from .coherence import CoherenceOperator
from .entropy import EntropyOperator
from .gauge import GaugeTransformation
from .gauge_groups import GaugeGroup
from .holonomy import HolonomyCalculator

__all__ = [
    'QuantumTensor',
    'EntanglementSpectrum',
    'QuantumStateVector',
    'Ordinal',
    'TransfiniteSum',
    'ordinal_distance',
    'ordinal_logarithm',
    'TransfiniteTensor',
    'shell_coupling_tensor',
    'compute_shell_flow',
    'CoherenceOperator',
    'EntropyOperator',
    'GaugeTransformation',
    'GaugeGroup',
    'HolonomyCalculator'
]

# Physical constants
PLANCK_LENGTH = 1.616255e-35  # meters
PLANCK_TIME = 5.391247e-44    # seconds
BOLTZMANN_CONSTANT = 1.380649e-23  # J/K

# Quantum configuration
DEFAULT_BOND_DIMENSION = 16
ENTANGLEMENT_CUTOFF = 1e-10
MAX_TRUNCATION_ERROR = 1e-12