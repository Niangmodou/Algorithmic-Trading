'''
Algorithmic-Trading Strategy using Python
Made with love by Modou Niang
'''

import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import quandl
import datetime as dt


def get_data():

    #Retrieving Apple stock information using quandl and storing result into a datafram
    aapl = pdr.get_data_yahoo('AAPL',start=dt.datetime(2006,10,1),end=dt.datetime(2012,1,1))
    #aapl = quandl.get('WIKI/AAPL',start_date='2006-10-1',end_date='2012-1-1')

    #print(aapl.head())
    #print(aapl.tail())
    #print(aapl.describe())

    #Saving information to a csv file
    aapl.to_csv('AppleInfo.csv')


def main():

    get_data()

main()
