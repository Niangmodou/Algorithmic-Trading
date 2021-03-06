'''
Algorithmic-Trading Strategy using Python
Moving Average Convergence/Divergence
Made with love by Modou Niang
'''

import pandas as pd
import numpy as np
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import quandl
import fix_yahoo_finance
import datetime as dt


def get_stock_data(tickers,start_date,end_date):
    '''
    Function takes in a list of stock symbol alongside start date and end date and returns
    a dataframe containing the stock information
    '''
    def data(ticker):
        return (pdr.get_data_yahoo(ticker,start=start_date,end=end_date))

    datas = map(data,tickers)

    return (pd.concat(datas,keys=tickers,names=['Ticker','Data']))

def get_data():
    #Retrieving Apple stock information using quandl and storing result into a dataframe
    aapl = pdr.get_data_yahoo('AAPL',start=dt.datetime(2006,10,1),end=dt.datetime(2012,1,1))
    #aapl = quandl.get('WIKI/AAPL',start_date='2006-10-1',end_date='2012-1-1')

    #Saving information to a csv file
    aapl.to_csv('AppleInfo.csv')

    #Storing daily price difference into a dataframe
    price_diff = aapl['Close'] - aapl['Open']

    #Visualizing Time Series Data
    aapl['Close'].plot(grid=True)
    plt.show()

    #Calculating daily percentage changes
    # Daily returns
    daily_pct_change = daily_close.pct_change()
    # Replace NA values with 0
    daily_pct_change.fillna(0, inplace=True)
    # Inspect daily returns
    print(daily_pct_change)
    # Daily log returns
    daily_log_returns = np.log(daily_close.pct_change()+1)
    # Print daily log returns
    print(daily_log_returns)


def simple_moving_average(stock):
    short_window, long_window = 40,100

    signals = pd.DataFrame(index=stock.index)
    signals['signal'] = 0.0

    #Creating a short simple moving average over the short window
    signals['Short_mAvg'] = stock['Close'].rolling(window=short_window,min_periods=1, center=False).mean()

    #Creating a long simple moving average over the long window
    signals['Long_mAvg'] = stock['Close'].rolling(window=long_window,min_periods=1, center=False).mean()

    #Creates a signal for when the SMA crosses the LMA
    signals['signal'][short_window:] = np.where(signals['Short_mAvg'][short_window:]
                                               > signals['Long_mAvg'][short_window:], 1.0,0.0)

    #Generate Trading orders by taking the difference
    signals['positions'] = signals['signal'].diff()

def backtest(signals,stock):
    initial_capital = 1000000

    positions = pd.DataFrame(index=signals.index).fillna(0.0)

    #Buy 100 shares
    positions['AAPL'] = 100*signals['signal']

    portfolio = positions.multiply(stock['Adj Close'],axis=0)

    pos_difference = positions.diff()

    portfolio['Holdings'] = (positions.multiply(stock['Adj Close'],axis=0)).sum(axis=1)

    portfolio['Cash'] = initial_capital - (pos_difference.multiply(stock['Adj Close'],
                                                                    axis=0)).sum(axis=1).cumsum()

    portfolio['Total'] = portfolio['Cash'] + portfolio['Holdings']

    portfolio['Returns'] = portfolio['Total'].pct_change()

    portfolio.head()

    #Visualizing portfolio value
    # Create a figure
    fig = plt.figure()

    ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')

    # Plot the equity curve in dollars
    portfolio['Total'].plot(ax=ax1, lw=2.)

    ax1.plot(portfolio.loc[signals.positions == 1.0].index,
             portfolio.Total[signals.positions == 1.0],
             '^', markersize=10, color='m')
    ax1.plot(portfolio.loc[signals.positions == -1.0].index,
             portfolio.Total[signals.positions == -1.0],
             'v', markersize=10, color='k')

    # Show the plot
    #plt.show()

def main():

    tickers = ['AAPL','MSFT','IBM','GOOG']

    all_data = get_stock_data(tickers,dt.datetime(2006,10,1),dt.datetime(2012,1,1))

    print(all_data)
    #get_data()
    #simple_moving_average()

main()
