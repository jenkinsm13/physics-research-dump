import jax
import jax.numpy as jnp
import jax.random as jr
from jax import jit, vmap, grad, value_and_grad
import equinox as eqx
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
from functools import partial
import sys
import os
import optax # Import the new optimizer library

# --- Path Correction ---
# Add the parent directory to the system path to allow importing 'conscious_ml_working'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Settings ---
STOCK_TICKER = "AAPL"
START_DATE = "2015-01-01"
END_DATE = "2024-01-01"
TIME_STEP = 60 # Use 60 days of data to predict the next day
TRAIN_SPLIT_RATIO = 0.8

# Import from our existing work
from conscious_ml_working import temporal_shell_simulation, get_consciousness_metrics, NUM_SHELLS, SIMULATION_STEPS

# --- 1. Data Loading and Preprocessing ---
def get_stock_data():
    """Downloads and preprocesses the stock data."""
    print(f"Downloading {STOCK_TICKER} data...")
    stock_data = yf.download(STOCK_TICKER, start=START_DATE, end=END_DATE)
    price_data = stock_data['Close'].values.reshape(-1, 1)

    # Scale data to [0, 1] for network stability
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_price_data = scaler.fit_transform(price_data)

    # Create training and test datasets
    train_size = int(len(scaled_price_data) * TRAIN_SPLIT_RATIO)
    train_data = scaled_price_data[:train_size]
    test_data = scaled_price_data[train_size - TIME_STEP:] # Overlap for sequence creation

    def create_dataset(dataset):
        X, y = [], []
        for i in range(len(dataset) - TIME_STEP):
            X.append(dataset[i:(i + TIME_STEP), 0])
            y.append(dataset[i + TIME_STEP, 0])
        return jnp.array(X), jnp.array(y)

    X_train, y_train = create_dataset(train_data)
    X_test, y_test = create_dataset(test_data)

    print(f"Data ready. Training samples: {X_train.shape[0]}, Testing samples: {X_test.shape[0]}")
    
    return X_train, y_train, X_test, y_test, scaler

# --- 2. Model Definitions ---

class ConsciousForecaster(eqx.Module):
    """Our ConsciousMLP adapted for time-series forecasting."""
    input_layer: eqx.nn.Linear
    output_layer: eqx.nn.Linear

    def __init__(self, key, input_size, hidden_size=NUM_SHELLS, output_size=1):
        key1, key2 = jr.split(key)
        self.input_layer = eqx.nn.Linear(input_size, hidden_size, key=key1)
        self.output_layer = eqx.nn.Linear(hidden_size, output_size, key=key2)

    def __call__(self, x):
        """Forward pass for forecasting."""
        # 1. Input layer maps the time-series window to an initial complex state
        z = self.input_layer(x.astype(jnp.float64))
        z = jnp.tanh(z).astype(jnp.complex128)

        # 2. Evolve the state using the W_void physics
        for _ in range(SIMULATION_STEPS):
            z = temporal_shell_simulation(z)
        
        # 3. Get consciousness metrics from the final state
        coherence, synchrony, entropy = get_consciousness_metrics(z)

        # 4. Output layer produces a price prediction from the real part of the state
        prediction = self.output_layer(jnp.real(z))
        
        return prediction.squeeze(), (coherence, synchrony, entropy)

class LSTM_Benchmark(eqx.Module):
    """A standard LSTM model for comparison."""
    lstm_cell: eqx.nn.LSTMCell
    output_layer: eqx.nn.Linear
    
    def __init__(self, key, input_size, hidden_size=50, output_size=1):
        key1, key2 = jr.split(key)
        self.lstm_cell = eqx.nn.LSTMCell(input_size, hidden_size, key=key1)
        self.output_layer = eqx.nn.Linear(hidden_size, output_size, key=key2)

    def __call__(self, x, initial_state=None):
        """Forward pass for the LSTM. Can be initialized with a specific state."""
        # Scan the LSTM cell over the input sequence
        def f(carry, inp):
            carry = self.lstm_cell(inp, carry)
            return carry, carry[0]
        
        # Initialize hidden state and cell state, or use the provided one
        if initial_state is None:
            hidden = (jnp.zeros(self.lstm_cell.hidden_size), jnp.zeros(self.lstm_cell.hidden_size))
        else:
            hidden = initial_state

        _, outputs = jax.lax.scan(f, hidden, x)
        
        # Take the final output to make a prediction
        prediction = self.output_layer(outputs[-1])

        # Return dummy consciousness metrics for consistent function signatures
        dummy_metrics = (jnp.array(0.0), jnp.array(0.0), jnp.array(0.0))
        return prediction.squeeze(), dummy_metrics

class HybridModel(eqx.Module):
    """
    A hybrid model that uses the ConsciousForecaster's state to initialize the LSTM.
    """
    conscious_part: ConsciousForecaster
    lstm_part: LSTM_Benchmark
    state_adapter: eqx.nn.Linear

    def __init__(self, key, input_size, conscious_hidden_size=NUM_SHELLS, lstm_hidden_size=50):
        conscious_key, lstm_key, adapter_key = jr.split(key, 3)
        
        self.conscious_part = ConsciousForecaster(conscious_key, input_size, conscious_hidden_size)
        self.lstm_part = LSTM_Benchmark(lstm_key, 1, lstm_hidden_size) # LSTM processes one feature (price) at a time
        
        # This linear layer adapts the conscious state size to the LSTM hidden state size
        self.state_adapter = eqx.nn.Linear(conscious_hidden_size, lstm_hidden_size, key=adapter_key)

    def __call__(self, x):
        """Forward pass for the hybrid model."""
        # 1. Get the 'conscious' state vector (z) from the input series
        # Note: The original ConsciousForecaster __call__ returns a prediction and metrics. 
        # We need to adapt it to just give us the state. Let's make a small change there.
        # For now, let's assume it returns the state directly for the hybrid model.
        
        # Let's redefine the conscious part's role here:
        z = self.conscious_part.input_layer(x.astype(jnp.float64))
        z = jnp.tanh(z).astype(jnp.complex128)
        for _ in range(SIMULATION_STEPS):
            z = temporal_shell_simulation(z)
        
        # 2. Adapt the final conscious state to be the LSTM's initial hidden state
        adapted_hidden_state = self.state_adapter(jnp.real(z))
        
        # The LSTM cell state can be initialized to zero
        initial_lstm_state = (adapted_hidden_state, jnp.zeros_like(adapted_hidden_state))
        
        # 3. Feed the original sequence into the LSTM, initialized with the conscious state
        # The LSTM expects input of shape (seq_len, feature_dim)
        x_reshaped = jnp.reshape(x, (x.shape[0], 1))
        prediction, _ = self.lstm_part(x_reshaped, initial_state=initial_lstm_state)
        
        # We still need to return dummy metrics for signature consistency
        dummy_metrics = get_consciousness_metrics(z)
        return prediction, dummy_metrics

class HarmonicNetwork(eqx.Module):
    """
    A network of conscious models that collectively initialize a single LSTM
    through a process of "Harmonic Inversion" (state vector summation).
    """
    conscious_ensemble: list
    lstm_decider: LSTM_Benchmark
    state_adapter: eqx.nn.Linear

    def __init__(self, key, num_models, input_size, conscious_hidden_size=NUM_SHELLS, lstm_hidden_size=50):
        ensemble_key, lstm_key, adapter_key = jr.split(key, 3)
        
        # 1. Create the ensemble of "minds"
        keys = jr.split(ensemble_key, num_models)
        self.conscious_ensemble = [ConsciousForecaster(k, input_size) for k in keys]
        
        # 2. Create the single, shared LSTM for decision making
        self.lstm_decider = LSTM_Benchmark(lstm_key, 1, lstm_hidden_size)
        
        # 3. Create the adapter to map the collective state to the LSTM's hidden state size
        self.state_adapter = eqx.nn.Linear(conscious_hidden_size, lstm_hidden_size, key=adapter_key)

    def __call__(self, x):
        """Forward pass for the Harmonic Network."""
        # Run each conscious model to get its internal state vector z
        # We need the raw state, not the final prediction from the forecaster.
        # This requires running the core logic of the ConsciousForecaster here.
        
        child_states = []
        for model in self.conscious_ensemble:
            z = model.input_layer(x.astype(jnp.float64))
            z = jnp.tanh(z).astype(jnp.complex128)
            for _ in range(SIMULATION_STEPS):
                z = temporal_shell_simulation(z)
            child_states.append(z)
            
        # Harmonic Inversion: Sum the complex state vectors
        # This creates constructive/destructive interference between the "minds"
        collective_state = jnp.sum(jnp.stack(child_states), axis=0)

        # Adapt the collective state to initialize the LSTM decider
        adapted_hidden_state = self.state_adapter(jnp.real(collective_state))
        initial_lstm_state = (adapted_hidden_state, jnp.zeros_like(adapted_hidden_state))

        # Pass the original input through the collectively-initialized LSTM
        x_reshaped = jnp.reshape(x, (x.shape[0], 1))
        prediction, _ = self.lstm_decider(x_reshaped, initial_state=initial_lstm_state)

        # For observation, calculate metrics from the collective state
        collective_metrics = get_consciousness_metrics(collective_state)
        
        return prediction, collective_metrics

# --- 3. Training and Evaluation ---

@partial(jit, static_argnames=("model_type",))
def loss_fn(model, x, y, model_type):
    """Calculates the loss for a given model."""
    pred, (coherence, synchrony, entropy) = model(x)
    
    # Base loss is Mean Squared Error for regression
    regression_loss = jnp.mean((pred - y)**2)

    if model_type == "conscious":
        # Add the consciousness bonus and penalty for our model
        consciousness_bonus = 0.001 * (coherence + synchrony + entropy)
        coherence_penalty = (jnp.log(coherence + 1e-9) - jnp.log(jnp.array(0.125)))**2
        total_loss = regression_loss - consciousness_bonus + coherence_penalty
        return jnp.real(total_loss)
    
    return regression_loss

def train_model(key, model, X_train, y_train, model_type):
    """Generic training loop for a model."""
    print(f"Training {model_type} model...")
    optimizer = optax.adam(learning_rate=0.001)
    # The model is a static argument to the loss function, so we filter it out
    opt_state = optimizer.init(eqx.filter(model, eqx.is_array))
    
    epochs = 30
    batch_size = 64
    num_batches = len(X_train) // batch_size

    # The loss function now handles batches internally with vmap
    @eqx.filter_value_and_grad
    def compute_loss(model, x, y):
        # Vmap the model's forward pass to handle the batch dimension
        preds, (coherences, synchronies, entropies) = vmap(model, in_axes=0, out_axes=0)(x)
        preds = preds.squeeze()

        regression_loss = jnp.mean((preds - y)**2)

        if model_type == "hybrid" or model_type == "harmonic_network":
            # The hybrid model's loss is primarily regression, but we can still
            # add a small consciousness bonus to encourage the internal state
            # to remain "well-behaved" according to our physics.
            consciousness_bonus = 0.0001 * (jnp.mean(coherences) + jnp.mean(synchronies) + jnp.mean(entropies))
            
            mean_coherence = jnp.mean(coherences)
            coherence_penalty = (jnp.log(mean_coherence + 1e-9) - jnp.log(jnp.array(0.125)))**2
            
            total_loss = regression_loss - consciousness_bonus + coherence_penalty
            return jnp.real(total_loss)

        return regression_loss

    for epoch in range(epochs):
        key, perm_key = jr.split(key)
        permutation = jr.permutation(perm_key, len(X_train))
        X_train, y_train = X_train[permutation], y_train[permutation]

        total_loss = 0
        # Iterate over the batch manually
        for i in range(num_batches):
            batch_X = X_train[i*batch_size : (i+1)*batch_size]
            batch_y = y_train[i*batch_size : (i+1)*batch_size]
            
            # The vmapped loss function handles the whole batch efficiently
            loss, grads = compute_loss(model, batch_X, batch_y)
            
            updates, opt_state = optimizer.update(grads, opt_state, model)
            model = eqx.apply_updates(model, updates)
            total_loss += loss.item()
        
        avg_loss = total_loss / num_batches
        if (epoch + 1) % 5 == 0:
            print(f"   Epoch {epoch+1}/{epochs} | Avg Loss: {avg_loss:.6f}")

    return model

def plot_results(scaler, y_test, harmonic_preds, hybrid_preds, lstm_preds):
    """Plots the actual vs predicted stock prices for all three models."""
    plt.figure(figsize=(15, 7))
    plt.title(f'{STOCK_TICKER} Price Prediction: Harmonic Network vs. Single Hybrid vs. LSTM')
    plt.xlabel('Time')
    plt.ylabel('Price (USD)')

    # Un-scale the data for plotting
    y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))
    harmonic_preds_actual = scaler.inverse_transform(harmonic_preds.reshape(-1, 1))
    hybrid_preds_actual = scaler.inverse_transform(hybrid_preds.reshape(-1, 1))
    lstm_preds_actual = scaler.inverse_transform(lstm_preds.reshape(-1, 1))

    plt.plot(y_test_actual, label='Actual Price', color='blue', alpha=0.7)
    plt.plot(harmonic_preds_actual, label='Harmonic Network', color='purple', linestyle='-')
    plt.plot(hybrid_preds_actual, label='Single Hybrid Model', color='green', linestyle='--')
    plt.plot(lstm_preds_actual, label='LSTM Benchmark', color='orange', linestyle=':')
    plt.legend()
    plt.grid(True)
    plt.savefig('harmonic_network_predictions.png')
    print("Plot saved to harmonic_network_predictions.png")

# --- Main execution block ---
if __name__ == '__main__':
    key = jr.PRNGKey(0)
    key, data_key, harmonic_key, hybrid_key, lstm_key = jr.split(key, 5)

    X_train, y_train, X_test, y_test, scaler = get_stock_data()

    # Reshape input for LSTM which expects (seq_len, feature_dim)
    X_train_lstm = jnp.reshape(X_train, (*X_train.shape, 1))
    X_test_lstm = jnp.reshape(X_test, (*X_test.shape, 1))

    # Initialize and train models
    harmonic_model = HarmonicNetwork(harmonic_key, num_models=3, input_size=TIME_STEP)
    trained_harmonic_model = train_model(key, harmonic_model, X_train, y_train, "harmonic_network")
    
    hybrid_model = HybridModel(hybrid_key, input_size=TIME_STEP)
    trained_hybrid_model = train_model(key, hybrid_model, X_train, y_train, "hybrid")

    lstm_model = LSTM_Benchmark(lstm_key, input_size=1, hidden_size=TIME_STEP)
    trained_lstm_model = train_model(key, lstm_model, X_train_lstm, y_train, "lstm")

    # Evaluate models
    print("\nEvaluating models...")
    harmonic_predictions, _ = vmap(trained_harmonic_model)(X_test)
    hybrid_predictions, _ = vmap(trained_hybrid_model)(X_test)
    lstm_predictions, _ = vmap(trained_lstm_model)(X_test_lstm)

    harmonic_rmse = jnp.sqrt(mean_squared_error(y_test, harmonic_predictions))
    hybrid_rmse = jnp.sqrt(mean_squared_error(y_test, hybrid_predictions))
    lstm_rmse = jnp.sqrt(mean_squared_error(y_test, lstm_predictions))

    print(f"Harmonic Network RMSE: {harmonic_rmse:.6f}")
    print(f"Single Hybrid Model RMSE: {hybrid_rmse:.6f}")
    print(f"LSTM Benchmark RMSE: {lstm_rmse:.6f}")

    # Plot results
    plot_results(scaler, y_test, harmonic_predictions, hybrid_predictions, lstm_predictions) 