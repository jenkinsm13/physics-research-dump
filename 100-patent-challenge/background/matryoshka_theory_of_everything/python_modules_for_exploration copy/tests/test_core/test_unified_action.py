"""
Tests for the unified_action module in the Matryoshka framework.

This module contains comprehensive tests for the UnifiedAction class and related 
components in the unified_action.py module, verifying correct implementation of
the action principle, variational calculations, and field equation derivation.
"""

import sys
import os
import pytest
import numpy as np
import sympy as sp
from sympy import Symbol, Function, Eq, Integral, oo, pi

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from matryoshka.core.ordinals import Ordinal
from matryoshka.core.shell_structure import ShellStructure
from matryoshka.core.temporal_flow import TemporalFlow
from matryoshka.core.unified_action import (
    MeasureTheory, RicciCurvature, UnifiedAction,
    derive_einstein_equations, derive_shell_field_equations,
    visualize_action_variation
)


class TestMeasureTheory:
    """Test measure theory components."""
    
    def test_initialization(self):
        """Test initialization of MeasureTheory."""
        shell = ShellStructure()
        measure = MeasureTheory(shell)
        
        assert measure.shell_structure == shell
        assert measure.omega_val == 1000.0
        
        # Custom omega_val
        measure_custom = MeasureTheory(shell, omega_val=500.0)
        assert measure_custom.omega_val == 500.0
    
    def test_spacetime_measure(self):
        """Test spacetime measure function."""
        shell = ShellStructure()
        measure = MeasureTheory(shell)
        
        # Spacetime measure should be the identity
        assert measure.spacetime_measure(5.0) == 5.0
        assert measure.spacetime_measure(0.0) == 0.0
        assert measure.spacetime_measure(-3.0) == -3.0
    
    def test_shell_measure(self):
        """Test shell measure function."""
        shell = ShellStructure()
        measure = MeasureTheory(shell)
        
        # Finite ordinals should have measure 1
        assert measure.shell_measure(0) == 1.0
        assert measure.shell_measure(10) == 1.0
        assert measure.shell_measure(Ordinal.finite(100)) == 1.0
        
        # Transfinite ordinals should have different measures
        # Exact values depend on implementation details
        measure_transfinite = measure.shell_measure(Ordinal.omega())
        assert isinstance(measure_transfinite, float)
    
    def test_product_measure(self):
        """Test product measure function."""
        shell = ShellStructure()
        measure = MeasureTheory(shell)
        
        # Product measure should be product of individual measures
        d4x = 2.0
        i = 5
        
        assert measure.product_measure(d4x, i) == d4x * measure.shell_measure(i)
        assert measure.product_measure(0.0, i) == 0.0
    
    def test_symbolic_shell_measure(self):
        """Test symbolic shell measure function."""
        shell = ShellStructure()
        measure = MeasureTheory(shell)
        
        i = Symbol('i')
        expr = measure.symbolic_shell_measure(i)
        
        assert isinstance(expr, sp.Expr)
        # Should be a piecewise function
        assert isinstance(expr, sp.Piecewise)
    
    def test_integral_approximation(self):
        """Test integral approximation method."""
        shell = ShellStructure()
        measure = MeasureTheory(shell)
        
        # Define a simple test function
        def f(x, i):
            return x * i
        
        # Integrate over x in [0, 1] and i in [1, 3]
        result = measure.integral_approximation(f, (0, 1), (1, 3), n_points=10)
        
        # This is a basic check that the function runs
        assert isinstance(result, float)
        
        # For a constant function, we can check the result more precisely
        def g(x, i):
            return 1.0
        
        result_const = measure.integral_approximation(g, (0, 1), (1, 3), n_points=10)
        
        # Expected result: integral of 1 over x in [0, 1] for each i in [1, 3]
        # Since shell measure is 1 for finite ordinals, this should be approximately 3
        assert result_const == pytest.approx(3.0, 0.1)


class TestRicciCurvature:
    """Test Ricci curvature calculations."""
    
    def test_initialization(self):
        """Test initialization of RicciCurvature."""
        shell = ShellStructure()
        ricci = RicciCurvature(shell)
        
        assert ricci.shell_structure == shell
    
    def test_christoffel_symbols(self):
        """Test Christoffel symbols calculation."""
        shell = ShellStructure()
        ricci = RicciCurvature(shell)
        
        # Get Christoffel symbols
        symbols = ricci.christoffel_symbols(1, 2, 3)
        
        # Basic check that the result is a dictionary with expected keys
        assert isinstance(symbols, dict)
        assert "Gamma^i_jk" in symbols
        assert "Gamma^j_ik" in symbols
        assert "Gamma^k_ij" in symbols
    
    def test_riemann_tensor(self):
        """Test Riemann tensor calculation."""
        shell = ShellStructure()
        ricci = RicciCurvature(shell)
        
        # Get Riemann tensor component
        r = ricci.riemann_tensor(1, 2, 3, 4)
        
        # Basic check that the result is a float
        assert isinstance(r, float)
    
    def test_ricci_tensor(self):
        """Test Ricci tensor calculation."""
        shell = ShellStructure()
        ricci = RicciCurvature(shell)
        
        # Get Ricci tensor components
        r_11 = ricci.ricci_tensor(1, 1)  # Diagonal
        r_12 = ricci.ricci_tensor(1, 2)  # Off-diagonal
        
        # Check that the results are floats
        assert isinstance(r_11, float)
        assert isinstance(r_12, float)
        
        # Diagonal and off-diagonal components should typically be different
        assert r_11 != r_12
    
    def test_ricci_scalar(self):
        """Test Ricci scalar calculation."""
        shell = ShellStructure()
        ricci = RicciCurvature(shell)
        
        # Get Ricci scalar
        r = ricci.ricci_scalar(5)  # Use 5 shells
        
        # Check that the result is a float
        assert isinstance(r, float)
    
    def test_symbolic_ricci_scalar(self):
        """Test symbolic Ricci scalar expression."""
        shell = ShellStructure()
        ricci = RicciCurvature(shell)
        
        # Get symbolic expression
        expr = ricci.symbolic_ricci_scalar()
        
        # Check that the result is a sympy expression
        assert isinstance(expr, sp.Expr)
        assert Symbol('R_\\mathcal{T}') in expr.free_symbols


class TestUnifiedAction:
    """Test unified action calculations."""
    
    @pytest.fixture
    def action_setup(self):
        """Fixture to set up common objects for tests."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        measure = MeasureTheory(shell)
        ricci = RicciCurvature(shell)
        action = UnifiedAction(shell, flow, measure, ricci)
        
        return {
            'shell': shell,
            'flow': flow,
            'measure': measure,
            'ricci': ricci,
            'action': action
        }
    
    def test_initialization(self, action_setup):
        """Test initialization of UnifiedAction."""
        action = action_setup['action']
        shell = action_setup['shell']
        flow = action_setup['flow']
        measure = action_setup['measure']
        ricci = action_setup['ricci']
        
        assert action.shell_structure == shell
        assert action.temporal_flow == flow
        assert action.measure_theory == measure
        assert action.ricci_curvature == ricci
    
    def test_gravitational_lagrangian(self, action_setup):
        """Test gravitational Lagrangian calculation."""
        action = action_setup['action']
        
        # Calculate for a few shells
        l_1 = action.gravitational_lagrangian(1)
        l_2 = action.gravitational_lagrangian(2)
        
        # Basic checks
        assert isinstance(l_1, float)
        assert isinstance(l_2, float)
        
        # Lagrangian should vary with shell index due to radius differences
        assert l_1 != l_2
    
    def test_matter_lagrangian(self, action_setup):
        """Test matter Lagrangian calculation."""
        action = action_setup['action']
        
        # Define some fields
        fields = {
            "scalar_field": 1.0,
            "scalar_field_derivative": 0.5
        }
        
        # Calculate for a shell
        l = action.matter_lagrangian(1, fields)
        
        # Basic check
        assert isinstance(l, float)
        
        # Check field dependency
        fields2 = {
            "scalar_field": 2.0,
            "scalar_field_derivative": 0.5
        }
        l2 = action.matter_lagrangian(1, fields2)
        
        assert l != l2
    
    def test_gauge_lagrangian(self, action_setup):
        """Test gauge Lagrangian calculation."""
        action = action_setup['action']
        
        # Define some fields
        fields = {
            "field_strength": np.eye(4) * 0.1
        }
        
        # Calculate for a shell
        l = action.gauge_lagrangian(1, fields)
        
        # Basic check
        assert isinstance(l, float)
        
        # Check field dependency
        fields2 = {
            "field_strength": np.eye(4) * 0.2
        }
        l2 = action.gauge_lagrangian(1, fields2)
        
        assert l != l2
    
    def test_total_lagrangian(self, action_setup):
        """Test total Lagrangian calculation."""
        action = action_setup['action']
        
        # Define some fields
        fields = {
            "scalar_field": 1.0,
            "scalar_field_derivative": 0.5,
            "field_strength": np.eye(4) * 0.1
        }
        
        # Calculate for a shell
        l = action.total_lagrangian(1, fields)
        
        # Basic check
        assert isinstance(l, float)
        
        # Should be sum of individual Lagrangians
        l_grav = action.gravitational_lagrangian(1)
        l_matter = action.matter_lagrangian(1, fields)
        l_gauge = action.gauge_lagrangian(1, fields)
        
        assert l == pytest.approx(l_grav + l_matter + l_gauge)
    
    def test_action_density(self, action_setup):
        """Test action density calculation."""
        action = action_setup['action']
        
        # Define some fields
        fields = {
            "scalar_field": 1.0,
            "scalar_field_derivative": 0.5,
            "field_strength": np.eye(4) * 0.1
        }
        
        # Calculate for a shell
        density = action.action_density(1, fields)
        
        # Basic check
        assert isinstance(density, float)
    
    def test_total_action(self, action_setup):
        """Test total action calculation."""
        action = action_setup['action']
        
        # Define some fields
        fields = {
            "scalar_field": 1.0,
            "scalar_field_derivative": 0.5,
            "field_strength": np.eye(4) * 0.1
        }
        
        # Calculate total action
        total = action.total_action((0, 1), (1, 3), fields, n_points=5)
        
        # Basic check
        assert isinstance(total, float)
    
    def test_symbolic_action(self, action_setup):
        """Test symbolic action expression."""
        action = action_setup['action']
        
        # Get symbolic expression
        expr = action.symbolic_action()
        
        # Check that it's an equation
        assert isinstance(expr, Eq)
        assert expr.lhs == Symbol('S')
        assert isinstance(expr.rhs, Integral)
    
    def test_variation(self, action_setup):
        """Test variation calculation."""
        action = action_setup['action']
        
        # Define a test functional and fields
        def functional(fields):
            return fields["x"]**2
        
        fields = {"x": 2.0}
        
        # Calculate variation
        var = action.variation(functional, "x", fields, epsilon=1e-5)
        
        # For f(x) = x^2, df/dx = 2x
        assert var == pytest.approx(4.0, 0.01)
    
    def test_field_equation(self, action_setup):
        """Test field equation calculation."""
        action = action_setup['action']
        
        # Define some fields
        fields = {
            "scalar_field": 1.0,
            "scalar_field_derivative": 0.5,
            "field_strength": np.eye(4) * 0.1
        }
        
        # Calculate field equation
        # This is mostly a check that the function runs without errors
        eq = action.field_equation("scalar_field", fields, (0, 1), (1, 2))
        
        # Basic check
        assert isinstance(eq, float)
    
    def test_energy_momentum_tensor(self, action_setup):
        """Test energy-momentum tensor calculation."""
        action = action_setup['action']
        
        # Define some fields
        fields = {
            "energy_density": 0.2
        }
        
        # Calculate for a few components
        t_11 = action.energy_momentum_tensor(1, 1, fields)  # Diagonal
        t_12 = action.energy_momentum_tensor(1, 2, fields)  # Off-diagonal
        
        # Basic checks
        assert isinstance(t_11, float)
        assert isinstance(t_12, float)
        
        # For a perfect fluid, diagonal should be energy density or pressure
        # while off-diagonal should be zero
        assert t_11 == fields["energy_density"]
        assert t_12 == 0.0


class TestDerivationFunctions:
    """Test equation derivation functions."""
    
    @pytest.fixture
    def action_setup(self):
        """Fixture to set up common objects for tests."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        measure = MeasureTheory(shell)
        ricci = RicciCurvature(shell)
        action = UnifiedAction(shell, flow, measure, ricci)
        
        return {
            'shell': shell,
            'flow': flow,
            'measure': measure,
            'ricci': ricci,
            'action': action
        }
    
    def test_derive_einstein_equations(self, action_setup):
        """Test derivation of Einstein equations."""
        action = action_setup['action']
        
        # Get symbolic equation
        eq = derive_einstein_equations(action)
        
        # Check that it's an equation
        assert isinstance(eq, Eq)
        
        # Check the structure of the equation
        lhs = eq.lhs
        rhs = eq.rhs
        
        assert lhs == Symbol('G_{\\mu\\nu}')
        assert Symbol('T_{\\mu\\nu}') in rhs.free_symbols
        assert Symbol('G') in rhs.free_symbols
        assert Symbol('c') in rhs.free_symbols
        assert pi in rhs.free_symbols
    
    def test_derive_shell_field_equations(self, action_setup):
        """Test derivation of shell field equations."""
        action = action_setup['action']
        
        # Get symbolic equation
        eq = derive_shell_field_equations(action)
        
        # Check that it's an equation
        assert isinstance(eq, Eq)
        
        # Check the structure of the equation
        lhs = eq.lhs
        rhs = eq.rhs
        
        assert Function('\\square_\\mathcal{T}')(Function('\\phi')(Symbol('i'))) == lhs
        assert Symbol('\\frac{\\partial V}{\\partial \\phi_i}') == rhs


class TestVisualization:
    """Test visualization functions."""
    
    @pytest.fixture
    def action_setup(self):
        """Fixture to set up common objects for tests."""
        shell = ShellStructure()
        flow = TemporalFlow(shell)
        measure = MeasureTheory(shell)
        ricci = RicciCurvature(shell)
        action = UnifiedAction(shell, flow, measure, ricci)
        
        return {
            'shell': shell,
            'flow': flow,
            'measure': measure,
            'ricci': ricci,
            'action': action
        }
    
    def test_visualize_action_variation(self, action_setup):
        """Test action variation visualization function."""
        action = action_setup['action']
        
        # Define some fields
        fields = {
            "scalar_field": 1.0,
            "scalar_field_derivative": 0.5,
            "field_strength": np.eye(4) * 0.1
        }
        
        # Run visualization function
        # This is mainly to check that it runs without errors
        field_values, action_values = visualize_action_variation(
            action, "scalar_field", (0.5, 1.5), fields, (0, 1), (1, 2), n_points=5
        )
        
        # Basic checks on the results
        assert len(field_values) == 5
        assert len(action_values) == 5
        assert field_values[0] == pytest.approx(0.5)
        assert field_values[-1] == pytest.approx(1.5)
        
        # Close the plot to avoid contaminating other tests
        import matplotlib.pyplot as plt
        plt.close()


if __name__ == "__main__":
    pytest.main(["-v", __file__])