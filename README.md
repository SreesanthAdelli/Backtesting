# Backtesting
Framework and code to backtest trading strategies.


#Introduction

I am making this project to test various strategies that I have, mostly for curiousity (nearly impossible to make money this way). I used data from NASDAQ (https://www.nasdaq.com/market-activity/etf/spy/historical). Data is not perfect - does not include many many things, but it is the best way to get free historical data ever since yahoo finance shut down their service :( They used to have an API.

#Raw Data

Downloaded raw data from link above. Data has a format that is incompatible with the backtrader library (specifically the cerebro engine - still don't know how that works), so I made some code (DataFormat.py) that fixes that problem. Lots of code for a small solution - something to learn from in the future.

#Fixed_Data / DataFormat.py

Pandas proves useful once again.

#example.py

This was originally code from the example given by the backtrader library. I changed quite a few things(wasn't working at the time), but most of it is the same. The code doesn't do what it orginally was supposed to, but my experimenting gave me a good enough understanding of the functions I could use and the code was still a good example to show what was possible.

#Overall_Summary.py

I didn't want to hold too much code in one file, so I made 