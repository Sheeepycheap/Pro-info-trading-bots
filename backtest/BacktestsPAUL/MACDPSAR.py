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
dataframe6mois5m = pd.read_pickle("./dataframe6mois5m.pkl")
dataframe6mois1m = pd.read_pickle("./dataframe6mois1m.pkl")
dataframe6mois4hBTC = pd.read_pickle("./dataframe6mois4hBTC")
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
        back2 = aut.backtest(dataframe6mois4hBTC, dataframe6mois1m, filename,\
        TP, SL,  int(k), end , enCours, Capital, nombreDeTrade, Winrate, Gainmoyentrade, Lindex ,Lprice, LCapital)
        while k < end:
            k+=Decimal(1)
            back2.updateL(back2.Capital,dataframe6mois4hBTC.loc[int(k),'date'],dataframe6mois4hBTC.loc[int(k),'price'])
            Entryconditionshort = dataframe6mois4hBTC.loc[int(k),'MACD'] < 0  and  dataframe6mois4hBTC.loc[int(k),'PSARdir'] == "bear"
            Entryconditionlong = dataframe6mois4hBTC.loc[int(k),'MACD'] > 0  and  dataframe6mois4hBTC.loc[int(k),'PSARdir'] == "bull"
            a = int(k)
            Outcondition =  dataframe6mois4hBTC.loc[a,'PSARdir'] == "bull"
            # if Entryconditionshort and not Entryconditionlong:
            #     typetrade = 'short'
            #     back2.automatisation_backtest_nonmonitored(typetrade, Entryconditionshort, Outcondition, int(k), enCours, Lindex, Lprice, LCapital)
            #     k = back2.indice
            if Entryconditionlong and not Entryconditionshort:
                typetrade = 'long'
                back2.automatisation_backtest_nonmonitored(typetrade, Entryconditionlong, Outcondition, int(k), enCours, Lindex, Lprice, LCapital)
                k = back2.indice
            

    Winrate = (back2.Winrate / back2.nombreDeTrade) * 100
    print("nombre de trade: " + str(back2.nombreDeTrade))
    print("gain moyen par trade: " + str(back2.Gainmoyentrade/back2.nombreDeTrade))
    print("Winrate: " + str(Winrate) + "%")
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(back2.Lindex, back2.LCapital)
    ax2.plot(back2.Lindex,back2.Lprice)
    plt.show()

asyncio.run(main('essai1.json' ,'True',100,1370))