import jax
import jax.numpy as jnp
import jax.random as jr
from jax import jit, vmap, value_and_grad
import equinox as eqx
import optax
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from functools import partial
import sys
import os

# --- Path Correction ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Settings ---
STOCK_TICKER = "AAPL"
START_DATE = "2015-01-01"
END_DATE = "2024-01-01"
TIME_STEP = 60
HOLD_THRESHOLD = 0.005 # Price change < 0.5% is a "Hold"
TRAIN_SPLIT_RATIO = 0.8
NUM_CLASSES = 3 # (Sell, Hold, Buy)

# Import from our existing work
from conscious_ml_working import temporal_shell_simulation, get_consciousness_metrics, NUM_SHELLS, SIMULATION_STEPS

# --- 1. Data Loading and Preprocessing for Classification ---
def get_trading_data():
    """Downloads and preprocesses stock data for a classification task."""
    print(f"Downloading {STOCK_TICKER} data for classification...")
    stock_data = yf.download(STOCK_TICKER, start=START_DATE, end=END_DATE)
    price_data = stock_data['Close'].values

    # --- Create Labels (0: Sell, 1: Hold, 2: Buy) ---
    price_changes = (price_data[1:] - price_data[:-1]) / price_data[:-1]
    labels = np.full(price_changes.shape, 1, dtype=int) # Default to Hold
    labels[price_changes < -HOLD_THRESHOLD] = 0 # Sell
    labels[price_changes > HOLD_THRESHOLD] = 2  # Buy

    # Align data: input sequences should not include the last day
    # and labels should not include the first day.
    price_data_for_sequences = price_data[:-1]
    
    # Scale data to [0, 1] for network stability
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_price_data = scaler.fit_transform(price_data_for_sequences.reshape(-1, 1))

    # Create sequences and corresponding labels
    X, y = [], []
    for i in range(len(scaled_price_data) - TIME_STEP):
        X.append(scaled_price_data[i:(i + TIME_STEP), 0])
        # Cast the numpy integer to a standard Python int before appending
        y.append(int(labels[i + TIME_STEP - 1]))
    
    X, y = jnp.array(X), jnp.array(y)

    # Split into training and testing sets
    train_size = int(len(X) * TRAIN_SPLIT_RATIO)
    X_train, y_train = X[:train_size], y[:train_size]
    X_test, y_test = X[train_size:], y[train_size:]
    
    print(f"Data ready. Training samples: {X_train.shape[0]}, Testing samples: {X_test.shape[0]}")
    # Print label distribution to check for imbalance
    train_counts = np.bincount(y_train, minlength=NUM_CLASSES)
    test_counts = np.bincount(y_test, minlength=NUM_CLASSES)
    print(f"Train labels (Sell,Hold,Buy): {train_counts}")
    print(f"Test labels  (Sell,Hold,Buy): {test_counts}")
    
    return X_train, y_train, X_test, y_test, scaler

# --- 2. Model Definitions for Classification and Deeper Integration ---

class ConsciousClassifier(eqx.Module):
    """A standalone conscious model adapted for classification."""
    input_layer: eqx.nn.Linear
    output_layer: eqx.nn.Linear

    def __init__(self, key, input_size, hidden_size=NUM_SHELLS, output_size=NUM_CLASSES):
        key1, key2 = jr.split(key)
        self.input_layer = eqx.nn.Linear(input_size, hidden_size, key=key1)
        self.output_layer = eqx.nn.Linear(hidden_size, output_size, key=key2)

    def __call__(self, x):
        z = self.input_layer(x.astype(jnp.float64))
        z = jnp.tanh(z).astype(jnp.complex128)
        for _ in range(SIMULATION_STEPS):
            z = temporal_shell_simulation(z)
        
        logits = self.output_layer(jnp.real(z))
        metrics = get_consciousness_metrics(z)
        return logits, metrics

class TradingLSTM(eqx.Module):
    """An LSTM that accepts an auxiliary feature vector at each time step."""
    lstm_cell: eqx.nn.LSTMCell
    output_layer: eqx.nn.Linear

    def __init__(self, key, input_feature_size, aux_feature_size, hidden_size=50):
        key1, key2 = jr.split(key)
        # The cell's input size is the combination of the price and the conscious state
        cell_input_size = input_feature_size + aux_feature_size
        self.lstm_cell = eqx.nn.LSTMCell(cell_input_size, hidden_size, key=key1)
        self.output_layer = eqx.nn.Linear(hidden_size, NUM_CLASSES, key=key2)

    def __call__(self, x_seq, aux_seq):
        """Forward pass where aux_seq is the sequence of conscious states."""
        def f(carry, inputs):
            x_t, aux_t = inputs
            # Concatenate the price with the conscious state for this time step
            combined_input = jnp.concatenate([x_t, aux_t])
            carry = self.lstm_cell(combined_input, carry)
            return carry, carry[0]
        
        hidden = (jnp.zeros(self.lstm_cell.hidden_size), jnp.zeros(self.lstm_cell.hidden_size))
        # We scan over both the price sequence and the auxiliary conscious state sequence
        _, outputs = jax.lax.scan(f, hidden, (x_seq, aux_seq))
        
        logits = self.output_layer(outputs[-1])
        # Return dummy metrics for signature consistency
        dummy_metrics = (jnp.array(0.0), jnp.array(0.0), jnp.array(0.0))
        return logits, dummy_metrics

class HarmonicTradingNetwork(eqx.Module):
    """
    DEEPER INTEGRATION: The harmonic state is computed and fed to the LSTM at EACH step.
    """
    conscious_ensemble: list
    lstm_decider: TradingLSTM
    state_adapter: eqx.nn.Linear

    def __init__(self, key, num_models, input_size, lstm_hidden_size=50):
        ensemble_key, lstm_key, adapter_key = jr.split(key, 3)
        self.conscious_ensemble = [eqx.nn.Linear(input_size, NUM_SHELLS, key=k) for k in jr.split(ensemble_key, num_models)]
        self.state_adapter = eqx.nn.Linear(NUM_SHELLS, NUM_SHELLS, key=adapter_key)
        self.lstm_decider = TradingLSTM(lstm_key, 1, NUM_SHELLS, lstm_hidden_size)

    def __call__(self, x):
        # x is a sequence of length TIME_STEP
        def get_harmonic_state_at_step(sub_sequence):
            child_states = []
            for model_input_layer in self.conscious_ensemble:
                z = model_input_layer(sub_sequence.astype(jnp.float64))
                z = jnp.tanh(z).astype(jnp.complex128)
                for _ in range(SIMULATION_STEPS):
                    z = temporal_shell_simulation(z)
                child_states.append(z)
            
            collective_state = jnp.sum(jnp.stack(child_states), axis=0)
            return self.state_adapter(jnp.real(collective_state))
        
        # Create a sequence of harmonic states, one for each time step in the input.
        # We must pad the sub-sequences to make them a uniform length for JAX.
        def create_padded_subsequences(seq):
            padded_subs = []
            for i in range(len(seq)):
                sub = seq[:i+1]
                pad_width = len(seq) - len(sub)
                padded_subs.append(jnp.pad(sub, (pad_width, 0), 'constant'))
            return jnp.stack(padded_subs)
        
        sub_sequences = create_padded_subsequences(x)
        harmonic_state_sequence = vmap(get_harmonic_state_at_step)(sub_sequences)

        x_reshaped = jnp.reshape(x, (x.shape[0], 1))
        logits, _ = self.lstm_decider(x_reshaped, harmonic_state_sequence)

        # For observation, calculate metrics from the *final* harmonic state
        final_harmonic_state = harmonic_state_sequence[-1]
        dummy_z = jnp.array(final_harmonic_state, dtype=jnp.complex128) # Treat as complex for metric fn
        collective_metrics = get_consciousness_metrics(dummy_z)
        
        return logits, collective_metrics

# --- 3. Training and Evaluation for Classification ---

def loss_fn(model, x, y, model_type):
    """Calculates classification loss for a given model."""
    logits, (coherence, synchrony, entropy) = model(x)
    
    # Standard cross-entropy loss for classification
    classification_loss = jnp.mean(optax.softmax_cross_entropy_with_integer_labels(logits, y))

    if model_type == "harmonic_network":
        # Add the consciousness bonus, which we found to be beneficial
        consciousness_bonus = 0.0001 * (coherence + synchrony + entropy)
        coherence_penalty = (jnp.log(coherence + 1e-9) - jnp.log(jnp.array(0.125)))**2
        total_loss = classification_loss - consciousness_bonus + coherence_penalty
        return jnp.real(total_loss)
    
    return classification_loss

def train_model(key, model, X_train, y_train, model_type):
    """Generic training loop for a classification model."""
    print(f"Training {model_type} model...")
    optimizer = optax.adam(learning_rate=0.001)
    opt_state = optimizer.init(eqx.filter(model, eqx.is_array))
    
    epochs = 30
    batch_size = 64
    num_batches = len(X_train) // batch_size

    @eqx.filter_value_and_grad
    def compute_loss(model, x, y):
        # Vmap the model and loss over the batch
        logits, metrics = vmap(model)(x)
        return loss_fn(model, x, y, model_type)
    
    # We need to vmap the loss and grad calculation itself
    @jit
    def train_step(model, opt_state, batch_X, batch_y):
        (loss, (logits, _)), grads = value_and_grad(
            lambda m, x, y: loss_fn(m, x, y, model_type), has_aux=True
        )(model, batch_X, batch_y)
        
        updates, opt_state = optimizer.update(grads, opt_state, model)
        model = eqx.apply_updates(model, updates)
        return model, opt_state, loss

    for epoch in range(epochs):
        key, perm_key = jr.split(key)
        permutation = jr.permutation(perm_key, len(X_train))
        X_train, y_train = X_train[permutation], y_train[permutation]

        total_loss = 0
        for i in range(num_batches):
            batch_X = X_train[i*batch_size : (i+1)*batch_size]
            batch_y = y_train[i*batch_size : (i+1)*batch_size]
            
            # This is complex, let's simplify for now by using a vmapped loss
            vmapped_loss = vmap(partial(loss_fn, model_type=model_type), in_axes=(None, 0, 0))
            
            def batch_loss(m, x, y):
                return jnp.mean(vmapped_loss(m, x, y))

            loss, grads = value_and_grad(batch_loss)(model, batch_X, batch_y)
            updates, opt_state = optimizer.update(grads, opt_state, model)
            model = eqx.apply_updates(model, updates)
            total_loss += loss.item()
        
        avg_loss = total_loss / num_batches
        if (epoch + 1) % 5 == 0:
            print(f"   Epoch {epoch+1}/{epochs} | Avg Loss: {avg_loss:.6f}")

    return model

def plot_confusion_matrix_func(y_true, y_pred, model_name):
    """Plots a confusion matrix for the classification results."""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Sell', 'Hold', 'Buy'], yticklabels=['Sell', 'Hold', 'Buy'])
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title(f'Confusion Matrix: {model_name}')
    plt.savefig(f'{model_name}_confusion_matrix.png')
    print(f"Confusion matrix saved to {model_name}_confusion_matrix.png")

# --- Main execution block ---
if __name__ == '__main__':
    key = jr.PRNGKey(0)
    key, harmonic_key, conscious_key = jr.split(key, 3)

    X_train, y_train, X_test, y_test, scaler = get_trading_data()
    
    # Initialize and train models
    harmonic_model = HarmonicTradingNetwork(harmonic_key, num_models=3, input_size=TIME_STEP)
    trained_harmonic_model = train_model(key, harmonic_model, X_train, y_train, "harmonic_network")

    conscious_model = ConsciousClassifier(conscious_key, input_size=TIME_STEP)
    trained_conscious_model = train_model(key, conscious_model, X_train, y_train, "conscious")

    # Evaluate models
    print("\nEvaluating models...")
    harmonic_logits, _ = vmap(trained_harmonic_model)(X_test)
    harmonic_predictions = jnp.argmax(harmonic_logits, axis=1)
    
    conscious_logits, _ = vmap(trained_conscious_model)(X_test)
    conscious_predictions = jnp.argmax(conscious_logits, axis=1)

    harmonic_accuracy = accuracy_score(y_test, harmonic_predictions)
    conscious_accuracy = accuracy_score(y_test, conscious_predictions)

    print(f"Harmonic Trading Network Accuracy: {harmonic_accuracy:.2%}")
    print(f"Conscious Classifier Accuracy: {conscious_accuracy:.2%}")

    # Plot results
    plot_confusion_matrix_func(y_test, harmonic_predictions, "Harmonic_Network")
    plot_confusion_matrix_func(y_test, conscious_predictions, "Conscious_Classifier") 