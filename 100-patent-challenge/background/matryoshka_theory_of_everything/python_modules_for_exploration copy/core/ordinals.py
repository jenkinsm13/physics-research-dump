"""
Ordinal Arithmetic for Matryoshka Temporal Shell Framework

This module implements transfinite ordinal representation and arithmetic
for the Matryoshka temporal shell framework. It provides the mathematical
foundation for working with both finite and transfinite ordinals, which
is essential for the shell structure and all subsequent derivations.

Key components:
- Ordinal class implementing transfinite ordinal arithmetic
- Ordinal distance function for computing distances in ordinal space
- Conversion functions between ordinals and numerical approximations
"""

import sympy as sp
import numpy as np
from sympy import Symbol, Integer, oo, exp, log
from typing import Union, Tuple, List, Dict, Optional


class Ordinal:
    """
    Class representing transfinite ordinals for the Matryoshka framework.
    
    Implements ordinal arithmetic with proper handling of both finite and
    transfinite cases. Represents ordinals in Cantor normal form:
    ω^α₁·β₁ + ω^α₂·β₂ + ... + ω^αₙ·βₙ
    where α₁ > α₂ > ... > αₙ and all βᵢ are positive integers.
    """
    
    def __init__(self, 
                 terms: Optional[Dict[Tuple[int, ...], int]] = None, 
                 finite_value: Optional[int] = None):
        """
        Initialize an ordinal number.
        
        Args:
            terms: Dictionary mapping exponent tuples to coefficients
                  Each exponent tuple represents powers of ω in descending order
            finite_value: For simple finite ordinals, just the integer value
        """
        # Special case for finite ordinals
        if finite_value is not None:
            if finite_value < 0:
                raise ValueError("Ordinals cannot be negative")
            self.terms = {(0,): finite_value} if finite_value > 0 else {}
            return
            
        # General case using Cantor normal form
        self.terms = terms or {}
        # Remove zero coefficients
        self.terms = {k: v for k, v in self.terms.items() if v > 0}
        # Sort keys in descending order
        self.terms = dict(sorted(self.terms.items(), key=lambda x: x[0], reverse=True))
    
    @classmethod
    def finite(cls, n: int) -> 'Ordinal':
        """Create a finite ordinal."""
        return cls(finite_value=n)
    
    @classmethod
    def omega(cls) -> 'Ordinal':
        """Create the first transfinite ordinal ω."""
        return cls(terms={(1,): 1})
    
    @classmethod
    def omega_power(cls, n: int) -> 'Ordinal':
        """Create ω^n."""
        if n < 0:
            raise ValueError("Ordinal powers cannot be negative")
        if n == 0:
            return cls.finite(1)
        return cls(terms={(n,): 1})
    
    @classmethod
    def from_symbolic(cls, expr) -> 'Ordinal':
        """
        Convert a symbolic expression to an Ordinal.
        Handles expressions of form ω^a + b or ω·a + b.
        
        Args:
            expr: SymPy expression representing an ordinal
            
        Returns:
            Ordinal: Corresponding ordinal number
        """
        if isinstance(expr, Integer):
            return cls.finite(int(expr))
        
        # Convert SymPy expression to ordinal
        terms = {}
        if expr.is_Add:
            for term in expr.args:
                if term.is_Integer:
                    # Constant term
                    terms[(0,)] = terms.get((0,), 0) + int(term)
                elif term.is_Mul:
                    # Term involving ω
                    coeff = 1
                    power = 1
                    for factor in term.args:
                        if factor.is_Integer:
                            coeff = int(factor)
                        elif factor.is_Pow and factor.args[0] == Symbol('ω'):
                            power = int(factor.args[1])
                    terms[(power,)] = terms.get((power,), 0) + coeff
                elif term == Symbol('ω'):
                    # Just ω
                    terms[(1,)] = terms.get((1,), 0) + 1
                elif term.is_Pow and term.args[0] == Symbol('ω'):
                    # ω^n
                    power = int(term.args[1])
                    terms[(power,)] = terms.get((power,), 0) + 1
        elif expr == Symbol('ω'):
            # Just ω
            terms[(1,)] = 1
        elif expr.is_Mul and Symbol('ω') in expr.args:
            # ω·n
            args = list(expr.args)
            args.remove(Symbol('ω'))
            coeff = 1
            for arg in args:
                if arg.is_Integer:
                    coeff *= int(arg)
            terms[(1,)] = coeff
        elif expr.is_Pow and expr.args[0] == Symbol('ω'):
            # ω^n
            power = int(expr.args[1])
            terms[(power,)] = 1
        
        return cls(terms=terms)
    
    def to_symbolic(self) -> sp.Expr:
        """
        Convert the ordinal to a symbolic expression.
        
        Returns:
            sympy.Expr: Symbolic representation of the ordinal
        """
        if not self.terms:
            return Integer(0)
        
        omega = Symbol('ω')
        result = Integer(0)
        
        for exponents, coeff in self.terms.items():
            term = Integer(coeff)
            if exponents != (0,):  # Not a finite term
                for exp in exponents:
                    if exp > 0:
                        term *= omega**exp
            result += term
            
        return result
    
    def is_finite(self) -> bool:
        """Check if this ordinal is finite."""
        return all(exponents == (0,) for exponents in self.terms.keys())
    
    def to_int(self) -> int:
        """
        Convert to integer if finite, raise ValueError otherwise.
        
        Returns:
            int: Integer value
            
        Raises:
            ValueError: If ordinal is not finite
        """
        if not self.is_finite():
            raise ValueError("Cannot convert transfinite ordinal to integer")
        return self.terms.get((0,), 0)
    
    def __add__(self, other: 'Ordinal') -> 'Ordinal':
        """
        Ordinal addition. For ordinals α and β:
        - If both are finite: α + β = standard addition
        - If either is transfinite: The larger dominates
        """
        if not isinstance(other, Ordinal):
            if isinstance(other, int):
                other = Ordinal.finite(other)
            else:
                return NotImplemented
        
        # If either is zero, return the other
        if not self.terms:
            return other
        if not other.terms:
            return self
            
        # If both are finite, do regular addition
        if self.is_finite() and other.is_finite():
            return Ordinal.finite(self.to_int() + other.to_int())
            
        # If one is finite and the other is transfinite,
        # the transfinite one dominates
        if self.is_finite():
            return other
        if other.is_finite():
            result = self.terms.copy()
            result[(0,)] = result.get((0,), 0) + other.terms.get((0,), 0)
            return Ordinal(terms=result)
            
        # Both are transfinite, compare the largest exponent
        self_max = list(self.terms.keys())[0]
        other_max = list(other.terms.keys())[0]
        
        if self_max > other_max:
            # Self dominates
            return self
        elif other_max > self_max:
            # Other dominates
            return other
        else:
            # Same largest exponent, add coefficients
            result = {}
            # Copy all terms from both
            for k, v in self.terms.items():
                result[k] = v
            for k, v in other.terms.items():
                if k in result:
                    result[k] += v
                else:
                    result[k] = v
            return Ordinal(terms=result)
    
    def __radd__(self, other):
        """Handle addition when ordinal is on the right."""
        if isinstance(other, int):
            return Ordinal.finite(other) + self
        return NotImplemented
    
    def __mul__(self, other: 'Ordinal') -> 'Ordinal':
        """
        Ordinal multiplication. For ordinals α and β:
        - If both are finite: α * β = standard multiplication
        - If α is finite and β is transfinite: α * β = β
        - If α is transfinite and β is finite > 0: α * β = α·β
        - If both are transfinite: Complex rules apply
        """
        if not isinstance(other, Ordinal):
            if isinstance(other, int):
                other = Ordinal.finite(other)
            else:
                return NotImplemented
        
        # If either is zero, return zero
        if not self.terms or not other.terms:
            return Ordinal()
            
        # If both are finite, do regular multiplication
        if self.is_finite() and other.is_finite():
            return Ordinal.finite(self.to_int() * other.to_int())
            
        # If one is finite and the other is transfinite
        if self.is_finite():
            n = self.to_int()
            # n * ω = ω for any finite n > 0
            if n > 0:
                return other
            return Ordinal()  # 0 * anything = 0
            
        if other.is_finite():
            n = other.to_int()
            if n == 0:
                return Ordinal()  # anything * 0 = 0
                
            # For α transfinite and n finite > 0, α * n means α repeated n times
            # Simplified implementation for basic cases
            if n == 1:
                return self
            
            # For simple case where self = ω^k, we have ω^k * n = ω^k * n
            if len(self.terms) == 1 and list(self.terms.values())[0] == 1:
                exponent = list(self.terms.keys())[0]
                return Ordinal(terms={exponent: n})
            
            # General case would require more complex implementation
            # This is a simplified version
            result = self.terms.copy()
            # Scale the coefficient of the smallest term
            min_exponent = min(self.terms.keys())
            result[min_exponent] *= n
            return Ordinal(terms=result)
            
        # Both are transfinite - advanced case
        # For now, we'll implement a simplified version for common cases
        # Full implementation would need Cantor normal form operations
        if len(self.terms) == 1 and len(other.terms) == 1:
            self_exp = list(self.terms.keys())[0]
            other_exp = list(other.terms.keys())[0]
            self_coeff = list(self.terms.values())[0]
            other_coeff = list(other.terms.values())[0]
            
            # ω^a * ω^b = ω^(a+b)
            if self_exp[0] > 0 and other_exp[0] > 0:
                new_exp = (self_exp[0] + other_exp[0],)
                return Ordinal(terms={new_exp: 1})
                
        # Fallback for unsupported cases
        raise NotImplementedError("Complex transfinite multiplication not fully implemented")
    
    def __rmul__(self, other):
        """Handle multiplication when ordinal is on the right."""
        if isinstance(other, int):
            return Ordinal.finite(other) * self
        return NotImplemented
    
    def __eq__(self, other) -> bool:
        """Check if two ordinals are equal."""
        if isinstance(other, int):
            other = Ordinal.finite(other)
        if not isinstance(other, Ordinal):
            return NotImplemented
        return self.terms == other.terms
    
    def __lt__(self, other) -> bool:
        """Check if self is less than other."""
        if isinstance(other, int):
            other = Ordinal.finite(other)
        if not isinstance(other, Ordinal):
            return NotImplemented
            
        # If self is empty (zero) and other is not, self < other
        if not self.terms:
            return bool(other.terms)
        # If other is empty (zero), self is not < other
        if not other.terms:
            return False
            
        # Compare by highest exponent
        self_keys = list(self.terms.keys())
        other_keys = list(other.terms.keys())
        
        # Compare exponents from highest to lowest
        for i in range(min(len(self_keys), len(other_keys))):
            if self_keys[i] < other_keys[i]:
                return True
            if self_keys[i] > other_keys[i]:
                return False
            # If exponents are equal, compare coefficients
            if self.terms[self_keys[i]] < other.terms[other_keys[i]]:
                return True
            if self.terms[self_keys[i]] > other.terms[other_keys[i]]:
                return False
                
        # If we get here, one ordinal is a prefix of the other
        return len(self_keys) < len(other_keys)
    
    def __le__(self, other) -> bool:
        """Check if self is less than or equal to other."""
        return self < other or self == other
    
    def __gt__(self, other) -> bool:
        """Check if self is greater than other."""
        if isinstance(other, int):
            other = Ordinal.finite(other)
        if not isinstance(other, Ordinal):
            return NotImplemented
        return other < self
    
    def __ge__(self, other) -> bool:
        """Check if self is greater than or equal to other."""
        return self > other or self == other
    
    def __repr__(self) -> str:
        """String representation of the ordinal."""
        if not self.terms:
            return "0"
            
        parts = []
        for exponents, coeff in self.terms.items():
            if exponents == (0,):
                parts.append(str(coeff))
            else:
                term = ""
                if coeff > 1:
                    term += str(coeff) + "·"
                term += "ω"
                if exponents[0] > 1:
                    term += f"^{exponents[0]}"
                parts.append(term)
                
        return " + ".join(parts)
    
    def numerical_value(self, max_finite: int = 1000000) -> float:
        """
        Approximate numerical value for comparison purposes.
        
        For finite ordinals, returns the actual value.
        For transfinite ordinals, returns a very large number
        that preserves ordering up to max_finite.
        
        Args:
            max_finite: Maximum value for finite ordinals
            
        Returns:
            float: Numerical approximation
        """
        if self.is_finite():
            return float(self.to_int())
            
        # For transfinite ordinals, return a large value that preserves ordering
        result = max_finite
        multiplier = max_finite
        
        # Process terms from largest to smallest
        for exponents, coeff in self.terms.items():
            if exponents == (0,):  # Finite term
                result += coeff
            else:
                # For ω^n term, add max_finite^(n+1) * coeff
                # This ensures proper ordering between different exponents
                exp_val = exponents[0]
                result += multiplier**(exp_val + 1) * coeff
                
        return float(result)


def ordinal_distance(a: Union[Ordinal, int], b: Union[Ordinal, int]) -> Ordinal:
    """
    Calculate the ordinal distance between two ordinals.
    
    In the Matryoshka framework, this determines coupling strength
    and other important parameters.
    
    Args:
        a: First ordinal
        b: Second ordinal
        
    Returns:
        Ordinal: Distance between the ordinals
    """
    if isinstance(a, int):
        a = Ordinal.finite(a)
    if isinstance(b, int):
        b = Ordinal.finite(b)
        
    # Ensure ordinals are properly compared
    if a < b:
        smaller, larger = a, b
    else:
        smaller, larger = b, a
        
    # Both finite case
    if smaller.is_finite() and larger.is_finite():
        return Ordinal.finite(abs(larger.to_int() - smaller.to_int()))
        
    # One finite, one transfinite case
    if smaller.is_finite() and not larger.is_finite():
        # For i < ω ≤ j, ord(|i-j|) = ω + (j-i)
        # Simplified: return ω
        return Ordinal.omega()
        
    # Both transfinite case
    # This is a simplified implementation
    # Full implementation would need Cantor normal form operations
    smaller_keys = list(smaller.terms.keys())
    larger_keys = list(larger.terms.keys())
    
    # If highest exponents differ, return the difference
    if smaller_keys[0] != larger_keys[0]:
        # Simplified: we should compute the actual ordinal difference
        # But for now, we'll return the larger's highest exponent
        return Ordinal(terms={larger_keys[0]: 1})
        
    # If highest exponents are the same but coefficients differ
    if smaller.terms[smaller_keys[0]] != larger.terms[larger_keys[0]]:
        # Return the difference in the coefficients
        diff = abs(larger.terms[larger_keys[0]] - smaller.terms[smaller_keys[0]])
        return Ordinal(terms={smaller_keys[0]: diff})
        
    # If highest term is the same, recurse to next term
    # This is a simplified implementation
    # For now, just return a simple approximation
    return Ordinal.finite(1)


def numerical_ordinal_distance(a: Union[Ordinal, int], b: Union[Ordinal, int], 
                              omega_val: float = 1000.0) -> float:
    """
    Calculate a numerical approximation of ordinal distance.
    
    This function is useful for numerical computations in the Matryoshka
    framework, where we need concrete values for shell couplings, etc.
    
    Args:
        a: First ordinal
        b: Second ordinal
        omega_val: Numerical value assigned to ω
        
    Returns:
        float: Numerical approximation of ordinal distance
    """
    if isinstance(a, int):
        a = Ordinal.finite(a)
    if isinstance(b, int):
        b = Ordinal.finite(b)
        
    # Both finite case
    if a.is_finite() and b.is_finite():
        return abs(a.to_int() - b.to_int())
        
    # One finite, one transfinite case
    if a.is_finite() and not b.is_finite():
        return omega_val + b.numerical_value(max_finite=omega_val) - a.to_int()
    if not a.is_finite() and b.is_finite():
        return omega_val + a.numerical_value(max_finite=omega_val) - b.to_int()
        
    # Both transfinite case
    return abs(a.numerical_value(max_finite=omega_val) - b.numerical_value(max_finite=omega_val))


# Quick access to common ordinals
ZERO = Ordinal.finite(0)
ONE = Ordinal.finite(1)
OMEGA = Ordinal.omega()
OMEGA_2 = OMEGA + OMEGA  # ω·2
OMEGA_SQUARED = Ordinal.omega_power(2)  # ω²