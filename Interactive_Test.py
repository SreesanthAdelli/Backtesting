import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button

# Load the aggregated analysis data
df = pd.read_csv('SPY_Aggregated_Analysis.csv', parse_dates=['Date'])

# Function to apply the trading strategy based on input values (inputs being buy_days and sell_days)
def apply_strategy(buy_days, sell_days):
    df['Up_Streak'] = (df['Daily Return'] > 0).astype(int).groupby((df['Daily Return'] <= 0).cumsum()).cumsum()
    df['Down_Streak'] = (df['Daily Return'] < 0).astype(int).groupby((df['Daily Return'] >= 0).cumsum()).cumsum()

    # Initialize position and state
    df['Position'] = 0
    in_position = False

    for i in range(1, len(df)):
        if not in_position and df['Up_Streak'].iloc[i] >= buy_days:
            df.at[i, 'Position'] = 1
            in_position = True
            print(f"Buying on {df['Date'].iloc[i]} at {df['Close/Last'].iloc[i]}")
        elif in_position and df['Down_Streak'].iloc[i] >= sell_days:
            df.at[i, 'Position'] = 0
            in_position = False
            print(f"Selling on {df['Date'].iloc[i]} at {df['Close/Last'].iloc[i]}")
        elif in_position: # Make sure to set Position to long if previously long
            df.at[i, 'Position'] = 1
    # Calculate returns
    df['Strategy Return'] = df['Position'].shift(1) * df['Daily Return']
    df['Cumulative Strategy Return'] = (1 + df['Strategy Return']).cumprod() - 1

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Cumulative Strategy Return'], label='Strategy Cumulative Return', color='orange')
    plt.plot(df['Date'], df['Cumulative Return'], label='SPY Cumulative Return', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.title('SPY vs. Strategy Cumulative Returns')
    plt.grid()
    plt.show()

# Function to get user input and run strategy
def on_submit():
    try:
        buy_days = int(buy_entry.get())
        sell_days = int(sell_entry.get())
        root.destroy()  # Close the dialog box
        apply_strategy(buy_days, sell_days)
    except ValueError:
        print("Please enter valid integer values.")

# Set up the Tkinter dialog box
root = Tk()
root.title("Strategy Input")

Label(root, text="Buy when up for how many days straight:").grid(row=0, column=0)
buy_entry = Entry(root)
buy_entry.grid(row=0, column=1)

Label(root, text="Sell when down for how many days straight:").grid(row=1, column=0)
sell_entry = Entry(root)
sell_entry.grid(row=1, column=1)

Button(root, text="Submit", command=on_submit).grid(row=2, column=0, columnspan=2)

root.mainloop()
