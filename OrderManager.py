import string
import time

import pandas as pd
import numpy as np
import re as regex
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
import time
from datetime import date, datetime
import statistics as stats

class OrderManager():
    def __init__(self, driver):
        self.driver = driver
    
    def send_buy_order(self, price, quantity):

        stockInput = self.driver.find_element(By.CLASS_NAME, 'react-autosuggest__input')
        # //*[@id="placeorder"]/div/div[2]/div/div/input
        stockInput.click() # the input label is  a little strange and we must use the class
        stockInput.send_keys('VN30F2108')
        # //*[@id="order-price-id"]
        priceInput = self.driver.find_element_by_xpath(
            '//*[@id="order-price-id"]')
        deleteRange = 10
        for i in range(0, deleteRange):
            priceInput.send_keys(Keys.BACK_SPACE)
        priceInput.send_keys(price)

        quantityInput = self.driver.find_element_by_xpath(
            '//*[@id="order-qtty-id"]')
        for i in range(0, deleteRange):
            quantityInput.send_keys(Keys.BACK_SPACE)
        quantityInput.send_keys(quantity)
        self.driver.find_element(By.CLASS_NAME, "buy").click()

    def send_sell_order(self, price, quantity):
        #method":"xpath","selector":"/html/body/div/div/div[2]/div/div/div[3]/div[2]/div/div[2]/div/div/input
        stockInput = self.driver.find_element(By.CLASS_NAME, 'react-autosuggest__input')
        # //*[@id="placeorder"]/div/div[2]/div/div/input
        stockInput.click() # the input label is  a little strange and we must use the class
     
        stockInput.send_keys('VN30F2108')

        # //*[@id="order-price-id"]
        priceInput = self.driver.find_element_by_xpath(
            '//*[@id="order-price-id"]')
        deleteRange = 10
        for i in range(0, deleteRange):
            priceInput.send_keys(Keys.BACK_SPACE)
        priceInput.send_keys(price)

        quantityInput = self.driver.find_element_by_xpath(
            '//*[@id="order-qtty-id"]')
        
        for i in range(0, deleteRange):
            quantityInput.send_keys(Keys.BACK_SPACE)
        quantityInput.send_keys(quantity)

        self.driver.find_element(By.CLASS_NAME, "sell").click()

    def refreshPage(self):
        # refreshPage to update the status of the order
        refreshButton = self.driver.find_element_by_xpath('//*[@id="orderbook"]/div[1]/i[1]')
        refreshButton.click()
    def checkOrderStatus(self):
        
        #searchRow = self.driver.find_element_by_xpath('//*[@id="orderbook"]/div[2]/table/tbody/tr[1]')
        # search the first trow
        # because this is the most recent order we sent
        matchedLogo =  self.driver.find_element_by_xpath(
            '//*[@id="orderbook"]/div[2]/table/tbody/tr[1]/td[6]/span')

        valueMatched = matchedLogo.get_attribute('data-tip')
        if valueMatched == "Khớp":
            return "match"
        elif valueMatched == 'Đã lên Sàn' or valueMatched =='Chờ gửi lên Sàn':
            return 'pending'
        else:
            return "error"

    def getMatchedPrice(self):
        return self.driver.find_element_by_xpath('//*[@id="orderbook"]/div[2]/table/tbody/tr[1]/td[5]')
    
    def cancelOrder(self):

        self.refreshPage()
        # the code send request quite fass
        # need the sleep for the web load
        time.sleep(0.3)
        if self.checkOrderStatus() == 'pending':
            #//*[@id="orderbook"]/div[2]/table/tbody/tr[1]/td[6]/div/a/i
            # open the cancel button:
            self.driver.find_element_by_xpath('//*[@id="orderbook"]/div[2]/table/tbody/tr[1]/td[6]/div/a/i').click() # click to see the delete button
            self.driver.find_element_by_xpath('//*[@id="orderbook"]/div[2]/table/tbody/tr[1]/td[6]/button[1]').click() # cancel the order
            #//*[@id="orderbook"]/div[2]/table/tbody/tr[1]/td[1]/input
            return  1 
        else:
            return  -1

    def cancelAllOrders(self):
        print("successfully run")
        self.refreshPage()
        time.sleep(0.5)
        checkBoxToDelete = self.driver.find_elements(By.CLASS_NAME, 'checkbox')
        cnt = 0
        for checkbox in checkBoxToDelete:

            checkBoxInput = checkbox.find_elements(By.TAG_NAME, 'input')
            if len(checkBoxInput) != 0: # we use the len not the size()
                # find the parent element and find the cancel button
                checkBoxInput[0].click() # unnecessary
                row = checkbox.find_element(By.XPATH, './..')

                print(row.text)
                row.find_elements(By.TAG_NAME, 'i')[1].click() # find and click on the delete icon
                row.find_elements(By.CLASS_NAME, 'btn-yes')[0].click() # find and click on the cancel button
