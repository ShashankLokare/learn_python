import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from datetime import datetime
import os

# Create a directory to store output Excel files
output_dir = "swing_trade_reports"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Fetch Historical Data
def fetch_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Prepare Data for LSTM
def prepare_data(data, feature='Close', window_size=60):
    data_scaled = MinMaxScaler(feature_range=(0, 1)).fit_transform(data[[feature]])
    
    X, y = [], []
    for i in range(window_size, len(data_scaled)):
        X.append(data_scaled[i-window_size:i, 0])
        y.append(data_scaled[i, 0])
    
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))  # Reshape for LSTM
    return X, y

# Build and Train LSTM Model
def build_and_train_lstm(X_train, y_train, epochs=50, batch_size=32):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))  # Output layer

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)
    
    return model

# Generate Swing Trade Signals
def generate_signals(data, model, window_size=60):
    data_scaled = MinMaxScaler(feature_range=(0, 1)).fit_transform(data[['Close']])
    
    # Prepare test data
    X_test, y_test = [], data_scaled[window_size:, 0]
    for i in range(window_size, len(data_scaled)):
        X_test.append(data_scaled[i-window_size:i, 0])
    
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # Predict
    predicted_prices = model.predict(X_test)
    predicted_prices = MinMaxScaler(feature_range=(0, 1)).fit(data[['Close']]).inverse_transform(predicted_prices)

    # Generate signals based on predicted future price movement
    buy_signals, sell_signals = [], []
    for i in range(1, len(predicted_prices)):
        if predicted_prices[i] > predicted_prices[i-1]:  # Simple rule: Buy if the price is predicted to go up
            buy_signals.append((data.index[i+window_size], predicted_prices[i][0]))
        elif predicted_prices[i] < predicted_prices[i-1]:  # Sell if the price is predicted to go down
            sell_signals.append((data.index[i+window_size], predicted_prices[i][0]))

    return buy_signals, sell_signals

# Estimate Potential Upper Price Movement
def estimate_potential_movement(buy_signals):
    # Assume the potential upper price movement is the highest price predicted in the next 20 days
    if not buy_signals:
        return None, None

    potential_upper_price = max([price for _, price in buy_signals])
    expected_duration = 20  # Assume it takes 20 days to reach this level
    
    return potential_upper_price, expected_duration

# Main Function
def main():
    ticker = 'JUNIORBEES.NS'
    start_date = '2020-01-01'
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Fetch and prepare data
    data = fetch_data(ticker, start_date, end_date)
    if data.empty:
        print(f"No data for {ticker}")
        return
    
    X, y = prepare_data(data)
    
    # Train LSTM model
    model = build_and_train_lstm(X, y)
    
    # Generate trade signals
    buy_signals, sell_signals = generate_signals(data, model)

    # Estimate potential movement
    potential_upper_price, expected_duration = estimate_potential_movement(buy_signals)
    
    # Prepare trade information
    if buy_signals:
        last_buy_date, last_buy_price = buy_signals[-1]
        trade_info = {
            'Ticker': ticker,
            'Last Buy Date': last_buy_date,
            'Close Price': last_buy_price,
            'Potential Upper Price': potential_upper_price,
            'Expected Duration (days)': expected_duration
        }
        print("Potential Swing Trade:")
        print(trade_info)
        create_excel_report(ticker, data, trade_info)
        visualize_data(data, buy_signals, sell_signals)
    else:
        print("No potential swing trades found.")

# Create Excel Report
def create_excel_report(ticker, data, trade_info):
    file_path = os.path.join(output_dir, f"{ticker}_swing_trade_report.xlsx")
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    
    # Save entire dataset
    data.to_excel(writer, sheet_name='Historical Data')
    
    # Save trade info
    trade_df = pd.DataFrame([trade_info])
    trade_df.to_excel(writer, sheet_name='Trade Info', index=False)
    
    writer.save()
    print(f"Excel report created for {ticker}: {file_path}")

# Visualization
def visualize_data(data, buy_signals, sell_signals):
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['Close'], label='Close Price', color='blue')
    
    # Plot buy signals
    for date, price in buy_signals:
        plt.scatter(date, price, color='green', marker='^', alpha=1.0, label='Buy Signal')

    # Plot sell signals
    for date, price in sell_signals:
        plt.scatter(date, price, color='red', marker='v', alpha=1.0, label='Sell Signal')
    
    plt.title('NTPC.NS Price and LSTM Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()