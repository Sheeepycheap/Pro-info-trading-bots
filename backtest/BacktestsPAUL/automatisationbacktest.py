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
# from glassnode import GlassnodeClient
import requests

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

    def updateLcapital(self, Capital):
        self.LCapital.append(Capital)


    
    def automatisation_backtest(self, typetrade : str, entrycondition : bool, outcondition : bool,\
        indice : Decimal, enCours : bool, Lindex = [], Lprice = [], LCapital = []):
        self.outcondition = outcondition
        # self.TP = TP
        # self.SL = SL
        self.indice = indice
        self.enCours = enCours
        self.Lindex = Lindex  
        self.Lprice = Lprice 
        if typetrade == 'short':
            if entrycondition:
                Entryprice = self.dataframe5.loc[int(self.indice),'price']
                entryTimestamp = self.dataframe5.loc[int(self.indice),'date']
                entryTime = datetime.utcfromtimestamp(entryTimestamp).strftime('%Y-%m-%d %H:%M:%S')
                #on initialise les datas pour la timeframe 1m
                index = self.dataframe1.loc[self.dataframe1['date'] == entryTimestamp+240,'price'].index[0]
                self.Lindex.append(self.dataframe1.loc[index,'date'])
                self.Lprice.append(self.dataframe5.loc[int(self.indice),'price'])
                self.enCours = True
                # while enCours:
                while outcondition and indice< self.end or enCours and self.indice< self.end: #currentZscore1m >= 0
                    #ici on passe sur la dataframe une minute
                    #Les données en commun sont la date et l'heure de la mesure donc on va récupérer ca
                    
                    index +=1
                    self.indice = Decimal(str(indice)) + Decimal('0.2')
                    self.Lindex.append(self.dataframe1.loc[index,'date'])
                    self.Lprice.append(self.dataframe1.loc[index,'price'])
                    if Decimal(str(self.indice))%1 == 0.0:
                        # LzScore.append(dataframe5.loc[int(indice),'zscore'])
                        # LzScoreMA.append(dataframe5.loc[int(indice),'zscoreMA'])
                        LCapital.append(self.Capital)
                    if (Entryprice-self.dataframe1.loc[index,'price'])/Entryprice > self.TP:
                        self.enCours = False
                        break
                    if (self.dataframe1.loc[index,'price']-Entryprice)/Entryprice > self.SL:
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
                    # LzScore.append(dataframe5.loc[int(indice),'zscore'])
                    # LzScoreMA.append(dataframe5.loc[int(indice),'zscoreMA'])
                    self.LCapital.append(self.Capital)
