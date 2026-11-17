import jax.numpy as jnp
import jax.random as jr
import equinox as eqx
from jax import jit

class LSTM(eqx.Module):
    """
    A standard Long Short-Term Memory (LSTM) network.
    """
    cell: eqx.nn.LSTMCell
    linear: eqx.nn.Linear

    def __init__(self, key, *, input_size, hidden_size):
        cell_key, linear_key = jr.split(key)
        self.cell = eqx.nn.LSTMCell(input_size, hidden_size, key=cell_key)
        self.linear = eqx.nn.Linear(hidden_size, 1, key=linear_key)

    def __call__(self, x):
        """
        Processes a sequence of inputs.
        x shape: (sequence_length, input_size)
        """
        # Initialize the hidden state
        hidden = (
            jnp.zeros((self.cell.hidden_size,)),
            jnp.zeros((self.cell.hidden_size,)),
        )

        # Scan over the sequence
        def f(carry, inp):
            return self.cell(inp, carry), None
        
        final_state, _ = eqx.internal.scan(f, hidden, x)
        
        # Get the hidden state from the final tuple (h, c)
        final_hidden_state = final_state[0]

        # Decode the final hidden state to a single prediction
        return self.linear(final_hidden_state).squeeze()

def create_benchmark_model(key, look_back):
    """
    Factory function to create a new LSTM model.
    """
    input_size = 1  # We have one feature: the closing price
    hidden_size = 50 # A common choice for hidden layer size
    
    print("Creating benchmark LSTM model...")
    model = LSTM(key, input_size=input_size, hidden_size=hidden_size)
    print("Benchmark model created.")
    
    return model

@jit
def benchmark_loss_fn(model, x, y):
    """
    Calculates the Mean Squared Error for the benchmark model.
    We process one sequence at a time.
    """
    pred = model(x)
    return jnp.mean((pred - y) ** 2) 