import jax
import jax.numpy as jnp
from jax import grad, jit, vmap, pmap, tree_map, value_and_grad
import jax.lax as lax
from jax.experimental.ode import odeint
import jax.scipy.integrate as jintegrate
from functools import partial
import optax
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from typing import Dict, Tuple, List, Callable, Any, Optional

# Import the division by zero handling library
import dividebyzero as dbz

# Enable JAX debug flags if needed
# jax.config.update('jax_debug_nans', True)
# jax.config.update('jax_disable_jit', True)  # Uncomment for easier debugging

# Check if multiple devices are available
devices = jax.devices()
use_pmap = len(devices) > 1
print(f"JAX devices available: {len(devices)}")
print(f"Using pmap: {use_pmap}")

# Create a dataclass for parameters to get better pytree handling
@dataclass
class ShellParams:
    r0: float = 1.0e-30  # Increased from 1.0e-33 to avoid underflow
    alpha: float = 0.1
    c0: float = 1.0
    beta: float = 0.5
    gamma: float = 2.0
    lambda_ord: float = 0.8
    kappa_minus: float = 1.0e-30  # Increased from 1.0e-50
    omega_jump: float = 100.0
    ordinal_factor: float = 1.5

# Register the dataclass as a pytree node
def _shell_params_flatten(params):
    return (params.r0, params.alpha, params.c0, params.beta, params.gamma, 
            params.lambda_ord, params.kappa_minus, params.omega_jump, params.ordinal_factor), None

def _shell_params_unflatten(aux_data, values):
    return ShellParams(*values)

jax.tree_util.register_pytree_node(
    ShellParams,
    _shell_params_flatten,
    _shell_params_unflatten
)

class JaxTemporalShellCalculator:
    def __init__(self, params: Optional[ShellParams] = None):
        # Initialize parameters
        self.params = params if params is not None else ShellParams()
        
        # Convert params to JAX arrays
        self.params = jax.tree_util.tree_map(jnp.asarray, self.params)
        
        # Physical constants as JAX arrays
        self.G = jnp.array(6.67430e-11)
        self.c = jnp.array(299792458.0)
        self.h_bar = jnp.array(1.05457181764e-34)
        self.l_p = jnp.sqrt(self.h_bar * self.G / jnp.power(self.c, 3))
        self.lambda_observed = jnp.array(1.1056e-52)  # Initialize with a valid value
        
        # Calculation settings
        self.max_finite_shell = 150
        self.transfinite_samples = 100
        
        # Initialize JIT-compiled functions
        self._initialize_jit_functions()
    
    def _initialize_jit_functions(self):
        """Initialize all JIT-compiled functions with proper handling of static arguments"""
        # Pure calculation functions (these don't need self)
        self._pure = {
            'shell_radius': jit(self._shell_radius),
            'coupling_strength': jit(self._coupling_strength),
            'term_value': jit(self._term_value),
            # Use partial to avoid passing constants every time
            'calculate_lambda': jit(
                partial(
                    self._calculate_lambda, 
                    G=self.G, 
                    c=self.c,
                    max_finite_shell=self.max_finite_shell,
                    transfinite_samples=self.transfinite_samples
                )
            ),
        }
        
        # JIT the loss function and its gradient
        self._loss_value_and_grad = jit(
            value_and_grad(
                partial(
                    self._loss_function, 
                    lambda_observed=self.lambda_observed,
                    G=self.G,
                    c=self.c,
                    max_finite_shell=self.max_finite_shell,
                    transfinite_samples=self.transfinite_samples
                )
            )
        )
        
        # Create a JIT-compiled update step for optimization
        # The optimizer is specified as a static argument since it's not a JAX array
        self._update_step_jit = jit(self._update_step, static_argnames=['optimizer'])
    
    def debug_lambda_calculation(self):
        """Non-JIT version of calculation for debugging"""
        params = self.params
        
        # Calculate each component separately
        finite = self._calculate_finite_contribution(params, self.max_finite_shell)
        transfinite = self._calculate_transfinite_contribution(
            params, self.max_finite_shell, self.transfinite_samples
        )
        
        # Calculate total and convert to physical units
        total = finite + transfinite
        lambda_physical = total * 8 * jnp.pi * self.G / jnp.power(self.c, 2)
        
        # Print debug information
        print(f"DEBUG: Finite contribution: {float(finite)}")
        print(f"DEBUG: Transfinite contribution: {float(transfinite)}")
        print(f"DEBUG: Total contribution: {float(total)}")
        print(f"DEBUG: Lambda physical: {float(lambda_physical)}")
        
        return lambda_physical, finite, transfinite
    
    def _shell_radius(self, params: ShellParams, i: jnp.ndarray) -> jnp.ndarray:
        """Pure function for calculating radius of shell i"""
        return params.r0 * jnp.exp(params.alpha * i)
    
    def _coupling_strength(self, params: ShellParams, i: jnp.ndarray, j: jnp.ndarray) -> jnp.ndarray:
        """Pure function for calculating coupling strength"""
        ord_dist = jnp.abs(i - j)
        return params.c0 / (1 + params.beta * jnp.power(ord_dist, params.gamma))
    
    def _term_value(self, params: ShellParams, i: jnp.ndarray, j: jnp.ndarray) -> jnp.ndarray:
        """Pure function for calculating single term using dbz.array for division"""
        # Only calculate for i > j
        def compute_term():
            # Use dbz.array for radius calculations
            r_i = dbz.array(self._shell_radius(params, i))
            r_j = dbz.array(self._shell_radius(params, j))
            c_ij = self._coupling_strength(params, i, j)
            # Use dbz division which handles division by zero properly
            return params.kappa_minus * c_ij / dbz.array(jnp.power(r_i - r_j, 3))
        
        def return_zero():
            return jnp.array(0.0, dtype=jnp.float32)
        
        # Use JAX's conditional primitive instead of Python if
        return lax.cond(i > j, compute_term, return_zero)
    
    def _process_chunk_with_vmap(self, params: ShellParams, i_chunk: jnp.ndarray, j_chunk: jnp.ndarray) -> jnp.ndarray:
        """Process a chunk of indices with vectorization"""
        # Vectorize term value calculation over both dimensions
        batch_term_value = vmap(vmap(lambda i, j: self._term_value(params, i, j)))
        return jnp.sum(batch_term_value(i_chunk, j_chunk))
    
    def _calculate_finite_contribution(
        self, 
        params: ShellParams, 
        max_finite_shell: int
    ) -> jnp.ndarray:
        """Pure function to calculate total finite shell contribution using dbz.array"""
        # Initialize result
        result = 0.0
        
        # Calculate manually with dbz.array for proper division by zero handling
        for i in range(max_finite_shell + 1):
            for j in range(max_finite_shell + 1):
                if i > j:  # Only calculate for i > j
                    # Use dbz.array for radius calculations
                    r_i = dbz.array(params.r0 * jnp.exp(params.alpha * i))
                    r_j = dbz.array(params.r0 * jnp.exp(params.alpha * j))
                    
                    # Calculate coupling strength
                    c_ij = params.c0 / (1 + params.beta * jnp.power(abs(i - j), params.gamma))
                    
                    # Use dbz division which handles division by zero properly
                    denominator = (r_i - r_j)**3
                    term = params.kappa_minus * c_ij / denominator
                    
                    # Convert back to regular float for summation
                    result += float(term)
        
        return result
    
    def _transfinite_integrand(self, params: ShellParams, i: jnp.ndarray, j: jnp.ndarray) -> jnp.ndarray:
        """Pure function for transfinite integrand using dbz division"""
        # Use dbz.array for radius calculations
        r_i = dbz.array(self._shell_radius(params, i))
        r_j = dbz.array(self._shell_radius(params, j))
        c_ij = self._coupling_strength(params, i, j)
        
        # Use dbz division which handles division by zero properly
        denominator = (r_i - r_j)**3
        result = params.kappa_minus * c_ij / denominator
        
        # Convert back to jnp.ndarray
        return jnp.array(float(result))
    
    def _transfinite_contribution_single(
        self, 
        params: ShellParams, 
        j: jnp.ndarray,
        max_finite_shell: int,
        transfinite_samples: int
    ) -> jnp.ndarray:
        """Calculate transfinite contribution for a single j value"""
        i_lower = max_finite_shell + 1
        i_upper = i_lower + params.omega_jump
        
        # Sample points for integration
        samples = jnp.linspace(i_lower, i_upper, transfinite_samples)
        
        # Use vmap for vectorization
        integrand_values = vmap(lambda i: self._transfinite_integrand(params, i, j))(samples)
        
        # Use JAX's integration
        integral = jintegrate.trapezoid(integrand_values, samples)
        
        # Use jax.lax.cond to handle potential NaN values
        return lax.cond(
            jnp.isnan(integral),
            lambda _: jnp.array(0.0),
            lambda _: integral,
            operand=None
        )
    
    def _calculate_transfinite_contribution(
        self, 
        params: ShellParams, 
        max_finite_shell: int,
        transfinite_samples: int
    ) -> jnp.ndarray:
        """Pure function to calculate transfinite contribution"""
        # Use fewer j values for efficiency (every 10th value)
        j_values = jnp.arange(0, max_finite_shell + 1, 10)
        
        # Vectorize calculation over all j_values
        contributions_fn = lambda j: self._transfinite_contribution_single(
            params, j, max_finite_shell, transfinite_samples
        )
        contributions = vmap(contributions_fn)(j_values)
        
        # Sum contributions and handle potential NaNs
        total = jnp.sum(jnp.where(jnp.isnan(contributions), 0.0, contributions))
        return lax.cond(jnp.isnan(total), lambda _: 0.0, lambda _: total, None)
    
    def _calculate_lambda(
        self, 
        params: ShellParams, 
        G: float, 
        c: float,
        max_finite_shell: int,
        transfinite_samples: int
    ) -> jnp.ndarray:
        """Pure function to calculate cosmological constant using dbz.array for safety"""
        # Calculate contributions with dbz safety
        finite_contribution = self._calculate_finite_contribution(params, max_finite_shell)
        transfinite_contribution = self._calculate_transfinite_contribution(
            params, max_finite_shell, transfinite_samples
        )
        
        # Convert to dbz arrays for safe operations
        finite_contribution = dbz.array(finite_contribution)
        transfinite_contribution = dbz.array(transfinite_contribution)
        
        # Total contribution with dbz safety
        total_contribution = finite_contribution + transfinite_contribution
        
        # Convert to physical units using dbz for safety
        G_dbz = dbz.array(G)
        c_dbz = dbz.array(c)
        lambda_physical = total_contribution * 8 * jnp.pi * G_dbz / (c_dbz ** 2)
        
        # Convert back to jnp.ndarray for JAX compatibility
        lambda_value = jnp.array(float(lambda_physical))
        
        # Ensure we don't return negative values
        return jnp.maximum(lambda_value, 1.0e-100)
    
    def _loss_function(
        self, 
        params: ShellParams, 
        lambda_observed: float,
        G: float,
        c: float,
        max_finite_shell: int,
        transfinite_samples: int
    ) -> jnp.ndarray:
        """Pure function for loss calculation using dbz for stability"""
        # Calculate lambda with dbz safety
        lambda_calc = self._calculate_lambda(params, G, c, max_finite_shell, transfinite_samples)
        
        # Convert to dbz arrays for safe division
        lambda_calc_dbz = dbz.array(lambda_calc)
        lambda_observed_dbz = dbz.array(max(lambda_observed, 1.0e-100))
        
        # Calculate ratio with dbz safety
        ratio = lambda_calc_dbz / lambda_observed_dbz
        
        # Calculate log with dbz safety
        log_ratio = dbz.log(ratio)
        
        # Convert back to regular value and take absolute for loss
        loss = jnp.abs(float(log_ratio))
        
        return jnp.where(jnp.isfinite(loss), loss, jnp.array(1.0e10))
    
    def _update_step(self, params, opt_state, optimizer):
        """Pure function for parameter update"""
        # Get loss and gradients
        loss, grads = self._loss_value_and_grad(params)
        
        # Check for invalid gradients (NaN, Inf)
        grads_flat = jax.tree_util.tree_leaves(grads)
        all_finite = jnp.all(jnp.array([jnp.all(jnp.isfinite(g)) for g in grads_flat]))
        
        # Define functions for the two branches of condition
        def update_params(_):
            updates, new_opt_state = optimizer.update(grads, opt_state)
            new_params = optax.apply_updates(params, updates)
            return new_params, new_opt_state, loss
        
        def keep_params(_):
            # Don't update if gradients are invalid
            return params, opt_state, loss
        
        # Use JAX's conditional primitive
        return lax.cond(all_finite, update_params, keep_params, None)
    
    # Public interface methods
    def calculate_lambda(self):
        """Public interface to calculate cosmological constant"""
        return self._pure['calculate_lambda'](self.params)
    
    def optimize_parameters(self, steps=1000, learning_rate=0.01):
        """Optimize parameters using JAX gradient descent without scan"""
        # Initialize optimizer
        optimizer = optax.adam(learning_rate)
        opt_state = optimizer.init(self.params)
        
        # Run a non-JIT calculation for debugging before optimization
        print("\nRunning non-JIT calculation for debugging:")
        lambda_val, finite, transfinite = self.debug_lambda_calculation()
        print(f"Initial lambda before optimization: {float(lambda_val)}")
        
        # Define a single optimization step that doesn't rely on scan
        losses = []
        params = self.params
        
        # Optimization loop
        for i in range(steps):
            params, opt_state, loss = self._update_step_jit(params, opt_state, optimizer)
            losses.append(float(loss))
            
            # Log progress periodically
            if i % 200 == 0 or i < 5:  # Show first few iterations plus periodic updates
                # Run non-JIT version for proper debugging output
                if i % 200 == 0:
                    # Update parameters and run debug calculation
                    self.params = params
                    lambda_value, _, _ = self.debug_lambda_calculation()
                    ratio = lambda_value / self.lambda_observed
                    ratio_str = f"{float(ratio):.4e}" if jnp.isfinite(ratio) else "NaN"
                    print(f"Step {i}, Loss: {float(loss):.4e}, "
                          f"Lambda: {float(lambda_value):.4e}, Ratio: {ratio_str}")
        
        # Update the parameters with the final values
        self.params = params
        
        # Run a final non-JIT calculation for debugging
        print("\nFinal non-JIT calculation for debugging:")
        lambda_val, finite, transfinite = self.debug_lambda_calculation()
        
        return np.array(losses), self.params

def hyperparameter_search(learning_rates, step_counts, rng_key):
    """Perform a grid search over hyperparameters"""
    best_loss = float('inf')
    best_params = None
    best_config = None
    
    for lr in learning_rates:
        for steps in step_counts:
            # Create a new PRNGKey for this run
            subkey, rng_key = jax.random.split(rng_key)
            
            # Initialize a fresh calculator
            calculator = JaxTemporalShellCalculator()
            
            # Run optimization
            print(f"\nTrying lr={lr}, steps={steps}")
            losses, params = calculator.optimize_parameters(steps=steps, learning_rate=lr)
            
            # Check if this is the best so far
            final_loss = float(losses[-1])
            if final_loss < best_loss:
                best_loss = final_loss
                best_params = params
                best_config = (lr, steps)
                print(f"New best: lr={lr}, steps={steps}, loss={best_loss:.4e}")
    
    return best_params, best_config, best_loss

def main():
    # Set a specific random seed for reproducibility
    key = jax.random.PRNGKey(42)
    
    # Create calculator instance
    print("Initializing JAX Temporal Shell Calculator...")
    calculator = JaxTemporalShellCalculator()
    
    # Ensure observed lambda is properly set and non-zero
    calculator.lambda_observed = jnp.array(1.1056e-52)
    print(f"Using observed λ: {float(calculator.lambda_observed):.6e} m^-2")
    
    # Set some reasonable parameters manually to ensure we get non-NaN outputs
    calculator.params.r0 = jnp.array(1.0e-30)
    calculator.params.alpha = jnp.array(0.1)
    calculator.params.kappa_minus = jnp.array(1.0e-30)
    calculator.params.c0 = jnp.array(1.0)
    print("Setting manual parameters to avoid numerical issues")
    
    # Re-initialize JIT functions with the proper values
    calculator._initialize_jit_functions()
    
    # Print initial values using non-jitted debugging function
    print("Computing initial values...")
    initial_lambda, finite, transfinite = calculator.debug_lambda_calculation()
    initial_ratio = initial_lambda / calculator.lambda_observed
    
    print(f"Initial calculated λ: {float(initial_lambda):.6e} m^-2")
    ratio_str = f"{float(initial_ratio):.6e}" if jnp.isfinite(float(initial_ratio)) else "NaN"
    print(f"Initial ratio (calculated/observed): {ratio_str}")
    
    # Option to run hyperparameter search
    run_hyperparam_search = False
    
    if run_hyperparam_search:
        print("\nRunning hyperparameter search...")
        learning_rates = [0.001, 0.005, 0.01, 0.05]
        step_counts = [500, 1000, 2000]
        best_params, (best_lr, best_steps), best_loss = hyperparameter_search(
            learning_rates, step_counts, key
        )
        print(f"\nBest hyperparameters: lr={best_lr}, steps={best_steps}, loss={best_loss:.4e}")
        calculator.params = best_params
    else:
        # Regular optimization with default hyperparameters
        print("\nStarting optimization with JAX...")
        losses, _ = calculator.optimize_parameters(steps=500, learning_rate=0.001)
    
    # Calculate final values using the non-jitted function for clarity
    final_lambda, finite, transfinite = calculator.debug_lambda_calculation()
    final_ratio = final_lambda / calculator.lambda_observed
    
    print("\nOptimization complete!")
    print(f"Final calculated λ: {float(final_lambda):.6e} m^-2")
    print(f"Observed λ: {float(calculator.lambda_observed):.6e} m^-2")
    
    final_ratio_str = f"{float(final_ratio):.6e}" if jnp.isfinite(float(final_ratio)) else "NaN"
    print(f"Final ratio: {final_ratio_str}")
    
    if jnp.isfinite(float(initial_ratio)) and jnp.isfinite(float(final_ratio)):
        improvement = float(initial_ratio) / float(final_ratio)
        print(f"Ratio improvement: {improvement:.2f}x better")
    else:
        print("Ratio improvement: Could not be calculated (NaN values)")
    
    # Print optimized parameters
    print("\nOptimized parameters:")
    for field_name, field_value in calculator.params.__dict__.items():
        print(f"  {field_name}: {float(field_value):.6e}")
    
    # Plot loss curve
    plt.figure(figsize=(10, 6))
    plt.plot(losses)
    plt.yscale('log')
    plt.title('Optimization Progress')
    plt.xlabel('Optimization Step')
    plt.ylabel('Loss Value (log scale)')
    plt.grid(True)
    plt.savefig('jax_optimization_results.png')
    plt.close()
    
    print("\nPlot saved as 'jax_optimization_results.png'")

if __name__ == "__main__":
    main()