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

LCapital = [1000]
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
        Entryprice = 0
        LzScore = [dataframe6mois5m.loc[start,'zscore']]
        LzScoreMA = [dataframe6mois5m.loc[start,'zscoreMA']]
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
            LzScore.append(dataframe6mois5m.loc[int(k),'zscore'])
            LzScoreMA.append(dataframe6mois5m.loc[int(k),'zscoreMA'])
            back1.updateLcapital(back1.Capital)
            Entryconditionshort = dataframe6mois5m.loc[int(k)-1,'zscore'] >= 2.4 and dataframe6mois5m.loc[int(k),'zscore'] < dataframe6mois5m.loc[int(k) - 1, 'zscore']
            Entryconditionlong = dataframe6mois5m.loc[int(k)-1,'zscore'] <= -2.4 and dataframe6mois5m.loc[int(k),'zscore'] > dataframe6mois5m.loc[int(k) - 1, 'zscore']
            Outcondition = dataframe6mois5m.loc[int(k)-1,'zscore'] > -2.4
            if Entryconditionshort == True:
                typetrade = 'short'
            back1.automatisation_backtest(typetrade, Entryconditionshort, Outcondition, k, enCours, Lindex, Lprice, LCapital)
            k = back1.indice

    Winrate = (back1.Winrate / back1.nombreDeTrade) * 100
    print("nombre de trade: " + str(back1.nombreDeTrade))
    print("gain moyen par trade: " + str(back1.Gainmoyentrade/back1.nombreDeTrade))
    print("Winrate: " + str(Winrate) + "%")
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(Selecttime(dataframe6mois5m,start, end), back1.LCapital)
    ax2.plot(Lindex,Lprice)
    plt.show()


# a = input("Entrez nom_du_fichier.json : ")
# b = input("backtestet ? (True or False) : ")
# debut = int(input("indice du début de 0 à 53200 : "))
# fin = int(input("indice de fin, doit être supérieur à indice de début : "))
# asyncio.run(main(a,b,debut,fin))

asyncio.run(main('essai1.json' ,'True',60000,60960))