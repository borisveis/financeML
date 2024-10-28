import yfinance as yf
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


# Define the stock symbols
stock_symbols = ['SPY', 'AAPL']  # Example: Apple and Microsoft

# Fetch historical data
data = {}
for symbol in stock_symbols:
    data[symbol] = yf.download(symbol, start='2020-01-01', end='2023-01-01')

# Convert to DataFrame
df_aapl = data['SPY']['Close']
df_msft = data['AAPL']['Close']

# Combine into a single DataFrame
df = pd.DataFrame({'SPY': df_aapl, 'AAPL': df_msft}).dropna()


scaler = MinMaxScaler(feature_range=(0, 1))

# Normalize the data
scaled_data = scaler.fit_transform(df)

# Create sequences for LSTM input
def create_sequences(data, seq_length):
    xs, ys = [], []
    for i in range(len(data) - seq_length):
        x = data[i:i + seq_length]
        y = data[i + seq_length][0]  # Predicting SPY price
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)

seq_length = 10  # Number of previous days to consider
X, y = create_sequences(scaled_data, seq_length)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert to PyTorch tensors
X_train_tensor = torch.FloatTensor(X_train)
y_train_tensor = torch.FloatTensor(y_train).view(-1, 1)
X_test_tensor = torch.FloatTensor(X_test)
y_test_tensor = torch.FloatTensor(y_test).view(-1, 1)


class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])  # Get the last time step's output
        return out

input_size = X_train.shape[2]  # Number of features (2 stocks)
hidden_size = 50  # Number of LSTM units
num_layers = 2    # Number of LSTM layers

model = LSTMModel(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers)


criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

num_epochs = 100

for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

        model.eval()
        with torch.no_grad():
            predictions = model(X_test_tensor)

        # Inverse transform to get actual values back from normalized values
        predicted_prices = scaler.inverse_transform(
            np.concatenate((predictions.numpy(), np.zeros((predictions.shape[0], scaled_data.shape[1] - 1))), axis=1))[
                           :, 0]
        actual_prices = scaler.inverse_transform(
            np.concatenate((y_test.reshape(-1, 1), np.zeros((y_test.shape[0], scaled_data.shape[1] - 1))), axis=1))[:,
                        0]

        # Plotting the results
        plt.figure(figsize=(14, 5))
        plt.plot(actual_prices, label='Actual SPY Prices', color='black')
        plt.plot(predicted_prices, label='Predicted SPY Prices', color='red')
        plt.title('SPY Stock Price Prediction')
        plt.xlabel('Time')
        plt.ylabel('Stock Price')
        plt.legend()
        plt.show()