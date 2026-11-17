import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from astropy.utils.data import download_file

# --- Parameters ---
N_SIMULATIONS = 1000
LMAX = 32 # Maximum multipole to consider

# --- Function for Axis Analysis (from previous script) ---
def get_principal_axes(alm, lmax, l):
    """Calculates the principal axes for a given multipole l."""
    if l == 2: # Quadrupole
        Q = np.zeros((3, 3))
        a20_r = np.real(alm[hp.Alm.getidx(lmax, 2, 0)])
        a21_r, a21_i = np.real(alm[hp.Alm.getidx(lmax, 2, 1)]), np.imag(alm[hp.Alm.getidx(lmax, 2, 1)])
        a22_r, a22_i = np.real(alm[hp.Alm.getidx(lmax, 2, 2)]), np.imag(alm[hp.Alm.getidx(lmax, 2, 2)])

        Q[0, 0] = -a20_r + np.sqrt(6) * a22_r
        Q[1, 1] = -a20_r - np.sqrt(6) * a22_r
        Q[2, 2] = 2 * a20_r
        Q[0, 1] = Q[1, 0] = np.sqrt(6) * a22_i
        Q[0, 2] = Q[2, 0] = -np.sqrt(6) * a21_r
        Q[1, 2] = Q[2, 1] = -np.sqrt(6) * a21_i
        
        eigvals, eigvecs = np.linalg.eigh(Q)
        return eigvecs.T[-1] # Return axis for largest eigenvalue

    elif l == 3: # Octopole
        T = np.zeros(3)
        T[0] = -3*np.sqrt(10)*np.real(alm[hp.Alm.getidx(lmax,3,1)]) + np.sqrt(6)*np.real(alm[hp.Alm.getidx(lmax,3,3)])
        T[1] = -3*np.sqrt(10)*np.imag(alm[hp.Alm.getidx(lmax,3,1)]) - np.sqrt(6)*np.imag(alm[hp.Alm.getidx(lmax,3,3)])
        T[2] = 4*np.real(alm[hp.Alm.getidx(lmax,3,0)]) - 2*np.sqrt(1.5)*np.real(alm[hp.Alm.getidx(lmax,3,2)])
        return T / np.linalg.norm(T)
    else:
        raise ValueError("Analysis only configured for l=2 and l=3")

def analyze_map(cmb_map, lmax):
    """Decomposes a map and returns the dot product of the l=2 and l=3 axes."""
    alm = hp.map2alm(cmb_map, lmax=lmax)
    quad_axis = get_principal_axes(alm, lmax, 2)
    octo_axis = get_principal_axes(alm, lmax, 3)
    return np.abs(np.dot(quad_axis, octo_axis))

# --- 1. Get Real Data and Observed Value ---
print("Acquiring Planck 2018 CMB data and analyzing observed alignment...")
cmb_map_url = 'http://pla.esac.esa.int/pla/aio/product-action?MAP.MAP_ID=COM_CMB_IQU-smica_2048_R3.00_full.fits'
cmb_map_file = download_file(cmb_map_url, cache=True)
planck_map = hp.read_map(cmb_map_file, field=0)
nside = hp.get_nside(planck_map)

# Get the observed power spectrum to generate simulations
observed_alm = hp.map2alm(planck_map, lmax=LMAX)
observed_cls = hp.alm2cl(observed_alm)

# Calculate the dot product for the actual observed data
observed_dot_product = analyze_map(planck_map, LMAX)
print(f"Observed dot product: {observed_dot_product:.4f}")

# --- 2. Run Monte Carlo Simulations ---
print(f"\nRunning {N_SIMULATIONS} Monte Carlo simulations...")
sim_dot_products = []
for i in range(N_SIMULATIONS):
    # Generate a random isotropic map with the same power spectrum as the observed data
    sim_map = hp.synfast(observed_cls, nside=nside, lmax=LMAX, verbose=False)
    
    # Analyze the simulated map
    dot_product = analyze_map(sim_map, LMAX)
    sim_dot_products.append(dot_product)
    
    if (i + 1) % 100 == 0:
        print(f"  ... completed {i + 1}/{N_SIMULATIONS} simulations.")

sim_dot_products = np.array(sim_dot_products)

# --- 3. Calculate p-value ---
# The p-value is the fraction of simulations with a dot product as large or larger than observed
p_value = np.sum(sim_dot_products >= observed_dot_product) / N_SIMULATIONS

print("\n--- Statistical Analysis Results ---")
print(f"Observed Quadrupole-Octopole alignment (dot product): {observed_dot_product:.4f}")
print(f"Number of simulations: {N_SIMULATIONS}")
print(f"Simulations with higher alignment: {np.sum(sim_dot_products >= observed_dot_product)}")
print(f"p-value: {p_value:.4f}")

# --- 4. Interpretation & Visualization ---
print("\n--- Interpretation ---")
if p_value < 0.05:
    print("The observed alignment is statistically significant (p < 0.05).")
    print("This result disfavors the null hypothesis of a perfectly isotropic universe.")
else:
    print("The observed alignment is not statistically significant (p >= 0.05).")
    print("This result is consistent with random fluctuations in an isotropic universe.")

plt.figure(figsize=(10, 6))
plt.hist(sim_dot_products, bins=50, density=True, label=f'Isotropic Universe Simulations (N={N_SIMULATIONS})')
plt.axvline(observed_dot_product, color='r', linestyle='--', linewidth=2, label=f'Observed Value ({observed_dot_product:.4f})')
plt.title('CMB Quadrupole-Octopole Alignment: Observed vs. Simulated')
plt.xlabel('Alignment Dot Product |v_q . v_o|')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True, alpha=0.5)
plt.savefig('p_value_analysis.png')
print("\nGenerated histogram plot: p_value_analysis.png") 