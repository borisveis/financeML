import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Import the pre-configured settings from your existing Config.py
from Config import config


# Fetch data for all tickers defined in your config
def fetch_data(prediction_settings):
    target = prediction_settings.get('target_ticker')
    features = prediction_settings.get('feature_tickers', [])
    all_tickers = [target] + features

    # Download 5y data as used in your current training set
    print(f"Fetching data for: {all_tickers}...")
    raw_data = yf.download(all_tickers, period="5y")['Close']
    data = raw_data.dropna()

    return data, target, features


# Train multivariate model
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model, X_test, y_test


# Evaluate model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2, y_pred


# Plot results
def plot_results(y_test, y_pred, target_name):
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, color="red", alpha=0.5, label="Predicted vs Actual")

    # 45-degree line representing perfect prediction
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)

    plt.xlabel(f"Actual {target_name} Prices")
    plt.ylabel(f"Predicted {target_name} Prices")
    plt.title(f"Multivariate Regression: {target_name} Price Prediction")
    plt.legend()
    plt.grid(True)
    plt.show(block=True)


# Main execution loop
if __name__ == "__main__":
    # Access the 'prediction_settings' block from the config object parsed by Config.py
    prediction_settings = config.get('prediction_settings', {})

    if not prediction_settings:
        print("Error: 'prediction_settings' not found in config.json.")
    else:
        # 1. Fetch market data using config-driven tickers
        data, target_col, feature_cols = fetch_data(prediction_settings)

        # 2. Define Features (X) and Target (y)
        X = data[feature_cols]
        y = data[target_col]

        # 3. Process Model
        model, X_test, y_test = train_model(X, y)
        mse, r2, y_pred = evaluate_model(model, X_test, y_test)

        # 4. Output Results
        print(f"\n--- Model Performance ---")
        print(f"Target: {target_col}")
        print(f"Features used: {feature_cols}")
        print(f"Mean Squared Error: {mse:.4f}")
        print(f"R-squared: {r2:.4f}")

        # 5. Visualize
        plot_results(y_test, y_pred, target_col)