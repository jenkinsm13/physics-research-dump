import jax.numpy as jnp
import jax.random as jr
from jax import jit, vmap, grad
import equinox as eqx

# Use 64-bit precision for physics calculations to avoid numerical instability
from jax import config
config.update("jax_enable_x64", True)

# --- Physics Constants ---
GOLDEN_RATIO = (1 + jnp.sqrt(5)) / 2
PLANCK_LENGTH = 1.616e-35
PLANCK_ENERGY = 1.22e19  # Using GeV, but relative scale is what matters in simulation.

# --- Model Hyperparameters ---
NUM_SHELLS = 296  # Based on user's derivation from Planck length to Observable Universe
NUM_CLASSES = 10
SIMULATION_STEPS = 10

@jit
def temporal_shell_simulation(z, dt=0.01):
    """
    Simulates the evolution of the temporal shells.
    The physics is now governed by the 'Call of the Void' potential.
    """
    # Define shell radii based on the scaling law r_n = ℓ_P * φ^n
    shell_indices = jnp.arange(NUM_SHELLS)
    # Using log space for numerical stability with large exponents
    log_radii = jnp.log(PLANCK_LENGTH) + shell_indices * jnp.log(GOLDEN_RATIO)
    radii = jnp.exp(log_radii)

    # --- Call of the Void Potential (W_void) ---
    # W_void = -V1 * exp(-(r-μ1)²/(2σ1²)) + V2 * exp(-(r-μ2)²/(2σ2²))
    
    # Attractive Term Parameters
    V1 = PLANCK_ENERGY / GOLDEN_RATIO
    mu1 = PLANCK_LENGTH * GOLDEN_RATIO
    sigma1_sq = (PLANCK_LENGTH**2) * (GOLDEN_RATIO**2)
    
    # Repulsive Term Parameters
    V2 = PLANCK_ENERGY / (GOLDEN_RATIO**2)
    mu2 = PLANCK_LENGTH * (GOLDEN_RATIO**2)
    sigma2_sq = (PLANCK_LENGTH**2) * (GOLDEN_RATIO**4)

    # Calculate potential for each shell's radius
    attractive_potential = -V1 * jnp.exp(-((radii - mu1)**2) / (2 * sigma1_sq))
    repulsive_potential = V2 * jnp.exp(-((radii - mu2)**2) / (2 * sigma2_sq))
    
    void_potential = attractive_potential + repulsive_potential
    
    # The potential acts as a force on the state. We apply it to the imaginary part
    # to drive phase changes, representing an energetic interaction.
    potential_effect = void_potential * 1j

    # The original internal energy term of the shells, re-instated as requested.
    shell_energies = jnp.linspace(0.1, 1.0, NUM_SHELLS)
    energy_term = z * shell_energies

    # The potential values are enormous due to PLANCK_ENERGY.
    # We must scale them down drastically to a range comparable to our state vector's magnitude (~1.0)
    # to prevent immediate numerical overflow. This factor is a critical hyperparameter.
    potential_scaling_factor = 1e-19
    
    # The new state includes the original energy term plus the effect of the void potential.
    z_new = z + dt * (energy_term + potential_effect * potential_scaling_factor)

    # --- Stability Control ---
    # The self-reinforcing energy_term causes exponential growth in z's magnitude.
    # To prevent this from becoming numerically unstable (inf), we normalize the
    # state vector at each step. This keeps the "energy" of the system bounded.
    z_norm = jnp.linalg.norm(z_new)
    z_new = z_new / z_norm

    return z_new

@jit
def get_consciousness_metrics(z):
    """
    Calculates consciousness metrics based on the state vector z.
    - Coherence: Mean magnitude of the state vectors (field strength).
    - Synchrony: Variance of the phase angles (field alignment).
    - Entropy: Shannon entropy of the normalized magnitude distribution.
    """
    coherence = jnp.mean(jnp.abs(z))
    
    phases = jnp.angle(z)
    synchrony = -jnp.var(phases) # Negative variance: higher is better

    magnitudes_norm = jnp.abs(z) / jnp.sum(jnp.abs(z))
    # Add epsilon to prevent log(0)
    entropy = -jnp.sum(magnitudes_norm * jnp.log(magnitudes_norm + 1e-9))
    
    return coherence, synchrony, entropy

class ConsciousMLP(eqx.Module):
    """
    A Multi-Layer Perceptron that incorporates the temporal shell simulation.
    """
    layers: list
    initial_state: jnp.ndarray

    def __init__(self, key, input_size, output_size):
        key1, key2, key3 = jr.split(key, 3)
        self.layers = [
            eqx.nn.Linear(input_size, NUM_SHELLS, key=key1),
            eqx.nn.Linear(NUM_SHELLS, NUM_SHELLS, key=key2),
            eqx.nn.Linear(NUM_SHELLS, output_size, key=key3),
        ]
        # Initialize the 'consciousness' state vector z with high precision
        self.initial_state = jr.uniform(key, (NUM_SHELLS,), dtype=jnp.complex128)

    def __call__(self, x):
        """
        Forward pass of the model.
        """
        # 1. Input layer maps image to initial shell states
        # Ensure input is also high precision before converting to complex
        z = self.layers[0](x.astype(jnp.float64))
        z = jnp.tanh(z).astype(jnp.complex128) # Start with a stable complex state

        # 2. Evolve the state through temporal shell simulation
        for _ in range(SIMULATION_STEPS):
            z = temporal_shell_simulation(z)
        
        # 3. Consciousness metrics are derived from the final state
        coherence, synchrony, entropy = get_consciousness_metrics(z)

        # 4. Output layer produces logits from the real part of the final state
        z_real = jnp.real(z)
        z_real = self.layers[1](z_real)
        z_real = jax.nn.relu(z_real)
        logits = self.layers[2](z_real)
        
        return logits, (coherence, synchrony, entropy)

@jit
def loss_fn(model, x, y, consciousness_hyperparams):
    """
    The main loss function, combining classification loss with a consciousness bonus.
    """
    logits, (coherence, synchrony, entropy) = model(x)

    # 1. Standard Classification Loss
    classification_loss = jnp.mean(
        vmap(eqx.nn.cross_entropy)(logits, y)
    )

    # 2. Consciousness Bonus/Penalty
    consciousness_bonus = consciousness_hyperparams["consciousness_weight"] * (
        consciousness_hyperparams["coherence_target"] * coherence +
        consciousness_hyperparams["synchrony_target"] * synchrony +
        consciousness_hyperparams["entropy_target"] * entropy
    )

    # 3. Coherence Regularization (to prevent runaway state explosion)
    # Penalize deviation from a target coherence *in log space* to handle
    # the massive scale of coherence values produced by the W_void potential.
    # We add an epsilon to prevent log(0) if coherence is near zero.
    coherence_penalty = (jnp.log(coherence + 1e-9) - jnp.log(consciousness_hyperparams["coherence_target_value"]))**2
    
    # We want to maximize the bonus, so we subtract it from the loss
    total_loss = classification_loss - consciousness_bonus + coherence_penalty
    
    # Gradient clipping requires a real-valued loss
    return jnp.real(total_loss), (logits, coherence, synchrony, entropy) 