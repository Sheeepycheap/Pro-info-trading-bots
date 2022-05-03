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
from abc import ABC, abstractmethod
from math import floor



class Bot(ABC) :
    @abstractmethod
    def open_buy(self) :
        #""
        # Cette méthode permet de lancer en parallèle (faire un thread) la méthode process_open_buy(). Dès 
        # qu'un objet de classe Trois Ema est instancié, on lui applique cette méthode pour lancer l'algorithme de 
        # trading automatique. 
        # ""
        thread = threading.Thread(target= self.process_open_buy) #lancement de la programation en parallèle.
        self.pill2kill.append(thread)
        thread.start()    
    @abstractmethod
    def kill(self) : 
        #""
        # Cette méthode permet d'ârreter les opérations d'achat et de vente, en arrêtant proccess_open_buy()
        #""
        self.dead = False 
        self.pill2kill[0].join()

class TroisMA(Bot) :
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
        self.df = ind.ydataframe(stock = ysymbol, start= '2022-03-14', interval='5m') 
        self.df = ind.ema(self.df,length=20,column='Close')
        self.df = ind.ema(self.df,length=5,column='Close')
        self.df = ind.ema(self.df,length=60,column='Close')
        self.pill2kill = []
        self.dead = True 
<<<<<<< Updated upstream
=======
        # self.dead sera utiliser plus tard pour terminer proccess_open_buy à terminer grâce à la méthode kill.
        self.position = 0
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
        self.df = ind.ydataframe(stock = self.ysymbol, start= '2022-03-14', interval='1m') 
=======
        #""
        # Cette méthode permet de mettre à jour self.df, ce qui est nécessaire pour faire du trading en direct. 
        #""
        self.df = ind.ydataframe(stock = self.ysymbol, start= '2022-03-14', interval='5m') 
>>>>>>> Stashed changes
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
                self.position = mt5.positions_get()[-1].ticket # On détermine la position de l'opération que l'on souhaite clôturer plus tard. 
            elif self.df['5EMA_Close'][n] < self.df['20EMA_Close'][n] and self.df['20EMA_Close'][n] < self.df['60EMA_Close'][n] and  self.position_ouverte == True :
                prix = mt5.symbol_info_tick(self.mt5symbol).bid
                self.request(action = mt5.TRADE_ACTION_DEAL, type = mt5.ORDER_TYPE_SELL, price = prix, sl = 0.0,tp=0.0, comment = "sell",  position_ouverte = False )
<<<<<<< Updated upstream
                position = mt5.positions_get()[-1].ticket
                ind.addkey(self.orders, position=position)  
=======
                ind.addkey(self.orders, position=self.position)  
>>>>>>> Stashed changes
                mt5.order_send(self.orders)
            print(self.df['5EMA_Close'][n])
            print(self.df['20EMA_Close'][n])
            print(self.df['60EMA_Close'][n])
            self.update_df()
            time.sleep(10)

    def open_buy(self) :
<<<<<<< Updated upstream
        thread = threading.Thread(target= self.process_open_buy)
        self.pill2kill.append(thread)
        thread.start()

    def kill(self) : 
        self.dead = False 
        self.pill2kill[0].join()
=======
        pass
    
    def kill(self) :
        pass


>>>>>>> Stashed changes


class Zscore(Bot) : 
    #""
    # Implémentons la stratégie du Zscore. Le Zscore à un instant T est simplement la distance entre la moyenne et le cours en nombre d'écart 
    # type.  
    #""

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
            self.df = ind.ydataframe(stock = ysymbol, start= '2022-03-14', interval='5m') 
            self.df = ind.zscore(self.df, length= 20, column = 'Close')
            # self.df = ind.sma(self.df,length=20,column='20Zscore_Close')
            # cette série d'opération sur self.df permet d'actualiser la dataframe (base de donnée) self.df en ajoutant 
            # les colonnes 20Zscore
            self.pill2kill = []
            # self.pill2kill contient la liste des threads à terminer. Pour cette exemple, il n'y aura que 
            # proccess_open_buy à terminer. 
            self.dead = True 
            # self.dead sera utiliser plus tard pour terminer proccess_open_buy à terminer grâce à la méthode kill.
            self.position = 0
            self.tp = 0.0
            self.sl = 0.0

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
            self.df = ind.ydataframe(stock = self.ysymbol, start= '2022-05-01', interval='5m') 
            self.df = ind.zscore(self.df, length= 20, column = 'Close')

        def process_open_buy(self) :
            while self.dead :
                print(mt5.symbol_info_tick(self.mt5symbol).bid)
                bid = mt5.symbol_info_tick(self.mt5symbol).bid
                n=len(self.df) - 1  
                print(self.df['20Zscore_Close'][n])   
                if  self.df['20Zscore_Close'][n] > 2.4 and self.position_ouverte == False :
                    print("Signal d'ouverture de position")
                    prix = mt5.symbol_info_tick(self.mt5symbol).ask
                    self.sl = 1.0012*bid
                    self.tp = 0.9804*bid
                    self.request(action = mt5.TRADE_ACTION_DEAL, type = mt5.ORDER_TYPE_SELL, price = prix, sl = 0.0,tp=0.0, comment = "short",  position_ouverte= True )
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
                    self.position = mt5.positions_get()[-1].ticket # On détermine la position de l'opération que l'on souhaite clôturer plus tard. 
                elif self.df['20Zscore_Close'][n] < -2.4 and  self.position_ouverte == True : 
                    print("Clôture par zscore trop bas")
                    prix = mt5.symbol_info_tick(self.mt5symbol).bid
                    self.request(action = mt5.TRADE_ACTION_DEAL, type = mt5.ORDER_TYPE_BUY, price = prix, sl = 0.0,tp=0.0, comment = "Clôture par zscore trop bas",  position_ouverte = False )
                    ind.addkey(self.orders, position=self.position) 
                    mt5.order_send(self.orders)
                elif bid >= self.sl and  self.position_ouverte == True : 
                    print("Clôture par SL")
                    prix = mt5.symbol_info_tick(self.mt5symbol).bid
                    self.request(action = mt5.TRADE_ACTION_DEAL, type = mt5.ORDER_TYPE_BUY, price = prix, sl = 0.0,tp=0.0, comment = "Clôture par SL",  position_ouverte = False )
                    ind.addkey(self.orders, position=self.position) 
                    mt5.order_send(self.orders)
                elif bid <= self.tp and  self.position_ouverte == True : 
                    print("Clôture par TP")
                    prix = mt5.symbol_info_tick(self.mt5symbol).bid
                    self.request(action = mt5.TRADE_ACTION_DEAL, type = mt5.ORDER_TYPE_BUY, price = prix, sl = 0.0,tp=0.0, comment = "Clôture par TP",  position_ouverte = False )
                    ind.addkey(self.orders, position=self.position) 
                    mt5.order_send(self.orders)
                self.update_df()
                time.sleep(10)  
        
        def open_buy(self) :
            pass

        def kill(self) : 
            pass






def usr_login(usr : int, mdp : str, server : str) :
    if not mt5.initialize() : 
         print("MetaTrader5 n'a pas pu être initialisée")
         quit()
    else : 
        if not mt5.login(usr,mdp,server) : 
            print("Vérifiez vos identifiants")
        else : 
            print("Connexion réussie !")

usr_login(usr = 41600933, mdp = "ZL6HzUageSX6", server = "AdmiralMarkets-Demo" )


botzsore = Zscore(mt5symbol="BTCUSD",volume=0.01,ysymbol="BTC-USD")
botzsore.process_open_buy()



