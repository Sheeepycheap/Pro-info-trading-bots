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
        # MetaTrader5 et celui de yfinance ! 
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
        # cette série d'opération sur self.df permet d'actualiser la dataframe (base de donnée) self.df en ajoutant 
        # les colonnes 20ema, 5ema, 60ema
        self.pill2kill = []
        # self.pill2kill contient la liste des threads à terminer. Pour cette exemple, il n'y aura que 
        # proccess_open_buy à terminer. 
        self.dead = True 
        # self.dead sera utiliser plus tard pour terminer proccess_open_buy à terminer grâce à la méthode kill.

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
        #""
        # Cette méthode permet de mettre à jour self.df, ce qui est nécessaire pour faire du trading en direct. 
        #""
        self.df = ind.ydataframe(stock = self.ysymbol, start= '2022-03-14', interval='1m') 
        self.df = ind.ema(self.df,length=20,column='Close')
        self.df = ind.ema(self.df,length=5,column='Close')
        self.df = ind.ema(self.df,length=60,column='Close')


    def process_open_buy(self) :
        #""
        # Il s'agit de la méthode qui permet l'achat et la vente de l'actif selon la stratégie. La stratégie est simple : 
        # Si la courbe de la moyenne mobile exponentielle de 5 jours (5ema) est au dessus de celle de 20ema, et que cette 
        # dernière est au dessus de 60ema, alors On achète. Si on a 5ema<20ema<60ema, on vend. Pour procéder à une 
        # opération d'achat il faut d'abord qu'il y ait eu un achat avant (c'est le rôle de self.position_ouverte)
        #"" 
        while self.dead :
            n=len(self.df) - 1 
            if self.df['5EMA_Close'][n] > self.df['20EMA_Close'][n] and self.df['20EMA_Close'][n] > self.df['60EMA_Close'][n] and  self.position_ouverte == False :
                # Les conditions d'achat sont respectées, et la dernière opération étaint une vente. Il n'y a donc pas de position ouverte. 
                prix = mt5.symbol_info_tick(self.mt5symbol).ask
                self.request(action = mt5.TRADE_ACTION_DEAL, type = mt5.ORDER_TYPE_BUY, price = prix, sl = 0.0,tp=0.0, comment = "call",  position_ouverte= True )
                if 'position' in self.orders.keys() :
                    # pour pouvoir acheter, il faut un ticket orders (dictionnaire) ne contenant pas de clé 'position'.
                    # En effet, pour vendre, il faut une clé en plus que pour le ticket d'achat, position, qui permet 
                    # d'indiquer l'opération que l'on souhaite modifier. Ici, vu que l'on souhaite acheter, on vérifie
                    # que self.orders a le bon format.
                    ind.removekey(self.orders)
                    mt5.order_send(self.orders)
                else :
                    # self.orders a le bon format.
                    mt5.order_send(self.orders)
                    print(self.orders)
            elif self.df['5EMA_Close'][n] < self.df['20EMA_Close'][n] and self.df['20EMA_Close'][n] < self.df['60EMA_Close'][n] and  self.position_ouverte == True :
                # Les conditions de ventes sont réunies.
                prix = mt5.symbol_info_tick(self.mt5symbol).bid
                self.request(action = mt5.TRADE_ACTION_DEAL, type = mt5.ORDER_TYPE_SELL, price = prix, sl = 0.0,tp=0.0, comment = "sell",  position_ouverte = False )
                position = mt5.positions_get()[-1].ticket
                # On détermine la position de l'opération que l'on souhaite clôturer. 
                ind.addkey(self.orders, position=position)  
                mt5.order_send(self.orders)
            self.update_df()
            time.sleep(10)

    def open_buy(self) :
        #""
        # Cette méthode permet de lancer en parallèle (faire un thread) la méthode process_open_buy(). Dès 
        # qu'un objet de classe Trois Ema est instancié, on lui applique cette méthode pour lancer l'algorithme de 
        # trading automatique. 
        # ""
        thread = threading.Thread(target= self.process_open_buy) #lancement de la programation en parallèle.
        self.pill2kill.append(thread)
        thread.start()

    def kill(self) : 
        #""
        # Cette méthode permet d'ârreter les opérations d'achat et de vente, en arrêtant proccess_open_buy()
        #""
        self.dead = False 
        self.pill2kill[0].join()



            

                  





        





