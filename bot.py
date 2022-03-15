import threading
import yfinance as yf 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import Indicateurs as ind
import MetaTrader5 as mt5
from datetime import datetime
from threading import Thread
import time 



class TroisMA :
    # ""
    # Il s'agit d'implémenter la stratégie des 3MA. Bien que peu efficace, elle reste rentable. 
    # ""

    def __init__(self, mt5symbol : str, volume : float, ysymbol :str) -> None:
        #""
        #Constructeur de la classe. On initialise le champ orders qui est le ticket d'entrée. On ne 
        #spécifie que le symbol et le volume. Attention pour le symbol, il faut spécifier celui de 
        # MetaTrader5 et pas celui de yfinance ! 
        #""
        self.mt5symbol = mt5symbol
        self.ysymbol = ysymbol
        self.orders = {
        "action" : "a"  ,  
        "symbol" : mt5symbol ,
        "volume" : volume ,
        "type" : "a" ,
        "price" : "a",
        "sl" : 0.0 ,
        "tp" : 0.0 ,
        "deviation" : 20 ,
        "magic" : 234000 ,
        "comment" : "test",
        "type_time" : mt5.ORDER_TIME_GTC,
        "type filling" : mt5.ORDER_FILLING_IOC,            
        }
        self.position_ouverte = False 
        # determine la position dans laquelle où nous sommes : a-t-on une 
        # position ouverte ? False signifie que nous n'avons pas de position ouverte : on peut procéder
        # à une opération. 
        self.df = ind.ydataframe(stock = ysymbol, start= '2022-03-14', interval='1m') 
        self.df = ind.ema(self.df,length=20,column='Close')
        self.df = ind.ema(self.df,length=5,column='Close')
        self.df = ind.ema(self.df,length=60,column='Close')
        self.pill2kill = []
        self.dead = True 

    def request(self,action,type,price,sl,tp,comment,position_ouverte : bool) -> None :
        #""
        #méthode pour update orders de l'objet. On update aussi position_ouverte
        #""
        self.orders['action'] = action
        self.orders['type'] = type
        self.orders['price'] = price
        self.orders['sl'] = sl
        self.orders['tp'] = tp
        self.orders['comment'] = comment
        self.position_ouverte = position_ouverte
    
    def update_df(self) : 
        self.df = ind.ydataframe(stock = self.ysymbol, start= '2022-03-14', interval='1m') 
        self.df = ind.ema(self.df,length=20,column='Close')
        self.df = ind.ema(self.df,length=5,column='Close')
        self.df = ind.ema(self.df,length=60,column='Close')


    def process_open_buy(self) :
        c=1 
        while self.dead :
            print(c)
            c+=1
            n=len(self.df) - 1 
            print(self.df['5EMA_Close'][n] > self.df['20EMA_Close'][n] and self.df['20EMA_Close'][n] > self.df['60EMA_Close'][n] and  self.position_ouverte == False )
            print(self.df['5EMA_Close'][n] < self.df['20EMA_Close'][n] and self.df['20EMA_Close'][n]<self.df['60EMA_Close'][n] and  self.position_ouverte == True)
            if self.df['5EMA_Close'][n] > self.df['20EMA_Close'][n] and self.df['20EMA_Close'][n] > self.df['60EMA_Close'][n] and  self.position_ouverte == False :
                prix = mt5.symbol_info_tick(self.mt5symbol).ask
                print("ok")
                self.request(action = mt5.TRADE_ACTION_DEAL, type = mt5.ORDER_TYPE_BUY, price = prix, sl = 0.0,tp=0.0, comment = "call",  position_ouverte= True )
                if 'position' in self.orders.keys() :
                    ind.removekey(self.orders)
                    mt5.order_send(self.orders)
                else :
                    mt5.order_send(self.orders)
                    print(self.orders)
            elif self.df['5EMA_Close'][n] < self.df['20EMA_Close'][n] and self.df['20EMA_Close'][n] < self.df['60EMA_Close'][n] and  self.position_ouverte == True :
                prix = mt5.symbol_info_tick(self.mt5symbol).bid
                self.request(action = mt5.TRADE_ACTION_DEAL, type = mt5.ORDER_TYPE_SELL, price = prix, sl = 0.0,tp=0.0, comment = "sell",  position_ouverte = False )
                position = mt5.positions_get()[-1].ticket
                ind.addkey(self.orders, position=position)  
                mt5.order_send(self.orders)
            print(self.df['5EMA_Close'][n])
            print(self.df['20EMA_Close'][n])
            print(self.df['60EMA_Close'][n])
            self.update_df()
            time.sleep(10)

    def open_buy(self) :
        thread = threading.Thread(target= self.process_open_buy)
        self.pill2kill.append(thread)
        thread.start()

    def kill(self) : 
        self.dead = False 
        self.pill2kill[0].join()



            

                  





        





