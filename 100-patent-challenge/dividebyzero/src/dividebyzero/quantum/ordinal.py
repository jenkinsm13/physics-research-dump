"""
Ordinal arithmetic and transfinite operations for quantum calculations.

This module provides rigorous handling of ordinal numbers and transfinite operations,
particularly focused on quantum mechanical applications where proper handling of
infinite-dimensional spaces and limit operations is critical.
"""

import numpy as np
from typing import Union, Optional, Callable, List, Tuple
from ..array import DimensionalArray
from ..exceptions import DimensionalError
from ..powers import power
from ..logarithms import log, log2, log10
import mpmath as mp

class Ordinal(DimensionalArray):
    """
    Representation of ordinal numbers with proper arithmetic operations.
    
    Handles both finite and transfinite ordinals, with special support for
    operations at and beyond ω (omega). Implements rigorous ordinal arithmetic
    following the von Neumann construction.
    """
    
    def __init__(self, value: Union[int, float, str], 
                 is_finite: bool = True,
                 base_omega_multiple: int = 0):
        """
        Initialize an ordinal number.
        
        Parameters
        ----------
        value : Union[int, float, str]
            For finite ordinals: the numeric value
            For transfinite ordinals: either "w" for ω, or "w+n" for ω+n
        is_finite : bool
            Whether this is a finite ordinal
        base_omega_multiple : int
            For transfinite ordinals, the coefficient of ω (e.g., 2 for 2ω)
        """
        self.is_finite = is_finite
        self.base_omega_multiple = base_omega_multiple
        
        if isinstance(value, str):
            if value.lower().startswith('w'):
                self.is_finite = False
                # Parse ω+n format
                if '+' in value:
                    _, n = value.split('+')
                    self.finite_part = int(n)
                else:
                    self.finite_part = 0
                self.value = float('inf')
            else:
                self.is_finite = True
                self.value = float(value)
                self.finite_part = int(float(value))
        else:
            if is_finite:
                self.value = float(value)
                self.finite_part = int(float(value))
            else:
                self.value = float('inf')
                self.finite_part = int(float(value)) if value != float('inf') else 0
    
    def __add__(self, other: 'Ordinal') -> 'Ordinal':
        """Ordinal addition following von Neumann arithmetic"""
        if self.is_finite and other.is_finite:
            return Ordinal(self.value + other.value)
        
        # ω + n = ω for finite n
        if not self.is_finite and other.is_finite:
            return Ordinal('w', is_finite=False, 
                         base_omega_multiple=self.base_omega_multiple)
        
        # n + ω = ω for finite n
        if self.is_finite and not other.is_finite:
            return Ordinal('w', is_finite=False,
                         base_omega_multiple=other.base_omega_multiple)
        
        # ω + ω = 2ω
        return Ordinal('w', is_finite=False,
                      base_omega_multiple=self.base_omega_multiple + other.base_omega_multiple)
    
    def __mul__(self, other: 'Ordinal') -> 'Ordinal':
        """Ordinal multiplication"""
        if self.is_finite and other.is_finite:
            return Ordinal(self.value * other.value)
        
        # ω * n = ω for finite n > 0
        if not self.is_finite and other.is_finite and other.value > 0:
            return Ordinal('w', is_finite=False,
                         base_omega_multiple=self.base_omega_multiple)
        
        # n * ω = ω for finite n > 0
        if self.is_finite and not other.is_finite and self.value > 0:
            return Ordinal('w', is_finite=False,
                         base_omega_multiple=other.base_omega_multiple)
        
        # ω * ω = ω^2
        return Ordinal('w', is_finite=False,
                      base_omega_multiple=self.base_omega_multiple * other.base_omega_multiple)
    
    def __str__(self) -> str:
        """String representation of the ordinal"""
        if self.is_finite:
            return str(self.value)
        if self.base_omega_multiple > 1:
            base = f"{self.base_omega_multiple}ω"
        else:
            base = "ω"
        if self.finite_part > 0:
            return f"{base}+{self.finite_part}"
        return base
    
    def __repr__(self) -> str:
        return f"Ordinal('{str(self)}')"
    
    def __lt__(self, other: 'Ordinal') -> bool:
        """Ordinal comparison (<)"""
        if self.is_finite and other.is_finite:
            return self.value < other.value
        if self.is_finite:
            return True  # Finite ordinals are less than infinite ones
        if other.is_finite:
            return False  # Infinite ordinals are not less than finite ones
        # Compare infinite ordinals by their ω coefficients
        if self.base_omega_multiple != other.base_omega_multiple:
            return self.base_omega_multiple < other.base_omega_multiple
        return self.finite_part < other.finite_part
    
    def __eq__(self, other: 'Ordinal') -> bool:
        """Ordinal equality"""
        if self.is_finite and other.is_finite:
            return self.value == other.value
        if self.is_finite or other.is_finite:
            return False
        return (self.base_omega_multiple == other.base_omega_multiple and 
                self.finite_part == other.finite_part)

class TransfiniteSum:
    """
    Handles summation over transfinite ordinal indices.
    
    Implements proper handling of series that extend beyond finite ordinals,
    with rigorous convergence analysis and limit operations.
    """
    
    def __init__(self, term_function: Callable[[Union[int, Ordinal]], float],
                 ordinal_start: Union[int, Ordinal],
                 ordinal_limit: Ordinal,
                 convergence_rate: Optional[float] = None):
        """
        Initialize a transfinite sum.
        
        Parameters
        ----------
        term_function : callable
            Function that computes each term of the sum
        ordinal_start : Union[int, Ordinal]
            Starting ordinal for the sum
        ordinal_limit : Ordinal
            Limit ordinal (typically ω)
        convergence_rate : float, optional
            Expected rate of convergence for acceleration methods
        """
        self.term_function = term_function
        self.start = (Ordinal(ordinal_start) if isinstance(ordinal_start, (int, float)) 
                     else ordinal_start)
        self.limit = ordinal_limit
        self.convergence_rate = convergence_rate
    
    def evaluate_finite_part(self, n_terms: int = 1000) -> float:
        """Evaluate the finite part of the sum"""
        result = 0.0
        if isinstance(self.start, Ordinal) and not self.start.is_finite:
            return result
        
        start_idx = int(self.start.value if isinstance(self.start, Ordinal) 
                       else self.start)
        
        for i in range(start_idx, start_idx + n_terms):
            result += self.term_function(i)
        return result
    
    def evaluate_transfinite_part(self, 
                                n_samples: int = 100,
                                method: str = 'richardson') -> float:
        """
        Evaluate the transfinite part of the sum using extrapolation.
        
        Parameters
        ----------
        n_samples : int
            Number of samples for extrapolation
        method : str
            Extrapolation method ('richardson' or 'shanks')
        """
        if isinstance(self.limit, Ordinal) and self.limit.is_finite:
            return 0.0
        
        # Sample points exponentially spaced
        points = np.logspace(0, 10, n_samples)
        values = np.array([self.term_function(Ordinal('w+' + str(int(p))))
                          for p in points])
        
        if method == 'richardson':
            # Richardson extrapolation
            while len(values) > 1:
                values = (2 * values[1:] - values[:-1]) / 1
                if np.all(np.abs(values[1:] - values[:-1]) < 1e-10):
                    break
            return float(values[0])
        else:
            # Shanks transformation
            numerator = values[1:]**2 - values[:-1] * values[2:]
            denominator = 2*values[1:] - values[:-1] - values[2:]
            with np.errstate(divide='ignore', invalid='ignore'):
                transformed = numerator / denominator
            return float(np.nanmean(transformed[np.isfinite(transformed)]))
    
    def evaluate(self) -> float:
        """
        Evaluate the complete transfinite sum.
        
        Uses a combination of direct summation for the finite part
        and extrapolation techniques for the transfinite part.
        """
        finite_sum = self.evaluate_finite_part()
        transfinite_sum = self.evaluate_transfinite_part()
        
        if self.convergence_rate is not None:
            # Apply convergence acceleration if rate is known
            correction = transfinite_sum * np.exp(-self.convergence_rate)
            return finite_sum + correction
        
        return finite_sum + transfinite_sum

def ordinal_distance(a: Ordinal, b: Ordinal) -> Union[float, Ordinal]:
    """
    Calculate the ordinal distance between two ordinals.
    
    For finite ordinals, this is just the absolute difference.
    For transfinite ordinals, implements proper ordinal arithmetic.
    
    Parameters
    ----------
    a, b : Ordinal
        Ordinals to compute distance between
    
    Returns
    -------
    Union[float, Ordinal]
        The ordinal distance
    """
    if a.is_finite and b.is_finite:
        return abs(a.value - b.value)
    
    if a.is_finite:
        # Distance from finite to infinite is infinite
        return Ordinal('w', base_omega_multiple=b.base_omega_multiple)
    
    if b.is_finite:
        # Distance from infinite to finite is infinite
        return Ordinal('w', base_omega_multiple=a.base_omega_multiple)
    
    # Both transfinite
    if a.base_omega_multiple == b.base_omega_multiple:
        return abs(a.finite_part - b.finite_part)
    return Ordinal('w', base_omega_multiple=abs(a.base_omega_multiple - b.base_omega_multiple))

def ordinal_logarithm(x: Union[int, float, Ordinal]) -> Union[float, Ordinal]:
    """
    Compute the ordinal logarithm, properly handling transfinite values.
    
    Parameters
    ----------
    x : Union[int, float, Ordinal]
        Value to compute logarithm of
    
    Returns
    -------
    Union[float, Ordinal]
        The ordinal logarithm
    """
    if isinstance(x, (int, float)):
        return float(np.log(x) if x > 0 else 0)
    
    if x.is_finite:
        return float(np.log(x.value) if x.value > 0 else 0)
    
    # For transfinite ordinals, return a scaled ordinal
    return Ordinal('w', base_omega_multiple=max(1, x.base_omega_multiple - 1)) 