
from datetime import date

from numpy.lib.stride_tricks import as_strided
import process
from numpy.core.fromnumeric import take
import pandas as pd 
import config
import numpy as np 

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import statistics as stats
from OrderManager import OrderManager
import time
import process 
class Strategy():
    
    def __init__(self, orderManager,  take_profit = 10, stop_loss = -4, trade_size = 1):
        self.pnls = []
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.open_pnl = 0
        self.close_pnl = 0
        self.position = 0
        self.real_time_price = 0
        self.real_time_volume = 0
        self.trade_size = trade_size
        self.price =  0
        self.total_buy  = 0
        self.total_sell = 0
        self.buy_quantity = 0 
        self.sell_quantity = 0 
        self.orderManager = orderManager

    def set_real_time_price (self, real_time_price):
        self.real_time_price = real_time_price

    def set_real_time_volume(self, real_time_volume):
        self.real_time_volume = real_time_volume
    def getCurrentPnl(self):
        return self.close_pnl + self.open_pnl

    def calculateOpenPnl(self):
        pass

    def signal(self):
        pass
    
    def BuyOder(self, price, quantity): # I plan that the orderManager will be different when we used differennt account in the sercurtites companyies
      
        self.orderManager.send_buy_order(price, quantity)

    def SellOrder(self, price, quantity):
        self.orderManager.send_sell_order(price, quantity)
    
    def StopLossOrder(self, orderManager): # this code is a speical type one I will code it in the last place
        alphaSignal = self.signal()
        orderManager.send_stop_loss_order('MTL', alphaSignal['price'], alphaSignal['quantity'], )

    def enterLongPosition(self):
        pass
    def enterShortPosition(self):
        pass

    def StopLoss(self ,price, quantity):
        if self.open_pnl  <= self.stop_loss:
            if self.position == 1:
                self.SellOrder(price, quantity)
            elif self.position == -1:
                self.BuyOder( price, quantity)

    def TakeProfit(self,price, quantity):
        if self.open_pnl  >= self.take_profit:
            if self.position == 1:
                self.SellOrder( price, quantity)
            elif self.position == -1:
                self.BuyOder( price, quantity)
# we implement the base strategy with some general characters:

# it must stop-loss and take-profit at some specific points # talk about the close position
# the entry point is based on the entry signal from a specific strattegy
# the exit point is based on the signal of overbought or oversold.
# Any technical analysis requires the price and the volume
# we buy and sell , not depend on the order book to find the best price because the 
class MA20(Strategy):
    def __init__(self, orderManager,dateList, time_interval, periods):
        super().__init__(orderManager)
        self.last_position = 0 # this is a mean reversion strategy then we want to know the last_position
        self.MA = self.get_MAs(dateList, time_interval, periods)
    def get_MAs(self, dateList, time_interval, periods):
        prices = process.process_past_data(dateList, time_interval=time_interval)['Price']
        MA_values = []
        MA_history = []

        for i, price in enumerate(prices):
            MA_values.append(price)
            if len(MA_values) > periods:
                del(MA_values[0])
            MA_value = stats.mean(MA_values)
            MA_history.append(MA_value)
        del(MA_values[0])

        return {'History': MA_history, 'LastMAPrice': MA_values}
    
    def updateStrategy(self, real_time_price, real_time_volume, vnds_real_time):
        
        self.set_real_time_price(real_time_price)
        self.set_real_time_volume(real_time_volume)
        

    def update_MA(self, new_value):
        self.MA['LastMAPrice'].append(new_value)
        self.MA['History'].append(stats.mean(self.MA['LastMAPrice']))
        del(self.MA['LastMAPrice'][0])

    def enterLongPosition(self):
        return self.real_time_price > self.MA['LastMAPrice'][-1] # enter long position
    def enterShortPosition(self):
        return self.real_time_price < self.MA['LastMAPrice'][-1] # enter short position
    def signal(self):
        if self.position == 0:
            if self.enterLongPosition() == 1: # return a dict for sell and buy orders
                self.BuyOder(self.real_time_price + 0.5, 1)
                self.position = 1
            elif self.enterShortPosition() == 1:
                self.position = -1
                self.SellOrder( self.real_time_price  - 0.5, 1) # we set the real_time_price - 0.5 to make sure that the order will match
        elif self.position == 1: # we check the stoploss first before check the take_profit
            self.StopLoss('MTL', 1) # prioritize stoploss with the MTL order
            self.TakeProfit(self.real_time_price + 0.4, 1)
        elif self.position == -1:
            self.StopLoss('MTL', 1) # prioritize stoploss with the MTL order
            self.TakeProfit(self.real_time_price + 0.4, 1)
    
    def getMatchedPrice(self):
        
        if self.orderManager.checkOrderStatus() == 'match':
            currentPrice = self.orderManager.getMatchedPrice().text.replace(',','')
            self.price = float(currentPrice)
            
            return 1
        return -1
    def calculateOpenPnl(self):
        if self.position == 0:
            self.open_pnl = 0
            return 0;
        elif self.position == 1:
            self.open_pnl = self.real_time_price - self.price
            return self.open_pnl
        else:
            self.open_pnl = self.real_time_price - self.price
