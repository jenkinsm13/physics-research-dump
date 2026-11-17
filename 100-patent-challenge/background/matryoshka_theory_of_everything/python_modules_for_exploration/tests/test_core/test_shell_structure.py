"""
Tests for the shell_structure module in the Matryoshka framework.

This module contains comprehensive tests for the ShellStructure class and related
functions in the shell_structure.py module, verifying correct implementation of
shell radii, couplings, and the temporal metric.
"""

import sys
import os
import pytest
import numpy as np
import sympy as sp
from sympy import Symbol, exp, Function, Eq

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from matryoshka.core.ordinals import Ordinal, OMEGA
from matryoshka.core.shell_structure import (
    ShellStructure, visualize_shell_structure, visualize_shell_couplings,
    derive_shell_radii_relation, derive_shell_coupling_relation, derive_temporal_metric_relation
)


class TestShellBasics:
    """Test basic shell structure properties."""
    
    def test_initialization(self):
        """Test creation of ShellStructure with default and custom parameters."""
        # Default parameters
        shell = ShellStructure()
        assert shell.r0 == 1.0
        assert shell.alpha == 0.1
        assert shell.c0 == 1.0
        assert shell.beta == 0.5
        assert shell.gamma == 2.0
        assert shell.lambda_ord == 0.1
        
        # Custom parameters
        custom_shell = ShellStructure(
            r0=2.0, alpha=0.2, c0=3.0, beta=0.3, gamma=1.5, lambda_ord=0.05
        )
        assert custom_shell.r0 == 2.0
        assert custom_shell.alpha == 0.2
        assert custom_shell.c0 == 3.0
        assert custom_shell.beta == 0.3
        assert custom_shell.gamma == 1.5
        assert custom_shell.lambda_ord == 0.05


class TestShellRadius:
    """Test shell radius calculations."""
    
    def test_finite_shell_radius(self):
        """Test radius calculation for finite ordinal shells."""
        shell = ShellStructure(r0=1.0, alpha=0.1)
        
        # Check specific values
        assert shell.shell_radius(0) == 1.0
        assert shell.shell_radius(1) == pytest.approx(1.1052, 0.0001)
        assert shell.shell_radius(10) == pytest.approx(2.7183, 0.0001)
        
        # Check with Ordinal objects
        assert shell.shell_radius(Ordinal.finite(5)) == pytest.approx(1.6487, 0.0001)
    
    def test_exponential_scaling(self):
        """Test that shell radii follow exponential scaling."""
        shell = ShellStructure(r0=1.0, alpha=0.1)
        
        # Check ratio between consecutive shells
        ratio = shell.shell_radius(2) / shell.shell_radius(1)
        expected_ratio = np.exp(0.1)
        assert ratio == pytest.approx(expected_ratio, 0.0001)
        
        # Check for other shell pairs
        for i in range(1, 10):
            ratio = shell.shell_radius(i+1) / shell.shell_radius(i)
            assert ratio == pytest.approx(expected_ratio, 0.0001)
    
    def test_symbolic_shell_radius(self):
        """Test symbolic expression for shell radius."""
        shell = ShellStructure()
        i = Symbol('i')
        
        # Check symbolic expression
        expr = shell.shell_radius_symbolic(i)
        expected = Symbol('r_0', positive=True) * exp(Symbol('alpha', positive=True) * i)
        assert expr == expected
        
        # Check with custom variables
        variables = {'r0': Symbol('r'), 'alpha': Symbol('a')}
        expr_custom = shell.shell_radius_symbolic(i, variables)
        expected_custom = Symbol('r') * exp(Symbol('a') * i)
        assert expr_custom == expected_custom


class TestShellCoupling:
    """Test shell coupling calculations."""
    
    def test_finite_shell_coupling(self):
        """Test coupling calculation for finite ordinal shells."""
        shell = ShellStructure(c0=1.0, beta=0.5, gamma=2.0, lambda_ord=0.1)
        
        # Diagonal terms should be zero (no self-coupling)
        assert shell.shell_coupling(3, 3) == 0.0
        
        # Check specific values
        coupling_1_2 = shell.shell_coupling(1, 2)
        coupling_1_5 = shell.shell_coupling(1, 5)
        
        # Coupling should decrease with distance
        assert coupling_1_2 > coupling_1_5
        
        # Check symmetry
        assert shell.shell_coupling(1, 5) == shell.shell_coupling(5, 1)
    
    def test_ordinal_decay(self):
        """Test that coupling follows ordinal decay."""
        shell = ShellStructure(c0=1.0, beta=0.5, gamma=2.0, lambda_ord=0.1)
        
        # Coupling to transfinite ordinals should be strongly suppressed
        finite_coupling = shell.shell_coupling(5, 10)
        transfinite_coupling = shell.shell_coupling(5, OMEGA)
        
        assert transfinite_coupling < finite_coupling
        
        # Coupling between distant shells should decrease
        couplings = [shell.shell_coupling(1, j) for j in range(2, 11)]
        assert all(couplings[i] > couplings[i+1] for i in range(len(couplings)-1))
    
    def test_symbolic_shell_coupling(self):
        """Test symbolic expression for shell coupling."""
        shell = ShellStructure()
        i, j = Symbol('i'), Symbol('j')
        
        # Check symbolic expression
        expr = shell.shell_coupling_symbolic(i, j)
        # This is a complex expression, so we check parts
        assert isinstance(expr, sp.Expr)
        assert Symbol('c_0', positive=True) in expr.free_symbols
        assert Symbol('beta', positive=True) in expr.free_symbols
        assert Symbol('lambda_{ord}', positive=True) in expr.free_symbols
        assert Function('ord')(sp.Abs(i - j)) in expr


class TestTemporalMetric:
    """Test temporal metric calculations."""
    
    def test_metric_components(self):
        """Test temporal metric components."""
        shell = ShellStructure()
        
        # Diagonal terms should equal shell radius
        for i in range(5):
            assert shell.temporal_metric(i, i) == shell.shell_radius(i)
        
        # Off-diagonal terms should equal shell coupling
        for i in range(5):
            for j in range(i+1, 5):
                assert shell.temporal_metric(i, j) == shell.shell_coupling(i, j)
                assert shell.temporal_metric(j, i) == shell.shell_coupling(j, i)
    
    def test_metric_matrix(self):
        """Test temporal metric matrix construction."""
        shell = ShellStructure()
        n_shells = 5
        
        # Construct matrix
        matrix = shell.temporal_metric_matrix(n_shells)
        
        # Check matrix shape
        assert matrix.shape == (n_shells, n_shells)
        
        # Check matrix properties
        for i in range(n_shells):
            for j in range(n_shells):
                assert matrix[i, j] == shell.temporal_metric(i, j)
    
    def test_symbolic_metric(self):
        """Test symbolic expression for temporal metric."""
        shell = ShellStructure()
        i, j = Symbol('i'), Symbol('j')
        
        # Check symbolic expression
        expr = shell.temporal_metric_symbolic(i, j)
        # Verify the expression contains delta function
        assert Function('delta')(i, j) in expr


class TestDerivations:
    """Test symbolic derivation functions."""
    
    def test_derive_shell_radii(self):
        """Test derivation of shell radius relation."""
        shell = ShellStructure()
        
        # Get symbolic equation
        eq = derive_shell_radii_relation(shell)
        
        # Check equation
        assert isinstance(eq, Eq)
        assert eq.lhs == Symbol('r_i')
        assert Symbol('r_0', positive=True) in eq.rhs.free_symbols
        assert Symbol('alpha', positive=True) in eq.rhs.free_symbols
    
    def test_derive_shell_coupling(self):
        """Test derivation of shell coupling relation."""
        shell = ShellStructure()
        
        # Get symbolic equation
        eq = derive_shell_coupling_relation(shell)
        
        # Check equation
        assert isinstance(eq, Eq)
        assert eq.lhs == Symbol('c_{ij}')
        assert Symbol('c_0', positive=True) in eq.rhs.free_symbols
        assert Symbol('beta', positive=True) in eq.rhs.free_symbols
    
    def test_derive_temporal_metric(self):
        """Test derivation of temporal metric relation."""
        shell = ShellStructure()
        
        # Get symbolic equation
        eq = derive_temporal_metric_relation(shell)
        
        # Check equation
        assert isinstance(eq, Eq)
        assert eq.lhs == Symbol('\\mathcal{T}_{ij}')
        assert Function('delta')(Symbol('i'), Symbol('j')) in eq.rhs


class TestVisualization:
    """Test visualization functions."""
    
    def test_visualize_shell_structure(self):
        """Test shell structure visualization function."""
        shell = ShellStructure()
        
        # This should run without errors and return an axis object
        ax = visualize_shell_structure(shell, n_shells=5, plot_size=6)
        
        # Basic checks on the axis
        assert ax is not None
        assert len(ax.patches) == 5  # Should have 5 circles
        
        # Close the plot
        plt = ax.figure.canvas.manager.matplotlib
        plt.close()
    
    def test_visualize_shell_couplings(self):
        """Test shell couplings visualization function."""
        shell = ShellStructure()
        
        # This should run without errors and return a coupling matrix
        matrix = visualize_shell_couplings(shell, n_shells=5, plot_size=6)
        
        # Basic checks on the matrix
        assert matrix.shape == (5, 5)
        assert np.all(np.diag(matrix) == 0)  # Diagonal should be zero
        
        # Close the plot (bit awkward with matplotlib)
        import matplotlib.pyplot as plt
        plt.close()


if __name__ == "__main__":
    pytest.main(["-v", __file__])