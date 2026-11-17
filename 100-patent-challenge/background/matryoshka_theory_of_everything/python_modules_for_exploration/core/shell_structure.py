"""
Shell Structure for Matryoshka Temporal Shell Framework

This module implements the fundamental shell structure of the Matryoshka
temporal model, including shell radii, shell couplings, and the basic
temporal metric. These components form the foundation for all subsequent
derivations in gravity, quantum field theory, and cosmology.

Key components:
- Shell radius calculation based on ordinal indices
- Shell coupling function with ordinal decay
- Temporal metric tensor construction
- Utility functions for shell structure visualization
"""

import numpy as np
import sympy as sp
from sympy import Symbol, exp, Function, Matrix, Rational, sqrt
import matplotlib.pyplot as plt
from typing import Union, Tuple, List, Dict, Optional, Callable

from matryoshka.core.ordinals import Ordinal, ordinal_distance, numerical_ordinal_distance


class ShellStructure:
    """
    Class representing the Matryoshka temporal shell structure.
    
    Implements shell radii, couplings, and the temporal metric tensor.
    This structure forms the foundation of the Matryoshka framework,
    from which both gravity and quantum fields emerge.
    """
    
    def __init__(self, 
                 r0: float = 1.0,
                 alpha: float = 0.1,
                 c0: float = 1.0,
                 beta: float = 0.5,
                 gamma: float = 2.0,
                 lambda_ord: float = 0.1):
        """
        Initialize the shell structure with given parameters.
        
        Args:
            r0: Base shell radius
            alpha: Shell radius scaling parameter
            c0: Base shell coupling strength
            beta: Coupling decay parameter
            gamma: Coupling decay exponent
            lambda_ord: Ordinal decay parameter
        """
        self.r0 = r0
        self.alpha = alpha
        self.c0 = c0
        self.beta = beta
        self.gamma = gamma
        self.lambda_ord = lambda_ord
    
    def shell_radius(self, i: Union[Ordinal, int]) -> float:
        """
        Calculate the radius of shell with ordinal index i.
        
        Args:
            i: Ordinal index of the shell
            
        Returns:
            float: Radius of the shell
        """
        if isinstance(i, int):
            return self.r0 * np.exp(self.alpha * i)
        
        # For symbolic calculation with Ordinals
        if i.is_finite():
            return self.r0 * np.exp(self.alpha * i.to_int())
        
        # For transfinite ordinals, return a symbolic expression
        return self.r0 * exp(self.alpha * i.to_symbolic())
    
    def shell_radius_symbolic(self, i, variables=None) -> sp.Expr:
        """
        Calculate the symbolic expression for shell radius.
        
        Args:
            i: Shell index (can be a SymPy symbol)
            variables: Optional dictionary of symbols to use
            
        Returns:
            sympy.Expr: Symbolic expression for shell radius
        """
        if variables is None:
            variables = {
                'r0': Symbol('r_0', positive=True),
                'alpha': Symbol('alpha', positive=True)
            }
        
        r0 = variables.get('r0', Symbol('r_0', positive=True))
        alpha = variables.get('alpha', Symbol('alpha', positive=True))
        
        return r0 * exp(alpha * i)
    
    def shell_coupling(self, i: Union[Ordinal, int], j: Union[Ordinal, int]) -> float:
        """
        Calculate the coupling strength between shells i and j.
        
        Args:
            i: Ordinal index of the first shell
            j: Ordinal index of the second shell
            
        Returns:
            float: Coupling strength between the shells
        """
        if isinstance(i, int):
            i = Ordinal.finite(i)
        if isinstance(j, int):
            j = Ordinal.finite(j)
        
        # If i = j, there's no coupling (diagonal terms are shell radii)
        if i == j:
            return 0.0
        
        # Calculate ordinal distance
        dist = ordinal_distance(i, j)
        num_dist = numerical_ordinal_distance(i, j, omega_val=1000.0)
        
        # Apply coupling decay function
        return self.c0 / (1 + self.beta * num_dist**self.gamma) * np.exp(-self.lambda_ord * num_dist)
    
    def shell_coupling_symbolic(self, i, j, variables=None) -> sp.Expr:
        """
        Calculate the symbolic expression for shell coupling.
        
        Args:
            i: Index of the first shell (can be a SymPy symbol)
            j: Index of the second shell (can be a SymPy symbol)
            variables: Optional dictionary of symbols to use
            
        Returns:
            sympy.Expr: Symbolic expression for shell coupling
        """
        if variables is None:
            variables = {
                'c0': Symbol('c_0', positive=True),
                'beta': Symbol('beta', positive=True),
                'gamma': Symbol('gamma', positive=True),
                'lambda_ord': Symbol('lambda_{ord}', positive=True)
            }
        
        c0 = variables.get('c0', Symbol('c_0', positive=True))
        beta = variables.get('beta', Symbol('beta', positive=True))
        gamma = variables.get('gamma', Symbol('gamma', positive=True))
        lambda_ord = variables.get('lambda_ord', Symbol('lambda_{ord}', positive=True))
        
        # Define ordinal distance function
        ord_dist = Function('ord')(sp.Abs(i - j))
        
        # Coupling formula
        return c0 / (1 + beta * sp.Abs(i - j)**gamma) * exp(-lambda_ord * ord_dist)
    
    def temporal_metric(self, i: Union[Ordinal, int], j: Union[Ordinal, int]) -> float:
        """
        Calculate the temporal metric tensor component T_ij.
        
        The temporal metric encodes both shell radii (diagonal terms)
        and shell couplings (off-diagonal terms).
        
        Args:
            i: Ordinal index of the first shell
            j: Ordinal index of the second shell
            
        Returns:
            float: Metric tensor component T_ij
        """
        if isinstance(i, int):
            i = Ordinal.finite(i)
        if isinstance(j, int):
            j = Ordinal.finite(j)
        
        # Diagonal term: shell radius
        if i == j:
            return self.shell_radius(i)
        
        # Off-diagonal term: shell coupling
        return self.shell_coupling(i, j)
    
    def temporal_metric_symbolic(self, i, j, variables=None) -> sp.Expr:
        """
        Calculate the symbolic expression for temporal metric component.
        
        Args:
            i: Index of the first shell (can be a SymPy symbol)
            j: Index of the second shell (can be a SymPy symbol)
            variables: Optional dictionary of symbols to use
            
        Returns:
            sympy.Expr: Symbolic expression for metric component
        """
        if variables is None:
            variables = {}
        
        # Use Kronecker delta for diagonal terms
        delta = Function('delta')(i, j)
        
        # Temporal metric formula
        r_i = self.shell_radius_symbolic(i, variables)
        c_ij = self.shell_coupling_symbolic(i, j, variables)
        
        return delta * r_i + (1 - delta) * c_ij
    
    def temporal_metric_matrix(self, n_shells: int) -> np.ndarray:
        """
        Construct the temporal metric tensor as a matrix.
        
        Args:
            n_shells: Number of shells to include
            
        Returns:
            numpy.ndarray: Matrix representation of temporal metric
        """
        matrix = np.zeros((n_shells, n_shells))
        
        for i in range(n_shells):
            for j in range(n_shells):
                matrix[i, j] = self.temporal_metric(i, j)
                
        return matrix
    
    def temporal_metric_matrix_symbolic(self, n_shells: int) -> sp.Matrix:
        """
        Construct the symbolic temporal metric tensor as a matrix.
        
        Args:
            n_shells: Number of shells to include
            
        Returns:
            sympy.Matrix: Symbolic matrix representation of temporal metric
        """
        matrix = sp.zeros(n_shells)
        
        for i in range(n_shells):
            for j in range(n_shells):
                matrix[i, j] = self.temporal_metric_symbolic(i, j)
                
        return matrix


def visualize_shell_structure(shell_structure: ShellStructure, n_shells: int = 10, plot_size: int = 10):
    """
    Visualize the shell structure as concentric circles.
    
    Args:
        shell_structure: ShellStructure object
        n_shells: Number of shells to visualize
        plot_size: Size of the plot
    """
    plt.figure(figsize=(plot_size, plot_size))
    ax = plt.subplot(111, aspect='equal')
    
    # Draw concentric circles for each shell
    for i in range(n_shells):
        radius = shell_structure.shell_radius(i)
        circle = plt.Circle((0, 0), radius, fill=False, linestyle='-', linewidth=1)
        ax.add_patch(circle)
        ax.text(0, radius, f"Shell {i}", ha='center', va='center', 
                bbox=dict(facecolor='white', alpha=0.7))
    
    # Set plot limits
    max_radius = shell_structure.shell_radius(n_shells - 1)
    ax.set_xlim(-max_radius * 1.1, max_radius * 1.1)
    ax.set_ylim(-max_radius * 1.1, max_radius * 1.1)
    
    # Add labels and title
    plt.title("Matryoshka Temporal Shell Structure")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlabel("x")
    plt.ylabel("y")
    
    return ax


def visualize_shell_couplings(shell_structure: ShellStructure, n_shells: int = 10, plot_size: int = 8):
    """
    Visualize the coupling strengths between shells as a heatmap.
    
    Args:
        shell_structure: ShellStructure object
        n_shells: Number of shells to visualize
        plot_size: Size of the plot
    """
    # Compute coupling matrix
    coupling_matrix = np.zeros((n_shells, n_shells))
    for i in range(n_shells):
        for j in range(n_shells):
            coupling_matrix[i, j] = shell_structure.shell_coupling(i, j)
    
    # Create heatmap
    plt.figure(figsize=(plot_size, plot_size))
    plt.imshow(coupling_matrix, interpolation='nearest', cmap='viridis')
    plt.colorbar(label='Coupling Strength')
    
    # Add labels and title
    plt.title("Shell Coupling Strengths")
    plt.xlabel("Shell Index j")
    plt.ylabel("Shell Index i")
    
    # Add grid
    plt.grid(False)
    
    return coupling_matrix


def derive_shell_radii_relation(shell_structure: ShellStructure, variables=None) -> sp.Eq:
    """
    Derive the symbolic relation for shell radii.
    
    Args:
        shell_structure: ShellStructure object
        variables: Optional dictionary of symbols to use
        
    Returns:
        sympy.Eq: Symbolic equation for shell radii
    """
    if variables is None:
        variables = {}
    
    i = Symbol('i')
    r_i = Symbol('r_i')
    
    expr = shell_structure.shell_radius_symbolic(i, variables)
    return sp.Eq(r_i, expr)


def derive_shell_coupling_relation(shell_structure: ShellStructure, variables=None) -> sp.Eq:
    """
    Derive the symbolic relation for shell coupling.
    
    Args:
        shell_structure: ShellStructure object
        variables: Optional dictionary of symbols to use
        
    Returns:
        sympy.Eq: Symbolic equation for shell coupling
    """
    if variables is None:
        variables = {}
    
    i = Symbol('i')
    j = Symbol('j')
    c_ij = Symbol('c_{ij}')
    
    expr = shell_structure.shell_coupling_symbolic(i, j, variables)
    return sp.Eq(c_ij, expr)


def derive_temporal_metric_relation(shell_structure: ShellStructure, variables=None) -> sp.Eq:
    """
    Derive the symbolic relation for temporal metric.
    
    Args:
        shell_structure: ShellStructure object
        variables: Optional dictionary of symbols to use
        
    Returns:
        sympy.Eq: Symbolic equation for temporal metric
    """
    if variables is None:
        variables = {}
    
    i = Symbol('i')
    j = Symbol('j')
    T_ij = Symbol('\\mathcal{T}_{ij}')
    
    expr = shell_structure.temporal_metric_symbolic(i, j, variables)
    return sp.Eq(T_ij, expr)