import numpy as np
import healpy as hp
from scipy.ndimage import gaussian_filter
from scipy.optimize import brentq

# --- 1. Foundational Parameters & Constants ---
# V_void potential parameters
r_eq = 5.0
A = 1.0
B = 0.5
alpha = 0.5
beta = 0.2
# Simulation parameters
GRID_SIZE = 1024
NSIDE_OUTPUT = 64
# The empirically observed target value from Planck data
TARGET_ASYMMETRY = -0.0194

# --- 2. V_void Force Function ---
def F_void(r, r_eq, A, B, alpha, beta):
    r_shifted = r - r_eq
    term1 = A * alpha * 2 * r_shifted * np.exp(-alpha * r_shifted**2)
    term2 = -B * beta * 2 * r_shifted * np.exp(-beta * r_shifted**2)
    return term1 - term2

# --- 3. Simulation Core Function ---
def run_simulation_and_get_asymmetry(smoothing_factor, initial_fluctuations, grid_coords):
    """
    Runs one instance of the simulation for a given smoothing_factor
    and returns the resulting asymmetry amplitude.
    """
    X, Y, R = grid_coords
    
    # Modulate fluctuations by the V_void force
    force_map = F_void(R, r_eq, A, B, alpha, beta)
    primordial_map = initial_fluctuations * (1 + force_map)
    
    # Simulate inflation
    smoothed_map = gaussian_filter(primordial_map, sigma=smoothing_factor)
    
    # Project to sphere
    npix_out = hp.nside2npix(NSIDE_OUTPUT)
    pix_indices = np.arange(npix_out)
    lon, lat = hp.pix2ang(NSIDE_OUTPUT, pix_indices, lonlat=True)
    grid_x = np.clip(((lon + 180) / 360 * GRID_SIZE).astype(int), 0, GRID_SIZE - 1)
    grid_y = np.clip(((lat + 90) / 180 * GRID_SIZE).astype(int), 0, GRID_SIZE - 1)
    simulated_cmb = smoothed_map[grid_y, grid_x]
    
    # Analyze asymmetry
    pix_vecs = hp.pix2vec(NSIDE_OUTPUT, pix_indices)
    map_mean = np.mean(simulated_cmb)
    map_fluctuations = simulated_cmb - map_mean
    power_map = map_fluctuations**2
    alm_power = hp.map2alm(power_map, lmax=1)
    a10 = alm_power[hp.Alm.getidx(1, 1, 0)]
    a11 = alm_power[hp.Alm.getidx(1, 1, 1)]
    dx, dy, dz = np.real(a11), -np.imag(a11), np.real(a10)
    asymmetry_axis = np.array([dx, dy, dz])
    asymmetry_axis /= np.linalg.norm(asymmetry_axis)
    dot_products = np.dot(asymmetry_axis, pix_vecs)
    h1_indices = np.where(dot_products >= 0)[0]
    h2_indices = np.where(dot_products < 0)[0]
    
    # Handle rare cases where a hemisphere might be empty
    if len(h1_indices) == 0 or len(h2_indices) == 0:
        return 0 # No asymmetry
        
    power_h1 = np.var(simulated_cmb[h1_indices])
    power_h2 = np.var(simulated_cmb[h2_indices])
    
    if (power_h1 + power_h2) == 0:
        return 0

    return (power_h1 - power_h2) / (power_h1 + power_h2)

# --- 4. Objective Function for Root-Finding ---
def objective_function(smoothing_factor, initial_fluctuations, grid_coords):
    """
    Returns the difference between simulated and target asymmetry.
    The root-finder will find where this function is zero.
    """
    simulated_A = run_simulation_and_get_asymmetry(smoothing_factor, initial_fluctuations, grid_coords)
    print(f"  Testing sigma = {smoothing_factor:.4f} -> A = {simulated_A:.4f}")
    return simulated_A - TARGET_ASYMMETRY

# --- 5. Execution ---
if __name__ == "__main__":
    print("Preparing simulation assets...")
    # Generate one persistent random field to ensure results are comparable
    initial_fluctuations = np.random.randn(GRID_SIZE, GRID_SIZE)
    x = np.linspace(-10, 10, GRID_SIZE)
    y = np.linspace(-10, 10, GRID_SIZE)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    grid_coords = (X, Y, R)

    print("\nCalibrating INFLATION_SMOOTHING_FACTOR to match observed CMB asymmetry...")
    print(f"Target Asymmetry (A) = {TARGET_ASYMMETRY}")
    
    # Bracket for the search [lower_bound, upper_bound]. Based on previous runs,
    # we know the value is > 80.
    search_bracket = [80.0, 200.0]
    
    try:
        calibrated_sigma = brentq(
            objective_function,
            a=search_bracket[0],
            b=search_bracket[1],
            args=(initial_fluctuations, grid_coords),
            xtol=1e-3, # Tolerance for convergence
            rtol=1e-3
        )
        print("\n--- Calibration Complete ---")
        print(f"Successfully calibrated smoothing factor to match observed data.")
        print(f"Calibrated INFLATION_SMOOTHING_FACTOR = {calibrated_sigma:.6f}")
    except ValueError:
        print("\n--- Calibration Failed ---")
        print("The root-finding algorithm failed. The target value may not be within the search bracket.")
        print("Or the function may not cross zero. Please check the bracket and model.")
    except Exception as e:
        print(f"\nAn error occurred during calibration: {e}") 