"""
Temporal Flow for Matryoshka Temporal Shell Framework

This module implements the bidirectional temporal flow mechanisms of the
Matryoshka model. It defines the forward and inverse flow equations that
govern the dynamics between nested temporal shells. The inverse flow is
particularly significant as it manifests as gravitational effects.

Key components:
- Forward temporal flow (future to past)
- Inverse temporal flow (past to future)
- Flow operators and dynamics
- Conservation laws and flow equilibrium
"""

import numpy as np
import sympy as sp
from sympy import Symbol, Function, Eq, exp, Matrix
import matplotlib.pyplot as plt
from typing import Union, Tuple, List, Dict, Optional, Callable

from matryoshka.core.ordinals import Ordinal
from matryoshka.core.shell_structure import ShellStructure


class TemporalFlow:
    """
    Class implementing bidirectional temporal flow in the Matryoshka framework.
    
    Temporal flow represents the influence propagation between shells,
    with forward flow (future→past) and inverse flow (past→future).
    The inverse flow manifests as gravitational effects.
    """
    
    def __init__(self, 
                 shell_structure: ShellStructure,
                 kappa_plus: float = 1.0,
                 kappa_minus: float = 0.8):
        """
        Initialize temporal flow with a shell structure.
        
        Args:
            shell_structure: ShellStructure object
            kappa_plus: Forward flow constant
            kappa_minus: Inverse flow constant
        """
        self.shell_structure = shell_structure
        self.kappa_plus = kappa_plus
        self.kappa_minus = kappa_minus
    
    def forward_flow(self, i: Union[Ordinal, int], j: Union[Ordinal, int]) -> float:
        """
        Calculate forward temporal flow from shell i to shell j.
        Forward flow goes from inner (future) to outer (past) shells.
        
        Args:
            i: Ordinal index of source shell (future)
            j: Ordinal index of target shell (past)
            
        Returns:
            float: Forward flow magnitude
        """
        if isinstance(i, int):
            i = Ordinal.finite(i)
        if isinstance(j, int):
            j = Ordinal.finite(j)
        
        # Forward flow only occurs from inner to outer shells (future to past)
        if i >= j:
            return 0.0
        
        # Get shell radii and coupling
        r_i = self.shell_structure.shell_radius(i)
        r_j = self.shell_structure.shell_radius(j)
        c_ij = self.shell_structure.shell_coupling(i, j)
        
        # Forward flow equation
        return self.kappa_plus * c_ij / (r_j - r_i)
    
    def inverse_flow(self, i: Union[Ordinal, int], j: Union[Ordinal, int]) -> float:
        """
        Calculate inverse temporal flow from shell i to shell j.
        Inverse flow goes from outer (past) to inner (future) shells.
        This is what manifests as gravitational effects.
        
        Args:
            i: Ordinal index of source shell (past)
            j: Ordinal index of target shell (future)
            
        Returns:
            float: Inverse flow magnitude
        """
        if isinstance(i, int):
            i = Ordinal.finite(i)
        if isinstance(j, int):
            j = Ordinal.finite(j)
        
        # Inverse flow only occurs from outer to inner shells (past to future)
        if i <= j:
            return 0.0
        
        # Get shell radii and coupling
        r_i = self.shell_structure.shell_radius(i)
        r_j = self.shell_structure.shell_radius(j)
        c_ij = self.shell_structure.shell_coupling(i, j)
        
        # Inverse flow equation
        return self.kappa_minus * c_ij / (r_i - r_j)
    
    def forward_flow_symbolic(self, i, j, variables=None) -> sp.Expr:
        """
        Calculate symbolic expression for forward flow.
        
        Args:
            i: Index of source shell (can be a SymPy symbol)
            j: Index of target shell (can be a SymPy symbol)
            variables: Optional dictionary of symbols to use
            
        Returns:
            sympy.Expr: Symbolic expression for forward flow
        """
        if variables is None:
            variables = {
                'kappa_plus': Symbol('kappa^+', positive=True)
            }
        
        kappa_plus = variables.get('kappa_plus', Symbol('kappa^+', positive=True))
        
        # Use Heaviside step function for flow directionality
        theta = Function('Theta')(j - i)
        
        # Get symbolic expressions for radii and coupling
        r_i = self.shell_structure.shell_radius_symbolic(i)
        r_j = self.shell_structure.shell_radius_symbolic(j)
        c_ij = self.shell_structure.shell_coupling_symbolic(i, j)
        
        # Forward flow equation
        return kappa_plus * c_ij / (r_j - r_i) * theta
    
    def inverse_flow_symbolic(self, i, j, variables=None) -> sp.Expr:
        """
        Calculate symbolic expression for inverse flow.
        
        Args:
            i: Index of source shell (can be a SymPy symbol)
            j: Index of target shell (can be a SymPy symbol)
            variables: Optional dictionary of symbols to use
            
        Returns:
            sympy.Expr: Symbolic expression for inverse flow
        """
        if variables is None:
            variables = {
                'kappa_minus': Symbol('kappa^-', positive=True)
            }
        
        kappa_minus = variables.get('kappa_minus', Symbol('kappa^-', positive=True))
        
        # Use Heaviside step function for flow directionality
        theta = Function('Theta')(i - j)
        
        # Get symbolic expressions for radii and coupling
        r_i = self.shell_structure.shell_radius_symbolic(i)
        r_j = self.shell_structure.shell_radius_symbolic(j)
        c_ij = self.shell_structure.shell_coupling_symbolic(i, j)
        
        # Inverse flow equation
        return kappa_minus * c_ij / (r_i - r_j) * theta
    
    def net_flow(self, i: Union[Ordinal, int], j: Union[Ordinal, int]) -> float:
        """
        Calculate net temporal flow between shells i and j.
        
        Args:
            i: Ordinal index of the first shell
            j: Ordinal index of the second shell
            
        Returns:
            float: Net flow (positive means flow from i to j)
        """
        forward = self.forward_flow(i, j)
        inverse = self.inverse_flow(i, j)
        
        # Net flow from i to j
        return forward - inverse
    
    def total_outflow(self, i: Union[Ordinal, int], n_shells: int) -> float:
        """
        Calculate total outflow from shell i to all other shells.
        
        Args:
            i: Ordinal index of the source shell
            n_shells: Number of shells to consider
            
        Returns:
            float: Total outflow from shell i
        """
        outflow = 0.0
        
        for j in range(n_shells):
            if j != i:
                outflow += self.net_flow(i, j)
        
        return outflow
    
    def flow_conservation(self, n_shells: int) -> bool:
        """
        Check if flow is conserved across all shells.
        
        For a closed system, the sum of all net flows should be zero.
        
        Args:
            n_shells: Number of shells to consider
            
        Returns:
            bool: True if flow is conserved (within numerical precision)
        """
        total_flow = 0.0
        
        for i in range(n_shells):
            for j in range(n_shells):
                if i != j:
                    total_flow += self.net_flow(i, j)
        
        # Check if total flow is close to zero
        return abs(total_flow) < 1e-10
    
    def flow_equilibrium(self, n_shells: int, tolerance: float = 1e-6) -> bool:
        """
        Check if the shell system is in flow equilibrium.
        
        Equilibrium means each shell has balanced inflow and outflow.
        
        Args:
            n_shells: Number of shells to consider
            tolerance: Numerical tolerance for equilibrium
            
        Returns:
            bool: True if system is in equilibrium
        """
        for i in range(n_shells):
            outflow = self.total_outflow(i, n_shells)
            if abs(outflow) > tolerance:
                return False
        
        return True
    
    def flow_matrix(self, n_shells: int) -> np.ndarray:
        """
        Construct the flow matrix between shells.
        
        Each element (i,j) represents the net flow from i to j.
        
        Args:
            n_shells: Number of shells to consider
            
        Returns:
            numpy.ndarray: Flow matrix
        """
        matrix = np.zeros((n_shells, n_shells))
        
        for i in range(n_shells):
            for j in range(n_shells):
                if i != j:
                    matrix[i, j] = self.net_flow(i, j)
        
        return matrix


def visualize_temporal_flows(temporal_flow: TemporalFlow, n_shells: int = 10, plot_size: int = 8):
    """
    Visualize forward and inverse temporal flows between shells.
    
    Args:
        temporal_flow: TemporalFlow object
        n_shells: Number of shells to visualize
        plot_size: Size of the plot
    """
    # Compute flow matrices
    forward_matrix = np.zeros((n_shells, n_shells))
    inverse_matrix = np.zeros((n_shells, n_shells))
    
    for i in range(n_shells):
        for j in range(n_shells):
            if i != j:
                forward_matrix[i, j] = temporal_flow.forward_flow(i, j)
                inverse_matrix[i, j] = temporal_flow.inverse_flow(i, j)
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(plot_size*2, plot_size))
    
    # Plot forward flow
    im1 = ax1.imshow(forward_matrix, interpolation='nearest', cmap='Blues')
    ax1.set_title("Forward Temporal Flow (Future → Past)")
    plt.colorbar(im1, ax=ax1, label='Flow Magnitude')
    ax1.set_xlabel("Target Shell (j)")
    ax1.set_ylabel("Source Shell (i)")
    
    # Plot inverse flow
    im2 = ax2.imshow(inverse_matrix, interpolation='nearest', cmap='Reds')
    ax2.set_title("Inverse Temporal Flow (Past → Future)")
    plt.colorbar(im2, ax=ax2, label='Flow Magnitude')
    ax2.set_xlabel("Target Shell (j)")
    ax2.set_ylabel("Source Shell (i)")
    
    plt.tight_layout()
    return fig, (ax1, ax2)


def visualize_net_flow(temporal_flow: TemporalFlow, n_shells: int = 10, plot_size: int = 8):
    """
    Visualize net temporal flow between shells.
    
    Args:
        temporal_flow: TemporalFlow object
        n_shells: Number of shells to visualize
        plot_size: Size of the plot
    """
    # Compute net flow matrix
    net_matrix = temporal_flow.flow_matrix(n_shells)
    
    # Create figure
    plt.figure(figsize=(plot_size, plot_size))
    im = plt.imshow(net_matrix, interpolation='nearest', cmap='coolwarm')
    plt.colorbar(im, label='Net Flow Magnitude')
    
    # Add labels and title
    plt.title("Net Temporal Flow")
    plt.xlabel("Target Shell (j)")
    plt.ylabel("Source Shell (i)")
    
    return net_matrix


def derive_flow_equations(temporal_flow: TemporalFlow, variables=None) -> Tuple[sp.Eq, sp.Eq]:
    """
    Derive the symbolic flow equations.
    
    Args:
        temporal_flow: TemporalFlow object
        variables: Optional dictionary of symbols to use
        
    Returns:
        tuple: (forward_flow_eq, inverse_flow_eq) - Symbolic equations
    """
    if variables is None:
        variables = {}
    
    i = Symbol('i')
    j = Symbol('j')
    F_plus = Symbol('\\mathcal{F}^+_{i \\to j}')
    F_minus = Symbol('\\mathcal{F}^-_{i \\to j}')
    
    # Derive expressions
    forward_expr = temporal_flow.forward_flow_symbolic(i, j, variables)
    inverse_expr = temporal_flow.inverse_flow_symbolic(i, j, variables)
    
    return (Eq(F_plus, forward_expr), Eq(F_minus, inverse_expr))


def analyze_flow_conservation(temporal_flow: TemporalFlow, n_shells: int = 10) -> Dict[str, float]:
    """
    Analyze flow conservation across the shell system.
    
    Args:
        temporal_flow: TemporalFlow object
        n_shells: Number of shells to consider
        
    Returns:
        dict: Analysis results including total flow and per-shell balances
    """
    # Calculate total flow
    total_flow = 0.0
    for i in range(n_shells):
        for j in range(n_shells):
            if i != j:
                total_flow += temporal_flow.net_flow(i, j)
    
    # Calculate per-shell flow balance
    shell_balances = {}
    for i in range(n_shells):
        balance = temporal_flow.total_outflow(i, n_shells)
        shell_balances[f"shell_{i}"] = balance
    
    # Determine if system is in equilibrium
    is_equilibrium = temporal_flow.flow_equilibrium(n_shells)
    
    return {
        "total_flow": total_flow,
        "shell_balances": shell_balances,
        "is_equilibrium": is_equilibrium
    }


def demonstrate_gravitational_manifestation(
    temporal_flow: TemporalFlow, 
    shell_i: int, 
    shell_j: int, 
    mass_ratio: float = 1.0
) -> Dict[str, float]:
    """
    Demonstrate how inverse temporal flow manifests as gravitational attraction.
    
    Args:
        temporal_flow: TemporalFlow object
        shell_i: Index of first shell
        shell_j: Index of second shell
        mass_ratio: Ratio of masses (m_j/m_i)
        
    Returns:
        dict: Gravitational parameters including force and potential
    """
    # Calculate inverse flow
    inverse_flow_ij = temporal_flow.inverse_flow(shell_i, shell_j)
    inverse_flow_ji = temporal_flow.inverse_flow(shell_j, shell_i)
    
    # Effective gravitational force (proportional to inverse flow)
    # F = m * acceleration, and acceleration ∝ inverse_flow
    force_on_i = inverse_flow_ji * mass_ratio
    force_on_j = inverse_flow_ij
    
    # Effective gravitational potential
    r_i = temporal_flow.shell_structure.shell_radius(shell_i)
    r_j = temporal_flow.shell_structure.shell_radius(shell_j)
    distance = abs(r_j - r_i)
    
    # Potential energy ∝ -G*m1*m2/r
    potential = -temporal_flow.kappa_minus * \
               temporal_flow.shell_structure.shell_coupling(shell_i, shell_j) * \
               mass_ratio / distance
    
    return {
        "inverse_flow_ij": inverse_flow_ij,
        "inverse_flow_ji": inverse_flow_ji,
        "force_on_i": force_on_i,
        "force_on_j": force_on_j,
        "distance": distance,
        "potential": potential
    }