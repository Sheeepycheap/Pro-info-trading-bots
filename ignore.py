from concurrent.futures import thread
from threading import Thread
import threading
from time import sleep
import Indicateurs as ind 
from datetime import datetime
import MetaTrader5 as mt5

data = ind.ydataframe(stock = "BTC-USD",start = '2022-03-04', interval='1m')
data = ind.ema(data,length=60,column='Close')

class Voiture :
    def __init__(self,ysymbol : str,mt5symbol: str) -> None:
        self.df = ind.ydataframe(stock = ysymbol, start= '2022-03-04', interval='1m')
        self.df = ind.ema(self.df,length=60,column='Close')
        self.mt5symbol = mt5symbol
        #self.prix = mt5.symbol_info_tick(self.mt5symbol).ask
    #def getprix(self) :
        #return self.prix
pr = mt5.symbol_info_tick("EURUSD")
v1 = Voiture(ysymbol="BTC-USD",mt5symbol="BTCUSD")
print(pr)
print(mt5.last_error())




 

