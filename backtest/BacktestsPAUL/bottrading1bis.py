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
import automatisationbacktest as aut


def Selecttime(dataframe,startime, endtime):
    Lx = []
    for k in range(startime,endtime+1):
        
        Lx.append(dataframe.loc[k,'date'])
    return Lx
#get unix TIME
#On va faire ça avec l'api binance
api_key = '0W0NnouXJG5kHRuvjm7AcZNOSYxHHPmNWItts8ZUWcIp9aQv4QyCKUa1EbRTE4Iw'
api_secret = 'NmW0ruph3E8qvg5c9c9ngEgukPVkHKCHYBPE27ZB8UBtD7kvI79JiWQDU7SXbwrF'
client = Client(api_key, api_secret)
dataframe6mois5m = pd.read_pickle("./dataframe6mois5mBTC")
dataframe6mois1m = pd.read_pickle("./dataframe6mois1mBTC")

LCapital = []
Lprice = []
Lindex = []
async def main(filename,backtest,start,end):
    TP = 0.0165
    SL = 0.0012
    file = open(filename, 'w+')
    entryTime = start
    typetrade = 'long'
    #On veut avoir le nombre de trade
    nombreDeTrade = 0
    #Variable pour savoir si le zscore est au dessus de 3 ou en dessous de -3
    Bornes = 0
    #Variable de teste pour savoir si un trade est en cours ou pas
    enCours = False
    Capital = 1000
    longpossibility = False
    shortpossibility = False
    if backtest == 'True':
#
#Truc habituel en dessous:
#
        Gainmoyentrade = 0 
        Winrate = 0 
        #Strategie va etre : sell when zscore < currentMA
        #Close trade when zscore = currentMA
        #Pour simuler le short en gain je vais juste faire prix de sortie-prix d'entrée
        k = Decimal(start)
        back1 = aut.backtest(dataframe6mois5m, dataframe6mois1m, filename,\
        TP, SL, k, end , enCours, Capital, nombreDeTrade, Winrate, Gainmoyentrade, Lindex ,Lprice, LCapital)

        while k < end:
            k+=Decimal(1)
            back1.updateL(back1.Capital,dataframe6mois5m.loc[int(k),'date'],dataframe6mois5m.loc[int(k),'price'])
            # if dataframe6mois5m.loc[int(k),'20Zscore_price'] >= 3:
            #     shortpossibility = True
            # elif dataframe6mois5m.loc[int(k),'20Zscore_price'] <= 1:
            #     shortpossibility = False
            # if dataframe6mois5m.loc[int(k),'20Zscore_price'] <= -3 :
            #     longpossibility = True
            # elif dataframe6mois5m.loc[int(k),'20Zscore_price'] >= -1:
            #     longpossibility = False
            Entryconditionshort = dataframe6mois5m.loc[int(k),'20Zscore_price'] < dataframe6mois5m.loc[int(k) - 1,'20Zscore_price'] and dataframe6mois5m.loc[int(k) - 1 ,'20Zscore_price'] > 2.4
            Entryconditionlong = dataframe6mois5m.loc[int(k),'7SMA_price'] <= dataframe6mois5m.loc[int(k),'20SMA_price'] and longpossibility and dataframe6mois5m.loc[int(k),'20Zscore_price'] > dataframe6mois5m.loc[int(k) - 1,'20Zscore_price']
            if Entryconditionshort and not Entryconditionlong:
                typetrade = 'short'
                back1.automatisation_backtest(TP , SL, typetrade, Entryconditionshort, Entryconditionlong, k, enCours, '5m', Lindex, Lprice, LCapital)
                k = back1.indice
                # shortpossibility = False
            # if Entryconditionlong and not Entryconditionshort:
            #     typetrade = 'long'
            #     back1.automatisation_backtest(TP , SL, typetrade, Entryconditionlong, Entryconditionlong, k, enCours, '5m', Lindex, Lprice, LCapital)
            #     k = back1.indice
            #     longpossibility = False

    Winrate = (back1.Winrate / back1.nombreDeTrade) * 100
    print("nombre de trade: " + str(back1.nombreDeTrade))
    print("gain moyen par trade: " + str(back1.Gainmoyentrade/back1.nombreDeTrade))
    print("Winrate: " + str(Winrate) + "%")
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(Lindex, back1.LCapital)
    ax2.plot(Lindex,Lprice)
    plt.show()


# a = input("Entrez nom_du_fichier.json : ")
# b = input("backtestet ? (True or False) : ")
# debut = int(input("indice du début de 0 à 53200 : "))
# fin = int(input("indice de fin, doit être supérieur à indice de début : "))
# asyncio.run(main(a,b,debut,fin))

asyncio.run(main('essai1.json' ,'True',100,67000))

#
#cas du bot stratégie 1 
#
# if dataframe6mois5m.loc[int(k),'20Zscore_price'] >= 3:
#    shortpossibility = True
#if dataframe6mois5m.loc[int(k),'20Zscore_price'] <= -3:
#    longpossibility = True
#Entryconditionshort = shortpossibility and dataframe6mois5m.loc[int(k),'20Zscore_price'] < dataframe6mois5m.loc[int(k) - 1, '20Zscore_price'] and dataframe6mois5m.loc[int(k),'20Zscore_price'] < dataframe6mois5m.loc[int(k), '20SMA_20Zscore_price']
#Entryconditionlong = longpossibility and dataframe6mois5m.loc[int(k),'20Zscore_price'] > dataframe6mois5m.loc[int(k) - 1, '20Zscore_price'] and dataframe6mois5m.loc[int(k),'20Zscore_price'] > dataframe6mois5m.loc[int(k), '20SMA_20Zscore_price']

#
#Cas du bot stratégie 2 
#
# if dataframe6mois5m.loc[int(k),'20Zscore_price'] >= 3:
#     shortpossibility = True
# elif dataframe6mois5m.loc[int(k),'20Zscore_price'] <= 1:
#     shortpossibility = False
# if dataframe6mois5m.loc[int(k),'20Zscore_price'] <= -3 :
#     longpossibility = True
# elif dataframe6mois5m.loc[int(k),'20Zscore_price'] >= -1:
#     longpossibility = False
# Entryconditionshort = dataframe6mois5m.loc[int(k),'7SMA_price'] >= dataframe6mois5m.loc[int(k),'20SMA_price'] and shortpossibility and dataframe6mois5m.loc[int(k),'20Zscore_price'] < dataframe6mois5m.loc[int(k) - 1,'20Zscore_price']
# Entryconditionlong = dataframe6mois5m.loc[int(k),'7SMA_price'] <= dataframe6mois5m.loc[int(k),'20SMA_price'] and longpossibility and dataframe6mois5m.loc[int(k),'20Zscore_price'] > dataframe6mois5m.loc[int(k) - 1,'20Zscore_price']