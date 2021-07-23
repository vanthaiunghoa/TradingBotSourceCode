from logging import currentframe
from matplotlib import legend
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import backtest_tool as tool
import string
import time
from bs4.element import SoupStrainer
import pandas as pd
import numpy as np
import re as regex
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from bs4 import BeautifulSoup
import requests
from datetime import date, datetime
import statistics as stats

def process_csv(date_time):

    # define the header and the column name

    df = pd.read_csv('VN30F1M.csv', sep=' ', header=None)

    df.columns = ['time', 'price', 'volume']

    df['price'] = df['price'].str.replace(',', '').astype(float)
    df['volume'] = df['volume'].str.replace(',', '').astype(float)

    # this is the file processing the real time data collected from the protrial
    df['time'] = date_time + df['time']
    for i in range(0, len(df.index)):
        df['time'].loc[i] = datetime.strptime(
            df['time'].loc[i], "%Y-%m-%d %H:%M:%S")

    return df

def convert5minute(datetime_object):

    hour = datetime_object.hour
    minute = datetime_object.minute

    current_time = hour*60 + minute  # the time fram calculate in the minutes
    return int(current_time / 5)  # divide by 5 minute


def convert1minute(datetime_object):
    hour = datetime_object.hour
    minute = datetime_object.minute

    return hour*60 + minute

def convertStringToMinute(timeString, time_interval):
    times = timeString.split(":")
    times = [int(time) for time in times]
    hour, minute, second = times

    return int((hour*60 + minute)/ time_interval)
def convert15minute(datetime_object):
    hour = datetime_object.hour
    minute = datetime_object.minute

    current_time = hour*60 + minute  # the time fram calculate in the minutes
    return int(current_time / 15)

def buy(driver, stock_label, price, quantity):

    stockInput = driver.find_element_by_xpath(
        '/html/body/div/div/div[2]/div/div/div[3]/div[2]/div/div[2]/div/div/input')

    stockInput.send_keys(stock_label)

    priceInput = driver.find_element_by_xpath(
        '/html/body/div/div/div[2]/div/div/div[3]/div[2]/div/div[3]/input')

    priceInput.send_keys(price)

    quantityInput = driver.find_element_by_xpath(
        '/html/body/div/div/div[2]/div/div/div[3]/div[2]/div/div[4]/input')

    quantityInput.send_keys(quantity)

    driver.find_element_by_xpath(
        '/html/body/div/div/div[2]/div/div/div[3]/div[2]/div/div[5]/button[1]').click()


def sell(driver, stock_label, price, quantity):

    stockInput = driver.find_element_by_xpath(
        '/html/body/div/div/div[2]/div/div/div[3]/div[2]/div/div[2]/div/div/input')

    #stockInput.send_keys(stock_label)

    priceInput = driver.find_element_by_xpath(
        '/html/body/div/div/div[2]/div/div/div[3]/div[2]/div/div[3]/input')

    priceInput.send_keys(price)

    quantityInput = driver.find_element_by_xpath(
        '/html/body/div/div/div[2]/div/div/div[3]/div[2]/div/div[4]/input')

    quantityInput.send_keys(quantity)

    driver.find_element_by_xpath(
        '/html/body/div/div/div[2]/div/div/div[3]/div[2]/div/div[5]/button[2]').click()


def stop(driver, stock_label, price, quantity, price_activate, when, action):

    stockInput = driver.find_element_by_xpath(
        '/html/body/div/div/div[2]/div/div/div[3]/div[2]/div/div[2]/div/div/input')

    stockInput.send_keys(stock_label)

    priceInput = driver.find_elememt_by_xpath(
        '/html/body/div/div/div[2]/div/div/div[3]/div[2]/div/div[3]/input')

    priceInput.send_keys(price)

    quantityInput = driver.find_element_by_xpath(
        '/html/body/div/div/div[2]/div/div/div[3]/div[2]/div/div[4]/input')

    quantityInput.send_keys(quantity)

    if (when == '>='):
        greaterTrigger = driver.find_element_by_xpath(
            '/html/body/div/div/div[2]/div/div/div[3]/div[2]/div/div[5]/div[1]/a[2]')
        greaterTrigger.click()
    else:
        lessTrigger = driver.find_element_by_xpath(
            '/html/body/div/div/div[2]/div/div/div[3]/div[2]/div/div[5]/div[1]/a[1]')

        lessTrigger.click()

    if action == 'buy':
        driver.find_elment_by_xpath(
            '/html/body/div/div/div[2]/div/div/div[3]/div[2]/div/div[7]/button[1]').click()

    else:
        driver.find_element_by_xpath(
            '/html/body/div/div/div[2]/div/div/div[3]/div[2]/div/div[7]/button[2]').click()
    
def convertToMinute(datetime_object, time_interval):

    hour = datetime_object.hour
    minute = datetime_object.minute
    
    current_time = hour*60 + minute

    return int(current_time / time_interval)
def checkTimeInterval(number, time_interval, date): # remove the above three functions because of redundancy
    
    number =  number*time_interval
    hour = int(number /60)
    minute = number %60 
    return "{:} {:}:{:}".format(date, hour, minute)
# I am going to optimize my code by combining some funcitons into one smaller function
def getDailyData(csv_file, time_interval):

    # pre processing data loaded from vietstock 
    # contain all the data int the csv format so we need to pre-process them before transforming and analyzing
    df = pd.read_csv(csv_file, usecols=[1,2,3])
    df = df.reindex(index=df.index[::-1])
    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)
    df['Time']  = pd.to_datetime(df['Time'])
    df['VolumeChange'] =  df['Volume'].diff()
    df.loc[0,'VolumeChange'] = df.loc[0, 'Volume'] # assign the value of volume at the ATO 

    time_column = str(time_interval)+'minute'
    df[time_column] = df['Time'].apply(convertToMinute, args = (time_interval,)) # apply needs to match the object in the first parameter
    # if we use the (number) which means the int 
    # then we must pass the (number, ) which means a tuple
    #df['5minute'] = df['Time'].apply(convert5minute)
    #df['15minute'] = df['Time'].apply(convert15minute)
    #df['1minute'] = df['Time'].apply(convert1minute)
    return df

def getAveragePrice(group, args): # we pass args we two parameters time_interval and date
    # we are using a formula applied to price in a group
    
    time_interval, date = args 

    price = (group.Price*group.VolumeChange).sum() / group.VolumeChange.sum()
    volume = group.VolumeChange.sum()
    #value_index = int(group['1minute'].mean()) # aha the groupby summarize the information based on the 1minute column
    # but sitll use the beginning index and reset index later on
    # so we could use the value_index with the 1 minute colume
    time = checkTimeInterval(int(group[str(time_interval)+'minute'].mean()), time_interval, date) # get the time 

    return pd.Series([price, volume,time ],index = ['Price','Volume','TimeInterval'])
def getData1minute(df):
    #new_df = df.groupby(by=['5minute']).aggregate({'Price':'mean', 'VolumeChange':'sum','15minute':"mean",'1minute':'mean'})
    # the code sample before
    # the limite of the aggregate seems prevent us from using the our own function
    # then we should use the apply instead
    return df.groupby(by=['1minute']).apply(getAveragePrice, (1))
def getData5minute(df):
    return df.groupby(by=['5minute']).apply(getAveragePrice, (5))
def getData15minute(df):
    return df.groupby(by=['15minute']).apply(getAveragePrice, (15))

def getDataByTimeInterval(df, time_interval, date):
    group = str(time_interval)+'minute'
    return df.groupby(by=[group]).apply(getAveragePrice,(time_interval, date))

def process_past_data(days, time_interval ):
    days_csv = ['VN30F1M-'+ day +'.csv' for day in days] # convert to csv file name
    merge_df =  pd.DataFrame()
    first_time = 0
    for i, csv_file in enumerate(days_csv):
        df = getDailyData(csv_file, time_interval)
        df = getDataByTimeInterval(df, time_interval = time_interval, date= days[i])
        if first_time == 0:
            merge_df = df
            first_time = 1
        else:
            merge_df = merge_df.append(df)
    merge_df.reset_index(inplace= True)
    return merge_df

def MA_strategy(data,STOP_LOSS = -4,TAKE_PROFIT = 10 ,periods = 20, time_interval = 1): # this fucntion is used for backtest not real-time trading
    """
    Backtest the strategy on a specific time fram without using the real data
    
    Entry: Price above MA
    Cut-loss: 4 points
    Take Profit: 5 points
    Aims: Because the T/p / S/l rate approximate 1 expect win rate > 50 % => Profit
    """
    MA_history = []
    MA_values = []
    MA = 0
    prices = data['Price'].tolist()

    # Define the limit and variables for the trade
    
    TRADING_FEE = 0.38
    open_pnl = 0
    close_pnl  = 0
    total_sell = 0
    total_buy = 0
    buy_quantity = 0
    sell_quantity = 0
    last_buy_date = -1
    last_buy_price = 0
    last_sell_price = 0
    last_signal = -2
    position = 0
    positions = []
    trades = []
    pnls = []
    close_pnls =[]
    profits = []
    losses = []
    trade_size = 1 # trade 1 future contract
    orders = []
    positions = [] # possible positions in the past
    pnls = []
    move = 0 # count number of moves
    for i, price in enumerate(prices):
    
        MA_values.append(price)
        if len(MA_values) > periods:
            del(MA_values[0])
        MA = stats.mean(MA_values)
        MA_history.append(MA)


        len_order_before_trade = len(orders)
        # we have 3 cases buy : buy to stop loss, buy to take profit, and buy to entry
        # we assume we would sell and buy at the lest convienent point
        if position == 0 and i > periods + 1: # we will not enter a trade until the MA is fully calculated based the previous periods

            if price > MA and last_signal != 1:
                orders.append(1)
                close_pnl -= TRADING_FEE
                total_buy = price*trade_size
                buy_quantity += trade_size
                position = 1
                last_signal = 1
                move += 1
            if price  < MA and last_signal != -1: # avoid folowing the trend with 2 simila moves
                close_pnl -= TRADING_FEE
                orders.append(-1)
                total_sell = price*trade_size
                sell_quantity += trade_size
                position = -1
                last_signal = -1 # last_signal used only for the entry part not for the TP or SL parts
                move += 1
        elif position == 1:
            if open_pnl >= TAKE_PROFIT:
                close_pnl += price*buy_quantity  - total_buy
                buy_quantity = 0
                total_buy = 0
                position = 0
                orders.append(-1)

            elif open_pnl <= STOP_LOSS:
                close_pnl += price*buy_quantity  - total_buy
                buy_quantity = 0
                total_buy = 0
                position = 0
                orders.append(-1)

        elif position == -1:
            if open_pnl >= TAKE_PROFIT:
                close_pnl += total_sell - price*sell_quantity
                sell_quantity = 0
                total_sell = 0
                position = 0
                orders.append(1)

            elif open_pnl <= STOP_LOSS:
                close_pnl += total_sell - price*sell_quantity 
                sell_quantity = 0
                total_sell = 0
                position = 0
                orders.append(1)
            
        if len_order_before_trade == len(orders):
            orders.append(0) # means that we don't add any trade at the current price


        if position == 1:
            open_pnl = price*buy_quantity - total_buy
        elif position == -1:
            open_pnl = total_sell - price*sell_quantity
        else:
            open_pnl = 0

        positions.append(position)
        pnls.append(open_pnl + close_pnl) # pnl dynamically updated based on the current position and price
        close_pnls.append(close_pnl) # only close_pnl


    
    return pd.DataFrame({
        'Price':prices,
        'Time':data['TimeInterval'].tolist(),
        'MA': MA_history,
        'Trade':orders,
        'Position':positions,
        'Pnl':pnls,
        'Close_pnl':close_pnls
    })

# Idea the strategy function will have a tuple of parameters, and profit and stoploss parameters

# because the take-profit and stop-loss parameters are used globally for every strategies
temporary_data= pd.DataFrame()


import ipywidgets as widgets
from IPython.display import display

def getBuySellDate(resultBackTest, time_interval):
    
    record ={}
    record['buy'] = [num for num in resultBackTest.Time[resultBackTest.Trade == 1].tolist()]
    record['sell'] = [num for num in resultBackTest.Time[resultBackTest.Trade == -1].tolist()]

    print('Buy: ',record['buy'],"\n")
    print('Sell: ',record['sell'])
    return record
def show_pnl(stop_loss=-4, take_profit=10, periods=20, time_interval=1):
    # track the pnl changes with the take profit and stop/loss

    data= process_past_data(['2021-07-15','2021-07-16','2021-07-19','2021-07-20'],time_interval)
    resultBackTest = MA_strategy(data, stop_loss, take_profit, periods, time_interval)

    ax = resultBackTest['Pnl'].plot(figsize=(20,10), legend=True)

    # loc return the row that sastify the arguement
    ax.plot(resultBackTest.loc[resultBackTest.Trade == 1].index, resultBackTest.Pnl[resultBackTest.Trade == 1], 
            color = 'r', lw = 0, marker='^', markersize=7, label='buy')
    ax.plot(resultBackTest.loc[resultBackTest.Trade == -1].index, resultBackTest.Pnl[resultBackTest.Trade == -1], 
            color = 'g', lw = 0, marker='v', markersize=7, label='sell')
    
    ax.legend()
    
    output = getBuySellDate(resultBackTest, time_interval)
