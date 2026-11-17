import numpy as np
import dividebyzero as dbz
import pytest
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

class TestDivideByZeroAdvanced:
    """Advanced test suite for dividebyzero library."""
    
    def setup_method(self):
        """Set up test environment."""
        # Enable more detailed logging for tests
        dbz.set_log_level('INFO')
        
    def test_singular_matrix_operations(self):
        """Test operations on singular matrices."""
        # Create a singular matrix
        A = dbz.array([[1, 2], [2, 4]])
        
        # Compute determinant (should be zero)
        det_A = dbz.linalg.det(A)
        assert np.isclose(det_A, 0)
        
        # Try inverting the singular matrix
        A_inv = dbz.linalg.inv(A)
        
        # The result should be a DimensionalArray with special properties
        assert isinstance(A_inv, dbz.DimensionalArray)
        
        # Check that A * A_inv is close to identity for non-singular subspace
        # This tests the dimensional reduction approach
        identity_approx = A @ A_inv
        
        # Check the reconstructed pseudo-inverse property
        # For singular matrices, we can't get perfect identity
        # But we should get identity in the row space
        U, S, Vh = dbz.linalg.svd(A)
        rank = np.sum(S > 1e-10)
        
        # The first 'rank' columns of U should be preserved
        U_rank = U[:, :rank]
        
        # U_rank.T @ identity_approx @ U_rank should be identity
        subspace_identity = U_rank.T @ identity_approx @ U_rank
        expected_subspace = dbz.eye(rank)
        
        # Check if close in the valid subspace
        assert dbz.linalg.norm(subspace_identity - expected_subspace) < 1e-6
        
        # Now test with random singular matrices
        for _ in range(5):
            n = 5
            # Create a random matrix with specific rank
            rank = np.random.randint(1, n)
            X = dbz.array(np.random.randn(n, rank))
            Y = dbz.array(np.random.randn(rank, n))
            B = X @ Y  # This creates an n×n matrix with rank=rank
            
            # Get inverse
            B_inv = dbz.linalg.inv(B)
            
            # Test reconstruction in valid subspace
            identity_approx = B @ B_inv
            U, S, Vh = dbz.linalg.svd(B)
            actual_rank = np.sum(S > 1e-10)
            assert actual_rank == rank
            
            # Test in valid subspace
            U_rank = U[:, :rank]
            subspace_identity = U_rank.T @ identity_approx @ U_rank
            expected_subspace = dbz.eye(rank)
            assert dbz.linalg.norm(subspace_identity - expected_subspace) < 1e-6
    
    def test_division_by_zero_vector_fields(self):
        """Test division by zero in vector fields."""
        # Create a grid
        x = np.linspace(-2, 2, 50)
        y = np.linspace(-2, 2, 50)
        X, Y = np.meshgrid(x, y)
        
        # Convert to dbz arrays
        X_dbz = dbz.array(X)
        Y_dbz = dbz.array(Y)
        
        # Create a function with singularity at origin
        # f(x,y) = (x, y) / (x² + y²)
        Z = X_dbz**2 + Y_dbz**2
        
        # This division would normally cause issues at (0,0)
        Vx = X_dbz / Z  # x component of vector field
        Vy = Y_dbz / Z  # y component of vector field
        
        # Check that we didn't get NaN or Inf at the singularity
        assert not np.any(np.isnan(Vx.asnumpy()))
        assert not np.any(np.isnan(Vy.asnumpy()))
        assert not np.any(np.isinf(Vx.asnumpy()))
        assert not np.any(np.isinf(Vy.asnumpy()))
        
        # We can also compute the divergence of this vector field
        # div(F) = ∂Vx/∂x + ∂Vy/∂y
        # For this particular field, the theoretical divergence is 0 away from origin
        # At origin, our library should handle it special
        
        # Compute numerical gradient
        dx = x[1] - x[0]
        dy = y[1] - y[0]
        
        # Forward differences for derivatives
        dVx_dx = dbz.zeros_like(Vx)
        dVy_dy = dbz.zeros_like(Vy)
        
        # Compute x derivative
        dVx_dx[:, 1:] = (Vx[:, 1:] - Vx[:, :-1]) / dx
        # Compute y derivative
        dVy_dy[1:, :] = (Vy[1:, :] - Vy[:-1, :]) / dy
        
        # Compute divergence
        div = dVx_dx + dVy_dy
        
        # Away from origin, divergence should be close to zero
        # Define "away from origin" as a distance > 0.5
        mask = (X_dbz**2 + Y_dbz**2) > 0.5**2
        div_away = div[mask]
        
        # Check that divergence is small away from singularity
        assert dbz.max(dbz.abs(div_away)) < 10.0
    
    def test_logarithmic_singularities(self):
        """Test logarithmic functions near singularities."""
        # Test scalar logarithm near zero
        x_small = dbz.array(1e-10)
        log_x = dbz.log(x_small)
        
        # Should return a finite value
        assert not np.isnan(log_x.asnumpy())
        assert not np.isinf(log_x.asnumpy())
        
        # Test matrix logarithm
        # Create a singular matrix
        A = dbz.array([[1, 1], [1, 1]])  # Rank 1 matrix
        log_A = dbz.logm(A)
        
        # Should be able to reconstruct approximately
        exp_log_A = dbz.linalg.expm(log_A)
        
        # Check reconstruction in the row space
        U, S, Vh = dbz.linalg.svd(A)
        rank = np.sum(S > 1e-10)
        U_rank = U[:, :rank]
        
        # Project back to row space
        A_proj = U_rank @ dbz.diag(S[:rank]) @ Vh[:rank, :]
        exp_log_A_proj = U_rank.T @ exp_log_A @ U_rank
        A_proj_reduced = U_rank.T @ A_proj @ U_rank
        
        # Should be close in valid subspace
        assert dbz.linalg.norm(exp_log_A_proj - A_proj_reduced) < 1e-6
        
        # Test log entropy on quantum state
        # Create a mixed quantum state (density matrix)
        rho = dbz.array([[0.7, 0.1], [0.1, 0.3]])
        entropy = dbz.log_entropy(rho)
        
        # von Neumann entropy should be between 0 and log(d)
        assert entropy >= 0
        assert entropy <= dbz.log(2)
        
        # Test with pure state (should have zero entropy)
        pure_state = dbz.array([[1, 0], [0, 0]])
        pure_entropy = dbz.log_entropy(pure_state)
        assert np.isclose(pure_entropy, 0)
        
        # Test log negativity for entangled states
        # Create a maximally entangled state (Bell state)
        # |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
        # As a density matrix, this is:
        bell_state = dbz.array([
            [0.5, 0, 0, 0.5],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0.5, 0, 0, 0.5]
        ])
        
        # Reshape to 2x2x2x2 for partial transpose
        bell_tensor = bell_state.reshape(2, 2, 2, 2)
        
        # Calculate log negativity
        negativity = dbz.log_negativity(bell_tensor)
        
        # For a Bell state, log negativity should be log(2)
        assert np.isclose(negativity, dbz.log(2))
    
    def test_fft_signal_processing(self):
        """Test FFT and signal processing capabilities."""
        # Create a signal with multiple frequency components
        t = dbz.linspace(0, 1, 1000)
        f1, f2, f3 = 5, 25, 50
        signal = dbz.sin(2 * dbz.pi * f1 * t) + \
                 0.5 * dbz.sin(2 * dbz.pi * f2 * t) + \
                 0.25 * dbz.sin(2 * dbz.pi * f3 * t)
        
        # Compute FFT
        fft_result = dbz.fft.fft(signal)
        
        # Compute frequency bins
        n = len(t)
        freqs = dbz.fft.fftfreq(n, 1/n)
        
        # Get the positive frequencies
        pos_freqs = freqs[freqs > 0]
        pos_fft = fft_result[freqs > 0]
        
        # Find the peaks
        amplitudes = dbz.abs(pos_fft)
        peak_indices = dbz.where(amplitudes > 0.1 * dbz.max(amplitudes))[0]
        peak_freqs = pos_freqs[peak_indices]
        
        # Check that we detected our three frequencies
        detected_freqs = sorted([int(f + 0.5) for f in peak_freqs])
        expected_freqs = [f1, f2, f3]
        
        # They should match within 1 Hz
        for detected, expected in zip(detected_freqs, expected_freqs):
            assert abs(detected - expected) <= 1
        
        # Test inverse FFT
        signal_reconstructed = dbz.fft.ifft(fft_result)
        
        # Real part should closely match original signal
        signal_reconstructed_real = dbz.real(signal_reconstructed)
        error = dbz.max(dbz.abs(signal_reconstructed_real - signal))
        assert error < 1e-10
    
    def test_quantum_operations(self):
        """Test quantum tensor operations."""
        # Create simple qubit states
        zero = dbz.array([1, 0])
        one = dbz.array([0, 1])
        
        # Create a Bell state using tensor product
        bell_state = dbz.quantum.tensor_product(
            1/dbz.sqrt(2) * (zero + one),
            1/dbz.sqrt(2) * (zero + one)
        )
        
        # Apply a quantum gate (X gate on first qubit)
        X_gate = dbz.array([[0, 1], [1, 0]])
        I_gate = dbz.array([[1, 0], [0, 1]])
        
        # Tensor product of X and I gates
        X_I_gate = dbz.quantum.tensor_product(X_gate, I_gate)
        
        # Apply gate to state
        new_state = X_I_gate @ bell_state
        
        # Test quantum measurement
        probabilities = dbz.abs(new_state)**2
        assert dbz.sum(probabilities) - 1.0 < 1e-10
        
        # Test partial trace
        system_size = (2, 2)  # Two qubits
        bell_density = dbz.outer(bell_state, bell_state)
        reduced_density = dbz.quantum.partial_trace(bell_density, system_size, [1])
        
        # For a Bell state, the reduced density matrix should be maximally mixed
        expected_reduced = dbz.array([[0.5, 0], [0, 0.5]])
        assert dbz.linalg.norm(reduced_density - expected_reduced) < 1e-10
    
    def test_performance_benchmarks(self):
        """Test library performance on large-scale operations."""
        # Performance benchmark for large matrix operations
        sizes = [100, 500, 1000]
        times_numpy = []
        times_dbz = []
        
        for size in sizes:
            # Create random matrices
            A_np = np.random.rand(size, size)
            B_np = np.random.rand(size, size)
            A_dbz = dbz.array(A_np)
            B_dbz = dbz.array(B_np)
            
            # Time NumPy matrix multiplication
            t0 = time.time()
            C_np = A_np @ B_np
            t1 = time.time()
            times_numpy.append(t1 - t0)
            
            # Time dividebyzero matrix multiplication
            t0 = time.time()
            C_dbz = A_dbz @ B_dbz
            t1 = time.time()
            times_dbz.append(t1 - t0)
            
            # Results should match
            assert np.allclose(C_np, C_dbz.asnumpy())
        
        # Performance shouldn't be more than 5x slower than NumPy
        # (This is a generous margin since the library does additional checks)
        for tnp, tdbz in zip(times_numpy, times_dbz):
            assert tdbz / tnp < 5.0
    
    def test_visualize_vector_field(self):
        """Create a visualization of a vector field with singularity."""
        # This is more a demonstration than a test
        # Create a grid
        x = np.linspace(-2, 2, 30)
        y = np.linspace(-2, 2, 30)
        X, Y = np.meshgrid(x, y)
        
        # Convert to dbz arrays
        X_dbz = dbz.array(X)
        Y_dbz = dbz.array(Y)
        
        # Create a function with singularity at origin
        # f(x,y) = (x, y) / (x² + y²)  (the normalized radial vector field)
        Z = X_dbz**2 + Y_dbz**2
        
        # This division would normally cause issues at (0,0)
        Vx = X_dbz / Z  # x component of vector field
        Vy = Y_dbz / Z  # y component of vector field
        
        # Compute field magnitude
        magnitude = dbz.sqrt(Vx**2 + Vy**2)
        
        # Convert back to NumPy for plotting
        Vx_np = Vx.asnumpy()
        Vy_np = Vy.asnumpy()
        magnitude_np = magnitude.asnumpy()
        
        # The plot itself is not part of the test, just demonstrating
        # that the computation worked without errors
        assert not np.any(np.isnan(Vx_np))
        assert not np.any(np.isnan(Vy_np))
        assert not np.any(np.isinf(Vx_np))
        assert not np.any(np.isinf(Vy_np))
        
        # For a real visualization, one would add:
        plt.figure(figsize=(10, 8))
        plt.quiver(X, Y, Vx_np, Vy_np, magnitude_np, cmap='viridis')
        plt.colorbar(label='Vector magnitude')
        plt.title('Vector Field with Singularity Handling')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig('vector_field.png')
        # plt.close()

if __name__ == "__main__":
    # Run the tests
    test_instance = TestDivideByZeroAdvanced()
    test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
    
    for method in test_methods:
        print(f"Running {method}...")
        test_instance.setup_method()
        getattr(test_instance, method)()
        print(f"{method} completed successfully.\n")