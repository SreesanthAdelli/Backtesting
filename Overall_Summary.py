import pandas as pd

# Load SPY data
df = pd.read_csv('Fixed_Data_SPY_10Y_General.csv', parse_dates=['Date'])
df = df.sort_values('Date')

# Calculate Daily Return
df['Daily Return'] = df['Close/Last'].pct_change()

# Calculate Cumulative Return
df['Cumulative Return'] = (1 + df['Daily Return']).cumprod() - 1

# Calculate Simple Moving Averages (SMA)
df['SMA_20'] = df['Close/Last'].rolling(window=20).mean()  # 20-day SMA
df['SMA_50'] = df['Close/Last'].rolling(window=50).mean()  # 50-day SMA

# Calculate Exponential Moving Averages (EMA)
df['EMA_20'] = df['Close/Last'].ewm(span=20, adjust=False).mean()  # 20-day EMA
df['EMA_50'] = df['Close/Last'].ewm(span=50, adjust=False).mean()  # 50-day EMA

# Calculate Rolling Volatility (Standard Deviation of Daily Returns)
df['Volatility_20'] = df['Daily Return'].rolling(window=20).std()  # 20-day rolling volatility

# Normalized Return for SPY
df['SPY Value Normalized'] = df['Close/Last'] / df['Close/Last'].iloc[0]
# Save to a new CSV file
output_file = 'SPY_Aggregated_Analysis.csv'
df.to_csv(output_file, index=False)

print(f"Aggregated analysis saved to {output_file}")
