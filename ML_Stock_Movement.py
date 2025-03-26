import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Fetch data
def fetch_data():
    spy = yf.Ticker("SPY").history(period="5y")
    aapl = yf.Ticker("AAPL").history(period="5y")
    data = pd.DataFrame({
        "SPY": spy["Close"],
        "AAPL": aapl["Close"]
    }).dropna()
    return data

# Train model
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
def plot_results(X_test, y_test, y_pred):
    plt.figure(figsize=(12, 6))

    # Scatter Plot: Actual vs Predicted
    plt.subplot(1, 2, 1)
    plt.scatter(y_test, y_pred, color="red", alpha=0.5, label="Predicted vs Actual")
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)  # 45-degree line
    plt.xlabel("Actual SPY Prices")
    plt.ylabel("Predicted SPY Prices")
    plt.title("Scatter: Actual vs Predicted SPY Prices")
    plt.legend()

    # Time Series Plot
    plt.subplot(1, 2, 2)
    sorted_indices = np.argsort(X_test.values.flatten())  # Sort for proper visualization
    plt.plot(X_test.iloc[sorted_indices], y_test.iloc[sorted_indices], label="Actual SPY", color="blue")
    plt.plot(X_test.iloc[sorted_indices], np.array(y_pred)[sorted_indices], label="Predicted SPY", color="red", linestyle="dashed")
    plt.xlabel("AAPL Prices")
    plt.ylabel("SPY Prices")
    plt.title("Time Series: Actual vs Predicted SPY Prices")
    plt.legend()

    plt.tight_layout()
    plt.show(block=True)  # Keep the plot open

# Run the script
data = fetch_data()
X = data[["AAPL"]]
y = data["SPY"]

model, X_test, y_test = train_model(X, y)
mse, r2, y_pred = evaluate_model(model, X_test, y_test)

print(f"Mean Squared Error: {mse:.4f}")
print(f"R-squared: {r2:.4f}")

plot_results(X_test, y_test, y_pred)
