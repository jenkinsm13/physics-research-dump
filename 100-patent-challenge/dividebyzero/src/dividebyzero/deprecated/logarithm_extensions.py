from ..array import DimensionalArray
from ..quantum.tensor import QuantumTensor
from .logarithmic_functions import (
    log as log_func,
    log2 as log2_func,
    log10 as log10_func,
    logm as logm_func,
    log_entropy as log_entropy_func,
    matrix_logm_divide,
    quantum_log_entropy,
    log_negativity as log_negativity_func
)
import numpy as np

def extend_dimensional_array():
    """
    Extend the DimensionalArray class with logarithmic dimensional manifold capabilities.
    
    This function should be called during framework initialization to add
    logarithmic operations to the DimensionalArray class.
    """
    from ..array import DimensionalArray
    
    # Add logarithmic division method
    original_truediv = DimensionalArray.__truediv__
    
    def enhanced_truediv(self, other):
        """
        Enhanced division with logarithmic dimensional manifold handling.
        
        For zero divisors, implements division through logarithmic space
        where division becomes subtraction of logarithms.
        """
        if isinstance(other, (int, float)):
            if other == 0:
                # For scalar zero, use DimensionalArray's direct division by zero 
                # This ensures proper error tracking for elevation
                return self._divide_by_zero()
            # Use standard division for non-zero scalars
            return original_truediv(self, other)
        
        if isinstance(other, DimensionalArray):
            # Check for zeros in denominator
            if np.any(other.array == 0):
                # Handle zeros via DimensionalArray's methods for proper error tracking
                if other.array.size == 1 and other.array.item() == 0:
                    # Single scalar zero
                    return self._divide_by_zero()
                else:
                    # More complex zero pattern - use partial divide by zero
                    mask = other.array == 0
                    return self._partial_divide_by_zero(mask)
            # Use standard division for non-zero arrays
            return original_truediv(self, other)
        
        # Handle other types as before
        return original_truediv(self, other)
    
    # Replace method with enhanced version
    DimensionalArray.__truediv__ = enhanced_truediv
    
    # Add logarithm methods
    def log(self, base=None):
        """
        Compute logarithm with dimensional manifold singularity handling.
        """
        from .logarithmic_functions import log as log_func
        return log_func(self, base)
    
    DimensionalArray.log = log
    
    def log2(self):
        """
        Compute base-2 logarithm with dimensional manifold singularity handling.
        """
        from .logarithmic_functions import log2 as log2_func
        return log2_func(self)
    
    DimensionalArray.log2 = log2
    
    def log10(self):
        """
        Compute base-10 logarithm with dimensional manifold singularity handling.
        """
        from .logarithmic_functions import log10 as log10_func
        return log10_func(self)
    
    DimensionalArray.log10 = log10
    
    def logm(self, preserve_structure=True, branch_cut='principal'):
        """
        Compute matrix logarithm with dimensional manifold singularity handling.
        """
        from .logarithmic_functions import logm as logm_func
        return logm_func(self, preserve_structure, branch_cut)
    
    DimensionalArray.logm = logm
    
    def log_entropy(self, axis=None):
        """
        Compute logarithmic entropy with dimensional manifold approach.
        """
        from .logarithmic_functions import log_entropy as log_entropy_func
        return log_entropy_func(self, axis)
    
    DimensionalArray.log_entropy = log_entropy
    
    return DimensionalArray


def extend_quantum_tensor():
    """
    Extend the QuantumTensor class with logarithmic dimensional manifold capabilities.
    
    This function should be called during framework initialization to add
    logarithmic operations to the QuantumTensor class.
    """
    from ..quantum.tensor import QuantumTensor
    
    # Add quantum logarithm method
    def logm(self, preserve_entanglement=True):
        """
        Compute logarithm of quantum state with entanglement preservation.
        
        Implements logarithmic dimensional manifold approach for quantum states,
        preserving entanglement structure and quantum information.
        """
        from .logarithmic_functions import logm as logm_func
        return logm_func(self.data, preserve_entanglement)
    
    QuantumTensor.logm = logm
    
    # Add quantum entropy method
    def von_neumann_entropy(self):
        """
        Compute von Neumann entropy S(ρ) = -Tr(ρ log ρ).
        
        Uses logarithmic dimensional manifold approach to handle
        zero eigenvalues in the density matrix.
        """
        from .logarithmic_functions import quantum_log_entropy
        return quantum_log_entropy(self)
    
    QuantumTensor.von_neumann_entropy = von_neumann_entropy
    
    # Add logarithmic negativity method
    def log_negativity(self):
        """
        Compute logarithmic negativity for entanglement quantification.
        
        Implements EN(ρ) = log₂ ||ρᵀₐ||₁ using dimensional manifold approach.
        """
        from .logarithmic_functions import log_negativity
        return log_negativity(self)
    
    QuantumTensor.log_negativity = log_negativity
    
    return QuantumTensor