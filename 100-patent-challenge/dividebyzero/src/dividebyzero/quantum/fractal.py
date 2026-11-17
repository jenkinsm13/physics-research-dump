"""
Quantum analysis of fractal systems with non-integer dimensional properties.

This module extends the quantum capabilities of DivideByZero to analyze
entanglement scaling, quantum walk dynamics, and phase transitions in
fractal geometries, leveraging the framework's ability to handle
operations in non-integer dimensional spaces.

The module properly implements the DivideByZero formalism for fractional dimensions
and handles dimensional reduction for quantum operations in non-integer spaces.
"""

import numpy as np
from ..array import DimensionalArray
from .tensor import QuantumTensor, EntanglementSpectrum
from .. import linalg
from typing import List, Tuple, Callable, Optional, Union
from ..registry import ErrorData, ErrorRegistry
from ..exceptions import DimensionalError
# Import specific power and logarithmic functions for proper singularity handling
from ..powers import power, matrix_power
from ..logarithms import log, log2, log10

class QuantumStateVector(QuantumTensor):
    """
    Representation of a quantum state vector with support for quantum operations.
    
    This class extends DimensionalArray with quantum-specific functionality while
    maintaining compatibility with the existing framework architecture.
    """
    def __init__(self, data, physical_dims=None, fractal_dimension=None, dtype=None):
        """
        Initialize quantum state vector.
        
        Parameters
        ----------
        data : array_like
            State vector data
        physical_dims : tuple, optional
            Physical dimensions for interpretation
        fractal_dimension : float, optional
            Fractal dimension of the system
        dtype : data-type, optional
            Data type (defaults to complex)
        """
        from .. import sum, sqrt, abs
        
        # Initialize with complex data type by default for quantum states
        super().__init__(data, fractal_dimension=fractal_dimension, dtype=dtype or complex)
        self.physical_dims = physical_dims
        
        # Use framework's approach for normalization
        # This properly handles potential singularities
        norm_squared = sum(abs(self)**2)
        
        # Use error tracking instead of direct threshold
        from ..registry import ErrorData
        norm_error_data = ErrorData(
            original_shape=(1,),
            error_tensor=np.array([float(norm_squared.array) - 1.0]),
            reduction_type='normalization',
            manifold_data={'target_norm': 1.0}
        )
        norm_error_id = self.error_registry.store(norm_error_data)
        
        # Apply normalization regardless to ensure proper state representation
        self.array = self.array / sqrt(norm_squared)
    
    def to_density_matrix(self) -> 'QuantumDensityMatrix':
        """
        Convert to density matrix using proper framework operations.
        """
        from .. import zeros, conjugate, outer
        
        state_vec = self.reshape(-1)
        # Use framework's outer product operation
        density = outer(state_vec, conjugate(state_vec))
        return QuantumDensityMatrix(density, self.physical_dims)
    
    def apply_operator(self, operator: DimensionalArray) -> 'QuantumStateVector':
        """
        Apply quantum operator to state vector.
        
        Parameters
        ----------
        operator : DimensionalArray
            Quantum operator as DimensionalArray
            
        Returns
        -------
        QuantumStateVector
            Resulting quantum state vector
        """
        new_state = operator @ self.reshape(-1)
        return QuantumStateVector(new_state, self.physical_dims)
    
    def expectation_value(self, operator: DimensionalArray) -> complex:
        """
        Compute expectation value of an operator.
        
        Parameters
        ----------
        operator : DimensionalArray
            Quantum operator as DimensionalArray
            
        Returns
        -------
        complex
            Complex expectation value ⟨ψ|O|ψ⟩
        """
        from .. import sum, conjugate
        
        state_vec = self.reshape(-1)
        return sum(conjugate(state_vec) * (operator @ state_vec))
    
    def schmidt_decomposition(self, partition_ratio, fractal_dimension=None):
        # Use instance fractal dimension if not provided
        d = fractal_dimension or self._fractal_dimension
        if not d:
            raise ValueError("Fractal dimension must be specified")
            
        # Convert to density matrix first
        density_matrix = self.to_density_matrix()
        
        # Calculate effective subsystem size based on fractal dimension
        from .. import power
        
        system_size = len(self.reshape(-1))
        effective_linear_size = power(system_size, 1/d)
        subsystem_a_size = int(power(effective_linear_size * partition_ratio, d))
        
        # Perform partial trace operations
        subsystem_a, subsystem_b = density_matrix.partial_trace(subsystem_a_size)
        
        # Store any dimensional reduction errors
        if hasattr(effective_linear_size, '_error_id'):
            self.error_registry.store(
                ErrorData(
                    original_shape=effective_linear_size.shape,
                    error_tensor=effective_linear_size.array,
                    reduction_type='fractal',
                    manifold_data={'dimension': d}
                )
            )
        
        return subsystem_a, subsystem_b


class QuantumDensityMatrix(DimensionalArray):
    """
    Representation of a quantum density matrix with support for quantum operations.
    
    This class extends DimensionalArray with functionality specific to density matrices
    while maintaining compatibility with the existing framework architecture.
    """
    def __init__(self, data, physical_dims=None, dtype=None):
        """
        Initialize quantum density matrix.
        
        Parameters
        ----------
        data : array_like
            Density matrix data
        physical_dims : tuple, optional
            Physical dimensions for interpretation
        dtype : data-type, optional
            Data type (defaults to complex)
        """
        from .. import sum, diag, abs
        
        # Initialize with complex data type by default for quantum states
        super().__init__(data, dtype=dtype or complex)
        self.physical_dims = physical_dims
        
        # Ensure trace normalization using proper framework approach
        trace = sum(diag(self.array))
        
        # Use error tracking instead of direct threshold
        from ..registry import ErrorData
        # Check if trace is DimensionalArray or a scalar
        trace_value = float(trace.array if hasattr(trace, 'array') else trace)
        trace_error_data = ErrorData(
            original_shape=(1,),
            error_tensor=np.array([trace_value - 1.0]),
            reduction_type='trace_normalization',
            manifold_data={'target_trace': 1.0}
        )
        self.error_registry.store(trace_error_data)
        
        # Always normalize to ensure proper density matrix
        self.array = self.array / trace
    
    def partial_trace(self, subsystem_a_size: int) -> Tuple['QuantumDensityMatrix', 'QuantumDensityMatrix']:
        """
        Perform partial trace operation to obtain reduced density matrices.
        
        Parameters
        ----------
        subsystem_a_size : int
            Size of subsystem A
            
        Returns
        -------
        Tuple[QuantumDensityMatrix, QuantumDensityMatrix]
            Reduced density matrices for subsystems A and B
        """
        from .. import zeros
        
        # Input validation
        if subsystem_a_size <= 0 or subsystem_a_size >= self.shape[0]:
            raise DimensionalError(f"Subsystem A size must be between 1 and {self.shape[0]-1}")
        
        system_size = self.shape[0]
        subsystem_b_size = system_size - subsystem_a_size
        
        # Define index ranges for subsystems
        indices_a = list(range(subsystem_a_size))
        indices_b = list(range(subsystem_a_size, system_size))
        
        # Calculate reduced density matrix for subsystem A by tracing over subsystem B
        rho_a = zeros((subsystem_a_size, subsystem_a_size), dtype=complex)
        for i in range(subsystem_a_size):
            for j in range(subsystem_a_size):
                # Proper trace operation involves summing over all indices of B
                for k in range(subsystem_b_size):
                    b_idx = indices_b[k]
                    # Get indices for full density matrix element
                    full_idx_i = i * system_size + b_idx
                    full_idx_j = j * system_size + b_idx
                    # Add to the reduced density matrix
                    rho_a[i, j] += self[full_idx_i // system_size, full_idx_j % system_size]
        
        # Calculate reduced density matrix for subsystem B by tracing over subsystem A
        rho_b = zeros((subsystem_b_size, subsystem_b_size), dtype=complex)
        for i in range(subsystem_b_size):
            for j in range(subsystem_b_size):
                # Proper trace operation involves summing over all indices of A
                for k in range(subsystem_a_size):
                    a_idx = indices_a[k]
                    # Get indices for full density matrix element
                    full_idx_i = a_idx * system_size + (i + subsystem_a_size)
                    full_idx_j = a_idx * system_size + (j + subsystem_a_size)
                    # Add to the reduced density matrix
                    rho_b[i, j] += self[full_idx_i // system_size, full_idx_j % system_size]
        
        # Track error information
        error_data = ErrorData(
            original_shape=self.shape,
            error_tensor=self.array,
            reduction_type='partial_trace',
            manifold_data={'subsystem_a_size': subsystem_a_size}
        )
        error_id = self.error_registry.store(error_data)
        
        # Create result objects with error tracking
        rho_a_result = QuantumDensityMatrix(rho_a)
        rho_b_result = QuantumDensityMatrix(rho_b)
        rho_a_result._error_id = error_id
        rho_b_result._error_id = error_id
        
        return rho_a_result, rho_b_result
    
    def entropy(self) -> float:
        """
        Compute von Neumann entropy S = -Tr(ρ log ρ).
        
        This implementation uses the centralized entropy module which properly handles
        zero eigenvalues through the DivideByZero framework's dimensional reduction approach.
        
        Returns
        -------
        float
            Von Neumann entropy
        """
        from .entropy import von_neumann_entropy
        return von_neumann_entropy(self, self.error_registry)
    
    def renyi_entropy(self, alpha: float = 2.0) -> float:
        """
        Compute Rényi entropy of order alpha.
        
        S_α = (1/(1-α)) log Tr(ρ^α)
        
        This implementation uses the centralized entropy module which properly handles
        zero eigenvalues through the DivideByZero framework's dimensional reduction approach.
        
        Parameters
        ----------
        alpha : float
            Rényi parameter (α ≠ 1)
            
        Returns
        -------
        float
            Rényi entropy of order alpha
        """
        from .entropy import renyi_entropy
        return renyi_entropy(self, alpha, self.error_registry)


def generate_sierpinski_quantum_state(order: int, state_type: str = "uniform") -> QuantumStateVector:
    """
    Generate a quantum state defined on a Sierpinski fractal lattice.
    
    Parameters
    ----------
    order : int
        Recursion depth of the fractal
    state_type : str
        Initial state configuration: "uniform", "localized", or "random"
    
    Returns
    -------
    QuantumStateVector
        Quantum state vector defined on the fractal lattice
    """
    # Generate classical fractal structure
    size = 2**order
    lattice = _generate_sierpinski_lattice(size)
    
    # Create quantum state vector
    state_vector = _create_quantum_state(lattice, state_type)
    
    # Create QuantumStateVector with appropriate physical dimensions
    return QuantumStateVector(state_vector, physical_dims=(size, size))


def _generate_sierpinski_lattice(size: int) -> DimensionalArray:
    """Generate Sierpinski triangle lattice of given size."""
    from .. import zeros
    
    lattice = zeros((size, size))
    
    def fill_sierpinski(x, y, size):
        if size == 1:
            lattice[y, x] = 1
            return
        
        half_size = size // 2
        fill_sierpinski(x, y, half_size)
        fill_sierpinski(x + half_size, y, half_size)
        fill_sierpinski(x, y + half_size, half_size)
    
    fill_sierpinski(0, 0, size)
    return lattice


def _create_quantum_state(lattice: DimensionalArray, state_type: str) -> DimensionalArray:
    """Create quantum state on fractal lattice."""
    from .. import zeros, sum, power
    import random
    
    size = lattice.shape[0]
    state_vector = zeros(size * size, dtype=complex)
    
    if state_type == "uniform":
        # Uniform superposition over occupied sites
        occupied_sites = sum(lattice)
        amplitude = power(occupied_sites, -0.5)  # Normalize amplitude
        
        for i in range(size):
            for j in range(size):
                if lattice[i, j] > 0:
                    index = i * size + j
                    state_vector[index] = amplitude
    
    elif state_type == "localized":
        # Localized state at the origin
        state_vector[0] = 1.0
    
    elif state_type == "random":
        # Random state with amplitudes only on occupied sites
        # Find occupied sites
        occupied_indices = []
        for i in range(size):
            for j in range(size):
                if lattice[i, j] > 0:
                    occupied_indices.append(i * size + j)
        
        # Generate random amplitudes
        amplitudes = []
        for _ in range(len(occupied_indices)):
            real_part = random.uniform(-1, 1)
            imag_part = random.uniform(-1, 1)
            amplitudes.append(complex(real_part, imag_part))
        
        # Normalize
        from .. import sum, sqrt
        norm_squared = sum([abs(amp)**2 for amp in amplitudes])
        normalization = 1.0 / sqrt(norm_squared)
        
        # Assign to state vector
        for idx, amp in zip(occupied_indices, amplitudes):
            state_vector[idx] = amp * normalization
    
    return state_vector


def fractal_quantum_walk(initial_state: QuantumStateVector, 
                        steps: int, 
                        fractal_dimension: float) -> DimensionalArray:
    """
    Simulate quantum walk dynamics on fractal lattice.
    
    Parameters
    ----------
    initial_state : QuantumStateVector
        Initial quantum state
    steps : int
        Number of time steps
    fractal_dimension : float
        Fractal dimension of the lattice
    
    Returns
    -------
    DimensionalArray
        Spatial spread measurements at each time step
    """
    from .. import zeros, eye, sqrt, sum, power, abs
    
    # Extract state information
    state_vector = initial_state.reshape(-1)
    system_size = len(state_vector)
    size = int(sqrt(system_size))
    
    # Create fractal hamiltonian
    hamiltonian = _create_fractal_hamiltonian(size, fractal_dimension)
    
    # Position operators for measuring spread
    x_positions = zeros(system_size)
    y_positions = zeros(system_size)
    
    for i in range(size):
        for j in range(size):
            idx = i * size + j
            x_positions[idx] = j
            y_positions[idx] = i
    
    # Evolution loop
    state = state_vector.copy()
    spread_measures = zeros(steps + 1)
    
    for t in range(steps + 1):
        # Calculate spread at current time
        prob_distribution = abs(state)**2
        
        # Mean position
        mean_x = sum(prob_distribution * x_positions)
        mean_y = sum(prob_distribution * y_positions)
        
        # Variance (spread)
        var_x = sum(prob_distribution * power(x_positions - mean_x, 2))
        var_y = sum(prob_distribution * power(y_positions - mean_y, 2))
        
        # Overall spatial spread
        spread_measures[t] = sqrt(var_x + var_y)
        
        if t < steps:
            # Time evolution using Hamiltonian
            time_factor = power(t + 1, (2 - fractal_dimension) / 2)
            evolution_operator = eye(hamiltonian.shape[0]) - 1j * hamiltonian * time_factor
            state = evolution_operator @ state
            
            # Renormalize
            norm = sqrt(sum(abs(state)**2))
            state = state / norm
    
    return spread_measures


def _create_fractal_hamiltonian(size: int, 
                              fractal_dimension: float) -> DimensionalArray:
    """Create Hamiltonian for fractal lattice with proper dimensional scaling."""
    from .. import zeros
    
    # Validate fractal dimension
    if fractal_dimension <= 0:
        raise DimensionalError("Fractal dimension must be positive")
    
    # Create fractal connectivity matrix
    sierpinski = _generate_sierpinski_lattice(size)
    system_size = size * size
    hamiltonian = zeros((system_size, system_size))
    
    # Fill Hamiltonian based on fractal connectivity
    for i in range(size):
        for j in range(size):
            if sierpinski[i, j] > 0:
                idx = i * size + j
                
                # Connect to neighbors that exist in the fractal
                neighbors = []
                if i > 0 and sierpinski[i-1, j] > 0:
                    neighbors.append((i-1) * size + j)
                if i < size-1 and sierpinski[i+1, j] > 0:
                    neighbors.append((i+1) * size + j)
                if j > 0 and sierpinski[i, j-1] > 0:
                    neighbors.append(i * size + (j-1))
                if j < size-1 and sierpinski[i, j+1] > 0:
                    neighbors.append(i * size + (j+1))
                
                for neighbor_idx in neighbors:
                    hamiltonian[idx, neighbor_idx] = 1.0
    
    # Normalize according to fractal dimension using the framework's power function
    # for proper handling of singularities and non-integer exponents
    normalization = power(DimensionalArray(size), fractal_dimension / 2)
    
    # Create error data for tracking
    error_data = ErrorData(
        original_shape=hamiltonian.shape,
        error_tensor=hamiltonian.array,
        reduction_type='fractal',
        manifold_data={'fractal_dimension': fractal_dimension}
    )
    error_id = hamiltonian.error_registry.store(error_data)
    
    # Use division operation from framework for potential singularity handling
    result = hamiltonian / normalization
    
    # Preserve error tracking
    if not hasattr(result, '_error_id') or result._error_id is None:
        result._error_id = error_id
    
    return result


def analyze_entanglement_scaling(fractal_dimension: float, 
                              max_order: int = 6) -> Tuple[DimensionalArray, DimensionalArray]:
    """
    Analyze entanglement entropy scaling with subsystem size in fractal systems.
    
    Parameters
    ----------
    fractal_dimension : float
        Fractal dimension of the lattice
    max_order : int
        Maximum order of the Sierpinski gasket
        
    Returns
    -------
    Tuple[DimensionalArray, DimensionalArray]
        Subsystem sizes and corresponding entanglement entropies
    """
    from .. import array, log, sum, power
    
    subsystem_sizes = []
    entropies = []
    
    # Analyze different system sizes to reveal scaling
    for order in range(3, max_order + 1):
        # Generate quantum state
        quantum_state = generate_sierpinski_quantum_state(order, "uniform")
        
        # Analyze different partition ratios
        for partition_ratio in [0.1, 0.2, 0.3, 0.4, 0.5]:
            # Perform Schmidt decomposition
            subsystem_a, _ = quantum_state.schmidt_decomposition(partition_ratio, fractal_dimension)
            
            # Calculate entropy
            entropy = subsystem_a.entropy()
            
            # Calculate effective subsystem size
            system_size = 2**order
            effective_linear_size = power(system_size * system_size, 1/fractal_dimension)
            subsystem_linear_size = effective_linear_size * partition_ratio
            
            subsystem_sizes.append(subsystem_linear_size)
            entropies.append(entropy)
    
    return array(subsystem_sizes), array(entropies)


def analyze_quantum_phase_transitions(fractal_dimension: float, 
                                   disorder_strengths: List[float],
                                   order: int = 5,
                                   ensemble_size: int = 5) -> DimensionalArray:
    """
    Analyze quantum phase transitions in disordered fractal systems.
    
    Parameters
    ----------
    fractal_dimension : float
        Fractal dimension of the lattice
    disorder_strengths : List[float]
        List of disorder strength parameters
    order : int
        Fractal order
    ensemble_size : int
        Number of disorder realizations to average over
    
    Returns
    -------
    DimensionalArray
        Order parameters for different disorder strengths
    """
    from .. import zeros, sum, power, eye, abs, random
    
    order_parameters = zeros(len(disorder_strengths))
    
    for d_idx, disorder in enumerate(disorder_strengths):
        # Generate ensemble of disordered systems
        ensemble_results = zeros(ensemble_size)
        
        for e_idx in range(ensemble_size):
            # Generate base fractal lattice
            sierpinski = _generate_sierpinski_lattice(2**order)
            size = sierpinski.shape[0]
            system_size = size * size
            
            # Create Hamiltonian with disorder
            hamiltonian = zeros((system_size, system_size))
            
            # Add hopping terms and disorder
            for i in range(size):
                for j in range(size):
                    if sierpinski[i, j] > 0:
                        idx = i * size + j
                        
                        # Add diagonal disorder
                        hamiltonian[idx, idx] = (random.random() - 0.5) * 2 * disorder
                        
                        # Add hopping terms
                        neighbors = []
                        if i > 0 and sierpinski[i-1, j] > 0:
                            neighbors.append((i-1) * size + j)
                        if i < size-1 and sierpinski[i+1, j] > 0:
                            neighbors.append((i+1) * size + j)
                        if j > 0 and sierpinski[i, j-1] > 0:
                            neighbors.append(i * size + (j-1))
                        if j < size-1 and sierpinski[i, j+1] > 0:
                            neighbors.append(i * size + (j+1))
                        
                        for neighbor_idx in neighbors:
                            hamiltonian[idx, neighbor_idx] = 1.0
            
            # Scale Hamiltonian according to fractal dimension
            normalization = power(size, fractal_dimension / 2)
            hamiltonian = hamiltonian / normalization
            
            # Calculate ground state properties
            eigenvalues, eigenvectors = linalg.eigh(hamiltonian)
            ground_state = eigenvectors[:, 0]
            
            # Calculate participation ratio
            participation_ratio = 1.0 / sum(power(abs(ground_state), 4))
            normalized_pr = participation_ratio / system_size
            
            ensemble_results[e_idx] = normalized_pr
        
        # Average over ensemble
        order_parameters[d_idx] = sum(ensemble_results) / ensemble_size
    
    return order_parameters