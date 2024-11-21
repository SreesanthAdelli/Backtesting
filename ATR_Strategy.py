import pandas as pd
import matplotlib.pyplot as plt

# Load the SPY Data (Date, Open, Close, High, Low)

df = pd.read_csv('SPY_Aggregated_Analysis.csv', parse_dates=['Date'])

# Create TR Values

df['TR'] = ((df['High'] - df['Low']) + (df['High'] - df['Close/Last'].shift(1)) + abs(df['Low'] - df['Close/Last'].shift(1)))/3

# Create ATR Values (10-day)

df['ATR - 10 day'] = df['TR'].rolling(window=10).mean()

# Initialize Position and Signals

df['Position'] = 0  # 0 - 1 representing portion of portfolio currently invested
df['Portfolio Value'] = 1 # representing current value of portfolio
df['Cash Value'] = 1 # representing current value of cash
df['Stock Value'] = 0 # representing current value of invested shares


# Set as Float

df['Position'] = df['Position'].astype(float)
df['Portfolio Value'] = df['Portfolio Value'].astype(float)
df['Cash Value'] = df['Cash Value'].astype(float)
df['Stock Value'] = df['Stock Value'].astype(float)


Target_Risk = 1
interest_rate = 0.0005

# Iterate through rows to apply strategy

for i in range (100, len(df)):

    # Accumulate interest on cash every (trading) day
    df.loc[i, 'Cash Value'] = float(df.loc[i - 1, 'Cash Value'] * (1 + interest_rate))

    # Update 'Position' column
    df.loc[i, 'Position'] = float(min(Target_Risk / df.loc[i, 'ATR - 10 day'], 1))

    # Update 'Stock Value' column
    df.loc[i, 'Stock Value'] = float(df.loc[i - 1, 'Stock Value'] * (1 + df.loc[i, 'Daily Return']))

    # Update 'Portfolio Value' column
    df.loc[i, 'Portfolio Value'] = float(df.loc[i, 'Stock Value'] + df.loc[i - 1, 'Cash Value'])
    
    # Update 'Stock Value' again based on 'Position'
    df.loc[i, 'Stock Value'] = float(df.loc[i, 'Position'] * df.loc[i, 'Portfolio Value'])

    # Update 'Cash Value' column
    df.loc[i, 'Cash Value'] = float(df.loc[i, 'Portfolio Value'] - df.loc[i, 'Stock Value'])
    

plt.figure(figsize = (10, 6))
plt.plot(df['Date'], df['Portfolio Value'], label='ATR Strategy Value', color='orange')
plt.plot(df['Date'], df['SPY Value Normalized'], label='SPY Value', color='blue')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.title('SPY vs. Strategy Cumulative Returns')
plt.grid()
plt.show()

# Save to a new CSV file
output_file = 'ATR_Strategy_Results.csv'
df.to_csv(output_file, index=False)

print(f"Strategy Results saved to {output_file}")
