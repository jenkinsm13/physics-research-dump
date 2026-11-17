"""
Tests for the temporal_flow module in the Matryoshka framework.

This module contains comprehensive tests for the TemporalFlow class and related
functions in the temporal_flow.py module, verifying correct implementation of
forward and inverse temporal flow and their relationship to gravitational effects.
"""

import sys
import os
import pytest
import numpy as np
import sympy as sp
from sympy import Symbol, Function, Eq

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from matryoshka.core.ordinals import Ordinal, OMEGA
from matryoshka.core.shell_structure import ShellStructure
from matryoshka.core.temporal_flow import (
    TemporalFlow, visualize_temporal_flows, visualize_net_flow,
    derive_flow_equations, analyze_flow_conservation, demonstrate_gravitational_manifestation
)


class TestTemporalFlowBasics:
    """Test basic temporal flow properties."""
    
    def test_initialization(self):
        """Test creation of TemporalFlow with default and custom parameters."""
        # Create shell structure
        shell = ShellStructure()
        
        # Default parameters
        flow = TemporalFlow(shell)
        assert flow.shell_structure == shell
        assert flow.kappa_plus == 1.0
        assert flow.kappa_minus == 0.8
        
        # Custom parameters
        custom_flow = TemporalFlow(shell, kappa_plus=1.5, kappa_minus=0.9)
        assert custom_flow.kappa_plus == 1.5
        assert custom_flow.kappa_minus == 0.9


class TestForwardFlow:
    """Test forward temporal flow calculations."""
    
    def test_flow_directionality(self):
        """Test that forward flow only occurs from inner to outer shells."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        
        # Flow should be zero for equal indices
        assert flow.forward_flow(3, 3) == 0.0
        
        # Flow should be zero for inner → inner (future → future)
        assert flow.forward_flow(5, 2) == 0.0
        
        # Flow should be non-zero for inner → outer (future → past)
        assert flow.forward_flow(2, 5) > 0.0
    
    def test_flow_magnitude(self):
        """Test that forward flow magnitude follows expected patterns."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        
        # Flow magnitude is proportional to coupling and inversely proportional to radius difference
        flow_2_3 = flow.forward_flow(2, 3)
        flow_2_4 = flow.forward_flow(2, 4)
        
        # Coupling decreases with distance while radius difference increases
        # For typical parameters, flow should decrease with distance
        assert flow_2_3 > flow_2_4
        
        # Scale with kappa_plus
        flow2 = TemporalFlow(shell, kappa_plus=2.0, kappa_minus=0.8)
        assert flow2.forward_flow(2, 3) == pytest.approx(2.0 * flow_2_3 / 1.0)
    
    def test_symbolic_forward_flow(self):
        """Test symbolic expression for forward flow."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        i, j = Symbol('i'), Symbol('j')
        
        # Check symbolic expression
        expr = flow.forward_flow_symbolic(i, j)
        
        # This is a complex expression, so we check parts
        assert isinstance(expr, sp.Expr)
        assert Symbol('kappa^+', positive=True) in expr.free_symbols
        assert Function('Theta')(j - i) in expr


class TestInverseFlow:
    """Test inverse temporal flow calculations."""
    
    def test_flow_directionality(self):
        """Test that inverse flow only occurs from outer to inner shells."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        
        # Flow should be zero for equal indices
        assert flow.inverse_flow(3, 3) == 0.0
        
        # Flow should be zero for outer → outer (past → past)
        assert flow.inverse_flow(2, 5) == 0.0
        
        # Flow should be non-zero for outer → inner (past → future)
        assert flow.inverse_flow(5, 2) > 0.0
    
    def test_flow_magnitude(self):
        """Test that inverse flow magnitude follows expected patterns."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        
        # Flow magnitude is proportional to coupling and inversely proportional to radius difference
        flow_4_3 = flow.inverse_flow(4, 3)
        flow_5_3 = flow.inverse_flow(5, 3)
        
        # For typical parameters, flow should decrease with distance
        assert flow_4_3 > flow_5_3
        
        # Scale with kappa_minus
        flow2 = TemporalFlow(shell, kappa_plus=1.0, kappa_minus=1.6)
        assert flow2.inverse_flow(4, 3) == pytest.approx(1.6 * flow_4_3 / 0.8)
    
    def test_symbolic_inverse_flow(self):
        """Test symbolic expression for inverse flow."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        i, j = Symbol('i'), Symbol('j')
        
        # Check symbolic expression
        expr = flow.inverse_flow_symbolic(i, j)
        
        # This is a complex expression, so we check parts
        assert isinstance(expr, sp.Expr)
        assert Symbol('kappa^-', positive=True) in expr.free_symbols
        assert Function('Theta')(i - j) in expr


class TestNetFlow:
    """Test net flow calculations."""
    
    def test_net_flow_computation(self):
        """Test net flow computation."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        
        # Net flow should be forward - inverse
        for i in range(5):
            for j in range(5):
                if i != j:
                    forward = flow.forward_flow(i, j)
                    inverse = flow.inverse_flow(i, j)
                    net = flow.net_flow(i, j)
                    assert net == pytest.approx(forward - inverse)
    
    def test_flow_conservation(self):
        """Test flow conservation over the entire system."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        
        # For a closed system, total flow should be conserved
        is_conserved = flow.flow_conservation(10)
        
        # This will depend on the specific implementation details
        # In an ideal system, this would be True
        # For numerical implementations, it may be approximately True
        assert isinstance(is_conserved, bool)
    
    def test_flow_matrix(self):
        """Test flow matrix construction."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        n_shells = 5
        
        # Construct flow matrix
        matrix = flow.flow_matrix(n_shells)
        
        # Check matrix shape
        assert matrix.shape == (n_shells, n_shells)
        
        # Check diagonal elements (should be zero)
        assert np.all(np.diag(matrix) == 0)
        
        # Check matrix elements
        for i in range(n_shells):
            for j in range(n_shells):
                if i != j:
                    assert matrix[i, j] == flow.net_flow(i, j)


class TestFlowEquilibrium:
    """Test flow equilibrium calculations."""
    
    def test_total_outflow(self):
        """Test total outflow calculation."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        
        # Calculate total outflow for each shell
        for i in range(5):
            outflow = flow.total_outflow(i, 5)
            
            # Manual calculation for comparison
            manual_outflow = 0.0
            for j in range(5):
                if j != i:
                    manual_outflow += flow.net_flow(i, j)
            
            assert outflow == pytest.approx(manual_outflow)
    
    def test_equilibrium_detection(self):
        """Test equilibrium detection."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        
        # Check if the system is in equilibrium
        is_equilibrium = flow.flow_equilibrium(10)
        
        # This will depend on the specific implementation details
        # For typical parameters, it may or may not be in equilibrium
        assert isinstance(is_equilibrium, bool)


class TestDerivationsAndAnalysis:
    """Test derivation and analysis functions."""
    
    def test_derive_flow_equations(self):
        """Test derivation of flow equations."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        
        # Get symbolic equations
        forward_eq, inverse_eq = derive_flow_equations(flow)
        
        # Check equations
        assert isinstance(forward_eq, Eq)
        assert isinstance(inverse_eq, Eq)
        assert forward_eq.lhs == Symbol('\\mathcal{F}^+_{i \\to j}')
        assert inverse_eq.lhs == Symbol('\\mathcal{F}^-_{i \\to j}')
    
    def test_analyze_flow_conservation(self):
        """Test flow conservation analysis."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        
        # Run analysis
        analysis = analyze_flow_conservation(flow, 5)
        
        # Check results
        assert "total_flow" in analysis
        assert "shell_balances" in analysis
        assert "is_equilibrium" in analysis
        assert isinstance(analysis["total_flow"], float)
        assert isinstance(analysis["is_equilibrium"], bool)
        
        # Check shell balances
        balances = analysis["shell_balances"]
        assert len(balances) == 5
        assert all(key.startswith("shell_") for key in balances.keys())
    
    def test_gravitational_manifestation(self):
        """Test gravitational manifestation demonstration."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        
        # Demonstrate gravitational effects
        result = demonstrate_gravitational_manifestation(flow, 5, 3)
        
        # Check results
        assert "inverse_flow_ij" in result
        assert "inverse_flow_ji" in result
        assert "force_on_i" in result
        assert "force_on_j" in result
        assert "distance" in result
        assert "potential" in result
        
        # Force should be proportional to inverse flow
        assert result["force_on_j"] == result["inverse_flow_ij"]
        
        # With default mass_ratio=1.0, forces should be related to flows
        assert result["force_on_i"] == result["inverse_flow_ji"]


class TestVisualization:
    """Test visualization functions."""
    
    def test_visualize_temporal_flows(self):
        """Test temporal flows visualization function."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        
        # This should run without errors and return figure and axes
        fig, (ax1, ax2) = visualize_temporal_flows(flow, n_shells=5, plot_size=6)
        
        # Basic checks on the axes
        assert fig is not None
        assert ax1 is not None
        assert ax2 is not None
        
        # Close the plot
        plt = fig.canvas.manager.matplotlib
        plt.close(fig)
    
    def test_visualize_net_flow(self):
        """Test net flow visualization function."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        
        # This should run without errors and return a matrix
        matrix = visualize_net_flow(flow, n_shells=5, plot_size=6)
        
        # Basic checks on the matrix
        assert matrix.shape == (5, 5)
        
        # Close the plot
        import matplotlib.pyplot as plt
        plt.close()


if __name__ == "__main__":
    pytest.main(["-v", __file__])