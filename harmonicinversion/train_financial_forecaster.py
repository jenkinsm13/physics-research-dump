import jax
import jax.numpy as jnp
import jax.random as jr
import optax
import equinox as eqx
from tqdm import trange
import matplotlib.pyplot as plt
import numpy as np

# Import our custom modules
from financial_data import prepare_data_for_model
from benchmark_model import create_benchmark_model, benchmark_loss_fn
from conscious_forecaster import create_conscious_model, conscious_loss_fn

# --- Configuration ---
LOOK_BACK = 60
EPOCHS = 20
LEARNING_RATE = 1e-3
BATCH_SIZE = 32

def train_model(model, loss_fn, optimizer, X_train, y_train, key):
    opt_state = optimizer.init(eqx.filter(model, eqx.is_array))
    
    @eqx.filter_jit
    def make_step(model, opt_state, x, y):
        loss, grads = eqx.filter_vmap(eqx.filter_value_and_grad(loss_fn))(model, x, y)
        grads = jax.tree.map(lambda x: jnp.mean(x, axis=0), grads) # Average gradients over the batch
        updates, opt_state = optimizer.update(grads, opt_state, model)
        model = eqx.apply_updates(model, updates)
        return model, opt_state, jnp.mean(loss)

    for epoch in range(EPOCHS):
        # Create batches
        num_batches = len(X_train) // BATCH_SIZE
        perms = jr.permutation(key, len(X_train))
        perms = perms[:num_batches * BATCH_SIZE].reshape((num_batches, BATCH_SIZE))
        
        total_loss = 0
        with trange(num_batches, desc=f"Epoch {epoch+1}/{EPOCHS}", unit="batch") as pbar:
            for perm in pbar:
                batch_x, batch_y = X_train[perm], y_train[perm]
                model, opt_state, loss = make_step(model, opt_state, batch_x, batch_y)
                total_loss += loss.item()
                pbar.set_postfix(loss=f"{loss.item():.4f}")
        
        print(f"Epoch {epoch+1}/{EPOCHS}, Avg Loss: {total_loss / num_batches:.4f}")

    return model

def main():
    # --- 1. Data Preparation ---
    X_train, y_train, X_test, y_test, scaler = prepare_data_for_model(look_back=LOOK_BACK)
    
    # --- 2. Model Initialization ---
    key = jr.PRNGKey(42)
    benchmark_key, conscious_key = jr.split(key)
    
    benchmark_model = create_benchmark_model(benchmark_key, look_back=LOOK_BACK)
    conscious_model = create_conscious_model(conscious_key, look_back=LOOK_BACK)
    
    optimizer = optax.adam(LEARNING_RATE)
    
    # --- 3. Train Benchmark Model ---
    print("\n--- Training Benchmark LSTM Model ---")
    benchmark_model = train_model(benchmark_model, benchmark_loss_fn, optimizer, X_train, y_train, benchmark_key)
    
    # --- 4. Train Conscious Forecaster ---
    print("\n--- Training Conscious Forecaster Model ---")
    conscious_model = train_model(conscious_model, conscious_loss_fn, optimizer, X_train, y_train, conscious_key)
    
    # --- 5. Evaluation ---
    print("\n--- Evaluating Models ---")
    
    # Get predictions
    benchmark_preds = jax.vmap(benchmark_model)(X_test).squeeze()
    conscious_preds, _ = jax.vmap(conscious_model)(X_test)
    conscious_preds = conscious_preds.squeeze()

    # Inverse transform to get actual price values
    benchmark_preds = scaler.inverse_transform(benchmark_preds.reshape(-1, 1))
    conscious_preds = scaler.inverse_transform(conscious_preds.reshape(-1, 1))
    y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))
    
    # Calculate RMSE
    benchmark_rmse = np.sqrt(np.mean((benchmark_preds - y_test_actual)**2))
    conscious_rmse = np.sqrt(np.mean((conscious_preds - y_test_actual)**2))
    
    print(f"Benchmark LSTM RMSE: {benchmark_rmse:.2f}")
    print(f"Conscious Forecaster RMSE: {conscious_rmse:.2f}")

    # --- 6. Plotting Results ---
    plt.figure(figsize=(15, 7))
    plt.title('S&P 500 Price Prediction: Conscious Forecaster vs. LSTM')
    plt.xlabel('Time')
    plt.ylabel('S&P 500 Closing Price (USD)')
    plt.plot(y_test_actual, label='Actual Price', color='blue', alpha=0.7)
    plt.plot(benchmark_preds, label=f'Benchmark LSTM (RMSE: {benchmark_rmse:.2f})', color='orange', linestyle='--')
    plt.plot(conscious_preds, label=f'Conscious Forecaster (RMSE: {conscious_rmse:.2f})', color='red', linestyle='--')
    plt.legend()
    plt.grid(True)
    plt.savefig("financial_forecast_comparison.png")
    print("\nPlot saved to 'financial_forecast_comparison.png'")

if __name__ == "__main__":
    main() 