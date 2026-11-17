import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import jax.numpy as jnp

def get_financial_data(ticker="^GSPC", start_date="2010-01-01", end_date="2023-12-31"):
    """
    Downloads historical stock data for a given ticker.
    """
    print(f"Downloading data for {ticker} from {start_date} to {end_date}...")
    data = yf.download(ticker, start=start_date, end=end_date)
    # We'll use the 'Close' price for our forecasting task.
    closing_prices = data[['Close']].values
    print("Data download complete.")
    return closing_prices

def create_dataset(data, look_back=60):
    """
    Creates time-series sequences from the data.
    For each sequence, the first `look_back` items are features (X)
    and the next item is the label (Y).
    """
    X, Y = [], []
    for i in range(len(data) - look_back):
        a = data[i:(i + look_back), 0]
        X.append(a)
        Y.append(data[i + look_back, 0])
    return np.array(X), np.array(Y)

def prepare_data_for_model(look_back=60):
    """
    Main function to orchestrate data downloading, processing, and splitting.
    """
    # 1. Download data
    raw_data = get_financial_data()

    # 2. Scale data to be between 0 and 1
    # This is crucial for neural network stability.
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(raw_data)

    # 3. Split into training and testing sets
    # We'll use 80% of the data for training and 20% for testing.
    training_data_len = int(len(scaled_data) * 0.8)
    train_data = scaled_data[0:training_data_len, :]
    test_data = scaled_data[training_data_len - look_back:, :]

    # 4. Create sequences
    X_train, y_train = create_dataset(train_data, look_back)
    X_test, y_test = create_dataset(test_data, look_back)

    # 5. Reshape for model input
    # The ConsciousMLP and LSTM will expect input of shape (batch_size, sequence_length, features)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # Convert to JAX arrays
    X_train, y_train = jnp.array(X_train), jnp.array(y_train)
    X_test, y_test = jnp.array(X_test), jnp.array(y_test)
    
    print("Data prepared successfully:")
    print(f"  - X_train shape: {X_train.shape}")
    print(f"  - y_train shape: {y_train.shape}")
    print(f"  - X_test shape: {X_test.shape}")
    print(f"  - y_test shape: {y_test.shape}")

    return X_train, y_train, X_test, y_test, scaler 