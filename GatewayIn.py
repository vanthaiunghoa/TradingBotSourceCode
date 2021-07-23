

from collections import deque
from re import A
from typing import Pattern
import pandas as pd 
import config
import numpy as np 
import time
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import statistics as stats
import process 
PATH=r"C:\Users\ThanhDat\Desktop\worldquant 2021\chromedriver.exe"

protrial_url = "https://protrade-trial.vndirect.com.vn/trang-chu"
class GateWayIn():
    
    def __init__(self):
        
        self.driver = webdriver.Chrome(PATH)
        self.dirver.get(url=protrial_url)
        self.real_time_price = []
        self.real_time_volume = []
        self.real_time = []
        # at first step my bot will only consider the matched price but not consider or analyze the orders
    
    def login(self):
        
        # Login the protrial and start collecting the data
        time.sleep(3)
        checkbox=  self.driver.find_element_by_xpath("/html/body/div/div/div[7]/section/div[2]/div/p/input")
        checkbox.click()
        confirmButton = self.driver.find_element_by_xpath("/html/body/div/div/div[7]/section/div[2]/div/button")
        confirmButton.click()
        time.sleep(2)
        my_username = config.USE_NAME
        my_password = config.PASSWORD
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')

        username.send_keys(my_username)
        password.send_keys(my_password)

    def getMatchedPrice(self):
        real_time_data = float(self.driverdriver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div[2]/div[2]/table/tbody/tr[1]/td[2]').text.replace(',',''))
        self.real_time_price.append(real_time_data)
        
        return real_time_data
    
    def getVolume(self):
        real_time_data = float(self.driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div[2]/div[2]/table/tbody/tr[1]/td[5]').text.replace(',',''))

        if len(self.real_time_volume) > 1:
            self.real_time_volume.append(real_time_data - self.real_time_volume[-1])
        else:
            self.real_time_volume.append(real_time_data)

        return self.real_time_volume[-1]
    
    def getRealTime(self):
        vnds_clock = self.driver.find_element_by_xpath('/html/body/div/div/div[1]/header/div[2]/span[1]').text # we should not convert time frame here
        # because the gateway in has only role in getting updates and data from the market
        self.real_time.append(vnds_clock)
        return vnds_clock

    def getRealTimeData(self):

        return {'Price':self.getMatchedPrice(), 'Volume':self.getVolume(), 'Time':self.getRealTime()}