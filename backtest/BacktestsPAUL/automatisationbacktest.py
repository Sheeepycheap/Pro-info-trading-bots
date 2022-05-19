from pickle import TRUE
from pandas import *
import pandas as pd
import yfinance as yf
import requests as rq
from binance import *
import asyncio
import json
import requests
import time
from matplotlib import *
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from math import *
from decimal import *
import requests

#Ce fichier et le fichier pour automatiser le backtest. Il est présent pour la lisibilité du code principal, pour faciliter les changements
#de conditions en fonction des différentes stratégies à tester
#
#Pour ce faire, nous allons créer un objet backteste qui d'implementera à chaque trade
#
#
class backtest:
    def __init__(self,dataframe5, dataframe1, filename : str, TP : float, SL : float, \
         indice : Decimal, end : int, enCours : bool, Capital : float, nombreDeTrade : int, Winrate, Gainmoyentrade : float, Lindex = [],\
            Lprice = [], LCapital = []):
        self.dataframe5 = dataframe5
        self.dataframe1 = dataframe1
        self.filename = filename
        self.TP = TP
        self.SL = SL
        self.indice = indice
        self.end = end
        self.enCours = enCours
        self.Capital = Capital
        self.nombreDeTrade = nombreDeTrade
        self.Winrate = Winrate
        self.Gainmoyentrade = Gainmoyentrade       
        self.Lindex = Lindex  
        self.Lprice = Lprice   
        self.LCapital = LCapital

    def updateL(self, Capital, indice, price):
        self.LCapital.append(Capital)
        self.Lindex.append(indice)
        self.Lprice.append(price)


    
    def automatisation_backtest(self, TP : float, SL : float, typetrade : str, entrycondition : bool, outcondition,\
        indice : Decimal, enCours : bool, timeframe : str, Lindex = [], Lprice = [], LCapital = []):
        self.outcondition = outcondition
        self.TP = TP
        self.SL = SL
        self.indice = indice
        self.enCours = enCours
        # self.Lindex = Lindex  
        # self.Lprice = Lprice
        Entryprice = 1
        Outprice = 1
        if self.indice == 60000:
            print(self.indice)
        if typetrade == 'long':
            Entryprice = self.dataframe5.loc[int(self.indice),'price']
            entryTimestamp = self.dataframe5.loc[int(self.indice),'date']
            entryTime = datetime.utcfromtimestamp(entryTimestamp).strftime('%Y-%m-%d %H:%M:%S')
            #on initialise les datas pour la timeframe 1m

            index = self.dataframe1.loc[self.dataframe1['date'] == entryTimestamp+self.getcurrentindex(timeframe),'price'].index[0]
            # self.Lindex.append(self.dataframe1.loc[index,'date'])
            # self.Lprice.append(self.dataframe5.loc[int(self.indice),'price'])
            self.enCours = True

            while (self.dataframe5.loc[int(self.indice),'20Zscore_price'] <= 0 or self.enCours) and self.indice < self.end: 
                #ici on passe sur la dataframe une minute
                #Les données en commun sont la date et l'heure de la mesure donc on va récupérer ca
                index +=1
                self.indice = Decimal(str(indice)) + Decimal('0.2')

                if Decimal(str(self.indice))%1 == 0.0:
                    self.LCapital.append(self.Capital)
                    self.Lindex.append(self.dataframe5.loc[self.indice,'date'])
                    self.Lprice.append(self.dataframe5.loc[self.indice,'price'])
                if (self.dataframe1.loc[index,'price'] - Entryprice)/Entryprice > self.TP:
                    self.enCours = False
                    break
                if (Entryprice -self.dataframe1.loc[index,'price'])/Entryprice > self.SL:
                    self.enCours = False
                    break
            outTime = datetime.utcfromtimestamp(self.dataframe1.loc[index,'date']).strftime('%Y-%m-%d %H:%M:%S')
            Outprice = self.dataframe1.loc[index,'price']
            #Donc faut arreter le backtesting si le capital tombe à 0 
            Resultattrade = self.Capital * (Outprice - Entryprice)/Entryprice
            if Resultattrade >= 0:
                self.Winrate +=1
            self.Capital = self.Capital + Resultattrade
            self.nombreDeTrade += 1
            self.Gainmoyentrade += Resultattrade
            ClosedTrade = {'Long ou short' : typetrade, 'Entry price' : Entryprice, 'Out price' : Outprice, 'Benefice on trade' : Resultattrade, 'Capital after this trade' : self.Capital, 'Date d\'entree' : entryTime, 'Date de sortie' : outTime}
            with open(self.filename, 'a+') as e:
                json.dump(ClosedTrade, e)
            if not Decimal(str(self.indice))%1 == 0.0:
                self.indice = Decimal(ceil(self.indice))
        if typetrade == 'short':
            Entryprice = self.dataframe5.loc[int(self.indice),'price']
            entryTimestamp = self.dataframe5.loc[int(self.indice),'date']
            entryTime = datetime.utcfromtimestamp(entryTimestamp).strftime('%Y-%m-%d %H:%M:%S')
            #on initialise les datas pour la timeframe 1m

            index = self.dataframe1.loc[self.dataframe1['date'] == entryTimestamp+self.getcurrentindex(timeframe),'price'].index[0]
            # self.Lindex.append(self.dataframe1.loc[index,'date'])
            # self.Lprice.append(self.dataframe5.loc[int(self.indice),'price'])
            self.enCours = True

            while (self.dataframe5.loc[int(self.indice),'20Zscore_price'] <= -2.4 or self.enCours) and self.indice < self.end: 
                #ici on passe sur la dataframe une minute
                #Les données en commun sont la date et l'heure de la mesure donc on va récupérer ca
                index +=1
                self.indice = Decimal(str(indice)) + Decimal('0.2')

                if Decimal(str(self.indice))%1 == 0.0:
                    self.LCapital.append(self.Capital)
                    self.Lindex.append(self.dataframe5.loc[self.indice,'date'])
                    self.Lprice.append(self.dataframe5.loc[self.indice,'price'])
                if (Entryprice - self.dataframe1.loc[index,'price'])/Entryprice > self.TP:
                    self.enCours = False
                    break
                if (self.dataframe1.loc[index,'price'] - Entryprice)/Entryprice > self.SL:
                    self.enCours = False
                    break
            outTime = datetime.utcfromtimestamp(self.dataframe1.loc[index,'date']).strftime('%Y-%m-%d %H:%M:%S')
            Outprice = self.dataframe1.loc[index,'price']
            #Donc faut arreter le backtesting si le capital tombe à 0 
            Resultattrade = self.Capital * (Entryprice - Outprice)/Entryprice
            if Resultattrade >= 0:
                self.Winrate +=1
            self.Capital = self.Capital + Resultattrade
            self.nombreDeTrade += 1
            self.Gainmoyentrade += Resultattrade
            ClosedTrade = {'Long ou short' : typetrade, 'Entry price' : Entryprice, 'Out price' : Outprice, 'Benefice on trade' : Resultattrade, 'Capital after this trade' : self.Capital, 'Date d\'entree' : entryTime, 'Date de sortie' : outTime}
            with open(self.filename, 'a+') as e:
                json.dump(ClosedTrade, e)
            if not Decimal(str(self.indice))%1 == 0.0:
                self.indice = Decimal(ceil(self.indice))
                

    def automatisation_backtest_nonmonitored(self, typetrade : str, entrycondition : bool, outcondition : bool,\
        indice : Decimal, enCours : bool, Lindex = [], Lprice = [], LCapital = []):
        # self.outcondition = outcondition
        # self.TP = TP
        # self.SL = SL
        self.indice = indice
        self.enCours = enCours
        EntrypriceTPSL = 1
        Entryprice = 1
        Outprice = 1
        if typetrade != 'short':
            EntrypriceTPSL = -1
            Outprice = -1
        if entrycondition:
            EntrypriceTPSL *= self.dataframe5.loc[int(self.indice),'price']
            Entryprice = self.dataframe5.loc[int(self.indice),'price']
            entryTimestamp = self.dataframe5.loc[int(self.indice),'date']
            entryTime = datetime.utcfromtimestamp(entryTimestamp).strftime('%Y-%m-%d %H:%M:%S')
            self.enCours = True
            print('IN 1')
            # while enCours:
            while not outcondition and self.indice < self.end or self.enCours and self.indice< self.end: 
                self.indice += Decimal('1')
                self.LCapital.append(self.Capital)
                self.Lindex.append(self.dataframe5.loc[int(self.indice),'date'])
                self.Lprice.append(self.dataframe5.loc[int(self.indice),'price'])
                # print(outcondition)
                if self.dataframe5.loc[int(self.indice),'PSARdir'] == "bear":
                    self.enCours = False
                    
                    break
                # if (EntrypriceTPSL-self.dataframe1.loc[index,'price'])/Entryprice > self.TP:
                #     self.enCours = False
                #     break
                # if (self.dataframe1.loc[index,'price']-EntrypriceTPSL)/Entryprice > self.SL:
                #     self.enCours = False
                #     break
            outTime = datetime.utcfromtimestamp(self.dataframe5.loc[int(self.indice),'date']).strftime('%Y-%m-%d %H:%M:%S')
            Outprice *= self.dataframe5.loc[int(self.indice),'price']

            Resultattrade = self.Capital * (EntrypriceTPSL - Outprice)/Entryprice
            if Resultattrade >= 0:
                self.Winrate +=1
            self.Capital = self.Capital + Resultattrade
            self.nombreDeTrade += 1
            self.Gainmoyentrade += Resultattrade
            ClosedTrade = {'Long ou short' : typetrade, 'Entry price' : Entryprice, 'Out price' : Outprice, 'Benefice on trade' : Resultattrade, 'Capital after this trade' : self.Capital, 'Date d\'entree' : entryTime, 'Date de sortie' : outTime}
            with open(self.filename, 'a+') as e:
                json.dump(ClosedTrade, e)
            if not Decimal(str(self.indice))%1 == 0.0:
                self.indice = Decimal(ceil(self.indice))
    
    def getcurrentindex(self, timeframe : str):
        pas = 0
        if timeframe == '5m':
            pas =  240 #5*60 - 60
        elif timeframe == '15m':
            pas = 15*60 - 60
        elif timeframe == '1h':
            pas = 60 * 60 - 60
        elif timeframe == '2h':
            pas = 120 * 60 - 60
        elif timeframe == '4h':
            pas = 240 * 60 - 60
        elif timeframe == '1d':
            pas = 24 * 60 * 60 - 60
        return pas

    def update_k(self):
        return self.indice