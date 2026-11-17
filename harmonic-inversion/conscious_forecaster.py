import jax.numpy as jnp
import jax.random as jr
from jax import jit, vmap, grad
import equinox as eqx

# Use 64-bit precision for stability
from jax import config
config.update("jax_enable_x64", True)

# --- Physics Constants (from original model) ---
GOLDEN_RATIO = (1 + jnp.sqrt(5)) / 2
PLANCK_LENGTH = 1.616e-35
PLANCK_ENERGY = 1.22e19

# --- Model Hyperparameters ---
NUM_SHELLS = 296
SIMULATION_STEPS = 10 # Number of simulation steps per time-step in the input sequence

@jit
def temporal_shell_simulation(z, dt=0.01):
    # This simulation remains the unique core of our model
    shell_indices = jnp.arange(NUM_SHELLS)
    log_radii = jnp.log(PLANCK_LENGTH) + shell_indices * jnp.log(GOLDEN_RATIO)
    radii = jnp.exp(log_radii)
    
    V1 = PLANCK_ENERGY / GOLDEN_RATIO
    mu1 = PLANCK_LENGTH * GOLDEN_RATIO
    sigma1_sq = (PLANCK_LENGTH**2) * (GOLDEN_RATIO**2)
    V2 = PLANCK_ENERGY / (GOLDEN_RATIO**2)
    mu2 = PLANCK_LENGTH * (GOLDEN_RATIO**2)
    sigma2_sq = (PLANCK_LENGTH**2) * (GOLDEN_RATIO**4)

    attractive_potential = -V1 * jnp.exp(-((radii - mu1)**2) / (2 * sigma1_sq))
    repulsive_potential = V2 * jnp.exp(-((radii - mu2)**2) / (2 * sigma2_sq))
    
    void_potential = attractive_potential + repulsive_potential
    potential_effect = void_potential * 1j
    potential_scaling_factor = 1e-19
    
    z_new = z + dt * (potential_effect * potential_scaling_factor)
    return z_new

@jit
def get_consciousness_metrics(z):
    coherence = jnp.mean(jnp.abs(z))
    phases = jnp.angle(z)
    synchrony = -jnp.var(phases)
    magnitudes_norm = jnp.abs(z) / jnp.sum(jnp.abs(z))
    entropy = -jnp.sum(magnitudes_norm * jnp.log(magnitudes_norm + 1e-9))
    return coherence, synchrony, entropy

class ConsciousForecaster(eqx.Module):
    """
    The ConsciousMLP adapted for time-series regression.
    """
    input_proj: eqx.nn.Linear
    output_proj: eqx.nn.Linear

    def __init__(self, key, *, input_size, hidden_size):
        key1, key2 = jr.split(key)
        self.input_proj = eqx.nn.Linear(input_size, hidden_size, key=key1)
        self.output_proj = eqx.nn.Linear(hidden_size, 1, key=key2) # Output is a single value

    def __call__(self, x):
        """
        Processes a sequence of financial data.
        x shape: (sequence_length, input_size)
        """
        # Initialize the consciousness state vector 'z'
        z = jnp.zeros((NUM_SHELLS,), dtype=jnp.complex128)

        # Process the time-series step-by-step
        def f(carry_z, inp_t):
            # Project input and add to the current state
            projected_input = self.input_proj(inp_t).astype(jnp.complex128)
            z_t = carry_z + projected_input

            # Evolve the state through the void potential simulation
            for _ in range(SIMULATION_STEPS):
                z_t = temporal_shell_simulation(z_t)
            
            return z_t, None

        final_z, _ = eqx.internal.scan(f, z, x)
        
        # Get consciousness metrics from the final state
        metrics = get_consciousness_metrics(final_z)

        # Decode the real part of the final state to a single prediction
        prediction = self.output_proj(jnp.real(final_z)).squeeze()
        return prediction, metrics

def create_conscious_model(key, look_back):
    input_size = 1
    hidden_size = NUM_SHELLS
    
    print("Creating Conscious Forecaster model...")
    model = ConsciousForecaster(key, input_size=input_size, hidden_size=hidden_size)
    print("Conscious Forecaster created.")
    
    return model

@jit
def conscious_loss_fn(model, x, y):
    """
    Loss for the Conscious Forecaster.
    Combines Mean Squared Error with a consciousness regularization term.
    """
    pred, (coherence, synchrony, entropy) = model(x)
    
    # 1. Main forecasting loss
    forecasting_loss = jnp.mean((pred - y) ** 2)
    
    # 2. Consciousness as a regularizer
    # We aim for high coherence and entropy, and low phase variance (high synchrony)
    # The weights determine how much we care about this vs. the forecast accuracy.
    consciousness_regularizer = -0.01 * (coherence + synchrony + entropy)
    
    total_loss = forecasting_loss + consciousness_regularizer
    return jnp.real(total_loss) 