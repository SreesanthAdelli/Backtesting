from datetime import datetime
import backtrader as bt

# Create a subclass of Strategy to define the indicators and logic
class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                print(f"Buy signal at {self.datas[0].datetime.date(0)}")
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            print(f"Sell signal at {self.datas[0].datetime.date(0)}")
            self.close()  # close long position

# Create a "Cerebro" engine instance
cerebro = bt.Cerebro()

# Create a data feed from CSV
data = bt.feeds.GenericCSVData(
    dataname=r'C:\Users\sadelli\Documents\GitHub\Backtesting\Fixed_Data_SPY_10Y_General.csv',  # Replace with your CSV file path
    dtformat='%Y-%m-%d',  # Adjust date format if necessary
    timeframe=bt.TimeFrame.Days,
    compression=1,
    openinterest=-1,  # -1 means this column is not present in the data
    nullvalue=0.0,  # Value to fill for missing data
    headers=True,  # Set to True if the CSV has column headers
)

cerebro.adddata(data)  # Add the data feed
cerebro.addstrategy(SmaCross)  # Add the trading strategy
cerebro.run()  # Run the backtest
cerebro.plot()  # Plot the results
