from ast import Break
from pickle import TRUE
import re
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
import Indicateurs as ind
from Indicateurs import *
dataframe6mois1m = pd.read_pickle("./backtest/Bot_trading/dataframe6mois1m.pkl")
dataframe6mois5mm = pd.read_pickle("./backtest/Bot_trading/dataframe6mois5m.pkl")
dataframe6mois5 = pd.read_pickle("./dataframe5mESSAI")  
#bot de backtest


def createrangefilter(data1, data2) -> pd.DataFrame:
    #""
    #Range filter. 
    #Creation de la colonne rangefilter à partir du reste on parcourt toute la bdd de base
    #On ajoute les valeurs à chaque ligne comme si on fesait du live trading
    #""
    # print(str(indice) + ' ' + str(rngfilt))

    #On initialise le rangefilter
    rangefilter = pd.DataFrame({'rngfilter' : [0]})
    for k in range(len(data1.index)):
        if data1.loc[k,'price'] > rangefilter.iloc[-1,0] :
            if data1.loc[k,'price'] - data2.loc[k] < rangefilter.iloc[-1,0]:
                rangefilter.loc[rangefilter.shape[0]] = rangefilter.iloc[-1,0]
            else:
                rangefilter.loc[rangefilter.shape[0]] = data1.loc[k,'price'] - data2.loc[k]
        else : 
            if data1.loc[k,'price'] + data2.loc[k] > rangefilter.iloc[-1,0]:
                rangefilter.loc[rangefilter.shape[0]] = rangefilter.iloc[-1,0]
            else :
                rangefilter.loc[rangefilter.shape[0]] = data1.loc[k,'price'] + data2.loc[k]
    data1["Rangefilter"] = rangefilter


def Upward(data1):
    upward = pd.DataFrame({'upwrd' : [0]})
    for k in range(1,len(data1.index)):
        if data1.loc[k,'Rangefilter'] > data1.loc[k-1,'Rangefilter']:
            upward.loc[upward.shape[0]] = upward.iloc[-1,0] + 1
        else:
            if data1.loc[k,'Rangefilter'] < data1.loc[k-1,'Rangefilter']:
                upward.loc[upward.shape[0]] = 0
            else:
                upward.loc[upward.shape[0]] = upward.iloc[-1,0]
    data1['Upward'] = upward

def Downward(data1):
    downward = pd.DataFrame({'dnwrd' : [0]})
    for k in range(1,len(data1.index)):
        if data1.loc[k,'Rangefilter'] < data1.loc[k-1,'Rangefilter']:
            downward.loc[downward.shape[0]] = downward.iloc[-1,0] + 1
        else:
            if data1.loc[k,'Rangefilter'] > data1.loc[k-1,'Rangefilter']:
                downward.loc[downward.shape[0]] = 0
            else:
                downward.loc[downward.shape[0]] = downward.iloc[-1,0]
    data1['Downward'] = downward

LCapital = []
Lprice = []
Lindex = [] 
def main(filename,start,end):
    file = open(filename, 'w+')
    #initialisation des variables
    entryTime = start
    Entryprice = 0
    Outprice = 0
    entryTime = 0
    #On Backtest avec un capital de 1000
    Capital = 1000
    #On veut avoir le nombre de trade
    nombreDeTrade = 0
    #Variable de teste pour savoir si un trade est en cours ou pas
    enCourslong = False
    enCoursshort = False

    #ICI on utilise ces valeurs pour la création du rangefilter
    # smrng1 = smoothaveragerange(dataframe6mois5, 'price',27.0, 1.6)
    # smrng2 = smoothaveragerange(dataframe6mois5, 'price',55.0, 2.0)
    # smrng = (smrng1 + smrng2) /2

    #ESSAI:
    # hband = filt + smrng
    # lband = filt - smrng 


    #Pour simuler le short en gain je vais juste faire (prix de sortie) - (prix d'entrée)
    #Pour simuler le long en gain je vais juste faire (prix d'entrée) - (prix de sortie)
    k = Decimal(start)
    while k < end:
        k+=Decimal(1)
        #long condition
        if enCourslong or\
             dataframe6mois5.loc[int(k),'price'] > dataframe6mois5.loc[int(k),'Rangefilter'] and dataframe6mois5.loc[int(k),'price'] != dataframe6mois5.loc[int(k)-1,'price'] and dataframe6mois5.loc[int(k),'Upward'] > 0:
            enCourslong = True
            Entryprice = dataframe6mois5.loc[int(k),'price']
            entryTimestamp = dataframe6mois5.loc[int(k),'date']
            entryTime = datetime.utcfromtimestamp(entryTimestamp).strftime('%Y-%m-%d %H:%M:%S')
            #on initialise les datas pour la timeframe 1m
            index = dataframe6mois1m.loc[dataframe6mois1m['date'] == entryTimestamp+240,'price'].index[0]
            #Pour avoir des retours graphiques on stoque les données du bazcktesting en cours dans une liste
            Lindex.append(dataframe6mois1m.loc[index,'date'])
            LCapital.append(Capital)
            while enCourslong == True:       
                index +=1
                k = Decimal(str(k)) + Decimal('0.2')
                if Decimal(str(k))%1 == 0.0:
                    Lindex.append(dataframe6mois1m.loc[index,'date'])
                    LCapital.append(Capital)
                    if dataframe6mois5.loc[int(k),'price'] < dataframe6mois5.loc[int(k),'Rangefilter'] and dataframe6mois5.loc[int(k),'price'] != dataframe6mois5.loc[int(k)-1,'price'] and dataframe6mois5.loc[int(k),'Downward'] > 0:
                        enCoursshort = True
                        enCourslong = False
                        break
                # #TP
                # if (dataframe6mois1m.loc[index,'price']-Entryprice)/Entryprice > 0.005:
                #     enCourslong = False
                #     k = int(k)
                #     break
                # #SL
                # if (Entryprice-dataframe6mois1m.loc[index,'price'])/Entryprice > 0.002:
                #     enCourslong = False
                #     k = int(k)
                #     break
            outTime = datetime.utcfromtimestamp(dataframe6mois1m.loc[index,'date']).strftime('%Y-%m-%d %H:%M:%S')
            Outprice = dataframe6mois1m.loc[index,'price']
            
            Resultattrade = Capital * (Entryprice - Outprice)/Entryprice
            Capital = Capital + Resultattrade
            nombreDeTrade+=1
            ClosedTrade = {'Entry price' : Entryprice, 'Out price' : Outprice, 'Benefice on trade' : Resultattrade, 'Capital after this trade' : Capital, 'Date d\'entree' : entryTime, 'Date de sortie' : outTime}
            with open(filename, 'a+') as e:
                json.dump(ClosedTrade, e)            
        if enCoursshort  or\
             dataframe6mois5.loc[int(k),'price'] <  dataframe6mois5.loc[int(k),'Rangefilter'] and dataframe6mois5.loc[int(k),'price'] != dataframe6mois5.loc[int(k)-1,'price'] and dataframe6mois5.loc[int(k),'Downward'] > 0:
            enCoursshort = True
            Entryprice = dataframe6mois5.loc[int(k),'price']
            entryTimestamp = dataframe6mois5.loc[int(k),'date']
            entryTime = datetime.utcfromtimestamp(entryTimestamp).strftime('%Y-%m-%d %H:%M:%S')
            #on initialise les datas pour la timeframe 1m pour corréler les prix
            index = dataframe6mois1m.loc[dataframe6mois1m['date'] == entryTimestamp+240,'price'].index[0]
            #Pour avoir des retours graphiques on stoque les données du bazcktesting en cours dans une liste
            Lindex.append(dataframe6mois1m.loc[index,'date'])
            LCapital.append(Capital)
            while enCoursshort == True:       
                index +=1
                k = Decimal(str(k)) + Decimal('0.2')
                if Decimal(str(k))%1 == 0.0:
                    Lindex.append(dataframe6mois1m.loc[index,'date'])
                    LCapital.append(Capital)
                    if dataframe6mois5.loc[int(k),'price'] > dataframe6mois5.loc[int(k),'Rangefilter'] and dataframe6mois5.loc[int(k),'price'] != dataframe6mois5.loc[int(k)-1,'price'] and dataframe6mois5.loc[int(k),'Upward'] > 0:
                        enCourslong = True
                        enCoursshort = False
                        break
                # #TP
                # if (Entryprice - dataframe6mois1m.loc[index,'price'])/Entryprice > 0.005:
                #     enCoursshort = False
                #     k = int(k)
                #     break
                # #SL
                # if (dataframe6mois1m.loc[index,'price'] - Entryprice)/Entryprice > 0.002:
                #     enCoursshort = False
                #     k = int(k)
                #     break
            outTime = datetime.utcfromtimestamp(dataframe6mois1m.loc[index,'date']).strftime('%Y-%m-%d %H:%M:%S')
            Outprice = dataframe6mois1m.loc[index,'price']
            
            Resultattrade = Capital * (Entryprice - Outprice)/Entryprice
            Capital = Capital + Resultattrade
            nombreDeTrade+=1
            ClosedTrade = {'Entry price' : Entryprice, 'Out price' : Outprice, 'Benefice on trade' : Resultattrade, 'Capital after this trade' : Capital, 'Date d\'entree' : entryTime, 'Date de sortie' : outTime}
            with open(filename, 'a+') as e:
                json.dump(ClosedTrade, e)

main('essai2.json',1000,53100)  

plt.subplot(1, 2, 1)
plt.plot(Lindex,LCapital)
dataframeint = dataframe6mois5.loc[1000:53100,'price']
plt.subplot(1, 2, 2)
dataframeint.plot(y = 'price', use_index = True)

plt.show()
