import numpy as np
import healpy as hp
from scipy.ndimage import gaussian_filter
from scipy.optimize import brentq
import time

# --- 1. Foundational Parameters & Constants ---
# V_void potential is assumed constant, λ modulates its effect.
r_eq = 5.0
A = 1.0
B = 0.5
alpha = 0.5
beta = 0.2
GRID_SIZE = 512  # Lower res for faster calibration runs
NSIDE_OUTPUT = 32
# We now target the MAGNITUDE of the asymmetry
TARGET_ASYMMETRY_MAGNITUDE = 0.0194
# The different hypothetical λ values to test
LAMBDA_TEST_VALUES = [0.005, 0.01, 0.02, 0.04]

# --- 2. Simulation & Analysis Core ---
def F_void(r, r_eq, A, B, alpha, beta):
    r_shifted = r - r_eq
    term1 = A * alpha * 2 * r_shifted * np.exp(-alpha * r_shifted**2)
    term2 = -B * beta * 2 * r_shifted * np.exp(-beta * r_shifted**2)
    return term1 - term2

def run_simulation_for_asymmetry(smoothing_factor, lambda_val, initial_fluctuations, grid_coords, phase):
    X, Y, R = grid_coords
    force_map = F_void(R, r_eq, A, B, alpha, beta)
    # λ now directly modulates the force's impact, WITH A PHASE
    primordial_map = initial_fluctuations * (1 + lambda_val * force_map * np.cos(phase))
    smoothed_map = gaussian_filter(primordial_map, sigma=smoothing_factor)
    
    npix_out = hp.nside2npix(NSIDE_OUTPUT)
    pix_indices = np.arange(npix_out)
    lon, lat = hp.pix2ang(NSIDE_OUTPUT, pix_indices, lonlat=True)
    grid_x = np.clip(((lon + 180) / 360 * GRID_SIZE).astype(int), 0, GRID_SIZE - 1)
    grid_y = np.clip(((lat + 90) / 180 * GRID_SIZE).astype(int), 0, GRID_SIZE - 1)
    simulated_cmb = smoothed_map[grid_y, grid_x]
    
    pix_vecs = hp.pix2vec(NSIDE_OUTPUT, pix_indices)
    map_mean = np.mean(simulated_cmb)
    map_fluctuations = simulated_cmb - map_mean
    power_map = map_fluctuations**2
    alm_power = hp.map2alm(power_map, lmax=1)
    a10, a11 = alm_power[hp.Alm.getidx(1, 1, 0)], alm_power[hp.Alm.getidx(1, 1, 1)]
    dx, dy, dz = np.real(a11), -np.imag(a11), np.real(a10)
    
    # Avoid division by zero if dipole is null
    norm = np.linalg.norm([dx, dy, dz])
    if norm == 0: return 0
    asymmetry_axis = np.array([dx, dy, dz]) / norm
    
    dot_products = np.dot(asymmetry_axis, pix_vecs)
    h1_indices = np.where(dot_products >= 0)[0]
    h2_indices = np.where(dot_products < 0)[0]
    if len(h1_indices) == 0 or len(h2_indices) == 0: return 0
    power_h1 = np.var(simulated_cmb[h1_indices])
    power_h2 = np.var(simulated_cmb[h2_indices])
    
    if (power_h1 + power_h2) == 0: return 0
    return (power_h1 - power_h2) / (power_h1 + power_h2)

def objective_function(smoothing_factor, lambda_val, initial_fluctuations, grid_coords, phase):
    # We now target the absolute value
    simulated_A = run_simulation_for_asymmetry(smoothing_factor, lambda_val, initial_fluctuations, grid_coords, phase)
    return np.abs(simulated_A) - TARGET_ASYMMETRY_MAGNITUDE

# --- 3. Main Execution Block ---
if __name__ == "__main__":
    print("Verifying the Unification Principle of Inverse Potency: S * λ = k")
    print("-" * 70)
    
    initial_fluctuations = np.random.randn(GRID_SIZE, GRID_SIZE)
    x = np.linspace(-10, 10, GRID_SIZE)
    y = np.linspace(-10, 10, GRID_SIZE)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    grid_coords = (X, Y, R)
    
    # Generate a random phase for this entire verification run
    phase = np.random.uniform(0, 2 * np.pi)
    print(f"Using a random simulation phase of {phase:.3f} radians.")

    results = []

    for lambda_val in LAMBDA_TEST_VALUES:
        start_time = time.time()
        print(f"\nTesting for λ = {lambda_val:.4f}...")
        
        expected_S = 1.0 / lambda_val
        search_bracket = [expected_S * 0.1, expected_S * 5.0] # Widen the bracket
        
        try:
            calibrated_S = brentq(
                objective_function,
                a=search_bracket[0],
                b=search_bracket[1],
                args=(lambda_val, initial_fluctuations, grid_coords, phase),
                xtol=1e-2,
                rtol=1e-2
            )
            k = calibrated_S * lambda_val
            results.append({'lambda': lambda_val, 'S': calibrated_S, 'k': k})
            duration = time.time() - start_time
            print(f"  SUCCESS: Found S = {calibrated_S:.2f} in {duration:.1f}s.  => k = {k:.4f}")
            
        except ValueError:
            duration = time.time() - start_time
            print(f"  FAILED: Could not find a solution for S in {duration:.1f}s.")
        
    print("\n--- Verification Complete ---")
    print("λ (Potency) | S (Smoothness) | k = S * λ (Principle Constant)")
    print("------------|----------------|---------------------------------")
    for res in results:
        print(f"  {res['lambda']:.4f}    |    {res['S']:.2f}      |    {res['k']:.4f}")

    if len(results) > 1:
        k_values = [res['k'] for res in results]
        mean_k = np.mean(k_values)
        std_k = np.std(k_values)
        print("\nStatistical Analysis of k:")
        print(f"  Mean Value of k: {mean_k:.4f}")
        print(f"  Standard Deviation of k: {std_k:.4f}")
        if std_k / mean_k < 0.1:
            print("\nCONCLUSION: The Unification Principle is computationally verified.")
            print("The value of k = S * λ remains approximately constant across different universal parameters.")
        else:
            print("\nCONCLUSION: The Unification Principle is not verified by this test.")
            print("The value of k = S * λ varies significantly.") 