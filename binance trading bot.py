import ccxt
import pandas as pd

# Initialize the exchange object with your API keys
exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
    'enableRateLimit': True,
})

# Define a function to fetch historical price data (OHLCV) for a given symbol and timeframe
def fetch_ohlcv(symbol, timeframe):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Define a function to calculate the moving averages
def calculate_moving_averages(df, short_window, long_window):
    df['short_mavg'] = df['close'].rolling(window=short_window).mean()
    df['long_mavg'] = df['close'].rolling(window=long_window).mean()
    return df

# Define a function to execute buy and sell orders based on the moving averages
def execute_orders(df, amount):
    in_position = False

    for index, row in df.iterrows():
        if row['short_mavg'] > row['long_mavg'] and not in_position:
            print("Buy")
            exchange.create_market_buy_order('BTC/USDT', amount)
            in_position = True
        elif row['short_mavg'] < row['long_mavg'] and in_position:
            print("Sell")
            exchange.create_market_sell_order('BTC/USDT', amount)
            in_position = False

# Set the symbol and timeframe
symbol = 'BTC/USDT'
timeframe = '1h'

# Fetch the historical price data
df = fetch_ohlcv(symbol, timeframe)

# Calculate the moving averages
df = calculate_moving_averages(df, 50, 200)

# Execute the orders
execute_orders(df, 0.01)