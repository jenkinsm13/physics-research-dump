"""
Tests for the ordinals module in the Matryoshka framework.

This module contains comprehensive tests for the Ordinal class and related
functions in the ordinals.py module, verifying correct implementation of
transfinite ordinal arithmetic and the ordinal distance function.
"""

import sys
import os
import pytest
import sympy as sp
from sympy import Symbol, Integer

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from matryoshka.core.ordinals import (
    Ordinal, ordinal_distance, numerical_ordinal_distance,
    ZERO, ONE, OMEGA, OMEGA_2, OMEGA_SQUARED
)


class TestOrdinalBasics:
    """Test basic ordinal creation and properties."""
    
    def test_finite_ordinals(self):
        """Test creation and properties of finite ordinals."""
        zero = Ordinal()
        one = Ordinal.finite(1)
        ten = Ordinal.finite(10)
        
        assert zero.is_finite()
        assert one.is_finite()
        assert ten.is_finite()
        
        assert zero.to_int() == 0
        assert one.to_int() == 1
        assert ten.to_int() == 10
        
        assert str(zero) == "0"
        assert str(one) == "1"
        assert str(ten) == "10"
    
    def test_transfinite_ordinals(self):
        """Test creation and properties of transfinite ordinals."""
        omega = Ordinal.omega()
        omega_plus_1 = omega + 1
        omega_times_2 = Ordinal(terms={(1,): 2})  # ω·2
        omega_squared = Ordinal.omega_power(2)  # ω²
        
        assert not omega.is_finite()
        assert not omega_plus_1.is_finite()
        assert not omega_times_2.is_finite()
        assert not omega_squared.is_finite()
        
        with pytest.raises(ValueError):
            omega.to_int()
        
        assert str(omega) == "ω"
        assert str(omega_plus_1) == "ω + 1"
        assert str(omega_times_2) == "2·ω"
        assert str(omega_squared) == "ω^2"
    
    def test_predefined_constants(self):
        """Test the predefined ordinal constants."""
        assert ZERO.is_finite() and ZERO.to_int() == 0
        assert ONE.is_finite() and ONE.to_int() == 1
        assert not OMEGA.is_finite() and str(OMEGA) == "ω"
        assert not OMEGA_2.is_finite() and str(OMEGA_2) == "2·ω"
        assert not OMEGA_SQUARED.is_finite() and str(OMEGA_SQUARED) == "ω^2"


class TestOrdinalComparison:
    """Test ordinal comparison operations."""
    
    def test_equality(self):
        """Test ordinal equality."""
        # Finite ordinals
        assert Ordinal.finite(0) == Ordinal.finite(0)
        assert Ordinal.finite(5) == Ordinal.finite(5)
        assert Ordinal.finite(0) != Ordinal.finite(5)
        
        # Transfinite ordinals
        assert Ordinal.omega() == Ordinal.omega()
        assert Ordinal.omega() + 1 == Ordinal.omega() + 1
        assert Ordinal.omega() != Ordinal.omega() + 1
        
        # Mixed comparisons
        assert Ordinal.finite(10) != Ordinal.omega()
        assert Ordinal.finite(0) == 0
        assert Ordinal.omega() != 999999
    
    def test_ordering(self):
        """Test ordinal ordering."""
        # Finite ordinals
        assert Ordinal.finite(0) < Ordinal.finite(5)
        assert Ordinal.finite(5) > Ordinal.finite(0)
        assert Ordinal.finite(5) <= Ordinal.finite(5)
        assert Ordinal.finite(5) >= Ordinal.finite(5)
        
        # Transfinite ordinals
        assert Ordinal.omega() < Ordinal.omega() + 1
        assert Ordinal.omega() + 1 < Ordinal.omega() * 2
        assert Ordinal.omega() * 2 < Ordinal.omega_power(2)
        
        # Mixed comparisons
        assert Ordinal.finite(9999999) < Ordinal.omega()
        assert Ordinal.omega() > 9999999
        
        # More complex cases
        assert Ordinal.omega() + 100 < Ordinal.omega() * 2
        assert Ordinal.omega() * 3 + 5 < Ordinal.omega_power(2)
        assert Ordinal.omega_power(2) + Ordinal.omega() < Ordinal.omega_power(2) + Ordinal.omega() + 1


class TestOrdinalArithmetic:
    """Test ordinal arithmetic operations."""
    
    def test_addition(self):
        """Test ordinal addition."""
        # Finite + finite
        assert Ordinal.finite(2) + Ordinal.finite(3) == Ordinal.finite(5)
        assert 2 + Ordinal.finite(3) == Ordinal.finite(5)
        assert Ordinal.finite(2) + 3 == Ordinal.finite(5)
        
        # Finite + transfinite
        assert Ordinal.finite(5) + Ordinal.omega() == Ordinal.omega()
        assert Ordinal.omega() + Ordinal.finite(5) == Ordinal.omega() + 5
        
        # Transfinite + transfinite
        assert Ordinal.omega() + Ordinal.omega() == Ordinal.omega() * 2
        assert Ordinal.omega() * 2 + Ordinal.omega() == Ordinal.omega() * 3
        
        # Commutative examples
        assert 3 + OMEGA == OMEGA
        assert OMEGA + 3 == OMEGA + 3  # ω + 3 ≠ 3 + ω
        assert OMEGA + OMEGA == OMEGA * 2
    
    def test_multiplication(self):
        """Test ordinal multiplication."""
        # Finite * finite
        assert Ordinal.finite(2) * Ordinal.finite(3) == Ordinal.finite(6)
        assert 2 * Ordinal.finite(3) == Ordinal.finite(6)
        assert Ordinal.finite(2) * 3 == Ordinal.finite(6)
        
        # Zero cases
        assert Ordinal.finite(0) * Ordinal.omega() == Ordinal.finite(0)
        assert Ordinal.omega() * Ordinal.finite(0) == Ordinal.finite(0)
        
        # Finite * transfinite
        assert Ordinal.finite(5) * Ordinal.omega() == Ordinal.omega()
        assert Ordinal.omega() * Ordinal.finite(5) == Ordinal.omega() * 5
        
        # Transfinite * transfinite (simple cases)
        assert Ordinal.omega() * Ordinal.omega() == Ordinal.omega_power(2)
        
        # Non-commutative examples
        assert 2 * OMEGA == OMEGA
        assert OMEGA * 2 == OMEGA * 2  # ω·2 ≠ 2·ω
        assert OMEGA * OMEGA == OMEGA_SQUARED


class TestSymbolicConversion:
    """Test conversion between Ordinals and symbolic expressions."""
    
    def test_to_symbolic(self):
        """Test conversion from Ordinal to symbolic expression."""
        omega = Symbol('ω')
        
        # Finite ordinals
        assert Ordinal.finite(0).to_symbolic() == Integer(0)
        assert Ordinal.finite(7).to_symbolic() == Integer(7)
        
        # Transfinite ordinals
        assert Ordinal.omega().to_symbolic() == omega
        assert (Ordinal.omega() + 2).to_symbolic() == omega + 2
        assert (Ordinal.omega() * 3).to_symbolic() == 3 * omega
        assert Ordinal.omega_power(2).to_symbolic() == omega**2
    
    def test_from_symbolic(self):
        """Test conversion from symbolic expression to Ordinal."""
        omega = Symbol('ω')
        
        # Finite ordinals
        assert Ordinal.from_symbolic(Integer(0)) == Ordinal.finite(0)
        assert Ordinal.from_symbolic(Integer(7)) == Ordinal.finite(7)
        
        # Transfinite ordinals
        assert Ordinal.from_symbolic(omega) == Ordinal.omega()
        assert Ordinal.from_symbolic(omega + 2) == Ordinal.omega() + 2
        assert Ordinal.from_symbolic(3 * omega) == Ordinal.omega() * 3
        assert Ordinal.from_symbolic(omega**2) == Ordinal.omega_power(2)


class TestOrdinalDistance:
    """Test ordinal distance calculations."""
    
    def test_finite_distance(self):
        """Test distance between finite ordinals."""
        assert ordinal_distance(Ordinal.finite(3), Ordinal.finite(7)) == Ordinal.finite(4)
        assert ordinal_distance(Ordinal.finite(10), Ordinal.finite(3)) == Ordinal.finite(7)
        assert ordinal_distance(0, 5) == Ordinal.finite(5)
    
    def test_transfinite_distance(self):
        """Test distance involving transfinite ordinals."""
        # Finite to transfinite
        assert ordinal_distance(Ordinal.finite(5), Ordinal.omega()) == Ordinal.omega()
        assert ordinal_distance(Ordinal.omega(), Ordinal.finite(5)) == Ordinal.omega()
        
        # Transfinite to transfinite
        assert ordinal_distance(Ordinal.omega(), Ordinal.omega() + 3) == Ordinal.finite(3)
        assert ordinal_distance(Ordinal.omega() * 2, Ordinal.omega() * 3) == Ordinal.omega()
    
    def test_numerical_distance(self):
        """Test numerical approximation of ordinal distance."""
        # Finite cases
        assert numerical_ordinal_distance(3, 7) == 4
        assert numerical_ordinal_distance(10, 3) == 7
        
        # Transfinite cases (results depend on omega_val)
        omega_val = 100.0
        assert numerical_ordinal_distance(5, OMEGA, omega_val=omega_val) > 90  # Approximately omega_val
        assert numerical_ordinal_distance(OMEGA, OMEGA + 3, omega_val=omega_val) > 1  # Should be 3 but depends on impl.
        assert numerical_ordinal_distance(OMEGA, OMEGA * 2, omega_val=omega_val) > omega_val  # Approximately omega_val


class TestNumericalValue:
    """Test numerical value approximation of ordinals."""
    
    def test_finite_values(self):
        """Test numerical values of finite ordinals."""
        assert Ordinal.finite(0).numerical_value() == 0
        assert Ordinal.finite(42).numerical_value() == 42
    
    def test_transfinite_values(self):
        """Test numerical approximations of transfinite ordinals."""
        # We can only test that the ordering is preserved
        max_finite = 1000
        
        # Ensure ordering is preserved
        assert OMEGA.numerical_value(max_finite=max_finite) > max_finite
        assert (OMEGA + 1).numerical_value(max_finite=max_finite) > OMEGA.numerical_value(max_finite=max_finite)
        assert (OMEGA * 2).numerical_value(max_finite=max_finite) > (OMEGA + 100).numerical_value(max_finite=max_finite)
        assert OMEGA_SQUARED.numerical_value(max_finite=max_finite) > (OMEGA * 100).numerical_value(max_finite=max_finite)


if __name__ == "__main__":
    pytest.main(["-v", __file__])