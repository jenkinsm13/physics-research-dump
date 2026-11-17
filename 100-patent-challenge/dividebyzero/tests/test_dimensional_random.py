"""Tests for dimensional_random module."""
import pytest
import numpy as np
from src.dividebyzero.dimensional_random import *
from src.dividebyzero.array import DimensionalArray

def test_rand():
    """Test rand function."""
    result = rand(3, 4)
    assert isinstance(result, DimensionalArray)
    assert result.array.shape == (3, 4)
    assert np.all((result.array >= 0) & (result.array < 1))

def test_randn():
    """Test randn function."""
    result = randn(2, 3)
    assert isinstance(result, DimensionalArray)
    assert result.array.shape == (2, 3)

def test_randint():
    """Test randint function."""
    result = randint(0, 10, size=(2, 3))
    assert isinstance(result, DimensionalArray)
    assert result.array.shape == (2, 3)
    assert np.all((result.array >= 0) & (result.array < 10))

def test_normal():
    """Test normal function."""
    result = normal(loc=5, scale=2, size=(2, 2))
    assert isinstance(result, DimensionalArray)
    assert result.array.shape == (2, 2)

def test_multivariate_normal():
    """Test multivariate_normal function."""
    mean = [0, 1]
    cov = [[1, 0], [0, 1]]
    result = multivariate_normal(mean, cov, size=5)
    assert isinstance(result, DimensionalArray)
    assert result.array.shape == (5, 2)

    # Test with DimensionalArray inputs
    mean_array = DimensionalArray(mean)
    cov_array = DimensionalArray(cov)
    result2 = multivariate_normal(mean_array, cov_array, size=5)
    assert isinstance(result2, DimensionalArray)
    assert result2.array.shape == (5, 2)

def test_poisson():
    """Test poisson function."""
    result = poisson(lam=5, size=(3, 3))
    assert isinstance(result, DimensionalArray)
    assert result.array.shape == (3, 3)

    # Test with DimensionalArray input
    lam_array = DimensionalArray([3, 4, 5])
    result2 = poisson(lam=lam_array)
    assert isinstance(result2, DimensionalArray)
    assert result2.array.shape == (3,)

def test_choice():
    """Test choice function."""
    result = choice([1, 2, 3, 4], size=5)
    assert isinstance(result, DimensionalArray)
    assert result.array.shape == (5,)
    assert np.all(np.isin(result.array, [1, 2, 3, 4]))

    # Test with DimensionalArray input
    choices = DimensionalArray([5, 6, 7, 8])
    result2 = choice(choices, size=3)
    assert isinstance(result2, DimensionalArray)
    assert result2.array.shape == (3,)
    assert np.all(np.isin(result2.array, [5, 6, 7, 8]))

def test_seed_and_state():
    """Test seed function and state management."""
    # Test setting a seed produces consistent results
    seed(42)
    result1 = rand(3, 3)
    
    seed(42)
    result2 = rand(3, 3)
    
    assert np.array_equal(result1.array, result2.array)
    
    # Test get_state and set_state
    seed(123)
    state = get_state()
    result3 = rand(2, 2)
    
    seed(456)  # Different seed
    result4 = rand(2, 2)  # Should be different from result3
    
    set_state(state)  # Restore earlier state
    result5 = rand(2, 2)  # Should match result3
    
    assert not np.array_equal(result3.array, result4.array)
    assert np.array_equal(result3.array, result5.array)

def test_permutation():
    """Test permutation function."""
    # Test permutation of a sequence
    x = np.array([1, 2, 3, 4, 5])
    result = permutation(x)
    assert isinstance(result, DimensionalArray)
    assert result.array.shape == (5,)
    assert set(result.array) == set(x)  # Same elements, different order
    
    # Test with DimensionalArray input
    x_array = DimensionalArray([5, 6, 7, 8, 9])
    result2 = permutation(x_array)
    assert isinstance(result2, DimensionalArray)
    assert result2.array.shape == (5,)
    assert set(result2.array) == set(x_array.array)
    
    # Test permutation of range
    result3 = permutation(10)  # Should create and permute range(10)
    assert isinstance(result3, DimensionalArray)
    assert result3.array.shape == (10,)
    assert set(result3.array) == set(range(10))

def test_shuffle():
    """Test shuffle function."""
    # Test in-place shuffle of numpy array
    x = np.array([1, 2, 3, 4, 5])
    x_copy = x.copy()
    shuffle(x)
    assert np.array_equal(x.shape, x_copy.shape)
    assert set(x) == set(x_copy)  # Same elements, potentially different order
    
    # Test in-place shuffle of DimensionalArray
    x_array = DimensionalArray([5, 6, 7, 8, 9])
    x_array_data = x_array.array.copy()
    shuffle(x_array)
    assert np.array_equal(x_array.array.shape, x_array_data.shape)
    assert set(x_array.array) == set(x_array_data)  # Same elements, potentially different order

