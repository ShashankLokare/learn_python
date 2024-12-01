import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
import matplotlib.pyplot as plt

# Step 1: Data Collection
def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# List of Indian stocks with >30% growth over the past 3 years (example)
# Replace these with your own criteria
indian_stocks = ['TCS.NS', 'RELIANCE.NS', 'HDFCBANK.NS', 'INFY.NS']  # Example tickers
start_date = '2020-01-01'
end_date = '2023-01-01'

data = {ticker: get_stock_data(ticker, start_date, end_date) for ticker in indian_stocks}

# Step 2: Data Preprocessing
def preprocess_data(df):
    df = df[['Close']].copy()
    df['Return'] = df['Close'].pct_change()
    df.dropna(inplace=True)
    return df

processed_data = {ticker: preprocess_data(data[ticker]) for ticker in indian_stocks}

# Step 3: Feature Engineering
def create_features(df, window_size=30):
    df['MA'] = df['Close'].rolling(window=window_size).mean()
    df['STD'] = df['Close'].rolling(window=window_size).std()
    df['Upper_Band'] = df['MA'] + (df['STD'] * 2)
    df['Lower_Band'] = df['MA'] - (df['STD'] * 2)
    df['RSI'] = compute_rsi(df['Close'])
    df.dropna(inplace=True)
    return df

def compute_rsi(series, period=14):
    delta = series.diff().dropna()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

features_data = {ticker: create_features(processed_data[ticker]) for ticker in indian_stocks}

# Step 4: Model Creation
def create_model(input_shape):
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(32, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer='adam', loss='mse')
    return model

# Step 5: Training and Evaluation
def train_and_evaluate(ticker, df):
    # Prepare data for LSTM model
    X, y = [], []
    window_size = 30

    for i in range(len(df) - window_size):
        X.append(df[['Close', 'MA', 'Upper_Band', 'Lower_Band', 'RSI']].values[i:i + window_size])
        y.append(df['Close'].values[i + window_size])

    X, y = np.array(X), np.array(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train.reshape(-1, X_train.shape[-1])).reshape(X_train.shape)
    X_test = scaler.transform(X_test.reshape(-1, X_test.shape[-1])).reshape(X_test.shape)

    model = create_model((X_train.shape[1], X_train.shape[2]))

    model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test), verbose=1)

    # Evaluate
    predictions = model.predict(X_test)
    
    plt.figure(figsize=(14, 7))
    plt.plot(y_test, label='Actual')
    plt.plot(predictions, label='Predicted')
    plt.title(f'Stock Price Prediction for {ticker}')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

    return model

# Train and evaluate for each stock
for ticker in indian_stocks:
    print(f"Training model for {ticker}")
    model = train_and_evaluate(ticker, features_data[ticker])