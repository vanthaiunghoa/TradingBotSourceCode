

from logging import setLoggerClass
from os import stat_result
from re import L, M


class TradingStrategy():
    def __init__(self, cash ):

        self.orders = []
        self.order_id = 0
        self.position = 0
        self.pnl = 0
        self.cash = 

    def creat_orders(self,side, price,quantity):

        ord = {
            'id': self.order_id,
            'price': price,
            'quantity': quantity,
            'side': side,
            'action': 'to_be_sent'
        }
        return ord

    def signal(self, realTimePrice): # realtimePrice is a list collecting data from the market based on the gatwayIn 

    

    def execution():
        
        