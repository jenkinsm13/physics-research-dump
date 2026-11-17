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
HOLD_THRESHOLD = 0.005
TRAIN_SPLIT_RATIO = 0.8
NUM_CLASSES = 3

# Import from our original, restored work
from conscious_ml_working import temporal_shell_simulation, get_consciousness_metrics, NUM_SHELLS, SIMULATION_STEPS

# --- 1. Data Loading ---
# (This is identical to trading_agent.py)
def get_trading_data():
    """Downloads and preprocesses stock data for a classification task."""
    print(f"Downloading {STOCK_TICKER} data...")
    stock_data = yf.download(STOCK_TICKER, start=START_DATE, end=END_DATE)
    price_data = stock_data['Close'].values

    price_changes = (price_data[1:] - price_data[:-1]) / price_data[:-1]
    labels = np.full(price_changes.shape, 1, dtype=int)
    labels[price_changes < -HOLD_THRESHOLD] = 0
    labels[price_changes > HOLD_THRESHOLD] = 2

    price_data_for_sequences = price_data[:-1]
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_price_data = scaler.fit_transform(price_data_for_sequences.reshape(-1, 1))

    X, y = [], []
    for i in range(len(scaled_price_data) - TIME_STEP):
        X.append(scaled_price_data[i:(i + TIME_STEP), 0])
        y.append(int(labels[i + TIME_STEP - 1]))
    
    X, y = jnp.array(X), jnp.array(y)

    train_size = int(len(X) * TRAIN_SPLIT_RATIO)
    X_train, y_train = X[:train_size], y[:train_size]
    X_test, y_test = X[train_size:], y[train_size:]
    
    # Print label distribution to check for imbalance
    train_counts = np.bincount(y_train, minlength=NUM_CLASSES)
    print(f"Train labels (Sell,Hold,Buy): {train_counts}")
    
    # --- Calculate Class Weights to Counter Imbalance ---
    class_weights = len(y_train) / (NUM_CLASSES * train_counts)
    print(f"Calculated Class Weights: {class_weights}")

    print("Data ready.")
    return X_train, y_train, X_test, y_test, scaler, jnp.array(class_weights)

# --- 2. Model Definitions ---

class ConsciousClassifier(eqx.Module):
    """Our standalone conscious model for the final showdown."""
    input_layer: eqx.nn.Linear
    output_layer: eqx.nn.Linear

    def __init__(self, key, input_size, hidden_size=NUM_SHELLS, output_size=NUM_CLASSES):
        key1, key2 = jr.split(key)
        self.input_layer = eqx.nn.Linear(input_size, hidden_size, key=key1)
        self.output_layer = eqx.nn.Linear(hidden_size * 2, output_size, key=key2)

    def __call__(self, x):
        z = self.input_layer(x.astype(jnp.float64))
        z = jnp.tanh(z).astype(jnp.complex128)
        for _ in range(SIMULATION_STEPS):
            z = temporal_shell_simulation(z)
        
        z_full_info = jnp.concatenate([jnp.real(z), jnp.imag(z)])
        logits = self.output_layer(z_full_info)
        
        metrics = get_consciousness_metrics(z)
        return logits, metrics

class HarmonicClassifier(eqx.Module):
    """
    The final architecture: A collective of conscious minds making a decision
    via Harmonic Inversion, with no LSTM.
    """
    conscious_ensemble: list
    output_layer: eqx.nn.Linear

    def __init__(self, key, num_models, input_size, hidden_size=NUM_SHELLS):
        ensemble_key, output_key = jr.split(key)
        self.conscious_ensemble = [ConsciousClassifier(k, input_size, hidden_size) for k in jr.split(ensemble_key, num_models)]
        self.output_layer = eqx.nn.Linear(hidden_size * 2, NUM_CLASSES, key=output_key)

    def __call__(self, x):
        child_states = []
        for model in self.conscious_ensemble:
            # Get the raw state `z` from each child model
            z = model.input_layer(x.astype(jnp.float64))
            z = jnp.tanh(z).astype(jnp.complex128)
            for _ in range(SIMULATION_STEPS):
                z = temporal_shell_simulation(z)
            child_states.append(z)
        
        # Harmonic Inversion: Sum the states to get the collective mind state
        collective_state = jnp.sum(jnp.stack(child_states), axis=0)
        
        # Concatenate real and imaginary parts of the collective state.
        collective_full_info = jnp.concatenate([jnp.real(collective_state), jnp.imag(collective_state)])
        logits = self.output_layer(collective_full_info)
        
        collective_metrics = get_consciousness_metrics(collective_state)
        return logits, collective_metrics

# --- 3. Final Showdown Training & Evaluation ---

def loss_fn(model, x, y, class_weights):
    """Calculates classification loss, applying a consciousness bonus and class weights."""
    logits, (coherence, synchrony, entropy) = model(x)
    
    # Weighted cross-entropy loss
    one_hot_labels = jax.nn.one_hot(y, num_classes=NUM_CLASSES)
    weighted_loss = optax.softmax_cross_entropy(logits, one_hot_labels)
    weighted_loss = weighted_loss * class_weights[y]
    classification_loss = jnp.mean(weighted_loss)
    
    # Apply the consciousness bonus to both models to encourage rich internal states
    consciousness_bonus = 0.0001 * (coherence + synchrony + entropy)
    coherence_penalty = (jnp.log(coherence + 1e-9) - jnp.log(jnp.array(0.125)))**2
    
    total_loss = classification_loss - consciousness_bonus + coherence_penalty
    return jnp.real(total_loss)

def train_model(key, model, X_train, y_train, class_weights):
    """Training loop for a conscious classifier."""
    model_name = model.__class__.__name__
    print(f"Training {model_name} model...")
    optimizer = optax.adam(learning_rate=0.001)
    opt_state = optimizer.init(eqx.filter(model, eqx.is_array))
    
    epochs = 30
    batch_size = 64
    num_batches = len(X_train) // batch_size

    @jit
    def train_step(model, opt_state, batch_X, batch_y):
        # Vmap the loss function over the batch, keeping the model and weights fixed
        def batch_loss(m, x, y):
            # Tell vmap to map over x and y, but not the model (m) or weights
            return jnp.mean(vmap(loss_fn, in_axes=(None, 0, 0, None))(m, x, y, class_weights))

        loss_val, grads = value_and_grad(batch_loss)(model, batch_X, batch_y)
        updates, opt_state = optimizer.update(grads, opt_state, model)
        model = eqx.apply_updates(model, updates)
        return model, opt_state, loss_val

    for epoch in range(epochs):
        key, perm_key = jr.split(key)
        permutation = jr.permutation(perm_key, len(X_train))
        X_train, y_train = X_train[permutation], y_train[permutation]

        total_loss = 0
        for i in range(num_batches):
            batch_X = X_train[i*batch_size:(i+1)*batch_size]
            batch_y = y_train[i*batch_size:(i+1)*batch_size]
            
            model, opt_state, loss = train_step(model, opt_state, batch_X, batch_y)
            total_loss += loss.item()
        
        avg_loss = total_loss / num_batches
        if (epoch + 1) % 5 == 0:
            print(f"   Epoch {epoch+1}/{epochs} | Avg Loss: {avg_loss:.6f}")
    return model

def plot_confusion_matrix_func(y_true, y_pred, model_name):
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
    # Correctly split the key for each model's initialization AND training
    key, harmonic_init_key, conscious_init_key, harmonic_train_key, conscious_train_key = jr.split(key, 5)

    X_train, y_train, X_test, y_test, scaler, class_weights = get_trading_data()
    
    # Initialize and train models with their own unique keys
    harmonic_model = HarmonicClassifier(harmonic_init_key, num_models=3, input_size=TIME_STEP)
    trained_harmonic_model = train_model(harmonic_train_key, harmonic_model, X_train, y_train, class_weights)

    conscious_model = ConsciousClassifier(conscious_init_key, input_size=TIME_STEP)
    trained_conscious_model = train_model(conscious_train_key, conscious_model, X_train, y_train, class_weights)

    # Evaluate models
    print("\nEvaluating models...")
    harmonic_logits, _ = vmap(trained_harmonic_model)(X_test)
    harmonic_predictions = jnp.argmax(harmonic_logits, axis=1)
    
    conscious_logits, _ = vmap(trained_conscious_model)(X_test)
    conscious_predictions = jnp.argmax(conscious_logits, axis=1)

    harmonic_accuracy = accuracy_score(y_test, harmonic_predictions)
    conscious_accuracy = accuracy_score(y_test, conscious_predictions)

    print(f"\n--- FINAL RESULTS ---")
    print(f"Harmonic Classifier Accuracy: {harmonic_accuracy:.2%}")
    print(f"Conscious Classifier (Single) Accuracy: {conscious_accuracy:.2%}")

    # Plot results
    plot_confusion_matrix_func(y_test, harmonic_predictions, "Harmonic_Classifier")
    plot_confusion_matrix_func(y_test, conscious_predictions, "Conscious_Classifier") 