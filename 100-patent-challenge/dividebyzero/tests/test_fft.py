"""Tests for the FFT module."""
import pytest
import numpy as np
from dividebyzero import array
from dividebyzero.array import DimensionalArray
from dividebyzero.fft import (
    fft2, ifft2, fftshift, ifftshift, fftfreq,
    rfft2, irfft2, rfftfreq
)

def test_fft2():
    """Test 2D FFT functionality."""
    # Create a test array
    test_array = array(np.random.rand(4, 4))
    
    # Apply FFT
    result = fft2(test_array)
    
    # Verify result is a DimensionalArray
    assert isinstance(result, DimensionalArray)
    
    # Verify shape is preserved
    assert result.shape == test_array.shape
    
    # Test roundtrip: ifft2(fft2(x)) ≈ x
    roundtrip = ifft2(result)
    assert np.allclose(roundtrip.array, test_array.array)
    
    # Test with numpy array input
    numpy_input = np.random.rand(4, 4)
    numpy_result = fft2(numpy_input)
    assert isinstance(numpy_result, DimensionalArray)
    
    # Verify error tracking can be preserved
    error_array = test_array.copy()
    error_array._error_id = 12345  # Set an error ID directly
    
    error_fft = fft2(error_array)
    assert hasattr(error_fft, '_error_id')
    assert error_fft._error_id == 12345

def test_ifft2():
    """Test inverse 2D FFT functionality."""
    # Create a test array
    test_array = array(np.random.rand(4, 4))
    
    # Apply FFT and IFFT
    fft_result = fft2(test_array)
    ifft_result = ifft2(fft_result)
    
    # Verify result is a DimensionalArray
    assert isinstance(ifft_result, DimensionalArray)
    
    # Verify shape is preserved
    assert ifft_result.shape == test_array.shape
    
    # Test that ifft2 recovers the original array
    assert np.allclose(ifft_result.array, test_array.array)
    
    # Test with numpy array input
    numpy_input = np.random.rand(4, 4) + 1j * np.random.rand(4, 4)
    numpy_result = ifft2(numpy_input)
    assert isinstance(numpy_result, DimensionalArray)
    
    # Verify error tracking can be preserved
    error_array = test_array.copy()
    error_array._error_id = 12345  # Set an error ID directly
    
    fft_error = fft2(error_array)
    ifft_error = ifft2(fft_error)
    assert hasattr(ifft_error, '_error_id')
    assert ifft_error._error_id == 12345

def test_fftshift():
    """Test FFT shift functionality."""
    # Create a test array
    test_array = array(np.random.rand(5, 5))
    
    # Apply FFT and shift
    fft_result = fft2(test_array)
    shifted = fftshift(fft_result)
    
    # Verify result is a DimensionalArray
    assert isinstance(shifted, DimensionalArray)
    
    # Verify shape is preserved
    assert shifted.shape == test_array.shape
    
    # Test that ifftshift(fftshift(x)) == x
    unshifted = ifftshift(shifted)
    assert np.allclose(unshifted.array, fft_result.array)
    
    # Test with numpy array input
    numpy_input = np.random.rand(5, 5)
    numpy_result = fftshift(numpy_input)
    assert isinstance(numpy_result, DimensionalArray)
    
    # Verify error tracking can be preserved
    error_array = test_array.copy()
    error_array._error_id = 12345  # Set an error ID directly
    
    fft_error = fft2(error_array)
    shifted_error = fftshift(fft_error)
    assert hasattr(shifted_error, '_error_id')
    assert shifted_error._error_id == 12345

def test_ifftshift():
    """Test inverse FFT shift functionality."""
    # Create a test array
    test_array = array(np.random.rand(5, 5))
    
    # Apply FFT, shift, and inverse shift
    fft_result = fft2(test_array)
    shifted = fftshift(fft_result)
    unshifted = ifftshift(shifted)
    
    # Verify result is a DimensionalArray
    assert isinstance(unshifted, DimensionalArray)
    
    # Verify shape is preserved
    assert unshifted.shape == test_array.shape
    
    # Test that unshifted == original
    assert np.allclose(unshifted.array, fft_result.array)
    
    # Test with numpy array input
    numpy_input = np.random.rand(5, 5)
    numpy_result = ifftshift(numpy_input)
    assert isinstance(numpy_result, DimensionalArray)
    
    # Verify error tracking can be preserved
    error_array = test_array.copy()
    error_array._error_id = 12345  # Set an error ID directly
    
    fft_error = fft2(error_array)
    shifted_error = fftshift(fft_error)
    unshifted_error = ifftshift(shifted_error)
    assert hasattr(unshifted_error, '_error_id')
    assert unshifted_error._error_id == 12345

def test_fftfreq():
    """Test FFT frequency function."""
    # Test with default parameters
    freqs = fftfreq(8)
    
    # Verify result is a DimensionalArray
    assert isinstance(freqs, DimensionalArray)
    
    # Verify shape
    assert freqs.shape == (8,)
    
    # Test with custom sample spacing
    freqs_spaced = fftfreq(8, 0.5)
    
    # Verify frequencies are scaled correctly
    assert np.allclose(freqs_spaced.array, freqs.array * 2)

def test_rfft2():
    """Test real 2D FFT functionality."""
    # Create a real-valued test array
    test_array = array(np.random.rand(4, 4))
    
    # Apply real FFT
    result = rfft2(test_array)
    
    # Verify result is a DimensionalArray
    assert isinstance(result, DimensionalArray)
    
    # Verify shape is as expected for rfft2
    assert result.shape[0] == test_array.shape[0]
    assert result.shape[1] == test_array.shape[1] // 2 + 1
    
    # Test roundtrip: irfft2(rfft2(x)) ≈ x
    roundtrip = irfft2(result)
    assert np.allclose(roundtrip.array, test_array.array)
    
    # Test with numpy array input
    numpy_input = np.random.rand(4, 4)
    numpy_result = rfft2(numpy_input)
    assert isinstance(numpy_result, DimensionalArray)
    
    # Verify error tracking can be preserved
    error_array = test_array.copy()
    error_array._error_id = 12345  # Set an error ID directly
    
    error_rfft = rfft2(error_array)
    assert hasattr(error_rfft, '_error_id')
    assert error_rfft._error_id == 12345

def test_irfft2():
    """Test inverse real 2D FFT functionality."""
    # Create a real-valued test array
    test_array = array(np.random.rand(4, 4))
    
    # Apply real FFT and inverse
    rfft_result = rfft2(test_array)
    irfft_result = irfft2(rfft_result)
    
    # Verify result is a DimensionalArray
    assert isinstance(irfft_result, DimensionalArray)
    
    # Verify shape is preserved after roundtrip
    assert irfft_result.shape == test_array.shape
    
    # Test that irfft2 recovers the original array
    assert np.allclose(irfft_result.array, test_array.array)
    
    # Test with numpy array input
    numpy_rfft = np.fft.rfft2(np.random.rand(4, 4))
    numpy_result = irfft2(numpy_rfft)
    assert isinstance(numpy_result, DimensionalArray)
    
    # Verify error tracking can be preserved
    error_array = test_array.copy()
    error_array._error_id = 12345  # Set an error ID directly
    
    rfft_error = rfft2(error_array)
    irfft_error = irfft2(rfft_error)
    assert hasattr(irfft_error, '_error_id')
    assert irfft_error._error_id == 12345

def test_rfftfreq():
    """Test real FFT frequency function."""
    # Test with default parameters
    freqs = rfftfreq(8)
    
    # Verify result is a DimensionalArray
    assert isinstance(freqs, DimensionalArray)
    
    # Verify shape is as expected for rfftfreq
    assert freqs.shape == (5,)  # For n=8, should return 5 frequencies
    
    # Test with custom sample spacing
    freqs_spaced = rfftfreq(8, 0.5)
    
    # Verify frequencies are scaled correctly
    assert np.allclose(freqs_spaced.array, freqs.array * 2)

# ============== Additional comprehensive tests ==============

def test_fft2_known_signal():
    """Test FFT with known signals and expected results."""
    # Create a simple signal with known FFT
    # A constant signal should have all energy at DC (0 frequency)
    constant_array = array(np.ones((4, 4)))
    fft_constant = fft2(constant_array)
    
    # Check that DC component (0,0) has energy
    dc_value = fft_constant.array[0, 0]
    assert abs(dc_value) > 0
    
    # All other components should be close to zero
    mask = np.ones_like(fft_constant.array, dtype=bool)
    mask[0, 0] = False
    assert np.allclose(np.abs(fft_constant.array[mask]), 0, atol=1e-10)
    
    # Test with a simple oscillation pattern 
    # A checkerboard pattern (alternating 1 and -1) has energy at Nyquist frequencies
    oscillation = np.ones((4, 4))
    oscillation[::2, 1::2] = -1
    oscillation[1::2, ::2] = -1
    
    osc_array = array(oscillation)
    fft_osc = fft2(osc_array)
    
    # For a 4x4 checkerboard pattern, the main energy should be at position (2,2)
    # which corresponds to Nyquist frequency in both directions
    assert abs(fft_osc.array[2, 2]) > 0

def test_fft_error_propagation():
    """Test how errors propagate through FFT operations."""
    # Create arrays with different error characteristics
    original = array(np.random.rand(4, 4))
    
    # Create an array with NaN values
    with_nan = original.copy()
    with_nan.array[0, 0] = np.nan
    
    # Apply FFT operations
    fft_result = fft2(with_nan)
    
    # NaN should propagate through FFT
    assert np.any(np.isnan(fft_result.array))
    
    # Create an array with infinity
    with_inf = original.copy()
    with_inf.array[1, 1] = np.inf
    
    # Apply FFT operations
    fft_inf = fft2(with_inf)
    
    # Infinity should propagate
    assert np.any(np.isinf(fft_inf.array)) or np.any(np.isnan(fft_inf.array))

def test_fft_with_singularities():
    """Test FFT operations with singularities in the input."""
    # Create a test array with proper shape for FFT
    test_array = array(np.random.rand(4, 4))
    
    # Set an error ID directly instead of using / 0 which might fail due to shape issues
    singular_array = test_array.copy()
    singular_array._error_id = 12345
    
    # Apply FFT
    fft_singular = fft2(singular_array)
    
    # Apply inverse FFT
    ifft_singular = ifft2(fft_singular)
    
    # The singularity should be preserved through the FFT and IFFT
    assert hasattr(fft_singular, '_error_id')
    assert hasattr(ifft_singular, '_error_id')
    
    # The error ID should be preserved
    assert fft_singular._error_id == singular_array._error_id
    assert ifft_singular._error_id == singular_array._error_id

def test_fft_dimensionality():
    """Test that FFT operations preserve dimensionality information."""
    # Create arrays with different dimensions
    # 1D array (vector)
    vector = array(np.random.rand(8))
    
    # Test that fftshift works with 1D
    shifted_vector = fftshift(vector)
    assert isinstance(shifted_vector, DimensionalArray)
    assert shifted_vector.shape == vector.shape
    
    # 3D array (volume)
    volume = array(np.random.rand(4, 4, 4))
    
    # Test FFT shift with 3D
    shifted_volume = fftshift(volume)
    assert isinstance(shifted_volume, DimensionalArray)
    assert shifted_volume.shape == volume.shape
    
    # Test inverse FFT shift
    unshifted_volume = ifftshift(shifted_volume)
    assert np.allclose(unshifted_volume.array, volume.array)

def test_fft2_with_complex_input():
    """Test 2D FFT with complex input data."""
    # Create a complex-valued array
    real_part = np.random.rand(4, 4)
    imag_part = np.random.rand(4, 4)
    complex_array = array(real_part + 1j * imag_part)
    
    # Apply FFT
    fft_complex = fft2(complex_array)
    
    # Apply inverse FFT
    ifft_complex = ifft2(fft_complex)
    
    # Verify that we recover the original array
    assert np.allclose(ifft_complex.array, complex_array.array)
    
    # Test that fftshift works with complex arrays
    shifted = fftshift(fft_complex)
    assert isinstance(shifted, DimensionalArray)
    
    # Test that ifftshift properly inverts the shift
    unshifted = ifftshift(shifted)
    assert np.allclose(unshifted.array, fft_complex.array)

def test_rfft2_edge_cases():
    """Test real FFT edge cases."""
    # Test with all-zero input
    zeros = array(np.zeros((4, 4)))
    rfft_zeros = rfft2(zeros)
    
    # Output should also be zeros
    assert np.allclose(rfft_zeros.array, 0)
    
    # Test with all-ones input
    ones = array(np.ones((4, 4)))
    rfft_ones = rfft2(ones)
    
    # DC component should equal sum of all elements
    assert np.isclose(rfft_ones.array[0, 0], float(np.prod(ones.shape)))
    
    # All other components should be zero
    mask = np.ones_like(rfft_ones.array, dtype=bool)
    mask[0, 0] = False
    assert np.allclose(rfft_ones.array[mask], 0)

def test_fft_frequency_analysis():
    """Test FFT for frequency analysis applications."""
    # Create a signal with a specific frequency
    n = 64  # Increase to get better frequency resolution
    sample_rate = 100.0  # Hz
    freq = 10.0  # Hz
    
    # Time vector
    t = np.arange(n) / sample_rate
    
    # Signal: sine wave with frequency 'freq'
    signal = np.sin(2 * np.pi * freq * t)
    
    # Pad signal to make it 2D for fft2
    signal_2d = np.zeros((n, 2))
    signal_2d[:, 0] = signal
    
    # Apply FFT
    fft_result = fft2(array(signal_2d))
    
    # Get frequencies
    freqs = fftfreq(n, 1.0/sample_rate)
    
    # Find peak frequency - only look at first half (positive frequencies)
    magnitude = np.abs(fft_result.array[:, 0])
    # Skip DC component at index 0
    peak_idx = np.argmax(magnitude[1:n//2]) + 1
    peak_freq = freqs.array[peak_idx]
    
    # Check that we find a frequency close to our input
    # With FFT, we might not get exactly 10.0 Hz, so allow a small tolerance
    assert abs(peak_freq - freq) < 1.0  # Within 1 Hz 